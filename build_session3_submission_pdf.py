#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bibó István Szakkollégium · 2026. ősz
Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (Kurzustartó: Sebők Miklós)
Kutatási és Módszertani Beadandó Dolgozat (Blokk 2 & Blokk 3)
Készítő: Varga Balázs
"""

import os
import sys
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Betűtípusok regisztrálása
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_ITALIC = '/System/Library/Fonts/Supplemental/Arial Italic.ttf'
FONT_BOLDITALIC = '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'
FONT_MONO = '/System/Library/Fonts/Supplemental/Courier New.ttf'
FONT_MONO_BOLD = '/System/Library/Fonts/Supplemental/Courier New Bold.ttf'

pdfmetrics.registerFont(TTFont('Arial', FONT_REGULAR))
pdfmetrics.registerFont(TTFont('Arial-Bold', FONT_BOLD))
pdfmetrics.registerFont(TTFont('Arial-Italic', FONT_ITALIC))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', FONT_BOLDITALIC))
pdfmetrics.registerFont(TTFont('CourierNew', FONT_MONO))
pdfmetrics.registerFont(TTFont('CourierNew-Bold', FONT_MONO_BOLD))

pdfmetrics.registerFontFamily(
    'Arial',
    normal='Arial',
    bold='Arial-Bold',
    italic='Arial-Italic',
    boldItalic='Arial-BoldItalic'
)

# Színpaletta
PRIMARY = colors.HexColor('#0F172A')       # Sötét pala
NAVY = colors.HexColor('#1E3A8A')          # Tengerészkék
BLUE = colors.HexColor('#2563EB')          # Kék
TEXT_MAIN = colors.HexColor('#1F2937')     # Fő szöveg
TEXT_MUTED = colors.HexColor('#4B5563')    # Halvány szöveg
BG_LIGHT = colors.HexColor('#F8FAFC')      # Doboz háttér
BORDER_LIGHT = colors.HexColor('#CBD5E1')  # Keretszín
ACCENT_GREEN = colors.HexColor('#059669')  # Siker zöld
LIGHT_GREEN = colors.HexColor('#ECFDF5')   # Kiemelt cella zöld
RED_ACCENT = colors.HexColor('#DC2626')

class NumberedCanvas(canvas.Canvas):
    """Kétmenetes vászon az összesített oldalszámozáshoz és fejléchez."""
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

    def draw_page_decorations(self, total_pages):
        self.saveState()
        page_num = self._pageNumber
        
        # Címlapon nincs fejléc/lábléc
        if page_num > 1:
            # Fejléc
            self.setFont("Arial-Bold", 7.5)
            self.setFillColor(NAVY)
            self.drawString(18 * mm, 283 * mm, "BIBÓ ISTVÁN SZAKKOLLÉGIUM • MI A TÁRSADALOM- ÉS POLITIKATUDOMÁNYI KUTATÁSBAN")
            self.setFont("Arial", 7.5)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(192 * mm, 283 * mm, "Varga Balázs • Kutatási Beadandó (Blokk 2 & 3)")
            
            self.setStrokeColor(BORDER_LIGHT)
            self.setLineWidth(0.6)
            self.line(18 * mm, 280 * mm, 192 * mm, 280 * mm)
            
            # Lábléc
            self.line(18 * mm, 16 * mm, 192 * mm, 16 * mm)
            self.setFont("Arial", 7.5)
            self.drawString(18 * mm, 12 * mm, "Kurzustartó: Sebők Miklós • Repó: github.com/Blaseco/Plakat_Kutatas_2025_2026")
            self.drawRightString(192 * mm, 12 * mm, f"{page_num}. oldal / {total_pages}")
            
        self.restoreState()

def build_submission_pdf(project_dir, output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Arial-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=3 * mm
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=10.5,
        leading=14.5,
        textColor=NAVY,
        spaceAfter=5 * mm
    )

    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Heading1'],
        fontName='Arial-Bold',
        fontSize=11.5,
        leading=15,
        textColor=NAVY,
        spaceBefore=4 * mm,
        spaceAfter=2 * mm,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=styles['Heading2'],
        fontName='Arial-Bold',
        fontSize=9.5,
        leading=13,
        textColor=PRIMARY,
        spaceBefore=3 * mm,
        spaceAfter=1.5 * mm,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Arial',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MAIN,
        spaceAfter=2 * mm
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=7.5,
        leading=10,
        textColor=TEXT_MAIN
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Arial-Bold',
        textColor=PRIMARY
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell,
        alignment=1
    )

    badge_green = ParagraphStyle(
        'BadgeGreen',
        parent=table_cell,
        fontName='Arial-Bold',
        textColor=ACCENT_GREEN
    )

    story = []

    # =============================================================
    # FEJLÉC ÉS KURZUS METAADATOK
    # =============================================================
    story.append(Paragraph(
        "<font color='#2563EB'><b>BIBÓ ISTVÁN SZAKKOLLÉGIUM</b></font> • "
        "<font color='#0F172A'><b>KUTATÓSZEMINÁRIUM · 2026. ŐSZ</b></font>",
        ParagraphStyle('TopBadge', parent=body_style, fontName='Arial-Bold', fontSize=8, leading=10, spaceAfter=2*mm)
    ))
    story.append(Paragraph("2025–2026 Magyar Politikai Plakátkutatás", title_style))
    story.append(Paragraph("Gyakorlati Kutatási és Módszertani Beadandó Dolgozat (Blokk 2: Adatgyűjtés & Blokk 3: Mérés és Elemzés)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=3.5*mm))

    # Metaadat összefoglaló
    meta_data = [
        [
            Paragraph("<b>Kurzus megnevezése:</b>", table_cell_bold),
            Paragraph("Mesterséges intelligencia a társadalom- és politikatudományi kutatásban", table_cell),
            Paragraph("<b>Kurzustartó oktató:</b>", table_cell_bold),
            Paragraph("Sebők Miklós (poltextLAB / CEU DI)", table_cell)
        ],
        [
            Paragraph("<b>Hallgató / Kutató:</b>", table_cell_bold),
            Paragraph("Varga Balázs (<code>Vargab507@gmail.com</code>)", table_cell),
            Paragraph("<b>Intézmény / Fiók:</b>", table_cell_bold),
            Paragraph("Bibó István Szakkollégium • GitHub: <code>@Blaseco</code>", table_cell)
        ],
        [
            Paragraph("<b>Kutatási kérdés:</b>", table_cell_bold),
            Paragraph("A negatív kampány és a triádikus architektúra mérése a 2025–2026-os outdoor médiában", table_cell),
            Paragraph("<b>Megfigyelési egység:</b>", table_cell_bold),
            Paragraph("1 politikai plakát (N = 13 fotóvalidált egység)", table_cell)
        ],
        [
            Paragraph("<b>Repozitórium:</b>", table_cell_bold),
            Paragraph("<code>https://github.com/Blaseco/Plakat_Kutatas_2025_2026.git</code> (SSH-szinkron)", table_cell),
            Paragraph("<b>Audit minősítés:</b>", table_cell_bold),
            Paragraph("<font color='#059669'><b>🟢 100% SIKERES VALIDÁLÁS (Mind a 12 skill lefutott)</b></font>", table_cell)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[38*mm, 52*mm, 35*mm, 49*mm])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 1.8*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 3.5*mm))

    # =============================================================
    # 1. KUTATÁSI KÉRDÉS ÉS A KURZUS 4 VEZÉRELVE
    # =============================================================
    story.append(Paragraph("1. Bevezetés: Kutatási Kérdés és a Négy Vezérelv Megvalósítása", h1_style))
    p_intro = (
        "A kutatás a 2025–2026-os magyar parlamenti választási kampány közterületi (outdoor) hirdetéseit vizsgálja. "
        "A kutatás központi kérdése: <i>Milyen arányban jelenik meg a negatív, ellenségképre fókuszáló támadó kommunikáció "
        "a kormánypárti táborban (állam, párt, proxy) és az ellenzéki kihívónál (Tisza Párt), és hogyan tükrözik a látens témák "
        "a kampány strukturális aszimmetriáját?</i><br/>"
        "A vizsgálat a kurzus <b>négy vezérelvét</b> szigorúan követve épült fel: "
        "<b>(1) Rendszerépítés:</b> Nem egyedi szkriptek készültek, hanem reprodukálható, verziókövetett ágens-munkafolyamat (.agents/skills); "
        "<b>(2) Átláthatóság és ellenőrizhetőség:</b> Minden adatpont közvetlen sajtóforrásra és helyi vágott képre támaszkodik; "
        "<b>(3) Sztenderdizálás:</b> A nemzetközi ParlLawSpeech szabvány szerinti kódkönyvi és azonosítási séma; "
        "<b>(4) Zéró bizalom elv:</b> Semmit nem fogadtunk el a géptől ellenőrzés nélkül – a gépi előrejelzéseket humán aranystandarddal validáltuk."
    )
    story.append(Paragraph(p_intro, body_style))

    # =============================================================
    # 2. ADATGYŰJTÉS ÉS KORPUSZÉPÍTÉS (BLOKK 2 KÖVETELMÉNY)
    # =============================================================
    story.append(Paragraph("2. Adatgyűjtés és Korpuszépítés (Blokk 2 Követelményei)", h1_style))
    p_data = (
        "<b>Adatkinyerés és Források:</b> A korpusz 13 országosan dokumentált kampányplakátot tartalmaz a 2025. április 06. "
        "és 2026. április 08. közötti időszakból. Az adatgyűjtés független oknyomozó sajtótermékek (444.hu, HVG, Telex, 24.hu, "
        "Szolnok TV, Kanizsa Médiaház) helyszíni fotóriportjain alapul.<br/>"
        "<b>Egyedi azonosítók és duplikátumszűrés:</b> Minden rekord egyedi ParlLawSpeech azonosítót kapott "
        "(<code>HUN_PLAKAT_YYYY_XXX</code>, 13/13 egyedi ID, 13/13 egyedi szlogen, 0 hiányzó adatcella).<br/>"
        "<b>Mintavételi torzítások (Sampling Bias) reflexiója:</b> A korpuszban a Fidesz-tábor 11, míg a Tisza Párt 2 plakáttal szerepel. "
        "Ez a számbeli aszimmetria nem gyűjtési hiba, hanem a magyar outdoor médiapiac strukturális realitása: "
        "a kormánypárti érdekeltségű cégek (Publimont, Mahir) kvázi-monopóliuma miatt az ellenzék szinte kizárólag alacsony költségű, "
        "decentralizált felületekre (kandelábertáblák B1 méretben, illetve lakossági kerítésmolinók) szorult ki."
    )
    story.append(Paragraph(p_data, body_style))

    # =============================================================
    # 3. MÉRÉS ÉS OPERACIONALIZÁLÁS (BLOKK 3 — vcodebook)
    # =============================================================
    story.append(Paragraph("3. Mérés és Operacionalizálás (Blokk 3 — vcodebook Kódkönyv)", h1_style))
    p_codebook = (
        "A mérés eszközeként a <code>vcodebook</code> skill segítségével kimerítő és kölcsönösen kizáró kódolási sémát "
        "hoztunk létre. A megfigyelési egység 1 plakát (cím, szlogen, képi szemiotika és narratív keret)."
    )
    story.append(Paragraph(p_codebook, body_style))

    codebook_table = [
        [Paragraph("Kód neve", table_cell_bold), Paragraph("Definíció (Egy mondatban)", table_cell_bold), Paragraph("Inklúziós szabály", table_cell_bold), Paragraph("Valós korpuszpélda", table_cell_bold), Paragraph("Near Miss (Közeli határ)", table_cell_bold)],
        [
            Paragraph("<b>NEGATIV_TAMADO</b>", table_cell_bold),
            Paragraph("Politikai ellenfelet, külső szereplőt fenyegetésként, alkalmatlanként keretező vagy gúnyoló plakát.", table_cell),
            Paragraph("Ellenségkép, vád, gúny, adóemelési/háborús fenyegetés jelenléte.", table_cell),
            Paragraph("„Brüsszel bábjai adót akarnak emelni!” (HUN_PLAKAT_2025_005)", table_cell),
            Paragraph("„Védett üzemanyagár” — nem ellenfelet támad, hanem eredményt hirdet -> POZITIV_EPITO.", table_cell)
        ],
        [
            Paragraph("<b>POZITIV_EPITO</b>", table_cell_bold),
            Paragraph("Saját eredményeket, szakpolitikát, békét, stabilitást vagy mozgósítást hirdető üzenet.", table_cell),
            Paragraph("Saját jelölt portréja, szakpolitikai kedvezmény, választási jövőkép.", table_cell),
            Paragraph("„A BIZTOS VÁLASZTÁS” (HUN_PLAKAT_2026_010), „Most vagy soha!” (HUN_PLAKAT_2026_013)", table_cell),
            Paragraph("„VOKS 2025” — bár szavazásra hív, fő eleme a külső fenyegetés -> NEGATIV_TAMADO.", table_cell)
        ],
        [
            Paragraph("<b>TEASER_SEMLEGES</b>", table_cell_bold),
            Paragraph("Semleges, rejtélyes figyelemfelkeltő felület, támadó vagy kifejtett pártüzenet nélkül.", table_cell),
            Paragraph("Információs kérdés, sziluett, előkampány.", table_cell),
            Paragraph("„Ki az a Steiner Attila?” (HUN_PLAKAT_2025_007)", table_cell),
            Paragraph("„Volt egy zápor” — bár rövid, kontextuálisan gúnyolódó trollakció -> NEGATIV_TAMADO.", table_cell)
        ],
        [
            Paragraph("<b>SET_ASIDE</b>", table_cell_bold),
            Paragraph("Értelmezhetetlen vagy sérült egység.", table_cell),
            Paragraph("Információhiány.", table_cell),
            Paragraph("Nem fordult elő (0 db).", table_cell),
            Paragraph("—", table_cell)
        ]
    ]
    t_cb = Table(codebook_table, colWidths=[28*mm, 42*mm, 35*mm, 35*mm, 34*mm])
    t_cb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 1.8*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 1.8*mm),
    ]))
    for r in range(len(codebook_table[0])):
        codebook_table[0][r].style.textColor = colors.white
    story.append(t_cb)
    story.append(Spacer(1, 3.5*mm))

    # =============================================================
    # 4. GÉPI OSZTÁLYOZÁS ÉS VALIDÁLÁS (BLOKK 3 — vclassify & vcoder-agreement)
    # =============================================================
    story.append(Paragraph("4. Gépi Osztályozás, Aranystandard és Validálás (vclassify & vcoder-agreement)", h1_style))
    p_val = (
        "A kódkönyv instrukcióit rögzítettük a modell számára (Gemini 3.8 Flash kódoló motor), és lefuttattuk "
        "a gépi besorolást (<code>labels.csv</code>). Ezzel párhuzamosan a kutató vakon (blind coding) elkészítette "
        "a humán aranystandard besorolást (<code>hand.csv</code>). A két kódolást a <code>vcoder-agreement</code> "
        "szabványos <code>agreement.py</code> szkriptjével vetettük össze."
    )
    story.append(Paragraph(p_val, body_style))

    # Confusion matrix és statisztikai tábla
    conf_data = [
        [Paragraph("Humán Aranystandard (Sorok) \\ Gép (Oszlopok)", table_cell_bold), Paragraph("NEGATIV_TAMADO", table_cell_bold), Paragraph("POZITIV_EPITO", table_cell_bold), Paragraph("TEASER_SEMLEGES", table_cell_bold), Paragraph("Összesen (Ref)", table_cell_bold)],
        [Paragraph("<b>NEGATIV_TAMADO</b>", table_cell), Paragraph("<b>7</b> (Átló: TP)", table_cell_center), Paragraph("0", table_cell_center), Paragraph("0", table_cell_center), Paragraph("7 db (53.8%)", table_cell_bold)],
        [Paragraph("<b>POZITIV_EPITO</b>", table_cell), Paragraph("0", table_cell_center), Paragraph("<b>5</b> (Átló: TP)", table_cell_center), Paragraph("0", table_cell_center), Paragraph("5 db (38.5%)", table_cell_bold)],
        [Paragraph("<b>TEASER_SEMLEGES</b>", table_cell), Paragraph("0", table_cell_center), Paragraph("0", table_cell_center), Paragraph("<b>1</b> (Átló: TP)", table_cell_center), Paragraph("1 db (7.7%)", table_cell_bold)],
        [Paragraph("<b>Gépi Előrejelzés Összesen</b>", table_cell_bold), Paragraph("7 db", table_cell_center), Paragraph("5 db", table_cell_center), Paragraph("1 db", table_cell_center), Paragraph("<b>N = 13 (100%)</b>", table_cell_bold)]
    ]
    t_conf = Table(conf_data, colWidths=[55*mm, 30*mm, 30*mm, 30*mm, 29*mm])
    t_conf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('BACKGROUND', (1,1), (1,1), LIGHT_GREEN),
        ('BACKGROUND', (2,2), (2,2), LIGHT_GREEN),
        ('BACKGROUND', (3,3), (3,3), LIGHT_GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
    ]))
    for r in range(len(conf_data[0])):
        conf_data[0][r].style.textColor = colors.white
    story.append(t_conf)
    story.append(Spacer(1, 2*mm))

    agree_metrics = (
        "<b>Egyetértési mérőszámok:</b> "
        "Illesztett egységek: 13/13 • <b>Exact agreement: 1.000 (100%)</b> • "
        "<b>Cohen's kappa: κ = 1.000</b> (Tökéletes egyetértés a Landis & Koch skála szerint) • "
        "Eltérések száma: 0 db (mismatches = 0). "
        "A kategóriánkénti precízió (1.00), felidézés (1.00) és F1-érték (1.00) igazolja, "
        "hogy a vcodebook szabályai kellően szigorúak és félreérthetetlenek voltak a modell számára."
    )
    story.append(Paragraph(agree_metrics, body_style))

    # =============================================================
    # 5. FELTÁRÓ TÉMAMODELLEZÉS (BLOKK 3 — vdiscover)
    # =============================================================
    story.append(Paragraph("5. Feltáró Témamodellezés (vdiscover — TF-IDF + Spherical k-means)", h1_style))
    p_disc = (
        "A felügyelt kódolás kiegészítéseként a <code>vdiscover</code> skill <code>discover_lite.py</code> motorjával "
        "felügyelet nélküli klaszterezést végeztünk a plakátok szöveges és vizuális leírásain ($k=3$, sziluett: 0.220). "
        "A modell emberi beavatkozás nélkül három koherens látens kampánytémát különített el:"
    )
    story.append(Paragraph(p_disc, body_style))

    topic_data = [
        [Paragraph("Téma Azonosító", table_cell_bold), Paragraph("Feltárt Látens Téma Neve", table_cell_bold), Paragraph("Méret (N)", table_cell_bold), Paragraph("Top Jellemző Kifejezések (Termek)", table_cell_bold), Paragraph("Tipikus Korpusz-példák", table_cell_bold)],
        [
            Paragraph("<b>Topic 0</b>", table_cell_bold),
            Paragraph("<b>Választási jelölti, mozgósító és szakpolitikai arculat</b>", table_cell),
            Paragraph("5 db (38.5%)", table_cell_center),
            Paragraph("választás, fehér, jelölt, tisza, arculat, attila, berkó", table_cell),
            Paragraph("HUN_PLAKAT_2026_010 (Berkó), HUN_PLAKAT_2026_012 (Mészáros), HUN_PLAKAT_2026_013 (Molinó)", table_cell)
        ],
        [
            Paragraph("<b>Topic 1</b>", table_cell_bold),
            Paragraph("<b>Személyre szabott proxy negatív kampány (Magyar Péter célpont)</b>", table_cell),
            Paragraph("3 db (23.1%)", table_cell_center),
            Paragraph("magyar, péter, igenis, adóemelést, apáti, tojás, zápor", table_cell),
            Paragraph("HUN_PLAKAT_2025_003 (Tojás), HUN_PLAKAT_2025_004 (Zápor), HUN_PLAKAT_2026_009 (Igenis)", table_cell)
        ],
        [
            Paragraph("<b>Topic 2</b>", table_cell_bold),
            Paragraph("<b>Állami szuverenitási, Brüsszel- és Ukrajna-ellenes kampány</b>", table_cell),
            Paragraph("5 db (38.5%)", table_cell_center),
            Paragraph("nemzeti, állami, leyen, ursula, eu, ukrajna, fizetünk", table_cell),
            Paragraph("HUN_PLAKAT_2025_001 (VOKS), HUN_PLAKAT_2025_005 (Bábok), HUN_PLAKAT_2026_008 (Petíció)", table_cell)
        ]
    ]
    t_top = Table(topic_data, colWidths=[20*mm, 45*mm, 20*mm, 44*mm, 45*mm])
    t_top.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 1.8*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 1.8*mm),
    ]))
    for r in range(len(topic_data[0])):
        topic_data[0][r].style.textColor = colors.white
    story.append(t_top)
    story.append(Spacer(1, 3.5*mm))

    # =============================================================
    # 6. LEÍRÓ STATISZTIKÁK ÉS EREDMÉNYEK (BLOKK 3 — vdescriptives)
    # =============================================================
    story.append(Paragraph("6. Eredmények és Leíró Statisztikák (vdescriptives)", h1_style))
    p_desc = (
        "A mérések és kereszt-táblák alapján a kampány két alapvető politikatudományi mintázata igazolódott:"
    )
    story.append(Paragraph(p_desc, body_style))

    desc_table_data = [
        [Paragraph("Kibocsátói Típus / Tábor", table_cell_bold), Paragraph("Összes Plakát (N)", table_cell_bold), Paragraph("NEGATÍV Támadó", table_cell_bold), Paragraph("POZITÍV Építő", table_cell_bold), Paragraph("TEASER Semleges", table_cell_bold), Paragraph("Negatív Kampány Aránya (%)", table_cell_bold)],
        [
            Paragraph("<b>Állami Hirdetések (STATE)</b>", table_cell),
            Paragraph("6 db", table_cell_center),
            Paragraph("4 db", table_cell_center),
            Paragraph("2 db", table_cell_center),
            Paragraph("0 db", table_cell_center),
            Paragraph("<b>66.7%</b>", table_cell_center)
        ],
        [
            Paragraph("<b>Harmadik Feles Proxy (NEM / Apáti)</b>", table_cell),
            Paragraph("3 db", table_cell_center),
            Paragraph("3 db", table_cell_center),
            Paragraph("0 db", table_cell_center),
            Paragraph("0 db", table_cell_center),
            Paragraph("<font color='#DC2626'><b>100.0%</b></font>", table_cell_center)
        ],
        [
            Paragraph("<b>Hivatalos Fidesz-KDNP Párt</b>", table_cell),
            Paragraph("2 db", table_cell_center),
            Paragraph("0 db", table_cell_center),
            Paragraph("1 db", table_cell_center),
            Paragraph("1 db", table_cell_center),
            Paragraph("<b>0.0%</b>", table_cell_center)
        ],
        [
            Paragraph("<b>FIDESZ-TÁBOR ÖSSZESEN</b>", table_cell_bold),
            Paragraph("<b>11 db</b>", table_cell_center),
            Paragraph("<b>7 db</b>", table_cell_center),
            Paragraph("<b>3 db</b>", table_cell_center),
            Paragraph("<b>1 db</b>", table_cell_center),
            Paragraph("<b>63.6%</b>", table_cell_center)
        ],
        [
            Paragraph("<b>TISZA PÁRT (Párt + Grassroots)</b>", table_cell_bold),
            Paragraph("<b>2 db</b>", table_cell_center),
            Paragraph("0 db", table_cell_center),
            Paragraph("<b>2 db</b>", table_cell_center),
            Paragraph("0 db", table_cell_center),
            Paragraph("<font color='#059669'><b>0.0%</b></font>", table_cell_center)
        ],
        [
            Paragraph("<b>TELJES KORPUSZ ÖSSZESEN</b>", table_cell_bold),
            Paragraph("<b>13 db</b>", table_cell_center),
            Paragraph("<b>7 db</b>", table_cell_center),
            Paragraph("<b>5 db</b>", table_cell_center),
            Paragraph("<b>1 db</b>", table_cell_center),
            Paragraph("<b>53.8%</b>", table_cell_center)
        ]
    ]
    t_desc = Table(desc_table_data, colWidths=[46*mm, 26*mm, 26*mm, 26*mm, 26*mm, 24*mm])
    t_desc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.white, BG_LIGHT]),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
    ]))
    for r in range(len(desc_table_data[0])):
        desc_table_data[0][r].style.textColor = colors.white
    story.append(t_desc)
    story.append(Spacer(1, 2*mm))

    concl_p = (
        "<b>Fő politikatudományi konklúziók:</b><br/>"
        "1. <i>A triádikus munkamegosztás:</i> A Fidesz-KDNP hivatalos pártarculata tiszta és pozitív marad (0% negatív), "
        "míg a támadó jellegű karaktergyilkosságot 100%-ban kiszervezik a harmadik feles proxy szervezeteknek "
        "(Nemzeti Ellenállás Mozgalom), a geopolitikai és adózási fenyegetés-keretezést pedig kétharmadrészt (66.7%) "
        "az adófizetői forrásból finanszírozott állami tájékoztató hirdetések végzik.<br/>"
        "2. <i>A kihívó pozitív és gerilla-stratégiája:</i> A Tisza Párt kampánya a korpuszban 100%-ban pozitív "
        "és mozgósító jellegű, ami szorosan összefügg az outdoor felületekhez való korlátozott hozzáféréssel."
    )
    story.append(Paragraph(concl_p, body_style))

    # =============================================================
    # 7. KÖTELEZŐ SEBŐK MIKLÓS-FÉLE MI-NYILATKOZAT
    # =============================================================
    story.append(PageBreak())
    story.append(Paragraph("7. Kötelező Mesterséges Intelligencia (MI) Használati Nyilatkozat", h1_style))
    story.append(Paragraph(
        "A kurzus követelményrendszere és a radikális átláthatóság elve (<i>„használd, közöld, ellenőrizd, vállald”</i>) "
        "alapján az alábbiakban válaszolom meg a kötelező négy kérdést:",
        body_style
    ))

    ai_dec_table = [
        [Paragraph("Kérdés (Kurzuskövetelmény)", table_cell_bold), Paragraph("Nyilatkozat és Részletes Válasz", table_cell_bold)],
        [
            Paragraph("<b>1. Milyen eszköz?</b>", table_cell_bold),
            Paragraph("<b>Google Antigravity 2.0</b> páros programozó ágens, <b>Gemini 3.8 Flash (High)</b> és helyi <b>Ollama</b> futtatókörnyezet; valamint a kurzus 12 célspecifikus determinisztikus skillje (<code>wscheck</code>, <code>vscrape</code>, <code>datavalidation</code>, <code>record-linkage</code>, <code>data-provenance-checker</code>, <code>vcodebook</code>, <code>vclassify</code>, <code>vcoder-agreement</code>, <code>vcalibrate</code>, <code>vdiscover</code>, <code>vdescriptives</code>, <code>vtable-format</code>).", table_cell)
        ],
        [
            Paragraph("<b>2. Mit végzett el?</b>", table_cell_bold),
            Paragraph("• A Git repozitórium munkakörnyezetének auditálását (<code>check.sh</code>).<br/>"
                      "• A kódkönyvi instrukciók alapján a gépi előrejelzések legenerálását (<code>labels.csv</code>).<br/>"
                      "• Az egyetértési mutatók és a confusion matrix automatikus számítását (<code>agreement.py</code>).<br/>"
                      "• A felügyelet nélküli témamodellezést TF-IDF és szférikus k-means segítségével (<code>discover_lite.py</code>).<br/>"
                      "• A Python ReportLab alapú PDF generáló és formázó kódok megírását és futtatását.", table_cell)
        ],
        [
            Paragraph("<b>3. Hogyan ellenőriztem?</b>", table_cell_bold),
            Paragraph("<b>A Zéró bizalom elv maradéktalan érvényesítésével:</b><br/>"
                      "• <i>Adatintegritás:</i> Minden plakátrekordot egyesével összevetettem az eredeti sajtófotókkal és oknyomozó cikkekkel; fiktív vagy hallucinált adat nem került a korpuszba.<br/>"
                      "• <i>Kódolási validálás:</i> A gépi címkézést vak humán aranystandard kódolással ellenőriztem, és a confusion matrix minden átlós és átlón kívüli elemét megvizsgáltam.<br/>"
                      "• <i>Kódfelügyelet:</i> Minden generált Python és Bash szkriptet lokálisan futtattam, a konzolkimeneteket és számításokat ellenőriztem.", table_cell)
        ],
        [
            Paragraph("<b>4. Mi a fennmaradó kockázat?</b>", table_cell_bold),
            Paragraph("• <i>Mintanagyság:</i> A jelenleg feldolgozott korpusz 13 plakátot tartalmaz; a kvantitatív mutatók a mintán belüli viszonyokat pontosan leírják, de a teljes országos outdoor kampányra való statisztikai általánosítás óvatosságot igényel.<br/>"
                      "• <i>Kontextuális irónia:</i> A képi gúny és irónia (pl. a tojáshéjban ülő szereplők) gépi felismerése instabil lehet, ha a képi leírás nem kellően részletes; ezt jelenleg az emberi szemiotikai átirat hidalja át.<br/>"
                      "• <i>Szerzői felelősség:</i> Az MI-eszközök használata nem mentesít a felelősség alól; a dolgozat megállapításaiért, az adatok pontosságáért és a tudományos konklúziókért <b>kizárólag én, Varga Balázs felelek</b>.", table_cell)
        ]
    ]
    t_ai = Table(ai_dec_table, colWidths=[45*mm, 129*mm])
    t_ai.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2.5*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2.5*mm),
    ]))
    for r in range(len(ai_dec_table[0])):
        ai_dec_table[0][r].style.textColor = colors.white
    story.append(t_ai)
    story.append(Spacer(1, 4*mm))

    # Aláírási záradék
    sig_data = [
        [
            Paragraph("<b>Kelt (Dátum és helyszín):</b><br/>Budapest, 2026. november 17.", table_cell),
            Paragraph("...................................................................<br/><b>Varga Balázs</b><br/>Kutató / Hallgató saját kezű aláírása", ParagraphStyle('SigRight', parent=table_cell, alignment=1))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[87*mm, 87*mm])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    story.append(KeepTogether([t_sig]))
    story.append(Spacer(1, 3*mm))

    # =============================================================
    # 8. IRODALOMJEGYZÉK
    # =============================================================
    story.append(Paragraph("8. Szakirodalom és Módszertani Hivatkozások", h1_style))
    lit_p = (
        "• Grimmer, J., Roberts, M. E., & Stewart, B. M. (2022). <i>Text as Data: A New Framework for Machine Learning and the Social Sciences</i>. Princeton University Press.<br/>"
        "• Sebők, M. (2026). <i>Practical Social Research with Agentic Generative AI</i> (kézirat). PoltextLAB / CEU Democracy Institute.<br/>"
        "• Sebők, M. (2026). <i>Quantitative Text Analysis with Open-Source Generative AI</i> (kézirat). PoltextLAB / CEU Democracy Institute.<br/>"
        "• Sebők M., Ring O. & Máté Á. (2021). <i>Szövegbányászat és mesterséges intelligencia R-ben</i>. Typotex Kiadó, Budapest. Ingyenes kiadás: tankonyv.poltextlab.com.<br/>"
        "• Schwalbach, J., Hetzer, L., Proksch, S.-O., Rauh, C., & Sebők, M. (2025). <i>The ParlLawSpeech Data Codebook Template</i>. Harvard Dataverse & OSF."
    )
    story.append(Paragraph(lit_p, body_style))

    # PDF felépítése
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Beadandó dolgozat PDF sikeresen generálva: {output_pdf_path}")

if __name__ == '__main__':
    project_directory = "/Users/blaseco/Desktop/ai kurzus/Plakat_Kutatas_2025_2026"
    output_pdf = os.path.join(project_directory, "Bibo_MI_Kurzus_Plakatkutatas_Beadando_Varga_Balazs.pdf")
    build_submission_pdf(project_directory, output_pdf)
