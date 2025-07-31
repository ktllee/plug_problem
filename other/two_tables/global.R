### dependencies
library(shiny)
library(tidyverse)

### options
# none yet

### helpers
# source('helpers/none_yet.R')

pascal <- function(n, n_r2, r1, r2) {
  
  # helper values
  x <- r2 * n_r2
  n_r1 <- (n - (r2 * n_r2)) / r1
  
  sign_r1 <- if (n_r1 %% 2 == 1) {-1} else {1}
  
  # figure out return
  if (n < x) {return(0)}
  else if (n == x) {return(sign_r1)}
  else if ((n - x) %% r1 != 0) {return(0)}
  else {
    n_r1 <- (n - (r2 * n_r2)) / r1
    return(sign_r1 * choose(n_r2 + n_r1, n_r1))}
}

pascal_col <- function(n_r2, r1, r2, max_n) {
  lapply(0:max_n, pascal, n_r2 = n_r2, r1 = r1, r2 = r2)
}

odd_suffix <- function(n) {
  if (n %% 2 == 1) {return(paste0(n, '_odd'))}
  else {return(paste0(n, '_even'))}
}

### panels
# source('panels/none_yet.R')

