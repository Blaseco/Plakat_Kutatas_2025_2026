#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beadandó Dokumentumok Összegyűjtése és Kihelyezése az Asztalra (Desktop)
Projekt: Magyar Közpolitikai Plakátkorpusz (2025–2026)
Készítő: Varga Balázs | Bibó István Szakkollégium
Kurzus: Mesterséges intelligencia a társadalom- és politikatudományi kutatásban (Sebők Miklós)
"""

import os
import shutil

DESKTOP_DIR = "/Users/blaseco/Desktop"
SUBMISSION_DIR = os.path.join(DESKTOP_DIR, "BIBO_BEADANDO_VARGA_BALAZS")
REPO_DIR = "/Users/blaseco/Desktop/ai kurzus/Plakat_Kutatas_2025_2026"

os.makedirs(SUBMISSION_DIR, exist_ok=True)

# Másolandó fájlok listája
files_to_copy = [
    # 1. Hivatalos 2 oldalas Kódkönyv PDF
    "Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf",
    # 2. Kibővített részletes fotós kódkönyv PDF
    "ParlLawSpeech_Plakat_Korpusz_Codebook_2025_2026.pdf",
    # 3. Prezentációs mesterdokumentáció Word formátumban (.docx)
    "Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx",
    # 4. Adatbázisok (CSV, Excel CSV, SQL, SQLite, JSON)
    "plakat_kutatas_korpusz_2025_2026.csv",
    "plakat_kutatas_korpusz_2025_2026_excel.csv",
    "plakat_adatbazis_2025_2026.sql",
    "plakat_adatbazis_2025_2026.db",
    "ParlLawSpeech_Plakat_Korpusz_2025_2026.json",
    # 5. Interaktív webes bemutatók
    "comparison.html",
    "index.html",
    # 6. Audit jegyzőkönyv és AI nyilatkozat
    "OSSZES_SKILL_ELLENORZESI_JEGYZOKONYV.md",
    "AI_Nyilatkozat_Varga_Balazs_2025_2026.pdf"
]

print("1. Fájlok másolása a dedikált BIBO_BEADANDO_VARGA_BALAZS mappába...")
for fname in files_to_copy:
    src = os.path.join(REPO_DIR, fname)
    if os.path.exists(src):
        dst = os.path.join(SUBMISSION_DIR, fname)
        shutil.copy2(src, dst)
        print(f" [OK] {fname} -> {dst}")
    else:
        print(f" [HIÁNYZIK] {fname}")

# Mappák másolása (képek és grafikonok)
dirs_to_copy = ["vagott_kepek", "kutatasi_grafikonok", "skill_audit_logs"]
for dname in dirs_to_copy:
    src_d = os.path.join(REPO_DIR, dname)
    dst_d = os.path.join(SUBMISSION_DIR, dname)
    if os.path.exists(src_d):
        if os.path.exists(dst_d):
            shutil.rmtree(dst_d)
        shutil.copytree(src_d, dst_d)
        print(f" [OK Mappa] {dname}/ másolva -> {dst_d}")

# 2. Közvetlen asztali elhelyezés a legfontosabb beadandó fájlokból
print("\n2. Kulcsfájlok másolása közvetlenül a Desktop gyökerébe...")
desktop_direct_files = [
    "Kodkonyv_Plakatkutatas_2025_2026_Varga_Balazs.pdf",
    "Prezentacio_es_Mesterdokumentacio_Plakatkutatas_2025_2026_Varga_Balazs.docx",
    "plakat_kutatas_korpusz_2025_2026_excel.csv",
    "plakat_adatbazis_2025_2026.sql",
    "comparison.html"
]

for fname in desktop_direct_files:
    src = os.path.join(REPO_DIR, fname)
    if os.path.exists(src):
        dst = os.path.join(DESKTOP_DIR, fname)
        shutil.copy2(src, dst)
        print(f" [OK Desktop] {fname} -> {dst}")

print("\nMinden dokumentum sikeresen kihelyezve az Asztalra!")
