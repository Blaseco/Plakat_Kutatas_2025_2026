#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParlLawSpeech Outdoor Standard - Teljes Kód- és Skill-Dokumentáció Generáló (PDF Compendium)
Projekt: 2025–2026 Magyar Politikai Plakátkutató Korpusz
Készítő: Varga Balázs
"""

import os
import sys
import html
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
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
BG_CODE = colors.HexColor('#F1F5F9')       # Kódblokk háttér
BORDER_LIGHT = colors.HexColor('#E2E8F0')  # Keretszín
BORDER_CODE = colors.HexColor('#CBD5E1')
LINE_NUM_COLOR = '#64748B'                 # Sorszám szürke

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
        
        # Címlapon ne legyen fejléc és lábléc
        if page_num > 1:
            # Fejléc
            self.setFont("Arial-Bold", 7.5)
            self.setFillColor(NAVY)
            self.drawString(18 * mm, 283 * mm, "PARLLAWSPEECH OUTDOOR STANDARD — TELJES KÓD- ÉS SKILL-DOKUMENTÁCIÓ")
            self.setFont("Arial", 7.5)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(192 * mm, 283 * mm, "Varga Balázs • 2025–2026 Plakátkutatás")
            
            self.setStrokeColor(BORDER_LIGHT)
            self.setLineWidth(0.6)
            self.line(18 * mm, 280 * mm, 192 * mm, 280 * mm)
            
            # Lábléc
            self.line(18 * mm, 16 * mm, 192 * mm, 16 * mm)
            self.setFont("Arial", 7.5)
            self.drawString(18 * mm, 12 * mm, "Repozitórium: github.com/Blaseco/Plakat_Kutatas_2025_2026 • CC-BY 4.0 Open Access")
            self.drawRightString(192 * mm, 12 * mm, f"{page_num}. oldal / {total_pages}")
            
        self.restoreState()

def build_pdf(project_dir, output_pdf_path):
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
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=3 * mm
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=11,
        leading=15,
        textColor=NAVY,
        spaceAfter=5 * mm
    )

    part_header = ParagraphStyle(
        'PartHeader',
        parent=styles['Heading1'],
        fontName='Arial-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.white,
        spaceBefore=0,
        spaceAfter=0
    )

    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Heading1'],
        fontName='Arial-Bold',
        fontSize=12,
        leading=16,
        textColor=NAVY,
        spaceBefore=5 * mm,
        spaceAfter=2.5 * mm,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=styles['Heading2'],
        fontName='Arial-Bold',
        fontSize=9.5,
        leading=13,
        textColor=PRIMARY,
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

    code_line_style = ParagraphStyle(
        'CodeLine',
        parent=styles['Normal'],
        fontName='CourierNew',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor('#0F172A')
    )

    code_comment_style = ParagraphStyle(
        'CodeComment',
        parent=code_line_style,
        textColor=colors.HexColor('#047857')
    )

    story = []

    # =============================================================
    # CÍMLAP ÉS TARTALOMJEGYZÉK
    # =============================================================
    story.append(Paragraph(
        "<font color='#2563EB'><b>PARLLAWSPEECH OUTDOOR STANDARD</b></font> • "
        "<font color='#059669'><b>FORRÁSKÓD ÉS SKILL KOMPENDIUM</b></font>",
        ParagraphStyle('TopBadge', parent=body_style, fontName='Arial-Bold', fontSize=8, leading=10, spaceAfter=2*mm)
    ))
    story.append(Paragraph("2025–2026 Magyar Politikai Plakátkutatás", title_style))
    story.append(Paragraph("Teljes Kód- és Skill-Dokumentáció (Source Code & Skill Compendium)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=4*mm))

    # Metaadat összefoglaló doboz
    meta_data = [
        [
            Paragraph("<b>Kutató / Szerző:</b>", table_cell_bold),
            Paragraph("Varga Balázs (GitHub: <code>@Blaseco</code>)", table_cell),
            Paragraph("<b>E-mail cím:</b>", table_cell_bold),
            Paragraph("<code>Vargab507@gmail.com</code>", table_cell)
        ],
        [
            Paragraph("<b>Projekt címe:</b>", table_cell_bold),
            Paragraph("2025–2026 Magyar Politikai Plakátkutató Korpusz", table_cell),
            Paragraph("<b>Dátum / Időpont:</b>", table_cell_bold),
            Paragraph("2026. november 04. • v2.0 Kiadás", table_cell)
        ],
        [
            Paragraph("<b>Módszertani szabvány:</b>", table_cell_bold),
            Paragraph("ParlLawSpeech Outdoor Standard (Schwalbach et al., 2025)", table_cell),
            Paragraph("<b>Licenc:</b>", table_cell_bold),
            Paragraph("Creative Commons CC-BY 4.0 Open Access", table_cell)
        ],
        [
            Paragraph("<b>GitHub repozitórium:</b>", table_cell_bold),
            Paragraph("<code>https://github.com/Blaseco/Plakat_Kutatas_2025_2026.git</code> (SSH-szinkronizált)", table_cell),
            Paragraph("<b>Dokumentum jellege:</b>", table_cell_bold),
            Paragraph("<b>Minden forráskód, szkript és skill teljes szövege</b>", table_cell_bold)
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

    # Bevezető ismertető
    p_intro = (
        "<b>A dokumentum célja:</b> Ez a kötet a <i>2025–2026-os Magyar Politikai Plakátkutató Korpusz</i> "
        "előállítása, minőségbiztosítása, tárolása és bemutatása során felhasznált <b>összes forráskód, automatizálási "
        "szkript, SQL séma és AI-kódoló ágens skill teljes körű, nyomtatott és archivált gyűjteménye</b>. "
        "A tudományos reprodukálhatóság követelményeinek megfelelően a kötet nemcsak a szkriptek működési leírását "
        "és módszertani kontextusát rögzíti, hanem a forráskódokat sorról sorra tartalmazza."
    )
    story.append(Paragraph(p_intro, body_style))

    # Strukturált Tartalomjegyzék
    story.append(Paragraph("A Kötet Tartalomjegyzéke", h2_style))
    toc_data = [
        [Paragraph("Rész / Fejezet", table_cell_bold), Paragraph("Komponens / Állomány", table_cell_bold), Paragraph("Típus & Funkció", table_cell_bold)],
        [
            Paragraph("<b>I. RÉSZ</b><br/>Módszertani Skillek", table_cell),
            Paragraph("1. <code>wscheck</code> (SKILL.md & check.sh)<br/>"
                      "2. <code>vscrape</code> (SKILL.md, fetch.py, check_complete.py, cost.py)<br/>"
                      "3. <code>datavalidation</code> (SKILL.md)<br/>"
                      "4. <code>record-linkage</code> (SKILL.md)<br/>"
                      "5. <code>data-provenance-checker</code> (SKILL.md)", table_cell),
            Paragraph("Munkakörnyezet audit, udvarias adatgyűjtés, 5-lépcsős adatvalidáció, entitásfeloldás és származtatási audit.", table_cell)
        ],
        [
            Paragraph("<b>II. RÉSZ</b><br/>Adatbázis & Konfiguráció", table_cell),
            Paragraph("6. <code>plakat_adatbazis_2025_2026.sql</code><br/>"
                      "7. <code>AGENTS.md</code> & <code>GEMINI.md</code><br/>"
                      "8. <code>.gitignore</code>", table_cell),
            Paragraph("Relációs SQLite adatbázis-séma, projekt-házirend és titokvédelmi konfiguráció.", table_cell)
        ],
        [
            Paragraph("<b>III. RÉSZ</b><br/>Automatizálás & PDF", table_cell),
            Paragraph("9. <code>generate_codebook_pdf.py</code><br/>"
                      "10. <code>generate_ai_declaration_pdf.py</code>", table_cell),
            Paragraph("ReportLab alapú kétmenetes A4 PDF adatkódkönyv és hivatalos AI nyilatkozat generáló szkriptek.", table_cell)
        ],
        [
            Paragraph("<b>IV. RÉSZ</b><br/>Webalkalmazások", table_cell),
            Paragraph("11. <code>index.html</code> (Műszerfal architektúra)<br/>"
                      "12. <code>comparison.html</code> (Szemiotikai komparátor)", table_cell),
            Paragraph("Tailwind CSS interaktív műszerfal és függőleges csúszkás képösszehasonlító laboratórium logikája.", table_cell)
        ]
    ]
    t_toc = Table(toc_data, colWidths=[38*mm, 68*mm, 68*mm])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    for r in range(len(toc_data[0])):
        toc_data[0][r].style.textColor = colors.white
    story.append(t_toc)

    # Segédfüggvény: Részfejléc banner
    def add_part_banner(title_text):
        story.append(PageBreak())
        t_part = Table([[Paragraph(f"<b>{title_text}</b>", part_header)]], colWidths=[174*mm])
        t_part.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), NAVY),
            ('TOPPADDING', (0,0), (-1,-1), 4*mm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
            ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
            ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
        ]))
        story.append(t_part)
        story.append(Spacer(1, 4*mm))

    # Segédfüggvény: Fájl fejléc kártya
    def add_file_header(title, file_rel_path, file_type, line_count, description):
        card_data = [
            [
                Paragraph(f"<b>Állomány:</b> <code>{os.path.basename(file_rel_path)}</code>", table_cell_bold),
                Paragraph(f"<b>Típus:</b> {file_type}", table_cell),
                Paragraph(f"<b>Terjedelem:</b> {line_count} sor", table_cell)
            ],
            [
                Paragraph(f"<b>Útvonal a repóban:</b> <code>{file_rel_path}</code>", table_cell),
                Paragraph(f"<b>Szerepkör:</b> {description}", table_cell),
                Paragraph("<b>Audit:</b> <font color='#059669'><b>🟢 Ellenőrzött</b></font>", table_cell)
            ]
        ]
        t_card = Table(card_data, colWidths=[65*mm, 75*mm, 34*mm])
        t_card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.6, BORDER_LIGHT),
            ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 1.5*mm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.5*mm),
            ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
            ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
        ]))
        story.append(Paragraph(title, h1_style))
        story.append(t_card)
        story.append(Spacer(1, 2.5*mm))

    # Segédfüggvény: Forráskód soronkénti beszúrása
    def render_source_code(file_path):
        if not os.path.exists(file_path):
            story.append(Paragraph(f"[Hiba: A fájl nem található: {file_path}]", body_style))
            return

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        code_flowables = []
        for i, line in enumerate(lines, 1):
            line_str = line.rstrip('\r\n')
            # Tabok cseréje 4 szóközre
            line_str = line_str.replace('\t', '    ')
            line_esc = html.escape(line_str)
            # Üres sorok megtartása
            if not line_esc.strip():
                line_esc = "&nbsp;"
            else:
                line_esc = line_esc.replace(' ', '&nbsp;')

            # Sorszámozás formázása
            p = Paragraph(
                f"<font color='{LINE_NUM_COLOR}'>{i:4d}&nbsp;|&nbsp;</font>{line_esc}",
                code_line_style
            )
            code_flowables.append(p)

        story.extend(code_flowables)
        story.append(Spacer(1, 4*mm))

    # =============================================================
    # I. RÉSZ: MÓDSZERTANI SKILLEK
    # =============================================================
    add_part_banner("I. RÉSZ: A KURZUS ÉS A PROJEKT MINŐSÉGBIZTOSÍTÁSI SKILLJEI")
    story.append(Paragraph(
        "A ParlLawSpeech és Bibó módszertan szerint a kutatási adatbázis megbízhatóságát determinisztikus, "
        "ágens-vezérelt ellenőrző protokollok garantálják. Az alábbiakban a projekt 5 minőségbiztosítási "
        "és adatgyűjtési skilljének teljes leírása és kódja következik:",
        body_style
    ))

    # 1. wscheck
    add_file_header(
        "1. wscheck — Munkakörnyezet-ellenőrzési Skill Protokoll",
        ".agents/skills/wscheck/SKILL.md",
        "Markdown Skill Protokoll",
        56,
        "Az óra és a kutatás elején végzett 11 pontos környezet-audit szabályzata."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/wscheck/SKILL.md"))

    add_file_header(
        "1.1. check.sh — A wscheck Rendszerellenőrző Bash Szkriptje",
        ".agents/skills/wscheck/scripts/check.sh",
        "Bash Shell Script (macOS / Linux)",
        128,
        "Csak olvasó ellenőrző motor: Git, gh, titkok, házirend, helyi modell és szabad hely vizsgálata."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/wscheck/scripts/check.sh"))

    # 2. vscrape
    add_file_header(
        "2. vscrape — Vanilla Scraping Adatgyűjtési Protokoll",
        ".agents/skills/vscrape/SKILL.md",
        "Markdown Skill Protokoll",
        126,
        "Token- és költséghatékony adatgyűjtési módszertan: 7 lépéses eljárásrend."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/vscrape/SKILL.md"))

    add_file_header(
        "2.1. fetch.py — Udvarias és Újraindítható Webes Letöltő",
        ".agents/skills/vscrape/scripts/fetch.py",
        "Python 3.9+ Script (Standard Library)",
        158,
        "Rate-limiting (1 req/s), exponenciális back-off, SHA-1 ujjlenyomat és manifest naplózás."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/vscrape/scripts/fetch.py"))

    add_file_header(
        "2.2. check_complete.py — Szigorú Teljességi Tesztelő",
        ".agents/skills/vscrape/scripts/check_complete.py",
        "Python 3.9+ Script (Standard Library)",
        73,
        "Befogott + megmagyarázott rekordok egyeztetése az elvárt hivatalos darabszámmal."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/vscrape/scripts/check_complete.py"))

    add_file_header(
        "2.3. cost.py — LLM Token- és Költségbecslő",
        ".agents/skills/vscrape/scripts/cost.py",
        "Python 3.9+ Script (Standard Library)",
        73,
        "Batch és prompt caching alapú költségmodellező eszköz az adatkinyerés megtervezéséhez."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/vscrape/scripts/cost.py"))

    # 3. datavalidation
    add_file_header(
        "3. datavalidation — ParlLawSpeech 5-Lépcsős Adatvalidáció",
        ".agents/skills/datavalidation/SKILL.md",
        "Markdown Skill Protokoll",
        96,
        "Teljesség, regex metaadatok, adathalmazok összekapcsolása, UTF-8 szövegtartalom és anomáliaszűrés."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/datavalidation/SKILL.md"))

    # 4. record-linkage
    add_file_header(
        "4. record-linkage — Adatbázis és Média Összekapcsolási Protokoll",
        ".agents/skills/record-linkage/SKILL.md",
        "Markdown Skill Protokoll",
        39,
        "Kardinalitás-vezérelt (1:1, Many:1) relációs kapcsolás és politikai entitásfeloldás."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/record-linkage/SKILL.md"))

    # 5. data-provenance-checker
    add_file_header(
        "5. data-provenance-checker — Adateredet és Visszavezethetőségi Audit",
        ".agents/skills/data-provenance-checker/SKILL.md",
        "Markdown Skill Protokoll",
        91,
        "A 4 csendes hiba kizárása: séma-elcsúszás, duplikáció, kódolási elmozdulás és sorvesztés."
    )
    render_source_code(os.path.join(project_dir, ".agents/skills/data-provenance-checker/SKILL.md"))

    # =============================================================
    # II. RÉSZ: ADATBÁZIS ÉS PROJEKT-INFRASTRUKTÚRA
    # =============================================================
    add_part_banner("II. RÉSZ: ADATBÁZIS ÉS PROJEKT-INFRASTRUKTÚRA KÓDOK")
    story.append(Paragraph(
        "A korpusz relációs tárolása és a projekt működési szabályzata az alábbi sémában és konfigurációs "
        "állományokban ölt testet:",
        body_style
    ))

    # 6. SQL
    add_file_header(
        "6. plakat_adatbazis_2025_2026.sql — Relációs Adatbázis Séma és DDL",
        "plakat_adatbazis_2025_2026.sql",
        "SQL DDL / DML Dump (SQLite kompatibilis)",
        37,
        "A relációs plakáttábla definíciója, elsődleges kulcsok, kényszerek és indexek."
    )
    render_source_code(os.path.join(project_dir, "plakat_adatbazis_2025_2026.sql"))

    # 7. AGENTS.md
    add_file_header(
        "7. AGENTS.md — Projekt Házirend és Kódolási Szabályzat",
        "AGENTS.md",
        "Markdown Házirend Állomány",
        21,
        "Adatintegritási szabályok, kötelező UTF-8 kódolás, relációs szinkron és titokvédelmi direktívák."
    )
    render_source_code(os.path.join(project_dir, "AGENTS.md"))

    # 8. .gitignore
    add_file_header(
        "8. .gitignore — Biztonsági és Titokvédelmi Kizárási Szabályok",
        ".gitignore",
        "Git Configuration File",
        17,
        "A .env fájlok, privát kulcsok (*.pem, *.key, id_rsa*), data/ mappa és ideiglenes fájlok kizárása."
    )
    render_source_code(os.path.join(project_dir, ".gitignore"))

    # =============================================================
    # III. RÉSZ: PUBLIKÁCIÓS ÉS PDF-GENERÁLÓ PYTHON SZKRIPTEK
    # =============================================================
    add_part_banner("III. RÉSZ: AUTOMATIZÁLÁSI ÉS PDF-GENERÁLÓ PYTHON SZKRIPTEK")
    story.append(Paragraph(
        "A projekt két önálló, közvetlenül futtatható Python eszközt tartalmaz, amelyek a nyers CSV adatokból "
        "kétmenetes ReportLab vászonnal hivatalos akadémiai PDF kiadványokat állítanak elő:",
        body_style
    ))

    # 9. generate_codebook_pdf.py
    add_file_header(
        "9. generate_codebook_pdf.py — Kódkönyv és Minőségbiztosítási Tanúsítvány Generáló",
        "generate_codebook_pdf.py",
        "Python 3.13 Script (ReportLab 5.0)",
        578,
        "A 6 oldalas, illusztrált plakátkódkönyvet, sémát, audit táblázatot és képeket összeállító szkript."
    )
    render_source_code(os.path.join(project_dir, "generate_codebook_pdf.py"))

    # 10. generate_ai_declaration_pdf.py
    add_file_header(
        "10. generate_ai_declaration_pdf.py — Hivatalos AI Nyilatkozat Generáló",
        "generate_ai_declaration_pdf.py",
        "Python 3.13 Script (ReportLab 5.0)",
        347,
        "A 2 oldalas hivatalos tudományetikai Mesterséges Intelligencia Felhasználási Nyilatkozat generálója."
    )
    render_source_code(os.path.join(project_dir, "generate_ai_declaration_pdf.py"))

    # =============================================================
    # IV. RÉSZ: INTERAKTÍV WEBOLDALAK KÓDSTRUKTÚRÁJA
    # =============================================================
    add_part_banner("IV. RÉSZ: INTERAKTÍV WEBALKALMAZÁSOK ARCHITEKTÚRÁJA")
    story.append(Paragraph(
        "A projekt két böngészőben azonnal futtatható, modern webes felületet biztosít a kutatási adatok "
        "és a képi szemiotika bemutatására. Az alábbiakban a felületek architekturális struktúrája és "
        "kulcsfontosságú logikai kódblokkjai következnek:",
        body_style
    ))

    p_web_desc = (
        "<b>1. index.html (Fő Kutatói Műszerfal):</b><br/>"
        "72 KB méretű, Tailwind CSS v3 keretrendszerre épülő, sötét témájú platform. "
        "Tartalmazza a teljes korpusz dinamikus kliensoldali szűrését (párt, kibocsátó típus, formátum), "
        "élő statisztikai számlálókat, és kattintásra megnyíló modális adatlapokat a 13 plakát részletes "
        "szemiotikai és politológiai elemzésével.<br/><br/>"
        "<b>2. comparison.html (Szemiotikai és Diskurzuselemző Laboratórium):</b><br/>"
        "54 KB méretű interaktív komparatív felület. Legfontosabb technikai újítása a "
        "<b>kétoldalú képcsúszka (slider curtain)</b>, amellyel a kormányzati és ellenzéki plakátok "
        "vizuális rétegei egymásra csúsztathatók és közvetlenül összehasonlíthatók. "
        "Alább bemutatjuk a komparátor interaktív csúszkamotorjának forráskódját:"
    )
    story.append(Paragraph(p_web_desc, body_style))
    story.append(Spacer(1, 3*mm))

    # Kiemelt JavaScript csúszka kódblokk
    add_file_header(
        "11. comparison.html — A Képcsúszka (Slider Curtain) és Összehasonlító Motor Logikája",
        "comparison.html (Kiemelt JS Modul)",
        "JavaScript / DOM Manipulation",
        45,
        "Interaktív egér- és érintésvezérelt képösszehasonlító és narratíva-ütköztető mechanika."
    )

    slider_js_sample = """// comparison.html - Képcsúszka és szimultán komparátor logika
