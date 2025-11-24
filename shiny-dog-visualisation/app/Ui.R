
library(shiny)
library(bslib)
library(leaflet)
library(ggiraph)
library(networkD3)
library(showtext)
library(ggtext)


showtext_auto()

# Load google fonts
font_add_google("Outfit", "title_font")
font_add_google("Cabin", "body_font")
showtext_auto()

# Define UI 
shinyUI(fixedPage(
  # Set style for one of the graph
  tags$style(
    "#detailedRow g:nth-child(3) {
      transform: scale(1.6) translate(-70px, -45px);
    }
    
    "
  ),
  
  # Set style for map
  tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "styles.css"), 
    tags$style(HTML("
      .leaflet-tooltip {
        white-space: pre-line;
      }
      .inset-plot {
        position: absolute;
        bottom: -2%;
        left: -10%;
        width: 90%;
        height: 50%;
        #border: 2px solid bl;ack
        background-color: gray;  
        z-index: 1000;
        transform: scale(0.7);  /* Scale down the plot */
      }
    "))
  ),
  
  # Write title of the project
  titlePanel(
    tags$div(
      HTML("Comprehensive Analysis of Pet Ownership and Its Impact <br>on Community Safety in South Australia"),
      style = "text-align: center; color: brown; font-family: 'Outfit'; font-size: 40px; font-weight: bold;"
    )
  ),

  # First row: first plot
  
  fixedRow(  
    
    column(12,
           girafeOutput("vis_1", height = "700px")
    )
  ),
  
  # Second row: introduction text and image
  fixedRow(
    column(8,
           tags$div(
           class = "margin-top",
           HTML("
        <span style='font-size:20px; color: black; line-height: 1.2;'>
            &nbsp;&nbsp;South Australia dogs play a significant role in many households. The chart above shows how dogs are spread out among different councils, giving us a good starting point for further exploration. 
        <br><br><span style='font-size:24px; color: brown; font-weight: bold;' > &nbsp;&nbsp;    But what do we know about the people behind these pets?</span> <br><br> The next set of graphs will explore who owns dogs, revealing how age and gender affect pet ownership trends in the region. After that, we'll look at responsible dog ownership patterns and how these factors connect to community safety.

        </span>

      "))
    ),
    column(4,
           tags$div(
             img(src = "beagle-dog-on-white-background-vector - Copy (2).jpg", height = "320px"),
             style = "text-align: center;"
           )
    )
  ),
  
  # Set space between lines
  tags$div(class = "spacing-bottom"),
  

  # Third row: sankey plot and description text
  fixedRow(
        column(8, id = "sankey-plot",
               tags$div(
                 class = "title-caption-left",
                 tags$h3(
                   "Sankey diagram of dog ownership by age and gender",
                   class = "margin-left-50",
                   style = "text-align: center; color: #A52A2A; font-family: 'Outfit'; font-size: 28px; font-weight: bold; margin-bottom: 20px;"
                 ),
                 sankeyNetworkOutput("vis_3", width = "1000px", height = "600px"),
                 tags$div(
                   HTML("Data:  DATA_SA_Owners - 2024-05-30 <br>  (https://data.sa.gov.au/data/dataset/dogs-and-cats-online-data
2023-2024/resource/7e605073-57ac-4cb6-9a2b-a23054b4e66f) "),
                   class = "margin-left-50",
                   style = "font-family: 'Cabin'; font-size: 14px; color: black; text-align: center; "
                 )
               )
               
        ),
    column(4,
           tags$div(
             HTML("
                   <div class='centered-content'>
                     <p style='font-size: 20px;  color: black;line-height: 1.2;'>On the chart, you can observe the following:</p>
                     <ul style='font-size: 20px;  color: bblack;line-height: 1.2;'>
                       <li>Owning <span style='color: brown; font-weight: bold;'>one dog</span> is the <span style='color: brown; font-weight: bold;'>most common scenario</span> across <span style='color: brown; font-weight: bold;'>all age groups</span>, with approximately 201,000 owners fitting this category.</li>
                       <li>The next most frequent category is two-dog ownership, followed by no dogs.</li>
                       <li>Ownership of <span style='color: brown; font-weight: bold;'>three</span>, four, five, <span style='color: brown; font-weight: bold;'>or more dogs</span> is significantly <span style='color: brown; font-weight: bold;'>less common</span> across age groups.</li>
                       <li>The <span style='color: brown; font-weight: bold;'>16-20 age</span> group is the <span style='color: brown; font-weight: bold;'>least likely to own dogs</span>, often preferring other pets, such as cats.</li>
                       <li>Overall, <span style='color: brown; font-weight: bold;'>women</span> are <span style='color: brown; font-weight: bold;'>more likely to own dogs</span> than men.</li>
                     </ul>
                     <p style='font-size: 20px;  color: black; line-height: 1.2;'>However, when broken down by council, for owners with 3 or more dogs, some councils show a higher number of male owners than female.</p>
                     <p style='font-size: 18px; font-weight: bold; color: black;'>(Hover over the chart to view specific counts for each category.)</p>
                   </div>
                 ")
           )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  # Fourth row: two plots (third plot and text, text and forth plot)
  fixedRow(
    column(7,
           fixedRow(
             column(12,
                    tags$div(
                      class = "margin-plot",  
                      girafeOutput("vis_2", width = "800px", height = "600px"),
                      id = "detailedRow"
                    )
             )
           ),
           fixedRow(
             column(12,
                    tags$div(
                      class = "margin-plot",  
                      HTML("
                            <span style='font-size:20px; color: black; line-height: 1.2;'>
                              On the chart, councils above the average number of dogs per person are in green, and those below are in red.
                            </span>
                        ")
             )
           )
    )),

    column(5,
           fixedRow(
             column(12, tags$div(
               class = "margin-right",
               tags$h3(
                 "Correlogram of dog data",
                 class = "title-padding", 
                 style = "color: #A52A2A; font-family: 'Outfit'; font-size: 28px; font-weight: bold; margin-bottom: 20px;"
               ),
               HTML("
                     <span style='font-size:20px; color: black; line-height: 1.2;'>
                       <br>The next graph shows how dog traits relate:<br><br>
                     </span>
                     <ul style='font-size:20px; color: black; line-height: 1.2;'>
                       <li>Gender doesn’t impact other traits much.</li>
                       <li>Desexing, registration, and microchipping are somewhat linked. When one increases, the others often do, too.</li>
                       <li>The strongest link is between microchipping and desexing: most microchipped dogs are desexed, and most unchipped dogs are not.</li>
                     </ul>
                   ")
             ))
           ),
           fixedRow(
             column(12,
                    tags$div(
                      class = "margin-plot vis_4-plot",
                      plotOutput("vis_4", width = "100%", height = "350px")
                    )
             )
           )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  # Fifth row: text and picture
  fixedRow(
    column(8,
           tags$div( tags$h3(
               "What can be said about responsible ownership?",
               style = "text-align: center; color: #A52A2A; font-family: 'Outfit'; font-size: 28px; font-weight: bold; margin-bottom: 20px;"
             ),
             
             HTML("
        <span style='font-size:20px; color: black; line-height: 1.2;'>
            <br>&nbsp;&nbsp;On the map, you can see how each council scores on responsible ownership traits. High <span style='color: brown; font-weight: bold;'>rates of registration and microchipping</span> in South Australia—<span style='color: brown; font-weight: bold;'>over 90%</span> in most councils — showcase a strong sense of responsibility among pet owners. While <span style='color: brown; font-weight: bold;'>desexing</span> is less common, ranging between <span style='color: brown; font-weight: bold;'>40-70%</span> due to a portion of owners choosing to breed their dogs.
        <br><br> &nbsp;&nbsp;   This map allows you to explore how each council scores on responsible ownership traits. Select traits individually or in combination, and hover over each area to see the exact data.<br> Which council do you think is leading in responsible pet care? <br>Dive in to find out!
       <br>
        </span>

      "))
    ),
    column(4,
           tags$div(
             img(src = "k9hspb31g3qgpxlb8a1zluiwinmruts03.jpg", height = "300px"),
             style = "text-align: center;"
           )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),

  # Sixth row: map
  layout_columns(
    card(
      card_header(" "),
      sidebarLayout(
        sidebarPanel(
          uiOutput('dynamic_checklist'),
          class = "sidebar-text",
          width = 3  # Make the sidebar narrower
        ),
        mainPanel(
          div(
            leafletOutput("map", height = "550px"),
            div(
              plotOutput("vis_5"),
              class = "inset-plot"
            )
          ),
          tags$div(
            HTML("Data: DATA_SA_Animals - 2024-05-30 <br>  (https://data.sa.gov.au/data/dataset/dogs-and-catsonline-data-2023-2024/resource/ebd3ee1b-96ca-474e-8184-fb2ad82fcf0c) "),
            class = "margin-left-50",
            style = "font-family: 'Cabin'; font-size: 14px; color: black; text-align: center;"
          )
        )
      )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  # Seventh row: text and picture
  fixedRow(
    column(9, 
           tags$div(
             tags$h3(
               "Does more bark mean less crime?",
               style = "text-align: center; color: #A52A2A; font-family: 'Outfit'; font-size: 28px; font-weight: bold; margin-bottom: 20px;"
             ),
             HTML("
                   <span style='font-size:20px; color: black; line-height: 1.2;'>
                     &nbsp;&nbsp;As we delve deeper into the role of our furry companions in our communities, an intriguing question arises: Could dogs be making a difference in public safety? <br> To investigate this, we examined crime rates alongside the number of dogs per thousand people. Let’s uncover whether there's a connection between our canine friends and the safety of our neighborhoods.
                   </span>
                 ")
           )
    ),     column(3,
                  tags$div(
                    img(src = "beware-of-dog-vector-4451794.jpg", height = "200px"),
                    style = "text-align: center;"
                  )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  # Eight row: crime plot
  layout_columns(
    card(
      card_header(" "),
      sidebarLayout(
        sidebarPanel(
          uiOutput('dynamic_checklist2'),
          class = "sidebar-text",
          width = 3  # Make the sidebar narrower
        ),
        mainPanel(
          plotOutput("vis_6", width = 750, height = 400),
          tags$div(
            HTML("Data:  Crime Statistics 2023-24 Q1_Q3 <br> (https://data.sa.gov.au/data/dataset/crime-statistics/resource/e18dfe2a-3ee8-4f01-9b50-0ae91458f7ff)  "),
            class = "margin-left-50",
            style = "font-family: 'Cabin'; font-size: 14px; color: black; text-align: center;"
          )
        )
      )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  
  # Ninth row: text
  fixedRow(
    column(9, 
           HTML("
                 <span style='font-size:20px; color: black; line-height: 1.2;'>
                   &nbsp;&nbsp;The results show a slight negative correlation, suggesting that <span style='color: brown; font-weight: bold;'>councils with more dogs</span> might <span style='color: brown; font-weight: bold;'>have</span> slightly <span style='color: brown; font-weight: bold;'>lower crime rates</span>. <br>Could it be that dogs help deter crime, or is it just a coincidence? <br>Dive into the plot and decide for yourself!
                 </span>
               ")
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  # Eleventh row: test and picture
  fixedRow(
    column(9, 
      HTML("
                 <span style='font-size:20px; color: black; line-height: 1.2;'>
                   While dogs can help ward off crime, they also play a complex role in community safety.<br>
                   <span style='font-size:24px; color: brown; font-weight: bold;' >Curious to know where dog-related incidents happen most?</span> <br>
                   The following two charts help answer this question. Our first interactive chart breaks down these incidents by year and location from 2018 to 2024, and you can explore this timeline yourself. <br><span style='font-size: 16px; font-weight: bold; color: black;'>(Any selection you make instantly reflects across both charts for an in-depth view.)</span>
                 </span>
               ")
    ),  column(3,
               tags$div(
                 img(src = "f3c5404022f44d7d761e4d2a52c8fd00.jpg", height = "150px"),
                 style = "text-align: center;"
               )
    )

  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  # Twelveth row: first incidents plot
  layout_columns(
    card(
      card_header(" ", height = "200%", width = "100%"),
      sidebarLayout(
        sidebarPanel(
          uiOutput('dynamic_slider'),  # Add dynamic slider output
          class = "sidebar-text",
          width = 3  # Make the sidebar narrower
        ),
        mainPanel(
         plotOutput("vis_7", width = 750, height = 436),
         tags$div(
           HTML("Data: DATA_SA_Incidents - 2024-05-30 <br> (https://data.sa.gov.au/data/dataset/dogs-and-cats-online-data-2023-2024/resource/437e7c2c-5b42
455b-b8b4-6cabe19c4db4) "),
           class = "margin-left-50",
           style = "font-family: 'Cabin'; font-size: 14px; color: black; text-align: center;"
         )
        )
      )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  # Thirteen row: text and picture
  fixedRow(
    column(8, 
           HTML("
                 <span style='font-size:20px; color: black; line-height: 1.2;'>
                   The second chart dives deeper, showing whether incidents impacted people or animals, ranked by location for clear insights. Use the leash status filters to uncover patterns—does location influence incident rates in different leash conditions? <br> Explore the data and see for yourself!
                 </span>
               ")
    ),    
    column(4,
           tags$div(
             img(src = "istockphoto-480384168-170667a2.jpg", height = "150px"),
             style = "text-align: center;"
           )
    )
  ),
  
  # Fourteen row: second incidents plot

  layout_columns(
    card(
      card_header(" "),
      sidebarLayout(
        sidebarPanel(
          uiOutput('dynamic_checklist3'),
          class = "sidebar-text",
          width = 3  # Make the sidebar narrower
        ),
        mainPanel(
          girafeOutput("vis_8", width = "118%", height = "500px"),
          tags$div(
            HTML("Data: DATA_SA_Incidents - 2024-05-30 <br> (https://data.sa.gov.au/data/dataset/dogs-and-cats-online-data-2023-2024/resource/437e7c2c-5b42
455b-b8b4-6cabe19c4db4) "),
            class = "margin-left-50",
            style = "font-family: 'Cabin'; font-size: 14px; color: black; text-align: center;"
          )
        )
      )
    )
  ),
  
  # Space between lines
  tags$div(class = "spacing-bottom"),
  
  
  # Fifteen row: picture and data sources
  fixedRow(  
    
    column(12,
           tags$div(
             img(src = "9OuVYle0X9c.jpg", height = "320px"),
             style = "text-align: center;"
           )
    )
  ),
  
  fixedRow(
    column(12,tags$div( 
           HTML("
                Additional Data Sources:<br>
                  Local Government Areas of South Australia (Wikipedia) <br>
                  (https://en.wikipedia.org/wiki/Local_government_areas_of_South_Australia);
                  List of Councils by Suburb/Locality (2021)<br>
                  (https://www.lga.sa.gov.au/__data/assets/excel_doc/0016/1212901/2021_List-of-Councils-bySuburb_Locality_Nov.xlsx);
                 <br>Local Government Areas of South Australia (shp)<br>
                 (https://www.dptiapps.com.au/dataportal/LGA_shp.zip).<br>
                 Images were sourced from (https://alchevsk.top/catalog/dobryy-den-kuplyu-vozmu-v-horoshie-ruki) and (https://petandme.ru/upload/iblock/390/k9hspb31g3qgpxlb8a1zluiwinmruts0.png)<br>
                 Isolated vector graphics were provided by Vecteezy (https://www.vecteezy.com/free-vector/isolated).
                 
                   "),            class = "margin-left-50",
           style = "font-family: 'Cabin'; font-size: 14px; color: black; text-align: center;")
    )), 


  
))