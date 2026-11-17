# Codebook — 2025–2026 Magyar Politikai Plakátkutatás · v1.0 · 2026-11-17
Unit of observation: one political poster (document level: headline slogan, visual semiotics, framing).
Set-aside code: SET_ASIDE (no code applies / insufficient data).

## Codes

### 1 NEGATIV_TAMADO
Definition: A plakát elsődleges célja egy politikai ellenfél, külső szereplő vagy nemzetközi intézmény negatív színben való feltüntetése, fenyegetésként vagy alkalmatlanként való keretezése.
Include when: Ellenségkép, támadás, gúny, bírálat, adóemelési, korrupciós vagy háborús vád jelenléte a szlogenben vagy a kép kompozíciójában.
Example: „Brüsszel bábjai adót akarnak emelni! – Nemzeti Konzultáció” (HUN_PLAKAT_2025_005)
Near miss: „Védett üzemanyagár – A benzin és a gázolaj hazánkban a legolcsóbb Európában!” (HUN_PLAKAT_2026_011) — nem negatív támadás, mert nem támad konkrét ellenfelet, hanem kormányzati intézkedést hirdet -> POZITIV_EPITO.

### 2 POZITIV_EPITO
Definition: A plakát elsődleges célja a saját politikai eredmények, szakpolitikák, stabilitás, családtámogatás, jövőkép vagy saját jelöltek melletti elköteleződés és választási mozgósítás bemutatása, támadó él nélkül.
Include when: Saját jelölt portréja pozitív felirattal, szakpolitikai intézkedés eredménye, békét, stabilitást, reményt hirdető üzenet, lakossági mozgósítás.
Example: „A családi adócsökkentés az Ön családjának is jár!” (HUN_PLAKAT_2025_006), „A BIZTOS VÁLASZTÁS – Fidesz–KDNP (Berkó Attila)” (HUN_PLAKAT_2026_010), „Most vagy soha!” (HUN_PLAKAT_2026_013)
Near miss: „VOKS 2025 – Ne hagyjuk, hogy a fejünk felett döntsenek!” (HUN_PLAKAT_2025_001) — bár szavazásra buzdít, a fő narratíva és kép az ellenségképre és külső fenyegetésre épül -> NEGATIV_TAMADO.

### 3 TEASER_SEMLEGES
Definition: Figyelemfelkeltő (teaser) vagy pusztán információs kampány, amely nem tartalmaz sem nyílt negatív támadást, sem kifejtett pozitív pártprogramot.
Include when: Információs kérdés, sziluett, rejtélyes bevezető elem, amely egy későbbi kampányfázist készít elő.
Example: „Ki az a Steiner Attila?” (HUN_PLAKAT_2025_007)
Near miss: „Volt egy zápor” (HUN_PLAKAT_2025_004) — bár rövid szöveg, kontextuálisan Magyar Pétert gúnyoló negatív akció -> NEGATIV_TAMADO.

## Decision rules
- Két kód versenye: Ha egy plakát egyszerre tartalmaz mozgósítást és ellenségképet (pl. VOKS 2025), a domináns negatív fenyegetés-keretezés nyer -> NEGATIV_TAMADO.
- Képi gúny vs. semlegesség: Ha a szöveg önmagában semlegesnek tűnne, de a képi kompozíció gúnyos (pl. tojáshéjban ülő politikusok), a negatív kód alkalmazandó -> NEGATIV_TAMADO.
- Üres vagy értékelhetetlen egység: SET_ASIDE.

## Hand-coding plan
Units: 13 (teljes korpusz) · coder: Varga Balázs · vak kódolás a gépi előrejelzések előtt · validálás: vcoder-agreement.
