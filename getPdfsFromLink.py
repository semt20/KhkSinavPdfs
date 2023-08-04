import requests
from bs4 import BeautifulSoup
import os

url = "https://khk.gov.ct.tr/YAZILI-SINAV-TAR%C4%B0HLER%C4%B0"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
pdf_links = soup.find_all("a", href=lambda href: href and ".pdf" in href)
if not os.path.exists("pdfs"):
    os.makedirs("pdfs")
for link in pdf_links:
    pdf_url = "https://khk.gov.ct.tr" +link.get("href").split("?")[0] 
    response = requests.get(pdf_url)
    filename = pdf_url.split("/")[-1]
    with open(os.path.join("pdfs", filename), "wb") as f:
        f.write(response.content)
