# 🎤 PREZENTÁCIÓS MESTERTÉRKÉP ÉS VÉDÉSI FORGATÓKÖNYV (10 PERC)
## Bibó István Szakkollégium · AI Kurzus (2026 ősz) · Dr. Sebők Miklós
**Előadó:** Varga Balázs  
**Kutatás:** A 2025–2026-os magyar óriásplakát-kampányok összehasonlító tartalomelemzése, szemiotikája és gépi kódolása  
**Fő fájl az előadáshoz:** `Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf`  
**Élő felület:** `https://3c0998cbb947e0.app.lhr.life/comparison.html` vagy `comparison.html`

---

## ⏱️ 1. Percről percre forgatókönyv (10 perc / 10 dia)

| Perc & Dia | Mit mutatsz a képernyőn? | Mit mondasz? (A lényeg 2 mondatban) |
|---|---|---|
| **1. perc**<br/>Cím & Kontextus | Címdia, kutatási kérdés, unit of analysis | *„A kutatásom a 2026-os választást megelőző óriásplakát-kampányokat vizsgálja. A megfigyelési egység az egyedi plakát (n=13), az elemzési egység pedig a politikai táborok stratégiai napirend-kijelölése.”* |
| **2. perc**<br/>Hipotézisek | Fő állítás (Claim) és a cáfolati feltétel (*What would sink it*) | *„Hipotézisem: a kormánypárt külső ellenségre és fenyegetésre épít, míg az ellenzék pozitív jövőképre és cselekvésre buzdít. A hipotézist az döntené meg, ha a kormánypártnál a pozitív szakpolitika >50% lenne, vagy az ellenzék karaktergyilkossággal kampányolna.”* |
| **3. perc**<br/>Módszertan | A 12 Sebők skill táblázata, κ = 1.000 megbízhatóság | *„A módszertan szigorúan a ParlLawSpeech és a kurzus 12 skilljére épül. A gépi címkéket (labels.csv) vakon teszteltem a saját kézi kódolásommal (hand.csv): 100% egyezés és Cohen κ = 1.000 jött ki.”* |
| **4. perc**<br/>1-2. Grafikon | 1. ábra (Tónus táboronként) & 2. ábra (Kibocsátók) | *„Az 1. ábrán látható a drámai aszimmetria: a kormánypárti mintában 63.6% a negatív, míg az ellenzéknél 100% a pozitív tónus. A 2. ábrán látszik a szerepmegosztás: a kormánynak a Miniszterelnöki Kabinetiroda, a Fidesz és a CÖF-CÖKA adja a felületeket.”* |
| **5. perc**<br/>3-4. Grafikon | 3. ábra (Latens témák) & 4. ábra (Szemiotikai mátrix) | *„A /vdiscover TF-IDF algoritmusa 3 látens témát tárt fel, amelyeket a plakátok elolvasása alapján neveztünk el. A szemiotikai mátrix bizonyítja: a kormánypártnál a montázs és a felszólító tagadás dominál, az ellenzéknél a partneri cselekvésre hívás.”* |
| **6. perc**<br/>Összehasonlítás 1 | VOKS 2025 vs CÖF „Mint két tojás” | *„Kvalitatív összehasonlítás 1: A kormányzat a szuverenitási fenyegetést intézményi szinten keretezi (Zelenszkij, Weber), míg a CÖF-CÖKA mint harmadik fél nyers gúnyos montázzsal (tojáshéj) támadja az ellenzéki vezetőt.”* |
| **7. perc**<br/>Összehasonlítás 2 | Steiner Attila teaser vs Tisza egyéni jelölt | *„Kvalitatív összehasonlítás 2: Kormánypárti oldalon a teaser technika jelenik meg ('Ki az a Steiner Attila?'), míg a Tisza Pártnál a helyi jelöltek közvetlen, mosolygó, elérhető arcképe a domináns.”* |
| **8. perc**<br/>Összehasonlítás 3 | „Nem fizetünk” vs Lakossági „Most vagy soha” | *„Kvalitatív összehasonlítás 3: A brüsszeli büntetés elleni agresszív nagybetűs dac ('NEM FIZETÜNK') áll szemben a grassroots, saját finanszírozású, rendszerváltó reményt kifejező plakátokkal.”* |
| **9. perc**<br/>Módszertani hibák & Védelem | Collection gap, Rogan-Gladen kalibráció, határesetek | *„Transzparens hibareflexió: A mintában az ellenzéki plakátok alacsonyabb száma médiavásárlási korlát (collection gap), nem pedig passzivitás. A Rogan-Gladen korrekció pedig megvédi a modellt, ha a klasszifikátor zajos lenne.”* |
| **10. perc**<br/>Konklúzió & A vposter skill | A reproduce.py futtatása, GitHub repó | *„Összegzésként létrehoztam a vposter skillt, amely egyetlen paranccsal (reproduce.py) bárki által újraellenőrizhetővé teszi az összes számot, táblázatot és ábrát. Köszönöm a figyelmet, várom az opponensi kérdéseket!”* |

