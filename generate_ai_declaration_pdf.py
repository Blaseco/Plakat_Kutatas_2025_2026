#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mesterséges Intelligencia (AI) Felhasználási Nyilatkozat Generáló Szkript
Projekt: 2025–2026 Magyar Politikai Plakátkutató Korpusz (ParlLawSpeech Outdoor Standard)
Kutató: Varga Balázs
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
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
PRIMARY = colors.HexColor('#0F172A')       # Sötét pala
NAVY = colors.HexColor('#1E3A8A')          # Tengerészkék
BLUE = colors.HexColor('#2563EB')          # Kék
TEXT_MAIN = colors.HexColor('#1F2937')     # Fő szövegszín
TEXT_MUTED = colors.HexColor('#4B5563')    # Halvány szöveg
BG_LIGHT = colors.HexColor('#F8FAFC')      # Doboz háttér
BORDER_LIGHT = colors.HexColor('#CBD5E1')  # Keretszín
ACCENT_GREEN = colors.HexColor('#059669')

class DeclarationCanvas(canvas.Canvas):
    """Fejlécet és láblécet rajzoló vászon."""
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
        
        # Felső díszítőcsík
        self.setFillColor(NAVY)
        self.rect(18 * mm, 283 * mm, 174 * mm, 1.5 * mm, fill=1, stroke=0)
        
        self.setFont("Arial-Bold", 7.5)
        self.setFillColor(NAVY)
        self.drawString(18 * mm, 280 * mm, "TUDOMÁNYOS ÉS KUTATÁSETIKAI MEGFELELŐSÉGI NYILATKOZAT")
        self.setFont("Arial", 7.5)
        self.setFillColor(TEXT_MUTED)
        self.drawRightString(192 * mm, 280 * mm, "ParlLawSpeech Outdoor Research Standard")
        
        # Alsó vonal és lábléc
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.6)
        self.line(18 * mm, 16 * mm, 192 * mm, 16 * mm)
        self.setFont("Arial", 7.5)
        self.drawString(18 * mm, 12 * mm, "Varga Balázs • 2025–2026 Magyar Politikai Plakátkutató Korpusz")
        self.drawRightString(192 * mm, 12 * mm, f"{page_num}. oldal / {total_pages}")
        
        self.restoreState()

