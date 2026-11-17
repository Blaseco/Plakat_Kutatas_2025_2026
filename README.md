# Bibó István Szakkollégium · AI Kurzus 2026 Ősz
## Mesterséges intelligencia a társadalom- és politikatudományi kutatásban
**Oktató:** Dr. Sebők Miklós (Syracuse University / poltextLAB)  
**Hallgató:** Varga Balázs  
**Kutatási téma:** A 2025–2026-os magyar óriásplakát-kampányok összehasonlító tartalomelemzése, szemiotikai vizsgálata és gépi kódolása  
**GitHub adattárház:** [https://github.com/Blaseco/Plakat_Kutatas_2025_2026](https://github.com/Blaseco/Plakat_Kutatas_2025_2026)  
**Élő interaktív felület (prezentációhoz):** [https://8de68d1ed90be0.app.lhr.life/comparison.html](https://8de68d1ed90be0.app.lhr.life/comparison.html)

---

## 📌 1. A 3. és 4. Blokk Hivatalos Követelményeinek Teljesülése

A projekt teljes egészében Dr. Sebők Miklós hivatalos kurzusdiái (*Block 3: Measurement and analysis: coding, classification, validation*, Slide 1–47) alapján készült, maradéktalanul teljesítve a **Slide 40** és **Slide 45 (Block 4 Homework)** előírásait:

1. **Rövid írásos elemzés (PDF, legfeljebb 3 oldal táblázatokkal és ábrákkal - Slide 45):**
   * Fájl: `Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf`
   * Terjedelem: **Pontosan 3 oldal** (1. oldal: Kutatási kérdés, operacionalizálás, kódkönyv; 2. oldal: Table 1 booktabs táblázat, 1. és 2. ábra, leíró statisztika; 3. oldal: Gépi kódolás, κ=1.000 megbízhatóság, témafeltárás, plakát-összehasonlítás, hipotézisteszt, mi cáfolná meg, szakirodalom).
2. **Önálló reprodukciós repó és script (Slide 40 & 45):**
   * *"THE POINT: Your opponent reproduces your numbers, so the repo has to run without you."*
   * Futtatás egyetlen parancssori utasítással:
     ```bash
     python3 reproduce.py
     ```
   * A script emberi segítség nélkül ellenőrzi az adatbázis teljességét, újraszámolja a megbízhatóságot (κ = 1.000), előállítja a leíró táblázatot (Table 1), determinisztikusan újragenerálja a diagramokat, és elvégzi a Rogan–Gladen mérési hiba korrekciót.
3. **10 perces prezentációs beszéd és védési forgatókönyv:**
   * Fájl: `Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf` (5 oldalas, 10 diára bontott előadói jegyzet, szemiotikai plakátelemzéssel és módszertani védelmi érvekkel).
4. **Mesterdokumentáció Word formátumban (kollégáknak és opponensnek):**
   * Fájl: `Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx` (5 MB, beágyazott nagyfelbontású plakátfotókkal, ábrákkal és APA 7th hivatkozásokkal).
5. **Kódkönyv (Codebook) akadémiai formátumban (Slide 4, 18):**
   * Fájl: `Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf` (2 oldal) és `CODEBOOK.md`.

---

## 📂 2. A Mappa Teljes Tartalomjegyzéke (`bibó ai 2026 végleges`)

### A) Hivatalos Dokumentumok és Elemzések (PDF & DOCX)
* `Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf` – **A hivatalos 3 oldalas beadandó (Block 4)**
* `Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf` – Hivatalos 2 oldalas kódkönyv APA 7th hivatkozásokkal
* `Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf` – 10 perces előadói szöveg és opponensi védelem
* `Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx` – Teljes Word mesterkönyv képekkel
* `AI_Nyilatkozat_Varga_Balazs_2025_2026.pdf` – Hivatalos AI etikai nyilatkozat
* `Bibo_MI_Kurzus_Plakatkutatas_Beadando_Varga_Balazs.pdf` – Korábbi teljes kutatási dokumentáció
* `Plakat_Kutatas_Teljes_Kod_es_Skill_Dokumentacio.pdf` – Skill futtatási napló PDF formátumban

### B) Adatbázisok és Adatkészletek (Minden formátumban)
* `plakat_kutatas_korpusz_2025_2026.csv` – Standard UTF-8 adathalmaz (18 oszlop, n=13)
* `plakat_kutatas_korpusz_2025_2026_excel.csv` – Magyar Excel kompatibilis adathalmaz (UTF-8 BOM, pontosvessző)
* `plakat_adatbazis_2025_2026.sql` – Relációs SQL adatbázis séma (DDL) és adatok (DML)
* `plakat_adatbazis_2025_2026.db` – Hordozható SQLite adatbázis fájl
* `ParlLawSpeech_Plakat_Korpusz_2025_2026.json` – Gépi feldolgozásra optimalizált JSON korpusz
* `labels.csv` – A nyelvi modell által generált kódok (/vclassify)
* `hand.csv` – Humán arany standard manuális kódok (/vcoder-agreement)
* `agreement_report.txt` – Megbízhatósági audit eredmény (κ = 1.000)

### C) Reprodukciós és Elemző Kódok (Python)
* `reproduce.py` – **Az opponens és az oktató által egy kattintással futtatható ellenőrző script**
* `run_all_skills_verifiable.py` – Mind a 12 kutatási skill verifikációs keretrendszere
* `generate_research_charts.py` – A kutatási diagramok determinisztikus újratermelése
* `build_3page_analysis_pdf.py` – A 3 oldalas beadandó PDF fordítója
* `build_2page_codebook_pdf.py` – A 2 oldalas kódkönyv PDF fordítója
* `build_10min_presentation_pdf.py` – A prezentációs beszéd PDF fordítója
* `build_presentation_master_docx.py` – A Word mesterdokumentáció fordítója

### D) Képi Mellékletek és Ábrák
* `kutatasi_grafikonok/`:
  * `grafikon_1_tonus_taborok.png` – Tónus megoszlás politikai táboronként
  * `grafikon_2_kibocsatok.png` – Kibocsátói intézményi megoszlás
  * `grafikon_3_latens_temak.png` – TF-IDF látens témák
  * `grafikon_4_szemiotikai_matrix.png` – Vizuális-retorikai szemiotikai eszközök
* `vagott_kepek/` – Mind a 13 db politikai óriásplakát nagyfelbontású képe (`HUN_PLAKAT_2025_001.jpg` – `HUN_PLAKAT_2026_013.jpg`)
* `eredeti_sajto_kepek/` – Nyers sajtófotók és forrásképek

### E) Webes Interaktív Felületek
* `comparison.html` – Dinamikus, böngészhető plakát-összehasonlító felület szűrőkkel és részletes vizuális elemzéssel
* `index.html` – Teljes kutatási bemutató weboldal
* `OSSZES_SKILL_ELLENORZESI_JEGYZOKONYV.md` – Hivatalos 12 pontos jegyzőkönyv

---

## 🔬 3. Módszertani Összefoglaló (A kurzus 12 skillje)

| # | Skill neve | Kurzusbeli szerep | Eredmény |
|---|---|---|---|
| 1 | `wscheck` | Munkakörnyezet, repó és titkok ellenőrzése | 🟢 PASS |
| 2 | `vscrape` | Transzparens köztéri adatgyűjtés | 🟢 PASS |
| 3 | `datavalidation` | Hiányzó értékek és integritás vizsgálata | 🟢 PASS |
| 4 | `data-provenance-checker` | Forráskód és sajtó-eredet visszakövethetősége | 🟢 PASS |
| 5 | `record-linkage` | Relációs kulcsok és entitás-összerendelés | 🟢 PASS |
| 6 | `vcodebook` | Zárt kategóriarendszer és döntési szabályok | 🟢 PASS |
| 7 | `vclassify` | LLM prompt alapú kódolás (Gemini-3.8-Flash) | 🟢 PASS |
| 8 | `vcoder-agreement` | Humán arany standard megbízhatósági teszt (**κ = 1.000**) | 🟢 PASS |
| 9 | `vdiscover` | TF-IDF és embedding alapú témafeltárás (3 téma) | 🟢 PASS |
| 10 | `vdescriptives` | Gyakoriságok és kereszttáblák a modellezés előtt | 🟢 PASS |
| 11 | `vtable-format` | Standard tudományos háromvonalas (booktabs) táblázatformátum | 🟢 PASS |
| 12 | `vcalibrate` | Rogan–Gladen mérési hiba korrekció | 🟢 PASS |

---

## 🚀 4. Reprodukciós Útmutató (Opponenseknek és Érdeklődőknek)

1. Nyissunk egy terminált a mappában:
   ```bash
   cd "/Users/blaseco/Desktop/bibó ai 2026 végleges"
   ```
2. Futtassuk a mester reprodukciós kódot:
   ```bash
   python3 reproduce.py
   ```
3. A kód automatikusan kiírja az ellenőrzési eredményeket, a konfúziós mátrixot, a leíró táblázatot és a Rogan–Gladen korrekciót.
