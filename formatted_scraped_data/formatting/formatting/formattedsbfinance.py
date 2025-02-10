import json
import random

# Step 1: Read JSON data from a file
with open("sbfinancemotorcycles.json", "r", encoding="utf-8") as file:
    motorcycles = json.load(file)

# Function to separate model and variant
def split_model_variant(model_name):
    parts = model_name.split()
    
    # Identify numbers in the model name (e.g., "125", "150", "160") as part of the model
    model_parts = []
    variant_parts = []
    for part in parts:
        if part.isdigit() or part.replace('(', '').replace(')', '').isdigit():  
            model_parts.append(part)
        elif not model_parts:  
            model_parts.append(part)  # Still part of the main model
        else:
            variant_parts.append(part)  # Everything after the model is variant

    model = " ".join(model_parts)
    variant = " ".join(variant_parts) if variant_parts else "Standard"

    return model, variant

# Step 2: Process each vehicle entry
for motorcycle in motorcycles:
    model, variant = split_model_variant(motorcycle["Model"])
    motorcycle["Model"] = model
    motorcycle["Variant"] = variant

# Step 3: Save the updated JSON back to a new file
with open("Formatted Scraped Data/sbfinance_updated.json", "w", encoding="utf-8") as file:
    json.dump(motorcycles, file, indent=4)

print("Updated JSON has been saved to 'vehicles_updated.json'.")
