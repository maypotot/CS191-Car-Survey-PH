import PyPDF2
import re
import json

def extract_text():
    pdfFile = open(r"pdfscraping/Repo-Units-for-Bidding-as-of-Sept-20-2024_v2_compressed.pdf", 'rb')
    pdf_reader = PyPDF2.PdfReader(pdfFile)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def parse_motorcycle_info(text):
    # Updated regex pattern to capture Brand and Model separately
    pattern = re.compile(
        r'(?P<mileage>\d+(\.\d+)?)\s+'         # Mileage
        r'(?P<price>[\d,]+\.\d{2})\s+'         # Price with decimal
        r'(?P<brand>[A-Z]+)\s+'                # Brand (one uppercase word)
        r'(?P<model>[^\n]*)'       # Model (additional words, numbers, and symbols)
    )

    motorcycles = []

    for match in pattern.finditer(text):
        motorcycle_info = {
            "Brand": match.group("brand"),
            "Model": match.group("model").strip(),
            "Mileage": float(match.group("mileage")),
            "Price": float(match.group("price").replace(",", ""))
            
        }
        motorcycles.append(motorcycle_info)

    return motorcycles

def save_to_json(data, filename="sbfinancemotorcycles.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

# Example usage
text = extract_text()
motorcycle_data = parse_motorcycle_info(text)
save_to_json(motorcycle_data)
