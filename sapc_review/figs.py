# -*- coding: utf-8 -*-
"""
Original schematic figures for the SAPC reliability literature-review chapter.

All figures are ORIGINAL drawings created with matplotlib (no copyrighted content
is reproduced). In-figure text is kept in English to avoid CJK glyph issues; figure
captions in the Word document are in Chinese.

Rev.2: enlarged canvases, wrapped/short labels and increased spacing to eliminate
text collisions ("串行"); higher dpi.
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
    "savefig.dpi": 220,
    "figure.dpi": 220,
})

C_ANODE = "#9fb6cd"
C_OXIDE = "#e8c46a"
C_POLY = "#7fb77e"
C_GRAPH = "#6b6b6b"
C_AG = "#cfcfcf"
C_MOLD = "#cdb79e"
C_BLUE = "#2b6cb0"
C_RED = "#c0392b"
C_GREEN = "#2e7d32"
C_GRAY = "#555555"


def _save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white", pad_inches=0.15)
    plt.close(fig)
    return path


def _box(ax, x, y, w, h, text, fc, fs=8.5, ec="k", lw=0.9, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                facecolor=fc, edgecolor=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, weight=weight, linespacing=1.25)


def fig_structure():
    """Cross-section schematic of a stacked aluminum solid capacitor (no label collisions)."""
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # ---- left: single element, layers with clear gaps + leader lines ----
    ax.text(2.4, 8.5, "Single capacitor element (cross-section)",
            ha="center", fontsize=10.5, weight="bold")
    layers = [
        ("Ag paste (cathode contact)", C_AG, 0.55),
        ("Graphite layer", C_GRAPH, 0.5),
        ("Conductive polymer (PEDOT) cathode", C_POLY, 0.8),
        ("Al2O3 dielectric (anodic oxide)", C_OXIDE, 0.5),
        ("Etched Al anode foil (porous)", C_ANODE, 1.0),
    ]
    x0, w = 0.7, 3.2
    y = 1.4
    centers = []
    for name, col, h in layers:
        ax.add_patch(Rectangle((x0, y), w, h, facecolor=col, edgecolor="k", lw=0.9))
        centers.append((name, y + h / 2))
        y += h + 0.28  # clear vertical gap -> no label overlap
    # leader lines + labels to the right, evenly spaced
    label_x = 4.6
    ys = np.linspace(1.6, 6.4, len(centers))
    for (name, yc), yl in zip(centers, ys):
        ax.annotate(name, xy=(x0 + w, yc), xytext=(label_x, yl),
                    fontsize=8.6, va="center", ha="left",
                    arrowprops=dict(arrowstyle="-", color=C_GRAY, lw=0.7))
    ax.text(2.3, 0.95, "etched surface gives ~100x effective area",
            ha="center", fontsize=7.6, style="italic", color=C_GRAY)

    # ---- right: stacked / laminated package ----
    ax.text(10.4, 8.5, "Stacked / laminated package", ha="center",
            fontsize=10.5, weight="bold")
    bx, bw = 8.9, 3.1
    for i in range(5):
        yy = 2.4 + i * 0.78
        ax.add_patch(Rectangle((bx, yy), bw, 0.62, facecolor=C_POLY,
                               edgecolor="k", lw=0.7))
        ax.add_patch(Rectangle((bx, yy + 0.22), bw, 0.18, facecolor=C_ANODE,
                               edgecolor="none"))
    ax.add_patch(FancyBboxPatch((8.6, 2.05), 3.7, 4.6, boxstyle="round,pad=0.02",
                                facecolor="none", edgecolor=C_MOLD, lw=7, alpha=0.9))
    ax.add_patch(Rectangle((8.2, 2.0), 0.5, 1.5, facecolor="#b08d57",
                           edgecolor="k", lw=0.7))
    ax.add_patch(Rectangle((12.3, 2.0), 0.5, 1.5, facecolor="#b08d57",
                           edgecolor="k", lw=0.7))
    ax.text(8.45, 1.7, "Anode (+)", ha="center", fontsize=8.2)
    ax.text(12.55, 1.7, "Cathode (-)", ha="center", fontsize=8.2)
    ax.text(10.45, 7.05, "Epoxy molding (moisture diffusion path)",
            ha="center", fontsize=8, color="#9a7b52", weight="bold")
    ax.add_patch(FancyArrowPatch((4.55, 5.2), (8.55, 4.6), arrowstyle="-|>",
                                 mutation_scale=14, color=C_GRAY, lw=1.2,
                                 connectionstyle="arc3,rad=-0.15"))
    ax.text(6.6, 5.35, "parallel stacking", fontsize=8, color=C_GRAY, ha="center")
    return _save(fig, "fig_structure.png")


def fig_taxonomy():
    """Failure-mode taxonomy tree (wide canvas, wrapped labels, no overlap)."""
    fig, ax = plt.subplots(figsize=(10.4, 6.2))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10.5)
    ax.axis("off")

    _box(ax, 5.6, 9.2, 3.8, 0.95, "SAPC failure modes", "#cde1f3", fs=10, weight="bold")
    roots = [
        (0.4, "Humid-heat\n(85C/85%RH, THB)", "#f6d9b8",
         ["Polymer oxidation\n& de-doping", "Interfacial corrosion\n/ delamination", "ESR rise,\nLC rise"]),
        (5.6, "High temperature\n(>=105-125C)", "#f6c6c6",
         ["Polymer thermal\nageing (oxidation)", "PEDOT grain\nshrinkage -> ESR rise", "C drift ->\nopen-mode EOL"]),
        (10.8, "Thermo-electric\ncoupling", "#cfead0",
         ["Self-heating\n(ESR x ripple)", "Bias-driven\nLC increase", "Thermo-mech.\ndelamination"]),
    ]
    for x, title, fc, subs in roots:
        _box(ax, x, 6.7, 3.8, 1.25, title, fc, fs=9)
        ax.add_patch(FancyArrowPatch((7.5, 9.2), (x + 1.9, 7.95), arrowstyle="-|>",
                                     mutation_scale=12, color=C_GRAY, lw=1.0))
        yy = 5.0
        for s in subs:
            _box(ax, x, yy - 0.55, 3.8, 1.0, s, "#f3f3f3", fs=8)
            ax.add_patch(FancyArrowPatch((x + 1.9, 6.7), (x + 1.9, yy + 0.45),
                                         arrowstyle="-", color=C_GRAY, lw=0.7))
            yy -= 1.45
    return _save(fig, "fig_taxonomy.png")


def fig_param_trends():
    t = np.linspace(0, 1, 200)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    esr = 1 + 0.15 * t + 3.0 * t**6
    cap = 1 - 0.04 * t - 0.20 * t**5
    lc = 1 + 0.4 * t + 8.0 * t**8
    ax.plot(t, esr, color=C_RED, lw=2.2, label="ESR (normalized)")
    ax.plot(t, cap, color=C_BLUE, lw=2.2, label="Capacitance (normalized)")
    ax.plot(t, lc, color=C_GREEN, lw=2.2, ls="--", label="Leakage current (normalized)")
    ax.axhline(2.0, color=C_GRAY, ls=":", lw=1.2)
    ax.text(0.02, 2.08, "End-of-life criterion (e.g. ESR=2x or dC=-20%)",
            fontsize=8, color=C_GRAY)
    ax.set_xlabel("Normalized stress time", fontsize=10)
    ax.set_ylabel("Normalized parameter", fontsize=10)
    ax.set_ylim(0, 4)
    ax.set_title("Conceptual degradation trends of SAPC (schematic)", fontsize=11)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(alpha=0.25)
    return _save(fig, "fig_param_trends.png")


def fig_pedot_grain():
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.9))
    rng = np.random.default_rng(7)
    centers = rng.uniform(0.15, 0.85, size=(18, 2))
    for ax, r, title in zip(axes, [0.085, 0.05],
                            ["Fresh: large conductive grains\n(low inter-grain barrier)",
                             "Aged: shrunken grains\n(wider hopping barriers)"]):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="#efe7d8", edgecolor="k"))
        for c in centers:
            ax.add_patch(Circle(c, r, facecolor=C_BLUE, edgecolor="k", lw=0.4, alpha=0.85))
        ax.set_title(title, fontsize=9, linespacing=1.3)
    fig.suptitle("PEDOT granular-metal conduction: grain shrinkage raises hopping barriers (-> ESR rise)",
                 fontsize=9.5, y=1.02)
    return _save(fig, "fig_pedot_grain.png")


def fig_moisture():
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6.5); ax.axis("off")
    ax.add_patch(FancyBboxPatch((1.0, 1.0), 9.0, 4.4, boxstyle="round,pad=0.02",
                                facecolor=C_MOLD, edgecolor="k", lw=1.0, alpha=0.55))
    ax.text(5.5, 5.65, "Encapsulant (epoxy)", ha="center", fontsize=9.5, color="#7a5e3a")
    ax.add_patch(Rectangle((3.2, 2.5), 4.6, 0.8, facecolor=C_ANODE, edgecolor="k"))
    ax.add_patch(Rectangle((3.2, 3.3), 4.6, 0.28, facecolor=C_OXIDE, edgecolor="k"))
    ax.add_patch(Rectangle((3.2, 3.58), 4.6, 0.7, facecolor=C_POLY, edgecolor="k"))
    ax.text(8.0, 2.9, "Al foil", fontsize=8.2, va="center")
    ax.text(8.0, 3.44, "Al2O3", fontsize=8.2, va="center")
    ax.text(8.0, 3.93, "PEDOT", fontsize=8.2, va="center")
    for x0 in [1.6, 2.3, 8.6, 9.3]:
        ax.add_patch(FancyArrowPatch((x0, 5.0), (x0 + 0.55, 4.4), arrowstyle="-|>",
                                     mutation_scale=11, color=C_BLUE, lw=1.4))
    ax.text(1.5, 5.2, "H2O ingress", fontsize=8.4, color=C_BLUE)
    ax.plot([3.7, 4.6, 5.5, 6.4, 7.3], [3.58, 3.63, 3.55, 3.62, 3.57],
            color=C_RED, lw=2.2)
    ax.text(5.5, 4.55, "swelling (+150% optical thickness, 9->80%RH)",
            fontsize=7.8, color=C_BLUE, ha="center")
    ax.text(5.5, 2.15, "interfacial delamination / debonding -> contact-R up",
            fontsize=8, color=C_RED, ha="center")
    ax.set_title("Moisture-driven swelling, oxidation/de-doping and interfacial delamination",
                 fontsize=10)
    return _save(fig, "fig_moisture.png")


def fig_model_map():
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    ax.set_xlim(0, 15); ax.set_ylim(0, 9); ax.axis("off")
    _box(ax, 5.6, 7.7, 3.8, 0.95, "Reliability modeling of SAPC", "#cde1f3", fs=10, weight="bold")
    cols = [
        (0.4, "Statistical / empirical", "#f6d9b8",
         ["Weibull / lognormal", "Arrhenius (10C rule)", "Peck / Eyring (T,RH)", "Coffin-Manson (cycling)"]),
        (5.6, "Physics-of-failure (PoF)", "#cfead0",
         ["PEDOT de-doping\n/oxidation kinetics", "Moisture diffusion\n(Fickian)", "Interface fracture\nmechanics", "Oxide field-driven\ndegradation"]),
        (10.8, "Data-driven / PHM", "#f6c6c6",
         ["Particle filter", "LSTM / deep learning", "Ensemble (bagging)", "Physics-informed NN"]),
    ]
    for x, title, fc, items in cols:
        _box(ax, x, 5.9, 3.8, 1.0, title, fc, fs=9)
        ax.add_patch(FancyArrowPatch((7.5, 7.7), (x + 1.9, 6.9), arrowstyle="-|>",
                                     mutation_scale=12, color=C_GRAY, lw=1.0))
        yy = 5.0
        for it in items:
            _box(ax, x, yy - 0.45, 3.8, 0.85, it, "#f4f4f4", fs=7.8)
            yy -= 1.12
    return _save(fig, "fig_model_map.png")


def fig_arrhenius_peck():
    invT = np.linspace(2.5, 3.4, 50)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for rh, col, lab in [(85, C_RED, "85% RH"), (60, C_GREEN, "60% RH"), (40, C_BLUE, "40% RH")]:
        logL = 1.2 * (invT - 2.5) * 3.0 + (-2.0 * np.log10(rh / 40.0)) + 1.0
        ax.plot(invT, logL, color=col, lw=2.2, marker="o", ms=3.5, label=lab)
    ax.set_xlabel("1000 / T  (1/K)", fontsize=10)
    ax.set_ylabel("log(time-to-failure)  [a.u.]", fontsize=10)
    ax.set_title("Arrhenius-Peck life model (schematic):\nparallel temperature lines shifted by humidity",
                 fontsize=10, linespacing=1.3)
    ax.legend(fontsize=9, title="Peck: t = A*RH^-n*exp(Ea/kT)")
    ax.grid(alpha=0.25)
    return _save(fig, "fig_arrhenius_peck.png")


def fig_weibull():
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for beta, eta, col, lab in [(2.2, 1.0, C_BLUE, "beta=2.2 (early/random)"),
                                (4.0, 1.4, C_RED, "beta=4.0 (wear-out)")]:
        u = np.sort(rng.uniform(0.02, 0.98, 30))
        t = eta * (-np.log(1 - u)) ** (1 / beta)
        x = np.log(t)
        y = np.log(-np.log(1 - u))
        ax.plot(x, y, "o", ms=4, color=col)
        b = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 10)
        ax.plot(xs, np.polyval(b, xs), color=col, lw=1.8, label=lab)
    ax.set_xlabel("ln(time-to-failure)", fontsize=10)
    ax.set_ylabel("ln(-ln(1-F))", fontsize=10)
    ax.set_title("Weibull probability plot (schematic)", fontsize=11)
    ax.legend(fontsize=8.5)
    ax.grid(alpha=0.25)
    return _save(fig, "fig_weibull.png")


def fig_gap_map():
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    ax.set_xlim(0, 13); ax.set_ylim(0, 10); ax.axis("off")
    gaps = [
        "G1  Qualitative failure-mode\nclassification; no unified metric",
        "G2  Single-stress models;\nmulti-mechanism competition ignored",
        "G3  PEDOT de-doping kinetics not\ncoupled to device-level life model",
        "G4  Small-sample; poor RUL accuracy\nfor stacked-package SAPC",
    ]
    contrib = [
        "C1  Quantitative multi-parameter\nfailure-mode framework",
        "C2  Competing-risk (multi-mechanism)\nreliability model",
        "C3  PoF model linking PEDOT\ndegradation to ESR / LC life",
        "C4  Hybrid physics + data-driven\nRUL with uncertainty bounds",
    ]
    for i, (g, c) in enumerate(zip(gaps, contrib)):
        y = 7.6 - i * 1.95
        _box(ax, 0.4, y, 5.3, 1.5, g, "#f6d9b8", fs=8.2)
        _box(ax, 7.3, y, 5.3, 1.5, c, "#cfead0", fs=8.2)
        ax.add_patch(FancyArrowPatch((5.75, y + 0.75), (7.25, y + 0.75),
                                     arrowstyle="-|>", mutation_scale=15, color=C_GRAY, lw=1.5))
    ax.text(3.05, 9.4, "Identified research gaps", ha="center", fontsize=10, weight="bold")
    ax.text(9.95, 9.4, "Dissertation contributions", ha="center", fontsize=10, weight="bold")
    return _save(fig, "fig_gap_map.png")


def fig_litdist():
    themes = ["Reviews/\noverview", "Device &\nmaterials", "Humid-heat\nfailure",
              "High-T &\nPEDOT ageing", "Modeling &\nALT", "Monitoring\n& RUL", "Standards &\nindustry"]
    counts = [4, 11, 9, 11, 9, 6, 12]
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.bar(range(len(themes)), counts, color=C_BLUE, alpha=0.85, edgecolor="k")
    ax.set_xticks(range(len(themes)))
    ax.set_xticklabels(themes, fontsize=8)
    ax.set_ylabel("Number of curated references", fontsize=10)
    ax.set_title("Thematic distribution of the curated reference set", fontsize=11)
    for i, c in enumerate(counts):
        ax.text(i, c + 0.12, str(c), ha="center", fontsize=8.5)
    ax.grid(axis="y", alpha=0.25)
    ax.set_ylim(0, max(counts) + 1.5)
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
