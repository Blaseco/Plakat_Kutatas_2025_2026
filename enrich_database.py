#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gazdagított adatbázis-generáló és integrációs szkript
Magyar Közpolitikai Plakátkorpusz (2025–2026)
Integrálja a tartalmi, vizuális és szlogenbeli összehasonlító dimenziókat,
valamint a vclassify és vdiscover kódolási eredményeket az SQL, CSV és JSON adatbázisokba.
"""

import os
import csv
import json
import sqlite3

BASE_DIR = "/Users/blaseco/Desktop/ai kurzus/Plakat_Kutatas_2025_2026"

# Kiegészítő szemiotikai, tartalmi és retorikai adatok
ENRICHMENT = {
    "HUN_PLAKAT_2025_001": {
        "kampany_tonus": "NEGATIV_TAMADO",
        "tartalmi_fokusz": "Kormányzati szuverenitásvédelem; a döntéshozatal kiszervezése elleni mozgósítás; Brüsszel és Ukrajna külső nyomásának elutasítása.",
        "vizualis_szemiotika": "Tekintélykék kormányzati háttér; montázs technika; V. Zelenszkij és M. Weber szigorú, komor fekete-fehér/szürkített tekintete; aránytalanul nagy arcok.",
        "szlogen_retorika": "Felszólító tagadás és kollektív cselekvésre buzdítás („Ne hagyjuk, hogy a fejünk felett döntsenek!”); polarizáló, veszélyelhárító keretezés.",
        "latens_tema_id": 2,
        "latens_tema_nev": "Állami szuverenitási & háborús diskurzus"
    },
    "HUN_PLAKAT_2025_002": {
        "kampany_tonus": "NEGATIV_TAMADO",
        "tartalmi_fokusz": "Plebiszciter legitimáció és Ukrajna EU-csatlakozásának elutasítása; véleménynyilvánítás demonstrálása.",
        "vizualis_szemiotika": "Tömegjelenet és sárga-kék EU-Ukrajna szimbolika; dinamikus feliratok; számszerűsített többségi legitimáció (2 millió).",
        "szlogen_retorika": "Győzelmi deklaráció és határozott elutasítás („Megmutattuk, hogy van véleményünk! 2 millió nem Ukrajna EU-tagságára!”); többségi felhatalmazás.",
        "latens_tema_id": 2,
        "latens_tema_nev": "Állami szuverenitási & háborús diskurzus"
    },
    "HUN_PLAKAT_2025_003": {
        "kampany_tonus": "NEGATIV_TAMADO",
        "tartalmi_fokusz": "Proxy karaktergyilkosság; Magyar Péter (Tisza) és Volodimir Zelenszkij azonosítása; külföldi érdekek kiszolgálásának vádja.",
        "vizualis_szemiotika": "Gúnyos karikatúra és szürreális montázs; törött tojáshéjakban ülő figurák; ukrán zászló lengetése; rikító sárga és kék színkód.",
        "szlogen_retorika": "Közmondásos metafora („MINT KÉT TOJÁS”); minimális magyarázat nélküli asszociatív identitás-összemosás.",
        "latens_tema_id": 1,
        "latens_tema_nev": "Proxy karaktergyilkosság & báb-narratíva"
    },
    "HUN_PLAKAT_2025_004": {
        "kampany_tonus": "NEGATIV_TAMADO",
        "tartalmi_fokusz": "Gúnyos politikai delegitimálás; a Tisza Párt kongresszusi eseményének és vezetőjének nevetségessé tétele.",
        "vizualis_szemiotika": "Mozgó teherautós gerilla-óriásplakát a Tisza kongresszus helyszínén; esőáztatta hangulat; minimalista betűtípus.",
        "szlogen_retorika": "Eufemisztikus gúny és idézőjeles lekicsinylés („Volt egy zápor”); kontextuális politikai vicc a sajtóhírekre reagálva.",
        "latens_tema_id": 1,
        "latens_tema_nev": "Proxy karaktergyilkosság & báb-narratíva"
    },
    "HUN_PLAKAT_2025_005": {
        "kampany_tonus": "NEGATIV_TAMADO",
        "tartalmi_fokusz": "Egzisztenciális fenyegetés (adóemelés); a brüsszeli vezetés és a hazai ellenzék báb-kapcsolatának vádkonstrukciója.",
        "vizualis_szemiotika": "Metaforikus bábozó kéz a felső képtérben; zsinóron mozgatott ellenzéki politikusok; hideg kék-sárga EU színvilág.",
        "szlogen_retorika": "Címkéző vádemelés és fenyegetéskeretezés („Brüsszel bábjai adót akarnak emelni!”); közvetlen anyagi fenyegetettség érzékeltetése.",
        "latens_tema_id": 2,
        "latens_tema_nev": "Állami szuverenitási & háborús diskurzus"
    },
    "HUN_PLAKAT_2025_006": {
        "kampany_tonus": "POZITIV_EPITO",
        "tartalmi_fokusz": "Családpolitikai jóléti intézkedések; adócsökkentés népszerűsítése; szociális biztonságérzet erősítése.",
        "vizualis_szemiotika": "Harmonikus, mosolygó többgenerációs család közös étkezése; meleg természetes fények; otthonos, polgári idill.",
        "szlogen_retorika": "Megszólító jogosultsági ígéret („A családi adócsökkentés az Ön családjának is jár!”); inkluzív állami gondoskodás.",
        "latens_tema_id": 2,
        "latens_tema_nev": "Kormányzati szakpolitikai kommunikáció"
    },
    "HUN_PLAKAT_2025_007": {
        "kampany_tonus": "TEASER_SEMLEGES",
        "tartalmi_fokusz": "Új politikai szereplő (Steiner Attila államtitkár/képviselőjelölt) bevezetése a közvéleménybe; figyelemfelkeltés.",
        "vizualis_szemiotika": "Magas kontrasztú fekete-fehér arculat; arc nélküli rejtélyes férfisziluett; tiszta, sallangmentes háttér.",
        "szlogen_retorika": "Kíváncsiságkeltő retorikai kérdés („Ki az a Steiner Attila?”); teaser kampánystratégia, várakozáskeltés.",
        "latens_tema_id": 0,
        "latens_tema_nev": "Választási jelöltállítás & mozgósítás"
    },
    "HUN_PLAKAT_2026_008": {
        "kampany_tonus": "NEGATIV_TAMADO",
        "tartalmi_fokusz": "Pénzügyi szuverenitás és büntetések megtagadása; uniós elvárásokkal szembeni ellenállás (Nemzeti Petíció).",
        "vizualis_szemiotika": "Ursula von der Leyen, Manfred Weber és Volodimir Zelenszkij arcképei nyomasztó háttérben; nagy méretű, vörös figyelmeztető tiltó sávok.",
        "szlogen_retorika": "Kollektív dac imperatívusza és elutasító felkiáltás („Üzenjük Brüsszelnek: NEM FIZETÜNK!”); harcias ellenállási retorika.",
        "latens_tema_id": 2,
        "latens_tema_nev": "Állami szuverenitási & háborús diskurzus"
    },
    "HUN_PLAKAT_2026_009": {
        "kampany_tonus": "NEGATIV_TAMADO",
        "tartalmi_fokusz": "Magyar Péter politikai akaratgyengeségének és brüsszeli alárendeltségének leleplezési kísérlete.",
        "vizualis_szemiotika": "Karikatúra-jellegű megalázkodó beállítás; parancsoló kezek felülről; rikító piros és sárga figyelemfelkeltő feliratok.",
        "szlogen_retorika": "Katonás parancs-engedelmesség struktúra („ADÓEMELÉST! PÉNZT UKRAJNÁNAK! – IGENIS!”) és sommás ítélet („NEM TUD NEKIK NEMET MONDANI”).",
        "latens_tema_id": 1,
        "latens_tema_nev": "Proxy karaktergyilkosság & báb-narratíva"
    },
    "HUN_PLAKAT_2026_010": {
        "kampany_tonus": "POZITIV_EPITO",
        "tartalmi_fokusz": "Kormányzati stabilitás és helyi képviselet; a hivatalos kormánypárti egyéni jelölt (Berkó Attila) legitimálása.",
        "vizualis_szemiotika": "Narancs-fehér hivatalos Fidesz-KDNP arculat; öltönyös, professzionális, bizalmat keltő politikusportré közvetlen szemkontaktussal.",
        "szlogen_retorika": "Minősítő tételmondat („A BIZTOS VÁLASZTÁS”); a kockázatkerülésre és a stabilitásra építő politikai toposz.",
        "latens_tema_id": 0,
        "latens_tema_nev": "Választási jelöltállítás & mozgósítás"
    },
    "HUN_PLAKAT_2026_011": {
        "kampany_tonus": "POZITIV_EPITO",
        "tartalmi_fokusz": "Rezsivédelem, megfizethető üzemanyagárak; a kormányzati gazdasági intézkedések nemzetközi felsőbbrendűsége.",
        "vizualis_szemiotika": "Benzinkút piktogram, ábrázolt árösszehasonlítás, kék kormányzati alapszín, pozitív zöld megerősítő grafikai elemek.",
        "szlogen_retorika": "Tényszerűséget sugalló szuperlatívusz („Védett üzemanyagár – ...legolcsóbb Európában!”); gazdasági sikerpropaganda.",
        "latens_tema_id": 0,
        "latens_tema_nev": "Kormányzati szakpolitikai kommunikáció"
    },
    "HUN_PLAKAT_2026_012": {
        "kampany_tonus": "POZITIV_EPITO",
        "tartalmi_fokusz": "Ellenzéki kihívó helyi szintű bemutatása; a Tisza Párt egyéni jelöltjének (Mészáros Dávid) ismertségépítése.",
        "vizualis_szemiotika": "Kandeláberre rögzített kartonplakát; piros-fehér-kék nemzeti trikolór arculat; fiatal, civil benyomást keltő portré.",
        "szlogen_retorika": "Funkcionális, azonosító márkázás („TISZA – VÁLASZTÁS 2026”); közvetlen jelölti megnevezés sallangok nélkül.",
        "latens_tema_id": 0,
        "latens_tema_nev": "Választási jelöltállítás & mozgósítás"
    },
    "HUN_PLAKAT_2026_013": {
        "kampany_tonus": "POZITIV_EPITO",
        "tartalmi_fokusz": "Rendszerváltó hangulat, állampolgári ellenállás és önkéntes mozgósítás; politikai fordulat sürgetése.",
        "vizualis_szemiotika": "Magánház kerítésére/erkélyére rögzített lakossági molinó; DIY / grassroots esztétika; Tisza logó és nemzeti színek.",
        "szlogen_retorika": "Petőfies, nemzeti-romantikus imperatívusz („Most vagy soha!”); végletes morális és történelmi döntéskényszer.",
        "latens_tema_id": 0,
        "latens_tema_nev": "Választási jelöltállítás & mozgósítás"
    }
}

# 1. Olvassuk be a létező CSV-t
csv_in = os.path.join(BASE_DIR, "plakat_kutatas_korpusz_2025_2026.csv")
with open(csv_in, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# 2. Gazdagítsuk az adatokat
enriched_rows = []
for r in rows:
    pid = r["id"]
    enr = ENRICHMENT.get(pid, {})
    new_r = dict(r)
    new_r["kampany_tonus"] = enr.get("kampany_tonus", "N/A")
    new_r["tartalmi_fokusz"] = enr.get("tartalmi_fokusz", "")
    new_r["vizualis_szemiotika"] = enr.get("vizualis_szemiotika", "")
    new_r["szlogen_retorika"] = enr.get("szlogen_retorika", "")
    new_r["latens_tema_id"] = enr.get("latens_tema_id", 0)
    new_r["latens_tema_nev"] = enr.get("latens_tema_nev", "")
    enriched_rows.append(new_r)

fieldnames = list(rows[0].keys()) + [
    "kampany_tonus", "tartalmi_fokusz", "vizualis_szemiotika", "szlogen_retorika", "latens_tema_id", "latens_tema_nev"
]

# 3. Írjuk ki a standard CSV-t
csv_out_std = os.path.join(BASE_DIR, "plakat_kutatas_korpusz_2025_2026.csv")
with open(csv_out_std, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(enriched_rows)
print(f"Standard CSV mentve: {csv_out_std}")

# 4. Írjuk ki az Excel-barát CSV-t (pontosvessző, UTF-8-sig)
csv_out_excel = os.path.join(BASE_DIR, "plakat_kutatas_korpusz_2025_2026_excel.csv")
with open(csv_out_excel, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    writer.writerows(enriched_rows)
print(f"Excel CSV mentve: {csv_out_excel}")

# Másolat a plakat_adatbazis_2025_2026.csv-be is
csv_out_db = os.path.join(BASE_DIR, "plakat_adatbazis_2025_2026.csv")
with open(csv_out_db, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(enriched_rows)
print(f"DB CSV mentve: {csv_out_db}")

# 5. Írjuk ki a JSON formátumot
json_out = os.path.join(BASE_DIR, "ParlLawSpeech_Plakat_Korpusz_2025_2026.json")
with open(json_out, "w", encoding="utf-8") as f:
    json.dump({
        "korpusz_meta": {
            "nev": "Magyar Közpolitikai Plakátkorpusz (2025–2026)",
            "keszito": "Varga Balázs",
            "kurzus": "Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (Bibó Szakkollégium)",
            "rekordok_szama": len(enriched_rows),
            "verzio": "2.0_Enriched"
        },
        "plakatok": enriched_rows
    }, f, ensure_ascii=False, indent=2)
print(f"JSON mentve: {json_out}")

# 6. SQLite adatbázis frissítése (.db)
db_path = os.path.join(BASE_DIR, "plakat_adatbazis_2025_2026.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Eldobjuk a régi táblát és újraépítjük a gazdagított struktúrával
cur.execute("DROP TABLE IF EXISTS plakatok;")
cur.execute("""
CREATE TABLE plakatok (
    id TEXT PRIMARY KEY,
    datum TEXT NOT NULL,
    politikai_tabor TEXT NOT NULL,
    kibocsato_tipus TEXT NOT NULL,
    hivatalos_kiado TEXT NOT NULL,
    fajl_nev TEXT NOT NULL,
    plakat_szlogen TEXT NOT NULL,
    vizualis_leiras TEXT NOT NULL,
    formatum_meret TEXT NOT NULL,
    politikai_elemzes TEXT NOT NULL,
    forras_nev TEXT NOT NULL,
    forras_url TEXT NOT NULL,
    kampany_tonus TEXT NOT NULL,
    tartalmi_fokusz TEXT NOT NULL,
    vizualis_szemiotika TEXT NOT NULL,
    szlogen_retorika TEXT NOT NULL,
    latens_tema_id INTEGER NOT NULL,
    latens_tema_nev TEXT NOT NULL
);
""")

for r in enriched_rows:
    cur.execute("""
    INSERT INTO plakatok (
        id, datum, politikai_tabor, kibocsato_tipus, hivatalos_kiado, fajl_nev,
        plakat_szlogen, vizualis_leiras, formatum_meret, politikai_elemzes,
        forras_nev, forras_url, kampany_tonus, tartalmi_fokusz, vizualis_szemiotika,
        szlogen_retorika, latens_tema_id, latens_tema_nev
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        r["id"], r["datum"], r["politikai_tabor"], r["kibocsato_tipus"], r["hivatalos_kiado"], r["fajl_nev"],
        r["plakat_szlogen"], r["vizualis_leiras"], r["formatum_meret"], r["politikai_elemzes"],
        r["forras_nev"], r["forras_url"], r["kampany_tonus"], r["tartalmi_fokusz"], r["vizualis_szemiotika"],
        r["szlogen_retorika"], r["latens_tema_id"], r["latens_tema_nev"]
    ))

