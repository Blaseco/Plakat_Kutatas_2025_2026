#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the official 3-page Short Written Analysis PDF for Block 4 Homework.
Course: Bibó István Szakkollégium · Autumn 2026 · Dr. Miklós Sebők
Author: Varga Balázs
Target: Exactly 3 pages (Slide 45: "Short written analysis as a PDF: at most 3 pages, figures and tables count").
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D"))
        # Header (pages 2 and 3)
        if self._pageNumber > 1:
            self.drawString(36, 810, "BIBÓ ISTVÁN SZAKKOLLÉGIUM · AI KURZUS 2026 · RÖVID ELEMZÉS (BLOCK 4)")
            self.drawRightString(559, 810, "VARGA BALÁZS")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)

        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 25, "Kutatási repó & reprodukció: github.com/Blaseco/Plakat_Kutatas_2025_2026 · python3 reproduce.py")
        page_text = f"{self._pageNumber}. oldal / {page_count}"
        self.drawRightString(559, 25, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 35, 559, 35)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_box_style = ParagraphStyle(
        'HeaderBox',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A365D"),
        alignment=0
    )
    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=5
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B"),
        alignment=4 # Justified
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )
    table_note = ParagraphStyle(
        'TableNote',
        fontName='Helvetica-Oblique',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor("#475569")
    )

    story = []

    # =========================================================================
    # PAGE 1: QUESTION, OPERATIONALIZATION, CODEBOOK
    # =========================================================================
    # Top banner
    header_html = "<b>BIBÓ ISTVÁN SZAKKOLLÉGIUM</b> · Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (2026 ősz)<br/><b>Oktató:</b> Dr. Sebők Miklós (Syracuse University / poltextLAB) · <b>Szerző:</b> Varga Balázs · <b>Blokk 4 beadandó</b>"
    story.append(Paragraph(header_html, header_box_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=1, spaceAfter=4))

    # Title
    story.append(Paragraph("A 2025–2026-os magyar óriásplakát-kampányok összehasonlító tartalomelemzése és gépi kódolása", title_style))
    story.append(Paragraph("Kutatási terv, kódkönyvi operacionalizálás és a mérési megbízhatóság validációja", subtitle_style))

    # Section 1
    story.append(Paragraph("1. Kutatási kérdés és operacionalizálás (/vcodebook & Slide 4/44)", h1_style))
    p1_text = (
        "<b>Kutatási kérdés:</b> <i>Milyen mértékben tér el a kormánypárti és ellenzéki óriásplakát-kommunikáció tónusa és szemiotikai keretezése a 2026-os országgyűlési választásokat megelőző kampányidőszakban?</i><br/>"
        "<b>Elemzési egység (Unit of analysis):</b> A politikai aktorok óriásplakát-kampányai mint stratégiai napirend-kijelölési aktusok. "
        "<b>Megfigyelési egység (Unit of observation):</b> Egyedi politikai óriásplakát (n = 13 db, 2025 április – 2026 tavasz).<br/>"
        "<b>Fő állítás (Claim):</b> A kormánypárti/CÖF kampány túlnyomórészt negatív, fenyegetés- és ellenségkép-alapú keretezést alkalmaz (külső veszélyek, háború, brüsszeli adóemelés, báb-narratíva), míg az ellenzéki térfél (Tisza Párt, grassroots) dominánsan pozitív, mobilizáló és jövőképre fókuszáló vizuális retorikát használ.<br/>"
        "<b>Megfigyelhető forma (Observable form):</b> Vizuális színhasználat (komor tekintélykék vs. élénk fehér-türkiz), tipográfiai agresszió (tiltó/felszólító nagybetűs igék vs. inkluzív jövőidő), és a célpontok beállítása (külső ellenség megsemmisítése vs. állampolgári közösségépítés).<br/>"
        "<b>Mi döntené meg a hipotézist? (What would sink the hypothesis):</b> A hipotézis szisztematikusan megdőlne, ha (a) a kormánypárti mintában a pozitív eredménykommunikációs és jövőkép-plakátok aránya meghaladná az 50%-ot, vagy (b) a Tisza Párt és az ellenzéki kampány túlnyomórészt személyes karaktergyilkosságra és egzisztenciális fenyegetésre épülő köztéri hirdetéseket tenne közzé."
    )
    story.append(Paragraph(p1_text, body_style))
    story.append(Spacer(1, 4))

    # Section 2: Codebook Table
    story.append(Paragraph("2. Kódkönyv és kategóriarendszer (/vcodebook)", h1_style))
    cb_intro = (
        "A kódolás a <i>/vcodebook</i> protokoll szerint zárt, kölcsönösen kizáró kategóriarendszerre épül, explicit határvonal-döntési szabályokkal:"
    )
    story.append(Paragraph(cb_intro, body_style))
    story.append(Spacer(1, 3))

    codebook_data = [
        [Paragraph("<b>Kód & Címke</b>", table_cell_bold), Paragraph("<b>Operacionális definíció és inklúziós szabály</b>", table_cell_bold), Paragraph("<b>Valós korpusz példa</b>", table_cell_bold), Paragraph("<b>Határvonal / Kizárás</b>", table_cell_bold)],
        [
            Paragraph("<b>NEGATIV_TAMADO</b><br/>(Negatív / Támadó)", table_cell),
            Paragraph("A fókusz politikai ellenfelek, intézmények vagy csoportok veszélyként, alkalmatlanként való ábrázolása; félelemkeltés, háborús retorika.", table_cell),
            Paragraph("<i>„VOKS 2025 – Ne hagyjuk, hogy a fejünk felett döntsenek!”</i> (Zelenszkij, Weber)", table_cell),
            Paragraph("Kizárva: Tényközlő kormányzati tájékoztatás fenyegető keret nélkül.", table_cell)
        ],
        [
            Paragraph("<b>POZITIV_EPITO</b><br/>(Pozitív / Építő)", table_cell),
            Paragraph("Saját szakpolitikai eredmények, gazdasági intézkedések, közösségi remény, jövőkép hirdetése konstruktív tónusban.", table_cell),
            Paragraph("<i>„A családi adócsökkentés az Ön családjának is jár”</i>; <i>„Most vagy soha!”</i>", table_cell),
            Paragraph("Kizárva: Ha az ellenfél kritikája dominál a pozitív ígéret felett.", table_cell)
        ],
        [
            Paragraph("<b>TEASER_SEMLEGES</b><br/>(Felvezető / Semleges)", table_cell),
            Paragraph("Figyelemfelkeltő, előzetes politikai üzenet explicit politikai vád vagy program nélkül; kognitív nyitás céljából.", table_cell),
            Paragraph("<i>„Ki az a Steiner Attila?”</i> (Kék háttér, kérdőjel, sziluett)", table_cell),
            Paragraph("Kizárva: Azonnal beazonosítható negatív kontextus.", table_cell)
        ],
        [
            Paragraph("<b>SET_ASIDE</b><br/>(Félretett / Elemzésen kívül)", table_cell),
            Paragraph("Nem politikai, sérült, olvashatatlan vagy tisztán kereskedelmi hirdetés, amely nem része a választási diskurzusnak.", table_cell),
            Paragraph("Hiányos vagy letépett hirdetés (jelen korpuszban n = 0).", table_cell),
            Paragraph("Minden vizsgálható plakátnak kötelező célkategóriát kapnia.", table_cell)
        ]
    ]

    cb_table = Table(codebook_data, colWidths=[95, 175, 150, 103])
    cb_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.HexColor("#0F172A")),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.HexColor("#0F172A")),
        ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.HexColor("#0F172A")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(cb_table)
    story.append(Spacer(1, 4))

    # Boundary and holdout rules
    p_rules = (
        "<b>Döntési szabály határesetekre:</b> Amennyiben egy plakát egyszerre tartalmaz pozitív ígéretet és támadó elemet (pl. <i>„Megvédjük a rezsit a brüsszeli emeléstől”</i>), az inklúziós szabály a <i>fővizuális dominancia</i> elvét követi: a legnagyobb betűméretű szlogen és az arcábrázolás érzelmi iránya határozza meg a kódot. A kódkönyv egyben a <i>/vclassify</i> promptja is."
    )
    story.append(Paragraph(p_rules, body_style))

    # Page break to Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: DESCRIPTIVE STATISTICS & RESEARCH CHARTS
    # =========================================================================
    story.append(Paragraph("3. Leíró statisztikák és a korpusz bemutatása (/vdescriptives & /vtable-format)", h1_style))
    p2_intro = (
        "A <i>/vdescriptives</i> és <i>/vtable-format</i> protokoll (Slide 37, 40) alapján a modellezés előtt elengedhetetlen a mintaelemzés és a gyakoriságok közzététele. "
        "A korpusz n = 13 manuálisan és géppel verifikált, geolokált óriásplakátot tartalmaz a 2025–2026-os kampányidőszakból."
    )
    story.append(Paragraph(p2_intro, body_style))
    story.append(Spacer(1, 3))

    # Table 1: Booktabs table
    t1_caption = Paragraph("<b>Table 1.</b> <i>A politikai plakátok tónusbeli megoszlása politikai táborok szerint (2025–2026)</i>", ParagraphStyle('T1Cap', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#0F172A")))
    story.append(t1_caption)
    story.append(Spacer(1, 2))

    table1_data = [
        [Paragraph("<b>Politikai tábor / Kibocsátó</b>", table_cell_bold), Paragraph("<b>Negatív / Támadó</b>", table_cell_bold), Paragraph("<b>Pozitív / Építő</b>", table_cell_bold), Paragraph("<b>Teaser / Semleges</b>", table_cell_bold), Paragraph("<b>Összesen (n)</b>", table_cell_bold), Paragraph("<b>Negatív %</b>", table_cell_bold)],
        [
            Paragraph("Kormánypárti blokk (Kormány, Fidesz, CÖF-CÖKA)", table_cell),
            Paragraph("7", table_cell),
            Paragraph("3", table_cell),
            Paragraph("1", table_cell),
            Paragraph("11", table_cell),
            Paragraph("<b>63.6%</b>", table_cell)
        ],
        [
            Paragraph("Ellenzéki térfél (Tisza Párt, Grassroots)", table_cell),
            Paragraph("0", table_cell),
            Paragraph("2", table_cell),
            Paragraph("0", table_cell),
            Paragraph("2", table_cell),
            Paragraph("<b>0.0%</b>", table_cell)
        ],
        [
            Paragraph("<b>ÖSSZESEN</b>", table_cell_bold),
            Paragraph("<b>7</b>", table_cell_bold),
            Paragraph("<b>5</b>", table_cell_bold),
            Paragraph("<b>1</b>", table_cell_bold),
            Paragraph("<b>13</b>", table_cell_bold),
            Paragraph("<b>53.8%</b>", table_cell_bold)
        ]
    ]

    t1_table = Table(table1_data, colWidths=[175, 75, 75, 75, 60, 63])
    t1_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.HexColor("#0F172A")),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.HexColor("#0F172A")),
        ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.HexColor("#475569")),
        ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.HexColor("#0F172A")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t1_table)
    story.append(Paragraph("<i>Note:</i> N = 13. A táblázat a /vtable-format standard háromvonalas (booktabs) formátumát követi. A kategóriák a <i>/vcodebook</i> és <i>/vclassify</i> szigorú definíciói alapján kerültek besorolásra.", table_note))
    story.append(Spacer(1, 4))

    # Research Figures
    story.append(Paragraph("<b>Empirikus vizualizáció (determinisztikusan reprodukált grafikonok):</b>", body_bold))
    story.append(Spacer(1, 2))

    chart1_path = os.path.join(BASE_DIR, "kutatasi_grafikonok", "grafikon_1_tonus_taborok.png")
    chart2_path = os.path.join(BASE_DIR, "kutatasi_grafikonok", "grafikon_2_kibocsatok.png")

    img1 = Image(chart1_path, width=255, height=135)
    img2 = Image(chart2_path, width=255, height=135)

    chart_table = Table([[img1, img2]], colWidths=[260, 260])
    chart_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(chart_table)

    chart_caption = Paragraph("<b>1. ábra:</b> Tónus megoszlás táboronként (balra). <b>2. ábra:</b> Kibocsátói struktúra és intézményi megoszlás (jobbra). <i>Forrás: Saját adatbázis és kutatási grafikon-generáló kód (generate_research_charts.py).</i>", table_note)
    story.append(chart_caption)
    story.append(Spacer(1, 4))

    # Detailed descriptive narrative
    p_desc_narrative = (
        "<b>Mintaelemzés és leíró megállapítások:</b><br/>"
        "1. <b>Aszimmetria a kommunikációs stratégiában:</b> A kormánypárti/CÖF tömb hirdetéseinek közel kétharmada (63.6%) nyíltan negatív, fenyegetés-alapú retorikát követ (háborús narratíva, gazdasági megszorítás réme, báb-motívum). Ezzel szemben az ellenzéki mintában kizárólag pozitív, jövőorientált vagy reményt kifejező üzenetek jelennek meg (100.0%).<br/>"
        "2. <b>Intézményi és kiadói rétegződés (2. ábra):</b> A mintában a kormánypárti narratívát három különálló kibocsátó közvetíti: a Miniszterelnöki Kabinetiroda (állami tájékoztatás kék háttérrel: 30.8%), a Fidesz pártlogós anyagai (23.1%), valamint a Civil Összefogás Fórum (CÖF-CÖKA, 23.1%). A CÖF funkciója a nyers karaktergyilkossági üzenetek kiszervezése (pl. <i>„Mint két tojás”</i> tojáshéj-montázs).<br/>"
        "3. <b>Gyűjtési rés és kontextus (Collection gap - Slide 41):</b> Az ellenzéki hirdetések alacsonyabb aránya a mintában nem a kampányintenzitás hiányát, hanem a köztéri médiavásárlási piac strukturális egyenlőtlenségeit és az ellenzéki források mikromédiába (közösségi média, kandeláber-táblák, önkéntes matricázás) történő átirányítását jelzi."
    )
    story.append(Paragraph(p_desc_narrative, body_style))

    # Page break to Page 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: MACHINE CODING, AGREEMENT, TOPIC DISCOVERY, SINKING THE HYPOTHESIS
    # =========================================================================
    story.append(Paragraph("4. Gépi kódolás és megbízhatósági validáció (/vclassify & /vcoder-agreement)", h1_style))
    p3_classify = (
        "<b>Gépi besorolás:</b> A teljes korpusz kódolását a rögzített kódkönyvvel ellátott Gemini-3.8-Flash nyelvi modell végezte el a <i>/vclassify</i> módszertan szerint. Minden egyes elemzéshez rögzítésre került az indoklás (<i>reason</i>) és a kódot alátámasztó pontos szlogen-idézet (<i>quote</i>).<br/>"
        "<b>Humán arany standard megbízhatósági teszt (Slide 27):</b> A gépi címkék megbízhatóságát vakon (blind coding) teszteltük a kutató által manuálisan kódolt arany standard (<i>hand.csv</i>) adatbázissal szemben (n = 13):<br/>"
        "• <b>Megfigyelt egyezés (Observed Agreement):</b> 100.0% (13 / 13 egyező rekord).<br/>"
        "• <b>Várható véletlen egyezés (Chance Agreement):</b> 44.38%.<br/>"
        "• <b>Cohen-féle kappa:</b> <b>κ = 1.0000</b> (tökéletes megbízhatóság, Landis & Koch, 1977 skála).<br/>"
        "• <b>Precízió, Felidézés és F1-érték:</b> 1.00 minden releváns kategóriában (<i>NEGATIV_TAMADO</i>: n=7, <i>POZITIV_EPITO</i>: n=5, <i>TEASER_SEMLEGES</i>: n=1). A konfúziós mátrix nulla besorolási hibát mutat."
    )
    story.append(Paragraph(p3_classify, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("5. Látens témák feltárása és kalibráció (/vdiscover & /vcalibrate)", h1_style))
    p3_discover = (
        "<b>Felügyelet nélküli témamodellezés (/vdiscover):</b> A korpusz szöveges tartalmát TF-IDF klaszterezéssel elemeztük. Az eljárás során feltárt három látens témát a reprezentatív dokumentumok tüzetes elolvasása alapján (Slide 32) neveztük el:<br/>"
        "1. <i>Állami szuverenitási és háborús fenyegetésdiskurzus</i> (pl. Zelenszkij, brüsszeli döntések elleni vétó, háborús részvétel veszélye).<br/>"
        "2. <i>Kormányzati korrupció és propaganda-kritika</i> (a hatalmi kommunikáció leleplezése, grassroots ellenállás).<br/>"
        "3. <i>Rendszerváltó optimizmus és jövőkép</i> (családi jólét, munkahelyek, közösségi remény, <i>„Most vagy soha”</i>).<br/>"
        "<b>Mérési hiba korrekciója (/vcalibrate - Rogan & Gladen, 1978):</b> A panelregresszió vagy aránybecslés előtt a nyers gépi prevalenciát korrigálni kell a szenzitivitás és specificitás függvényében: <i>P* = (P + Sp - 1) / (Se + Sp - 1)</i>. Mivel a validált mintában Se = 1.00 és Sp = 1.00, a korrigált negatív prevalencia megegyezik a mért értékkel (53.8%). Zajos modell esetén (pl. Se=0.85, Sp=0.80) a formula megvédi a kutatást a szisztematikus torzítástól."
    )
    story.append(Paragraph(p3_discover, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("6. Szemiotikai plakát-összehasonlítás és a hipotézis tesztelése", h1_style))
    p3_comp = (
        "<b>Vizuális és retorikai kontraszt:</b> A kormánypárti és CÖF hirdetések domináns vizuális eszköze a montázs-technika: politikai ellenfelek komor, monokróm arcképei sötétkék háttéren, agresszív felszólító tagadásokkal (<i>„NEM FIZETÜNK”</i>, <i>„Ne hagyjuk”</i>). Ezzel szemben a Tisza Párt és az ellenzéki hirdetések világos fehér-türkiz arculatot, mosolygó portrékat és partnerségi, cselekvésre hívó szlogeneket alkalmaznak (<i>„Lépésről lépésre, tégláról téglára”</i>).<br/>"
        "<b>Hipotézis értékelése:</b> Az empirikus adatok teljes mértékben alátámasztják a kiinduló hipotézist. A kormánypárti kommunikáció gerincét a külső és belső ellenségképek elleni mozgósítás képezi, míg az új ellenzéki erő a jövőre és a változásra építi köztéri megjelenését."
    )
    story.append(Paragraph(p3_comp, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("7. Reprodukálhatósági nyilatkozat és Szakirodalom (Block 4 elvárások)", h1_style))
    p3_repro = (
        "<b>Reprodukálhatóság (Slide 40 & 45):</b> A kutatás teljes forráskódja, a strukturált adatbázis (CSV, SQL, DB, JSON), a kódkönyv és a diagramgeneráló scriptek nyilvánosan elérhetők a GitHub repóban: <b>https://github.com/Blaseco/Plakat_Kutatas_2025_2026</b>. "
        "A teljes kutatási folyamat és minden számadat egyetlen parancssori utasítással ellenőrizhető: <b><code>python3 reproduce.py</code></b>.<br/>"
        "<b>Hivatkozások (APA 7th):</b><br/>"
        "• Benoit, K., Conway, D., Lauderdale, B. E., Laver, M., & Mikhaylov, S. (2016). Crowd-sourced text analysis: Reproducible and agile production of political data. <i>APSR</i>, 110(2), 278–295.<br/>"
        "• Cohen, J. (1960). A coefficient of agreement for nominal scales. <i>Educational and Psychological Measurement</i>, 20(1), 37–46.<br/>"
        "• Rogan, W. J., & Gladen, B. (1978). Estimating prevalence from the results of a screening test. <i>American Journal of Epidemiology</i>, 107(1), 71–76.<br/>"
        "• Sebők, M., Berki, B., & Szabó, F. (2021). The Hungarian Legislative Database. <i>poltextLAB Data Releases</i>."
    )
    story.append(Paragraph(p3_repro, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Sikeres PDF generálás: {PDF_PATH}")

if __name__ == '__main__':
    build_pdf()
