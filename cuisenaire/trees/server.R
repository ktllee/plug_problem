# server
function(input, output, session) {
  
  # rod set as coefficient vector
  coefs <- reactive({
    # rods1
    rods1 <- if (input$rods1 == '') {c(1, 1)}
    else {as.numeric(unlist(strsplit(input$rods1, ',')))}

    # coefs
    final <- rep(0, max(rods1))
    for (i in 1:max(rods1)) {final[i] <- sum(rods1 == i)}

    c(rev(-final), 1)
    })

  # growth
  output$growth <- renderText({max(abs(polyroot(coefs())))})
  
  # polynomials
  polys <- reactiveValues()
  
  observe({
    growth <- max(abs(polyroot(coefs())))
    
    # full
    fpoly <- ''
    for (i in 1:length(coefs())) {
      if (coefs()[i] > 0) {
        fpoly <- 
          paste0('+', as.character(coefs()[i]),
                 '*x^', as.character(i - 1), fpoly)}
      if (coefs()[i] < 0) {
        fpoly <- 
          paste0(as.character(coefs()[i]), '*x^', as.character(i - 1), fpoly)}}
    fpoly <- as_sym(fpoly)
    polys$full <- as.character(fpoly)
    
    # # factored
    # factors <- strsplit(as.character(sympy_func(fpoly, 'factor')), ')*(')
    # for (q in factors) {
    #   sympy_func(as_sym(q),'all_coeffs')
    # }
    
    polys$min <- as.character(sympy_func(fpoly, 'factor'))
  })
  
  # send to output
  output$full_poly <- renderText({polys$full})
  output$min_poly <- renderText({polys$min})
  
}