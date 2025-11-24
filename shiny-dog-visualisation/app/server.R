# Load libraries

library(shiny)
library(maps)
library(tidyverse)
library(stringr)
library(ggplot2)
library(leaflet)
library(sf)
library(ggiraph)
library(colorspace)
library(htmlwidgets)
library(networkD3)
library(dplyr)
library(ggcorrplot)
library(RColorBrewer)
library(ggExtra)
library(waffle)
library(MetBrewer)
library(ggh4x)
require(showtext) 
library(ggtext)
library(readr)

# Load Google Fonts

font_add_google("Outfit", "title_font")
font_add_google("Cabin", "body_font")
# Automatically use showtext to render text
showtext_auto()
showtext_opts(dpi = 320)
# Define font aliases
title_font <- "title_font"
body_font <- "body_font"


# Define server logic

shinyServer(function(input, output) {
  
  # -----------------------------
  # First visualisation
  # -----------------------------
  
  # Load the CSV file
  df_dogs_plot <- read_csv('../data/processed/df_dogs_plot.csv')
  
  # Define the color palette
  short_palette <- c("#1b9e77", "#d95f02", "#7570b3") 
  # Repeat colors to make 67
  color_palette <- rep(short_palette, length.out = 67) 
  
  # Calculate max_cbrt and sum_dog
  max_cbrt <- max(df_dogs_plot$num_dogs_cbrt)
  sum_dog <- sum(df_dogs_plot$total_count)
  
  # Create the ggplot
  main <- ggplot(df_dogs_plot, aes(x = rank, y = num_dogs_cbrt, color = as.factor(Council.x))) +
    # Set tooltips
    geom_segment_interactive(
      aes(x = rank, xend = rank, y = 0, yend = num_dogs_cbrt, tooltip = paste("Council:", Council.x, "<br>Total Count:", total_count)),
      size = 1.2
    ) +
    # Create circle and tooltip
    geom_rect_interactive(
      aes(xmin = 1, xmax = nrow(df_dogs_plot) + 1, ymin = 0, ymax = (500)^(1/3), tooltip = paste(sum_dog, "dogs")),
      fill = "grey97", color = "grey97"
    ) + 
    # Set tooltip o points
    geom_point_interactive(aes(size = num_dogs_cbrt, tooltip = paste( Council.x, "<br>Number of dogs:", total_count))) +
    # Use manual palette
    scale_color_manual(values = color_palette) +  
    # Scale
    scale_size(
      range = c(1, 2), 
      limits = c(0, max_cbrt), 
      guide = "none"
    ) +
    # Set boundaries for y
    scale_y_continuous(limits = c(0, max_cbrt)) +  
    # Change to circle 
    coord_polar() +
    # Delete unnecessary elements
    theme_void() +
    theme(
      # Hide legend
      legend.position = "none",  
      # Hide grid
      panel.grid = element_blank(),  
      # Set background color
      panel.background = element_rect(fill = "#F5F4EF", color = NA), 
      # Set color for circle 
      plot.background = element_rect(fill = "white", color = NA), 
      # Use margin
      plot.margin = margin(-110, 0, -110, 0),  
      # Delete space between panels
      panel.spacing = unit(0, "lines")  
    ) +
    # Add text to circle
    geom_text(
      x = 100, y = -1,
      label = "********\nHow many\ndogs live in\nSouth Australia?\n********",
      size = 5,
      lineheight = 0.87,
      color = "brown",
      family = "body_font"
    ) +
    geom_text(
      x = 100, y = 5,
      label = "(Hover your mouse \nto see the answer)",
      size = 3,
      lineheight = 0.87,
      family = "body_font",
      color = "brown"
    )
  
  # Convert the ggplot to an interactive plot using ggiraph
  tooltip_css <- "background-color:white;color:brown;padding:5px;border-radius:3px;"
  interactive_plot <- girafe(ggobj = main, width_svg = 8, height_svg = 5)
  interactive_plot <- girafe_options(interactive_plot, opts_tooltip(css = tooltip_css))
  
  # Output the interactive plot
  output$vis_1 <- renderGirafe({
    interactive_plot
  })
  
  # -----------------------------
  # Second visualisation
  # -----------------------------
  
  # Load csv
  owner_heat2 <- read_csv('../data/processed/owner_heat2.csv')
  # Calculate mean value
  mean_dogs <- mean(owner_heat2$AvNumofDog)
  # Set Councils as factor
  owner_heat2$Council <- factor(owner_heat2$Council, levels = owner_heat2$Council)
  
  # Create the ggplot
  diff <- ggplot(owner_heat2, aes(x = Council, y = num_dogs_diff, label = num_dogs_diff)) + 
    geom_bar_interactive(stat = 'identity', aes(fill = num_dogs_type, tooltip = paste(Council, "<br>Number of dogs per person:", AvNumofDog)), width = .5) +
    scale_fill_manual(name = " ",
                      labels = c("Above Average", "Below Average"), 
                      values = c("above" = "#00ba38", "below" = "#f8766d")) + 
    labs(title = "Average number of dogs per person:\nCouncils above and below average") + 
    geom_hline(yintercept = 0, linetype = "dashed", color = "black") +  
    coord_polar() +
    scale_y_continuous(
      name = "Number of Dogs",
      labels = function(x) round(x + mean_dogs)  
    ) +
    theme(
      panel.background = element_rect(fill = "#F5F4EF", color = NA), 
      plot.background = element_rect(fill = "#F5F4EF", color = NA), 
      panel.grid.major = element_blank(), 
      panel.grid.minor = element_blank(),  
      plot.margin = margin(0, 0, 0, -120),  
      axis.title = element_blank(),  
      axis.text = element_blank(),  
      axis.ticks = element_blank(),
      plot.title = element_text(
        face = "bold",
        hjust = 0.5,
        color = 'brown',
        size = 16
      ), 
      legend.position = "none"  
    ) +
    geom_text(
      x = 3, y = -0.55,
      label = paste0("The average number \nof dogs per person is:\n ", round(mean_dogs, 2),'\n********'),
      size = 3.5,
      lineheight = 0.87,
      color = "black"
    ) +
    geom_text(
      x = 1, y = -0.72,
      label = "(Hover your mouse to see\n the numbers by councils.)",
      size = 2.2,
      lineheight = 0.87,
      color = "black"
    )
  
  tooltip2_css <- "background-color:white;color:brown;padding:5px;border-radius:3px;"
  interactive_plot2 <- girafe(ggobj = diff, width_svg = 6, height_svg = 5)
  interactive_plot2 <- girafe_options(interactive_plot2, opts_tooltip(css = tooltip2_css))
  
  output$vis_2 <- renderGirafe({
    interactive_plot2
  })
  
  # -----------------------------
  # Third visualisation
  # -----------------------------
  
  own_gend2 <- read_csv('../data/processed/own_gend2.csv')
  
  nodes2 <- data.frame(name = unique(c(own_gend2$AgeCategory, 
                                       own_gend2$NumOfDogs, 
                                       own_gend2$Gender)))
  
  links_age_dogs <- own_gend2 %>%
    mutate(source = match(AgeCategory, nodes2$name) - 1,
           target = match(NumOfDogs, nodes2$name) - 1,
           value = Count) %>%
    select(source, target, value)
  
  links_dogs_gender <- own_gend2 %>%
    mutate(source = match(NumOfDogs, nodes2$name) - 1,
           target = match(Gender, nodes2$name) - 1,
           value = Count) %>%
    select(source, target, value)
  
  links2 <- bind_rows(links_age_dogs, links_dogs_gender)
  
  color_scale <- 'd3.scaleOrdinal().range(["#1b9e77", "#d95f02", "#7570b3", "#800000", "#556b2f", "#8b4513", "#006400", "#4b0082", "#8b008b", "#228b22", "#b22222", "#d62728", "#1f77b4", "#a52a2a", "#2e8b57", "#9932cc", "#7f7f7f", "#aec7e8", "#ff6347", "#bdb76b", "#556b2f", "#c5b0d5"])'  
  
  sankey_gender <- sankeyNetwork(Links = links2, Nodes = nodes2, 
                                 Source = "source", Target = "target", 
                                 Value = "value", NodeID = "name",
                                 units = "Count",
                                 fontSize = 12, nodeWidth = 30,
                                 sinksRight = FALSE,
                                 colourScale = JS(color_scale),
                                 nodePadding = 10)
  
  sankey_gender <- htmlwidgets::onRender(
    sankey_gender,
    '
  function(el, x) {

      d3.selectAll(".node text")
      .style("fill", "#A52A2A")
      .style("font-weight", "bold");
    d3.selectAll(".node").select("title")
      .text(function(d) { return d.name + ": " + d.value + " people"; });
    d3.selectAll(".link").select("title")
      .text(function(d) { return d.source.name + " → " + d.target.name + ": " + d.value + " people"; });
  }
  '
  )
  
  output$vis_3 <- renderSankeyNetwork({
    sankey_gender
  })
  
  # -----------------------------
  # Visualisation fourth
  # -----------------------------
  
  # Load the CSV file
  expanded_data <- read_csv('../data/processed/expanded_data.csv')
  
  # Convert categorical data to factors
  expanded_data <- expanded_data %>%
    mutate(across(c(Gender, Reg_status, Microchipped, Desexed), as.factor))
  
  # Function to calculate Cramer's V
  cramers_v <- function(x, y) {
    tbl <- table(x, y)
    chi2 <- chisq.test(tbl)$statistic
    n <- sum(tbl)
    min_dim <- min(dim(tbl)) - 1
    v <- sqrt(chi2 / (n * min_dim))
    return(v)
  }
  
  # Define the variables to be included in the correlation matrix
  vars <- c("Gender", "Reg_status", "Microchipped", "Desexed")
  
  # Create an empty matrix to store Cramer's V values
  corr_matrix <- matrix(NA, nrow = length(vars), ncol = length(vars), dimnames = list(vars, vars))
  
  # Loop through each pair of variables to calculate Cramer's V
  for (i in 1:length(vars)) {
    for (j in i:length(vars)) {
      # Calculate Cramer's V for the pair of variables and store it in the matrix
      corr_matrix[i, j] <- cramers_v(expanded_data[[vars[i]]], expanded_data[[vars[j]]])
      corr_matrix[j, i] <- corr_matrix[i, j]
    }
  }
  
  # Create plot
  output$vis_4 <- renderPlot({
    ggcorrplot(corr_matrix, hc.order = TRUE, 
               type = "lower", 
               lab = TRUE, 
               lab_size = 4, 
               method = "circle", 
               colors = c("tomato2", "white", "springgreen3"), 
               title = " ", 
               ggtheme = theme_bw() + theme(
                 rect = element_rect(fill = "transparent"),
                 # Hide grid
                 panel.grid.major = element_blank(),  
                 panel.grid.minor = element_blank(),  
                 #panel.border = element_rect(color = "brown", fill = NA, size = 1.5),
                 panel.border = element_blank(), 
                 # Set background color
                 strip.background = element_rect(fill = "#F5F4EF", color=NA),
                 panel.background = element_rect(fill = "#F5F4EF", color = NA),  
                 plot.background = element_rect(fill = "#F5F4EF", color = NA), 
                 # Set text font
                 text = element_text( color = 'black', face = "bold"), 
                 axis.title = element_text(color = 'black'), 
                 axis.text = element_text(color = 'black'),  
                 # Add title
                 plot.title = element_text(color = 'brown'),  
                 plot.tag = element_text(color = 'red'),
                 # Set legend background color
                 legend.background = element_rect(fill = "#F5F4EF", color = NA),  
                 legend.key = element_rect(fill = "#F5F4EF", color = NA),
                 # Set legend color font
                 lab_col = "black",  
                 outline.color = "springgreen3"))  + geom_text(aes(x = Var1, y = Var2, label = round(value, 2)), color = "brown", size = 4)
  }, height=350, width=422)
  
  # -----------------------------
  # Visualisation fifth
  # -----------------------------
  
  # Load the GeoJSON file
  pet_counc <- st_read("www/pet_counc.geojson")
  
  # Define bins and color palette
  bins <- c(0, 40, 60, 70, 80, 90, 100)
  
  # Define the choices for the checklist
  choices <- c(
    "Registered Percent" = "registered_percent",
    "Desexed Percent" = "desexed_percent",
    "Chipped Percent" = "chipped_percent",
    "Registered, Desexed, and Chipped Percent" = "reg_desex_chip_percent",
    "Registered and Chipped Percent" = "reg_chip_percent"
  )
  
  # Set checklist
  output$dynamic_checklist <- renderUI({
    radioButtons("checklist", 
                 "Choose option:", 
                 choices = choices,
                 selected = "registered_percent")
  })
  
  # Create the leaflet map
  output$map <- renderLeaflet({
    selected_column <- input$checklist
    # Change df
    pet_counc <- pet_counc %>% mutate(percentage = .[[selected_column]])
    # Create colors
    qpal <- colorBin("YlGnBu", domain = pet_counc$percentage, bins = bins)
    
    # Create map plot
    leaflet(pet_counc) %>% 
      # Set initial point
      setView(lng = 138.6070, lat = -34.94074, zoom = 6) %>% 
      # Choose background
      addProviderTiles(providers$CartoDB.Positron) %>% 
      # Color councils
      addPolygons(
        fillColor = ~qpal(percentage),
        fillOpacity = 0.7,
        color = "white",
        weight = 1,
        popup = ~paste("LGA:", lga, "<br>",
                       "Percent:", round(percentage, 2), "%"),
        label = ~paste0(lga, "\n",
                        "Percent:", round(percentage, 2), "%")
      ) %>% 
      # Add legend
      addLegend(
        pal = qpal,
        values = ~percentage,
        title = names(choices)[choices == selected_column],
        opacity = 1,
        position = "topright"
      )
  })
  
  # Create bar chart
  output$vis_5 <- renderPlot({
    selected_column <- input$checklist
    # Change df
    pet_counc <- pet_counc %>% mutate(percentage = .[[selected_column]])
    # Aggregate data
    bin_summary <- pet_counc %>%
      mutate(bin = cut(percentage, breaks = bins, include.lowest = TRUE)) %>%
      group_by(bin) %>%
      summarise(count = n()) %>%
      mutate(percentage = count / sum(count) * 100)
    
    # Set color
    qpal <- colorBin("YlGnBu", domain = pet_counc$percentage, bins = bins)
    bin_colors <- qpal(bins)
    # save color for bins
    names(bin_colors) <- levels(cut(bins, breaks = bins, include.lowest = TRUE))
    
    # Create bars
    ggplot(bin_summary, aes(x = bin, y = percentage, fill = bin)) +
      geom_col() +
      #geom_text(aes(label = paste0(round(percentage, 1), "%")),hjust = 0.2, vjust = 0.1, size = 4, fontface = "bold", angle = 45, 
      #          color = "brown", stroke = 1, fill = "white") + 
      scale_fill_manual(values = bin_colors, name = "Bins") + 
      labs(
        title = "Percentage breakdown",
        fill = "Bins"  # Add a title for the legend
      ) +
      # Change axis
      coord_flip() +
      theme_minimal() +
      theme(
        # Hide grid
        panel.grid = element_blank(),
        # Set font for text elements of the plot
        plot.title = element_text(size = 12, color = 'black', hjust = 0.5, face = "bold", family = "Arial"),
        axis.text.x = element_text(size = 10, color = 'black', face = "bold", family = "Arial"),  
        axis.text.y = element_text(size = 10, color = 'black', face = "bold", family = "Arial"),  
        # Hide axis titles
        axis.title.x = element_blank(),  
        axis.title.y = element_blank(), 
        legend.position = "none",
        # Set color of legend
        legend.text = element_text(color = 'black', face = "bold", family = "Arial"),  
        legend.title = element_text(color = 'black', face = "bold", family = "Arial"),
        # Set background transparent
        plot.background = element_rect(fill = "transparent", color = NA),  
        panel.background = element_rect(fill = "transparent", color = NA), 
        # Hide grid
        panel.grid.major = element_blank(),  
        panel.grid.minor = element_blank(), 
        # Set margin
        plot.margin = margin(1, 1, 1, 1, "cm") 
      )
  }, bg = "transparent") 
  
  # -----------------------------
  # Sixth visualisation
  # -----------------------------
  
  # Load the CSV file
  df_crime_pet2 <- read_csv('../data/processed/df_crime_pet2.csv')
  
  # Dynamic checklist for excluding outliers
  output$dynamic_checklist2 <- renderUI({
    radioButtons("checklist2", 
                 'Exclude outliers?', 
                 choices = c('Yes', 'No'),
                 selected = 'No')
  })
  
  # Create plot
  output$vis_6 <- renderPlot({
    # Filter dataset
    if (input$checklist2 == "Yes") {
      data <- df_crime_pet2 %>%
        filter(Council_seat != "Coober Pedy", Council_seat != "Ceduna", Council_seat != "Port Augusta", Council_seat != "Adelaide", Council_seat != "Mallala")
    } else {
      data <- df_crime_pet2
    }
    
    # Calculate correlation
    correlation2 <- cor.test(data$property_pop, data$dog_pop)
    corr_label2 <- paste("Correlation: ", round(correlation2$estimate, 2))
    # Plot data
    crime_plot <- ggplot(data, aes(x = property_pop, y = dog_pop)) +
      # Change colors of points
      geom_point(color = "#1b9e77") +  
      # Set text
      labs(title = "Dog density in relation to crime rate",
           x = "Number of crimes",
           y = "Dog Density per 1,000 people") +
      # Add smooth line
      geom_smooth(method = "lm", col = "blue") +
      # Add correlation text
      annotate("text", x = Inf, y = Inf, label = corr_label2, hjust = 1.1, vjust = 2, size = 5,face = "bold", color = "#d95f02") +
      theme_minimal() +
      theme(
        # Set font of text
        plot.title = element_text(color = "brown", face = "bold", hjust = 0.5, margin = margin(30,0,0,0)),
        axis.title = element_text(color = "brown", face = "bold"),  
        axis.text = element_text(color = "brown", face = "bold"), 
        # Hide grid
        panel.grid = element_blank(),  
        # Hide panel border
        panel.border = element_blank(), 
        # Set background to white
        panel.background = element_rect(fill = "white", color = NA), 
        plot.background = element_rect(fill = "white", color = NA)
      )
    
    # Create marginal histograms
    x_hist <- ggplot(data, aes(x = property_pop)) +
      geom_histogram(fill = brewer.pal(9, "YlGnBu")[9], color = NA) +
      theme_void() +
      theme(
        panel.background = element_rect(fill = "#F5F4EF", color = NA),  
        plot.background = element_rect(fill = "#F5F4EF", color = NA)  
      )
    
    # Add marginal histograms
    ggMarginal(crime_plot, type = "histogram", fill = "transparent", 
               margins = "both", 
               # Use blue color from palette
               xparams = list(fill = brewer.pal(9, "YlGnBu")[9]),  
               # Use yellow color from palette
               yparams = list(fill = brewer.pal(9, "YlGnBu")[2]))  
  }, width = 750, height = 400)
  
  # -----------------------------
  # Visualisation seventh
  # -----------------------------
  
  # Load the CSV file
  incident_data <- read_csv('../data/processed/incident_data.csv')
  
  # Create dynamic slider 
  output$dynamic_slider <- renderUI({
    # Find max and minimum year
    max_year <- max(incident_data$YearExtracted)
    min_year <- min(incident_data$YearExtracted)
    # Set time slider
    sliderInput("incident_year",
                "The time period for dog-related incidents (years)",
                min = min_year,
                max = max_year,
                value = c(min_year, max_year),
                step = 1,
                # Remove comma separator
                sep = "")  
  })
  
  # Aggregate dataset
  incident_data3 <- incident_data %>%
    group_by(YearExtracted, LocationType) %>%
    summarise(count = sum(Count), .groups = "drop")
  
  output$vis_7 <- renderPlot({
    # Filter data based on input
    incident_data_filtered <- incident_data3 %>%
      filter(YearExtracted >= input$incident_year[1] & YearExtracted <= input$incident_year[2]) 
    
    # Define the color palette from RColorBrewer
    paired_palette <- brewer.pal(12, "Spectral")
    
    # Create waffle plot
    p <- ggplot(incident_data_filtered, aes(fill = LocationType, values = count)) +
      geom_waffle(color = "white", size = 0.45, n_rows = 20, flip = TRUE) +
      facet_wrap(~YearExtracted, nrow = 1, strip.position = "bottom") +
      scale_x_discrete() + 
      scale_y_continuous(labels = function(x) x * 10, expand = c(0,0)) +
      scale_fill_manual(values = paired_palette) +   
      coord_equal() +
      theme_minimal() +
      theme(
        # Hide titles of axis
        axis.title = element_blank(),
        axis.text.x = element_text(family = body_font, size = 12),
        axis.text.y = element_text(family = body_font, size = 12),
        # Set legend
        legend.position = "top",
        legend.spacing = unit(0.5, 'cm'),
        legend.key.height = unit(0.5, 'cm'),
        legend.key.width = unit(0.7, 'cm'),
        legend.text = element_text(family = body_font,
                                   size = 10,
                                   face = 'plain',
                                   color = "grey10"),
        # Set white background
        panel.background = element_rect(fill = "white", color = NA), 
        plot.background = element_rect(fill = "white", color = NA), 
        # Add margin
        plot.margin = margin(10, 10, 10, 10)
      )
    
    print(p)
  }, width = 750, height = 436)
  
  
  # -----------------------------
  # Eight visualisation
  # -----------------------------
  
  # Create checklist
  choices3 <- c(
    "On a leash" = "On a Leash",
    "No leash" = "No Leash",
    "All" = "All"
  )
  
  output$dynamic_checklist3 <- renderUI({
    radioButtons(
      "checklist3", 
      "Choose option:", 
      choices = choices3,
      selected = "All"
    )
  })
  
  # Create plot
  output$vis_8 <- renderGirafe({
    # Filter dataset and aggregate
    incident_data4 <- incident_data %>%
      # Filter by leash status based on user selection
      filter((OffendingAnimalLeashStatus == input$checklist3 | input$checklist3 == "All")) %>%
      filter(YearExtracted >= input$incident_year[1] & YearExtracted <= input$incident_year[2]) %>%
      group_by(YearExtracted, LocationType, VictimType) %>%
      summarise(count = sum(Count), .groups = "drop") %>%
      pivot_wider(names_from = VictimType, values_from = count, values_fill = 0)
    
    # Calculate the average value for each location
    average_values <- incident_data4 %>%
      group_by(LocationType) %>%
      summarise(avg_animal = mean(Animal), avg_human = mean(Human), .groups = "drop") %>%
      mutate(avg_total = (avg_animal + avg_human) / 2) %>%
      arrange(desc(avg_total))
    
    incident_data4$LocationType <- factor(incident_data4$LocationType, levels = average_values$LocationType)
    

    # Build the line plot
    line <- ggplot(incident_data4, aes(x = YearExtracted)) +
      # Add animal line
      geom_line(aes(y = Animal, color = "animal")) +
      # Add human line
      geom_line(aes(y = Human, color = "human")) +
      # Add points for tooltip
      geom_point_interactive(
        aes(y = Animal, color = "animal",
            tooltip = paste("Year:", YearExtracted, "<br>Count:", Animal, "<br>Victim: Animal")),
        size = 0.5
      ) +
      geom_point_interactive(
        aes(y = Human, color = "human",
            tooltip = paste("Year:", YearExtracted, "<br>Count:", Human, "<br>Victim: Human")),
        size = 0.5
      ) +
      # Find difference
      stat_difference(aes(ymin = Human, ymax = Animal), alpha = 0.3) +
      # Add locations facet
      facet_wrap(~ LocationType, scales = "free_y") +
      # Colors for the lines
      scale_color_manual(values = c("#3D85F7", "#C32E5A")) +
      scale_fill_manual(
        values = c(
          colorspace::lighten("#3D85F7"), 
          colorspace::lighten("#C32E5A"), 
          "grey60"
        ),
        labels = c("more animal", "more human", "same")
      ) +
      # Ensure x-axis only shows whole years
      scale_x_continuous(breaks = seq(min(incident_data4$YearExtracted), max(incident_data4$YearExtracted), by = 1)) +
      # Add labels
      labs(
        title = "Victims of dog-related incidents (Human vs Animal)\n by leash status in 2018-2024"
      ) +
      # Specify the order for the guides
      guides(
        color = guide_legend(order = 1),
        fill = guide_legend(order = 2)
      ) +
      theme_minimal() +
      theme(
        # Elements within a guide are placed one next to the other in the same row
        legend.direction = "horizontal",
        # Different guides are stacked vertically
        legend.box = "vertical",
        # Hide legend title
        legend.title = element_blank(),
        # Set background color
        plot.background = element_rect(fill = "#F5F4EF", color = NA),
        plot.margin = margin(20, 30, 20, 30),
        plot.title = element_text(
          margin = margin(0, 0, 0, 0),
          size = 16,
          face = "bold",
          vjust = 0,
          color = "grey25"
        ),
        # Remove titles for axes
        axis.title = element_blank(),
        axis.text = element_text(color = "grey40"),
        # Set font
        strip.text = element_text(face = "bold"),
        axis.text.x = element_text(angle = 45, hjust = 1)
      )
    
    # Set tooltip css
    tooltip5_css <- "background-color:white;color:black;padding:5px;border-radius:3px;"
    
    # Convert ggplot to ggiraph for interactivity
    interactive_line <- girafe(ggobj = line, width_svg = 10, height_svg = 5)
    interactive_line <- girafe_options(interactive_line, opts_tooltip(css = tooltip5_css))
    interactive_line
  })
  
  
})