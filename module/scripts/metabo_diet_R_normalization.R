# Canonicalize metabolomicsWorkbenchR and cached REST outputs.
#
# The Bioconductor client intentionally reshapes several study endpoints:
# - flat endpoints become data.frames;
# - factors becomes a study-keyed list of data.frames with the original factor
#   string removed and expanded factor columns appended;
# - data becomes an analysis-keyed list of data.frames with DATA sample values
#   flattened into columns (and non-syntactic sample IDs altered by data.frame).
#
# These helpers convert both paths to one internal contract: summary is one
# named record; every other endpoint is a list of named row records; quantitative
# records contain a named DATA list using the original factor-table sample IDs.

MW_CANONICAL_ENDPOINTS <- c("summary", "factors", "analysis", "metabolites", "data")

MW_CANONICAL_REQUIRED <- list(
  summary = c("study_id", "study_title"),
  factors = c("study_id", "local_sample_id", "sample_source", "factors"),
  analysis = c("study_id", "analysis_id", "analysis_summary", "analysis_type"),
  metabolites = c(
    "study_id", "analysis_id", "analysis_summary", "metabolite_name", "refmet_name"
  ),
  data = c(
    "study_id", "analysis_id", "analysis_summary", "metabolite_name",
    "metabolite_id", "refmet_name", "units", "DATA"
  )
)

MW_FACTOR_BASE_COLUMNS <- c(
  "study_id", "local_sample_id", "subject_type", "sample_source",
  "mb_sample_id", "raw_data"
)

MW_DATA_METADATA_COLUMNS <- c(
  "study_id", "analysis_id", "analysis_summary", "metabolite_name",
  "metabolite_id", "refmet_name", "units"
)


mw_clean_name <- function(value) {
  value <- tolower(as.character(value))
  value <- gsub("([[:punct:]])|\\s+", "_", value)
  value <- gsub("_+", "_", value)
  gsub("^_|_$", "", value)
}


mw_scalar <- function(value) {
  if (is.factor(value)) value <- as.character(value)
  while (is.list(value) && length(value) == 1L) value <- value[[1L]]
  if (length(value) == 0L || is.null(value)) return(NA)
  if (length(value) != 1L) stop("Expected one scalar value; got length ", length(value))
  if (is.factor(value)) value <- as.character(value)
  unname(value)
}


mw_frame_row <- function(frame, index) {
  if (!is.data.frame(frame)) stop("Expected a data.frame")
  values <- lapply(seq_along(frame), function(column) {
    value <- if (is.list(frame[[column]])) frame[[column]][[index]] else frame[[column]][index]
    mw_scalar(value)
  })
  names(values) <- mw_clean_name(names(frame))
  values
}


mw_normalize_record <- function(record) {
  if (!is.list(record) || is.data.frame(record)) stop("Expected one named record list")
  original_names <- names(record)
  if (is.null(original_names)) stop("Canonical records must be named")
  clean_names <- mw_clean_name(original_names)
  output <- list()
  for (index in seq_along(record)) {
    name <- clean_names[index]
    value <- record[[index]]
    if (identical(name, "data") && is.list(value)) {
      data_values <- lapply(value, mw_scalar)
      names(data_values) <- names(value)
      output[["DATA"]] <- data_values
    } else {
      output[[name]] <- mw_scalar(value)
    }
  }
  output
}


mw_is_raw_record_collection <- function(payload, endpoint) {
  if (!is.list(payload) || is.data.frame(payload) || length(payload) == 0L) return(FALSE)
  required <- MW_CANONICAL_REQUIRED[[endpoint]]
  all(vapply(payload, function(record) {
    if (!is.list(record) || is.data.frame(record) || is.null(names(record))) return(FALSE)
    names_clean <- mw_clean_name(names(record))
    if (endpoint == "data") names_clean[names_clean == "data"] <- "DATA"
    all(required %in% names_clean)
  }, logical(1)))
}


mw_flat_records <- function(payload, endpoint) {
  if (is.data.frame(payload)) {
    return(lapply(seq_len(nrow(payload)), function(index) mw_frame_row(payload, index)))
  }
  if (mw_is_raw_record_collection(payload, endpoint)) {
    return(unname(lapply(payload, mw_normalize_record)))
  }
  if (is.list(payload) && length(payload) > 0L &&
      all(vapply(payload, is.data.frame, logical(1)))) {
    return(unlist(lapply(payload, function(frame) {
      lapply(seq_len(nrow(frame)), function(index) mw_frame_row(frame, index))
    }), recursive = FALSE, use.names = FALSE))
  }
  stop("Unsupported ", endpoint, " output shape: ", paste(class(payload), collapse = "/"))
}


