# ui
# contained in single fluidPage
fluidPage(
  
  # overall title
  titlePanel('Testing Trees'),
  
  # select rods
  textInput(
    'rods',
    'Base rod lengths',
    width = '90%',
    placeholder = 'Enter values separated by commas...'),
  
  # outputs and controls
  sidebarLayout(
    
    # sidebar
    sidebarPanel(
      width = 3,
      HTML('Options:'), br(), br(),
      actionButton('expand', 'Expand'), br(),
      actionButton('prune', 'Prune')
    ),
    
    # growth rate, polynomials, etc.
    mainPanel(
      width = 9,
      fluidPage(
        fluidRow(
          column(
            width = 4,
            HTML('Growth rate:'),
            textOutput('growth')),
          column(
            width = 8,
            HTML('Full polynomial:'),
            textOutput('full_poly'))
        ), br(),
        fluidRow(
          column(
            width = 12,
            HTML('Minimal polynomial:'),
            textOutput('min_poly'))
        ),br(),br(),
        fluidRow(visNetworkOutput('graph')))
    ))
  
)