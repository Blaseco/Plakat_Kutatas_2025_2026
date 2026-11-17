#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kutatási és összehasonlító grafikonok generálása
Projekt: Magyar Közpolitikai Plakátkorpusz (2025–2026)
Készítő: Varga Balázs | Bibó István Szakkollégium
"""

import os
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

BASE_DIR = "/Users/blaseco/Desktop/ai kurzus/Plakat_Kutatas_2025_2026"
CHARTS_DIR = os.path.join(BASE_DIR, "kutatasi_grafikonok")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Betöltjük az adatokat
csv_path = os.path.join(BASE_DIR, "plakat_kutatas_korpusz_2025_2026.csv")
with open(csv_path, "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

# Beállítások
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

# -----------------------------------------------------------------------------
# 1. GRAFIKON: Kampánytónus megoszlása politikai táboronként
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)

camps = ["FIDESZ-TÁBOR", "TISZA PÁRT"]
tones = ["NEGATIV_TAMADO", "POZITIV_EPITO", "TEASER_SEMLEGES"]
tone_labels = ["Negatív / Támadó", "Pozitív / Építő", "Teaser / Semleges"]
colors_palette = ["#EF4444", "#10B981", "#64748B"]

data = np.zeros((len(camps), len(tones)))
for r in rows:
    c_idx = camps.index(r["politikai_tabor"])
    t_idx = tones.index(r["kampany_tonus"])
    data[c_idx, t_idx] += 1

x = np.arange(len(camps))
width = 0.24

for i, (tone_name, col) in enumerate(zip(tone_labels, colors_palette)):
    rects = ax.bar(x + (i - 1) * width, data[:, i], width, label=tone_name, color=col, edgecolor='none', zorder=3)
    for rect in rects:
        h = rect.get_height()
        if h > 0:
            ax.annotate(f"{int(h)} db",
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

ax.set_ylabel("Plakátok száma (db)", fontsize=10, fontweight='bold', color='#1E293B')
ax.set_title("1. Ábra: Kommunikációs tónus megoszlása politikai táboronként (N = 13)", fontsize=12, fontweight='bold', pad=14, color='#0F172A')
ax.set_xticks(x)
ax.set_xticklabels(["Fidesz-tábor (Kormányzat + Párt + CÖF/Megafon)\n[n = 11]", "Tisza Párt (Párt + Grassroots lakossági)\n[n = 2]"], fontsize=10, fontweight='medium')
ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
ax.set_ylim(0, 8.5)

fig.text(0.12, 0.02, "Forrás: Magyar Közpolitikai Plakátkorpusz (2025–2026) · ParlLawSpeech módszertani audit", fontsize=7.5, color='#64748B')
plt.tight_layout()
p1 = os.path.join(CHARTS_DIR, "grafikon_1_tonus_taborok.png")
plt.savefig(p1, bbox_inches='tight')
plt.close()
print(f"Mentve: {p1}")

# -----------------------------------------------------------------------------
# 2. GRAFIKON: Kibocsátói csatornák és jogállások megoszlása
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

channels = ["STATE\n(Állami hirdetés)", "PROXY\n(CÖF & Megafon)", "PARTY\n(Pártjelölt)", "GRASSROOTS\n(Lakossági molinó)"]
counts = [5, 3, 3, 2]
bar_colors = ["#2563EB", "#DC2626", "#EA580C", "#059669"]

bars = ax.bar(channels, counts, color=bar_colors, width=0.45, zorder=3)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f"{yval} db ({yval/13*100:.1f}%)", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0F172A')

ax.set_ylabel("Plakátok száma (db)", fontsize=10, fontweight='bold', color='#1E293B')
ax.set_title("2. Ábra: Plakátok megoszlása intézményi közzétételi csatorna szerint (N = 13)", fontsize=12, fontweight='bold', pad=14, color='#0F172A')
ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
ax.set_ylim(0, 6.2)
fig.text(0.12, 0.02, "Megjegyzés: STATE = Kormányzati közpénzes tájékoztatás; PROXY = Kormánypárti civil/alapítványi proxyk.", fontsize=7.5, color='#64748B')
plt.tight_layout()
p2 = os.path.join(CHARTS_DIR, "grafikon_2_kibocsatok.png")
plt.savefig(p2, bbox_inches='tight')
plt.close()
print(f"Mentve: {p2}")

# -----------------------------------------------------------------------------
# 3. GRAFIKON: vdiscover TF-IDF Látens Diskurzustémák Eloszlása
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=300)

topics = [
    "1. Téma: Állami szuverenitási &\nháborús diskurzus (5 db)",
    "2. Téma: Proxy karaktergyilkosság &\nbáb-narratíva (3 db)",
    "3. Téma: Választási jelöltállítás &\nmozgósítás (5 db)"
]
shares = [5, 3, 5]
pie_colors = ["#1E3A8A", "#B91C1C", "#0D9488"]

wedges, texts, autotexts = ax.pie(
    shares, labels=topics, autopct='%1.1f%%',
    startangle=140, colors=pie_colors,
    wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2),
    pctdistance=0.75, textprops={'fontsize': 8.5, 'color': '#0F172A', 'fontweight': 'medium'}
)
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(9.5)
    at.set_fontweight('bold')

ax.set_title("3. Ábra: Látens diskurzustémák aránya a korpuszban (vdiscover k=3 klaszterezés)", fontsize=11, fontweight='bold', pad=12, color='#0F172A')
plt.tight_layout()
p3 = os.path.join(CHARTS_DIR, "grafikon_3_latens_temak.png")
plt.savefig(p3, bbox_inches='tight')
plt.close()
print(f"Mentve: {p3}")

# -----------------------------------------------------------------------------
# 4. GRAFIKON: Szemiotikai és Retorikai Eszköztár Profil
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)

devices = [
    "Felszólító tagadás / kollektív dac\n(„Ne hagyjuk!”, „NEM FIZETÜNK!”)",
    "Karikatúra / gúnyos metafora\n(„MINT KÉT TOJÁS”, „Volt egy zápor”)",
    "Parancs-engedelmesség bábvád\n(„ADÓEMELÉST! – IGENIS!”)",
    "Kormányzati szakpolitikai siker\n(Családi adókedvezmény, üzemanyagár)",
    "Hivatalos jelölti stabilitás\n(„A BIZTOS VÁLASZTÁS”, Berkó Attila)",
    "Ellenzéki alternatíva & imperatívusz\n(„TISZA 2026”, „Most vagy soha!”)"
]
counts_dev = [3, 2, 2, 2, 2, 2]
y_pos = np.arange(len(devices))

bars = ax.barh(y_pos, counts_dev, color='#3B82F6', height=0.55, edgecolor='none', zorder=3)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.08, bar.get_y() + bar.get_height()/2.0, f"{int(w)} db", ha='left', va='center', fontsize=9, fontweight='bold', color='#1E293B')

ax.set_yticks(y_pos)
ax.set_yticklabels(devices, fontsize=8.5, color='#1E293B')
ax.invert_yaxis()  # Legfelső legyen az első
ax.set_xlabel("Előfordulási gyakoriság (db)", fontsize=9.5, fontweight='bold', color='#1E293B')
ax.set_title("4. Ábra: Domináns vizuális-retorikai alakzatok a korpuszban", fontsize=11.5, fontweight='bold', pad=12, color='#0F172A')
ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
ax.set_xlim(0, 3.8)

plt.tight_layout()
p4 = os.path.join(CHARTS_DIR, "grafikon_4_szemiotikai_matrix.png")
plt.savefig(p4, bbox_inches='tight')
plt.close()
print(f"Mentve: {p4}")

print("Minden kutatási grafikon sikeresen legenerálva!")
