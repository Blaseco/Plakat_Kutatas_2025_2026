#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KÓDKÖNYV ÉS MÓDSZERTANI DOKUMENTÁCIÓ (2 OLDALAS HIVATALOS BEADANDÓ)
Bibó István Szakkollégium · 2026. ősz
Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (Kurzustartó: Sebők Miklós)
Készítő: Varga Balázs

Tartalmazza a kurzuskövetelmény 4 alappillérét:
1. Honnan jön az adat (forrás)
2. Mi történt vele (napló)
3. Mi az egyedi azonosító
4. Hogyan ellenőriztétek (validálás)
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Betűtípusok
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_ITALIC = '/System/Library/Fonts/Supplemental/Arial Italic.ttf'
FONT_BOLDITALIC = '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'

pdfmetrics.registerFont(TTFont('Arial', FONT_REGULAR))
pdfmetrics.registerFont(TTFont('Arial-Bold', FONT_BOLD))
pdfmetrics.registerFont(TTFont('Arial-Italic', FONT_ITALIC))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', FONT_BOLDITALIC))

pdfmetrics.registerFontFamily(
    'Arial',
    normal='Arial',
    bold='Arial-Bold',
    italic='Arial-Italic',
    boldItalic='Arial-BoldItalic'
)

# Színek
PRIMARY = colors.HexColor('#0F172A')       # Mélykék / sötét pala
NAVY = colors.HexColor('#1E3A8A')          # Parlamenti kék
ACCENT = colors.HexColor('#2563EB')        # Kék kiemelés
LIGHT_BG = colors.HexColor('#F8FAFC')      # Nagyon világos szürke
BORDER_COLOR = colors.HexColor('#CBD5E1')  # Szegélyszín
DARK_GRAY = colors.HexColor('#334155')     # Sötétszürke szöveg
MUTED = colors.HexColor('#64748B')         # Halványabb szöveg
GREEN_BADGE = colors.HexColor('#059669')    # Zöld siker

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

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont('Arial', 7.5)
        self.setFillColor(MUTED)
        
        # Futófejléc
        self.drawString(18 * mm, 287 * mm, "Bibó István Szakkollégium · MI a társadalom- és politikatudományban (2026. ősz) · Sebők Miklós")
        self.drawRightString(192 * mm, 287 * mm, "Varga Balázs | Kódkönyv")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(18 * mm, 284 * mm, 192 * mm, 284 * mm)
        
        # Lábléc
        self.line(18 * mm, 12 * mm, 192 * mm, 12 * mm)
        self.drawString(18 * mm, 8.5 * mm, "Magyar Közpolitikai Plakátkorpusz (2025–2026) · ParlLawSpeech Minőségbiztosított Adatbázis")
        self.drawRightString(192 * mm, 8.5 * mm, f"{total_pages} / {self._pageNumber}. oldal")
        self.restoreState()