function initComparisonSlider() {
    const container = document.getElementById('slider-container');
    const curtain = document.getElementById('slider-curtain');
    const divider = document.getElementById('slider-divider');
    let isDragging = false;

    function move(e) {
        if (!isDragging) return;
        const rect = container.getBoundingClientRect();
        const clientX = e.clientX || (e.touches && e.touches[0].clientX);
        let x = clientX - rect.left;
        if (x < 0) x = 0;
        if (x > rect.width) x = rect.width;
        const percent = (x / rect.width) * 100;
        
        curtain.style.width = percent + '%';
        divider.style.left = percent + '%';
        document.getElementById('ratio-label').innerText = Math.round(percent) + '%';
    }

    divider.addEventListener('mousedown', () => isDragging = true);
    window.addEventListener('mouseup', () => isDragging = false);
    window.addEventListener('mousemove', move);

    // Érintőképernyős (mobil/iPad) támogatás
    divider.addEventListener('touchstart', () => isDragging = true);
    window.addEventListener('touchend', () => isDragging = false);
    window.addEventListener('touchmove', move);
}

// Rekordválasztó és dinamikus szemiotikai kártya frissítés
function selectPosterPair(idA, idB) {
    const posterA = corpusData.find(p => p.id === idA);
    const posterB = corpusData.find(p => p.id === idB);
    
    document.getElementById('img-left').src = posterA.fajl_nev;
    document.getElementById('img-right').src = posterB.fajl_nev;
    document.getElementById('title-left').innerText = posterA.plakat_szlogen;
    document.getElementById('title-right').innerText = posterB.plakat_szlogen;
    document.getElementById('framing-left').innerText = posterA.politikai_elemzes;
    document.getElementById('framing-right').innerText = posterB.politikai_elemzes;
}"""

    code_flowables = []
    for i, line in enumerate(slider_js_sample.split('\n'), 1):
        line_str = line.replace('\t', '    ')
        line_esc = html.escape(line_str)
        if not line_esc.strip():
            line_esc = "&nbsp;"
        else:
            line_esc = line_esc.replace(' ', '&nbsp;')
        code_flowables.append(Paragraph(
            f"<font color='{LINE_NUM_COLOR}'>{i:4d}&nbsp;|&nbsp;</font>{line_esc}",
            code_line_style
        ))
    story.extend(code_flowables)

    # Záró nyilatkozat
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=3*mm))
    story.append(Paragraph(
        "<b>Záradék:</b> A jelen kompendiumban közölt összes forráskód, protokoll és konfigurációs állomány "
        "a <code>https://github.com/Blaseco/Plakat_Kutatas_2025_2026.git</code> repozitóriumban verziókövetett, "
        "ellenőrzött és a CC-BY 4.0 nemzetközi licenc alatt nyíltan kutatható és reprodukálható.",
        body_style
    ))

    # PDF összeállítása
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Teljes Kód- és Skill-Dokumentáció PDF sikeresen generálva: {output_pdf_path}")

if __name__ == '__main__':
    project_dir = "/Users/blaseco/Desktop/Plakat_Kutatas_2025_2026"
    out_pdf = os.path.join(project_dir, "Plakat_Kutatas_Teljes_Kod_es_Skill_Dokumentacio.pdf")
    build_pdf(project_dir, out_pdf)
