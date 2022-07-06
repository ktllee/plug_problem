# server
function(input, output, session) {
  
  # rod set as coefficient vector
  coefs <- reactive({
    # rods
    rods <- if (input$rods == '') {c(1, 1)}
    else {sort(as.numeric(unlist(strsplit(input$rods, ','))))}

    # coefs
    final <- rep(0, max(rods))
    for (i in 1:max(rods)) {final[i] <- sum(rods == i)}

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
  
  
  # network
  dat <- read_csv('example.txt')
  fib <- graph_from_data_frame(dat)
  output$graph <- renderVisNetwork({
    visIgraph(fib) %>% 
      visOptions(highlightNearest = T, nodesIdSelection = T) %>% 
      visIgraphLayout(layout = 'layout_as_tree') %>%
      visNodes(color = list(background = "blue", highlight = 'red'))
  })
  
  
  
  
}