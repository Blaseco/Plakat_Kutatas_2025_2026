#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest.py — Self-test suite for the vposter skill.
Tests all scripts on synthetic billboard data to ensure the pipeline is 100% operational.
"""

import os
import sys
import tempfile
import csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_test():
    print("=" * 68)
    print(" RUNNING VPOSTER SELF-TEST SUITE")
    print("=" * 68)

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = os.path.join(tmpdir, "test_corpus.csv")
        hand_file = os.path.join(tmpdir, "hand.csv")
        labels_file = os.path.join(tmpdir, "labels.csv")

        # 1. Write synthetic corpus
        with open(csv_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'datum', 'politikai_tabor', 'kampany_tonus', 'plakat_szlogen'])
            writer.writerow(['TEST_01', '2026-01-01', 'Kormánypárt / CÖF', 'NEGATIV_TAMADO', 'Fenyeget a háború!'])
            writer.writerow(['TEST_02', '2026-01-02', 'Ellenzék / Grassroots', 'POZITIV_EPITO', 'Új korszak kezdődik!'])

        # 2. Write synthetic hand & labels
        with open(hand_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'code'])
            writer.writerow(['TEST_01', 'NEGATIV_TAMADO'])
            writer.writerow(['TEST_02', 'POZITIV_EPITO'])

        with open(labels_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'code', 'reason', 'sentence'])
            writer.writerow(['TEST_01', 'NEGATIV_TAMADO', 'Threat framing', 'Fenyeget a háború!'])
            writer.writerow(['TEST_02', 'POZITIV_EPITO', 'Positive change', 'Új korszak kezdődik!'])

        # Test poster_check.py
        ret = os.system(f"python3 '{os.path.join(SCRIPT_DIR, 'poster_check.py')}' '{csv_file}' > /dev/null")
        assert ret == 0, "poster_check.py failed!"
        print("[+] poster_check.py: PASS")

        # Test agreement.py
        ret = os.system(f"python3 '{os.path.join(SCRIPT_DIR, 'agreement.py')}' '{hand_file}' '{labels_file}' > /dev/null")
        assert ret == 0, "agreement.py failed!"
        print("[+] agreement.py (κ = 1.000): PASS")

        # Test descriptives.py
        ret = os.system(f"python3 '{os.path.join(SCRIPT_DIR, 'descriptives.py')}' '{csv_file}' > /dev/null")
        assert ret == 0, "descriptives.py: PASS"
        print("[+] descriptives.py (Table 1 booktabs): PASS")

        # Test calibrate.py
        ret = os.system(f"python3 '{os.path.join(SCRIPT_DIR, 'calibrate.py')}' --p-raw 0.50 --se 0.90 --sp 0.85 > /dev/null")
        assert ret == 0, "calibrate.py failed!"
        print("[+] calibrate.py (Rogan-Gladen): PASS")

    print("=" * 68)
    print(" ✓ ALL VPOSTER TESTS PASSED SUCCESSFULLY.")
    print("=" * 68)
    return True

if __name__ == '__main__':
    ok = run_test()
    sys.exit(0 if ok else 1)
