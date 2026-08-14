#!/usr/bin/env Rscript

# Install the packages used by the Metabo-Diet R companion and its QA test.
# Run from the directory that contains module/:
#
#   Rscript module/notebooks/install_r_packages.R

minimum_r <- "4.3.0"
if (getRversion() < minimum_r) {
  stop(
    "Metabo-Diet requires R ", minimum_r, " or later; found ",
    as.character(getRversion()), "."
  )
}

cran_repository <- "https://cloud.r-project.org"
cran_packages <- c("rmarkdown", "knitr", "jsonlite", "data.table", "httr")
missing_cran <- cran_packages[
  !vapply(cran_packages, requireNamespace, quietly = TRUE, FUN.VALUE = logical(1))
]

if (length(missing_cran)) {
  install.packages(missing_cran, repos = cran_repository)
}

if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager", repos = cran_repository)
}

if (!requireNamespace("metabolomicsWorkbenchR", quietly = TRUE)) {
  BiocManager::install("metabolomicsWorkbenchR", ask = FALSE, update = FALSE)
}

required_packages <- c(cran_packages, "BiocManager", "metabolomicsWorkbenchR")
status <- vapply(
  required_packages,
  function(package) {
    if (!requireNamespace(package, quietly = TRUE)) return("MISSING")
    as.character(utils::packageVersion(package))
  },
  FUN.VALUE = character(1)
)

cat("R", as.character(getRversion()), "package check\n")
for (package in names(status)) {
  cat("  ", package, "==", status[[package]], "\n", sep = "")
}

if (any(status == "MISSING")) {
  stop("One or more required R packages could not be installed.")
}

cat("Metabo-Diet R environment check passed.\n")
