# Projekt Házirend (Project Guidelines) — 2025–2026 Magyar Politikai Plakátkutató Korpusz

## 1. Általános adatintegritási szabályok
- **Módszertani szabvány:** ParlLawSpeech Outdoor Standard (2025).
- **Karakterkódolás:** Kizárólag érvényes UTF-8 kódolás engedélyezett (helyettesítő karakterek, roncsolt ékezetek tilosak).
- **Kötelező változók:** A 12 alapadatmező (`id`, `datum`, `politikai_tabor`, `kibocsato_tipus`, `hivatalos_kiado`, `fajl_nev`, `plakat_szlogen`, `vizualis_leiras`, `formatum_meret`, `politikai_elemzes`, `forras_nev`, `forras_url`) minden rekordnál 100%-os teljességgel kitöltendő.
- **Relációs szinkronitás:** A CSV (`plakat_kutatas_korpusz_2025_2026.csv`), a JSON (`ParlLawSpeech_Plakat_Korpusz_2025_2026.json`) és az SQLite adatbázis (`plakat_adatbazis_2025_2026.db`) mindig azonos rekordszámmal és tartalommal kell rendelkezzen.

## 2. Kép- és médiaarchívum
- Minden rögzített plakáthoz tartoznia kell egy vágott sajtófotónak a `vagott_kepek/` mappában (`HUN_PLAKAT_YYYY_XXX.jpg` elnevezéssel).
- Az eredeti, vágatlan sajtófotókat a forrásazonosítóval az `eredeti_sajto_kepek/` mappa tárolja.

## 3. Minőségbiztosítás és Skillek
- Új rekordok felvétele vagy forráskaparás után kötelező a minőségbiztosítási skillek futtatása:
  - `vscrape`: Udvarias, olcsó scraping és forrásletöltés (`fetch.py`).
  - `datavalidation`: Teljességi, duplikációs és anomália-ellenőrzés (5 lépés).
  - `record-linkage`: Entitás- és reláció-ellenőrzés.
  - `data-provenance-checker`: Származtatott adatok forrásigazolása.

## 4. Biztonság és Git fegyelem
- `.env`, API kulcsok, jelszavak és személyes hitelesítő adatok tárolása a repóban tilos.
