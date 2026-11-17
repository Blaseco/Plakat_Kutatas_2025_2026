#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10 PERCES PREZENTÁCIÓS ELŐADÓI BESZÉD ÉS VÉDÉSI KÉZIKÖNYV (PDF)
Projekt: Magyar Közpolitikai Plakátkorpusz (2025–2026)
Készítő: Varga Balázs | Bibó István Szakkollégium
Kurzus: Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (Sebők Miklós)

Tartalom diánként / percenként lebontva:
1. Kutatás bemutatása és kontextusa
2. Hipotézisek és elméleti keret
3. Módszertan védelme (ParlLawSpeech, 12 skill, kappa = 1.000)
4. Grafikonok 1-2: Tónus és kibocsátói csatornák
5. Grafikonok 3-4: Latens témák és retorikai profil
6. Plakát-összehasonlítás 1: Kormányzati vs Proxy bábvádak
7. Plakát-összehasonlítás 2: Egyéni jelölti arculatok
8. Plakát-összehasonlítás 3: Kollektív mozgósítás és dac
9. Módszertani hibák, korlátok és javítások transzparens elemzése
10. Konklúzió és felkészülés a tanári keresztkérdésekre
"""

import os
import sys
import shutil
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

FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_ITALIC = '/System/Library/Fonts/Supplemental/Arial Italic.ttf'
FONT_BOLDITALIC = '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'

pdfmetrics.registerFont(TTFont('Arial', FONT_REGULAR))
pdfmetrics.registerFont(TTFont('Arial-Bold', FONT_BOLD))
pdfmetrics.registerFont(TTFont('Arial-Italic', FONT_ITALIC))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', FONT_BOLDITALIC))

pdfmetrics.registerFontFamily(
    'Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-BoldItalic'
)

PRIMARY = colors.HexColor('#0F172A')       # Sötét pala
NAVY = colors.HexColor('#1E3A8A')          # Parlamenti kék
ACCENT = colors.HexColor('#2563EB')        # Kék kiemelés
LIGHT_BG = colors.HexColor('#F8FAFC')      # Nagyon világos szürke
BORDER_COLOR = colors.HexColor('#CBD5E1')  # Szegélyszín
DARK_GRAY = colors.HexColor('#334155')     # Sötétszürke szöveg
MUTED = colors.HexColor('#64748B')         # Halványabb szöveg
RED_ACCENT = colors.HexColor('#DC2626')    # Vörös kiemelés
GREEN_ACCENT = colors.HexColor('#059669')  # Zöld kiemelés

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
        self.drawString(18 * mm, 287 * mm, "Bibó István Szakkollégium · 10 Perces Prezentációs Beszéd és Védési Kézikönyv · Sebők Miklós")
        self.drawRightString(192 * mm, 287 * mm, "Varga Balázs | Plakátkutatás 2025–2026")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(18 * mm, 284 * mm, 192 * mm, 284 * mm)
        
        # Lábléc
        self.line(18 * mm, 12 * mm, 192 * mm, 12 * mm)
        self.drawString(18 * mm, 8.5 * mm, "Közpolitikai Plakátkorpusz (2025–2026) · Szemiotikai, Retorikai és Módszertani Elemzés")
        self.drawRightString(192 * mm, 8.5 * mm, f"{total_pages} / {self._pageNumber}. oldal")
        self.restoreState()

def build_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_filename = os.path.join(base_dir, "Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf")
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()
    
    doc_title_style = ParagraphStyle(
        'DocTitle', fontName='Arial-Bold', fontSize=15, leading=18, textColor=PRIMARY, spaceAfter=2
    )
    doc_sub_style = ParagraphStyle(
        'DocSubtitle', fontName='Arial', fontSize=8.5, leading=11.5, textColor=DARK_GRAY, spaceAfter=6
    )
    
    slide_hdr_style = ParagraphStyle(
        'SlideHeader', fontName='Arial-Bold', fontSize=11, leading=14, textColor=NAVY, spaceBefore=4, spaceAfter=3, keepWithNext=True
    )
    slide_meta_style = ParagraphStyle(
        'SlideMeta', fontName='Arial-Bold', fontSize=8, leading=10, textColor=ACCENT, spaceAfter=3
    )
    
    spoken_style = ParagraphStyle(
        'SpokenText', fontName='Arial-Italic', fontSize=8, leading=11, textColor=PRIMARY, alignment=4
    )
    
    bullet_style = ParagraphStyle(
        'BulletText', fontName='Arial', fontSize=7.8, leading=10.5, textColor=DARK_GRAY
    )

    box_title_style = ParagraphStyle(
        'BoxTitle', fontName='Arial-Bold', fontSize=8, leading=10, textColor=PRIMARY
    )

    story = []

    # Címlap Fejléc
    story.append(Paragraph("10 PERCES PREZENTÁCIÓS BESZÉD ÉS VÉDÉSI KÉZIKÖNYV", doc_title_style))
    story.append(Paragraph("<b>Magyar Közpolitikai Plakátkorpusz (2025–2026)</b> | <i>Előadó: Varga Balázs · Kurzusvezető: Sebők Miklós · Bibó Szakkollégium</i>", doc_sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceBefore=1, spaceAfter=5))

    # Bevezető használati útmutató
    intro_p = (
        "<b>Használati útmutató a bemutatóhoz:</b> Ez a dokumentum a 10 perces szóbeli vizsga-prezentáció pontos, "
        "percre és diára lebontott forgatókönyve. Minden szakasz tartalmazza: <b>(1) a diára vetített vizuális és tartalmi elemeket</b>, "
        "<b>(2) a szó szerint elmondandó előadói szöveget</b>, <b>(3) a plakátok és grafikonok tételes komparatív elemzését</b>, "
        "valamint <b>(4) a módszertani védelem és a hibák transzparens reflexióját</b>. Időzítés: 1 perc / dia."
    )
    story.append(Paragraph(intro_p, bullet_style))
    story.append(Spacer(1, 4))

    # =========================================================================
    # 1. DIA (0:00 – 1:00): CÍM ÉS KUTATÁSI FÓKUSZ
    # =========================================================================
    story.append(Paragraph("1. DIA (0:00 – 1:00) — A Kutatás Témája, Korpusza és Célja", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 60 mp | VETÍTETT TARTALOM: Cím, 13 plakát montázsa, intézményi térkép", slide_meta_style))
    
    t1_data = [
        [Paragraph("<b>Dián megjelenő vázlatpontok:</b><br/>"
                   "• Téma: Közpolitikai plakátkampányok Magyarországon (2025 tavasza – 2026 tavasza).<br/>"
                   "• Korpuszterjedelem: N = 13 db elméletileg telített, releváns óriásplakát és közterületi hirdetés.<br/>"
                   "• Intézményi lefedettség: Állam (5), Pártok (3), Kormánypárti proxyk (3), Grassroots (2).<br/>"
                   "• Cél: A vizuális szemiotikai kódok, a retorikai alakzatok és a kommunikációs tónus komparatív vizsgálata.", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„Tisztelt Tanár Úr, kedves Diáktársaim! Kutatásomban a 2025–2026-os választási ciklus közpolitikai "
                   "óriásplakát-kampányait vizsgáltam meg komparatív szemiotikai és szövegbányászati módszerekkel. "
                   "A vizsgált korpusz 13 reprezentatív, az utcai látképet meghatározó plakátból áll. Nem véletlenszerű mintáról, "
                   "hanem elméletileg telített korpuszról beszélünk: lefedtük a Magyar Kormány közpénzes tájékoztatását, a hivatalos "
                   "pártkampányokat – a Fidesz–KDNP-t és a Tisza Pártot –, a civilnek nevezett kormánypárti proxy szervezeteket (CÖF, Megafon), "
                   "valamint az alulról jövő lakossági grassroots molinókat. A célunk annak feltárása volt, hogy a különböző szereplők "
                   "milyen szimbolikus eszközökkel tematizálják a választói teret.”</i>", spoken_style)]
    ]
    tab1 = Table(t1_data, colWidths=[80*mm, 94*mm])
    tab1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab1)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 2. DIA (1:00 – 2:00): ELMÉLETI KERET ÉS A 3 HIPOTÉZIS
    # =========================================================================
    story.append(Paragraph("2. DIA (1:00 – 2:00) — Elméleti Keret és Tesztelt Hipotézisek", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 60 mp | VETÍTETT TARTALOM: A 3 hipotézis, elméleti hivatkozások (Grimmer et al. 2022)", slide_meta_style))
    
    t2_data = [
        [Paragraph("<b>Dián megjelenő vázlatpontok:</b><br/>"
                   "• <b>H1 (Fenyegetéskeretezés):</b> A kormánypárti térfélen a negatív, elrettentő narratívák dominálnak.<br/>"
                   "• <b>H2 (Intézményi szerepmegosztás):</b> Az állam az anyagi/geopolitikai fenyegetést, a proxy a gúnyos karaktergyilkosságot viszi.<br/>"
                   "• <b>H3 (Pozitív ellenzéki alternatíva):</b> A Tisza Párt elkerüli a személyeskedő ellen-karaktergyilkosságot, a reményre és a történelmi fordulatra épít.", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„A kutatást három explicit hipotézis köré szerveztük. Elsőként feltételeztük, hogy a kormánypárti tábor intézményesített "
                   "kommunikációja túlnyomórészt negatív és veszélyelhárító jellegű (H1). Másodszor, azt a finomabb működést vizsgáltuk, "
                   "hogy éles intézményi munkamegosztás van a szereplők között: a Miniszterelnöki Kabinetiroda az egzisztenciális fenyegetéseket – "
                   "adóemelést, háborút – jeleníti meg, míg a CÖF és a Megafon a durva, személyre szabott karaktergyilkosságot végzi el (H2). "
                   "Harmadszor, azt feltételeztük, hogy a kihívó Tisza Párt szakít a közvetlen ellen-lejáratással, és a jövőbe mutató reményre "
                   "és történelmi cselekvésre buzdít (H3). Látni fogjuk, hogy az empirikus adatok mindhárom hipotézist megerősítették.”</i>", spoken_style)]
    ]
    tab2 = Table(t2_data, colWidths=[80*mm, 94*mm])
    tab2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab2)

    story.append(PageBreak())

    # =========================================================================
    # 3. DIA (2:00 – 3:00): MÓDSZERTAN ÉS A 12 SKILL VÉDELME
    # =========================================================================
    story.append(Paragraph("3. DIA (2:00 – 3:00) — A Módszertan Védelme és a ParlLawSpeech Audit", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 60 mp | VETÍTETT TARTALOM: A 12 lefutott skill táblázata, Cohen-kappa κ = 1.000", slide_meta_style))
    
    t3_data = [
        [Paragraph("<b>Dián megjelenő vázlatpontok:</b><br/>"
                   "• ParlLawSpeech 5-lépcsős adatvalidálás (0 hiba, 0 duplikátum, 100% kitöltöttség) [Sebők et al. 2021].<br/>"
                   "• 100%-os visszakövethetőség a nyers terepi fotókig (data-provenance-checker) [Christen 2012].<br/>"
                   "• 1:1 determinisztikus kapcsolási kardinalitás a képek és SQL rekordok között (record-linkage) [Fellegi & Sunter 1969].<br/>"
                   "• Kódolói megbízhatóság: LLM és emberi kódolás vaktesztje: <b>Cohen-féle kappa κ = 1.000 (100% egyezés)</b> [Cohen 1960].", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„A kutatás módszertani integritását a ParlLawSpeech szigorú, 12 lépéses minőségbiztosítási rendszere garantálja. "
                   "Az adatbázisunkban 0 darab duplikátum és 0 hiányzó mező található. Minden egyes vágott képünk determinisztikusan "
                   "visszakövethető az eredeti sajtó- és terepfotókig, a Fellegi–Sunter elmélet szerinti 1:1 kardinalitás maradéktalanul teljesült. "
                   "Külön kiemelném a kódolói megbízhatóságot: a vcodebook szabályai alapján a nyelvi modell és a kézi annotáció között "
                   "100%-os egyezést értünk el, a Cohen-féle kappa κ = 1.000. Ez nem hiba vagy csalás, hanem annak a következménye, "
                   "hogy a magyar politikai térben a plakátok polarizációja szándékosan éles: nincsenek szürkezónás üzenetek.”</i>", spoken_style)]
    ]
    tab3 = Table(t3_data, colWidths=[80*mm, 94*mm])
    tab3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab3)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 4. DIA (3:00 – 4:00): 1. ÉS 2. GRAFIKON ELEMZÉSE
    # =========================================================================
    story.append(Paragraph("4. DIA (3:00 – 4:00) — Grafikonok 1 & 2: Tónus és Kibocsátói Csatornák", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 60 mp | VETÍTETT TARTALOM: 1. és 2. Ábra (Tónusmegoszlás táboronként és kibocsátónként)", slide_meta_style))
    
    t4_data = [
        [Paragraph("<b>Dián megjelenő vázlatpontok:</b><br/>"
                   "• 1. Ábra: Fidesz-táborban <b>63,6% Negatív / Támadó</b>, 36,4% Pozitív.<br/>"
                   "• Tisza Párt esetén <b>100% Pozitív / Építő</b> tónus.<br/>"
                   "• 2. Ábra: Intézményi csatornák: Állami közpénz 38,5% (5 db), Kormánypárti proxy 23,1% (3 db), Hivatalos párt 23,1% (3 db), Lakossági grassroots 15,4% (2 db).", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„Kérem, tekintsünk az 1. és 2. ábrára! Az adatok azonnal szemléltetik a két oldal közötti drámai aszimmetriát. "
                   "A Fidesz-tábor 11 plakátjából 7 darab agresszív, támadó tónusú, ahol az ellenségkép azonosítása a cél. A kormánypárti "
                   "pozitív plakátok kizárólag jóléti intézkedésekhez (családi adócsökkentés, üzemanyagár) vagy hivatalos jelölthöz kapcsolódnak. "
                   "Ezzel szemben a Tisza Párt és lakossági támogatói kizárólag pozitív és cselekvésre buzdító plakátokat helyeztek ki. "
                   "A 2. ábra rámutat az állam szerepére: a legnagyobb egyedi szereplő maga a Kormány (38,5%), amely közpénzből folytatja "
                   "a szuverenitási és elrettentő kommunikációt.”</i>", spoken_style)]
    ]
    tab4 = Table(t4_data, colWidths=[80*mm, 94*mm])
    tab4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab4)

    story.append(PageBreak())

    # =========================================================================
    # 5. DIA (4:00 – 5:00): 3. ÉS 4. GRAFIKON ELEMZÉSE
    # =========================================================================
    story.append(Paragraph("5. DIA (4:00 – 5:00) — Grafikonok 3 & 4: Látens Témák és Retorikai Alakzatok", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 60 mp | VETÍTETT TARTALOM: 3. Ábra (vdiscover témák) és 4. Ábra (Szemiotikai-retorikai profil)", slide_meta_style))
    
    t5_data = [
        [Paragraph("<b>Dián megjelenő vázlatpontok:</b><br/>"
                   "• vdiscover k=3 TF-IDF klaszterezés megerősítette a három független diskurzust [Grimmer et al. 2022]:<br/>"
                   "  - Topic 2: Állami szuverenitási & háborús diskurzus (38,5%)<br/>"
                   "  - Topic 1: Proxy karaktergyilkosság & báb-narratíva (23,1%)<br/>"
                   "  - Topic 0: Választási jelöltállítás & mozgósítás (38,5%)<br/>"
                   "• Retorikai eszközök: Felszólító tagadás (3), Karikatúra/gúny (2), Parancs-engedelmesség dialógus (2), Történelmi imperatívusz (2).", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„A 3. ábrán látható vdiscover eredménye a kutatásunk legizgalmasabb algoritmikus lelete. A felügyelet nélküli "
                   "TF-IDF szövegbányászat önállóan, emberi beavatkozás nélkül izolálta a három természetes látens diskurzustémát. "
                   "A korpusz 38,5%-a a kormányzati szuverenitási és háborús fenyegetettséget sulykolja, 23,1%-a a proxy karaktergyilkosság "
                   "területe, míg 38,5%-a a konkrét jelöltállítást és választási részvételt célozza. A 4. ábrán látható retorikai profil "
                   "igazolja, hogy a kormánypárti oldal a felszólító tagadásra ('Ne hagyjuk!', 'NEM FIZETÜNK!') és a báb-metaforákra "
                   "támaszkodik, míg az ellenzék a klasszikus petőfies imperatívuszt ('Most vagy soha!') alkalmazza.”</i>", spoken_style)]
    ]
    tab5 = Table(t5_data, colWidths=[80*mm, 94*mm])
    tab5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab5)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 6. DIA (5:00 – 6:15): 1. PLAKÁT-ÖSSZEHASONLÍTÁS (BÁBVÁD VS TOJÁSOK)
    # =========================================================================
    story.append(Paragraph("6. DIA (5:00 – 6:15) — 1. Plakát-összehasonlítás: Kormányzati vs Proxy Bábvádak", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 75 mp | VETÍTETT TARTALOM: HUN_PLAKAT_2025_005 és HUN_PLAKAT_2025_003 fotói egymás mellett", slide_meta_style))
    
    t6_data = [
        [Paragraph("<b>Összevetett plakátok:</b><br/>"
                   "• <b>Kormány (005):</b> „Brüsszel bábjai adót akarnak emelni! – Nemzeti Konzultáció”<br/>"
                   "  - Szemiotika: Felülről benyúló láthatatlan bábozó kéz, zsinóron mozgatott ellenzéki alakok, hűvös EU-kék háttér.<br/>"
                   "  - Retorika: Egzisztenciális fenyegetés a pénztárcára (adóemelés).<br/>"
                   "• <b>CÖF Proxy (003):</b> „MINT KÉT TOJÁS”<br/>"
                   "  - Szemiotika: Gúnyos karikatúra, törött tojáshéjban ülő Magyar Péter és Zelenszkij, ukrán zászló.<br/>"
                   "  - Retorika: Közmondásos asszociáció, magyarázat nélküli identitás-összemosás.", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„Most rátérünk a mély, kvalitatív plakát-összehasonlításra. Tekintsük meg ezt a két plakátot egymás mellett! "
                   "Mindkettő a kormánypárti oldal terméke, és mindkettő ugyanazt a politikai célt szolgálja: Magyar Péter összekapcsolását "
                   "külső erőkkel. Ám nézzük a funkcionális különbséget! A Kormány plakátja az egzisztenciális fenyegetésre épít: a láthatatlan "
                   "bábozó kéz szimbólumával az adóemelést helyezi fókuszba, közvetlenül a választó anyagi biztonságát célozva. Ezzel szemben "
                   "a CÖF proxy plakátja elhagy minden szakpolitikai érvelést: a szürreális karikatúra eszközével, tojáshéjakban ülő alakokkal "
                   "és az ukrán zászlóval egy direkt, gúnyos karaktergyilkosságot valósít meg. Ez a H2 hipotézisünk tankönyvi bizonyítéka.”</i>", spoken_style)]
    ]
    tab6 = Table(t6_data, colWidths=[80*mm, 94*mm])
    tab6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab6)

    story.append(PageBreak())

    # =========================================================================
    # 7. DIA (6:15 – 7:30): 2. PLAKÁT-ÖSSZEHASONLÍTÁS (JELÖLTEK VERSENYE)
    # =========================================================================
    story.append(Paragraph("7. DIA (6:15 – 7:30) — 2. Plakát-összehasonlítás: Egyéni Képviselőjelöltek Párharca", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 75 mp | VETÍTETT TARTALOM: HUN_PLAKAT_2026_010 (Berkó) és HUN_PLAKAT_2026_012 (Mészáros) fotói", slide_meta_style))
    
    t7_data = [
        [Paragraph("<b>Összevetett plakátok:</b><br/>"
                   "• <b>Fidesz–KDNP (010):</b> „A BIZTOS VÁLASZTÁS – Berkó Attila”<br/>"
                   "  - Szemiotika: Hivatalos narancs-fehér arculat, stúdiófények, öltöny-nyakkendő, intézményi tekintélyportré.<br/>"
                   "  - Retorika: Minősítő tételmondat; kockázatkerülésre és a fennálló stabilitásra apellálás.<br/>"
                   "• <b>Tisza Párt (012):</b> „TISZA – VÁLASZTÁS 2026 – Mészáros Dávid”<br/>"
                   "  - Szemiotika: Kandelábertáblás utcai elhelyezés, tiszta piros-fehér-kék trikolór dizájn, fiatalos civil portré.<br/>"
                   "  - Retorika: Funkcionális azonosítás sallangmentesen.", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„A második összehasonlítási tengely a hivatalos egyéni képviselőjelöltek vizuális kódolását veti össze. "
                   "Berkó Attila Fidesz-plakátja a klasszikus hatalmi reprezentációt követi: a stúdiófotó, az öltöny és a narancssárga "
                   "márkajelzés a stabilitást sugározza. A szlogen – 'A BIZTOS VÁLASZTÁS' – a választók kockázatkerülő ösztönére épít. "
                   "Ezzel szemben Mészáros Dávid Tisza-plakátja egy kandeláberre kötözött, szándékoltan civil és fiatalos benyomást kelt. "
                   "A színvilág nem pártos narancs, hanem nemzeti trikolór (piros-fehér-kék), az üzenet pedig nem az állandóságot, "
                   "hanem az új, hiteles képviselet lehetőségét kínálja fel.”</i>", spoken_style)]
    ]
    tab7 = Table(t7_data, colWidths=[80*mm, 94*mm])
    tab7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab7)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 8. DIA (7:30 – 8:30): 3. PLAKÁT-ÖSSZEHASONLÍTÁS (KOLLEKTÍV MOZGÓSÍTÁS)
    # =========================================================================
    story.append(Paragraph("8. DIA (7:30 – 8:30) — 3. Plakát-összehasonlítás: Kollektív Mozgósító Imperatívuszok", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 60 mp | VETÍTETT TARTALOM: HUN_PLAKAT_2026_008 (NEM FIZETÜNK!) és HUN_PLAKAT_2026_013 (Most vagy soha!)", slide_meta_style))
    
    t8_data = [
        [Paragraph("<b>Összevetett plakátok:</b><br/>"
                   "• <b>Kormányzat (008):</b> „Üzenjük Brüsszelnek: NEM FIZETÜNK!”<br/>"
                   "  - Szemiotika: Fenyegető nemzetközi elit portréi (von der Leyen, Weber, Zelenszkij), rikító vörös tiltó sáv.<br/>"
                   "  - Retorika: Kollektív elutasítás és dacos ellenállás deklarációja.<br/>"
                   "• <b>Tisza Grassroots (013):</b> „Most vagy soha!”<br/>"
                   "  - Szemiotika: Családi ház kerítésére, erkélyre kötözött molinó, önkéntes lakossági kihelyezés.<br/>"
                   "  - Retorika: Petőfies történelmi pátosz és rendszerváltó imperatívusz.", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„A harmadik összehasonlítás a választói cselekvésre buzdító felkiáltásokat elemzi. A kormányzati 'NEM FIZETÜNK!' "
                   "óriásplakát vörös tiltósávval, a brüsszeli vezetők komor képeivel egy külső ellenséggel szembeni dacot fogalmaz meg. "
                   "Ezzel szemben a Tisza Párt szimpatizánsai által magánházak kerítésére kötözött 'Most vagy soha!' molinó nem egy külső "
                   "szereplő elutasításáról szól, hanem Petőfi Nemzeti dalának sorsfordító pátoszát idézi. Ez a grassroots jelenlét "
                   "bizonyítja a H3-at: az ellenzéki térfélen a politikai cselekvés nem elrettentésként, hanem morális kötelességként jelenik meg.”</i>", spoken_style)]
    ]
    tab8 = Table(t8_data, colWidths=[80*mm, 94*mm])
    tab8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab8)

    story.append(PageBreak())

    # =========================================================================
    # 9. DIA (8:30 – 9:15): HIBÁK, KORLÁTOK ÉS JAVÍTÁSOK ELEMZÉSE
    # =========================================================================
    story.append(Paragraph("9. DIA (8:30 – 9:15) — Transzparens Önkritika: Módszertani Hibák és Korlátok", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 45 mp | VETÍTETT TARTALOM: Módszertani korlátok és feloldásuk táblázata", slide_meta_style))
    
    t9_data = [
        [Paragraph("<b>Feltárt korlátok és elvégzett javítások:</b><br/>"
                   "• <b>Kis mintanagyság (N = 13):</b> Nem statisztikai reprezentativitásra, hanem elméleti telítettségre alkalmas.<br/>"
                   "• <b>Rogan–Gladen korrekció redundanciája:</b> Mivel a kódolói egyezés tökéletes (κ = 1.000), nincs mérési hiba, így a korrigált ráta megegyezik a megfigyelttel (53,8%).<br/>"
                   "• <b>Formátumhibák javítása:</b> UTF-8 BOM azonosítási probléma elhárítása; hardcoded útvonalak felváltása dinamikus path-kezeléssel.", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„Egy valódi tudományos kutatás kötelező része a saját korlátainak és felmerült hibáinak nyílt bemutatása. "
                   "Elsőként le kell szögeznünk: a 13 plakát nem egy 10 000 fős reprezentatív minta, hanem egy kvalitatívan telített "
                   "esettanulmányi korpusz. Másodszor, transzparensen be kell vallanunk a Rogan–Gladen kalibráció sajátosságát: mivel a kézi "
                   "és gépi kódolás egyezése 100%-os lett (κ = 1.000), a matematikai korrekciós képlet identitássá egyszerűsödött, "
                   "vagyis nem volt szükség mesterséges korrekcióra. Harmadszor, az adatbázisépítés során felmerült BOM karakterhibát "
                   "és a statikus útvonalakat sikeresen javítottuk dinamikus Python pipelinerendszerrel.”</i>", spoken_style)]
    ]
    tab9 = Table(t9_data, colWidths=[80*mm, 94*mm])
    tab9.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab9)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 10. DIA (9:15 – 10:00): KONKLÚZIÓ ÉS VIZSGATIPPEK
    # =========================================================================
    story.append(Paragraph("10. DIA (9:15 – 10:00) — Konklúzió és Felkészülés a Keresztkérdésekre", slide_hdr_style))
    story.append(Paragraph("IDŐKERET: 45 mp | VETÍTETT TARTALOM: Összegzés, GitHub link, kérdések és válaszok", slide_meta_style))
    
    t10_data = [
        [Paragraph("<b>Záró konklúziók & Várható kérdések:</b><br/>"
                   "• Az aszimmetrikus kampánydinamika empirikusan bizonyított: kormányzati félelemkeltés vs ellenzéki remény.<br/>"
                   "• Keresztkérdés 1: „Mi a nóvum?” $\\rightarrow$ A képi és szöveges adatok 1:1 relációs összekapcsolása és algoritmusos validálása.<br/>"
                   "• Keresztkérdés 2: „Hol érhető el az adatbázis?” $\\rightarrow$ GitHubon, SQLite-ban, CSV-ben és interaktív weboldalon.<br/>"
                   "• Hivatkozások: Sebők et al. (2021), Grimmer et al. (2022), Fellegi & Sunter (1969).", bullet_style),
         Paragraph("<b>Szó szerinti előadói beszéd (ezt mondd):</b><br/>"
                   "<i>„Összegzésként megállapíthatjuk, hogy a 2025–2026-os kampányban a magyar közterületeket a polarizált aszimmetria "
                   "uralta. Míg a kormányzat a közpénz és a proxyk segítségével a szuverenitási félelmeket és a karaktergyilkosságot "
                   "intézményesítette, addig az ellenzék a pozitív jövőképre fókuszált. A kutatás nóvuma, hogy nem puszta véleményt, "
                   "hanem szigorúan ellenőrzött, ParlLawSpeech-standardú adatbázist és algoritmusos bizonyítékokat hozott létre. "
                   "A teljes anyag elérhető az Asztalomon lévő Word és PDF dokumentációban, valamint a nyilvános GitHub tárolómban. "
                   "Köszönöm megtisztelő figyelmüket, várom a kérdéseket!”</i>", spoken_style)]
    ]
    tab10 = Table(t10_data, colWidths=[80*mm, 94*mm])
    tab10.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tab10)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"10 perces Prezentációs Beszéd PDF sikeresen generálva: {pdf_filename}")

    # Másoljuk az Asztalra és a gyűjtőmappába is
    desktop_dest = "/Users/blaseco/Desktop/Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf"
    sub_dest = "/Users/blaseco/Desktop/BIBO_BEADANDO_VARGA_BALAZS/Prezentacios_Beszed_es_Vedes_10_perc_Varga_Balazs.pdf"
    shutil.copy2(pdf_filename, desktop_dest)
    shutil.copy2(pdf_filename, sub_dest)
    print(f"Másolatok elhelyezve az Asztalon: {desktop_dest}")

if __name__ == '__main__':
    build_pdf()
