library(dplyr)
library(ggplot2)

# Load data
leases <- read.csv("data/Leases.csv")
kastle <- read.csv("data/Major Market Occupancy Data-revised.csv")


# Calculate 2024 Q3 average occupancy for each city
final_occupancy <- kastle %>%
  filter(year == 2024, quarter == "Q3", market %in% c("Dallas/Ft Worth", "Manhattan", "San Francisco")) %>%
  mutate(city = case_when(
    market == "Dallas/Ft Worth" ~ "Dallas",
    market == "Manhattan" ~ "New York",
    market == "San Francisco" ~ "San Francisco"
  )) %>%
  group_by(city) %>%
  summarise(final_avg_occupancy = mean(avg_occupancy_proportion, na.rm = TRUE) * 100)

print(final_occupancy)


# Find the quarter where occupancy bottomed out for each city
lowest_point <- kastle %>%
  filter(market %in% c("Dallas/Ft Worth", "Manhattan", "San Francisco")) %>%
  mutate(city = case_when(
    market == "Dallas/Ft Worth" ~ "Dallas",
    market == "Manhattan" ~ "New York",
    market == "San Francisco" ~ "San Francisco"
  )) %>%
  group_by(city) %>%
  slice_min(avg_occupancy_proportion, with_ties = FALSE)

print(lowest_point)


# --- Lease Size Analysis ---

# Filter for Dallas, Manhattan, San Francisco
leases_filtered <- leases %>%
  filter(grepl("Dallas|Manhattan|San Francisco", market, ignore.case = TRUE)) %>%
  mutate(city = case_when(
    grepl("Dallas", market, ignore.case = TRUE) ~ "Dallas",
    grepl("Manhattan", market, ignore.case = TRUE) ~ "New York",
    grepl("San Francisco", market, ignore.case = TRUE) ~ "San Francisco"
  ))

# Average Leased Square Footage
leases_filtered %>%
  group_by(city) %>%
  summarise(avg_leasedSF = mean(leasedSF, na.rm = TRUE)) %>%
  ggplot(aes(x = city, y = avg_leasedSF, fill = city)) +
  geom_col() +
  labs(title = "Average Lease Size by City (2018-2024)",
       y = "Avg Leased Square Feet",
       x = "City") +
  scale_fill_manual(values = c("navyblue", "firebrick", "forestgreen")) +
  theme_minimal()

# Number of Leases
leases_filtered %>%
  group_by(city) %>%
  summarise(num_leases = n()) %>%
  ggplot(aes(x = city, y = num_leases, fill = city)) +
  geom_col() +
  labs(title = "Total Number of Leases by City (2018-2024)",
       y = "Number of Leases",
       x = "City") +
  scale_fill_manual(values = c("navyblue", "firebrick", "forestgreen")) +
  theme_minimal()

# --- Occupancy Rate Analysis ---

# Occupancy Latest (2024 Q3)
kastle_filtered <- kastle %>%
  filter(market %in% c("Dallas/Ft Worth", "Manhattan", "San Francisco")) %>%
  mutate(city = case_when(
    market == "Dallas/Ft Worth" ~ "Dallas",
    market == "Manhattan" ~ "New York",
    market == "San Francisco" ~ "San Francisco"
  ))

kastle_latest <- kastle_filtered %>%
  group_by(city) %>%
  summarise(latest_occupancy = last(avg_occupancy_proportion) * 100)

# Latest Occupancy Rate
ggplot(kastle_latest, aes(x = city, y = latest_occupancy, fill = city)) +
  geom_col() +
  geom_hline(yintercept = 100, linetype = "dashed", color = "red", size = 1.2) +
  labs(title = "Office Occupancy Rate by City (2024 Q3)",
       y = "Occupancy Rate (%)",
       x = "City") +
  scale_fill_manual(values = c("navyblue", "firebrick", "forestgreen")) +
  theme_minimal()


# ----- lowest occupancy rate ------ 
lowest_occupancy <- data.frame(
  city = c("Dallas", "New York", "San Francisco"),
  occupancy_2020Q2 = c(27.2, 5.2, 9.1)
)

ggplot(lowest_occupancy, aes(x = city, y = occupancy_2020Q2, fill = city)) +
  geom_col() +
  labs(title = "Minimum Office Occupancy During COVID Crash (2020 Q2)",
       y = "Occupancy Rate (%)",
       x = "City") +
  scale_fill_manual(values = c("navyblue", "firebrick", "forestgreen")) +
  theme_minimal()

latest_occupancy <- data.frame(
  city = c("Dallas", "New York", "San Francisco"),
  occupancy_2024Q3 = c(57.5, 47.5, 41.5)
)

library(scales)


ggplot(leases_filtered, aes(x = leasedSF, color = city)) +
  geom_density(size = 1.8) +
  geom_vline(xintercept = c(5000, 50000), linetype = "dashed", color = "gray40", size = 0.8) +
  scale_color_manual(values = c("navyblue", "firebrick", "forestgreen")) +
  scale_x_log10(labels = comma) +
  labs(
    title = "Lease Size Distribution by City (2018–2024)",
    x = "Leased Square Feet (Log Scale)",
    y = "Density",
    color = "City"
  ) +
  theme_minimal(base_size = 16) +
  theme(
    plot.title = element_text(face = "bold", size = 20, margin = margin(b = 10)),
    plot.subtitle = element_text(size = 14, margin = margin(b = 15)),
    axis.text.x = element_text(size = 12),
    axis.text.y = element_text(size = 12),
    legend.position = "bottom",
    legend.title = element_blank(),
    legend.text = element_text(size = 13),
    plot.margin = margin(10, 15, 10, 15)
  )