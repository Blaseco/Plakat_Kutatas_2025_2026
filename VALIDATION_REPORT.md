# ParlLawSpeech Korpusz Adatvalidációs Jelentés (Data Validation Report)
**Protokoll szabvány:** ParlLawSpeech Data Validation Workflow (5-Step Procedure)
**Célkorpusz:** 2025–2026 Magyar Politikai Plakát Adatbázis (`Plakat_Kutatas_2025_2026`)
**Dátum:** 2026-11-04
**Validációs státusz:** TELJES KÖRŰ ELLENŐRZÉS LEFUTOTT (ALL CHECKS PASSED)

---

**Elemzési egységek száma (N):** 13 rekord

## 1. Általános Teljesség és Duplikáció Ellenőrzés (General Completeness & Duplicate Checks)

- [x] **Azonosítók egyedisége (ID Uniqueness):** 13/13 egyedi azonosító. SIKERES (Nincs duplikáció)
- [x] **Szövegek egyedisége (Text Uniqueness - Context-Aware):** 13 különböző szlogen 13 rekord között.
  * Nincs nem szándékolt szövegduplikáció (100% egyedi kampányüzenetek).
- [x] **Forrás-URL egyediség és cikk-többszörösség:** 12 egyedi sajtóforrás.
  * Többes forrás azonosítva: `https://hvg.hu/itthon/20251004_Ursula-Von-der-Leyen-babozas-nemzeti-konzultacio-plakat-ebx` (2 rekord: HUN_PLAKAT_2025_005, HUN_PLAKAT_2025_006) -> *Kontextuálisan valid*: egy sajtócikk több párhuzamos plakátot mutat be (pl. HVG konzultáció ikerplakátok).
- [x] **Hiányzó adatok ellenőrzése (No NA / Missing Value Check):** 0 hiányzó cella a 12 core-változóban.
  * Teljességi arány: **100.0%** (Minden kötelező mező kitöltve).

### Alcsoportok szerinti lefedettség (Coverage by Subgroups):
| Politikai Tábor | Kibocsátó Típusa | Esetszám ($N$) | Megoszlás (%) |
| :--- | :--- | :---: | :---: |
| FIDESZ-TÁBOR | `PARTY` | 2 | 15.4% |
| FIDESZ-TÁBOR | `PROXY` | 3 | 23.1% |
| FIDESZ-TÁBOR | `STATE` | 6 | 46.2% |
| TISZA PÁRT | `GRASSROOTS` | 1 | 7.7% |
| TISZA PÁRT | `PARTY` | 1 | 7.7% |

## 2. Metaadatok Ellenőrzése és Strukturális Szabványosítás (Metadata Inspection)

- [x] **Azonosító struktúra ellenőrzése (Regex: `^HUN_PLAKAT_\d{4}_\d{3}$`):**
  * Minden rekord azonosítója (13/13) szigorúan illeszkedik a nemzetközi ParlLawSpeech formátumhoz.
- [x] **Dátumformátum (ISO 8601: `YYYY-MM-DD`):**
  * Minden időbélyeg (13/13) érvényes ISO formátumú.
- [x] **Kategória-mezők szabványossága (Categorical Standardization):**
  * `politikai_tabor` érvényesség: 0 hiba. Értékek: {'FIDESZ-TÁBOR', 'TISZA PÁRT'}
  * `kibocsato_tipus` érvényesség: 0 hiba. Értékek: {'GRASSROOTS', 'PARTY', 'STATE', 'PROXY'}

## 3. Adathalmazok Keresztkapcsolása és Rekordegyeztetés (Cross-Dataset Linking)

