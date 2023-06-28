# ui
fluidPage(
  
  # overall title
  # titlePanel('Trees??'),
  br(),
  
  # select rods
  textInput(
    'rods',
    'Rod Lengths',
    width = '100%',
    placeholder = 
      'Enter values separated by commas.  Format antirods as -{length}.'),
  br(),
  
  # debug rod entry
  HTML('[DEBUG] Rods: '),
  textOutput('rods'),
  br(),
  
  # # polynomial
  # HTML('Full Polynomial: '),
  # textOutput('fullpoly'),
  # br(),
  # HTML('Factored Polynomial: '),
  # textOutput('facpoly'),
  # br(),
  
  # tree
  HTML('Select a node then click below to expand or prune.'),
  br(),
  actionButton('expand', 'Expand Leaf'),
  actionButton('prune', 'Prune Lower Leaves'),
  br(),
  span(textOutput('misaction'), style = "color:red"),
  visNetworkOutput('tree'),
  br(),
  
  # debug nodes and edges
  HTML('[DEBUG] Nodes: '),
  tableOutput('nodes'),
  br(),
  HTML('[DEBUG] Edges:'),
  tableOutput('edges')
)