# server
function(input, output, session) {
  
  # rod set as coefficient vector
  rods <- reactive({
    if (input$rods == '') {c('0')}
    else {unlist(strsplit(input$rods, ','))}
    })
  
  # show rods
  output$rods <- renderPrint(rods())
  
  # # polynomials
  # output$fullpoly <- renderPrint('in progress')
  # output$facpoly <- renderPrint('in progress')
  
  ### initial network
  # nodes and edges from base rod set
  root <- reactiveValues()
  observe({
    root$nodes <- 
      data.frame(id = c('R', paste0('R', rods(), '.')),
                 label = c('ROOT', as.numeric(rods())),
                 shape = 'circle',
                 font.size = c(5, rep(20, length(rods()))))
    root$edges <- 
      data.frame(id = paste0('R', rods(), '.'),
                 from = rep('R', length(rods())),
                 to = paste0('R', rods(), '.'))
  })
  
  # output network
  output$tree <- renderVisNetwork({
    visNetwork(root$nodes, root$edges) %>% 
      visHierarchicalLayout(sortMethod = 'directed') %>% 
      visInteraction(dragNodes = F, 
                     dragView = F, 
                     zoomView = F) %>% 
      visEvents(click = "function(nodes){
                  Shiny.onInputChange('click', nodes.nodes[0]);
                  ;}")})
  
  # helper to expand nodes
  grow <- function (leaf, root) {
    (abs(leaf) + abs(root)) * sign(leaf * root)}
  
  # debug
  output$nodes <- renderTable(root$nodes)
  output$edges <- renderTable(root$edges)
  
  ### after expand click
  observeEvent(input$expand, {
    # clear error text and get nodes
    output$misaction <- renderText('')
    visNetworkProxy('tree') %>%
      visGetSelectedNodes(input = 'tree_expand')})
  observeEvent(input$tree_expand, {
    root$leaf <- input$tree_expand
    leaf_val <- filter(root$nodes, id %in% root$leaf)[['label']]

    # check node is a leaf
    if (root$leaf %in% root$edges[['from']]) {
      output$misaction <- renderText('Node is already expanded')}
    else {
      # the new nodes
      new_id <- paste0(root$leaf, rods(), '.')
      new_label <- grow(as.numeric(leaf_val), as.numeric(rods()))
      new_nodes <-
        data.frame(id = new_id,
                   label = new_label,
                   shape = 'circle',
                   font.size = 20)
      root$nodes <- rbind(root$nodes, new_nodes)

      # new edges
      new_edges <-
        data.frame(id = paste0(root$leaf, new_id),
                   from = root$leaf,
                   to = new_id)
      root$edges <- rbind(root$edges, new_edges)

      # update graph
      visNetworkProxy('tree') %>%
        visUpdateNodes(nodes = root$nodes)
      visNetworkProxy('tree') %>%
        visUpdateEdges(edges = root$edges)
    }
  })
  
  ### after prune click
  observeEvent(input$prune, {
    # clear error text and get nodes
    output$misaction <- renderText('')
    visNetworkProxy('tree') %>%
      visGetSelectedNodes(input = 'tree_prune')})
  observeEvent(input$tree_prune, {
    
    # find nodes to remove
    prune <- filter(root$edges, from %in% input$tree_prune)[['to']]
    if (identical(prune, integer(0))) {
      output$misaction <- renderText('Nothing to prune.')}
    else {
      edges <- root$edges
      child <- T
      i <- 1
      while (child) {
        behbehs <- filter(edges, from %in% prune)$to
        edges <- filter(edges, !(from %in% prune))
        i <- 1 + i
        if (identical(behbehs, integer(0))) {child <- F}
        else {
          prune <- c(prune, behbehs)}
        if (i > 5) {break} ### ???
      }
      edges <- filter(edges, !(from %in% input$tree_prune))

      # remove nodes
      root$edges <- edges
      root$nodes <- filter(root$nodes, !(id %in% prune))

      # update graph
      visNetworkProxy('tree') %>%
        visUpdateNodes(nodes = root$nodes)
      visNetworkProxy('tree') %>%
        visUpdateEdges(edges = root$edges)
    }
  })
  
  # # option with click instead of buttons to get node
  # observe({
  #   if (length(input$click) == 1) {
  #     visNetworkProxy('tree') %>%
  #       visGetConnectedNodes(id = input$click)}
  # })
  # output$click <- renderPrint(input$tree_connectedNodes)
}