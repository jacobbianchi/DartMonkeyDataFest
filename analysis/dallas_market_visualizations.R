library(dplyr)
library(ggplot2)
library(ggrepel)


# Load and filter
kastle <- read.csv("data/Major Market Occupancy Data-revised.csv")
dallas_kastle <- kastle %>%
  filter(market == "Dallas/Ft Worth") %>%
  mutate(year_quarter = paste(year, quarter, sep = " "))

ny_kastle <- kastle %>%
  filter(market == "Manhattan") %>%
  mutate(year_quarter = paste(year, quarter, sep = " "))

sf_kastle <- kastle %>%
  filter(market == "San Francisco") %>%
  mutate(year_quarter = paste(year, quarter, sep = " "))

library(dplyr)
library(ggplot2)

# Load data
kastle <- read.csv("data/Major Market Occupancy Data-revised.csv")

# Prepare each city's data
dallas_kastle <- kastle %>%
  filter(market == "Dallas/Ft Worth") %>%
  mutate(year_quarter = paste(year, quarter, sep = " "), city = "Dallas")

ny_kastle <- kastle %>%
  filter(market == "Manhattan") %>%
  mutate(year_quarter = paste(year, quarter, sep = " "), city = "New York")

sf_kastle <- kastle %>%
  filter(market == "San Francisco") %>%
  mutate(year_quarter = paste(year, quarter, sep = " "), city = "San Francisco")

# Combine all three into one
combined_kastle <- bind_rows(dallas_kastle, ny_kastle, sf_kastle)
library(dplyr)
library(ggplot2)

# Assume combined_kastle already created

ggplot(combined_kastle, aes(x = year_quarter, y = avg_occupancy_proportion * 100, color = city, group = city)) +
  geom_line(size = 2) +                     # Thicker trend lines
  geom_point(size = 3) +
geom_hline(yintercept = 100, linetype = "dashed", color = "red", size = 1.5) +   # Thicker baseline
  labs(
    title = "Dallas Leads Office Market Recovery Post-COVID",
    subtitle = "Dallas rebounds faster than New York and San Francisco (relative to pre-pandemic baseline)",
    x = "Quarter",
    y = "Average Occupancy Rate (%)",
    color = "City",
    caption = "Source: Kastle Systems, Savills Data Analysis"
  ) +
  scale_color_manual(values = c("Dallas" = "navyblue", "New York" = "firebrick", "San Francisco" = "forestgreen")) +
  scale_x_discrete(breaks = unique(combined_kastle$year_quarter)[seq(1, length(unique(combined_kastle$year_quarter)), by = 2)]) + # Show every other quarter
  theme_minimal(base_size = 15) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
    axis.text.y = element_text(size = 12),
    plot.title = element_text(face = "bold", size = 18),
    plot.subtitle = element_text(size = 14),
    legend.title = element_text(size = 13),
    legend.text = element_text(size = 12),
    panel.grid.minor = element_blank()   # Remove minor grid clutter
  )
+ coord_cartesian(ylim = c(0, 100))

