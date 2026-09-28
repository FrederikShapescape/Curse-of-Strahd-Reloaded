# Combat Tracker — overvejelser og setup

> [!info]+ **Status**
> Frederik bruger allerede et solidt Google Sheets-format (se [[D&D combat tracker 7 - Red Dragon mountain fight.csv]]). Denne fil samler valgmulighederne for fremtidige encountere og dokumenterer formler-formatet så vi kan gentage workflow'en.

---

# Frederiks eksisterende Sheets-format

Kolonner i nuværende combat tracker:

| Kolonne | Indhold | Kilde |
|---|---|---|
| Initiative | Initiative-roll (decimal for tie-breaks, fx 19.7) | Manuel |
| Name | Karakter/fjende-navn | Manuel |
| Turn | Round counter (starter 0) | Manuel |
| AC | Armor Class | Manuel |
| Full health | Max HP | Manuel |
| Health | Current HP | Manuel — opdateres efter hvert hit |
| **Percent** | %-andel HP tilbage | **Formel** `=F2/E2` (formateret som %) |
| **Condition** | Auto-status fra Percent | **Formel** (se nedenfor) |
| Effect | Aktive statuseffekter | Manuel |
| Ends in turn | Hvornår effekten udløber | Manuel |
| EVNER MAN SKAL HUSKE! | DM-noter om særlige features | Manuel |
| CR | Challenge Rating (kun fjender) | Manuel |

## Formler

**Percent (kolonne G):**
```
=F2/E2
```
Format som procent (Format → Number → Percent eller "0%").

**Condition (kolonne H) — nested IF:**
```
=IF(F2<=0,"Dead",IF(G2<=0.1,"Near Death",IF(G2<=0.25,"Bloodied",IF(G2<=0.5,"Injured",IF(G2<1,"Barely Injured","Uninjured")))))
```

Tærskler:
| Percent | Condition |
|---|---|
| 0 eller mindre | **Dead** |
| 0-10% | **Near Death** |
| 10-25% | **Bloodied** |
| 25-50% | **Injured** |
| 50-99% | **Barely Injured** |
| 100% | **Uninjured** |

(Du brugte "Injured" og "Near Death" i din Red Dragon-tracker. Jeg har tilføjet "Bloodied" mellem dem som mellemkategori — fjern den hvis du foretrækker færre niveauer.)

---

# Klar-til-import filer

Jeg har lagt to filer i `Combat Trackers/` mappen:

| Fil | Brug |
|---|---|
| `Combat Tracker - TEMPLATE.csv` | Tom skabelon med formler i Percent og Condition for række 2-13. Kopier og fyld ud per encounter. |
| `Combat Tracker - Arc A - Animated Armor.csv` | Færdig encounter for Death House A2d. Balcony — Animated Armor + alle 4 PCs med stats, evner og Sneak Attack-noter for Sabski. |

## Import-flow til Google Sheets

1. Åbn Google Sheets → File → Import
2. Vælg "Upload" → drag CSV-filen ind
3. Import location: "Replace spreadsheet" eller "Insert new sheet(s)"
4. Separator: Detect automatically (eller "Comma")
5. ✅ Convert text to numbers, dates, and formulas

Formlerne i Percent og Condition aktiveres automatisk når du importerer med "convert to formulas" tjekket.

## Sortering

Sortér efter kolonne A (Initiative) descending når combat starter — så øverste række handler først.

---

# Mulighederne på et brædt

| Løsning | Status | Pro | Con |
|---|---|---|---|
| **A. Google Sheets (din nuværende)** | ✅ Bruges | Fuld formel-power, familiar, god til at vise i sidepanel ved bordet (på iPad/laptop) | Uden for Obsidian, kræver browser |
| **B. Initiative Tracker plugin** | Tilbud | Native HP/AC/init, side-panel altid synligt, integration med statblocks | Kræver plugin-install + opsætning, kort læringskurve |
| **C. Markdown-tabel med Advanced Tables formler** | Tilbud | Native i Obsidian, formler i markdown via `<!-- TBLFM: -->` | Begrænset i forhold til Sheets |

## Min anbefaling

**Bliv ved Google Sheets** — du har et velfungerende format med smarte features (decimal-initiative, auto-condition, EVNER-kolonne). At skifte til en Obsidian-plugin sparer dig ikke tid, og du mister dit eksisterende muscle memory.

**Workflow-forslag:**
1. **Prep i Obsidian** — encounter-narrativ, taktik, foreshadowing, NPC-noter (markdown)
2. **Live tracking i Sheets** — én tab per encounter ved bordet
3. **Link mellem dem** — i markdown-encounter-fil, embedde et link til Sheets-tabben

Det giver dig:
- Sheets til hurtig matematik og initiative-håndtering
- Obsidian til al narrativ kontekst, NPC-evner-noter, callbacks
- Én "single source of truth" for narrativ; én for mekanik

---

# Encounter-CSV-filer fremover

Forslag til navngivning:

```
Combat Trackers/
├── Combat Tracker - TEMPLATE.csv
├── Combat Tracker - Arc A - Animated Armor.csv
├── Combat Tracker - Arc A - Grick.csv
├── Combat Tracker - Arc A - Ghouls.csv
├── Combat Tracker - Arc A - Shadows.csv
├── Combat Tracker - Arc A - Boneless.csv
├── Combat Tracker - Arc A - Flesh Mound.csv
├── Combat Tracker - Arc A - Gustav.csv
├── Combat Tracker - Arc B - Siege Wave 1.csv
├── Combat Tracker - Arc B - Siege Wave 2.csv
├── ... osv
```

Eller alternativt: én master-Sheet i Google Sheets med én tab per encounter, organiseret efter Arc.

---

# PC HP-værdier brugt i template

Bemærk at HP-værdierne i Animated Armor-templaten er beregnede gennemsnit baseret på nuværende karakter-info. **Bekræft de stemmer med spillernes faktiske karakterark inden Session 1:**

| PC | Class @ Lvl 2 | CON | Beregnet HP | Bemærkning |
|---|---|---|---|---|
| Sir Darius (Bentley) | Paladin 2 | 13 (+1) | **18** | (10+1) + (6+1) = 18 |
| Anders | Bard 2 | 14 (+2) | **17** | (8+2) + (5+2) = 17 |
| Bogoris | Druid 1 / Warlock 1 | 16 (+3) | **19** | (8+3) + (5+3) = 19 |
| Håkan (Sabski) | Rogue 2 | 12 (+1) | **15** | (8+1) + (5+1) = 15 |

Disse antager **gennemsnit-rul på lvl 2 HD**. Hvis nogen rullede deres lvl 2 HP, juster CSV'erne tilsvarende.

---

# Næste skridt

Sig hvad du vil have:

1. **Bygge resten af Death House-encounterene** som CSV'er i samme format (Grick, Ghouls, Shadows, Boneless, Flesh Mound, Gustav) — jeg kan have dem klar i `Combat Trackers/`-mappen
2. **Bygge Arc B-encounterene** (Siege bølger 1/2/3, Town Square Plague Spreader)
3. **Bygge Arc C-encounterene** (Strix, Wolves, Werewolves)
4. **Bygge en master Google Sheets-template** med faner per Arc — i så fald kan jeg skrive en singel CSV fil og du importerer som flere tabs

Lad mig vide om du vil have alle Death House-encounterene først, eller om du vil teste Animated Armor-CSV'en alene først for at se om format-matchet fungerer.