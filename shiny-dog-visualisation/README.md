# Dog Ownership Visualisation in South Australia (R Shiny App) 🐶

## **TL;DR:**  
Interactive **R Shiny application** analysing dog ownership patterns and dog-related incidents in South Australia. Demonstrates expertise in **data wrangling, aggregation, preprocessing, and merging of tabular and spatial datasets**, combined with **exploratory data analysis** and creation of **interactive, non-standard visualisations** (e.g., circular lollipop plots, Sankey diagrams, polar diverging bars, maps, waffle charts, and conditional time series). Highlights skills in **dashboard design, storytelling with data, and interactivity implementation**, directly applicable to **junior data analyst and data scientist roles**.


## Project Overview
Dogs in Australia are not only loyal companions but can also contribute to safer communities by deterring crime. However, challenges exist, with around 2,000 dog attacks reported between 2022 and 2023.

This project explores the dynamics of dog ownership and dog-related incidents in South Australia, providing insights into responsible ownership and community safety through interactive, narrative visualisation.

Implemented as an **interactive R Shiny application**, the project allows users to explore the data dynamically using filters, checkboxes, and time sliders. It features **non-standard, visually engaging charts**—including circular lollipop plots, Sankey diagrams, polar diverging bars, waffle charts, and conditional time series plots—moving beyond typical bar or scatter plots to offer a richer, more insightful narrative.

The project aims to answer three key questions:

1. **Patterns of Dog Ownership**  
   What are the patterns of dog ownership in South Australia, and how do factors like age and gender of owners shape responsible pet ownership?

2. **Dogs and Community Safety**  
   Do dogs contribute to neighborhood safety by acting as a crime deterrent, or is their influence on crime levels minimal?

3. **Trends in Dog-Related Incidents**  
   What are the trends in dog-related incidents, and how do these vary over time and across different locations?

The project combines narrative visualization with interactive elements to provide an engaging, data-driven story for dog owners, enthusiasts, and the general public.

### Motivation 🐾

As a dog owner, I adopted a Staffordshire Bull Terrier named Beau from a shelter. Beau faces challenges with socialising and can sometimes act unpredictably. Given Australia’s strict regulations around dog-related incidents, including hefty fines and potential euthanasia, this project was motivated by a desire to understand patterns in dog ownership and incidents in South Australia, promoting responsible ownership and safety for both dogs and the community.

---

## Data Overview

The analysis uses five large datasets, including one spatial dataset (SHP files). The datasets include:

- Dog ownership demographics (age, gender, council)
- Dog registration, microchipping, and desexing data
- Dog-related incidents (location, leash status, victim type)
- Crime statistics by council
- Spatial boundaries for councils in South Australia

Data sources include **government open data portals**, **Wikipedia (for web scraping)**, and shapefiles for geographic visualization.

---

## Methods and Actions Taken

1. **Data Wrangling & Cleaning in R**  
   - Libraries: `tidyverse`, `dplyr`, `readr`  
   - Data was preprocessed and formatted, aggregated by council and relevant categories, derived metrics (e.g., average dogs per person, responsible ownership percentages) were calculated, and tabular datasets were merged with each other and with spatial data.

2. **Visualisation & Analysis**  
   - Libraries: `ggplot2`, `ggiraph`, `ggcorrplot`, `waffle`, `leaflet`, `networkD3`, `ggExtra`, `ggh4x`, `ggtext`, `showtext`  
   - Charts: circular lollipop plot, Sankey diagram, diverging bar chart (polar coordinates), correlogram, map + bar chart, scatter plot with marginal histograms, waffle chart, time series with conditional area fill.

3. **Interactivity & Storytelling**  
   - Shiny app (`ui.R` + `server.R`) with checkboxes, time sliders, zoomable maps, and tooltips.  
   - Drill-down structure allows users to explore trends, responsible ownership, and incident patterns interactively.

