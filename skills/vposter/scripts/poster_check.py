#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poster_check.py — Verify the integrity of a political poster corpus.
Checks completeness, ID uniqueness, required metadata fields, and image existence.
"""

import sys
import os
import csv
import argparse

def check_corpus(csv_path, images_dir=None):
    if not os.path.exists(csv_path):
        print(f"[-] ERROR: Corpus CSV not found: {csv_path}", file=sys.stderr)
        return False

    required_fields = ['id', 'politikai_tabor', 'kampany_tonus', 'plakat_szlogen']
    records = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    n = len(records)
    print(f"[+] Loaded {n} billboard records from {csv_path}")

    # 1. Uniqueness of ID
    ids = [r.get('id', '').strip() for r in records]
    if len(set(ids)) != n:
        print(f"[-] ERROR: Duplicate IDs detected! Unique: {len(set(ids))}, Total: {n}", file=sys.stderr)
        return False
    print(f"[+] IDs are unique: {n}/{n}")

    # 2. Required fields completeness
    missing = {k: 0 for k in required_fields}
    for r in records:
        for k in required_fields:
            if not r.get(k) or r.get(k).strip() == '':
                missing[k] += 1

    has_missing = any(v > 0 for v in missing.values())
    if has_missing:
        print(f"[-] ERROR: Missing values in required fields: {missing}", file=sys.stderr)
        return False
    print(f"[+] No missing values in primary fields (100% completeness)")

    # 3. Image file existence check
    if images_dir and os.path.exists(images_dir):
        missing_images = 0
        for r in records:
            img_rel = r.get('fajl_nev', '')
            if img_rel:
                # Check directly or relative to images_dir
                img_name = os.path.basename(img_rel)
                p1 = os.path.join(images_dir, img_name)
                p2 = os.path.join(os.path.dirname(csv_path), img_rel)
                if not os.path.exists(p1) and not os.path.exists(p2):
                    print(f"[-] Warning: Image file not found for ID {r['id']}: {img_name}")
                    missing_images += 1
        if missing_images == 0:
            print(f"[+] All referenced image files verified on disk.")
        else:
            print(f"[-] Warning: {missing_images} image files could not be located.")

    print("[+] CORPUS CHECK PASSED.")
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Verify political poster corpus integrity.")
    parser.add_argument("csv_path", help="Path to corpus CSV file")
    parser.add_argument("--images-dir", help="Directory where poster images are stored", default=None)
    args = parser.parse_args()

    ok = check_corpus(args.csv_path, args.images_dir)
    sys.exit(0 if ok else 1)
