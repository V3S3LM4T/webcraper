# Volební scraper

Python skript pro stahování výsledků voleb z webu [voleb](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a jejich uložení do CSV souboru.

## Popis

Skript prochází stránku s výsledky voleb pro daný kraj/okres, stáhne data za každou obec (počty voličů, vydané a platné obálky, výsledky stran) a zapíše je do CSV souboru.

Instalace závislostí:

```bash
pip install requests beautifulsoup4
```

## Použití

```bash
python volby.py <URL> <název_souboru.csv>
```

**Argumenty:**

| Argument | Popis |
|---|---|
| `<URL>` | Odkaz na stránku s výsledky voleb pro daný okres/kraj |
| `<název_souboru.csv>` | Název výstupního CSV souboru |

**Příklad:**

```bash
python volby.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_olomouc.csv
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
- Výstupní soubor je kódován v UTF-8.