4. **Design Process**  
   - Munzner’s **What-Why-How framework** and **5-sheet design methodology** guided iterative chart selection and layout refinement.  
   - Color palettes (`MetBrewer`, `RColorBrewer`) chosen for clarity and visual attention.  
   - Typography and layout optimized for readability and audience comprehension.

---
## Technical Stack & Key Libraries 🛠️

This **R-based project** is implemented as an **interactive Shiny application**, leveraging a combination of data wrangling, visualisation, and spatial/network tools:

- **Shiny & Interactivity**: `shiny`, `htmlwidgets`, `ggiraph`  
- **Data Wrangling**: `tidyverse`, `dplyr`, `readr`  
- **Visualisation**: `ggplot2`, `ggcorrplot`, `waffle`, `MetBrewer`, `RColorBrewer`, `ggExtra`, `ggh4x`, `ggtext`, `showtext`  
- **Spatial & Network**: `leaflet`, `sf`, `networkD3`  
- **Utilities**: `colorspace`, `stringr` 

---

## Visualisations

### 1. Circular Lollipop Plot
- **Purpose:** Introductory visualisation showing the total number of dogs in each council of South Australia, as well as the overall total across all councils.  
- **Interactivity:** Hover over individual council bars to see the exact number of dogs per council; hover over the center to see the total number of dogs in South Australia.



![Circular Lollipop Plot GIF](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/circular_lollipop.gif)

---

### 2. Sankey Diagram  
- **Purpose:** Shows the flow of dog ownership by owner age and gender across South Australia, illustrating how many dogs are owned by each demographic group. This provides a clear overview of the distribution of dog ownership across different ages and genders.  
- **Interactivity:** Hover over nodes to see the age/gender category and the corresponding number of dogs.



![Sankey Diagram GIF](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/sankey_diagram.gif)

---

### 3. Diverging Bar Chart / Polar Plot  
- **Purpose:** Compares the average number of dogs per person across councils. Councils with above-average dog ownership are highlighted in green, while those below the South Australia average are shown in red, providing an intuitive view of regional differences.  
- **Interactivity:** Hover over bars to see council names and exact averages.



![Polar Plot GIF](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/polar_plot.gif)


---

### 4. Correlogram  
- **Purpose:** Shows correlations between responsible ownership indicators (registration, microchipping, desexing).  

![Correlogram](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/correlogram.png)



---

### 5. Map + Bar Chart  
- **Purpose:** Visualizes the percentage of responsible dog ownership across councils in South Australia. Different colors represent varying levels of responsible ownership, while the accompanying bar chart provides a detailed breakdown of these percentages.  
- **Interactivity:** Zoomable and pannable map, tooltips showing council-specific data, and a checklist to select which ownership criteria to display.


![Map GIF](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/map.gif)


---

### 6. Scatter Plot + Marginal Histograms  
- **Purpose:** Explores the relationship between the number of dogs and crime rates across councils. Histograms provide distributions of both variables, while the scatter plot shows correlations.  
- **Interactivity:** Users can exclude outliers to better observe overall trends.



![Scatter + Hist GIF](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/scatter_hist_demo.gif)
)

---

### 7. Waffle Chart  
- **Purpose:** Shows number of dog-related incidents over time and locations.  
- **Interactivity:** Time slider updates this and the next chart.


![Waffle Chart GIF](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/waffle_chart.gif)


---

### 8. Time Series with Conditional Area Fill  
- **Purpose:** This visualisation explores dog-related incidents by leash status and victim type over time. It allows users to select different leash statuses, compare the types of victims under various conditions across locations and years, and gain a deeper understanding of how leash status influences the nature of incidents in the community.  
- **Interactivity:** Users can filter by leash status.



![Time Series GIF](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/time_series.gif)


---
## Key Findings

### 1. Patterns of Dog Ownership

Dog ownership in South Australia is characterised by clear and consistent demographic and behavioural patterns:

