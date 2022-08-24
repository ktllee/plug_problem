# helpers - for growth, equations, etc.

# quick and small example
dat <- read_csv('cuisenaire/trees/example.txt')
fib <- graph_from_data_frame(dat)
visIgraph(fib) %>% 
  visOptions(highlightNearest = T, nodesIdSelection = T) %>% 
  visIgraphLayout(layout = 'layout_as_tree') %>%
  visNodes(color = list(background = "blue", highlight = 'red'))
