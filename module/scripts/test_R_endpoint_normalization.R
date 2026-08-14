#!/usr/bin/env Rscript

# Regression-test canonical endpoint normalization against both cached REST
# JSON and fixtures shaped exactly like metabolomicsWorkbenchR 1.22.0 parsers.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg)) sub("^--file=", "", file_arg[[1L]]) else ""
if (nzchar(script_path) && script_path != "-") {
  MODULE_DIR <- normalizePath(file.path(dirname(script_path), ".."))
} else {
  current <- normalizePath(getwd())
  repeat {
    if (dir.exists(file.path(current, "module", "data", "raw"))) {
      MODULE_DIR <- file.path(current, "module")
      break
    }
    if (dir.exists(file.path(current, "data", "raw")) &&
        dir.exists(file.path(current, "scripts"))) {
      MODULE_DIR <- current
      break
    }
    parent <- dirname(current)
    if (identical(parent, current)) stop("Could not locate module directory")
    current <- parent
  }
}
RAW_DIR <- file.path(MODULE_DIR, "data", "raw")

source(file.path(MODULE_DIR, "scripts", "metabo_diet_R_normalization.R"))

STUDIES <- c("ST001521", "ST003348")
ENDPOINTS <- c("summary", "factors", "analysis", "metabolites", "data")


read_raw <- function(study_id, endpoint) {
  jsonlite::fromJSON(
    file.path(RAW_DIR, paste0(study_id, "_", endpoint, ".json")),
    simplifyVector = FALSE
  )
}


fixture_flat_frame <- function(payload, endpoint) {
  if (endpoint == "summary") {
    return(as.data.frame(lapply(payload, mw_scalar), stringsAsFactors = FALSE))
  }
  records <- unname(payload)
  data.table::rbindlist(lapply(records, function(record) {
    as.data.frame(lapply(record, mw_scalar), stringsAsFactors = FALSE)
  }), fill = TRUE) |>
    as.data.frame()
}


# Mirror metabolomicsWorkbenchR::parse_factors(): split factor strings, append
# factor columns, remove the original factor string, and key frames by study ID.
fixture_factors <- function(payload) {
  flat <- fixture_flat_frame(payload, "factors")
  output <- list()
  for (study_id in unique(flat$study_id)) {
    frame <- flat[flat$study_id == study_id, , drop = FALSE]
    parsed <- lapply(frame$factors, function(value) {
      parts <- strsplit(value, "|", fixed = TRUE)[[1L]]
      values <- lapply(parts, function(part) {
        at_colon <- strsplit(part, ":", fixed = TRUE)[[1L]]
        key <- gsub("([[:punct:]])|\\s+", "_", at_colon[[1L]])
        if (substr(key, 1L, 1L) == "_") key <- substring(key, 2L)
        stats::setNames(trimws(at_colon[[2L]]), key)
      })
      unlist(values)
    })
    factor_names <- unique(unlist(lapply(parsed, names)))
    expanded <- as.data.frame(lapply(factor_names, function(key) {
      factor(vapply(parsed, function(values) {
        value <- values[[key]]
        if (is.null(value)) NA_character_ else value
      }, character(1)))
    }))
    names(expanded) <- factor_names
    frame$factors <- NULL
    output[[study_id]] <- cbind(frame, expanded)
  }
  output
}


# Mirror metabolomicsWorkbenchR::parse_data(): data.frame() flattens DATA and
# sanitizes sample column names, rbindlist() unions columns, and results split by
# analysis_id. This intentionally produces `9002.3.PA` from `9002-3-PA`.
fixture_data <- function(payload) {
  records <- lapply(unname(payload), function(record) {
    record$DATA <- lapply(record$DATA, function(value) {
      if (is.null(value)) NA else value
    })
    record
  })
  flattened <- lapply(records, data.frame)
  combined <- data.table::rbindlist(flattened, fill = TRUE)
  names(combined) <- gsub("DATA.", "", names(combined), fixed = TRUE)
  combined <- as.data.frame(combined)
  combined[8:ncol(combined)] <- lapply(combined[8:ncol(combined)], as.numeric)
  analyses <- unique(combined$analysis_id)
  stats::setNames(
    lapply(analyses, function(analysis_id) {
      combined[combined$analysis_id == analysis_id, , drop = FALSE]
    }),
    analyses
  )
}


package_fixture <- function(payload, endpoint) {
  switch(
    endpoint,
    summary = fixture_flat_frame(payload, endpoint),
    factors = fixture_factors(payload),
    analysis = fixture_flat_frame(payload, endpoint),
    metabolites = fixture_flat_frame(payload, endpoint),
    data = fixture_data(payload)
  )
}


character_or_na <- function(value) {
  if (length(value) == 0L || is.null(value) || is.na(value)) NA_character_
  else as.character(value)
}


compare_canonical <- function(study_id, endpoint, cached, package) {
  if (endpoint == "summary") {
    fields <- MW_CANONICAL_REQUIRED$summary
    stopifnot(all(vapply(fields, function(field) {
      identical(character_or_na(cached[[field]]), character_or_na(package[[field]]))
    }, logical(1))))
    return(invisible(TRUE))
  }

  stopifnot(length(cached) == length(package))
  metadata <- setdiff(MW_CANONICAL_REQUIRED[[endpoint]], "DATA")
  for (index in seq_along(cached)) {
    for (field in metadata) {
      cached_value <- character_or_na(cached[[index]][[field]])
      package_value <- character_or_na(package[[index]][[field]])
      if (!identical(cached_value, package_value)) {
        stop(
          study_id, "/", endpoint, " record ", index, " field ", field,
          " differs: cache=", cached_value, ", package=", package_value
        )
      }
    }
    if (endpoint == "data") {
      cached_data <- cached[[index]]$DATA
      package_data <- package[[index]]$DATA
      stopifnot(identical(names(cached_data), names(package_data)))
      cached_values <- vapply(cached_data, function(value) as.numeric(mw_scalar(value)), numeric(1))
      package_values <- vapply(package_data, function(value) as.numeric(mw_scalar(value)), numeric(1))
      stopifnot(isTRUE(all.equal(cached_values, package_values, tolerance = 0)))
    }
  }
  invisible(TRUE)
}


