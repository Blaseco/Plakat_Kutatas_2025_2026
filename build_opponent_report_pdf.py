#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the Official Opponent Evaluation and Reproduction Report PDF.
Bibó István Szakkollégium · AI Kurzus · Dr. Miklós Sebők
Opponens: Varga Balázs
Követelmény: "készüljetek fel egy társatok elemzésének opponálására (szóbeli vita + reprodukciós jelentés)."
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Opponensi_Ertekelo_Lap_es_Reprodukcios_Jelentes_Varga_Balazs.pdf")

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
        if self._pageNumber > 1:
            self.drawString(36, 810, "BIBÓ ISTVÁN SZAKKOLLÉGIUM · AI KURZUS · OPPONENSI JELENTÉS (BLOCK 4)")
            self.drawRightString(559, 810, "OPPONENS: VARGA BALÁZS")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 25, "Hivatalos kurzusdokumentum · Block 4 szóbeli vita és opponensi jelentés")
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

    header_style = ParagraphStyle(
        'HeaderStyle',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A365D")
    )
    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=5
    )
    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=4,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )
    cell_style = ParagraphStyle(
        'CellStyle',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # PAGE 1
    story.append(Paragraph("<b>BIBÓ ISTVÁN SZAKKOLLÉGIUM</b> · Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (2026 ősz)<br/><b>Oktató:</b> Dr. Sebők Miklós · <b>Hivatalos kurzuskövetelmény: Block 4 Opponensi Értékelés</b>", header_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=1, spaceAfter=4))

    story.append(Paragraph("OPPONENSI ÉRTÉKELŐ LAP ÉS REPRODUKCIÓS JELENTÉS", title_style))
    story.append(Paragraph("A hallgatótárs kutatásának és kódjának formai, módszertani és reprodukálhatósági vizsgálata", subtitle_style))

    # Meta table
    meta_data = [
        [Paragraph("<b>Opponens hallgató neve:</b>", cell_bold), Paragraph("Varga Balázs", cell_style), Paragraph("<b>Dátum / Alkalom:</b>", cell_bold), Paragraph("2026. november (4. blokk)", cell_style)],
        [Paragraph("<b>Opponált hallgató neve:</b>", cell_bold), Paragraph("<i>[Kitöltendő a bemutató során]</i>", cell_style), Paragraph("<b>Kutatási téma:</b>", cell_bold), Paragraph("<i>[Opponált kutatás címe]</i>", cell_style)],
        [Paragraph("<b>Opponált GitHub repó URL:</b>", cell_bold), Paragraph("https://github.com/...", cell_style), Paragraph("<b>Repó reprodukálva?</b>", cell_bold), Paragraph("[ ] Igen  [ ] Részben  [ ] Nem", cell_style)],
    ]
    t_meta = Table(meta_data, colWidths=[120, 150, 110, 143])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    # Section 1: Reproduction Audit
    story.append(Paragraph("1. Reprodukálhatósági ellenőrzés (A repó önálló futása – Slide 40 & 45)", h1_style))
    p_repro_intro = (
        "<i>„THE POINT: Your opponent reproduces your numbers, so the repo has to run without you.”</i> (Slide 45). "
        "Az opponensi feladat annak ellenőrzése, hogy a repó külső szerzői segítség nélkül reprodukálja-e a közzétett számokat."
    )
    story.append(Paragraph(p_repro_intro, body_style))
    story.append(Spacer(1, 2))

    repro_checklist = [
        [Paragraph("<b>Ellenőrzött szempont</b>", cell_bold), Paragraph("<b>Elvárás (Sebők-standard)</b>", cell_bold), Paragraph("<b>Értékelés</b>", cell_bold), Paragraph("<b>Megjegyzés / Hibaleírás</b>", cell_bold)],
        [Paragraph("<b>1. Adatkészlet (Data)</b>", cell_style), Paragraph("CSV vagy SQL formátum, zérus hiányzó kulcsmező, egyedi azonosítók.", cell_style), Paragraph("[ ] PASS  [ ] FAIL", cell_bold), Paragraph("", cell_style)],
        [Paragraph("<b>2. Kódkönyv (Codebook)</b>", cell_style), Paragraph("Zárt kategóriák, inklúziós szabályok, példák, kizárások, set-aside kód.", cell_style), Paragraph("[ ] PASS  [ ] FAIL", cell_bold), Paragraph("", cell_style)],
        [Paragraph("<b>3. Futtathatóság (reproduce.py)</b>", cell_style), Paragraph("Egyetlen paranccsal lefut; nem igényel manuális beavatkozást.", cell_style), Paragraph("[ ] PASS  [ ] FAIL", cell_bold), Paragraph("", cell_style)],
        [Paragraph("<b>4. Megbízhatóság (Agreement)</b>", cell_style), Paragraph("Vak humán arany standard (`hand.csv`), Cohen-kappa (κ) kiszámítva.", cell_style), Paragraph("[ ] PASS  [ ] FAIL", cell_bold), Paragraph("", cell_style)],
        [Paragraph("<b>5. Táblázatok és Ábrák</b>", cell_style), Paragraph("Kétszer futtatva determinisztikusan ugyanazt az ábrát termeli (Slide 40).", cell_style), Paragraph("[ ] PASS  [ ] FAIL", cell_bold), Paragraph("", cell_style)],
        [Paragraph("<b>6. MI-nyilatkozat</b>", cell_style), Paragraph("Eszközök, elvégzett feladatok, ellenőrzési mód, fennmaradó kockázat.", cell_style), Paragraph("[ ] PASS  [ ] FAIL", cell_bold), Paragraph("", cell_style)]
    ]
    t_repro = Table(repro_checklist, colWidths=[110, 175, 75, 163])
    t_repro.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor("#0F172A")),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor("#0F172A")),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.HexColor("#0F172A")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_repro)
    story.append(Spacer(1, 4))

    # Section 2: Methodological critique
    story.append(Paragraph("2. Módszertani és tartalmi minőségbiztosítás (Sebők-kritériumok)", h1_style))
    method_data = [
        [Paragraph("<b>Kritérium</b>", cell_bold), Paragraph("<b>Opponensi vizsgálati kérdés</b>", cell_bold), Paragraph("<b>Tapasztalat az opponált munkában</b>", cell_bold)],
        [
            Paragraph("<b>Unit of Analysis vs. Observation</b>", cell_style),
            Paragraph("Világosan elválik-e a megfigyelési egység (pl. szöveg, plakát) az elemzési egységtől (aktor, párt, időszak)? (Slide 4)", cell_style),
            Paragraph("<i>[Megfelelő / Nem tisztázott]</i>", cell_style)
        ],
        [
            Paragraph("<b>Falszifikálhatóság (*What sinks it*)</b>", cell_style),
            Paragraph("Megfogalmazta-e a szerző, hogy milyen empirikus eredmény döntené meg a hipotézisét? (Slide 4/44)", cell_style),
            Paragraph("<i>[Egyértelmű / Hiányzik a cáfolati feltétel]</i>", cell_style)
        ],
        [
            Paragraph("<b>Leíró statisztikák (*Describe before model*)</b>", cell_style),
            Paragraph("Bemutatta-e a szerző az adatokat a modellezés előtt? Standard booktabs táblázat készült-e? (Slide 37, 41)", cell_style),
            Paragraph("<i>[Igen, Table 1 rendelkezésre áll / Nem]</i>", cell_style)
        ],
        [
            Paragraph("<b>Mérési hiba és kalibráció (/vcalibrate)</b>", cell_style),
            Paragraph("Reflektál-e a szerző a nyelvi modell tévesztéseire? Alkalmaz-e Rogan–Gladen korrekciót? (Slide 42)", cell_style),
            Paragraph("<i>[Korrekció elvégezve / Nyers prevalencia szerepel]</i>", cell_style)
        ],
        [
            Paragraph("<b>Gyűjtési rés kezelése (*Collection gap*)</b>", cell_style),
            Paragraph("Helyesen értelmezi-e a szerző az aszimmetrikus cellákat mint gyűjtési rést, nem pedig csendes hírt? (Slide 41)", cell_style),
            Paragraph("<i>[Helyes kontextualizálás / Tévesen trendként kezeli]</i>", cell_style)
        ]
    ]
    t_method = Table(method_data, colWidths=[120, 230, 173])
    t_method.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor("#0F172A")),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor("#0F172A")),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.HexColor("#0F172A")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_method)

    story.append(PageBreak())

    # PAGE 2: QUESTIONS AND FINAL VERDICT
    story.append(Paragraph("3. Célzott vitakérdések az opponált szerzőhöz (Szóbeli vita forgatókönyve)", h1_style))
    p_q_intro = "A szóbeli vita során felteendő 3 módszertani keresztkérdés az elemzés gyenge pontjainak tesztelésére:"
    story.append(Paragraph(p_q_intro, body_style))
    story.append(Spacer(1, 3))

    q_box_data = [
        [
            Paragraph("<b>1. KÉRDÉS (Kódkönyvi határesetek és validitás):</b><br/>"
                      "<i>„Hogyan járt el a kódkönyve azokban a határesetekben, ahol a szövegben egyszerre jelent meg pozitív szakpolitikai eredmény és az ellenfél támadása? "
                      "Milyen döntési szabállyal védte meg a klasszifikátort attól, hogy a gép önkényesen válasszon kategóriát?”</i>", cell_style)
        ],
        [
            Paragraph("<b>2. KÉRDÉS (Mérési hiba és Rogan–Gladen korrekció):</b><br/>"
                      "<i>„A prezentációban bemutatott arányok a modell nyers megfigyelt prevalenciáját tükrözik, vagy korrigálva lettek a classifier szenzitivitása és specificitása alapján? "
                      "Ha a modell hibázna a ritkább kategóriáknál, hogyan védené meg a regressziót a szisztematikus torzítástól?”</i>", cell_style)
        ],
        [
            Paragraph("<b>3. KÉRDÉS (Gyűjtési rés vs. valódi trend – Slide 41):</b><br/>"
                      "<i>„Az adatbázisban megfigyelhető mintavételi aszimmetria (pl. az egyik csoport jóval alacsonyabb esetszáma) valóban a politikai aktivitás különbsége, "
                      "vagy egy strukturális gyűjtési rés (collection gap) eredménye? Hogyan támasztja alá, hogy ez nem gyűjtési hiba?”</i>", cell_style)
        ]
    ]
    t_q = Table(q_box_data, colWidths=[523])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_q)
    story.append(Spacer(1, 5))

    story.append(Paragraph("4. Opponensi összegzés és minősítés", h1_style))
    summary_data = [
        [Paragraph("<b>Opponensi javaslat:</b>", cell_bold), Paragraph("[ ] ELFOGADÁSRA JAVASLOM (A kutatás és kód maradéktalanul reprodukálható)<br/>[ ] JAVÍTÁSSAL ELFOGADHATÓ (Kisebb kódolási vagy reprodukciós hiánypótlás szükséges)<br/>[ ] ÁTDOLGOZÁS SZÜKSÉGES (A repó nem fut le vagy a kódkönyv nem validálható)", cell_style)],
        [Paragraph("<b>Szóbeli értékelés fő pontjai:</b>", cell_bold), Paragraph("1. Erősségek: <i>[Repó tisztasága, önálló futás, releváns téma]</i><br/>2. Fejlesztendő pontok: <i>[Mérési hibák kezelése, határvonal-döntések dokumentálása]</i>", cell_style)],
        [Paragraph("<b>Aláírás:</b>", cell_bold), Paragraph("<b>Varga Balázs</b> s.k. (Opponens hallgató)", cell_style)]
    ]
    t_sum = Table(summary_data, colWidths=[130, 393])
    t_sum.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_sum)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Sikeres Opponensi Jelentés PDF generálás: {PDF_PATH}")

if __name__ == '__main__':
    build_pdf()
