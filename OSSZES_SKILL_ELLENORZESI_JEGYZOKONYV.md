# Teljes Ellenőrzési Jegyzőkönyv – Kurzus Skillek Auditja (Blokk 2 & Blokk 3)

**Készítő:** Varga Balázs | Bibó István Szakkollégium
**Kurzus:** Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (2026. ősz)
**Audit időpontja:** 2026-11-17 16:55:47

| Ssz. | Skill Neve | Blokk | Státusz | Eredmény / Megjegyzés |
|:---:|:---|:---:|:---:|:---|
| 1. | `wscheck` | Blokk 2 | **PASS** | Munkakörnyezet érvényes, git repó tiszta, házirendek és DB jelen. |
| 2. | `datavalidation` | Blokk 2 | **PASS** | 13/13 rekord érvényes, 0 duplikátum, 0 hiányzó mező, 100% képkapcsolás. |
| 3. | `data-provenance-checker` | Blokk 2 | **PASS** | 100%-os visszakövethetőség a nyers terep- és sajtófotókig. |
| 4. | `record-linkage` | Blokk 2 | **PASS** | 1:1 determinisztikus adatkapcsolás hibátlan (13/13 rekord). |
| 5. | `vscrape` | Blokk 2 | **PASS** | Minden gyűjtött rekord forrása és metaadata igazolt (7 forrás). |
| 6. | `vcodebook` | Blokk 3 | **PASS** | Kódkönyv és kategóriadefiníciók szigorúan dokumentálva. |
| 7. | `vclassify` | Blokk 3 | **PASS** | 13 rekord sikeresen gépi kódolva, teljes indoklással. |
| 8. | `vcoder-agreement` | Blokk 3 | **PASS** | Tökéletes annotátori megbízhatóság: κ = 1.000 (100% egyezés). |
| 9. | `vdiscover` | Blokk 3 | **PASS** | 3 jól szeparált latens diskurzustéma azonosítva. |
| 10. | `vdescriptives` | Blokk 3 | **PASS** | Bivariate statisztikák és keresztmetszetek kalkulálva. |
| 11. | `vtable-format` | Blokk 3 | **PASS** | Minden táblázat megfelel a booktabs tudományos formátumnak. |
| 12. | `vcalibrate` | Blokk 3 | **PASS** | Rogan-Gladen aránykorrekciós teszt sikeres. |


## Részletes Eredmények és Lefutási Naplók

### wscheck (Blokk 2) – PASS
*Munkakörnyezet érvényes, git repó tiszta, házirendek és DB jelen.*

```
Git távoli tár: origin	git@github.com:Blaseco/Plakat_Kutatas_2025_2026.git (fetch)
origin	git@github.com:Blaseco/Plakat_Kutatas_2025_2026.git (push)
Gitignore létezik: True
AGENTS.md házirend létezik: True
SQLite adatbázis jelen: True
Munkakörnyezet állapota: Tiszta, szinkronizált origin/main.
```

### datavalidation (Blokk 2) – PASS
*13/13 rekord érvényes, 0 duplikátum, 0 hiányzó mező, 100% képkapcsolás.*

```
Összes megfigyelési egység: 13
Egyedi azonosítók száma: 13 (Duplikátumok: 0)
Hiányzó mezők oszloponként: {"id": 0, "datum": 0, "politikai_tabor": 0, "kibocsato_tipus": 0, "hivatalos_kiado": 0, "fajl_nev": 0, "plakat_szlogen": 0, "vizualis_leiras": 0, "formatum_meret": 0, "politikai_elemzes": 0, "forras_nev": 0, "forras_url": 0, "kampany_tonus": 0, "tartalmi_fokusz": 0, "vizualis_szemiotika": 0, "szlogen_retorika": 0, "latens_tema_id": 0, "latens_tema_nev": 0}
Hiányzó csatolt képfájlok: 0
Minden dátum ISO-8601 (YYYY-MM-DD) szabványú.
Minden forrás URL érvényes protokollal kezdődik.
```

### data-provenance-checker (Blokk 2) – PASS
*100%-os visszakövethetőség a nyers terep- és sajtófotókig.*

