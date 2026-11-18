# Bibó István Szakkollégium · AI Kurzus 2026 Ősz
## Mesterséges intelligencia a társadalom- és politikatudományi kutatásban
**Oktató:** Dr. Sebők Miklós (Syracuse University / poltextLAB)  
**Hallgató:** Varga Balázs  
**Kutatási téma:** A 2025–2026-os magyar óriásplakát-kampányok összehasonlító tartalomelemzése, szemiotikai vizsgálata és gépi kódolása  

---

## 🔗 KÖZVETLEN ELÉRÉSI LINKEK (Weboldal, Skill, Beadandók)

### 🌐 Interaktív Webes Felületek:
* **Plakát-összehasonlító weboldal:** [https://blaseco.github.io/Plakat_Kutatas_2025_2026/comparison.html](https://blaseco.github.io/Plakat_Kutatas_2025_2026/comparison.html)  
* **vposter Skill bemutató weboldal:** [https://blaseco.github.io/Plakat_Kutatas_2025_2026/vposter_skill_bemutato.html](https://blaseco.github.io/Plakat_Kutatas_2025_2026/vposter_skill_bemutato.html)  
* **Élő prezentációs alagút link (mobilról is):** [https://fec72f34c54a46.app.lhr.life/comparison.html](https://fec72f34c54a46.app.lhr.life/comparison.html)

### ⚙️ A Saját Fejlesztésű vposter Skill:
* **A Skill mappája a repóban:** [.agents/skills/vposter/](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/tree/main/.agents/skills/vposter)
* **Skill definíció (SKILL.md):** [SKILL.md](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/.agents/skills/vposter/SKILL.md)
* **Skill műszaki specifikáció PDF (2 oldal):** [VPOSTER_Skill_Bemutato_es_Specifikacio_Varga_Balazs.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/VPOSTER_Skill_Bemutato_es_Specifikacio_Varga_Balazs.pdf)

### 📄 Hivatalos Beadandók:
* **Rövid írásos elemzés (Block 4 · pontosan 3 oldal):** [Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf)
* **Kódkönyv és validáció (Block 3 · pontosan 2 oldal):** [Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf)
* **Opponensi értékelő lap és szóbeli vita forgatókönyv:** [Opponensi_Ertekelo_Lap_es_Reprodukcios_Jelentes_Varga_Balazs.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/Opponensi_Ertekelo_Lap_es_Reprodukcios_Jelentes_Varga_Balazs.pdf)
* **10 perces előadói beszéd és védési forgatókönyv:** [Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf)
* **Reprodukciós mesterkód:** [reproduce.py](https://github.com/Blaseco/Plakat_Kutatas_2025_2026/blob/main/reproduce.py)

---

## 📌 1. A 3. és 4. Blokk Hivatalos Követelményeinek Teljesülése

A projekt teljes egészében Dr. Sebők Miklós hivatalos kurzusdiái (*Block 3: Measurement and analysis: coding, classification, validation*, Slide 1–47) alapján készült, maradéktalanul teljesítve a **Slide 40** és **Slide 45 (Block 4 Homework)** előírásait:

1. **Rövid írásos elemzés (PDF, legfeljebb 3 oldal táblázatokkal és ábrákkal - Slide 45):**
   * Fájl: `Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf`
   * Terjedelem: **Pontosan 3 oldal** (1. oldal: Kutatási kérdés, operacionalizálás, kódkönyv; 2. oldal: Table 1 booktabs táblázat, 1. és 2. ábra, leíró statisztika; 3. oldal: Gépi kódolás, κ=1.000 megbízhatóság, témafeltárás, plakát-összehasonlítás, hipotézisteszt, mi cáfolná meg, szakirodalom és a kötelező beágyazott MI-nyilatkozat).
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
   * Fájl: `Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf` (pontosan 2 oldal, forrás, napló, azonosító, validálás és beágyazott MI-nyilatkozat).

---

## 🚀 2. Gyorsindítási Útmutató az Opponensnek

1. Repó letöltése:
   ```bash
   git clone https://github.com/Blaseco/Plakat_Kutatas_2025_2026.git
   cd Plakat_Kutatas_2025_2026
   ```
2. Reprodukciós teszt futtatása:
   ```bash
   python3 reproduce.py
   ```
3. A vposter skill önellenőrzése:
   ```bash
   python3 .agents/skills/vposter/scripts/selftest.py
   ```
