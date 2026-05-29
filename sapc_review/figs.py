# -*- coding: utf-8 -*-
"""
Original schematic figures for the SAPC reliability literature-review chapter.
All figures are ORIGINAL drawings created with matplotlib (no copyrighted
content is reproduced). In-figure text is kept in English to avoid CJK glyph
issues; figure captions in the Word document are in Chinese.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.linewidth": 0.8,
    "savefig.dpi": 200,
    "figure.dpi": 200,
})

C_ANODE = "#9fb6cd"
C_OXIDE = "#e8c46a"
C_POLY = "#7fb77e"
C_GRAPH = "#5a5a5a"
C_AG = "#c9c9c9"
C_MOLD = "#d9c7b8"
C_BLUE = "#2b6cb0"
C_RED = "#c0392b"
C_GREEN = "#2e7d32"
C_GRAY = "#555555"


def _save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_structure():
    """Cross-section schematic of a stacked (multilayer) aluminum solid capacitor."""
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # One capacitor element (zoom) on the left
    ax.text(2.6, 7.5, "Single capacitor element (zoom)", ha="center", fontsize=10, weight="bold")
    layers = [
        ("Etched Al anode foil", C_ANODE, 1.0),
        ("Al2O3 dielectric (oxide)", C_OXIDE, 0.32),
        ("Conductive polymer (PEDOT) cathode", C_POLY, 0.55),
        ("Graphite layer", C_GRAPH, 0.30),
        ("Ag paste (cathode contact)", C_AG, 0.40),
    ]
    y = 4.2
    for name, col, h in layers:
        ax.add_patch(Rectangle((0.6, y), 4.0, h, facecolor=col, edgecolor="k", lw=0.8))
        ax.text(4.75, y + h / 2, name, va="center", fontsize=8.2)
        y += h + 0.06
    # mirror oxide+poly+graphite+ag below the foil to show both surfaces
    ax.text(2.6, 4.05, "(porous etched surface, ~100x area gain)", ha="center", fontsize=7.2, style="italic", color=C_GRAY)

    # Stacked elements (right)
    ax.text(7.7, 7.5, "Stacked / laminated package", ha="center", fontsize=10, weight="bold")
    bx = 6.2
    for i in range(5):
        yy = 2.2 + i * 0.62
        ax.add_patch(Rectangle((bx, yy), 2.9, 0.5, facecolor=C_POLY, edgecolor="k", lw=0.7))
        ax.add_patch(Rectangle((bx, yy + 0.18), 2.9, 0.16, facecolor=C_ANODE, edgecolor="none"))
    # molding compound
    ax.add_patch(FancyBboxPatch((5.95, 1.95), 3.4, 3.7, boxstyle="round,pad=0.02",
                                facecolor="none", edgecolor=C_MOLD, lw=6, alpha=0.9))
    # anode & cathode lead frames
    ax.add_patch(Rectangle((5.55, 1.7), 0.5, 1.3, facecolor="#b08d57", edgecolor="k", lw=0.7))
    ax.add_patch(Rectangle((9.3, 1.7), 0.5, 1.3, facecolor="#b08d57", edgecolor="k", lw=0.7))
    ax.text(5.8, 1.45, "Anode (+)", ha="center", fontsize=8)
    ax.text(9.55, 1.45, "Cathode (-)", ha="center", fontsize=8)
    ax.text(7.7, 1.0, "Epoxy molding compound (moisture path)", ha="center", fontsize=7.6, color=C_MOLD, weight="bold")

    # connector arrow
    ax.add_patch(FancyArrowPatch((4.7, 5.0), (6.1, 4.2), arrowstyle="-|>",
                                 mutation_scale=14, color=C_GRAY, lw=1.2))
    return _save(fig, "fig_structure.png")


def fig_taxonomy():
    """Failure-mode taxonomy tree of SAPC."""
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis("off")

    def box(x, y, w, h, text, fc):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                                    facecolor=fc, edgecolor="k", lw=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.2)

    box(4.5, 7.8, 3.0, 0.9, "SAPC failure modes", "#cde1f3")
    roots = [
        (0.3, "Humid-heat\n(85C/85%RH)", "#f6d9b8", ["Polymer oxidation / de-doping",
                                                     "Interface corrosion",
                                                     "Capacitance / ESR drift"]),
        (4.5, "High temperature\n(>=125C)", "#f6c6c6", ["Polymer thermal aging",
                                                        "Grain shrinkage -> ESR rise",
                                                        "Oxide / contact damage"]),
        (8.7, "Thermo-electric\ncoupling", "#cfead0", ["Leakage current rise",
                                                       "Local Joule heating",
                                                       "Thermo-mech. delamination"]),
    ]
    for x, title, fc, subs in roots:
        box(x, 5.4, 3.0, 1.1, title, fc)
        ax.add_patch(FancyArrowPatch((6.0, 7.8), (x + 1.5, 6.5), arrowstyle="-|>",
                                     mutation_scale=12, color=C_GRAY, lw=1.0))
        yy = 4.4
        for s in subs:
            box(x, yy - 0.5, 3.0, 0.8, s, "#f2f2f2")
            ax.add_patch(FancyArrowPatch((x + 1.5, 5.4), (x + 1.5, yy + 0.3),
                                         arrowstyle="-", color=C_GRAY, lw=0.7))
            yy -= 1.15
    return _save(fig, "fig_taxonomy.png")


def fig_param_trends():
    """Conceptual degradation trends of C, ESR, LC vs time (schematic)."""
    t = np.linspace(0, 1, 200)
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    esr = 1 + 0.15 * t + 3.0 * t**6
    cap = 1 - 0.04 * t - 0.20 * t**5
    lc = 1 + 0.4 * t + 8.0 * t**8
    ax.plot(t, esr, color=C_RED, lw=2, label="ESR (normalized)")
    ax.plot(t, cap, color=C_BLUE, lw=2, label="Capacitance (normalized)")
    ax.plot(t, lc, color=C_GREEN, lw=2, ls="--", label="Leakage current (normalized)")
    ax.axhline(2.0, color=C_GRAY, ls=":", lw=1)
    ax.text(0.02, 2.05, "End-of-life criterion (e.g. ESR=2x or C drop 20%)", fontsize=7.5, color=C_GRAY)
    ax.set_xlabel("Normalized stress time")
    ax.set_ylabel("Normalized parameter")
    ax.set_ylim(0, 4)
    ax.set_title("Conceptual degradation trends (schematic)", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.25)
    return _save(fig, "fig_param_trends.png")


def fig_pedot_grain():
    """Granular-metal model: conductive PEDOT grains shrink with aging."""
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
    rng = np.random.default_rng(7)
    centers = rng.uniform(0.15, 0.85, size=(18, 2))
    for ax, r, title in zip(axes, [0.085, 0.05], ["Fresh: large conductive grains",
                                                  "Aged: shrunken grains, wider barriers"]):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="#efe7d8", edgecolor="k"))
        for c in centers:
            ax.add_patch(Circle(c, r, facecolor=C_BLUE, edgecolor="k", lw=0.4, alpha=0.85))
        ax.set_title(title, fontsize=8.6)
    fig.suptitle("PEDOT granular-metal conduction: grain shrinkage raises hopping barriers (-> ESR rise)",
                 fontsize=9)
    return _save(fig, "fig_pedot_grain.png")


def fig_moisture():
    """Moisture ingress and interface delamination schematic."""
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(FancyBboxPatch((1.0, 1.0), 8.0, 4.0, boxstyle="round,pad=0.02",
                                facecolor=C_MOLD, edgecolor="k", lw=1.0, alpha=0.6))
    ax.text(5, 5.3, "Encapsulant", ha="center", fontsize=9, color=C_GRAY)
    # anode/oxide/polymer stack inside
    ax.add_patch(Rectangle((3.0, 2.4), 4.0, 0.7, facecolor=C_ANODE, edgecolor="k"))
    ax.add_patch(Rectangle((3.0, 3.1), 4.0, 0.22, facecolor=C_OXIDE, edgecolor="k"))
    ax.add_patch(Rectangle((3.0, 3.32), 4.0, 0.6, facecolor=C_POLY, edgecolor="k"))
    ax.text(7.15, 2.75, "Al foil", fontsize=7.5, va="center")
    ax.text(7.15, 3.21, "Al2O3", fontsize=7.5, va="center")
    ax.text(7.15, 3.62, "PEDOT", fontsize=7.5, va="center")
    # moisture arrows
    for x0 in [1.6, 2.2, 8.0, 8.6]:
        ax.add_patch(FancyArrowPatch((x0, 4.7), (x0 + 0.6, 3.9), arrowstyle="-|>",
                                     mutation_scale=11, color=C_BLUE, lw=1.3))
    ax.text(1.4, 4.85, "H2O ingress", fontsize=8, color=C_BLUE)
    # delamination crack
    ax.plot([3.5, 4.3, 5.0, 5.8], [3.32, 3.36, 3.30, 3.34], color=C_RED, lw=2)
    ax.text(4.6, 3.0, "delamination / debonding", fontsize=7.6, color=C_RED, ha="center")
    ax.set_title("Moisture-driven oxidation & thermo-mechanical delamination at polymer/oxide interface",
                 fontsize=9)
    return _save(fig, "fig_moisture.png")


def fig_model_map():
    """Map of reliability-modeling approaches."""
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")

    def box(x, y, w, h, text, fc, fs=8.2):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                                    facecolor=fc, edgecolor="k", lw=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)

    box(4.5, 6.7, 3.0, 0.9, "Reliability modeling", "#cde1f3", 9)
    cols = [
        (0.3, "Statistical / empirical", "#f6d9b8",
         ["Weibull / lognormal", "Arrhenius (T)", "Peck/Eyring (T,RH)", "Coffin-Manson (cycling)"]),
        (4.5, "Physics-of-failure (PoF)", "#cfead0",
         ["Polymer de-doping kinetics", "Moisture diffusion (Fickian)", "Interface fracture mechanics",
          "Oxide field crystallization"]),
        (8.7, "Data-driven / PHM", "#f6c6c6",
         ["Particle filter", "LSTM / deep learning", "Ensemble (bagging)", "Physics-informed NN"]),
    ]
    for x, title, fc, items in cols:
        box(x, 5.0, 3.0, 1.0, title, fc, 8.6)
        ax.add_patch(FancyArrowPatch((6.0, 6.7), (x + 1.5, 6.0), arrowstyle="-|>",
                                     mutation_scale=12, color=C_GRAY, lw=1.0))
        yy = 4.2
        for it in items:
            box(x, yy - 0.4, 3.0, 0.7, it, "#f4f4f4", 7.8)
            yy -= 0.95
    return _save(fig, "fig_model_map.png")


def fig_arrhenius_peck():
    """Conceptual Arrhenius/Peck lifetime vs 1/T for several RH (schematic)."""
    invT = np.linspace(2.5, 3.4, 50)  # 1000/T (K^-1)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for rh, col, lab in [(85, C_RED, "85% RH"), (60, C_GREEN, "60% RH"), (40, C_BLUE, "40% RH")]:
        # log(life) = A + Ea/k*(1/T) - n*log(RH); slopes parallel (Ea), offset by RH
        logL = 1.2 * (invT - 2.5) * 3.0 + (- 2.0 * np.log10(rh / 40.0)) + 1.0
        ax.plot(invT, logL, color=col, lw=2, marker="o", ms=3, label=lab)
    ax.set_xlabel("1000/T  (1/K)")
    ax.set_ylabel("log(time-to-failure)  [a.u.]")
    ax.set_title("Arrhenius-Peck life model (schematic): parallel T-lines shifted by humidity",
                 fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    return _save(fig, "fig_arrhenius_peck.png")


def fig_weibull():
    """Conceptual Weibull probability plot (schematic)."""
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for beta, eta, col, lab in [(2.2, 1.0, C_BLUE, "beta=2.2"), (4.0, 1.4, C_RED, "beta=4.0")]:
        u = np.sort(rng.uniform(0.02, 0.98, 30))
        t = eta * (-np.log(1 - u)) ** (1 / beta)
        x = np.log(t)
        y = np.log(-np.log(1 - u))
        ax.plot(x, y, "o", ms=4, color=col)
        # fit line
        b = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 10)
        ax.plot(xs, np.polyval(b, xs), color=col, lw=1.6, label=lab)
    ax.set_xlabel("ln(time-to-failure)")
    ax.set_ylabel("ln(-ln(1-F))")
    ax.set_title("Weibull probability plot (schematic)", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    return _save(fig, "fig_weibull.png")


def fig_gap_map():
    """Research-gap -> dissertation-contribution mapping."""
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 9); ax.axis("off")
    gaps = [
        "G1 Qualitative failure-mode\nclassification, no unified metric",
        "G2 Single-stress models; multi-\nmechanism competition ignored",
        "G3 Polymer de-doping kinetics not\ncoupled to device-level life model",
        "G4 Small-sample, poor RUL accuracy\nfor stacked-package SAPC",
    ]
    contrib = [
        "C1 Quantitative multi-parameter\nfailure-mode framework",
        "C2 Competing-risk (multi-mechanism)\nreliability model",
        "C3 PoF model linking PEDOT\ndegradation to ESR/LC life",
        "C4 Hybrid physics + data-driven\nRUL with uncertainty",
    ]
    for i, (g, c) in enumerate(zip(gaps, contrib)):
        y = 7.2 - i * 1.9
        ax.add_patch(FancyBboxPatch((0.3, y), 4.6, 1.5, boxstyle="round,pad=0.04",
                                    facecolor="#f6d9b8", edgecolor="k", lw=0.8))
        ax.text(2.6, y + 0.75, g, ha="center", va="center", fontsize=7.8)
        ax.add_patch(FancyBboxPatch((7.1, y), 4.6, 1.5, boxstyle="round,pad=0.04",
                                    facecolor="#cfead0", edgecolor="k", lw=0.8))
        ax.text(9.4, y + 0.75, c, ha="center", va="center", fontsize=7.8)
        ax.add_patch(FancyArrowPatch((4.95, y + 0.75), (7.05, y + 0.75), arrowstyle="-|>",
                                     mutation_scale=14, color=C_GRAY, lw=1.4))
    ax.text(2.6, 8.4, "Identified research gaps", ha="center", fontsize=9.5, weight="bold")
    ax.text(9.4, 8.4, "Dissertation contributions", ha="center", fontsize=9.5, weight="bold")
    return _save(fig, "fig_gap_map.png")


def fig_litdist():
    """Honest bar chart of the curated reference set by theme."""
    themes = ["Reviews/\noverview", "Device &\nmaterials", "Humid-heat\nfailure",
              "High-T &\nPEDOT aging", "Modeling &\nALT", "Monitoring &\nRUL", "Standards"]
    counts = [4, 9, 8, 9, 8, 7, 4]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.bar(range(len(themes)), counts, color=C_BLUE, alpha=0.85, edgecolor="k")
    ax.set_xticks(range(len(themes)))
    ax.set_xticklabels(themes, fontsize=7.8)
    ax.set_ylabel("Number of curated references")
    ax.set_title("Distribution of the curated reference set by theme", fontsize=10)
    for i, c in enumerate(counts):
        ax.text(i, c + 0.1, str(c), ha="center", fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    return _save(fig, "fig_litdist.png")


def build_all():
    funcs = [fig_structure, fig_taxonomy, fig_param_trends, fig_pedot_grain,
             fig_moisture, fig_model_map, fig_arrhenius_peck, fig_weibull,
             fig_gap_map, fig_litdist]
    paths = []
    for f in funcs:
        paths.append(f())
        print("built", f.__name__)
    return paths


if __name__ == "__main__":
    build_all()
