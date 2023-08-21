import requests
from bs4 import BeautifulSoup
import os

class Exam:
    def __init__(self , siraNo, daireBakanlik, kadroAdi, sinavKonulari, pdfLinkleri, sinavTarihi, sinavCagrisi):
        self.siraNo = siraNo
        self.daireBakanlik = daireBakanlik
        self.kadroAdi = kadroAdi
        self.sinavKonulari = sinavKonulari # can be list 
        self.pdfLinkleri = pdfLinkleri # can be list 
        self.sinavTarihi = sinavTarihi # can be list
        self.sinavCagrisi = sinavCagrisi
        

url = "https://khk.gov.ct.tr/YAZILI-SINAV-TAR%C4%B0HLER%C4%B0"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table", {"align": "center", "border": "1", "cellpadding": "5", "cellspacing": "5", "style": "width:1100px"})
tbody = table.find("tbody")
trs = tbody.find_all("tr")
examList = []
for tr in trs[2:]:
    tds = tr.find_all("td")
    
    # Check if there are enough elements in tds
    if len(tds) >= 6:
        siraNo = tds[0].text
        daireBakanlik = tds[1].text
        kadroAdi = tds[2].text if tds[2].text else ""  # Handle the case where kadroAdi is missing
        sinavKonulari = []
        pdfLinkleri = []
        sinavTarihi = []

        # Check if there are links in the third column (index 2)
        if tds[3].find("a"):
            for td in tds[3].find_all("a"):
                sinavKonulari.append(td.text)
                pdfLinkleri.append(td["href"])

        # Check if there are dates in the fourth column (index 3)
        if tds[4].find("span"):
            for td in tds[4].find_all("span"):
                sinavTarihi.append(td.text)

        sinavCagrisi = tds[5].text
        exam = Exam(siraNo, daireBakanlik, kadroAdi, sinavKonulari, pdfLinkleri, sinavTarihi, sinavCagrisi)
        examList.append(exam)

if not os.path.exists("pdfs"):
    os.makedirs("pdfs")
for exam in examList:
    for i in range(len(exam.pdfLinkleri)):
        try:
            pdfUrl = "https://khk.gov.ct.tr" + exam.pdfLinkleri[i]
            pdfResponse = requests.get(pdfUrl)
            with open("pdfs/"+exam.siraNo+"-ST-"+exam.sinavTarihi[i] +"+DB-" + exam.daireBakanlik + "+KA-" + exam.kadroAdi +   ".pdf", "wb") as f:                f.write(pdfResponse.content)

        except:
            print("Dosya indirilirken hata olustu " + exam.siraNo + " " + exam.daireBakanlik + " " + exam.kadroAdi + " " + exam.sinavTarihi[i])
