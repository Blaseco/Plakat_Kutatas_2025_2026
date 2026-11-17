#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibrate.py — Apply Rogan & Gladen (1978) measurement error correction
to raw classifier prevalence before regression or population inference (/vcalibrate).
"""

import sys
import argparse

def rogan_gladen(p_raw, se, sp):
    """
    Rogan & Gladen (1978) estimator:
    P* = (P_raw + Sp - 1) / (Se + Sp - 1)
    """
    denom = se + sp - 1.0
    if abs(denom) < 1e-6:
        raise ValueError("Classifier is uninformative: Se + Sp - 1 = 0")
    p_adj = (p_raw + sp - 1.0) / denom
    # Bound within [0, 1]
    return max(0.0, min(1.0, p_adj))

def run_calibration(p_raw, se=1.0, sp=1.0):
    print("=" * 68)
    print(" ROGAN-GLADEN MEASUREMENT ERROR CORRECTION (/vcalibrate)")
    print("=" * 68)
    print(f"Observed Raw Prevalence (P_raw): {p_raw*100:.2f}%")
    print(f"Classifier Sensitivity (Se):     {se:.4f}")
    print(f"Classifier Specificity (Sp):     {sp:.4f}")

    p_adj = rogan_gladen(p_raw, se, sp)
    print(f"Corrected Prevalence (P*):       {p_adj*100:.2f}%")
    bias = (p_raw - p_adj) * 100
    print(f"Classifier Distortion Removed:   {bias:+.2f} percentage points")
    print("=" * 68)
    return p_adj

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Apply Rogan-Gladen correction.")
    parser.add_argument("--p-raw", type=float, required=True, help="Raw observed prevalence (0 to 1)")
    parser.add_argument("--se", type=float, default=1.0, help="Classifier sensitivity on gold sample (0 to 1)")
    parser.add_argument("--sp", type=float, default=1.0, help="Classifier specificity on gold sample (0 to 1)")
    args = parser.parse_args()

    run_calibration(args.p_raw, args.se, args.sp)
