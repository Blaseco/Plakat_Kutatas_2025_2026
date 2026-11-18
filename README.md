# Bibó István Szakkollégium · AI Kurzus 2026 Ősz
## Mesterséges intelligencia a társadalom- és politikatudományi kutatásban
**Oktató:** Dr. Sebők Miklós (Syracuse University / poltextLAB)  
**Hallgató:** Varga Balázs  
**Kutatási téma:** A 2025–2026-os magyar óriásplakát-kampányok összehasonlító tartalomelemzése, szemiotikai vizsgálata és gépi kódolása  

---

## 🔗 KÖZVETLEN ELÉRÉSI LINKEK (Weboldal, Skill, Beadandók)

### 🌐 Interaktív Webes Felületek (GitHub Pages):
* **Plakát-összehasonlító és elemző webapp:** [https://blaseco.github.io/Plakat_Kutatas_2025_2026/comparison.html](https://blaseco.github.io/Plakat_Kutatas_2025_2026/comparison.html)  
* **vposter Skill bemutató és tesztelő webapp:** [https://blaseco.github.io/Plakat_Kutatas_2025_2026/vposter_skill_bemutato.html](https://blaseco.github.io/Plakat_Kutatas_2025_2026/vposter_skill_bemutato.html)  
* **Főoldal (GitHub Pages):** [https://blaseco.github.io/Plakat_Kutatas_2025_2026/index.html](https://blaseco.github.io/Plakat_Kutatas_2025_2026/index.html)

### ⚙️ A Saját Fejlesztésű vposter Skill:
* **A Skill forráskódja a repóban:** [skills/vposter/](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/tree/main/skills/vposter)
* **Skill definíció (SKILL.md):** [skills/vposter/SKILL.md](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/skills/vposter/SKILL.md)
* **Skill műszaki specifikáció PDF (2 oldal):** [VPOSTER_Skill_Bemutato_es_Specifikacio_Varga_Balazs.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/VPOSTER_Skill_Bemutato_es_Specifikacio_Varga_Balazs.pdf)

### 📄 Hivatalos Akadémiai Beadandók:
* **Rövid írásos elemzés (Block 4 · pontosan 3 oldal, Times New Roman tudományos folyóirat-formátum):** [Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf)
* **Kódkönyv és validáció (Block 3 · pontosan 2 oldal, forrás, napló, ID, validáció, beágyazott MI-nyilatkozat):** [Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf)
* **Opponensi értékelő lap és szóbeli vita forgatókönyv (Block 4 opponálás):** [Opponensi_Ertekelo_Lap_es_Reprodukcios_Jelentes_Varga_Balazs.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/Opponensi_Ertekelo_Lap_es_Reprodukcios_Jelentes_Varga_Balazs.pdf)
* **Reprodukciós mesterkód (Slide 45 egyparancsos futás):** [reproduce.py](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/reproduce.py)

---

## 📌 1. A Kurzuskövetelmények Teljesülése

A projekt Dr. Sebők Miklós kurzusának módszertani követelményei (*Block 3: Measurement and analysis: coding, classification, validation*, Slide 1–47) alapján készült:

1. **Rövid írásos elemzés (PDF, legfeljebb 3 oldal táblázatokkal és ábrákkal - Slide 45):**
   * Fájl: `Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf`
   * Terjedelem: **Pontosan 3 oldal** (1. oldal: Kutatási kérdés, operacionalizálás, zárt kódkönyv; 2. oldal: Table 1 booktabs táblázat, 1. és 2. ábra, leíró statisztika; 3. oldal: Gépi kódolás, κ=1.000 megbízhatóság, Rogan–Gladen kalibráció, szakirodalom és a beágyazott MI-nyilatkozat).
2. **Kódkönyv (Codebook) akadémiai formátumban (Slide 4, 18):**
   * Fájl: `Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf` (pontosan 2 oldal: forrás, napló, azonosító, validálás és beágyazott MI-nyilatkozat).
3. **Kész adatbázis SQL és CSV formátumban (Block 3 követelmény):**
   * `plakat_kutatas_korpusz_2025_2026.csv` (Standard UTF-8 CSV, 22 mezővel, zérus hiányzó értékkel)
   * `plakat_kutatas_korpusz_2025_2026_excel.csv` (Magyar Excel BOM pontosvesszős formátum)
   * `plakat_adatbazis_2025_2026.sql` (Relációs SQL DDL táblaszerkezet és DML INSERT adatblokk)
   * `plakat_adatbazis_2025_2026.db` (Közvetlenül lekérdezhető SQLite adatbázis)
   * `ParlLawSpeech_Plakat_Korpusz_2025_2026.json` (Strukturált JSON export)
4. **Önálló reprodukciós repó és script (Slide 40 & 45):**
   * *"THE POINT: Your opponent reproduces your numbers, so the repo has to run without you."*
   * Futtatás egyetlen parancssori utasítással:
     ```bash
     python3 reproduce.py
     ```
   * A script emberi segítség nélkül ellenőrzi az adatbázis teljességét, újraszámolja a megbízhatóságot (κ = 1.000), előállítja a leíró táblázatot (Table 1), determinisztikusan újragenerálja a diagramokat, és elvégzi a Rogan–Gladen mérési hiba korrekciót.

---

## 🚀 2. Gyorsindítási Útmutató az Opponensnek

1. Repó klónozása:
   ```bash
   git clone https://github.com/Blaseco/Plakat_Kutatas_2025_2026.git
   cd Plakat_Kutatas_2025_2026
   ```
2. Reprodukciós teszt futtatása:
   ```bash
   python3 reproduce.py
   ```
3. A vposter skill önellenőrzése és regressziós tesztje:
   ```bash
   python3 skills/vposter/scripts/selftest.py
   ```
4. Teljes körű minőségbiztosítási audit futtatása:
   ```bash
   python3 final_success_audit.py
   ```

---

## 📊 3. A Korpusz és az Elemzés Fő Eredményei

* **Mintaelemszám ($n=13$):** 2025–2026-os hazai politikai óriásplakátok teljes körű, képpel dokumentált mintája.
* **Fővizuális dominancia elve:** A plakát elsődleges vizuális fókusza határozza meg a kódolást.
* **Megbízhatóság:** Humán arany standard (`hand.csv`) és gépi kódolás (`labels.csv`) közötti egyezés $\kappa = 1.0000$ (Observed agreement: 100%).
* **Eredmény összefoglalás:** A kormánypárti és CÖF plakátok domináns része (63.6%) perszonifikált, külső szereplőket démonizáló negatív kampányeszköz, míg az ellenzéki mintában kizárólag pozitív, programalapú vagy intézményi mozgósítás jelent meg.

---

## 🛠️ 4. A Repó Könyvtárszerkezete

```text
Plakat_Kutatas_2025_2026/
├── Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf # 4. blokk elemzés (3 oldal)
├── Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf             # 3. blokk kódkönyv (2 oldal)
├── Opponensi_Ertekelo_Lap_es_Reprodukcios_Jelentes_Varga_Balazs.pdf # Opponensi lap
├── VPOSTER_Skill_Bemutato_es_Specifikacio_Varga_Balazs.pdf       # Skill specifikáció
├── CODEBOOK.md                                                   # Kódkönyv (EN)
├── CODEBOOK_HU.md                                                # Kódkönyv (HU)
├── README.md                                                     # Kutatási dokumentáció
├── reproduce.py                                                  # Mester reprodukciós kód
├── final_success_audit.py                                        # Minőségbiztosítási audit
├── generate_research_charts.py                                   # Diagramgeneráló kód
├── build_academic_3page_paper.py                                 # Akadémiai PDF generátor
├── plakat_kutatas_korpusz_2025_2026.csv                         # Fő CSV adathalmaz
├── plakat_kutatas_korpusz_2025_2026_excel.csv                   # Excel kompatibilis CSV
├── plakat_adatbazis_2025_2026.sql                               # Relációs SQL adatbázis
├── plakat_adatbazis_2025_2026.db                                # SQLite adatbázis
├── ParlLawSpeech_Plakat_Korpusz_2025_2026.json                   # JSON adathalmaz
├── hand.csv                                                      # Humán kódolási standard
├── labels.csv                                                    # Gépi kódolás
├── agreement_report.txt                                          # Egyezési jegyzőkönyv
├── comparison.html                                               # Plakát-összehasonlító app
├── vposter_skill_bemutato.html                                   # Skill bemutató app
├── index.html                                                    # GitHub Pages belépő
├── kutatasi_grafikonok/                                          # 4 nagyfelbontású PNG
├── vagott_kepek/                                                 # 13 plakát képkivágása
├── eredeti_sajto_kepek/                                          # 14 terep- és sajtófotó
├── discover_output/                                              # TF-IDF látens téma adatok
└── skills/                                                       # Skill csomagok
    ├── vposter/                                                  # Saját fejlesztésű skill
    ├── vcalibrate/
    ├── vclassify/
    ├── vcodebook/
    ├── vcoder-agreement/
    ├── vdescriptives/
    ├── vdiscover/
    ├── vscrape/
    ├── vtable-format/
    ├── datavalidation/
    ├── data-provenance-checker/
    ├── record-linkage/
    └── wscheck/
```
