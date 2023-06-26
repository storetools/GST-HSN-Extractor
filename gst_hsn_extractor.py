import requests
import pandas as pd
import json
import io
import math


url = "https://tutorial.gst.gov.in/downloads/HSN_SAC.xlsx"
response = requests.get(url)
excel_data = response.content
hsn_sheet = pd.read_excel(io.BytesIO(excel_data), sheet_name="HSN")
hsn_columns = hsn_sheet.columns.tolist()


hsn_data = []

for index, row in hsn_sheet.iterrows():
    hsn_code = row[hsn_columns[0]]
    hsn_description = row[hsn_columns[1]]

    # Check if the description is not NaN
    if not isinstance(hsn_description, float) or not math.isnan(hsn_description):
        hsn_description = str(hsn_description).split(",")  # Split the description by commas

        hsn_entry = {
            "HSN Code": hsn_code,
            "HSN Description": hsn_description
        }

        # Add the HSN entry to the data dictionary
        hsn_data.append(hsn_entry)

# Convert the HSN data to JSON
hsn_json = json.dumps(hsn_data, indent=4)

# Print the JSON data
print(hsn_json)
