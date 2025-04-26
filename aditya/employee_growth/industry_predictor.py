import csv
import pandas as pd
from transformers import pipeline
import uuid

# Define the input and output file paths
input_file = "/Users/adityacode/DartMonkeyDataFest/aditya/employee_growth/search_results.txt"  # Replace with your semicolon-separated text file
output_file = "/Users/adityacode/DartMonkeyDataFest/aditya/employee_growth/employees.csv"

# Define possible industry labels
industries = [
    "Technology",
    "Healthcare",
    "Finance",
    "Education",
    "Manufacturing",
    "Government",
    "Legal Services",
    "Retail",
    "Other"
]

# Load the zero-shot classification pipeline with BART-MNLI
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device='cuda:0')

# Read the semicolon-separated text file
try:
    # Read all columns dynamically, assuming the first 3 columns are address, name, search_results
    df = pd.read_csv(input_file, sep=";", header=None, on_bad_lines="warn", quoting=csv.QUOTE_ALL)
    if df.shape[1] < 3:
        raise ValueError("Input file must have at least 3 columns.")
    # Rename the first three columns
    df.columns = ["address", "name", "search_results"] + [f"col{i}" for i in range(3, df.shape[1])]
except Exception as e:
    print(f"Error reading input file: {e}")
    exit(1)

# Function to predict industry from search results
def predict_industry(search_text):
    try:
        if pd.isna(search_text) or not isinstance(search_text, str):
            return "Other"
        # Truncate text to 512 tokens (model's max length)
        result = classifier(search_text, candidate_labels=industries, multi_label=False)
        return result["labels"][0]  # Return the top predicted industry
    except Exception as e:
        print(f"Error processing text: {e}")
        return "Other"

# Apply the prediction to the search_results column
df["predicted_industry"] = df["search_results"].apply(predict_industry)

# Select relevant columns for output
output_df = df[["address", "name", "predicted_industry"]]

# Save the results to a CSV file
try:
    output_df.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")
except Exception as e:
    print(f"Error saving output file: {e}")