```
Rekordok száma: 13
Visszakövethető források: 13/13 (100%)
 - HUN_PLAKAT_2025_001 -> Raw: HUN_PLAKAT_2025_001_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2025_001.jpg | Forrás: 444.hu
 - HUN_PLAKAT_2025_002 -> Raw: HUN_PLAKAT_2025_002_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2025_002.jpg | Forrás: HVG
 - HUN_PLAKAT_2025_003 -> Raw: HUN_PLAKAT_2025_003_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2025_003.jpg | Forrás: 444.hu
 - HUN_PLAKAT_2025_004 -> Raw: HUN_PLAKAT_2025_004_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2025_004.jpg | Forrás: Telex
 - HUN_PLAKAT_2025_005 -> Raw: HUN_PLAKAT_2025_005_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2025_005.jpg | Forrás: HVG
 - HUN_PLAKAT_2025_006 -> Raw: HUN_PLAKAT_2025_006_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2025_006.jpg | Forrás: HVG
 - HUN_PLAKAT_2025_007 -> Raw: HUN_PLAKAT_2025_007_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2025_007.jpg | Forrás: 444.hu
 - HUN_PLAKAT_2026_008 -> Raw: HUN_PLAKAT_2026_008_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2026_008.jpg | Forrás: Telex
 - HUN_PLAKAT_2026_009 -> Raw: HUN_PLAKAT_2026_009_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2026_009.jpg | Forrás: 24.hu
 - HUN_PLAKAT_2026_010 -> Raw: HUN_PLAKAT_2026_010_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2026_010.jpg | Forrás: Szolnok TV / Hírös.hu
 - HUN_PLAKAT_2026_011 -> Raw: HUN_PLAKAT_2026_011_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2026_011.jpg | Forrás: Telex
 - HUN_PLAKAT_2026_012 -> Raw: HUN_PLAKAT_2026_012_orig.png -> Crop: vagott_kepek/HUN_PLAKAT_2026_012.jpg | Forrás: Kanizsa Médiaház / Szolnok TV
 - HUN_PLAKAT_2026_013 -> Raw: HUN_PLAKAT_2026_013_orig.jpg -> Crop: vagott_kepek/HUN_PLAKAT_2026_013.jpg | Forrás: 444.hu / HVG

```

### record-linkage (Blokk 2) – PASS
*1:1 determinisztikus adatkapcsolás hibátlan (13/13 rekord).*

```
Kardinalitási elvárás: 1:1 determinisztikus kapcsolás.
CSV rekordok: 13
SQLite DB rekordok: 13
Kölcsönös egyezési arány: 13/13 (100.0%)
Árva (unmatched) rekordok száma: 0
Duplikált kulcsok száma: 0
```

### vscrape (Blokk 2) – PASS
*Minden gyűjtött rekord forrása és metaadata igazolt (7 forrás).*

```
Adatgyűjtési kör: 2025–2026-os magyar óriásplakátok és közterületi hirdetések.
Feltárt primer források (7 db): Telex, Szolnok TV / Hírös.hu, 444.hu, HVG, 24.hu, Kanizsa Médiaház / Szolnok TV, 444.hu / HVG
Kibocsátó entitások (7 db): TISZA – Tisztelet és Szabadság Párt, Fidesz – Magyar Polgári Szövetség – KDNP, Kormánypárti kampányfelület, Hegyvidéki Fidesz-kampány (XII. kerület), Magyarország Kormánya (Miniszterelnöki Kabinetiroda), TISZA Párt (Szimpatizánsok otthonai), Nemzeti Ellenállás Mozgalom (Apáti Bence)
Adatgyűjtési módszer: Közterületi terepfotók és sajtóarchívumi scrapelt anyagok kétszintű tisztítással.
```

### vcodebook (Blokk 3) – PASS
*Kódkönyv és kategóriadefiníciók szigorúan dokumentálva.*

```
Kódkönyv fájl: codebook_session3.md (jelen: True)
Megfigyelési egység: Egyedi, 2025–2026-ban közzétett magyar politikai óriásplakát vagy kandelábertábla.
Rögzített kategóriák:
 1. NEGATIV_TAMADO: Ellenségkép-fókuszú, elrettentő, karaktergyilkos vagy vádoló plakátok.
 2. POZITIV_EPITO: Kormányzati szakpolitikai eredményt vagy ellenzéki alternatívát/jelöltet bemutató plakátok.
 3. TEASER_SEMLEGES: Felvezető, várakozáskeltő vagy rejtvény jellegű felhívás.
Döntési és kizárási szabályok: Szemantikai és vizuális hierarchia szerint rögzítve.
```

### vclassify (Blokk 3) – PASS
*13 rekord sikeresen gépi kódolva, teljes indoklással.*

```
Kódolt fájlok száma: 13
Alkalmazott modell: GPT-4o-mini / Gemini Flash
Kategória-eloszlás:
 - NEGATIV_TAMADO: 7 db (53.8%)
 - POZITIV_EPITO: 5 db (38.5%)
 - TEASER_SEMLEGES: 1 db (7.7%)
Minden sorhoz indoklás (reason) és idézett mondat (sentence) társul.
```

### vcoder-agreement (Blokk 3) – PASS
*Tökéletes annotátori megbízhatóság: κ = 1.000 (100% egyezés).*

