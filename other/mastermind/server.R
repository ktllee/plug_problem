# server
function(input, output, session) {
  
  # annoyed with first setup
  updateTabsetPanel(session, 'page', selected = 'setup2')
  
  ##### inputs and setup
  ### start game
  # set
  initial_set <- new_set(pegs)
  set <- reactiveValues(set = initial_set, string = stringify(initial_set))
  # guesses
  feedback <- reactiveValues(
    history_setup1 = 'Guess History:',
    history = 'Guess History:',
    group1 = ' ',
    group2 = ' ',
    group3 = ' ',
    group4 = ' ')
  
  ### restart game
  observeEvent(input$restart, {
    set$set <- new_set(pegs)
    set$string <- stringify(set$set)
    feedback$history_setup1 <- 'Guess History:'
    feedback$history <- 'Guess History:'
    feedback$group1 <- ' '
    feedback$group2 <- ' '
    feedback$group3 <- ' '
    feedback$group4 <- ' '
    
    updateCheckboxGroupButtons(
      session, 'group1', choices = pegs, selected = NULL)
    updateCheckboxGroupButtons(
      session, 'group2', choices = pegs, selected = NULL)
    updateCheckboxGroupButtons(
      session, 'group3', choices = pegs, selected = NULL)
    updateCheckboxGroupButtons(
      session, 'group4', choices = pegs, selected = NULL)
    })
  
  # setup 1 - guesses and history at bottom
  observeEvent(input$submit, {
    guess <- list(input$group1_setup1, input$group2_setup1,
                  input$group3_setup1, input$group4_setup1)
    guess <- lapply(guess[-which(sapply(guess, is.null))], sort)
    
    # feedback
    correct <- 
      paste(lapply(guess, match_set, correct = set$set), collapse = ', ') 
    new_feed <- paste(stringify(guess), "->", correct)
    feedback$history_setup1 <- paste(feedback$history, new_feed, sep = "\n")
  })
  
  # setup 2 - direct feedback alongside
  observeEvent(input$submit, {
    # individual feedback
    feedback$group1 <- match_set(input$group1, set$set)
    feedback$group2 <- match_set(input$group2, set$set)
    feedback$group3 <- match_set(input$group3, set$set)
    feedback$group4 <- match_set(input$group4, set$set)
    
    # as a whole
    guess <- list(input$group1, input$group2, input$group3, input$group4, NULL)
    # feedback$debug <- guess
    guess <- lapply(guess[-which(sapply(guess, is.null))], sort)
    correct <- 
      c(feedback$group1, feedback$group2, feedback$group3, feedback$group4)
    correct <- paste(correct[correct != ' '], collapse = ', ')
    new_feed <- paste(stringify(guess), "->", correct)
    feedback$history <- paste(feedback$history, new_feed, sep = "\n")
  })
  
  ##### outputs
  ### setup 1
  output$feedback_setup1 <- renderText({feedback$history_setup1})
  ### setup 2
  output$history <- renderText({feedback$history})
  output$feedback1 <- renderText({feedback$group1})
  output$feedback2 <- renderText({feedback$group2})
  output$feedback3 <- renderText({feedback$group3})
  output$feedback4 <- renderText({feedback$group4})

  ### debuggers
  # output$debug_guess <- renderPrint({feedback$debug})
  # output$debug_setup1 <- renderPrint({set$set})
  # output$debug_setup2 <- renderPrint({set$set})
}