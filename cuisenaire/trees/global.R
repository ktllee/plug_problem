# dependencies
library(shiny)
library(tidyverse)
library(reticulate)

# python modules
py_install(c('numpy', 'sympy'))

# source rods
source_python('rods_r.py')