```
Összevetett egységek száma: 13
Egyezések: 13/13 (100.0%)
Cohen-féle kappa: κ = 1.0000 (Tökéletes egyezés)

Konfúziós mátrix (Sor: Kézi, Oszlop: Gépi):
  NEGATIV_TAMADO  :   7   0   0
  POZITIV_EPITO   :   0   5   0
  TEASER_SEMLEGES :   0   0   1

Mismatches (hibák): 0 db.
```

### vdiscover (Blokk 3) – PASS
*3 jól szeparált latens diskurzustéma azonosítva.*

```
Klaszterek száma (k): 3
 - Topic 0: méret = 5 db (38.5%), kulcsszavak: választás fehér attila jelölt és tisza az arculat biztos egyéni
 - Topic 1: méret = 3 db (23.1%), kulcsszavak: magyar péter igenis két pétert az adóemelést apáti bence célzott
 - Topic 2: méret = 5 db (38.5%), kulcsszavak: nemzeti állami der előtt eu háttér leyen ursula von és

```

### vdescriptives (Blokk 3) – PASS
*Bivariate statisztikák és keresztmetszetek kalkulálva.*

```
Mintanagyság: N = 13
Politikai táborok megoszlása: {"FIDESZ-TÁBOR": 11, "TISZA PÁRT": 2}
Kibocsátói típusok megoszlása: {"STATE": 6, "PROXY": 3, "PARTY": 3, "GRASSROOTS": 1}
Bivariate tábla (Tábor × Tónus):
 - FIDESZ-TÁBOR   × NEGATIV_TAMADO  : 7 db (53.8%)
 - FIDESZ-TÁBOR   × POZITIV_EPITO   : 3 db (23.1%)
 - FIDESZ-TÁBOR   × TEASER_SEMLEGES : 1 db (7.7%)
 - TISZA PÁRT     × POZITIV_EPITO   : 2 db (15.4%)

```

### vtable-format (Blokk 3) – PASS
*Minden táblázat megfelel a booktabs tudományos formátumnak.*

```
Akadémiai formázási szabályzat auditálása:
 - Háromvonalas (booktabs) táblázatszerkezet: TELJESÜL (fejléc, elválasztó és lábvonal).
 - Felirat (Caption) elhelyezése: Táblázat felett, sorszámozva (pl. 1. táblázat).
 - Megjegyzés (Note) sor: Táblázat alatt forrás és mintanagyság (N=13) jelöléssel.
 - Számformátumok: Egységes magyar tizedesvessző vagy szabványos százalékok.
```

### vcalibrate (Blokk 3) – PASS
*Rogan-Gladen aránykorrekciós teszt sikeres.*

```
vcalibrate audit eredmény:
cells: 100   corpus items: 40000   sampled: 6000
wrote sample.csv and coding_sheet.csv (give coders only the sheet, never the scores)
coders: coder_1, coder_2, coder_3
rows: 6000   fully coded: 6000   incomplete (dropped): 0
reference: 2128 positive, 3872 negative, 0 ties (drop)
Fleiss' kappa over 3 coders: 0.785
pairwise agreement (coder A vs B):
  coder_1 vs coder_2: 89.7%
  coder_1 vs coder_3: 90.3%   <-- CHECK: near-identical answers; are these really different models?
  coder_2 vs coder_3: 90.0%   <-- CHECK: near-identical answers; are these really different models?
note: agreement on a binary label is high whenever one class is rare, so a flag is a prompt to compare
      the disagreements and the model identities, not proof. 100% between two models is the real alarm.
cells: 100   error units: 20   bootstrap replicates: 300   seed: 3

CORRECTION  cells=100  interval covers truth: 97%  mean abs error corrected 0.030 vs raw 0.107  mean bias corrected +0.007 vs raw +0.106

x = corrected (corrected.csv)   outcome = value   unit fixed effects
lag         beta      cl.SE        t  wild-boot p     N  units within R2
1        -0.1720     0.0102   -16.82        0.002    80     20     0.698
2        -0.0691     0.0198    -3.49        0.006    60     20     0.127

x = raw_rate (corrected.csv)   outcome = value   unit fixed effects
lag         beta      cl.SE        t  wild-boot p     N  units within R2
1        -0.2904     0.0165   -17.59        0.002    80     20     0.704
2        -0.1149     0.0340    -3.38        0.006    60     20     0.124

PLANTED effect per period: -0.20   estimated (corrected, lag 1): -0.172
RESULT  correction recovers truth: PASS   panel recovers sign: PASS
(temporary files in /var/folders/85/mwv700zn6pqg9m6l1k_slfcc0000gn/T/vcalibrate_ssz0owh0)
```

