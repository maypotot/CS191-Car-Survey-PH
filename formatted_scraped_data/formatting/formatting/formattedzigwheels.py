import json
import os

# Read JSON data from a file
with open("webscraping/zigwheels_data.json", "r", encoding="utf-8") as file:
    vehicles = json.load(file)

# Function to split vehicle_name into Maker, Model, and Variant
def split_vehicle_name(vehicle_name):
    parts = vehicle_name.split()
    
    maker = parts[0]  # The first word is usually the brand (Maker)
    model = parts[1] if len(parts) > 1 else ""  # The second word is the model
    variant = " ".join(parts[2:]) if len(parts) > 2 else "Standard"  # Remaining words are the variant
    
    return maker, model, variant

# Process each vehicle entry
for vehicle in vehicles:
    maker, model, variant = split_vehicle_name(vehicle["vehicle_name"])
    
    vehicle["Maker"] = maker
    vehicle["Model"] = model
    vehicle["Variant"] = variant
    
    # Remove old field
    del vehicle["vehicle_name"]



# Save the updated JSON
with open("Formatted Scraped Data/zigwheels_updated.json", "w", encoding="utf-8") as file:
    json.dump(vehicles, file, indent=4)

print(f"Updated JSON saved")