results <- list()
cached_by_study <- list()
for (study_id in STUDIES) {
  raw_payloads <- stats::setNames(lapply(ENDPOINTS, function(endpoint) {
    read_raw(study_id, endpoint)
  }), ENDPOINTS)

  cached_canonical <- list()
  fixture_canonical <- list()
  for (endpoint in ENDPOINTS) {
    expected_sample_ids <- NULL
    if (endpoint == "data") {
      expected_sample_ids <- vapply(
        cached_canonical$factors,
        function(record) as.character(record$local_sample_id),
        character(1)
      )
    }
    cached_canonical[[endpoint]] <- normalize_mw_endpoint(
      study_id, endpoint, raw_payloads[[endpoint]], expected_sample_ids
    )
    shaped <- package_fixture(raw_payloads[[endpoint]], endpoint)
    fixture_canonical[[endpoint]] <- normalize_mw_endpoint(
      study_id, endpoint, shaped, expected_sample_ids
    )
    compare_canonical(
      study_id, endpoint, cached_canonical[[endpoint]], fixture_canonical[[endpoint]]
    )
    results[[length(results) + 1L]] <- data.frame(
      study_id = study_id,
      endpoint = endpoint,
      cached_records = mw_endpoint_record_count(endpoint, cached_canonical[[endpoint]]),
      package_fixture_records = mw_endpoint_record_count(endpoint, fixture_canonical[[endpoint]]),
      canonical_equal = TRUE
    )
  }

  factor_ids <- vapply(cached_canonical$factors, `[[`, character(1), "local_sample_id")
  data_sample_ids <- names(cached_canonical$data[[1L]]$DATA)
  stopifnot(identical(factor_ids, data_sample_ids))
  if (study_id == "ST001521") {
    fixture_columns <- names(package_fixture(raw_payloads$data, "data")[[1L]])
    stopifnot("9002.3.PA" %in% fixture_columns)
    stopifnot("9002-3-PA" %in% names(fixture_canonical$data[[1L]]$DATA))
  }
  cached_by_study[[study_id]] <- cached_canonical
}

results <- do.call(rbind, results)
stopifnot(nrow(results) == 10L, all(results$canonical_equal))
print(results, row.names = FALSE)
cat("PASS: cached and metabolomicsWorkbenchR-shaped fixtures canonicalize identically for all 10 endpoints.\n")


# Optional integration test against live REST responses parsed by the official
# Bioconductor parse_fcns.R implementation. This avoids modifying the immutable
# cache and does not require loading the package's unrelated experiment classes.
if (identical(Sys.getenv("METABO_DIET_TEST_LIVE", "0"), "1")) {
  parser_source <- Sys.getenv("MWR_PARSE_SOURCE", "")
  if (!file.exists(parser_source)) {
    stop("Set MWR_PARSE_SOURCE to the official metabolomicsWorkbenchR R/parse_fcns.R")
  }
  source(parser_source)
  official_fields <- list(
    summary = c("study_id", "study_title", "study_type", "institute"),
    factors = c("study_id", "local_sample_id", "subject_type", "factors"),
    analysis = c("study_id", "analysis_id", "analysis_summary", "analysis_type"),
    metabolites = c(
      "study_id", "analysis_id", "analysis_summary", "metabolite_name", "refmet_name"
    ),
    data = c(
      "study_id", "analysis_id", "analysis_summary", "metabolite_name",
      "metabolite_id", "refmet_name", "units", "data"
    )
  )
  official_parser <- list(
    summary = parse_data_frame,
    factors = parse_factors,
    analysis = parse_data_frame,
    metabolites = parse_data_frame,
    data = parse_data
  )
  live_results <- list()
  for (study_id in STUDIES) {
    live_canonical <- list()
    for (endpoint in ENDPOINTS) {
      url <- paste(
        "https://www.metabolomicsworkbench.org/rest/study/study_id",
        study_id, endpoint, sep = "/"
      )
      response <- httr::GET(url)
      httr::stop_for_status(response)
      shaped <- official_parser[[endpoint]](
        response,
        list(fields = official_fields[[endpoint]]),
        study_id
      )
      expected_sample_ids <- NULL
      if (endpoint == "data") {
        expected_sample_ids <- vapply(
          live_canonical$factors,
          function(record) as.character(record$local_sample_id),
          character(1)
        )
      }
      live_canonical[[endpoint]] <- normalize_mw_endpoint(
        study_id, endpoint, shaped, expected_sample_ids
      )
      compare_canonical(
        study_id, endpoint, cached_by_study[[study_id]][[endpoint]],
        live_canonical[[endpoint]]
      )
      live_results[[length(live_results) + 1L]] <- data.frame(
        study_id = study_id,
        endpoint = endpoint,
        official_parser_records = mw_endpoint_record_count(endpoint, live_canonical[[endpoint]]),
        equals_cached_canonical = TRUE
      )
    }
  }
  live_results <- do.call(rbind, live_results)
  print(live_results, row.names = FALSE)
  cat("PASS: official Bioconductor parsers on live REST responses match cached canonical data for all 10 endpoints.\n")
}
