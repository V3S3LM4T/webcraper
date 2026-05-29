# Volební scraper

Python skript pro stahování výsledků voleb z webu a jejich uložení do CSV souboru. ( [web](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) )

## Popis

Skript prochází stránku s výsledky voleb pro daný kraj/okres, stáhne data za každou obec (počty voličů, vydané a platné obálky, výsledky stran) a zapíše je do CSV souboru.



**Jak program použít?**
Spouštíme pomocí dvou argumentů:
| Argument | Popis |
|---|---|
| `<URL>` | Odkaz na stránku s výsledky voleb pro daný okres/kraj |
| `<název_souboru.csv>` | Název výstupního CSV souboru |

**Příklad:**

```bash
python volby17_MV.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_olomouc.csv
```

## Výstup

CSV soubor oddělený středníkem (`;`) s následujícími sloupci:

| Sloupec | Popis |
|---|---|
| `code` | Název obce |
| `location` | Číslo obce/lokace |
| `registered` | Počet registrovaných voličů |
| `envelopes` | Počet vydaných obálek |
| `valid` | Počet platných hlasů |
| `strana` | Počet hlasů pro každou stranu |

## Poznámky

- Skript automaticky opakuje pokus o stažení (až 3×) při výpadku spojení.
- Mezi opakovanými pokusy čeká 5 sekund.
- Odkaz vkládat mezi uvozovky
- Výstupní soubor je kódován v UTF-8.
