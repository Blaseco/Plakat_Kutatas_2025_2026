# vposter — Multimodal Political Campaign Poster Analysis (Vanilla)

The shareable, agent-neutral recipe for collecting, cataloging, classifying, and validating political campaign posters and outdoor advertisements into a reproducible research dataset and report.

Part of the **Bibó AI 2026 / poltextLAB** quantitative political text analysis curriculum (Dr. Miklós Sebők).

## Features
- **Multimodal corpus integrity check** (`poster_check.py`): IDs, missing data, and image links.
- **Inter-coder agreement** (`agreement.py`): Blind hand vs machine labels, Cohen's kappa ($\kappa$), confusion matrix.
- **Academic descriptives** (`descriptives.py`): Three-line booktabs Table 1 and distributions.
- **Measurement error correction** (`calibrate.py`): Rogan–Gladen (1978) prevalence correction.
- **Self-test suite** (`selftest.py`): Synthetic test verifying the entire pipeline.

## Usage
Type `/vposter` in Antigravity or run the scripts from the command line:
```bash
python3 scripts/selftest.py
python3 scripts/poster_check.py corpus.csv --images-dir vagott_kepek/
python3 scripts/agreement.py hand.csv labels.csv
python3 scripts/descriptives.py corpus.csv
python3 scripts/calibrate.py --p-raw 0.538 --se 1.0 --sp 1.0
```