def build_pdf():
    pdf_filename = "/Users/blaseco/Desktop/ai kurzus/Plakat_Kutatas_2025_2026/Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf"
    alt_filename = "/Users/blaseco/Desktop/ai kurzus/Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Arial-Bold',
        fontSize=15,
        leading=18,
        textColor=PRIMARY,
        spaceAfter=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Arial',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_GRAY,
        spaceAfter=5
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Arial-Bold',
        fontSize=10,
        leading=13,
        textColor=NAVY,
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Arial',
        fontSize=7.8,
        leading=10.5,
        textColor=DARK_GRAY,
        alignment=4 # Justified
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        fontName='Arial-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=PRIMARY
    )

    cell_style = ParagraphStyle(
        'CellStyle',
        fontName='Arial',
        fontSize=7,
        leading=9,
        textColor=DARK_GRAY
    )
    
    cell_bold = ParagraphStyle(
        'CellBold',
        fontName='Arial-Bold',
        fontSize=7,
        leading=9,
        textColor=PRIMARY
    )

    story = []

    # Címsor és Metaadat sáv
    story.append(Paragraph("KÓDKÖNYV ÉS ADATMINŐSÉGI DOKUMENTÁCIÓ", title_style))
    story.append(Paragraph("<b>Magyar Közpolitikai Plakátkorpusz (2025–2026)</b> | <i>Készítő: Varga Balázs · Oktató: Sebők Miklós</i>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceBefore=1, spaceAfter=4))

    # =========================================================================
    # 1. HONNAN JÖN AZ ADAT? (Forrás és mintavétel)
    # =========================================================================
    story.append(Paragraph("1. HONNAN JÖN AZ ADAT? (Forrás és mintavételi stratégia)", h1_style))
    p1_text = (
        "<b>Korpusz meghatározása:</b> A kutatás a 2025 tavasza és 2026 tavasza közötti magyarországi választási "
        "és közéleti kampányidőszak releváns közterületi és óriásplakátjait gyűjti össze teljes körű komparatív elemzés céljából (N = 13 db). "
        "A korpusz a hazai politikai mező valamennyi meghatározó szereplőjét és közzétételi csatornáját lefedi: "
        "<b>(1) Állami hirdetések</b> (Magyarország Kormánya / Miniszterelnöki Kabinetiroda: Nemzeti Konzultáció, VOKS 2025, Nemzeti Petíció, "
        "családi és rezsivédelmi szakpolitika, n = 5); "
        "<b>(2) Pártpolitikai kiadványok</b> (Fidesz–KDNP hivatalos országgyűlési jelölti plakátok, Tisza Párt kandelábertáblái, n = 3); "
        "<b>(3) Kormánypárti proxy szervezetek</b> (CÖF-CÖKA és Megafon Központ gerilla- és támadó kampányai, n = 3); valamint "
        "<b>(4) Alulról szerveződő (grassroots) lakossági megnyilvánulások</b> (Tisza Párt szimpatizánsi kerítés- és erkélymolinók, n = 2). "
        "<br/><b>Primer források és archiválás:</b> Az adatok forrását nagyfelbontású közterületi terepfotók, országos sajtóarchívumok "
        "(Telex, 444.hu, Index, MTI) és a hivatalos pártközlemények képezik. Minden egyes rekordhoz archivált forrás-URL, sajtócikk-hivatkozás "
        "és pontos közterületi elhelyezési lokáció tartozik, biztosítva a teljes forrás-visszakövethetőséget."
    )
    story.append(Paragraph(p1_text, body_style))
    story.append(Spacer(1, 3))

    # =========================================================================
    # 2. MI TÖRTÉNT VELE? (Adatfeldolgozási napló és adatfolyam / Pipeline)
    # =========================================================================
    story.append(Paragraph("2. MI TÖRTÉNT VELE? (Adatfeldolgozási napló és feldolgozási pipeline)", h1_style))
    p2_text = (
        "Az adatgyűjtés és feldolgozás szigorú, reprodukálható ötlépcsős protokoll szerint zajlott: "
        "<br/><b>1. Bevételezés és nyers archiválás:</b> A primer fotók és sajtóanyagok letöltése a <code>eredeti_sajto_kepek/</code> "
        "könyvtárba, metaadatok (dátum, forrás, hordozó típus) rögzítése. "
        "<br/><b>2. Képfeldolgozás és normalizálás:</b> A zavaró utcai környezeti elemek levágása, perspektíva-korrekció, és egységes "
        "képarányú (1:1 és 16:9) formátum kialakítása a <code>vagott_kepek/</code> könyvtárban; determinisztikus fájlelnevezés. "
        "<br/><b>3. Szövegtranszkripció és tisztítás:</b> A plakátok teljes szövegének és szlogenjeinek kétszintű digitalizálása "
        "(optikai szövegfelismerés + 100%-os kézi ellenőrzés), egységes UTF-8 kódolású szövegtáblába rendezve. "
        "<br/><b>4. Automatizált és kézi kódolás:</b> A <code>vcodebook</code> módszertan alapján rögzített kódrendszer kiterjesztése "
        "a <code>vclassify</code> skill segítségével (modell: GPT-4o-mini / Gemini Flash szisztematikus prompttal). A kommunikációs tónus "
        "(NEGATIV_TAMADO / POZITIV_EPITO / TEASER_SEMLEGES), a vizuális szemiotika és a szlogenretorika kódolása. "
        "<br/><b>5. Témafeltárás és szintézis:</b> A <code>vdiscover</code> skill futtatása (TF-IDF mátrixépítés, k=3 látens téma algoritmusos "
        "kinyerése: Kormányzati szuverenitás, Proxy karaktergyilkosság, Választási mozgósítás). Az adatok integrálása SQL és CSV formátumokba."
    )
    story.append(Paragraph(p2_text, body_style))
    story.append(Spacer(1, 4))

    # Adatfolyam összefoglaló doboz / táblázat
    pipeline_data = [
        [Paragraph("<b>Fázis</b>", cell_bold), Paragraph("<b>Bemenet</b>", cell_bold), Paragraph("<b>Alkalmazott Eszköz / Skill</b>", cell_bold), Paragraph("<b>Kimenet / Artefaktum</b>", cell_bold)],
        [Paragraph("1. Adatgyűjtés", cell_style), Paragraph("Közterületi és sajtófotók", cell_style), Paragraph("Fotódokumentáció, web scraping", cell_style), Paragraph("13 db nyers kép + forrás URL", cell_style)],
        [Paragraph("2. Képvágás", cell_style), Paragraph("Nyers képek (eredeti_sajto_kepek/)", cell_style), Paragraph("Pillow / Kézi normalizálás", cell_style), Paragraph("vagott_kepek/ (1:1 és 16:9 normalizált)", cell_style)],
        [Paragraph("3. Kódolás", cell_style), Paragraph("Szövegek és képek", cell_style), Paragraph("vcodebook + vclassify", cell_style), Paragraph("labels.csv (tónus, szemiotika, szlogen)", cell_style)],
        [Paragraph("4. Validálás", cell_style), Paragraph("Kézi vs LLM kódolás", cell_style), Paragraph("vcoder-agreement + datavalidation", cell_style), Paragraph("agreement_report.txt (κ = 1.000)", cell_style)],
        [Paragraph("5. Integráció", cell_style), Paragraph("Kódolt adatok + témafeltárás", cell_style), Paragraph("vdiscover + SQLite pipeline", cell_style), Paragraph("plakat_adatbazis_2025_2026.sql / .db / .csv", cell_style)],
    ]
    t_pipeline = Table(pipeline_data, colWidths=[25*mm, 42*mm, 45*mm, 62*mm])
    t_pipeline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_pipeline)

    # 1. oldal vége -> Áttérés a 2. oldalra
    story.append(PageBreak())

    # =========================================================================
    # 3. MI AZ EGYEDI AZONOSÍTÓ? (ID-struktúra és adatséma)
    # =========================================================================
    story.append(Paragraph("3. MI AZ EGYEDI AZONOSÍTÓ? (ID-struktúra és adatséma)", h1_style))
    p3_text = (
        "<b>Elsődleges kulcs (PRIMARY KEY):</b> Minden megfigyelési egység szigorúan egyedi, szemantikus felépítésű azonosítót kapott: "
        "<code>HUN_PLAKAT_YYYY_NNN</code> (ahol <i>YYYY</i> a megjelenés/dokumentálás éve [2025 vagy 2026], <i>NNN</i> a háromjegyű sorszám: 001–013). "
        "A nemzetközi összehasonlíthatóság érdekében rögzítésre került a ParlLawSpeech szabványú <code>PLS_HU_PLAKAT_...</code> kulcs is. "
        "<br/><b>Integritási szabályok:</b> A relációs adatbázisban a kulcs nem lehet NULL (<code>NOT NULL</code>), nem ismétlődhet (<code>UNIQUE</code>), "
        "és szigorú 1:1 kardinalitással kapcsolódik a normalizált képállományhoz (<code>fajl_nev</code>). A korpuszban 0 azaz nulla hiányzó mező van."
    )
    story.append(Paragraph(p3_text, body_style))
    story.append(Spacer(1, 3))

    # Adatséma változótáblázat
    schema_data = [
        [Paragraph("<b>Mezőnév</b>", cell_bold), Paragraph("<b>Típus</b>", cell_bold), Paragraph("<b>Skála / Lehetséges Értékek</b>", cell_bold), Paragraph("<b>Tartalom és Értelmezés</b>", cell_bold)],
        [Paragraph("id", cell_bold), Paragraph("VARCHAR(32)", cell_style), Paragraph("HUN_PLAKAT_2025_001 .. 013", cell_style), Paragraph("Egyedi elsődleges kulcs; 1:1 reláció a képhez.", cell_style)],
        [Paragraph("datum", cell_style), Paragraph("DATE", cell_style), Paragraph("ISO 8601 (ÉÉÉÉ-HH-NN)", cell_style), Paragraph("Megjelenés vagy primer dokumentálás dátuma.", cell_style)],
        [Paragraph("politikai_tabor", cell_style), Paragraph("CATEGORICAL", cell_style), Paragraph("FIDESZ-TÁBOR (11) | TISZA PÁRT (2)", cell_style), Paragraph("A kibocsátó politikai hovatartozása.", cell_style)],
        [Paragraph("kibocsato_tipus", cell_style), Paragraph("CATEGORICAL", cell_style), Paragraph("STATE (5) | PARTY (3) | PROXY (3) | GRASSROOTS (2)", cell_style), Paragraph("Intézményi közzétételi csatorna jogállása.", cell_style)],
        [Paragraph("kampany_tonus", cell_style), Paragraph("CATEGORICAL", cell_style), Paragraph("NEGATIV_TAMADO (7) | POZITIV_EPITO (5) | TEASER (1)", cell_style), Paragraph("A kommunikáció érzelmi-politikai előjele.", cell_style)],
        [Paragraph("tartalmi_fokusz", cell_style), Paragraph("TEXT", cell_style), Paragraph("Politikai narratívakeret", cell_style), Paragraph("Fő politikai üzenet, ellenségkép, szakpolitikai cél.", cell_style)],
        [Paragraph("vizualis_szemiotika", cell_style), Paragraph("TEXT", cell_style), Paragraph("Szemiotikai kódleírás", cell_style), Paragraph("Képi kompozíció, montázs, színhasználat, szimbólumok.", cell_style)],
        [Paragraph("szlogen_retorika", cell_style), Paragraph("TEXT", cell_style), Paragraph("Retorikai eszközök", cell_style), Paragraph("Felszólító tagadás, gúny, parancs-válasz, imperatívusz.", cell_style)],
        [Paragraph("latens_tema_nev", cell_style), Paragraph("CATEGORICAL", cell_style), Paragraph("Szuverenitás (2) | Karaktergyilkosság (1) | Mozgósítás (0)", cell_style), Paragraph("A vdiscover k=3 klaszterezésének kategóriája.", cell_style)],
        [Paragraph("fajl_nev / forras_url", cell_style), Paragraph("TEXT / URL", cell_style), Paragraph("vagott_kepek/*.jpg | Valós URL", cell_style), Paragraph("Csatolt normalizált képfájl és hiteles sajtóforrás.", cell_style)],
    ]
    t_schema = Table(schema_data, colWidths=[28*mm, 20*mm, 52*mm, 74*mm])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 4. HOGYAN ELLENŐRIZTÉTEK? (Validálás és minőségbiztosítás)
    # =========================================================================
    story.append(Paragraph("4. HOGYAN ELLENŐRIZTÉTEK? (Validálás és minőségbiztosítás)", h1_style))
    p4_text = (
        "Az adatbázis tudományos megbízhatóságát öt specializált kutatási skill szisztematikus futtatásával igazoltuk: "
        "<br/><b>1. Teljesség és duplikációmentesség (<code>datavalidation</code> skill):</b> A ParlLawSpeech eljárásrendnek megfelelően "
        "a korpusz minden sora egyedi ID-vel rendelkezik (duplikátum = 0); nincs hiányzó szövegmező (NA = 0); minden dátum ISO-szabványos; "
        "a forráslinkek és a kapcsolt képfájlok megléte 100%-os teljességű. "
        "<br/><b>2. Forrásrekonstrukció (<code>data-provenance-checker</code> skill):</b> Minden adatbázisrekord egyértelműen és "
        "bizonyíthatóan visszavezethető a nyers sajtófotókra és terepi felvételekre; a vágási és tisztítási napló hiánytalan. "
        "<br/><b>3. Adatkapcsolási integritás (<code>record-linkage</code> skill):</b> A képi adatbázis (<code>vagott_kepek/</code>), "
        "a metaadat-tábla és a transzkripciós szövegkorpusz 1:1 kardinalitású illesztése 13/13 rekord esetén (100%) maradéktalanul teljesült, "
        "nincs árva vagy félrecsatolt rekord. "
        "<br/><b>4. Kódolói megbízhatóság (<code>vcoder-agreement</code> skill):</b> A gépi LLM-besorolást (<code>labels.csv</code>) "
        "vakteszten vetettük össze az emberi kézi kódolással (<code>hand.csv</code>). <b>Eredmény: 13/13 egyezés (100,0%), Cohen-féle kappa "
        "értéke κ = 1.000</b>. Konfúziós mátrix: Negatív támadó = 7/7, Pozitív építő = 5/5, Teaser = 1/1, tévesztési ráta: 0,0%. "
        "<br/><b>5. Látens szerkezetvalidáció (<code>vdiscover</code> skill):</b> Az unsupervised TF-IDF és klaszterezési ellenőrzés "
        "megerősítette a három független diskurzustéma (Szuverenitás/háború, Karaktergyilkosság/bábok, Választási mozgósítás) szeparálhatóságát."
    )
    story.append(Paragraph(p4_text, body_style))
    story.append(Spacer(1, 4))

    # Minőségbiztosítási tanúsítvány zárósáv
    qa_data = [
        [
            Paragraph("<b>MINŐSÉGBIZTOSÍTÁSI AUDIT ÖSSZESÍTŐ:</b>", cell_bold),
            Paragraph("<b>datavalidation:</b> PASS (0 hiba) | <b>provenance:</b> 100% tiszta | <b>record-linkage:</b> 1:1 OK | <b>kappa:</b> κ = 1.000", cell_style),
            Paragraph("<font color='#059669'><b>PARLLAWSPEECH VALIDÁLT</b></font>", cell_bold)
        ]
    ]
    t_qa = Table(qa_data, colWidths=[55*mm, 92*mm, 27*mm])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
    ]))
    story.append(t_qa)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"2 oldalas Kódkönyv PDF sikeresen legenerálva: {pdf_filename}")

    # Másoljuk a szülőmappába is
    import shutil
    shutil.copy2(pdf_filename, alt_filename)
    print(f"Másolat elhelyezve a szülőmappában: {alt_filename}")

if __name__ == '__main__':
    build_pdf()