def create_ai_declaration_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Arial-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceAfter=2 * mm,
        alignment=1 # Középre igazított
    )

    doc_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=10,
        leading=14,
        textColor=NAVY,
        spaceAfter=5 * mm,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Heading1'],
        fontName='Arial-Bold',
        fontSize=10.5,
        leading=14,
        textColor=NAVY,
        spaceBefore=3.5 * mm,
        spaceAfter=2 * mm,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Arial',
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_MAIN,
        spaceAfter=2.5 * mm
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=8,
        leading=11,
        textColor=TEXT_MAIN
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Arial-Bold',
        textColor=PRIMARY
    )

    story = []

    # Cím és fejléc
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("MESTERSÉGES INTELLIGENCIA (AI) FELHASZNÁLÁSI NYILATKOZAT", doc_title))
    story.append(Paragraph("Declaration of Generative AI Tool Usage in Research & Data Engineering", doc_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=4*mm))

    # Kutatói és projektazonosító táblázat
    meta_data = [
        [
            Paragraph("<b>Kutató / Hallgató neve:</b>", table_cell_bold),
            Paragraph("Varga Balázs", table_cell),
            Paragraph("<b>E-mail cím:</b>", table_cell_bold),
            Paragraph("<code>Vargab507@gmail.com</code>", table_cell)
        ],
        [
            Paragraph("<b>GitHub azonosító:</b>", table_cell_bold),
            Paragraph("<code>@Blaseco</code>", table_cell),
            Paragraph("<b>Kutatási projekt:</b>", table_cell_bold),
            Paragraph("2025–2026 Magyar Politikai Plakátkutató Korpusz", table_cell)
        ],
        [
            Paragraph("<b>Intézményi háttér:</b>", table_cell_bold),
            Paragraph("2. blokk: Munkakörnyezet és adatgyűjtés (Bibó módszertan)", table_cell),
            Paragraph("<b>Repozitórium:</b>", table_cell_bold),
            Paragraph("<code>github.com/Blaseco/Plakat_Kutatas_2025_2026</code>", table_cell)
        ],
        [
            Paragraph("<b>Dátum / Időpont:</b>", table_cell_bold),
            Paragraph("2026. november 04.", table_cell),
            Paragraph("<b>Módszertani szabvány:</b>", table_cell_bold),
            Paragraph("ParlLawSpeech Outdoor Standard (2025)", table_cell)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[38*mm, 52*mm, 35*mm, 49*mm])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2.5*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2.5*mm),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4*mm))

    # 1. Bevezető nyilatkozat
    story.append(Paragraph("1. Általános Nyilatkozat és Módszertani Elkötelezettség", h1_style))
    p1 = (
        "Alulírott <b>Varga Balázs</b> büntetőjogi és tudományetikai felelősségem tudatában kijelentem, hogy "
        "a <i>2025–2026 Magyar Politikai Plakátkutató Korpusz</i> adatkészletének felépítése, minőségbiztosítása, "
        "kódkönyvének megírása és kapcsolódó platformjainak kialakítása során mesterséges intelligencia (Generative AI) "
        "és autonóm kódoló ágens (Agentic AI) technológiákat vettem igénybe, az alábbiakban részletezett módon és mértékben."
    )
    story.append(Paragraph(p1, body_style))

    # 2. Felhasznált eszközök leltára
    story.append(Paragraph("2. Az Igénybe Vett AI Rendszerek és Céleszközök Leltára", h1_style))
    ai_tools_data = [
        [Paragraph("AI Eszköz / Rendszer", table_cell_bold), Paragraph("Verzió / Modell", table_cell_bold), Paragraph("Funkció a Projektben", table_cell_bold), Paragraph("Felhasználás Módja", table_cell_bold)],
        [
            Paragraph("<b>Google Antigravity</b>", table_cell),
            Paragraph("Antigravity 2.0 / Gemini 3.8 Flash (High)", table_cell),
            Paragraph("Páros programozó és kutatási ágens (Agentic Pair Programmer)", table_cell),
            Paragraph("Git repó inicializálása, SSH konfigurálás, Python feldolgozó és PDF generáló kódok írása, webes interfész fejlesztés.", table_cell)
        ],
        [
            Paragraph("<b>Bibó Validációs Skillek</b>", table_cell),
            Paragraph("wscheck, datavalidation, record-linkage, provenance, vscrape", table_cell),
            Paragraph("Determinisztikus ágens-vezérelt ellenőrző protokollok", table_cell),
            Paragraph("A munkakörnyezet auditálása, 5-lépcsős adatintegritás-ellenőrzés, relációk és forrásvisszavezethetőség igazolása.", table_cell)
        ],
        [
            Paragraph("<b>Helyi AI Motor</b>", table_cell),
            Paragraph("Ollama v0.5+ (Helyi nyelvi modell környezet)", table_cell),
            Paragraph("Offline adatelemzési és szűrési felkészültség", table_cell),
            Paragraph("Adatvédelmi szempontból érzékeny helyi tokenizáció és háttér-infrastruktúra biztosítása.", table_cell)
        ]
    ]
    t_tools = Table(ai_tools_data, colWidths=[38*mm, 35*mm, 45*mm, 56*mm])
    t_tools.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 1.8*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    for r in range(len(ai_tools_data[0])):
        ai_tools_data[0][r].style.textColor = colors.white
    story.append(t_tools)
    story.append(Spacer(1, 3.5*mm))

    # 3. Miben segített az AI és miben NEM?
    story.append(Paragraph("3. Az Emberi és Gépi Munka Szerepmegosztása (Human-in-the-Loop)", h1_style))
    p3 = (
        "A projekt során szigorúan érvényesült az <b>ember a hurokban (Human-in-the-Loop)</b> elv. "
        "A mesterséges intelligencia nem helyettesítette a kutatói döntéshozatalt, hanem asszisztensként támogatta a repetitív technikai munkát:"
    )
    story.append(Paragraph(p3, body_style))

    roles_data = [
        [Paragraph("Munkafázis", table_cell_bold), Paragraph("AI Ágens Szerepe (Mi történt géppel?)", table_cell_bold), Paragraph("Kutatói Felügyelet (Mi történt emberi kézzel?)", table_cell_bold)],
        [
            Paragraph("<b>Kutatási kérdés és fókusz</b>", table_cell),
            Paragraph("Nem vett részt a hipotézisek és fókusz kiválasztásában.", table_cell),
            Paragraph("A kutató határozta meg a 2025–2026-os időszakot és a kampányidőszaki outdoor médiateret mint vizsgálati tárgyat.", table_cell)
        ],
        [
            Paragraph("<b>Adatgyűjtés és forrásolás</b>", table_cell),
            Paragraph("Sajtófotók ellenőrzése, metaadat-összerendelés szkriptekkel.", table_cell),
            Paragraph("A forráscikkek (444, HVG, Telex, 24.hu) és a valós közterületi plakátok kiválasztását a kutató validálta.", table_cell)
        ],
        [
            Paragraph("<b>Kódolás és diskurzuselemzés</b>", table_cell),
            Paragraph("Szöveghossz-statisztikák, táblázatba rendezés, formázás.", table_cell),
            Paragraph("A politikai táborok (Fidesz, Tisza) és a triádikus kibocsátói típusok (State, Proxy, Party) kategorizálását a kutató ellenőrizte és hagyta jóvá.", table_cell)
        ],
        [
            Paragraph("<b>Szoftver- és adatbázisfejlesztés</b>", table_cell),
            Paragraph("SQL sémaírás, ReportLab PDF generáló kódok és HTML platformok kódolása.", table_cell),
            Paragraph("A generált kódok tesztelése, futtatása, a Git környezet felállítása és az SSH hitelesítés elvégzése a kutató által.", table_cell)
        ]
    ]
    t_roles = Table(roles_data, colWidths=[38*mm, 68*mm, 68*mm])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 1.8*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    for r in range(len(roles_data[0])):
        roles_data[0][r].style.textColor = colors.white
    story.append(t_roles)
    story.append(Spacer(1, 3.5*mm))

    # 4. Adathitelesség és etikai nyilatkozatok
    story.append(Paragraph("4. Adathitelességi és Etikai Garanciák", h1_style))
    p4 = (
        "<b>1. Hallucinációmentesség és valósághűség:</b> Kijelentem, hogy az adatbázisban szereplő 13 plakátrekord "
        "egyike sem mesterséges intelligencia által generált fiktív adat vagy kép. Minden rekordhoz fizikailag létező, "
        "valós sajtóforrásból archivált eredeti és vágott képfájl tartozik a <code>vagott_kepek/</code> mappában.<br/>"
        "<b>2. Adatbiztonság és adatvédelem:</b> Az AI-munkamenetek során nem kerültek megosztásra személyes adatok, "
        "jelszavak, tokenek vagy védett szellemi tulajdont képező bizalmas anyagok. A hitelesítést (SSH) a kutató lokálisan végezte.<br/>"
        "<b>3. Szerzői és tudományos felelősségvállalás:</b> Elismerem és kijelentem, hogy az AI eszközök használata nem mentesít "
        "a személyes kutatói felelősség alól. A beadott tanulmány, adatkészlet és kódkönyv tartalmáért, pontosságáért és "
        "tudományos integritásáért <b>kizárólag én, mint szerző felelek</b>."
    )
    story.append(Paragraph(p4, body_style))
    story.append(Spacer(1, 5 * mm))

    # Aláírási záradék
    sig_data = [
        [
            Paragraph("<b>Kelt (Dátum és helyszín):</b><br/>Budapest, 2026. november 04.", table_cell),
            Paragraph("...................................................................<br/><b>Varga Balázs</b><br/>Kutató / Hallgató saját kezű aláírása", ParagraphStyle('SigRight', parent=table_cell, alignment=1))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[87*mm, 87*mm])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
    ]))
    story.append(KeepTogether([t_sig]))

    doc.build(story, canvasmaker=DeclarationCanvas)
    print(f"[OK] AI Nyilatkozat PDF sikeresen generálva: {output_pdf_path}")

if __name__ == '__main__':
    project_dir = "/Users/blaseco/Desktop/Plakat_Kutatas_2025_2026"
    out_pdf = os.path.join(project_dir, "AI_Nyilatkozat_Varga_Balazs_2025_2026.pdf")
    create_ai_declaration_pdf(out_pdf)
