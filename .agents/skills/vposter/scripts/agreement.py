#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agreement.py — Compute inter-coder reliability (Cohen's Kappa), confusion matrix,
and per-category precision/recall between human gold standard and machine labels.
"""

import sys
import os
import csv
import argparse

def compute_agreement(hand_csv, labels_csv):
    if not os.path.exists(hand_csv) or not os.path.exists(labels_csv):
        print("[-] ERROR: hand_csv or labels_csv not found!", file=sys.stderr)
        return False

    hand = {}
    with open(hand_csv, 'r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            hand[r['id'].strip()] = r['code'].strip()

    labels = {}
    with open(labels_csv, 'r', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            labels[r['id'].strip()] = r['code'].strip()

    matched_ids = sorted(list(set(hand.keys()) & set(labels.keys())))
    n = len(matched_ids)
    if n == 0:
        print("[-] ERROR: No matching IDs found!", file=sys.stderr)
        return False

    categories = sorted(list(set(hand.values()) | set(labels.values())))
    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}

    agreements = 0
    mismatches = []
    for uid in matched_ids:
        h = hand[uid]
        m = labels[uid]
        matrix[h][m] += 1
        if h == m:
            agreements += 1
        else:
            mismatches.append((uid, h, m))

    p_o = agreements / n
    p_e = 0.0
    for c in categories:
        r_sum = sum(matrix[c][c2] for c2 in categories)
        c_sum = sum(matrix[c1][c] for c1 in categories)
        p_e += (r_sum / n) * (c_sum / n)

    kappa = (p_o - p_e) / (1.0 - p_e) if (1.0 - p_e) != 0 else 1.0

    print("=" * 68)
    print(" INTER-CODER RELIABILITY & AGREEMENT REPORT (/vcoder-agreement)")
    print("=" * 68)
    print(f"Matched units: {n} · Observed agreement (p_o): {p_o*100:.2f}% · Cohen's Kappa: {kappa:.4f}")
    print("\n--- CONFUSION MATRIX (Rows: Hand Gold Standard, Cols: Machine) ---")
    hdr = f"{'Category':<18} | " + " | ".join(f"{c[:10]:<10}" for c in categories) + " | Total"
    print(hdr)
    print("-" * len(hdr))
    for c1 in categories:
        vals = [f"{matrix[c1][c2]:<10}" for c2 in categories]
        tot = sum(matrix[c1][c2] for c2 in categories)
        print(f"{c1:<18} | " + " | ".join(vals) + f" | {tot}")

    print("\n--- PER-CATEGORY METRICS ---")
    print(f"{'Category':<18} | {'Base (n)':<10} | {'Precision':<10} | {'Recall':<10} | {'F1':<10}")
    print("-" * 65)
    for c in categories:
        tp = matrix[c][c]
        fp = sum(matrix[o][c] for o in categories if o != c)
        fn = sum(matrix[c][o] for o in categories if o != c)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        tot = sum(matrix[c][c2] for c2 in categories)
        print(f"{c:<18} | {tot:<10} | {prec:<10.2f} | {rec:<10.2f} | {f1:<10.2f}")

    if mismatches:
        print(f"\nMismatches ({len(mismatches)}):")
        for uid, h, m in mismatches:
            print(f"  Unit {uid}: hand={h} vs machine={m}")
    else:
        print("\nMismatches: 0 (Flawless agreement)")
    print("=" * 68)
    return kappa >= 0.80

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate Cohen's Kappa and confusion matrix.")
    parser.add_argument("hand_csv", help="Path to hand.csv")
    parser.add_argument("labels_csv", help="Path to labels.csv")
    args = parser.parse_args()

    ok = compute_agreement(args.hand_csv, args.labels_csv)
    sys.exit(0 if ok else 1)
