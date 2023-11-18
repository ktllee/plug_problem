# ui
fluidPage(
  titlePanel('Set Partition Game?'),
  
  # overall control buttons
  br(),
  fluidRow(
    column(
      width = 10,
      actionButton('restart', 'Restart Game')),
    column(
      width = 2,
      actionButton('submit', 'Submit Guess')
    )),
  br(),
  
  tabsetPanel(
    id = 'page',
    tabPanel(
      'setup1',
             
      fluidPage(
        
        # select group members
        br(), br(),
        selectizeInput(
          inputId = 'group1_setup1',
          label = NULL,
          width = '100%',
          multiple = T,
          choices = pegs,
          options = list(placeholder = 'Select members for this bucket.')),
        br(),
        
        br(),
        selectizeInput(
          inputId = 'group2_setup1',
          label = NULL,
          width = '100%',
          multiple = T,
          choices = pegs,
          options = list(placeholder = 'Select members for this bucket.')),
        br(),
        
        br(),
        selectizeInput(
          inputId = 'group3_setup1',
          label = NULL,
          width = '100%',
          multiple = T,
          choices = pegs,
          options = list(placeholder = 'Select members for this bucket.')),
        br(),
        
        br(),
        selectizeInput(
          inputId = 'group4_setup1',
          label = NULL,
          width = '100%',
          multiple = T,
          choices = pegs,
          options = list(placeholder = 'Select members for this bucket.')),
        br(),
        
        verbatimTextOutput('feedback_setup1'),
        
        br(),
        textOutput('debug_setup1')
      )),
    
    tabPanel(
      'setup2',
      
      fluidPage(
 
        fluidRow(
          column(
            width = 6,
            
            # select group members
            br(), HTML('<b>Guess</b>'), br(), br(), HTML('Bucket 1'),
            checkboxGroupButtons(
              inputId = 'group1',
              label = NULL,
              individual = T,
              choices = pegs),
            br(),
            
            br(), HTML('Bucket 2'),
            checkboxGroupButtons(
              inputId = 'group2',
              label = NULL,
              individual = T,
              choices = pegs),
            br(),
            
            br(), HTML('Bucket 3'),
            checkboxGroupButtons(
              inputId = 'group3',
              label = NULL,
              individual = T,
              choices = pegs),
            br(),
            
            br(), HTML('Bucket 4'),
            checkboxGroupButtons(
              inputId = 'group4',
              label = NULL,
              individual = T,
              choices = pegs),
            br()),
          
          # feedback
          column(
            width = 6,
            
            br(), HTML('<b>Feedback</b>'), br(), br(), br(),
            verbatimTextOutput('feedback1'),
            
            br(), br(), br(),
            verbatimTextOutput('feedback2'),
            
            br(), br(), br(),
            verbatimTextOutput('feedback3'),
            
            br(), br(), br(),
            verbatimTextOutput('feedback4'),
            
            br(), br(),
            textOutput('debug_setup2'))),
        
        verbatimTextOutput('debug_guess'),
        verbatimTextOutput('history')
        )),
    
    tabPanel(
      'notes',
      fluidPage(
        br(), br(),
        HTML('Select each option only once.  Use all options.'),
        br(), br(),
        HTML("It doesn't matter which bucket any subset is entered in."),
        br(), br(),
        HTML('The feedback reads "correct" when a subset is correct.')
      )
  ))
)