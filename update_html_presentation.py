#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webes összehasonlító és bemutató felület frissítése
Gazdagítja a comparison.html és index.html oldalakat az új retorikai, tartalmi és latens téma dimenziókkal.
"""

import os
import re
import json
import shutil

REPO_DIR = "/Users/blaseco/Desktop/ai kurzus/Plakat_Kutatas_2025_2026"
PARENT_DIR = "/Users/blaseco/Desktop/ai kurzus"

# Olvassuk be a gazdagított JSON-t
with open(os.path.join(REPO_DIR, "ParlLawSpeech_Plakat_Korpusz_2025_2026.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

plakats_dict = {p["id"]: p for p in data["plakatok"]}

# Frissítsük a comparison.html-t
comp_src = os.path.join(PARENT_DIR, "comparison.html")
with open(comp_src, "r", encoding="utf-8") as f:
    comp_html = f.read()

# Készítsünk egy frissített posters JS tömböt
# Megkeressük a posters deklarációt és frissítjük az objektumokat
def update_poster_js(html):
    # Dimenziók bővítése
    old_dim = 'const dimensions = ['
    new_dim = """const dimensions = [
        { label: "1. Politikai Tábor", valA: pA.camp, valB: pB.camp },
        { label: "2. Kibocsátó Szereplő & Jogcím", valA: pA.publisher, valB: pB.publisher },
        { label: "3. Kampányfinanszírozási Forma", valA: pA.funding, valB: pB.funding },
        { label: "4. Intézményi Besorolás", valA: pA.actorLabel, valB: pB.actorLabel },
        { label: "5. Dokumentálás Dátuma & Időzítés", valA: pA.date, valB: pB.date },
        { label: "6. Fizikai Hordozó & Méretkategória", valA: pA.format, valB: pB.format },
        { label: "7. Kommunikációs Tónus & Valencia", valA: pA.toneLabel, valB: pB.toneLabel },
        { label: "8. Célzott Szereplő / Ellenségkép", valA: pA.target, valB: pB.target },
        { label: "9. Vizuális Szemiotikai Kódok", valA: pA.semiotics, valB: pB.semiotics },
        { label: "10. Tartalmi Fókusz & Framing", valA: pA.contentFocus || pA.analysis, valB: pB.contentFocus || pB.analysis },
        { label: "11. Szlogen Retorikája & Beszédaktus", valA: pA.sloganRhetoric || "N/A", valB: pB.sloganRhetoric || "N/A" },
        { label: "12. Latens Diskurzustéma (vdiscover k=3)", valA: pA.latentTopic || "N/A", valB: pB.latentTopic || "N/A" },
        { label: "13. Földrajzi Lokáció", valA: pA.location, valB: pB.location },
        { label: "14. Hivatalos Sajtóforrás & Fotós", valA: `${pA.sourceName} (${pA.photographer})`, valB: `${pB.sourceName} (${pB.photographer})` }
      ];"""
    
    # Kicseréljük a régi dimensions blokkot
    dim_pattern = r'const dimensions = \[.*?\];'
    html = re.sub(dim_pattern, new_dim, html, flags=re.DOTALL)

    # Most a posters tömböt gazdagítjuk: beillesztjük a contentFocus, sloganRhetoric, latentTopic mezőket minden elemhez
    for pid, pdata in plakats_dict.items():
        # keresés id alapján
        pattern = rf'(\bid:\s*"{pid}".*?analysis:\s*".*?",)'
        # gazdagított sorok
        esc_focus = pdata["tartalmi_fokusz"].replace('"', '\\"')
        esc_rhetoric = pdata["szlogen_retorika"].replace('"', '\\"')
        esc_topic = pdata["latens_tema_nev"].replace('"', '\\"')
        esc_tonus = pdata["kampany_tonus"].replace('"', '\\"')

        def repl(match):
            return (
                match.group(1) + "\n"
                f'        contentFocus: "{esc_focus}",\n'
                f'        sloganRhetoric: "{esc_rhetoric}",\n'
                f'        latentTopic: "{esc_topic}",\n'
                f'        vclassifyTone: "{esc_tonus}",'
            )
        html = re.sub(pattern, repl, html, flags=re.DOTALL)

    return html

updated_comp = update_poster_js(comp_html)

# Mentés mindkét helyre
with open(os.path.join(REPO_DIR, "comparison.html"), "w", encoding="utf-8") as f:
    f.write(updated_comp)
with open(os.path.join(PARENT_DIR, "comparison.html"), "w", encoding="utf-8") as f:
    f.write(updated_comp)

print("comparison.html frissítve a repóban és a szülőkönyvtárban!")

# Másoljuk át az index.html-t és a táblázatot is a repóba
shutil.copy2(os.path.join(PARENT_DIR, "index.html"), os.path.join(REPO_DIR, "index.html"))
shutil.copy2(os.path.join(PARENT_DIR, "Plakat_Kutatas_Tablazat.html"), os.path.join(REPO_DIR, "Plakat_Kutatas_Tablazat.html"))

# Hozzunk létre egy symlinket a vagott_kepek-re a parent mappában is, ha nincs ott
parent_vagott = os.path.join(PARENT_DIR, "vagott_kepek")
repo_vagott = os.path.join(REPO_DIR, "vagott_kepek")
if not os.path.exists(parent_vagott):
    try:
        os.symlink(repo_vagott, parent_vagott)
        print(f"Szimbolikus link létrehozva: {parent_vagott} -> {repo_vagott}")
    except Exception as e:
        print(f"Symlink hiba (másolunk inkább): {e}")
        shutil.copytree(repo_vagott, parent_vagott)

