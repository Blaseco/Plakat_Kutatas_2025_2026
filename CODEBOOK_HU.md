# 2025–2026 Magyar Politikai Plakátkutató Korpusz — Adatkódkönyv (Codebook)
**Verzió:** 1.0 (ParlLawSpeech Outdoor Standard & Skill Validation)  
**Dátum:** 2026-04-10  
**Projekt Repozitórium:** Antigravity Local Research Environment  
**Licenc:** CC-BY 4.0 (Open Access)

---

## 1. Bevezetés
Ez a kódkönyv a 2025–2026-os magyarországi politikai outdoor kampányok korpuszának (13 dokumentált rekord) strukturált dokumentációja. A korpusz rögzíti a vizuális elemeket, a kibocsátói típust (triádikus architektúra: állam, párt, proxy), valamint a sajtófotó-alapú validációs naplót.

---

## 2. Adatgyűjtés, Lefedettség és Források (Coverage & Data Collection)
* **Időszak:** 2025. április 06. – 2026. április 08.
* **Egységek (Units of Analysis):** 13 db politikai plakát / kampányfelület.
* **Földrajzi lefedettség:** Országos (Budapest, Szolnok, Nagykanizsa, Pécs).
* **Adatforrások (Források listája):** Független online sajtótermékek, amelyek fotógalériái és tudósításai dokumentálták a közterületi plakátokat:
  * `444.hu` (Fotósok: Mészáros Juli, Kovács Gergely, Bábel Vilmos, szerkesztőség)
  * `HVG` (Fotósok: Cabrera Martin, Túry Gergely, Lakos Gábor)
  * `Telex` (Fotósok: Huszti István, Zách Dániel, szerkesztőség)
  * `24.hu` (Fotós: Kőrös Gábor)
  * `Szolnok TV / Kanizsa Médiaház` (Helyi sajtódokumentáció)

---

## 3. Adatstruktúra, Változók és Egyedi Azonosító (Data Structure & Variables)
Az adatok tárolása UTF-8 kódolású CSV és SQL formátumban történik.

* **Egyedi linking identifier (Központi azonosító):** Minden egyes rekord a `id` változót (pl. `HUN_PLAKAT_2025_001` – `HUN_PLAKAT_2026_013`) használja egyedi azonosítóként, amely összeköti a relációs adatbázist a helyi `vagott_kepek/` mappában lévő vizuális fájlokkal.

### Core-változók táblázata:
| Változónév (`variable`) | Típus | Leírás |
| :--- | :--- | :--- |
| `id` | VARCHAR (PK) | Egyedi azonosító a ParlLawSpeech szabvány szerint |
| `datum` | DATE | A közterületi megjelenés vagy sajtódokumentálás napja (`YYYY-MM-DD`) |
| `politikai_tabor` | VARCHAR | A politikai oldal (`FIDESZ-TÁBOR` vagy `TISZA PÁRT`) |
| `kibocsato_tipus` | VARCHAR | A kibocsátó kategóriája (`STATE` = állami, `PROXY` = harmadik feles, `PARTY` = párt, `GRASSROOTS` = lakossági) |
| `hivatalos_kiado` | TEXT | A hirdetést megrendelő szervezet (pl. Miniszterelnöki Kabinetiroda, Nemzeti Ellenállás Mozgalom) |
| `fajl_nev` | VARCHAR | A vágott sajtófotó helyi útvonala (`vagott_kepek/HUN_PLAKAT_...jpg`) |
| `plakat_szlogen` | TEXT | A plakáton szereplő fő felirat / szlogen |
| `vizualis_leiras` | TEXT | A vizuális elemek, szereplők és szemiotikai jelek leírása |
| `formatum_meret` | VARCHAR | A hordozó típusa és mérete (pl. Óriásplakát 12 m², Kandeláberplakát B1) |
| `politikai_elemzes` | TEXT | Médiakommunikációs és politológiai elemzés |
| `forras_nev` | VARCHAR | A sajtócikk kiadója és a fotós neve |
| `forras_url` | TEXT | Az eredeti online forráscikk közvetlen hivatkozása |

---

## 4. Validálási Munkafolyamat és Napló (Validation Workflow)
A korpusz adatai az alábbi szigorú ellenőrzési lépéseken mentek keresztül:

1. **Vizuális és Fotóvalidáció (100%):** 
   * *Művelet:* Minden egyes online sajtócikkből kitermelésre és méretre vágásra kerültek a plakátfotók. 
   * *Ellenőrzés:* A képek fizikai létezése a `vagott_kepek/` mappában ellenőrizve lett, így elkerülhető a holt linkek (broken links) problémája a kutatás során.
2. **Forrás- és URL-ellenőrzés (Traceability):** 
   * *Művelet:* Minden rekordhoz csatolva lett az eredeti hírportál URL-címe. 
   * *Ellenőrzés:* Kereszthivatkozásos teszttel igazoltuk, hogy a leírt szlogenek és vizuális elemek megegyeznek az eredeti sajtódokumentációval.
3. **Kategória-konzisztencia (Coding Validation):** 
   * *Művelet:* A kibocsátói típusok besorolása (`STATE` vs. `PROXY` vs. `PARTY`) független politológiai kódolási szempontok szerint történt (szétválasztva a hivatalos pártkommunikációt a harmadik feles proxy szervezetek negatív kampányaitól).

---

## 5. Hivatkozási Sablon (APA 7th & Open Access Licenc)
> Magyar Politikai Plakátkutató Korpusz (2025–2026). *ParlLawSpeech Outdoor Standard*. Antigravity Local Research Database. Licenc: CC-BY 4.0. Elérhető: `vagott_kepek/` és `plakat_kutatas_korpusz_2025_2026.csv`.
