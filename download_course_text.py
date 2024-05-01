import requests
from bs4 import BeautifulSoup
import os
from rs_html import html_content

# HTML content provided by the user (for the sake of example, this is simplified)

soup = BeautifulSoup(html_content, 'html.parser')
accordions = soup.find_all('div', class_='accordion')
panels = soup.find_all('div', class_='panel')

# Ensure the output directory exists
output_dir = "downloaded_pdfs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to download a PDF file
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")

# Loop through each accordion and its corresponding panel
for accordion, panel in zip(accordions, panels):
    language = accordion.text.strip()
    links = panel.find_all('a')
    for link in links:
        pdf_url = link['href']
        unit_info = link.text.strip()
        filename = f"{output_dir}/" + f"{language} - {unit_info}.pdf".replace(" ", "_").replace("/", "-")
        download_pdf(pdf_url, filename)

print("All PDFs have been downloaded.")

