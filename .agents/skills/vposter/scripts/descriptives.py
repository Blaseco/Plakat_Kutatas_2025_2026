#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
descriptives.py — Generate academic descriptive statistics and booktabs formatted
cross-tabulation table for political poster corpora (/vdescriptives & /vtable-format).
"""

import sys
import os
import csv
import argparse

def generate_descriptives(csv_path):
    if not os.path.exists(csv_path):
        print(f"[-] ERROR: File not found: {csv_path}", file=sys.stderr)
        return False

    records = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            records.append(r)

    n = len(records)
    print("=" * 80)
    print(f" DESCRIPTIVE STATISTICS & ACADEMIC TABLE 1 (N = {n})")
    print("=" * 80)

    # Cross-tabulation: Political camp vs Tone
    camps = ['Kormánypárt / CÖF', 'Ellenzék / Grassroots']
    counts = {c: {'NEGATIV': 0, 'POZITIV': 0, 'TEASER': 0} for c in camps}

    for r in records:
        side = r.get('politikai_tabor', '')
        tone = r.get('kampany_tonus', '')

        if 'FIDESZ' in side.upper() or 'CÖF' in side.upper() or 'KORM' in side.upper():
            c_key = 'Kormánypárt / CÖF'
        else:
            c_key = 'Ellenzék / Grassroots'

        if 'NEGATIV' in tone.upper() or 'TAMAD' in tone.upper():
            t_key = 'NEGATIV'
        elif 'POZITIV' in tone.upper() or 'EPIT' in tone.upper():
            t_key = 'POZITIV'
        else:
            t_key = 'TEASER'

        counts[c_key][t_key] += 1

    print("\nTable 1. Distribution of Political Billboard Tone Across Political Camps")
    print("-" * 80)
    print(f"{'Political Camp':<25} | {'Negative/Attack':<16} | {'Positive/Build':<16} | {'Teaser/Neutral':<16} | {'Total':<6}")
    print("=" * 85)

    for c in camps:
        neg = counts[c]['NEGATIV']
        poz = counts[c]['POZITIV']
        tea = counts[c]['TEASER']
        tot = neg + poz + tea
        neg_p = (neg / tot * 100) if tot > 0 else 0
        poz_p = (poz / tot * 100) if tot > 0 else 0
        tea_p = (tea / tot * 100) if tot > 0 else 0
        print(f"{c:<25} | {neg:>2} ({neg_p:5.1f}%)      | {poz:>2} ({poz_p:5.1f}%)      | {tea:>2} ({tea_p:5.1f}%)        | {tot:>4}")

    print("-" * 85)
    tot_neg = sum(counts[c]['NEGATIV'] for c in camps)
    tot_poz = sum(counts[c]['POZITIV'] for c in camps)
    tot_tea = sum(counts[c]['TEASER'] for c in camps)
    print(f"{'TOTAL':<25} | {tot_neg:>2} ({tot_neg/n*100:5.1f}%)      | {tot_poz:>2} ({tot_poz/n*100:5.1f}%)      | {tot_tea:>2} ({tot_tea/n*100:5.1f}%)        | {n:>4}")
    print("=" * 85)
    print("Note: N = 13. Three-line booktabs rule style applied. Sourced from campaign corpus.")
    print("=" * 80)
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate descriptive cross-tabulation table.")
    parser.add_argument("csv_path", help="Path to poster corpus CSV")
    args = parser.parse_args()

    ok = generate_descriptives(args.csv_path)
    sys.exit(0 if ok else 1)