mw_normalize_summary <- function(payload) {
  if (is.data.frame(payload)) {
    if (nrow(payload) != 1L) stop("Study-ID summary query must return exactly one row")
    return(mw_frame_row(payload, 1L))
  }
  if (is.list(payload) && !is.data.frame(payload) && !is.null(names(payload)) &&
      "study_id" %in% mw_clean_name(names(payload))) {
    return(mw_normalize_record(payload))
  }
  if (mw_is_raw_record_collection(payload, "summary") && length(payload) == 1L) {
    return(mw_normalize_record(payload[[1L]]))
  }
  stop("Unsupported summary output shape")
}


mw_factor_frames <- function(payload) {
  if (is.data.frame(payload)) return(list(payload))
  if (is.list(payload) && length(payload) > 0L &&
      all(vapply(payload, is.data.frame, logical(1)))) return(unname(payload))
  stop("Expected a data.frame or study-keyed list of factor data.frames")
}


mw_canonical_factor_string <- function(value) {
  parts <- trimws(strsplit(as.character(value), "|", fixed = TRUE)[[1L]])
  normalized <- vapply(parts, function(part) {
    location <- regexpr(":", part, fixed = TRUE)[1L]
    if (location < 1L) stop("Malformed factor component: ", part)
    key <- trimws(substr(part, 1L, location - 1L))
    factor_value <- trimws(substr(part, location + 1L, nchar(part)))
    paste0(key, ":", factor_value)
  }, character(1))
  paste(normalized, collapse = " | ")
}


mw_normalize_factors <- function(payload) {
  if (mw_is_raw_record_collection(payload, "factors")) {
    records <- unname(lapply(payload, mw_normalize_record))
    return(lapply(records, function(record) {
      record$factors <- mw_canonical_factor_string(record$factors)
      record
    }))
  }

  output <- list()
  for (frame in mw_factor_frames(payload)) {
    clean_names <- mw_clean_name(names(frame))
    factor_indexes <- which(!clean_names %in% MW_FACTOR_BASE_COLUMNS)
    if (length(factor_indexes) == 0L) {
      stop("Expanded metabolomicsWorkbenchR factor columns were not found")
    }
    for (row_index in seq_len(nrow(frame))) {
      row <- mw_frame_row(frame, row_index)
      factor_parts <- vapply(factor_indexes, function(column_index) {
        key <- names(frame)[column_index]
        key <- gsub("([[:punct:]])|\\s+", "_", key)
        key <- sub("^_", "", key)
        value <- mw_scalar(
          if (is.list(frame[[column_index]])) frame[[column_index]][[row_index]]
          else frame[[column_index]][row_index]
        )
        if (is.na(value)) value <- "NA"
        paste0(key, ":", as.character(value))
      }, character(1))
      sample_source <- row[["sample_source"]]
      if (is.null(sample_source) || is.na(sample_source) || !nzchar(as.character(sample_source))) {
        sample_source <- row[["subject_type"]]
      }
      record <- list(
        study_id = row[["study_id"]],
        local_sample_id = row[["local_sample_id"]],
        sample_source = sample_source,
        factors = mw_canonical_factor_string(paste(factor_parts, collapse = " | "))
      )
      for (optional in c("mb_sample_id", "raw_data")) {
        if (!is.null(row[[optional]])) record[[optional]] <- row[[optional]]
      }
      output[[length(output) + 1L]] <- record
    }
  }
  output
}


mw_data_frames <- function(payload) {
  if (is.data.frame(payload)) {
    output <- list(payload)
    names(output) <- ""
    return(output)
  }
  if (is.list(payload) && length(payload) > 0L &&
      all(vapply(payload, is.data.frame, logical(1)))) return(payload)
  stop("Expected a data.frame or analysis-keyed list of data.frames")
}


mw_package_sample_name <- function(sample_id) {
  # parse_data() first calls data.frame() on a nested DATA list and only later
  # removes the literal DATA. prefix. Reproduce that transformation exactly.
  sub("DATA.", "", make.names(paste0("DATA.", sample_id)), fixed = TRUE)
}


mw_restore_sample_names <- function(observed_names, expected_sample_ids) {
  if (is.null(expected_sample_ids) || length(expected_sample_ids) == 0L) {
    stop("Expected factor-table sample IDs are required for live data normalization")
  }
  expected_sample_ids <- unique(as.character(expected_sample_ids))
  transformed <- vapply(expected_sample_ids, mw_package_sample_name, character(1))
  if (anyDuplicated(transformed)) {
    stop("Package-style sample-name transformation is not one-to-one")
  }
  transform_map <- stats::setNames(expected_sample_ids, transformed)
  restored <- vapply(observed_names, function(observed) {
    if (observed %in% expected_sample_ids) return(observed)
    if (observed %in% names(transform_map)) return(unname(transform_map[[observed]]))
    stop("Unexpected quantitative sample column after package parsing: ", observed)
  }, character(1))
  if (anyDuplicated(restored)) stop("Restored sample IDs are not unique")
  restored
}


