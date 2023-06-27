import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://cleartax.in/s/gst-rates"

link_list = []
json_list = []
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
h2_tag = soup.find("h2", id="GST")

# Find the sibling figure tag
figure_tag = h2_tag.find_next_sibling("figure")

if figure_tag and figure_tag.find("table"):
    table = figure_tag.find("table")
    td_elements = table.find_all("td")

    for td in td_elements:
        link = td.find("a")
        if link:
            href = link.get("href")
            link_list.append(href)
else:
    print("Figure tag or table not found with the specified structure.")

for link in link_list:
  # Send a GET request to the website
  response = requests.get(link)

  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")

  # Find the element with the id "hsn-sac-table-container"
  element = soup.find(id="hsn-sac-table-container")

  # Check if the element is found
  if element:
      # Find the table within the element
      table = element.find("table")

      # Check if a table is found
      if table:
          # Extract the table data using pandas
          table_data = pd.read_html(str(table))
          extracted_table = table_data[0]  # Assuming the table is the first one within the element

          # Convert table data to JSON
          json_data = extracted_table.to_json(orient="records")
          json_list = json_list + json.loads(json_data)
      else:
          print("Table not found within the element.")
  else:
      print("Element with id 'hsn-sac-table-container' not found.")
      
      
print(json_list)
with open("gst-hsn.json", "w") as f:
            f.write(json.dumps(json_list))
