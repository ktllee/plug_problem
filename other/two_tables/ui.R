# ui
fluidPage(
  titlePanel('Tables for Two-Rod Sets'),
  
  # controls
  br(),
  fluidRow(
    column(
      width = 3,
      numericInput('r1', 'first rod length', 1)),
    column(
      width = 3,
      numericInput('r2', 'second rod length', 2)),
    column(width = 4),
    column(
      width = 2,
      actionButton('submit', 'calculate'))
    ),
  fluidRow(
    column(
      width = 3,
      numericInput('maxn', 'max n (rows)', 20)),
    column(
      width = 3,
      numericInput('maxr2', 'max # of second rod (cols)', 6))
    ),
  br(),
  
  # tables
  tableOutput('table')
)