mw_normalize_data <- function(payload, expected_sample_ids = NULL) {
  if (mw_is_raw_record_collection(payload, "data")) {
    records <- unname(lapply(payload, mw_normalize_record))
    if (!is.null(expected_sample_ids) && length(expected_sample_ids) > 0L) {
      expected_sample_ids <- unique(as.character(expected_sample_ids))
      records <- lapply(records, function(record) {
        unexpected <- setdiff(names(record$DATA), expected_sample_ids)
        if (length(unexpected)) {
          stop("Cached DATA contains sample IDs absent from factors: ",
               paste(unexpected, collapse = ", "))
        }
        aligned <- lapply(expected_sample_ids, function(sample_id) {
          value <- record$DATA[[sample_id]]
          if (is.null(value) || length(value) == 0L) NA else mw_scalar(value)
        })
        names(aligned) <- expected_sample_ids
        record$DATA <- aligned
        record
      })
    }
    return(records)
  }

  output <- list()
  frames <- mw_data_frames(payload)
  for (frame_key in names(frames)) {
    frame <- frames[[frame_key]]
    clean_names <- mw_clean_name(names(frame))
    if (!all(MW_DATA_METADATA_COLUMNS %in% clean_names)) {
      stop("Live data frame is missing required metadata columns")
    }
    sample_indexes <- which(!clean_names %in% MW_DATA_METADATA_COLUMNS)
    if (length(sample_indexes) == 0L) stop("Live data frame has no sample columns")
    restored_sample_ids <- mw_restore_sample_names(
      names(frame)[sample_indexes], expected_sample_ids
    )

    for (row_index in seq_len(nrow(frame))) {
      row <- mw_frame_row(frame, row_index)
      record <- row[MW_DATA_METADATA_COLUMNS]
      data_values <- lapply(sample_indexes, function(column_index) {
        value <- if (is.list(frame[[column_index]])) frame[[column_index]][[row_index]]
        else frame[[column_index]][row_index]
        mw_scalar(value)
      })
      names(data_values) <- restored_sample_ids
      # Align to factor-table order so live and cached paths have exactly the
      # same sample universe and ordering, including explicit NA placeholders.
      aligned <- lapply(unique(as.character(expected_sample_ids)), function(sample_id) {
        value <- data_values[[sample_id]]
        if (is.null(value) || length(value) == 0L) NA else mw_scalar(value)
      })
      names(aligned) <- unique(as.character(expected_sample_ids))
      record[["DATA"]] <- aligned
      if (nzchar(frame_key) && !is.na(record$analysis_id) &&
          !identical(as.character(record$analysis_id), frame_key)) {
        stop("Analysis-list key does not match row analysis_id")
      }
      output[[length(output) + 1L]] <- record
    }
  }
  output
}


normalize_mw_endpoint <- function(study_id, endpoint, payload, expected_sample_ids = NULL) {
  if (!endpoint %in% MW_CANONICAL_ENDPOINTS) stop("Unknown endpoint: ", endpoint)
  canonical <- switch(
    endpoint,
    summary = mw_normalize_summary(payload),
    factors = mw_normalize_factors(payload),
    analysis = mw_flat_records(payload, endpoint),
    metabolites = mw_flat_records(payload, endpoint),
    data = mw_normalize_data(payload, expected_sample_ids)
  )
  validate_canonical_mw_payload(study_id, endpoint, canonical)
  canonical
}


validate_canonical_mw_payload <- function(study_id, endpoint, payload) {
  records <- if (endpoint == "summary") list(payload) else payload
  if (!is.list(records) || length(records) == 0L) {
    stop(study_id, "/", endpoint, ": empty canonical payload")
  }
  required <- MW_CANONICAL_REQUIRED[[endpoint]]
  for (index in seq_along(records)) {
    record <- records[[index]]
    missing <- setdiff(required, names(record))
    if (length(missing)) {
      stop(study_id, "/", endpoint, " record ", index,
           ": missing ", paste(missing, collapse = ", "))
    }
    if (!identical(as.character(record$study_id), study_id)) {
      stop(study_id, "/", endpoint, " record ", index, ": study_id mismatch")
    }
    if (endpoint == "data") {
      if (!is.list(record$DATA) || length(record$DATA) == 0L ||
          is.null(names(record$DATA)) || any(names(record$DATA) == "")) {
        stop(study_id, "/data record ", index, ": DATA must be a named nonempty list")
      }
    }
  }
  invisible(TRUE)
}


mw_endpoint_record_count <- function(endpoint, payload) {
  if (endpoint == "summary") 1L else length(payload)
}