| Tábla / Adatforrás | Rekordszám ($N$) | Egyezés a főkulccsal (`id`) | Állapot |
| :--- | :---: | :---: | :--- |
| `plakat_kutatas_korpusz_2025_2026.csv` | 13 | 13 / 13 | EGYEZIK (Referencia) |
| `plakat_kutatas_korpusz_2025_2026_excel.csv` | 13 | 13 / 13 | EGYEZIK (100%) |
| `ParlLawSpeech_Plakat_Korpusz_2025_2026.csv` | 13 | 13 / 13 | EGYEZIK (100%) |
| `plakat_adatbazis_2025_2026.db` (SQLite) | 13 | 13 / 13 | EGYEZIK (100%) |
| Vágott sajtóképek (`vagott_kepek/`) | 13 | 13 / 13 | EGYEZIK (100% fizikai lefedettség) |
| Eredeti sajtóképek (`eredeti_sajto_kepek/`) | 13 | 13 / 13 | EGYEZIK (100% archivált eredeti) |

- [x] **Relációs integritás:** Nincs árva rekord (zero orphan rows), nincs feloldatlan idegen kulcs (zero dangling keys).

## 4. Szövegtartalom és Kódolás Ellenőrzése (Text Content Inspection)

- [x] **Karakterkódolás és UTF-8 épség:**
  * Hibás helyettesítő karakterek (`\ufffd` / kérdőjeles roncsolódás): **0 db**. A magyar ékezetes karakterek épek és hibátlanok.

- [x] **Szlogenek szövegtisztítása, idézőjelek és tipográfia:**
| ID | Tisztított Szlogen | Szavak | Írásjelek | Karakter (szóközzel) |
| :--- | :--- | :---: | :---: | :---: |
| `HUN_PLAKAT_2025_001` | „VOKS 2025 – Ne hagyjuk, hogy a fejünk felett döntsenek!” | 10 | 5 | 57 |
| `HUN_PLAKAT_2025_002` | „Megmutattuk, hogy van véleményünk! 2 millió nem Ukrajna EU-tagságára!” | 9 | 6 | 71 |
| `HUN_PLAKAT_2025_003` | „MINT KÉT TOJÁS” | 3 | 2 | 16 |
| `HUN_PLAKAT_2025_004` | „Volt egy zápor” | 3 | 2 | 16 |
| `HUN_PLAKAT_2025_005` | „Brüsszel bábjai adót akarnak emelni! – Nemzeti Konzultáció” | 8 | 4 | 60 |
| `HUN_PLAKAT_2025_006` | „A családi adócsökkentés az Ön családjának is jár!” | 8 | 3 | 51 |
| `HUN_PLAKAT_2025_007` | „Ki az a Steiner Attila?” | 5 | 3 | 25 |
| `HUN_PLAKAT_2026_008` | „Üzenjük Brüsszelnek: NEM FIZETÜNK! – Nemzeti Petíció” | 7 | 5 | 54 |
| `HUN_PLAKAT_2026_009` | „ADÓEMELÉST! / PÉNZT UKRAJNÁNAK! – IGENIS! – NEM TUD NEKIK NEMET MONDANI” | 12 | 8 | 73 |
| `HUN_PLAKAT_2026_010` | „A BIZTOS VÁLASZTÁS – Fidesz–KDNP (Berkó Attila)” | 7 | 6 | 49 |
| `HUN_PLAKAT_2026_011` | „Védett üzemanyagár – A benzin és a gázolaj hazánkban a legolcsóbb Európában!” | 12 | 4 | 78 |
| `HUN_PLAKAT_2026_012` | „TISZA – VÁLASZTÁS 2026 (Mészáros Dávid)” | 6 | 5 | 41 |
| `HUN_PLAKAT_2026_013` | „Most vagy soha!” | 3 | 3 | 17 |

## 5. Feltáró Validáció és Anomália-detektálás (Exploratory Validation)

### Statisztikai összefoglaló a szövegmezőkről:
- **Plakát szlogen hossz:** Átlag = 46.8 karakter | Min = 16 (`HUN_PLAKAT_2025_003` - „MINT KÉT TOJÁS”) | Max = 78 (`HUN_PLAKAT_2026_011` - Védett üzemanyagár)
- **Vizuális leírás hossz:** Átlag = 90.2 karakter | Min = 52 | Max = 129
- **Politikai elemzés hossz:** Átlag = 89.6 karakter | Min = 60 | Max = 104

