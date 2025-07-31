# server
function(input, output, session) {
  
  feedback <- reactiveValues()
  
  observeEvent(input$submit, {
    # inputs
    r1 <- input$r1
    r2 <- input$r2
    maxn <- input$maxn
    maxr2 <- input$maxr2
    
    # table of combinations
    df <- cbind(
      0:maxn,
      sapply(0:maxr2, pascal_col, r1 = r1, r2 = r2, max_n = maxn)) 
    colnames(df) <- c('n', lapply(0:maxr2, odd_suffix))
    
    # totals
    df <- df %>% 
      as_tibble() %>% 
      mutate(across(everything(), as.integer))
    df_temp <- df %>% 
      mutate(
        mp = rowSums(across(-n)),
        mm = rowSums(across(ends_with('_even'))) - rowSums(across(ends_with('_odd')))
      ) %>% 
      select(n, mp, mm)
    df <- df %>% 
      mutate(across(everything(), abs)) %>% 
      mutate(
        pp = rowSums(across(-n)),
        pm = rowSums(across(ends_with('_even'))) - rowSums(across(ends_with('_odd')))
      ) %>% 
      full_join(df_temp)
    
    # render
    pp <- paste0('[', r1, ',', r2, ']')
    pm <- paste0('[', r1, ',-', r2, ']')
    mp <- paste0('[-', r1, ',', r2, ']')
    mm <- paste0('[-', r1, ',-', r2, ']')
    df <- df %>% 
      mutate(across(everything(), as.integer)) %>% 
      mutate(across(-c(n, pp, pm, mp, mm), ~replace(.x, .x == 0, '')))
    colnames(df) <- c('n', 0:maxr2, pp, pm, mp, mm)
    output$table <- renderTable(df)
    })
}