'''
volby17_MV.py: třetí projekt - webscraper

author: Matyáš Veselý
email: vesel86545@mot.sps-dopravni.cz
discord: reet00 / 701755619501277295
'''

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import csv
from sys import argv
import time as t

#   testovano pomoci odkazu: "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" - Okres Prostějov


def zpracovani_radku(url, cislo, obec, odkaz, tries=3):
    if not cislo or not obec or not odkaz:
        return

    print(f"zpracovávám {obec.get_text()} ({cislo.get_text()})")

    absolute_url = urljoin(url, odkaz.a.get('href'))

    try:
        soup2 = BeautifulSoup(requests.get(absolute_url).content, "html.parser")
        # print(soup2)
    except requests.exceptions.ConnectionError as error:
        print(f"[ERROR] Obec {cislo} nevypsana (ConnectionError). Zbyva {tries - 1} pokusů.")
        t.sleep(5)
        return zpracovani_radku(cislo, obec, odkaz, tries - 1)

    #
    tabulka = soup2.table
    bunky = tabulka.find_all("td")

    volici = bunky[3].get_text().replace('\xa0', '')
    vydane_obalky = bunky[4].get_text().replace('\xa0', '')
    platne_obalky = bunky[7].get_text().replace('\xa0', '')

    data = {
        "code": obec.get_text(),
        "location": cislo.get_text(),
        "registered": volici,
        "envelopes": vydane_obalky,
        "valid": platne_obalky,
    }

    strany = soup2.find("div", {"id": "inner"}).find_all("tr")

    for strana in strany:
        bunky = strana.find_all("td")
        if not bunky:
            continue
        data.update({bunky[1].get_text().replace('\xa0', ''): bunky[2].get_text().replace('\xa0', '')})

    return data


def main():

    url = argv[1]
    nazev = argv[2]


    #   stahnout stranku do promenne    #
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
    except requests.exceptions.ConnectionError as error:
        return


    #   najdeme vsechny tabulky #
    tb = soup.find_all("table")



    #   nejdrive zjisti jestli ma vsechny argumenty, jinak skonci
    #





    souhrn = []


    # prochazi vsechny tabulky na prvni strance,
    for table in tb:
        trow = []


        # prochazi jednotlive radky ve vsech tabulkach "table"
        for tr in table.find_all("tr"):

            # hleda prvky v radku: cislo lokace, nazev lokace, pripise zaznam do csv souboru pro dany radek
            score = zpracovani_radku(
                url = url,
                cislo=tr.find("td", class_ = "cislo"),
                obec=tr.find("td", class_ = "overflow_name"),
                odkaz=tr.find("td", class_ = "cislo")
            )

            if not score:
                continue

            souhrn.append(score)



    #   zapisovani do souboru


    with open(nazev, "w", newline="", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(souhrn[0].keys())
        for zaznam in souhrn:
            zaznam.values()
            spamwriter.writerow(zaznam.values())

if __name__ == "__main__":
    main()
