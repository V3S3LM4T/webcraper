"""
projekt_3.py: třetí projekt
author: Matyas Vesely
email: matyves01@gmail.com@gmail.com
discord: reet00
"""
import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://volby.cz/pls/ps2017nss/"

def get_obce(url):
    page = requests.get(url)
    page.encoding = "utf-8" #pry to pomaha zobrazit hacky a carky
    soup = BeautifulSoup(page.text, "html.parser")
    
    obce = []
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 3:
            cislo_tag = cells[0].find("a")
            nazev = cells[1].get_text(strip=True)
            vyber_tag = cells[2].find("a") 
            
            if cislo_tag and vyber_tag:
                cislo = cislo_tag.get_text(strip=True)
                href = vyber_tag.get("href") 
                obce.append({
                    "cislo": cislo,
                    "nazev": nazev,
                    "href": href
                })
    return obce

def get_detail(href):
    url = BASE_URL + href
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    
    data = {}
    
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if cells:
                for i, cell in enumerate(cells):
                    if i < len(headers) and headers[i]:
                        data[headers[i]] = cell.get_text(strip=True)
    
    return data

def main():
    hlavni_url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    
    print("Stahuji seznam obcí...")
    obce = get_obce(hlavni_url)
    print(f"Nalezeno {len(obce)} obcí")
    
    vysledky = []
    
    for obec in obce:
        print(f"Zpracovávám: {obec['nazev']}...")
        detail = get_detail(obec["href"])
        
        radek = {
            "code": obec["cislo"],
            "location": obec["nazev"],
            **detail  # přidá všechny sloupce z detailu
        }
        vysledky.append(radek)
        time.sleep(0.3)  # slušnost vůči serveru
    
    # Zápis do CSV
    if vysledky:
        fieldnames = list(vysledky[0].keys())
        with open("vysledky.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(vysledky)
        print("Hotovo! Uloženo do vysledky.csv")

if __name__ == "__main__":
    main()

