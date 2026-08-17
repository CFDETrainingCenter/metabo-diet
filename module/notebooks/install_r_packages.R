#!/usr/bin/env Rscript

# Install the packages used by the Metabo-Diet R companion and its QA test.
# Run from the directory that contains module/:
#
#   Rscript module/notebooks/install_r_packages.R
#
# Add --live only when you intend to install metabolomicsWorkbenchR and test
# the optional live API path.

minimum_r <- "4.3.0"
if (getRversion() < minimum_r) {
  stop(
    "Metabo-Diet requires R ", minimum_r, " or later; found ",
    as.character(getRversion()), "."
  )
}

cran_repository <- "https://cloud.r-project.org"
cran_packages <- c("rmarkdown", "knitr", "jsonlite", "data.table", "httr")
arguments <- commandArgs(trailingOnly = TRUE)
install_live_packages <- "--live" %in% arguments ||
  identical(Sys.getenv("METABO_DIET_INSTALL_LIVE", "0"), "1")
missing_cran <- cran_packages[
  !vapply(cran_packages, requireNamespace, quietly = TRUE, FUN.VALUE = logical(1))
]

if (length(missing_cran)) {
  install.packages(missing_cran, repos = cran_repository)
}

if (install_live_packages) {
  if (!requireNamespace("BiocManager", quietly = TRUE)) {
    install.packages("BiocManager", repos = cran_repository)
  }
  if (!requireNamespace("metabolomicsWorkbenchR", quietly = TRUE)) {
    BiocManager::install("metabolomicsWorkbenchR", ask = FALSE, update = FALSE)
  }
}

required_packages <- cran_packages
if (install_live_packages) {
  required_packages <- c(required_packages, "BiocManager", "metabolomicsWorkbenchR")
}
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
if (!install_live_packages) {
  cat("Live retrieval packages were not requested. Use --live only when testing live retrieval.\n")
}
