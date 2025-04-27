import pandas as pd

input_file = "/Users/adityamurthy/DartMonkeyDataFest/external_data/employee_growth/homeowner.txt"
output_file = "/Users/adityamurthy/DartMonkeyDataFest/external_data/employee_growth/homeowner_unique.csv"

try:
    # Read the file
    df = pd.read_csv(input_file, delimiter=";", encoding="utf-8")
    
    # Check if the DataFrame is empty
    print("DataFrame shape (rows, columns):", df.shape)
    print("Columns:", df.columns.tolist())
    print("First few rows:\n", df.head(5))
    
    # Check duplicates
    print("Rows before dropping duplicates:", len(df))
    df = df.drop_duplicates()
    print("Rows after dropping duplicates:", len(df))
    
    # Write to output
    if not df.empty:
        df.to_csv(output_file, sep=";", index=False)
        print(f"File saved to {output_file}")
        # Verify the output file
        output_df = pd.read_csv(output_file, delimiter=";")
        print("Output file shape:", output_df.shape)
    else:
        print("DataFrame is empty, no file written.")
        
except FileNotFoundError:
    print(f"Input file not found: {input_file}")
except pd.errors.EmptyDataError:
    print("Input file is empty or invalid.")
except pd.errors.ParserError:
    print("Error parsing the file. Check delimiter or file format.")
except Exception as e:
    print(f"An error occurred: {str(e)}")