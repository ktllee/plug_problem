# ui
# contained in single fluidPage
fluidPage(
  
  # overall title
  titlePanel('Comparing Rod Sets'),
  
  # select rods 1
  textInput(
    'rods1',
    'Base rod lengths',
    width = '90%',
    placeholder = 'Enter values separated by commas...'),
  
  # select rods 2
  textInput(
    'rods2',
    'Base rod lengths',
    width = '90%',
    placeholder = 'Enter values separated by commas...'),
  
  # select rods 3
  textInput(
    'rods3',
    'Base rod lengths',
    width = '90%',
    placeholder = 'Enter values separated by commas...'),
  
  # select rods 4
  textInput(
    'rods4',
    'Base rod lengths',
    width = '90%',
    placeholder = 'Enter values separated by commas...'),
  
  # select rods 5
  textInput(
    'rods5',
    'Base rod lengths',
    width = '90%',
    placeholder = 'Enter values separated by commas...')
  
)