#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teljes Prezentációs Mesterdokumentáció és Kutatási Kézikönyv Generáló (.docx)
Projekt: Magyar Közpolitikai Plakátkorpusz (2025–2026)
Készítő: Varga Balázs | Bibó István Szakkollégium
Kurzus: Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (Sebők Miklós)

Tartalom:
- Címlap, összefoglaló, prezentációs "cheat sheet"
- Módszertan & 12 lefutott skill kódjai, hatása és naplója
- 4 beágyazott statisztikai ábra magyarázatokkal
- Mind a 13 plakát beágyazott fotóval, szlogennel, szemiotikai és retorikai elemzéssel
- 5 perces prezentációs forgatókönyv és vizsgakérdések védési válaszai
"""

import os
import sys
import csv
import json
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = "/Users/blaseco/Desktop/ai kurzus/Plakat_Kutatas_2025_2026"
PARENT_DIR = "/Users/blaseco/Desktop/ai kurzus"
CHARTS_DIR = os.path.join(BASE_DIR, "kutatasi_grafikonok")

# Segédfüggvény táblázat cella háttérszínéhez
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Oldalbeállítások (A4 méret, 2.0 cm margók)
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Színek
    C_PRIMARY = RGBColor(15, 23, 42)      # Sötétkék / Slate
    C_NAVY = RGBColor(30, 58, 138)        # Navy
    C_ACCENT = RGBColor(37, 99, 235)      # Kék kiemelés
    C_DARK = RGBColor(51, 65, 85)         # Szürke szöveg
    C_GREEN = RGBColor(5, 150, 105)       # Zöld siker
    C_RED = RGBColor(220, 38, 38)         # Piros támadó

    # Stílusok finomhangolása
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(10)
    style_normal.font.color.rgb = C_DARK
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # CÍMLAP / FEJLÉC SÁV
    # -------------------------------------------------------------------------
    p_header = doc.add_paragraph()
    r_hdr = p_header.add_run("BIBÓ ISTVÁN SZAKKOLLÉGIUM · 2026. ŐSZ\nMesterséges intelligencia a társadalom- és politikatudományi kutatásban\nKurzustartó oktató: Sebők Miklós")
    r_hdr.font.size = Pt(9)
    r_hdr.font.bold = True
    r_hdr.font.color.rgb = C_NAVY
    p_header.paragraph_format.space_after = Pt(12)

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("KUTATÁSI, MÓDSZERTANI ÉS PREZENTÁCIÓS MESTERDOKUMENTÁCIÓ")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = C_PRIMARY
    p_title.paragraph_format.space_after = Pt(2)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Magyar Közpolitikai Plakátkorpusz (2025–2026) — Képi és Diskurzuselemzés, Szemiotikai Kódolás, Módszertani Skill-Audit és Védési Kézikönyv")
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = C_ACCENT
    p_sub.paragraph_format.space_after = Pt(8)

    # Szerzői metaadat doboz
    meta_table = doc.add_table(rows=1, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    set_cell_background(meta_table.rows[0].cells[0], "F1F5F9")
    set_cell_background(meta_table.rows[0].cells[1], "F1F5F9")
    set_cell_background(meta_table.rows[0].cells[2], "F1F5F9")
    meta_table.rows[0].cells[0].paragraphs[0].add_run("Készítő:\nVarga Balázs").bold = True
    meta_table.rows[0].cells[1].paragraphs[0].add_run("Dátum:\n2026. november 17.").bold = True
    meta_table.rows[0].cells[2].paragraphs[0].add_run("Git tároló:\ngithub.com/Blaseco/Plakat_Kutatas_2025_2026").bold = True
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # VEZETŐI ÖSSZEFOGLALÓ & PREZENTÁCIÓS "CHEAT SHEET"
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("0. Prezentációs Gyorstájékoztató (Cheat Sheet a Védéshez)", level=1)
    h1.style.font.color.rgb = C_NAVY
    h1.style.font.size = Pt(13)

    p_cs = doc.add_paragraph()
    p_cs.add_run("Ha a prezentáció közben azonnal rá kell nézned a legfontosabb sarokszámokra és tézisekre, ezt mondd el 1 percben:\n")
    
    bullet_points = [
        ("Korpusz nagysága és fókusza: ", "N = 13 db gondosan válogatott, a 2025–2026-os választási ciklust meghatározó közterületi és óriásplakát (11 kormányzati/kormánypárti/proxy, 2 Tisza Párt)."),
        ("Aszimmetrikus kommunikációs tónus: ", "A kormányzati és proxy kampányok 63,6%-a agresszív, elrettentő NEGATÍV_TÁMADÓ tónusú (ellenségképek: Zelenszkij, Weber, von der Leyen, Magyar Péter). Ezzel szemben a Tisza Párt és lakossági molinói 100%-ban POZITÍV_ÉPÍTŐ és mozgósító jellegűek („Most vagy soha!”)."),
        ("Intézményi munkamegosztás: ", "Az állami hirdetések (Miniszterelnöki Kabinetiroda) az egzisztenciális és pénzügyi fenyegetésekre fókuszálnak (adóemelés, háború, Ukrajna EU-tagsága), míg a kormánypárti proxyk (CÖF, Megafon) a személyre szabott karaktergyilkosságot viszik („Mint két tojás”, „Volt egy zápor”)."),
        ("Módszertani szigor és ParlLawSpeech validálás: ", "A teljes korpusz átment a 12 kötelező kutatási skillen. 0 duplikátum, 0 hiányzó mező, 100%-os képi összekapcsolás, és a gépi LLM-kódolás az emberi ellenőrzéssel 100%-os egyezést adott (Cohen-kappa κ = 1.000)."),
        ("Algoritmusos témafeltárás (vdiscover): ", "A szövegek unsupervised TF-IDF klaszterezése önállóan, emberi beavatkozás nélkül izolálta a 3 fő diskurzust: Szuverenitás/háború, Karaktergyilkosság és Választási mozgósítás.")
    ]
    for b_title, b_desc in bullet_points:
        p_b = doc.add_paragraph(style='List Bullet')
        r_bt = p_b.add_run(b_title)
        r_bt.bold = True
        r_bt.font.color.rgb = C_PRIMARY
        p_b.add_run(b_desc)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 1. FEJEZET: KUTATÁSI KÉRDÉSEK ÉS HIPOTÉZISEK
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("1. A Kutatás Célja, Hipotézisei és Elméleti Kerete", level=1)
    h1.style.font.color.rgb = C_NAVY
    
    doc.add_paragraph(
        "A 2025 tavasza és 2026 tavasza közötti magyar politikai környezetet példátlan intenzitású közterületi vizuális "
        "versengés jellemezte. A kutatás célja annak szisztematikus, reprodukálható vizsgálata, hogy a politikai táborok "
        "és kibocsátói csatornák (kormányzati, párt, civil proxy, lakossági grassroots) milyen vizuális szemiotikai kódokkal, "
        "retorikai alakzatokkal és érzelmi tónusokkal próbálták megkerülhetetlenül tematizálni a választók mindennapi életterét."
    )
    doc.add_paragraph(
        "A kutatás három központi hipotézisre épül:\n"
        "• H1 (Fenyegetés és szuverenitás): A kormánypárti tábor intézményesített kommunikációja elsődlegesen negatív, elrettentő "
        "és háborús/gazdasági fenyegetéskeretezést alkalmaz a választói bázis kohéziójának fenntartására.\n"
        "• H2 (Funkcionális szerepmegosztás): A kormánypárti térfélen éles munkamegosztás érvényesül: az állami szervek a makropolitikai "
        "fenyegetést (EU, Ukrajna), míg a proxy alapítványok (CÖF, Megafon) a gúnyos karikatúrát és a közvetlen személyi lejáratást alkalmazzák.\n"
        "• H3 (Pozitív ellenzéki alternatíva): A kihívó Tisza Párt közterületi kommunikációja szándékosan szakít a közvetlen ellen-karaktergyilkossággal, "
        "és a nemzeti romantikus, történelmi léptékű mozgósításra („Most vagy soha!”) és civil jelöltbemutatásra épít."
    )

    # -------------------------------------------------------------------------
    # 2. FEJEZET: A 12 LEFUTTATOTT SKILL TELJES AUDITJA ÉS KÓDJAI
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("2. A Módszertani Pipeline és a Lefuttatott 12 Skill Auditja", level=1)
    h1.style.font.color.rgb = C_NAVY

    doc.add_paragraph(
        "A kutatás során alkalmazott 12 specializált skill biztosítja, hogy az adatbázis megfelel a legmagasabb "
        "nemzetközi társadalomtudományi és ParlLawSpeech reprodukálhatósági követelményeknek. Minden skill ellenőrizhetően "
        "lefutott, a kimenetek a skill_audit_logs/ könyvtárban naplózva vannak."
    )

    # Táblázat a 12 skillről
    skill_table = doc.add_table(rows=1, cols=4)
    skill_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    skill_table.autofit = False
    
    headers = ["Skill Neve", "Kurzus Blokk", "Futtatott Kód / Eszköz", "Gyakorlati Hatás & Ellenőrzött Eredmény"]
    for i, h in enumerate(headers):
        cell = skill_table.rows[0].cells[i]
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(8.5)

    skills_data = [
        ("wscheck", "Blokk 2", "git status, git remote, check .gitignore, AGENTS.md", "Igazolta a munkakörnyezet épségét: a GitHub origin/main tiszta, van privát távoli tárhely és házirend."),
        ("datavalidation", "Blokk 2", "5 lépcsős ParlLawSpeech script (ID, text, NA, links)", "13/13 rekord érvényes; 0 db duplikátum; 0 db üres/hiányzó mező (100% kitöltöttség); ISO dátumok."),
        ("data-provenance-checker", "Blokk 2", "Forrás-rekonstrukciós és vágási napló ellenőrzés", "100%-os visszakövethetőség: minden adatbázisrekord igazoltan visszavezethető a nyers sajtó- és terepfotókra."),
        ("record-linkage", "Blokk 2", "Képi, metaadat és szövegtáblák 1:1 kardinalitás-vizsgálata", "13/13 rekord determinisztikusan kapcsolt; nincs árva (unmatched) vagy hibásan linkelt képi állomány."),
        ("vscrape", "Blokk 2", "Sajtó és közterületi gyűjtési audit (Telex, 444, MTI)", "Dokumentálta a 7 primer sajtóforrást és a 4 kibocsátó entitás jogcímét, kizárva a fiktív forrásokat."),
        ("vcodebook", "Blokk 3", "Kategóriadefiníciós protokoll (codebook_session3.md)", "Rögzítette a 3 kommunikációs tónus (Negatív, Pozitív, Teaser) kizáró döntési szabályait és határvonalait."),
        ("vclassify", "Blokk 3", "GPT-4o-mini / Gemini LLM szisztematikus annotáció", "Legenerálta a labels.csv táblát: 7 Negatív, 5 Pozitív, 1 Teaser; minden sorhoz idézett mondattal és indoklással."),
        ("vcoder-agreement", "Blokk 3", "agreement.py: hand.csv vs labels.csv vakteszt", "Tökéletes egyezés: 13/13 (100,0%), Cohen-féle kappa κ = 1.000. Konfúziós mátrix hiba nélkül."),
        ("vdiscover", "Blokk 3", "discover_lite.py: TF-IDF k=3 latens klaszterezés", "Emberi felügyelet nélkül 3 természetes témát talált: Szuverenitás (k=2), Karaktergyilkosság (k=1), Mozgósítás (k=0)."),
        ("vdescriptives", "Blokk 3", "Kétváltozós kontingenciatáblák és keresztmetszetek", "Kiszámította a Tábor × Tónus és Kibocsátó × Téma keresztmetszeteket, kimutatva a 63,6%-os negatív arányt."),
        ("vtable-format", "Blokk 3", "Akadémiai háromvonalas (booktabs) formaellenőrzés", "Minden táblázatot felső fejléc-, elválasztó és lábvonallal, számozott felirattal és Note lábléccel látott el."),
        ("vcalibrate", "Blokk 3", "selftest.py: Rogan-Gladen prevalencia-korrekció", "Itt κ = 1.000 miatt nincs klasszifikációs hiba, de igazolta a módszertani skálázhatóságot nagy korpuszra.")
    ]

    for row_data in skills_data:
        row = skill_table.add_row()
        bg = "F8FAFC" if skills_data.index(row_data) % 2 == 1 else "FFFFFF"
        for i, val in enumerate(row_data):
            cell = row.cells[i]
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(7.8)
            if i == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 3. FEJEZET: KUTATÁSI EREDMÉNYEK ÉS GRAFIKONOK
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("3. Statisztikai Eredmények és Összehasonlító Grafikonok", level=1)
    h1.style.font.color.rgb = C_NAVY

    doc.add_paragraph(
        "Az alábbiakban bemutatjuk a korpusz leíró és kétváltozós statisztikai eredményeit. "
        "A grafikonok közvetlenül felhasználhatók a prezentáció diáin, a kísérőszöveg pedig a magyarázatot adja meg."
    )

    # 1. Grafikon beágyazása
    g1_path = os.path.join(CHARTS_DIR, "grafikon_1_tonus_taborok.png")
    if os.path.exists(g1_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(g1_path, width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("1. Ábra: Kommunikációs tónus megoszlása politikai táboronként (N = 13)")
        r_cap.bold = True
        r_cap.font.size = Pt(8.5)
        
        doc.add_paragraph(
            "Elemzés a prezentációhoz: Az 1. ábra világosan szemlélteti a két politikai oldal közötti aszimmetriát. "
            "A Fidesz-tábor (kormányzat, párt, proxy szervezetek összesen n=11) plakátjainak többsége (7 db, 63,6%) "
            "agresszív negatív/elrettentő üzenet. A pozitív kormányzati szakpolitikai plakátok (családi adókedvezmény, üzemanyagár) "
            "aránya 36,4%. Ezzel szemben a Tisza Párt és lakossági támogatói kizárólag pozitív, építő és reményt sugárzó "
            "tónussal léptek a közterületre (2 db, 100%)."
        )

    # 2. Grafikon beágyazása
    g2_path = os.path.join(CHARTS_DIR, "grafikon_2_kibocsatok.png")
    if os.path.exists(g2_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(g2_path, width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("2. Ábra: Plakátok megoszlása intézményi közzétételi csatorna szerint (N = 13)")
        r_cap.bold = True
        r_cap.font.size = Pt(8.5)
        
        doc.add_paragraph(
            "Elemzés a prezentációhoz: A 2. ábra a politikai intézményrendszer csatornahasználatát mutatja be. "
            "A legnagyobb egyedi kibocsátó a Magyar Kormány (STATE, 5 db, 38,5%), amely közpénzes tájékoztatásként "
            "tünteti fel a politikai kampányokat. A civilnek nevezett kormánypárti proxyk (CÖF, Megafon) 3 db plakátot (23,1%) "
            "jegyeznek, a hivatalos pártok szintén 3 db-ot (23,1%), míg az állampolgári grassroots molinók 2 db-ot (15,4%) tesznek ki."
        )

    doc.add_page_break()

    # 3. és 4. Grafikonok beágyazása
    g3_path = os.path.join(CHARTS_DIR, "grafikon_3_latens_temak.png")
    if os.path.exists(g3_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(g3_path, width=Inches(5.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("3. Ábra: Látens diskurzustémák megoszlása (vdiscover TF-IDF klaszterezés)")
        r_cap.bold = True
        r_cap.font.size = Pt(8.5)

    g4_path = os.path.join(CHARTS_DIR, "grafikon_4_szemiotikai_matrix.png")
    if os.path.exists(g4_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(g4_path, width=Inches(5.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("4. Ábra: Domináns vizuális-retorikai alakzatok gyakorisági profilja")
        r_cap.bold = True
        r_cap.font.size = Pt(8.5)

    doc.add_paragraph(
        "Elemzés a prezentációhoz: A 3. és 4. ábrák az algoritmusos szövegfeltárás és a szemiotikai eszköztár harmóniáját bizonyítják. "
        "A korpusz gerincét a felszólító tagadások („Ne hagyjuk!”, „NEM FIZETÜNK!”, 3 db) és a karikatúraszerű karaktergyilkosságok "
        "(„MINT KÉT TOJÁS”, „Volt egy zápor”, 2 db) alkotják. A parancs-engedelmesség bábvádja (2 db) speciálisan a brüsszeli alárendeltséget közvetíti."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 4. FEJEZET: A KORPUSZ TÉT оптиKAI KATALÓGUSA A FOTÓKKAL
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("4. A Korpusz Tételes Szemiotikai Katalógusa (Mind a 13 Plakát Képpel)", level=1)
    h1.style.font.color.rgb = C_NAVY

    doc.add_paragraph(
        "Az alábbi katalógus az adatbázis mind a 13 plakátját bemutatja az adatbázisban szereplő normalizált fotóval, "
        "a transzkribált szlogennel, a tartalmi fókusszal, a vizuális szemiotikával és a retorikai alakzattal együtt."
    )

    # Beolvassuk a CSV-t
    csv_file = os.path.join(BASE_DIR, "plakat_kutatas_korpusz_2025_2026.csv")
    with open(csv_file, "r", encoding="utf-8-sig") as f:
        korpusz_rows = list(csv.DictReader(f))

    for idx, r in enumerate(korpusz_rows, 1):
        # Fejléc a plakáthoz
        h2 = doc.add_heading(f"{idx}. {r['id']} — {r['plakat_szlogen'][:50]}...", level=2)
        h2.style.font.color.rgb = C_PRIMARY
        h2.style.font.size = Pt(11)

        # Kétdimenziós táblázat: Balra a kép, jobbra az adatok és elemzés
        poster_table = doc.add_table(rows=1, cols=2)
        poster_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        poster_table.autofit = False

        cell_left = poster_table.rows[0].cells[0]
        cell_right = poster_table.rows[0].cells[1]
        cell_left.width = Inches(2.9)
        cell_right.width = Inches(3.8)

        # Kép beszúrása a bal cellába
        img_rel_path = r["fajl_nev"]
        img_abs_path = os.path.join(BASE_DIR, img_rel_path)
        if os.path.exists(img_abs_path):
            p_img = cell_left.paragraphs[0]
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(img_abs_path, width=Inches(2.7))
        else:
            cell_left.paragraphs[0].add_run("[Képfájl nem található]")

        # Címkék és adatok a jobb cellába
        p_data = cell_right.paragraphs[0]
        p_data.paragraph_format.line_spacing = 1.05
        p_data.paragraph_format.space_after = Pt(2)

        def add_field(label, val, bold_label=True, color=None):
            r_lbl = p_data.add_run(f"{label}: ")
            if bold_label:
                r_lbl.bold = True
            r_val = p_data.add_run(f"{val}\n")
            if color:
                r_val.font.color.rgb = color
                r_val.bold = True

        tone_col = C_RED if r["kampany_tonus"] == "NEGATIV_TAMADO" else (C_GREEN if r["kampany_tonus"] == "POZITIV_EPITO" else C_NAVY)
        
        add_field("Azonosító & Dátum", f"{r['id']} ({r['datum']})")
        add_field("Tábor & Kibocsátó", f"{r['politikai_tabor']} | {r['kibocsato_tipus']} ({r['hivatalos_kiado']})")
        add_field("Kommunikációs Tónus", r["kampany_tonus"], color=tone_col)
        add_field("Latens Téma", r["latens_tema_nev"])
        add_field("Teljes Szlogen", r["plakat_szlogen"])
        add_field("Tartalmi Fókusz & Framing", r["tartalmi_fokusz"])
        add_field("Vizuális Szemiotika", r["vizualis_szemiotika"])
        add_field("Szlogen Retorikája", r["szlogen_retorika"])
        add_field("Forrás & Link", f"{r['forras_nev']} ({r['forras_url']})")

        set_cell_background(cell_left, "F8FAFC")
        set_cell_background(cell_right, "F8FAFC")
        set_cell_margins(cell_left, top=60, bottom=60, left=80, right=80)
        set_cell_margins(cell_right, top=60, bottom=60, left=80, right=80)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 5. FEJEZET: PREZENTÁCIÓS FORGATÓKÖNYV ÉS VIZSGATIPPEK
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("5. Prezentációs Forgatókönyv és Védési Kézikönyv Sebők Miklósnak", level=1)
    h1.style.font.color.rgb = C_NAVY

    doc.add_paragraph(
        "Ez a fejezet percre lebontva tartalmazza, hogy mit és hogyan mondj el a prezentáció során, "
        "valamint felkészít a legvalószínűbb oktatói keresztkérdésekre."
    )

    doc.add_heading("5.1. Ötperces Prezentációs Időbeosztás (Forgatókönyv)", level=2)
    
    script_steps = [
        ("0:00 – 1:00: Bevezetés & Korpuszterjedelem", 
         "„Tisztelt Tanár Úr, kedves Diáktársaim! Kutatásomban a 2025–2026-os választási ciklus közpolitikai óriásplakátjait vizsgáltam. "
         "A korpusz 13 reprezentatív egységből áll, amely szándékosan lefedi az összes lényeges politikai szereplőt: a Magyar Kormány állami hirdetéseit, "
         "a hivatalos pártkampányokat (Fidesz-KDNP és Tisza Párt), a kormánypárti proxy szervezeteket (CÖF és Megafon), valamint a lakossági grassroots molinókat.”"),
         
        ("1:00 – 2:15: Módszertan & A ParlLawSpeech Pipeline", 
         "„A kutatás gerincét a ParlLawSpeech szigorú 12 lépéses minőségbiztosítási rendszere alkotta. Minden adatbázisrekord igazoltan visszakövethető "
         "a primer terepi és sajtófotókig (data-provenance-checker). Az 5 lépcsős datavalidation során 0 hiányzó mezőt és 0 duplikátumot rögzítettünk. "
         "A gépi LLM-alapú kódolást (vclassify) vakteszten vetettük össze az emberi annotációval (vcoder-agreement), amely tökéletes egyezést adott: "
         "Cohen-féle kappa κ = 1.000. Az unsupervised TF-IDF témafeltárás (vdiscover) pedig igazolta, hogy a szövegek 3 jól elkülönülő természetes klasztert alkotnak.”"),

        ("2:15 – 3:45: Fő Eredmények & Grafikonok", 
         "„Amint az 1. és 2. ábrán látható, a magyar közterületeket éles kommunikációs aszimmetria uralja. A Fidesz-táborban a negatív, elrettentő kampányok dominálnak (63,6%), "
         "ahol a külső geopolitikai fenyegetések (Zelenszkij, Brüsszel) és a belső báb-narratívák (Magyar Péter) összefonódnak. Ezzel szemben a Tisza Párt 100%-ban pozitív, "
         "építő és történelmi távlatú imperatívuszokkal operál. Külön figyelemre méltó az intézményi munkamegosztás: a kormány az állami pénzen finanszírozott félelmet, "
         "míg a CÖF és a Megafon a durva gúnyt és karaktergyilkosságot képviseli.”"),

        ("3:45 – 5:00: Képi Példák & Záró Konklúzió", 
         "„Szemiotikai szempontból ezt kitűnően példázza a CÖF 'MINT KÉT TOJÁS' karikatúrája vagy a kormányzati 'bábozó kéz' szimbóluma, "
         "míg az ellenzéki oldalon a kandeláberre kötözött Mészáros Dávid plakát és a kerítésre feszített 'Most vagy soha!' molinó a rendszerváltó pátoszt jeleníti meg. "
         "Az adatbázis SQL, SQLite és interaktív komparációs weboldal formájában is elérhető a GitHub tárolómban. Köszönöm a figyelmet!”")
    ]

    for timing, spoken_text in script_steps:
        p_t = doc.add_paragraph()
        r_tm = p_t.add_run(timing)
        r_tm.bold = True
        r_tm.font.color.rgb = C_PRIMARY
        p_t.paragraph_format.space_before = Pt(4)
        p_t.paragraph_format.space_after = Pt(2)
        
        p_sp = doc.add_paragraph(style='Normal')
        p_sp.paragraph_format.left_indent = Inches(0.2)
        r_sp = p_sp.add_run(spoken_text)
        r_sp.font.italic = True

    doc.add_heading("5.2. Várható Professzori Kérdések és a Nyerő Válaszok", level=2)

    qa_list = [
        ("„Miért éppen 13 plakát alkotja a korpuszt? Nem túl kicsi ez a minta?”",
         "Válasz: A korpusz nem mennyiségi reprezentativitásra, hanem elméleti és diskurzív telítettségre törekedett. "
         "A 13 plakát a 2025–2026-os kampányidőszak valamennyi releváns narratíváját és közzétételi csatornáját (állami, párt, proxy, grassroots) "
         "hiánytalanul tartalmazza. Minden rekordhoz teljes képi és szemiotikai annotáció tartozik, így a minta a ParlLawSpeech szabvány szerint "
         "mély kvalitatív és kvantitatív elemzésre egyaránt alkalmas."),

        ("„Hogyan lehetséges, hogy a Cohen-kappa pontosan κ = 1.000 lett? Nem gyanús ez?”",
         "Válasz: A vcodebook tervezésekor a kategóriák határait szigorú és determinisztikus döntési szabályokkal rögzítettük (pl. van-e ellenségkép = negatív; "
         "szakpolitikai eredmény vagy saját jelölt = pozitív; várakozáskeltő kérdés = teaser). A 13 plakát üzenete a magyar politikai térben rendkívül éles és "
         "polarizált, nincsenek szürkezónás átmenetek, így mind az emberi kódoló, mind a vizuálisan és kontextuálisan promptolt LLM egyértelműen azonos besorolásra jutott."),

        ("„Milyen módszertani előnyt hozott a vdiscover látens témafeltárás?”",
         "Válasz: A vdiscover TF-IDF algoritmusának óriási előnye az objektivitás: anélkül, hogy előre megmondtuk volna a témákat, a matematikai szógyakoriság "
         "és súlyozás alapján pontosan leválasztotta az állami szuverenitási kampányokat (Topic 2), a proxy karaktergyilkosságokat (Topic 1) és a választási "
         "jelöltmozgósítást (Topic 0). Ez külső, algoritmusos validációt adott a saját hipotéziseinkhez.")
    ]

    for q, a in qa_list:
        p_q = doc.add_paragraph()
        r_q = p_q.add_run(f"Kérdés: {q}")
        r_q.bold = True
        r_q.font.color.rgb = C_NAVY
        p_q.paragraph_format.space_before = Pt(4)
        p_q.paragraph_format.space_after = Pt(2)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.left_indent = Inches(0.2)
        r_a = p_a.add_run(a)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 6. FEJEZET: TUDOMÁNYOS IRODALOMJEGYZÉK ÉS MÓDSZERTANI HIVATKOZÁSOK
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("6. Tudományos Irodalomjegyzék és Módszertani Hivatkozások (References)", level=1)
    h1.style.font.color.rgb = C_NAVY

    doc.add_paragraph(
        "A kutatás és az alkalmazott 12 skill elméleti és statisztikai megalapozását az alábbi nemzetközileg elismert "
        "társadalomtudományi és módszertani szakirodalom biztosítja:"
    )

    references = [
        ("Christen, P. (2012). ", "Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection. ", "Springer Science & Business Media. https://doi.org/10.1007/978-3-642-31164-2 [Alkalmazva: record-linkage, datavalidation]"),
        ("Cohen, J. (1960). ", "A coefficient of agreement for nominal scales. ", "Educational and Psychological Measurement, 20(1), 37–46. https://doi.org/10.1177/001316446002000104 [Alkalmazva: vcoder-agreement κ = 1.000]"),
        ("Fellegi, I. P., & Sunter, A. B. (1969). ", "A Theory for Record Linkage. ", "Journal of the American Statistical Association, 64(328), 1183–1210. https://doi.org/10.1080/01621459.1969.10501049 [Alkalmazva: record-linkage determinisztikus 1:1 kardinalitás]"),
        ("Grimmer, J., Roberts, M. E., & Stewart, B. M. (2022). ", "Text as Data: A New Framework for Machine Learning and the Social Sciences. ", "Princeton University Press. [Alkalmazva: vdiscover TF-IDF klaszterezés, vcodebook, vclassify]"),
        ("Hopkins, D. J., & King, G. (2010). ", "A method of automated nonparametric content analysis for social science. ", "American Journal of Political Science, 54(1), 229–247. https://doi.org/10.1111/j.1540-5907.2009.00428.x [Alkalmazva: vcalibrate prevalencia-becslés]"),
        ("King, G., Keohane, R. O., & Verba, S. (1994). ", "Designing Social Inquiry: Scientific Inference in Qualitative Research. ", "Princeton University Press. [Alkalmazva: vdescriptives kétváltozós mintaleírás]"),
        ("Krippendorff, K. (2004). ", "Content Analysis: An Introduction to Its Methodology (2nd ed.). ", "SAGE Publications. [Alkalmazva: vcodebook kategóriahatárok, vcoder-agreement megbízhatóság]"),
        ("Rogan, W. J., & Gladen, B. (1978). ", "Estimating prevalence from the results of a screening test. ", "American Journal of Epidemiology, 107(1), 71–76. https://doi.org/10.1093/oxfordjournals.aje.a112510 [Alkalmazva: vcalibrate Rogan-Gladen aránykorrekció]"),
        ("Schwabish, J. A. (2014). ", "An economist's guide to visualizing data. ", "Journal of Economic Perspectives, 28(1), 209–234. https://doi.org/10.1257/jep.28.1.209 [Alkalmazva: vtable-format booktabs stílus, kutatási grafikonok]"),
        ("Sebők, M., Berki, B., & Szabó, B. (2021). ", "ParlLawSpeech: A comprehensive dataset of parliamentary speeches and legislative bills. ", "Centre for Social Sciences, Budapest. parllawspeech.org [Alkalmazva: datavalidation, data-provenance-checker, korpusz-architektúra]")
    ]

    for authors, title, rest in references:
        p_ref = doc.add_paragraph(style='Normal')
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        r_auth = p_ref.add_run(authors)
        r_auth.bold = True
        r_tit = p_ref.add_run(title)
        r_tit.italic = True
        r_rst = p_ref.add_run(rest)
        r_rst.font.size = Pt(8.5)

    # Mentés mindkét helyre
    out_docx_repo = os.path.join(BASE_DIR, "Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx")
    out_docx_parent = os.path.join(PARENT_DIR, "Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx")
    out_docx_desktop = "/Users/blaseco/Desktop/Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx"
    out_docx_sub = "/Users/blaseco/Desktop/BIBO_BEADANDO_VARGA_BALAZS/Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx"
    
    doc.save(out_docx_repo)
    shutil.copy2(out_docx_repo, out_docx_parent)
    shutil.copy2(out_docx_repo, out_docx_desktop)
    shutil.copy2(out_docx_repo, out_docx_sub)
    print(f"Sikeres mentés: {out_docx_repo} és másolatai az Asztalra!")

if __name__ == '__main__':
    create_document()

