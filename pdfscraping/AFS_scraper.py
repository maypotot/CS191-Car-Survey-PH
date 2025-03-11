import pandas as pd

# Load the CSV file
csv_file = "pdfscraping/AFS.csv"
df = pd.read_csv(csv_file)

# Convert to JSON
json_file = "AFS.json"
df.to_json(json_file, orient="records", indent=4)  # "records" creates a list of dictionaries

print(f"JSON file saved as {json_file}")