### Anomália- és Kiugró Érték Szűrés (Outlier Detection):
1. **Rövid, tömör szlogenek (< 25 karakter):** 3 db
   * `HUN_PLAKAT_2025_003`: „MINT KÉT TOJÁS” (16 kar.) -> *Elemzés*: Fókuszált érzelmi / asszociációs kulcsszavak (Apáti/NEM, Steiner teaser, Tisza mozgósítás).
   * `HUN_PLAKAT_2025_004`: „Volt egy zápor” (16 kar.) -> *Elemzés*: Fókuszált érzelmi / asszociációs kulcsszavak (Apáti/NEM, Steiner teaser, Tisza mozgósítás).
   * `HUN_PLAKAT_2026_013`: „Most vagy soha!” (17 kar.) -> *Elemzés*: Fókuszált érzelmi / asszociációs kulcsszavak (Apáti/NEM, Steiner teaser, Tisza mozgósítás).
2. **Hosszú, szakpolitikai vagy összetett szlogenek (> 65 karakter):** 3 db
   * `HUN_PLAKAT_2025_002`: „Megmutattuk, hogy van véleményünk! 2 millió nem Ukrajna EU-tagságára!” (71 kar.) -> *Elemzés*: Állami és proxy tájékoztató hirdetések részletes üzenetei (VOKS 2025, Nemzeti Petíció, Védett üzemanyagár).
   * `HUN_PLAKAT_2026_009`: „ADÓEMELÉST! / PÉNZT UKRAJNÁNAK! – IGENIS! – NEM TUD NEKIK NEMET MONDANI” (73 kar.) -> *Elemzés*: Állami és proxy tájékoztató hirdetések részletes üzenetei (VOKS 2025, Nemzeti Petíció, Védett üzemanyagár).
   * `HUN_PLAKAT_2026_011`: „Védett üzemanyagár – A benzin és a gázolaj hazánkban a legolcsóbb Európában!” (78 kar.) -> *Elemzés*: Állami és proxy tájékoztató hirdetések részletes üzenetei (VOKS 2025, Nemzeti Petíció, Védett üzemanyagár).

### Szemiotikai és Szóhasználati Keresztellenőrzés:
- **Fidesz-tábor arculatmegoszlás ($N=11$):**
  * Állami hirdetések (Kormány / Miniszterelnöki Kabinetiroda): 6 db (Kék háttér, sárga/fehér betűk, intézményi tekintély)
  * Proxy negatív kampányok (NEM / Apáti Bence): 3 db (Gúny, karikatúra, Magyar Péter és Brüsszel/Ukrajna összekapcsolása)
  * Hivatalos Fidesz-KDNP pártkampány: 2 db (Narancs-fehér arculat, stabilitás, egyéni jelölt)
- **Tisza Párt kampánymegoszlás ($N=2$):**
  * Hivatalos jelölti jelenlét: 1 db (Kandeláberes hullámpolitén tábla, B1 formátum, költséghatékony)
  * Lakossági / Grassroots kampány: 1 db (Privát erkélyek, kerítések, molinók, decentralizált részvétel)

---

## 6. Összegző Validációs Értékelés (Conclusion & Certification)
A 2025–2026-os Magyar Politikai Plakát Adatbázis korpusza a **ParlLawSpeech Data Validation Workflow mind az 5 lépésén sikeresen és hibátlanul átment**:
1. **Teljesség és duplikáció:** Nincs hiányzó érték (100% kitöltöttség), nincs azonosító duplikáció.
2. **Metaadatok:** Strukturált ISO dátumok, érvényes reguláris kifejezésű azonosítók, sztenderdizált kategóriák.
3. **Keresztkapcsolás:** 100%-os relációs és fizikai lefedettség mind a 13 vágott és eredeti sajtófotóval és adatbázis-táblával.
4. **Szövegminőség:** Hibátlan UTF-8 kódolás, tiszta tipográfia, pontos szlogen- és elemzés-transzkripció.
5. **Feltáró anomália-szűrés:** A szöveghosszúságok és kategóriák megfelelnek a kvalitatív politológiai várakozásoknak.

**Ajánlás:** A korpusz kutatásra, statisztikai elemzésre és nyilvános közzétételre készen áll (*Validated and Release-Ready*).
