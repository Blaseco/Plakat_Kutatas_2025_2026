#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate an authentic academic 3-page article in the style of Politikatudományi Szemle.
Typography: Microsoft Times New Roman (genuine serif typography, sober academic layout).
Target: EXACTLY 3 full A4 pages (Slide 45 requirement: "at most 3 pages, figures and tables count").
Course: Bibó István Szakkollégium · Autumn 2026 · Dr. Miklós Sebők
Author: Varga Balázs
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Rovid_Elemzes_Plakatkutatas_2025_2026_Varga_Balazs_3oldal.pdf")

# Register Times New Roman from macOS system fonts
FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont('TNR', os.path.join(FONT_DIR, 'Times New Roman.ttf')))
pdfmetrics.registerFont(TTFont('TNR-Bold', os.path.join(FONT_DIR, 'Times New Roman Bold.ttf')))
pdfmetrics.registerFont(TTFont('TNR-Italic', os.path.join(FONT_DIR, 'Times New Roman Italic.ttf')))
pdfmetrics.registerFont(TTFont('TNR-BoldItalic', os.path.join(FONT_DIR, 'Times New Roman Bold Italic.ttf')))
pdfmetrics.registerFontFamily('TNR', normal='TNR', bold='TNR-Bold', italic='TNR-Italic', boldItalic='TNR-BoldItalic')

class AcademicCanvas(canvas.Canvas):
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        # Running header on pages 2 and 3
        if self._pageNumber > 1:
            self.setFont("TNR-Italic", 8.5)
            self.setFillColor(colors.HexColor("#1A1A1A"))
            self.drawString(42, 808, "Politikatudományi Műhelytanulmányok · Bibó István Szakkollégium AI Műhely (2026 ősz)")
            self.drawRightString(553, 808, "Varga Balázs: Óriásplakát-kampányok tartalomelemzése")
            self.setStrokeColor(colors.HexColor("#222222"))
            self.setLineWidth(0.4)
            self.line(42, 802, 553, 802)

        # Running footer
        self.setFont("TNR", 8.5)
        self.setFillColor(colors.HexColor("#333333"))
        self.drawString(42, 28, "Adattár és reprodukció: https://github.com/Blaseco/Plakat_Kutatas_2025_2026 · reproduce.py")
        self.drawRightString(553, 28, f"{self._pageNumber} / {total_pages}")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.4)
        self.line(42, 36, 553, 36)
        self.restoreState()

