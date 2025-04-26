library(tidyverse)

setwd(here::here())
leases <- read_csv('data/Leases.csv')  

# Filter for Dallas leases
dallas_leases <- leases %>%
  filter(str_detect(market, regex("Dallas", ignore_case = TRUE))) %>%
  filter(year >= 2018, year <= 2024) %>%
  filter(leasedSF >= 5000, leasedSF <= 50000)

# Split into pre- and post-COVID
pre_covid <- dallas_leases %>% filter(year < 2020) %>% pull(leasedSF)
post_covid <- dallas_leases %>% filter(year >= 2020) %>% pull(leasedSF)

# Two-Sample t-test
t_test_result <- t.test(pre_covid, post_covid, var.equal = FALSE)

cat("Pre-COVID Mean Lease Size:", mean(pre_covid, na.rm = TRUE), "sqft\n")
cat("Post-COVID Mean Lease Size:", mean(post_covid, na.rm = TRUE), "sqft\n")
cat("T-Statistic:", t_test_result$statistic, "\n")
cat("P-Value:", t_test_result$p.value, "\n")

if (t_test_result$p.value < 0.05) {
  cat("Result: Statistically significant difference — lease sizes changed after COVID.\n")
} else {
  cat("Result: No statistically significant difference — lease sizes stayed about the same.\n")
}