---

## ⚡ 2. A 3 másodperces terminálos villantás (Live Demo)

Ha Sebők tanár úr vagy az opponens megkérdezi: *„Valóban működik a kódod?”*:

1. Nyisd meg a terminált:
   ```bash
   cd "/Users/blaseco/Desktop/bibó ai 2026 végleges"
   ```
2. Futtasd a reprodukciós mesterkódot:
   ```bash
   python3 reproduce.py
   ```
3. **Mit fog látni a tanár és az opponens?**
   * Ellenőrzi a 13 plakát 100%-os teljességét.
   * Kiírja a $\kappa = 1.0000$ megbízhatóságot és a konfúziós mátrixot.
   * Megrajzolja a **Table 1** booktabs táblázatot.
   * Újragenerálja mind a 4 diagramot determinisztikusan.
   * Kiszámolja a Rogan–Gladen korrekciót ($P^* = 53.8\%$).
   * Zárás: `✓ REPRODUKCIÓ SIKERESEN LEFUTOTT!`

---

## 🛡️ 3. Felkészülés a tanári és opponensi keresztkérdésekre

### 1. Kérdés: *„Nem túl kevés az n = 13 plakát egy komoly elemzéshez?”*
* **A nyerő válasz:** *„Tanár úr, a kurzus Slide 4-es és 37-es diája alapján a cél egy szigorúan operacionalizált, ellenőrizhető pilot és munkafolyamat felépítése volt. A 13 plakát nem random gyűjtés, hanem a 2025–2026-os kampányidőszak összes releváns, közterületen megjelent fő kampánytípusának reprezentatív lefedése (kormány, párt, CÖF, Tisza, grassroots). A vposter skill architektúrája skálázható: az add_poster.py segítségével 130 vagy 1300 plakátra is másodpercek alatt lefut ugyanez a verifikáció.”*

### 2. Kérdés: *„Miért lett a Cohen-kappa pontosan 1.000? Nem túl tökéletes?”*
* **A nyerő válasz:** *„A tökéletes egyezés oka a /vcodebook szigorúsága: nem bíztuk a véletlenre a kategóriákat, hanem zárt rendszert alkottunk (Negatív, Pozitív, Teaser, Set-aside), explicit határvonal-szabállyal (fővizuális dominancia elve). Mivel a kódkönyv egyértelmű volt, a Gemini nyelvi modell és a kutatói arany standard (hand.csv) pontosan ugyanarra a következtetésre jutott. Ezt a Slide 27 elvárása szerint a konfúziós mátrix nulla hibával bizonyítja.”*

### 3. Kérdés: *„Miért számoltál Rogan–Gladen korrekciót, ha a klasszifikátorod hibátlan (Se=1.0, Sp=1.0)?”*
* **A nyerő válasz:** *„Mert a /vcalibrate módszertan lényege (Slide 42), hogy a regresszió megörökli a mérési hibát. Ha a modell tökéletes, a Rogan–Gladen formula P* = P értéket ad vissza (53.8%). Viszont a reproduce.py szimulációjában levezettem azt is, hogy mi történik, ha egy olcsóbb, zajosabb modellt használnánk (Se=0.85, Sp=0.80): a formula azonnal levonja a torzítást, megvédve a kutatást a hamis trendektől.”*

### 4. Kérdés: *„Miért van olyan kevés ellenzéki plakát a mintában?”*
* **A nyerő válasz:** *„Ez a Slide 41-en tárgyalt klasszikus 'collection gap' esete: nem a politikai passzivitás jele, hanem a magyar köztéri médiavásárlási piac aszimmetriájának (pl. Publimont, állami felületek) közvetlen következménye. Az ellenzéki és Tisza-párti kampány nem az óriásplakát-piacon, hanem a közösségi médiában, kandeláber-táblákon és önkéntes felületeken koncentrálódik.”*

---

## 🌐 4. Mit nyiss meg a kivetítőn a prezentáció előtt?

1. **A PDF bemutatót:** `Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf` (itt van minden szöveg és kép diákra bontva).
2. **Az interaktív összehasonlítót egy külön böngészőlapon:**  
   `https://3c0998cbb947e0.app.lhr.life/comparison.html`
3. **Egy terminál ablakot** a háttérben készenlétben a `python3 reproduce.py` parancshoz.
