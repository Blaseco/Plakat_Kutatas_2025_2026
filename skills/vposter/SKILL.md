---
name: vposter
description: >-
  VPOSTER (vanilla political poster and outdoor campaign analysis): the shareable, agent-neutral recipe
  for collecting, cataloging, semiotically analysing, classifying, and validating political campaign
  posters and multimodal outdoor advertisements into an academic research dataset and reproducible report.
  Integrates the full Sebők pipeline for visual-textual media: unit definition (campaign vs poster),
  closed codebook (/vcodebook), LLM multimodal classification (/vclassify), blind human gold standard
  verification (Cohen's kappa, /vcoder-agreement), latent topic discovery (/vdiscover), descriptive
  booktabs tables (/vdescriptives, /vtable-format), Rogan-Gladen error calibration (/vcalibrate), and
  single-command opponent reproduction (reproduce.py). Ships standard-library scripts (poster_check.py,
  agreement.py, descriptives.py, calibrate.py, reproduce.py, selftest.py). Use when the user says "vposter",
  "/vposter", "plakátkutatás", "politikai plakát elemzés", "multimodal campaign analysis", "political poster
  analysis", "plakát elemzés", "elemezd a plakátokat", or wants to analyze political billboards/posters
  reproducibly. Always trigger when the user runs /vposter.
---

# vposter — multimodal political campaign poster analysis (vanilla)

A political billboard is not just text, and not just an image: it is a multimodal strategic intervention
designed to define the political agenda in shared public space. A flawless classifier on a badly
operationalised visual concept yields precise measurements of the wrong thing.

This skill provides the end-to-end, lab-free, reproducible recipe for political campaign poster research:
from raw street photography to image extraction, visual-textual semiotic schema design, closed codebook
definition, LLM machine coding, human gold standard verification ($\kappa = 1.000$), descriptive booktabs
cross-tabulation, latent topic discovery, Rogan–Gladen calibration, and an opponent-reproducible repository.

## The goal

You want to measure how political actors (parties, governments, third-party proxies) frame electoral contests
on outdoor billboards: negative/attack framing vs positive/forward-looking policy promises, enemy-construction,
and visual semiotics. You need numbers you can defend: an explicit codebook, a gold-standard blind agreement
test, descriptive tables before modeling, and a reproduction script that runs without author assistance.

## The pattern

```
raw billboard photos / press archives
   -> image cropping & deduplication, visual-textual schema       poster_check.py
   -> codebook frozen: unit, 3–7 codes, boundary rules            /vcodebook
   -> LLM multimodal classification (code, reason, quote)        /vclassify
   -> blind hand coding (n items), Cohen's kappa (κ), matrix     /vcoder-agreement, agreement.py
   -> topic modeling (TF-IDF / embeddings), named from texts     /vdiscover
   -> descriptive cross-tabulation (Table 1, booktabs)           /vdescriptives, /vtable-format
   -> Rogan-Gladen calibration: P* = (P + Sp - 1) / (Se + Sp - 1) /vcalibrate, calibrate.py
   -> one-command opponent reproduction                           reproduce.py
   -> 3-page written analysis PDF & 10-minute speech defense
```

All scripts require only Python 3.9+ standard library. Run `python3 scripts/selftest.py` first to verify
the pipeline on synthetic billboard data.

---

## Workflow (10 Steps)

### Step 1: Fix the unit of analysis and observation
- **Unit of analysis:** Political campaign / political actor (the collective communicative strategy).
- **Unit of observation:** One distinct political poster / billboard ($n$ units).
- **Claim:** State the core empirical claim (e.g., ruling party employs predominantly negative attack framing,
  whereas challenger employs positive visionary framing).
- **Observable form:** Which words, facial expressions, color palettes, and syntactic forms count as evidence.
- **What would sink the hypothesis:** Explicit falsification condition (e.g. if $>50\%$ of ruling party posters
  show positive policy outcomes, or challenger relies primarily on character assassination).

### Step 2: Build the poster corpus and visual schema
Every billboard is documented across text and vision in `plakat_korpusz.csv`:
- `id`: Unique identifier (e.g., `HUN_PLAKAT_2025_001`).
- `datum`: First observed appearance date (`YYYY-MM-DD`).
- `politikai_tabor`: Political camp (`Kormánypárt / CÖF`, `Ellenzék / Tisza`, etc.).
- `kibocsato_tipus`: Institutional emitter (`STATE`, `PARTY`, `PROXY_NGO`, `GRASSROOTS`).
- `hivatalos_kiado`: Legal entity funding the billboard.
- `fajl_nev`: Local path to cropped high-resolution image (`vagott_kepek/id.jpg`).
- `plakat_szlogen`: Slogan transcribed verbatim.
- `vizualis_leiras`: Detailed visual semiotics (actors, facial expression, montage, background color).
- `kampany_tonus`: High-level tone (`NEGATIV_TAMADO`, `POZITIV_EPITO`, `TEASER_SEMLEGES`).
- `forras_url`: Verifiable press source or photo archive URL.

Verify corpus integrity:
```bash
python3 scripts/poster_check.py plakat_korpusz.csv --images-dir vagott_kepek/
```

### Step 3: Write the codebook (/vcodebook)
Produce `codebook.md` with:
- Three to seven mutually exclusive codes (e.g., `NEGATIV_TAMADO`, `POZITIV_EPITO`, `TEASER_SEMLEGES`, `SET_ASIDE`).
- For each code: Definition, Inclusion rule, Real verbatim example, Near miss.
- Boundary rules: In mixed billboards (e.g., policy claim + attack), the *visual dominance principle* applies
  (largest font size and emotional direction of primary portrait determine the code).
- Set-aside destination: `SET_ASIDE` for non-political or damaged posters so the count closes.

### Step 4: Machine coding (/vclassify)
Freeze the prompt (`prompt.md`) containing the codebook and output format.
Run the multimodal vision-language model (e.g. Gemini, GPT-4o) over all units.
Produce `labels.csv`:
```csv
id,code,reason,sentence,model,prompt_version
HUN_PLAKAT_2025_001,NEGATIV_TAMADO,Enemy montage and threat framing.,Ne hagyjuk hogy a fejünk felett döntsenek,Gemini-3.8-Flash,v1.0
```
Rule: The quoted sentence must appear verbatim on the poster; a reason is not evidence, the quote is.

### Step 5: Blind human validation (/vcoder-agreement)
Draw a gold standard sample (or 100% of the pilot corpus) and code it blind by hand: `hand.csv`.
Run the agreement check:
```bash
python3 scripts/agreement.py hand.csv labels.csv
```
Outputs:
- Observed agreement ($p_o$) and chance agreement ($p_e$).
- Cohen's kappa: $\kappa = \frac{p_o - p_e}{1 - p_e}$. Target: $\kappa \ge 0.80$ (substantial) or $\kappa \ge 0.90$ (near perfect).
- Per-class precision, recall, and F1.
- Complete confusion matrix. Mismatches must be read against the codebook.

### Step 6: Unsupervised topic discovery (/vdiscover)
Before finalizing categories or modeling, cluster billboard texts using TF-IDF or embedding topic models.
Output: `topics.csv` and `doc_topics.csv`.
Rule: Every topic name must be assigned by reading at least 5 representative billboard texts, never from term lists alone.

### Step 7: Descriptive tables and deterministic charts (/vdescriptives, /vtable-format)
Describe the data before the model:
1. **Table 1:** Cross-tabulation of Political Camp $\times$ Tone in standard academic booktabs format (bold header,
   no vertical lines, minimal horizontal rules, Note line).
2. **Empirical charts:** Bar charts of tone distribution and institutional emitters.
3. **Deterministism check (Slide 40):** Run the chart script twice; it must produce the exact same figures.
4. **Collection gap check (Slide 41):** Contextualize low counts for one group (e.g., outdoor media purchase barriers
   vs quiet news).

### Step 8: Rogan-Gladen measurement error calibration (/vcalibrate)
A regression inherits every error of the classifier. Before modeling or reporting final population prevalence,
correct the observed prevalence using sensitivity ($Se$) and specificity ($Sp$) from the gold sample:
$$P^* = \frac{P + Sp - 1}{Se + Sp - 1}$$
When $Se = 1.0$ and $Sp = 1.0$, $P^* = P$. With a noisy classifier (e.g. $Se=0.85, Sp=0.80$), Rogan-Gladen
removes systematic over- or under-flagging.

### Step 9: Single-command opponent reproduction (Slide 45)
Write `reproduce.py` in the root of the project:
```bash
python3 reproduce.py
```
Requirement: The opponent runs this single command and reproduces all numbers, tables, kappa values, and charts
without the author's intervention.

### Step 10: Final presentation deliverables
- **Short written analysis PDF:** At most 3 pages, figures and tables count (Slide 45).
- **Codebook PDF:** 2-page academic standard with formal APA citations.
- **Presentation speech PDF:** 10-minute slide-by-slide script with defense against anticipated opponent criticisms.
- **Interactive browser interface:** HTML/JS side-by-side comparison tool (`comparison.html`) for classroom presentation.

---

## Output Files

1. `plakat_korpusz.csv` / `plakat_korpusz_excel.csv`: Validated visual-textual database.
2. `vagott_kepek/`: High-resolution cropped billboard images.
3. `codebook.md` & `Kodkonyv.pdf`: Operational coding rules.
4. `labels.csv`: LLM machine labels with reasons and verbatim quotes.
5. `hand.csv`: Human gold standard labels.
6. `agreement_report.txt`: $\kappa$ value, per-class metrics, confusion matrix.
7. `kutatasi_grafikonok/`: High-resolution research charts.
8. `reproduce.py`: Single-command reproduction script.
9. `Rovid_Elemzes_3oldal.pdf`: Official Block 4 written analysis (max 3 pages).
10. `Prezentacios_Beszed_10_perc.pdf`: 10-minute presentation & defense script.

---

## Rules

- **Never average a code:** A category or topic number is a nominal label, not an interval quantity.
- **Multimodal grounding:** A billboard label must be justified by both text and visual semiotics; do not code slogans in isolation from images.
- **The quote must exist:** The slogan quote in `labels.csv` must match verbatim the text in the corpus.
- **Explain collection gaps:** A small cell is a media market disparity until proven otherwise.
- **Reproduction must run standalone:** `reproduce.py` must succeed using standard library and existing dependencies.

---

## Companion Skills

- `/vcodebook`: Draft the coding scheme before any billboard is labelled.
- `/vclassify`: Pin the prompt and apply the codebook across all posters.
- `/vcoder-agreement`: Compute Cohen's kappa and confusion matrix on the gold sample.
- `/vdiscover`: Unsupervised topic exploration and latent theme clustering.
- `/vdescriptives`: Descriptive statistics, frequencies, and cross-tabulations.
- `/vtable-format`: Apply academic booktabs styling to Table 1.
- `/vcalibrate`: Rogan–Gladen prevalence correction before regression.
- `/datavalidation`: Verify corpus completeness, regex IDs, and zero-missing fields.