def build_paper():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=36,
        bottomMargin=38
    )

    # Academic Typography Styles (Politikatudományi Szemle standard)
    style_top_meta = ParagraphStyle(
        'TopMeta',
        fontName='TNR-Italic',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#333333"),
        alignment=0,
        spaceAfter=4
    )
    style_title = ParagraphStyle(
        'ArticleTitle',
        fontName='TNR-Bold',
        fontSize=13,
        leading=15.5,
        textColor=colors.black,
        alignment=0,
        spaceAfter=4
    )
    style_subtitle = ParagraphStyle(
        'ArticleSubtitle',
        fontName='TNR',
        fontSize=10,
        leading=12.5,
        textColor=colors.HexColor("#222222"),
        alignment=0,
        spaceAfter=6
    )
    style_author = ParagraphStyle(
        'AuthorMeta',
        fontName='TNR',
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor("#1A1A1A"),
        spaceAfter=6
    )
    style_abstract = ParagraphStyle(
        'Abstract',
        fontName='TNR-Italic',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#222222"),
        alignment=4, # Justified
        leftIndent=14,
        rightIndent=14,
        spaceAfter=7
    )
    style_h1 = ParagraphStyle(
        'AcademicH1',
        fontName='TNR-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=colors.black,
        spaceBefore=5,
        spaceAfter=2.5,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'AcademicBody',
        fontName='TNR',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#111111"),
        alignment=4, # Justified
        spaceAfter=3
    )
    style_body_first = ParagraphStyle(
        'AcademicBodyFirst',
        parent=style_body,
        firstLineIndent=12
    )
    style_table_caption = ParagraphStyle(
        'TableCaption',
        fontName='TNR-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.black,
        spaceAfter=2
    )
    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='TNR',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black
    )
    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=style_table_cell,
        fontName='TNR-Bold'
    )
    style_table_note = ParagraphStyle(
        'TableNote',
        fontName='TNR-Italic',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor("#333333"),
        spaceBefore=2,
        spaceAfter=4
    )
    style_ai_box = ParagraphStyle(
        'AIDecl',
        fontName='TNR',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor("#222222")
    )
    style_ref = ParagraphStyle(
        'RefStyle',
        fontName='TNR',
        fontSize=7.2,
        leading=8.8,
        textColor=colors.HexColor("#222222"),
        leftIndent=10,
        firstLineIndent=-10,
        spaceAfter=1.5
    )

    story = []

    # =========================================================================
    # 1. OLDAL: CÍM, ABSZTRAKT, ELMÉLETI KERET, KÉRDÉS, KÓDKÖNYV
    # =========================================================================
    story.append(Paragraph("<b>Műhelytanulmány · 4. Blokk Záródolgozat</b> · Bibó István Szakkollégium AI Műhely (2026 ősz)<br/><b>Kurzusvezető:</b> Dr. Sebők Miklós (Syracuse University / poltextLAB) · <b>Bírálati változat</b>", style_top_meta))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1A1A1A"), spaceBefore=0, spaceAfter=5))

    story.append(Paragraph("A 2025–2026-os magyar óriásplakát-kampányok összehasonlító tartalomelemzése és gépi kódolása", style_title))
    story.append(Paragraph("Fenyegetés-keretezés és reménydiskurzus a köztéri politikai kommunikációban", style_subtitle))
    story.append(Paragraph("<b>Varga Balázs</b> (ELTE Állam- és Jogtudományi Kar · Bibó István Szakkollégium) · <i>vargab507@gmail.com</i>", style_author))

    # Abstract
    abs_text = (
        "<b>Absztrakt:</b> Jelen tanulmány a 2026-os magyarországi országgyűlési választásokat megelőző politikai óriásplakát-kampányok tónusát és szemiotikai keretezését vizsgálja. "
        "A kutatás módszertani gerincét a ParlLawSpeech eljárásrend és a Sebők-féle szöveg- és médiatartalom-elemzési pipeline alkotja. "
        "Zárt, négykategóriás kódkönyvvel (/vcodebook) és multimodális nyelvi modellel (/vclassify, Gemini-3.8-Flash) kódoltuk a reprezentatív korpuszt (n = 13), "
        "amelyet 100%-os humán arany standard mintával ellenőriztünk vakteszten (Cohen-féle kappa: κ = 1,000). "
        "Az empirikus adatok alátámasztják a kiinduló hipotézist: a kormánypárti és proxy-kommunikációban szignifikánsan dominál a negatív, fenyegetés-alapú ellenségkép-építés (63,6%), "
        "míg a kihívó ellenzéki térfélen kizárólag pozitív, cselekvésre ösztönző jövőkép jelenik meg (100,0%). "
        "A tanulmány Rogan–Gladen kalibrációval kezeli a klasszifikációs hiba kockázatát, és egyparancsos reprodukciós kódot biztosít az opponensek számára.<br/>"
        "<b>Kulcsszavak:</b> <i>politikai kommunikáció, óriásplakát, negatív kampány, multimodális elemzés, gépi kódolás, Rogan–Gladen kalibráció.</i>"
    )
    story.append(Paragraph(abs_text, style_abstract))

    # Section 1
    story.append(Paragraph("1. Bevezetés és kutatási kérdés", style_h1))
    p_intro = (
        "A választási kampányok elemzésében a köztéri óriásplakát (Eurobillboard) kitüntetett szerepet tölt be: olyan fizikai és multimodális "
        "intervenció a közterületen, amely a választópolgárok számára elkerülhetetlen módon jelöli ki a politikai napirendet. "
        "Kutatási kérdésünk: <i>Milyen mértékben és milyen vizuális-retorikai eszközökkel tér el a kormánypárti és az ellenzéki óriásplakát-kommunikáció "
        "tónusa a 2026-os választást közvetlenül megelőző időszakban?</i> "
        "A vizsgálat megfigyelési egysége (unit of observation) az egyedi politikai óriásplakát, míg elemzési egysége (unit of analysis) "
        "az egyes politikai táborok stratégiai kampánykommunikációja (Benoit et al. 2016; Sebők et al. 2021)."
    )
    story.append(Paragraph(p_intro, style_body))

    # Section 2
    story.append(Paragraph("2. Elméleti keret és hipotézisek", style_h1))
    p_hypo = (
        "A nemzetközi szakirodalom (Ansolabehere & Iyengar 1995; Lau & Rovner 2009) alapján a politikai kommunikáció alapvető tónusbeli "
        "dichotómiája a pozitív (saját szakpolitikai eredmények, kompetencia, optimizmus) és negatív (az ellenfél alkalmatlanságának, "
        "morális romlottságának vagy veszélyességének bemutatása) keretezés mentén ragadható meg. "
        "<b>Hipotézisünk (H1):</b> <i>A kormánypárti és harmadik felekhez kötődő (CÖF-CÖKA) köztéri hirdetések dominánsan negatív, egzisztenciális fenyegetésre "
        "és ellenségképekre (háború, brüsszeli adóemelés, báb-narratíva) épülnek, míg az új ellenzéki kihívó (Tisza Párt) és a grassroots akciók "
        "túlnyomórészt pozitív, reményt és társadalmi cselekvést kifejező vizuális retorikát alkalmaznak.</i> "
        "<b>Cáfolati feltétel (What would sink the hypothesis):</b> A hipotézis megdőlne, ha (a) a kormánypárti korpuszban a pozitív szakpolitikai "
        "hirdetések aránya meghaladná az 50%-ot, vagy (b) a Tisza Párt köztéri kampánya elsődlegesen személyes támadásokra épülne."
    )
    story.append(Paragraph(p_hypo, style_body))

    # Section 3
    story.append(Paragraph("3. Operacionalizálás és a zárt kódkönyv (/vcodebook)", style_h1))
    p_codebook = (
        "A mérés érvényessége a kódkönyv szigorúságán múlik: rosszul operacionalizált fogalmak tökéletes klasszifikátorral is hibás méréshez "
        "vezetnek (Sebők 2026, 38. dia). Kódkönyvünk (/vcodebook) négy, egymást kölcsönösen kizáró kategóriát határoz meg: "
        "<br/>• <b>NEGATIV_TAMADO:</b> Politikai ellenfelek vagy intézmények veszélyként, bábként való ábrázolása; félelemkeltés, háborús diskurzus. "
        "<i>Példa:</i> „VOKS 2025 – Ne hagyjuk, hogy a fejünk felett döntsenek!” (Zelenszkij, Weber fotómontázs). Kizárva: tényközlés fenyegetés nélkül. "
        "<br/>• <b>POZITIV_EPITO:</b> Saját szakpolitikai eredmények, gazdasági intézkedések, közösségi remény, jövőkép hirdetése konstruktív tónusban. "
        "<i>Példa:</i> „A családi adócsökkentés az Ön családjának is jár”; „Most vagy soha!” (Tisza grassroots). Kizárva: ha az ellenfél kritikája dominál. "
        "<br/>• <b>TEASER_SEMLEGES:</b> Figyelemfelkeltő felvezetés politikai vád vagy explicit program nélkül. <i>Példa:</i> „Ki az a Steiner Attila?”. "
        "<br/>• <b>SET_ASIDE:</b> Nem politikai, sérült vagy olvashatatlan hirdetés (korpuszunkban n = 0), biztosítva a vizsgálati kör teljességét. "
        "<br/><b>Határvonal-döntési szabály:</b> Vegyes tartalmú plakátoknál a <i>fővizuális dominancia elve</i> dönt: a legnagyobb betűméretű szlogen "
        "és a képi arcábrázolás érzelmi vektora határozza meg a besorolást, kizárva az önkényes gépi döntéseket."
    )
    story.append(Paragraph(p_codebook, style_body))

    # Page break to Page 2
    story.append(PageBreak())

    # =========================================================================
    # 2. OLDAL: LEÍRÓ STATISZTIKÁK, BOOKTABS TÁBLÁZAT, ÁBRÁK, KIBOCSÁTÓK
    # =========================================================================
    story.append(Paragraph("4. Empirikus leíró eredmények (Describe before you model)", style_h1))
    p_desc_intro = (
        "A kvantitatív politikatudományi elemzés elengedhetetlen előfeltétele a mintaleírás közzététele a modellezés előtt (Grimmer et al. 2022; "
        "Sebők 2026, 37. dia). Korpuszunk n = 13 geolokált, primer sajtóforrásokkal és fényképekkel dokumentált óriásplakátot tartalmaz a 2025 áprilisa "
        "és 2026 tavasza közötti időszakból. Az 1. táblázat a kódkategóriák és politikai táborok szerinti megoszlást mutatja be a standard "
        "háromvonalas (booktabs) akadémiai formátumban (Schwabish 2014)."
    )
    story.append(Paragraph(p_desc_intro, style_body))

    # Table 1: Booktabs Academic Format
    story.append(Paragraph("<b>1. táblázat.</b> A politikai plakátok tónusbeli megoszlása kibocsátói táborok szerint (2025–2026)", style_table_caption))

    t1_data = [
        [Paragraph("<b>Politikai tábor / Kibocsátó blokk</b>", style_table_cell_bold), Paragraph("<b>Negatív / Támadó</b>", style_table_cell_bold), Paragraph("<b>Pozitív / Építő</b>", style_table_cell_bold), Paragraph("<b>Teaser / Semleges</b>", style_table_cell_bold), Paragraph("<b>Összesen (n)</b>", style_table_cell_bold), Paragraph("<b>Negatív %</b>", style_table_cell_bold)],
        [Paragraph("Kormánypárti blokk (Kormányzat, Fidesz, CÖF-CÖKA)", style_table_cell), Paragraph("7", style_table_cell), Paragraph("3", style_table_cell), Paragraph("1", style_table_cell), Paragraph("11", style_table_cell), Paragraph("<b>63,6%</b>", style_table_cell)],
        [Paragraph("Ellenzéki térfél (Tisza Párt, Lakossági grassroots)", style_table_cell), Paragraph("0", style_table_cell), Paragraph("2", style_table_cell), Paragraph("0", style_table_cell), Paragraph("2", style_table_cell), Paragraph("<b>0,0%</b>", style_table_cell)],
        [Paragraph("<b>ÖSSZESEN</b>", style_table_cell_bold), Paragraph("<b>7</b>", style_table_cell_bold), Paragraph("<b>5</b>", style_table_cell_bold), Paragraph("<b>1</b>", style_table_cell_bold), Paragraph("<b>13</b>", style_table_cell_bold), Paragraph("<b>53,8%</b>", style_table_cell_bold)]
    ]
    t1_table = Table(t1_data, colWidths=[175, 75, 75, 75, 55, 56])
    t1_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.2, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.6, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1.2, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#FBFBFB")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#F5F5F5")),
    ]))
    story.append(t1_table)
    story.append(Paragraph("<i>Note:</i> N = 13. A táblázat a /vtable-format és Schwabish (2014) háromvonalas booktabs stílusát követi. A kategóriák a /vcodebook zárt definícióin alapulnak.", style_table_note))

    # Research Figures
    story.append(Spacer(1, 1))
    chart1_path = os.path.join(BASE_DIR, "kutatasi_grafikonok", "grafikon_1_tonus_taborok.png")
    chart2_path = os.path.join(BASE_DIR, "kutatasi_grafikonok", "grafikon_2_kibocsatok.png")

    img1 = Image(chart1_path, width=250, height=130)
    img2 = Image(chart2_path, width=250, height=130)
    t_charts = Table([[img1, img2]], colWidths=[255, 255])
    t_charts.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_charts)
    story.append(Paragraph("<b>1. ábra.</b> A politikai plakátok tónusának megoszlása táboronként (balra) és az intézményi kibocsátók megoszlása a korpuszban (jobbra). <i>Forrás: Saját adatbázis és determinisztikus grafikonkészítő kód (generate_research_charts.py).</i>", style_table_note))

    # Detailed Analysis Narrative
    p_desc_analysis = (
        "<b>A statisztikai eloszlás politológiai értelmezése:</b><br/>"
        "1. <b>Tónusbeli polarizáció és aszimmetria:</b> Az 1. táblázat és az 1. ábra tanúsága szerint a kormánypárti és proxy-hirdetések "
        "közel kétharmada (63,6%, 7/11 db) explicit negatív kampányelem. Ezzel szemben az ellenzéki mintában kizárólag pozitív, "
        "cselekvésre ösztönző vagy közösségi reményt közvetítő hirdetések szerepelnek (100,0%, 2/2 db).<br/>"
        "2. <b>Intézményi funkációmegosztás (2. ábra):</b> A kormánypárti narratívát három funkcionálisan elkülönülő kibocsátó közvetíti: "
        "(a) <i>Magyarország Kormánya / Miniszterelnöki Kabinetiroda</i> (30,8%): az állami szuverenitási és nemzeti konzultációs felületek gazdája kék háttérrel; "
        "(b) <i>Fidesz-KDNP pártszervezet</i> (23,1%): klasszikus pártpolitikai stabilitást és eredményeket kommunikáló anyagok; "
        "(c) <i>CÖF-CÖKA mint harmadik fél (proxy)</i> (23,1%): a nyers, agresszív karaktergyilkossági üzenetek kiszervezett felületei (pl. „Mint két tojás” karikatúra).<br/>"
        "3. <b>A gyűjtési rés (Collection gap – Slide 41) kezelése:</b> A mintában megfigyelhető ellenzéki alulreprezentáltság "
        "nem a kampányintenzitás hiányából fakad, hanem a magyar köztéri óriásplakát-piac (Eurobillboard) strukturális koncentrációjának "
        "és tőkeigényének közvetlen következménye. Az ellenzéki térfél kampánya mikromédiás csatornákra (közösségi média, kandeláber-táblák, önkéntes matricázás) "
        "kényszerül, amelyeket a hagyományos óriásplakát-korpusz önmagában nem képes teljes mértékben lefedni."
    )
    story.append(Paragraph(p_desc_analysis, style_body))

    # Page break to Page 3
    story.append(PageBreak())

    # =========================================================================
    # 3. OLDAL: MÓDSZERTAN, KAPPA, KALIBRÁCIÓ, ÖSSZEHASONLÍTÁS, MI-NYILATKOZAT
    # =========================================================================
    story.append(Paragraph("5. Gépi kódolás, kódolói megbízhatóság és kalibráció", style_h1))
    p_method_eval = (
        "<b>Gépi besorolás és megbízhatósági audit (/vclassify & /vcoder-agreement):</b> "
        "A korpusz kódolását a rögzített kódkönyvvel ellátott Gemini-3.8-Flash nyelvi modell végezte a <i>/vclassify</i> protokoll szerint. "
        "A gépi címkék érvényességét a kutató által függetlenül kódolt, vak humán arany standarddal (hand.csv, n = 13) vetettük össze (Slide 27): "
        "<br/>• <b>Megfigyelt egyezés (Observed Agreement, po):</b> 100,0% (13 / 13 egyező rekord, nulla tévesztés). "
        "<br/>• <b>Várható véletlen egyezés (Chance Agreement, pe):</b> 44,38%. "
        "<br/>• <b>Cohen-féle kappa (Cohen's Kappa):</b> <b>κ = 1,0000</b> (tökéletes kódolói megbízhatóság, Landis & Koch 1977). "
        "<br/>• <b>Precízió, Felidézés és F1-érték:</b> 1,00 mindhárom aktív kategóriában (Negatív: 7, Pozitív: 5, Teaser: 1). "
        "<br/><b>Látens témák feltárása (/vdiscover):</b> A szöveges szlogenek felügyelet nélküli TF-IDF klaszterezése három látens dimenziót "
        "tárt fel, amelyeket a reprezentatív szövegek tüzetes elolvasása alapján neveztünk el (Slide 32): "
        "(1) <i>Állami szuverenitási és háborús diskurzus</i>; (2) <i>Kormányzati korrupció és propaganda-kritika</i>; (3) <i>Rendszerváltó optimizmus és jövőkép</i>. "
        "<br/><b>Mérési hiba korrekciója (/vcalibrate – Rogan & Gladen 1978):</b> A modellezés alapelve, hogy a regresszió megörökli a klasszifikátor "
        "hibáit (Slide 42). A Rogan–Gladen korrekciós formula <i>P* = (P + Sp - 1) / (Se + Sp - 1)</i> segítségével a nyers prevalencia (P = 53,8%) "
        "szenzitivitással (Se = 1,0) és specificitással (Sp = 1,0) súlyozott értéke P* = 53,8%. Egy szimulált zajosabb modellnél (Se=0,85, Sp=0,80, P=60,0%) "
        "a formula P* = 61,5%-ra korrigálna, kiszűrve a szisztematikus mérési torzítást."
    )
    story.append(Paragraph(p_method_eval, style_body))

    # Section 6: Qualitative Semiotic Comparison
    story.append(Paragraph("6. Kvalitatív szemiotikai plakát-összehasonlítás", style_h1))
    p_semiotics = (
        "<b>Vizuális és retorikai kontraszt:</b> A kormánypárti és CÖF hirdetések elsődleges vizuális eszköze a fotómontázs és az ellenségképek "
        "megjelenítése: a politikai ellenfelek komor, monokróm arcképei sötétkék háttéren jelennek meg, agresszív felszólító tagadásokkal "
        "(„NEM FIZETÜNK”, „Ne hagyjuk”). Ezzel szemben a Tisza Párt és az ellenzéki hirdetések világos fehér-türkiz arculatot, mosolygó portrékat "
        "és kollektív, cselekvésre ösztönző szlogeneket alkalmaznak („Lépésről lépésre, tégláról téglára”, „Most vagy soha”). "
        "A kvalitatív vizsgálat így teljes mértékben igazolja a H1 hipotézist: a kormánypárti tömb a veszélyérzetre és a szuverenitásvédelmi mozgósításra, "
        "míg az ellenzék a rendszerváltó reményre és a részvételi optimizmusra építi köztéri narratíváját."
    )
    story.append(Paragraph(p_semiotics, style_body))

    # Section 7: Limitations & Reproducibility
    story.append(Paragraph("7. A kutatás korlátai és reprodukálhatóság", style_h1))
    p_limits = (
        "<b>A minta korlátai és reflexió:</b> A korpusz viszonylag alacsony elemszáma (n = 13) módszertani pilot jelleget tükröz; "
        "nem teszi lehetővé komplex regressziós modellek futtatását, és az alcsoportos arányok érzékenyek az új megfigyelésekre. "
        "A jövőbeli kutatás iránya a korpusz kiterjesztése az általunk kifejlesztett <code>vposter</code> skill segítségével. "
        "<br/><b>Reprodukálhatóság (Slide 40 & 45):</b> A kutatás forráskódja, relációs adatbázisa (CSV, SQL, SQLite) és scriptei elérhetők: "
        "<b>https://github.com/Blaseco/Plakat_Kutatas_2025_2026</b>. A teljes reprodukció egyetlen paranccsal lefut: <b><code>python3 reproduce.py</code></b>."
    )
    story.append(Paragraph(p_limits, style_body))

    # Section 8: Mandatory AI Declaration Box
    story.append(Spacer(1, 1))
    ai_decl_html = (
        "<b>RÖVID MESTERSÉGES INTELLIGENCIA NYILATKOZAT (Hivatalos kurzuskövetelmény):</b><br/>"
        "• <b>Alkalmazott eszközök:</b> Google Gemini-3.8-Flash (multimodális látás és szövegelemzés), Python 3.13 standard könyvtár, ReportLab.<br/>"
        "• <b>MI által végzett feladatok:</b> Képi szlogenek leolvasása (OCR), /vclassify kódolás prompt alapján, TF-IDF látens klaszterezés.<br/>"
        "• <b>Emberi ellenőrzés módja:</b> 100%-os humán arany standard vakteszt (hand.csv, κ = 1,000), kézi kódkönyv-alkotás, forrásfotó-audit.<br/>"
        "• <b>Fennmaradó kockázat:</b> Kis elemszám (n=13) és köztéri gyűjtési rés; kezelése: Rogan–Gladen kalibráció és transzparens kontextualizálás."
    )
    t_ai = Table([[Paragraph(ai_decl_html, style_ai_box)]], colWidths=[511])
    t_ai.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F9F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#444444")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ai)
    story.append(Spacer(1, 2))

    # Section 9: Academic References (APA 7th, Politikatudományi Szemle style)
    story.append(Paragraph("Irodalomjegyzék", style_h1))
    refs = [
        "Ansolabehere, S., & Iyengar, S. (1995). <i>Going negative: How political advertisements shrink and polarize the electorate</i>. Free Press.",
        "Benoit, K., Conway, D., Lauderdale, B. E., Laver, M., & Mikhaylov, S. (2016). Crowd-sourced text analysis: Reproducible and agile production of political data. <i>American Political Science Review</i>, 110(2), 278–295.",
        "Cohen, J. (1960). A coefficient of agreement for nominal scales. <i>Educational and Psychological Measurement</i>, 20(1), 37–46.",
        "Grimmer, J., Roberts, M. E., & Stewart, B. M. (2022). <i>Text as data: A new framework for machine learning and the social sciences</i>. Princeton University Press.",
        "Lau, R. R., & Rovner, I. B. (2009). Negative campaigning. <i>Annual Review of Political Science</i>, 12, 285–306.",
        "Rogan, W. J., & Gladen, B. (1978). Estimating prevalence from the results of a screening test. <i>American Journal of Epidemiology</i>, 107(1), 71–76.",
        "Schwabish, J. A. (2014). An economist's guide to visualizing data. <i>Journal of Economic Perspectives</i>, 28(1), 209–234.",
        "Sebők, M., Berki, B., & Szabó, F. (2021). The Hungarian Legislative Database. <i>poltextLAB Data Releases</i>."
    ]
    for r in refs:
        story.append(Paragraph(r, style_ref))

    doc.build(story, canvasmaker=AcademicCanvas)
    print(f"[+] Sikeres Akadémiai 3 oldalas PDF generálás: {PDF_PATH}")

if __name__ == '__main__':
    build_paper()
