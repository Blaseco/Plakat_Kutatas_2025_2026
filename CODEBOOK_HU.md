# 2025–2026 Magyar Politikai Plakátkutató Korpusz — Adatkódkönyv (Codebook)
**Verzió:** 1.0 (ParlLawSpeech Outdoor Standard)  
**Dátum:** 2026-04-10  
**Projekt URL / Repozitórium:** `~/Desktop/Plakat_Kutatas_2025_2026/`  
**Licenc:** CC-BY 4.0 (Open Access)  
**Módszertani szabvány:** ParlLawSpeech Data Codebook Template (Schwalbach, Hetzer, Proksch, Rauh & Sebők, 2025)

---

## 1. Bevezetés
Ez a kódkönyv a 2025–2026-os magyarországi politikai outdoor kampányok korpuszának (13 dokumentált rekord) strukturált dokumentációja. Rögzíti a vizuális elemeket, a kibocsátói típust (triádikus architektúra: állam, párt, proxy), valamint a sajtófotó-alapú validációs naplót.

---

## 2. Adatgyűjtés és Lefedettség (Coverage)
* **Időszak:** 2025. április 06. – 2026. április 08.
* **Egységek (Units of Analysis):** 13 db politikai plakát / kampányfelület.
* **Földrajzi lefedettség:** Országos (Budapest, Szolnok, Nagykanizsa, Pécs).
* **Adatforrások:** Független online sajtótermékek (444.hu, HVG, Telex, 24.hu, Szolnok TV, Kanizsa Médiaház).

### Összesítő statisztikai tábla:

| Politikai Tábor | Elemzési Egység ($N$) | Hordozóformák | Kibocsátói típusok |
| :--- | :---: | :--- | :--- |
| **Fidesz-tábor** | 11 | Óriásplakát (12 m²), Hengeroszlop, Citylight, Teherautó, Kandeláber | Állami (6), Harmadik feles proxy (3), Hivatalos párt (2) |
| **Tisza Párt** | 2 | Kandelábertábla (B1/A1), Lakossági kerítésmolinó (200x100 cm) | Hivatalos párt (1), Lakossági grassroots (1) |
| **Összesen** | **13** | **Közterületi és lakossági outdoor média** | **100% fotóvalidált** |

---

## 3. Adatstruktúra & Változók (Core Variables)
Az adatok tárolása UTF-8 kódolású CSV (`plakat_kutatas_korpusz_2025_2026.csv`) és SQL (`plakat_adatbazis_2025_2026.sql` / `.db`) formátumban történik.

| Változónév (`variable`) | Típus | Leírás |
| :--- | :--- | :--- |
| `id` | VARCHAR (PK) | Egyedi azonosító a ParlLawSpeech szabvány szerint (pl. `HUN_PLAKAT_2025_001`) |
| `datum` | DATE | A közterületi megjelenés vagy sajtódokumentálás napja (`YYYY-MM-DD`) |
| `politikai_tabor` | VARCHAR | A politikai oldal (`FIDESZ-TÁBOR` vagy `TISZA PÁRT`) |
| `kibocsato_tipus` | VARCHAR | A kibocsátó kategóriája (`STATE` = állami, `PROXY` = harmadik feles, `PARTY` = párt, `GRASSROOTS` = lakossági) |
| `hivatalos_kiado` | TEXT | A hirdetést megrendelő szervezet (pl. Miniszterelnöki Kabinetiroda, NEM Non-Profit Kft., Fidesz–KDNP, TISZA Párt) |
| `fajl_nev` | VARCHAR | A vágott sajtófotó helyi relatív útvonala (`vagott_kepek/HUN_PLAKAT_...jpg`) |
| `plakat_szlogen` | TEXT | A plakáton szereplő fő felirat / szlogen |
| `vizualis_leiras` | TEXT | A vizuális elemek, szereplők és szemiotikai jelek leírása |
| `formatum_meret` | VARCHAR | A hordozó típusa és mérete (pl. Óriásplakát 12 m², Kandeláberplakát B1, Molinó) |
| `politikai_elemzes` | TEXT | Médiakommunikációs és politológiai elemzés (diskurzus, keretezés, célcsoport) |
| `forras_nev` | VARCHAR | A sajtócikk kiadója és a fotós neve |
| `forras_url` | TEXT | Az eredeti online forráscikk közvetlen hivatkozása |

---

## 4. Validálási Napló (Validation & Traceability)
1. **Fotóvalidáció (100%):** Minden egyes rekordhoz tartozik egy helyben tárolt, ellenőrzött és vágott sajtófotó a `vagott_kepek/` könyvtárban, amely kizárja a hivatkozástörés és a külső képtörlés kockázatát.
2. **Kereszthivatkozás:** A rekordok egyedi `id`-jei és a `forras_url` biztosítják a teljes visszakereshetőséget az eredeti oknyomozó sajtócikkekhez.
3. **Független ellenőrzés:** A kormánypárti és ellenzéki plakátok aránya, valamint a proxy szervezetek (pl. Nemzeti Ellenállás Mozgalom) szerepe dokumentálva van a triádikus kampányelmélet keretében.

---

## 5. Hivatkozási Sablon (APA 7th)
> Magyar Politikai Plakátkutató Korpusz (2025–2026). *ParlLawSpeech Outdoor Standard*. Antigravity Local Research Database. Elérhető: `vagott_kepek/` és `plakat_kutatas_korpusz_2025_2026.csv`.
