### dependencies
library(shiny)
library(shinyWidgets)

### options
# number of pegs? for now:
pegs <- c(1:8)
# grouping options.

### helpers
# source('helpers/none_yet.R')

# function to create new set partition
new_set <- function(pegs, min_bucket = 2, min_together = 2) {
  # parameters and empty matrix
  n <- length(pegs)
  max_bucket <- floor(n / min_together)
  max_together <- floor(n - ((min_bucket - 1) * min_together))
  final <- matrix(NA, max_together, max_bucket)
  # sampling
  shuffle <- sample(pegs)
  cutoff <- c(1, 1)
  while (cutoff[2] < n) {
    possible <- c(1:(n - cutoff[2] - min_together + 1), (n - cutoff[2] + 1))
    possible <- intersect(possible, min_together:max_together)
    if (length(possible) > 1) {draw <- sample(possible, 1)}
    else {draw <- possible}
    jump <- draw + cutoff[2] - 1
    final[1:draw, cutoff[1]] <- shuffle[cutoff[2]:jump]
    cutoff <- cutoff + c(1, draw)}
  # change to list
  final <- lapply(as.list(as.data.frame(final)),
                  function(x) {sort(x[!is.na(x)])})
  return(final[lapply(final, length) > 0])
}

# function to find max matches for test set with any of correct sets
match_set <- function(test, correct) {
  if (is.null(test)) {return(' ')}
  m_num <- lapply(correct, function(x) {length(intersect(x, test))})
  m_ind <- which.max(unlist(m_num))
  if (setequal(correct[[m_ind]], test)) {return('correct')}
  else {return(as.character(max(unlist(m_num))))}
}

# function to change list of vectors to string for feedback
stringify <- function(l) {
  str_l <- lapply(l, paste, collapse = ', ')
  return(paste(str_l, collapse = ' | '))
}

### panels
# source('panels/none_yet.R')

