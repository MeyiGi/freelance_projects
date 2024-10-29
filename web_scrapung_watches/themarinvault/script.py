import os
import pandas as pd

def combine_excel_files(output_filename="combined_file.xlsx"):
    # Get all Excel files in the current directory
    excel_files = [file for file in os.listdir() if file.endswith('.xlsx') or file.endswith('.xls')]

    # Check if there are any Excel files
    if not excel_files:
        print("No Excel files found in the current directory.")
        return

    # List to store each DataFrame
    dataframes = []

    # Read each Excel file and append it to the list
    for file in excel_files:
        df = pd.read_excel(file)
        dataframes.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the combined DataFrame to a new Excel file
    combined_df.to_excel(output_filename, index=False)
    print(f"Combined file saved as '{output_filename}'")

# Run the function
combine_excel_files()