- Owning **one dog** is the most common situation across all age groups and councils, while ownership of three or more dogs remains rare.
- **Women** are generally more likely to own dogs than men, with only a few councils showing the opposite trend among owners of multiple dogs.
- Indicators of responsible ownership — microchipping, desexing, and registration appear largely independent of a dog’s gender.
- Overall levels of **responsible ownership are high** across most councils, though notable regional differences exist.
- The lowest levels are found primarily in northern councils, with Coober Pedy falling below 30%, and several others below 70%, indicating pockets where compliance and awareness may be reduced.



### 2. Dogs and Community Safety

The analysis explores whether dog ownership contributes to neighbourhood safety:

- A **slight negative correlation** indicates that councils with higher numbers of dogs tend to have slightly lower crime rates.
- While this relationship does not imply causation, it suggests that dogs may play a **modest deterrent role**, either through presence, vigilance, or community engagement.
- Additional data would be needed to determine whether this association reflects behavioural effects, demographic patterns, or coincidence.


### 3. Trends in Dog-Related Incidents

Incident data reveal meaningful temporal and spatial variations:

- The number of dog-related incidents **varies substantially over time**, reaching a peak around 2021 before declining sharply in 2024.
- **Footpaths** are the most common setting for incidents, with residential areas and parks appearing less frequently.
- Differences in leash status and victim type across locations and years highlight changing conditions and contextual risk factors.

---
## Project Structure
```text
shiny-dog-visualisation/
│
├─ app/                        # Main Shiny app code
│   ├─ ui.R                     # User interface
│   ├─ server.R                 # Server logic
│   └─ www/                     # Web assets (CSS, images)
│
├─ data/                        # Project data
│   ├─ raw/                     # Raw/unprocessed data
│   └─ processed/               # Processed/aggregated data
│
├─ notebooks/                   # Jupyter / R Notebooks
│   └─ dog_data_preparation.ipynb
│
├─ demo/                        # Demo media: GIFs, images, videos
│
├─ renv/                        # Local R package library (from renv)
│
├─ renv.lock
├─ README.md
├─ .gitignore
```
---
## How to Run the Project
### 1. Clone the repository
```bash
git clone https://github.com/Sveta2732/Svetlana-Portfolio.git
cd Svetlana-Portfolio/shiny-dog-visualisation
```
### 2. Install R and RStudio

Ensure R and RStudio are installed.

### 3. Restore required packages
```bash
install.packages("renv")
renv::restore()
```
### 4. Launch the Shiny app

```bash
shiny::runApp("app")
```
Alternatively, open app/ui.R or app/server.R and click Run App in RStudio.

### Loading Process

The app loads in approximately one minute, in three stages:

1. **Text content** – loads first, so users can start reading immediately.
2. **First half of the plots** – visualizations appear after the text.
3. **Remaining plots** – the last set of visualizations loads last.
---
## Full App Visualization Demo

This GIF/video demonstrates the full loading sequence of the Shiny app.  


![Full App Shiny Demo](https://raw.githubusercontent.com/Sveta2732/Svetlana-Portfolio/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/demo_shiny.gif)


*or, if using a video:*

[Watch Full App Demo Video](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/shiny-dog-visualisation/demo/demo.mp4)

---
## Reflections and Learning Outcomes

Working on this project provided valuable insights into designing data visualisations for both exploration and communication. I strengthened my ability to plan and structure a cohesive narrative using the 5-sheet design approach, ensuring that each visualisation served a clear purpose.  

Through this project, I expanded my visualisation toolkit beyond traditional bar charts, scatter plots, and box plots, incorporating advanced techniques such as Sankey diagrams, polar diverging bars, circular lollipop plots, and interactive maps. This experience enhanced my proficiency in R, Shiny, and multiple specialised libraries, allowing me to create engaging, interactive, and non-standard visualisations.  

If I were to undertake a similar project again, I would allocate more time to exploring the full capabilities of libraries from the start, ensuring maximum use of available features and avoiding implementation constraints.  

Overall, this project reinforced my skills in data analysis, interactive visualisation, and storytelling with data, equipping me with practical expertise directly applicable to professional roles in data science, analytics, and visual communication.
