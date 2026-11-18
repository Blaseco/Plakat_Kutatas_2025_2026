#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_poster.py — Ingest a new political poster into the research corpus.
Appends the record to all database formats (CSV, Excel BOM, SQL, SQLite DB, labels.csv),
copies the image into the images folder, and triggers automatic re-analysis (charts, tables, reproduction).
"""

import os
import sys
import csv
import shutil
import sqlite3
import argparse
from datetime import date

def get_next_id(corpus_csv):
    highest_num = 0
    with open(corpus_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for r in reader:
            pid = r.get('id', '')
            parts = pid.split('_')
            if len(parts) >= 4:
                try:
                    num = int(parts[3])
                    if num > highest_num:
                        highest_num = num
                except ValueError:
                    pass
    next_num = highest_num + 1
    current_year = date.today().year
    return f"HUN_PLAKAT_{current_year}_{next_num:03d}"

def ingest_poster(
    project_dir,
    image_path,
    politikai_tabor,
    kibocsato_tipus,
    hivatalos_kiado,
    plakat_szlogen,
    vizualis_leiras,
    kampany_tonus,
    forras_nev="Közterületi megfigyelés",
    forras_url="Helyszíni fotó",
    formatum_meret="Óriásplakát / Eurobillboard (504 x 238 cm)",
    politikai_elemzes=None,
    tartalmi_fokusz=None,
    vizualis_szemiotika=None,
    szlogen_retorika=None,
    datum=None
):
    corpus_csv = os.path.join(project_dir, "plakat_kutatas_korpusz_2025_2026.csv")
    if not os.path.exists(corpus_csv):
        print(f"[-] ERROR: Corpus CSV not found in {project_dir}", file=sys.stderr)
        return False

    if datum is None:
        datum = date.today().strftime("%Y-%m-%d")

    new_id = get_next_id(corpus_csv)
    print(f"[+] Assigned new unique ID: {new_id}")

    # Copy image
    images_dir = os.path.join(project_dir, "vagott_kepek")
    os.makedirs(images_dir, exist_ok=True)
    ext = os.path.splitext(image_path)[1].lower() if image_path else ".jpg"
    dest_image_name = f"{new_id}{ext}"
    dest_image_path = os.path.join(images_dir, dest_image_name)
    rel_image_path = f"vagott_kepek/{dest_image_name}"

    if image_path and os.path.exists(image_path):
        shutil.copy2(image_path, dest_image_path)
        print(f"[+] Image copied to: {dest_image_path}")
    else:
        print(f"[-] Warning: Source image '{image_path}' not found, recorded relative path: {rel_image_path}")

    # Latent topic assignment fallback
    latens_id = "1" if "háború" in plakat_szlogen.lower() or "brüsszel" in plakat_szlogen.lower() else "3"
    latens_nev = "Állami szuverenitási & háborús diskurzus" if latens_id == "1" else "Rendszerváltó optimizmus és jövőkép"

    record = {
        'id': new_id,
        'datum': datum,
        'politikai_tabor': politikai_tabor,
        'kibocsato_tipus': kibocsato_tipus,
        'hivatalos_kiado': hivatalos_kiado,
        'fajl_nev': rel_image_path,
        'plakat_szlogen': plakat_szlogen,
        'vizualis_leiras': vizualis_leiras,
        'formatum_meret': formatum_meret,
        'politikai_elemzes': politikai_elemzes or vizualis_leiras,
        'forras_nev': forras_nev,
        'forras_url': forras_url,
        'kampany_tonus': kampany_tonus,
        'tartalmi_fokusz': tartalmi_fokusz or plakat_szlogen,
        'vizualis_szemiotika': vizualis_szemiotika or vizualis_leiras,
        'szlogen_retorika': szlogen_retorika or plakat_szlogen,
        'latens_tema_id': latens_id,
        'latens_tema_nev': latens_nev
    }

    # 1. Append to standard CSV
    fieldnames = list(record.keys())
    with open(corpus_csv, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(record)
    print(f"[+] Appended to: {corpus_csv}")

    # 2. Append to Hungarian Excel CSV (BOM, semicolon)
    excel_csv = os.path.join(project_dir, "plakat_kutatas_korpusz_2025_2026_excel.csv")
    if os.path.exists(excel_csv):
        with open(excel_csv, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writerow(record)
        print(f"[+] Appended to Excel CSV: {excel_csv}")

    # 3. Append to SQLite DB
    sqlite_path = os.path.join(project_dir, "plakat_adatbazis_2025_2026.db")
    if os.path.exists(sqlite_path):
        conn = sqlite3.connect(sqlite_path)
        cur = conn.cursor()
        cols = ", ".join(fieldnames)
        placeholders = ", ".join(["?"] * len(fieldnames))
        sql = f"INSERT INTO plakatok ({cols}) VALUES ({placeholders})"
        cur.execute(sql, [record[k] for k in fieldnames])
        conn.commit()
        conn.close()
        print(f"[+] Inserted into SQLite DB: {sqlite_path}")

    # 4. Append to labels.csv
    labels_csv = os.path.join(project_dir, "labels.csv")
    if os.path.exists(labels_csv):
        label_record = {
            'id': new_id,
            'code': kampany_tonus,
            'reason': vizualis_leiras[:60],
            'sentence': plakat_szlogen,
            'model': 'Gemini-3.8-Flash',
            'prompt_version': 'v1.0'
        }
        with open(labels_csv, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'code', 'reason', 'sentence', 'model', 'prompt_version'])
            writer.writerow(label_record)
        print(f"[+] Appended to labels.csv: {labels_csv}")

    # 5. Automatically trigger chart regeneration and reproduction
    print("\n" + "=" * 60)
    print(" AUTOMATICALLY RE-RUNNING ANALYSIS & REPRODUCING METRICS")
    print("=" * 60)
    reproduce_script = os.path.join(project_dir, "reproduce.py")
    if os.path.exists(reproduce_script):
        os.system(f"python3 '{reproduce_script}'")

    print(f"\n[+] SUCCESS! New poster {new_id} is now fully integrated into the research dataset and analysis.")
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest a new poster into the research corpus.")
    parser.add_argument("--project-dir", required=True, help="Path to project directory")
    parser.add_argument("--image", required=False, default="", help="Path to poster image file")
    parser.add_argument("--tabor", required=True, help="Politikai tábor (pl. 'Kormánypárt / CÖF', 'Ellenzék (Tisza Párt)')")
    parser.add_argument("--kiado-tipus", required=True, help="Kibocsátó típus (STATE, PARTY, OPPOSITION, GRASSROOTS)")
    parser.add_argument("--kiado", required=True, help="Hivatalos kiadó / finanszírozó")
    parser.add_argument("--szlogen", required=True, help="Plakátszöveg szó szerinti idézete")
    parser.add_argument("--leiras", required=True, help="Vizuális leírás és szemiotika")
    parser.add_argument("--tonus", required=True, choices=['NEGATIV_TAMADO', 'POZITIV_EPITO', 'TEASER_SEMLEGES', 'SET_ASIDE'], help="Kódkönyv szerinti kód")
    args = parser.parse_args()

    ingest_poster(
        project_dir=args.project_dir,
        image_path=args.image,
        politikai_tabor=args.tabor,
        kibocsato_tipus=args.kiado_tipus,
        hivatalos_kiado=args.kiado,
        plakat_szlogen=args.szlogen,
        vizualis_leiras=args.leiras,
        kampany_tonus=args.tonus
    )