conn.commit()
conn.close()
print(f"SQLite DB frissítve: {db_path}")

# 7. SQL export script generálása (.sql)
sql_path = os.path.join(BASE_DIR, "plakat_adatbazis_2025_2026.sql")
with open(sql_path, "w", encoding="utf-8") as f:
    f.write("-- ====================================================================\n")
    f.write("-- Magyar Közpolitikai Plakátkorpusz (2025–2026) Adatbázis\n")
    f.write("-- Készítő: Varga Balázs | Bibó István Szakkollégium\n")
    f.write("-- Kurzus: Mesterséges intelligencia a társadalom- és politikatudományi kutatásban\n")
    f.write("-- ====================================================================\n\n")
    f.write("DROP TABLE IF EXISTS plakatok;\n\n")
    f.write("CREATE TABLE plakatok (\n")
    f.write("    id VARCHAR(32) PRIMARY KEY,\n")
    f.write("    datum DATE NOT NULL,\n")
    f.write("    politikai_tabor VARCHAR(64) NOT NULL,\n")
    f.write("    kibocsato_tipus VARCHAR(32) NOT NULL,\n")
    f.write("    hivatalos_kiado VARCHAR(128) NOT NULL,\n")
    f.write("    fajl_nev VARCHAR(128) NOT NULL,\n")
    f.write("    plakat_szlogen TEXT NOT NULL,\n")
    f.write("    vizualis_leiras TEXT NOT NULL,\n")
    f.write("    formatum_meret VARCHAR(64) NOT NULL,\n")
    f.write("    politikai_elemzes TEXT NOT NULL,\n")
    f.write("    forras_nev VARCHAR(128) NOT NULL,\n")
    f.write("    forras_url TEXT NOT NULL,\n")
    f.write("    kampany_tonus VARCHAR(32) NOT NULL,\n")
    f.write("    tartalmi_fokusz TEXT NOT NULL,\n")
    f.write("    vizualis_szemiotika TEXT NOT NULL,\n")
    f.write("    szlogen_retorika TEXT NOT NULL,\n")
    f.write("    latens_tema_id INT NOT NULL,\n")
    f.write("    latens_tema_nev VARCHAR(128) NOT NULL\n")
    f.write(");\n\n")

    for r in enriched_rows:
        def esc(val):
            return str(val).replace("'", "''")
        cols = ", ".join(fieldnames)
        vals = ", ".join(f"'{esc(r[fn])}'" if not isinstance(r[fn], int) else str(r[fn]) for fn in fieldnames)
        f.write(f"INSERT INTO plakatok ({cols}) VALUES ({vals});\n")

print(f"SQL dump mentve: {sql_path}")
