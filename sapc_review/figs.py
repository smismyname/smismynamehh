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


def fig_anodize():
    """Forming: capacitance and oxide thickness vs forming voltage; etched-foil area gain."""
    Vf = np.linspace(0, 100, 200)
    d = 1.2 * Vf + 1.0            # oxide thickness ~ 1.2 nm/V
    C = 1.0 / (d + 1e-6)          # C ~ 1/d (arbitrary units)
    C = C / C[10] * 100
    fig, ax1 = plt.subplots(figsize=(7.2, 4.2))
    ax1.plot(Vf, d, color=C_BLUE, lw=2.2, label="Oxide thickness d (nm)")
    ax1.set_xlabel("Forming (anodizing) voltage  Vf  (V)", fontsize=10)
    ax1.set_ylabel("Oxide thickness  d  (nm)", color=C_BLUE, fontsize=10)
    ax1.tick_params(axis="y", labelcolor=C_BLUE)
    ax2 = ax1.twinx()
    ax2.plot(Vf, C, color=C_RED, lw=2.2, ls="--", label="Capacitance C (a.u.)")
    ax2.set_ylabel("Capacitance per area  C  (a.u.)", color=C_RED, fontsize=10)
    ax2.tick_params(axis="y", labelcolor=C_RED)
    ax1.set_title("Anodic oxide growth: d proportional to Vf, C inversely proportional to d (C = e0*er*A/d)",
                  fontsize=9.5)
    ax1.grid(alpha=0.25)
    ax1.text(40, 25, "etched foil: ~100x area A\n-> high C in small volume",
             fontsize=8.4, color=C_GRAY, ha="center",
             bbox=dict(boxstyle="round", fc="#eef3f8", ec=C_GRAY, lw=0.7))
    return _save(fig, "fig_anodize.png")


def fig_pedot_chem():
    """Schematic of PEDOT chain (positively doped) charge-balanced by PSS- (original)."""
    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis("off")
    # PEDOT backbone: a row of fused thiophene-EDOT units (stylized as pentagons + O-CH2 bridge)
    for i in range(5):
        x = 1.0 + i * 2.2
        ax.add_patch(FancyBboxPatch((x, 3.2), 1.5, 1.0, boxstyle="round,pad=0.03",
                                    facecolor=C_BLUE, edgecolor="k", lw=0.8, alpha=0.85))
        ax.text(x + 0.75, 3.7, "EDOT", ha="center", va="center", fontsize=8, color="white")
        if i < 4:
            ax.plot([x + 1.5, x + 2.2], [3.7, 3.7], color="k", lw=1.4)
        ax.text(x + 0.75, 4.45, "+", ha="center", fontsize=11, color=C_RED, weight="bold")
    ax.text(6.0, 5.4, "PEDOT+ conjugated backbone (holes = charge carriers)",
            ha="center", fontsize=9, color=C_BLUE, weight="bold")
    # PSS- chain below
    ax.add_patch(FancyBboxPatch((1.0, 1.0), 11.2, 0.9, boxstyle="round,pad=0.03",
                                facecolor="#d9b38c", edgecolor="k", lw=0.8, alpha=0.8))
    ax.text(6.6, 1.45, "PSS- polyanion (SO3- groups, acidic, hygroscopic)  -> dopant / dispersant",
            ha="center", va="center", fontsize=8.6, color="#5a4126")
    for i in range(5):
        x = 1.75 + i * 2.2
        ax.annotate("", xy=(x + 0.75, 2.95), xytext=(x + 0.75, 2.0),
                    arrowprops=dict(arrowstyle="<->", color=C_GRAY, lw=0.9))
    ax.text(12.6, 2.5, "Coulomb\ncoupling", fontsize=7.6, color=C_GRAY, va="center")
    ax.set_title("PEDOT:PSS: doped conjugated PEDOT+ charge-balanced by PSS- (schematic)",
                 fontsize=10)
    return _save(fig, "fig_pedot_chem.png")


def fig_vrh():
    """ln(sigma) vs T^-1/4 (Mott) and T^-1/2 (ES): fresh vs aged slopes (T0 increases)."""
    T = np.linspace(250, 400, 60)
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0))
    for ax, p, lab in zip(axes, [0.25, 0.5],
                          ["Mott-VRH  (p = 1/4)", "Efros-Shklovskii  (p = 1/2)"]):
        x = T ** (-p)
        for T0, col, name in [(1.2e4 if p == 0.25 else 200, C_BLUE, "fresh (low T0)"),
                              (4.0e4 if p == 0.25 else 520, C_RED, "aged (high T0)")]:
            lnsig = 6.0 - (T0 ** p) * x
            ax.plot(x, lnsig, color=col, lw=2.2, marker="o", ms=3, label=name)
        ax.set_xlabel(f"T^(-{ '1/4' if p==0.25 else '1/2' })", fontsize=10)
        ax.set_ylabel("ln(conductivity)  [a.u.]", fontsize=9.5)
        ax.set_title(lab, fontsize=10)
        ax.legend(fontsize=8.5)
        ax.grid(alpha=0.25)
    fig.suptitle("VRH transport: ageing raises characteristic temperature T0 -> lower conductivity -> ESR rise",
                 fontsize=9.8, y=1.02)
    return _save(fig, "fig_vrh.png")


def fig_impedance():
    """Capacitor impedance |Z| vs frequency with C / ESR / ESL regions + equiv. circuit."""
    f = np.logspace(2, 7, 400)
    C = 100e-6; ESR = 0.012; ESL = 3e-9
    w = 2 * np.pi * f
    Zc = 1 / (w * C); Zl = w * ESL
    Z = np.sqrt(ESR**2 + (Zc - Zl)**2)
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.loglog(f, Z, color=C_BLUE, lw=2.3)
    ax.axhline(ESR, color=C_GRAY, ls=":", lw=1.2)
    f0 = 1 / (2 * np.pi * np.sqrt(ESL * C))
    ax.axvline(f0, color=C_RED, ls="--", lw=1.0)
    ax.text(2e2, 2.0, "1/(wC):\ncapacitive", fontsize=8.4, color=C_GREEN)
    ax.text(2e4, ESR * 1.25, "ESR floor (resistive)", fontsize=8.4, color=C_GRAY)
    ax.text(2.0e6, 2.0, "wL:\ninductive (ESL)", fontsize=8.4, color=C_RED, ha="center")
    ax.text(f0 * 1.05, 0.03, "self-resonance f0", fontsize=8.0, color=C_RED)
    ax.set_xlabel("Frequency (Hz)", fontsize=10)
    ax.set_ylabel("|Z| (ohm)", fontsize=10)
    ax.set_title("Capacitor impedance: Z = sqrt(ESR^2 + (1/wC - wL)^2);\nseries RLC equivalent circuit (C-ESR-ESL)",
                 fontsize=9.6, linespacing=1.3)
    ax.grid(which="both", alpha=0.2)
    return _save(fig, "fig_impedance.png")


def fig_nyquist():
    """EIS Nyquist evolution with ageing (ESR shifts right, arc grows)."""
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    theta = np.linspace(0, np.pi, 120)
    for esr, rad, col, lab in [(0.012, 0.010, C_BLUE, "fresh"),
                               (0.020, 0.020, C_GREEN, "mid-life"),
                               (0.035, 0.040, C_RED, "aged")]:
        xr = esr + rad - rad * np.cos(theta)
        yi = -rad * np.sin(theta)
        ax.plot(xr * 1e3, -yi * 1e3, color=col, lw=2.2, label=lab)
    ax.set_xlabel("Re(Z)  (mohm)", fontsize=10)
    ax.set_ylabel("-Im(Z)  (mohm)", fontsize=10)
    ax.set_title("EIS Nyquist evolution: ESR intercept shifts right,\ninterfacial arc grows with ageing",
                 fontsize=9.6, linespacing=1.3)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.25)
    ax.annotate("ESR = high-freq\nReal intercept", xy=(12, 1.5), xytext=(28, 12),
                fontsize=8.2, color=C_GRAY,
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=0.8))
    return _save(fig, "fig_nyquist.png")


def fig_bathtub():
    t = np.linspace(0, 10, 400)
    infant = 0.8 * np.exp(-t / 0.8)
    random = 0.12 * np.ones_like(t)
    wear = 0.02 * np.exp((t - 7.5) / 1.0)
    total = infant + random + wear
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ax.plot(t, total, color=C_BLUE, lw=2.4, label="total hazard h(t)")
    ax.plot(t, infant + random, color=C_GREEN, lw=1.2, ls="--", alpha=0.8)
    ax.fill_between(t, 0, total, where=(t < 2.2), color="#f6d9b8", alpha=0.5)
    ax.fill_between(t, 0, total, where=((t >= 2.2) & (t < 7.2)), color="#cfead0", alpha=0.5)
    ax.fill_between(t, 0, total, where=(t >= 7.2), color="#f6c6c6", alpha=0.5)
    ax.text(1.0, 0.78, "infant\nmortality\n(beta<1)", fontsize=8.2, ha="center")
    ax.text(4.7, 0.32, "useful life\n(random, beta~1)", fontsize=8.2, ha="center")
    ax.text(8.7, 0.78, "wear-out\n(beta>1)", fontsize=8.2, ha="center")
    ax.set_xlabel("Time", fontsize=10); ax.set_ylabel("Hazard rate  h(t)", fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.set_title("Bathtub hazard-rate curve and Weibull shape-parameter regimes", fontsize=10)
    ax.grid(alpha=0.2)
    return _save(fig, "fig_bathtub.png")


def fig_competing():
    t = np.linspace(0, 2.2, 300)
    R_esr = np.exp(-(t / 1.6) ** 3.0)
    R_lc = np.exp(-(t / 1.9) ** 2.0)
    R_mech = np.exp(-(t / 2.6) ** 4.0)
    R_sys = R_esr * R_lc * R_mech
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(t, R_esr, color=C_RED, lw=1.8, ls="--", label="R_ESR (ESR rise)")
    ax.plot(t, R_lc, color=C_GREEN, lw=1.8, ls="--", label="R_LC (leakage)")
    ax.plot(t, R_mech, color="#8e44ad", lw=1.8, ls="--", label="R_mech (delamination)")
    ax.plot(t, R_sys, color=C_BLUE, lw=2.6, label="R_system = product R_i")
    ax.set_xlabel("Normalized time", fontsize=10)
    ax.set_ylabel("Reliability  R(t)", fontsize=10)
    ax.set_title("Competing-risk reliability: system reliability is the product of\nindependent mechanism reliabilities",
                 fontsize=9.6, linespacing=1.3)
    ax.legend(fontsize=8.5, loc="lower left")
    ax.grid(alpha=0.25)
    return _save(fig, "fig_competing.png")


def fig_stochastic():
    """Wiener vs Gamma degradation sample paths to a threshold; RUL pdf (first-passage)."""
    rng = np.random.default_rng(11)
    t = np.linspace(0, 1, 200)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0))
    # left: sample paths
    ax = axes[0]
    thr = 1.0
    for _ in range(6):
        drift = 0.9 * t
        diff = np.cumsum(rng.normal(0, 0.035, size=t.size))
        path = drift + diff
        ax.plot(t, path, color=C_BLUE, lw=1.0, alpha=0.7)
    for _ in range(6):
        inc = rng.gamma(shape=0.6, scale=0.06, size=t.size)
        path = np.cumsum(inc)
        ax.plot(t, path, color=C_GREEN, lw=1.0, alpha=0.7)
    ax.axhline(thr, color=C_RED, ls="--", lw=1.6)
    ax.text(0.02, thr + 0.02, "failure threshold (e.g. ESR = 2x)", fontsize=8.2, color=C_RED)
    ax.plot([], [], color=C_BLUE, label="Wiener (non-monotonic)")
    ax.plot([], [], color=C_GREEN, label="Gamma (monotonic)")
    ax.set_xlabel("Time", fontsize=10); ax.set_ylabel("Degradation  X(t)", fontsize=10)
    ax.set_title("Stochastic degradation paths", fontsize=10)
    ax.legend(fontsize=8.2, loc="upper left"); ax.grid(alpha=0.2)
    ax.set_ylim(0, 1.4)
    # right: RUL pdf (inverse Gaussian-like)
    ax2 = axes[1]
    tt = np.linspace(0.01, 1.2, 300)
    mu, lam = 0.5, 8.0
    pdf = np.sqrt(lam / (2 * np.pi * tt**3)) * np.exp(-lam * (tt - mu)**2 / (2 * mu**2 * tt))
    ax2.plot(tt, pdf, color=C_BLUE, lw=2.4)
    ax2.fill_between(tt, 0, pdf, color="#cde1f3", alpha=0.6)
    ax2.axvline(mu, color=C_RED, ls="--", lw=1.2)
    ax2.text(mu + 0.02, max(pdf) * 0.8, "median RUL", fontsize=8.4, color=C_RED)
    ax2.set_xlabel("Remaining useful life", fontsize=10)
    ax2.set_ylabel("Probability density", fontsize=10)
    ax2.set_title("First-passage RUL distribution (inverse-Gaussian)", fontsize=9.6)
    ax2.grid(alpha=0.2)
    return _save(fig, "fig_stochastic.png")


def fig_thermal():
    """Thermal network for ripple self-heating: core hotspot -> case -> ambient."""
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis("off")
    _box(ax, 0.6, 2.3, 2.2, 1.4, "Core hotspot\nT_hot", "#f6c6c6", fs=9)
    _box(ax, 5.0, 2.3, 2.2, 1.4, "Case\nT_case", "#f6d9b8", fs=9)
    _box(ax, 9.4, 2.3, 2.2, 1.4, "Ambient\nT_amb", "#cfead0", fs=9)
    ax.add_patch(FancyArrowPatch((2.8, 3.0), (5.0, 3.0), arrowstyle="-|>",
                                 mutation_scale=14, color=C_GRAY, lw=1.3))
    ax.add_patch(FancyArrowPatch((7.2, 3.0), (9.4, 3.0), arrowstyle="-|>",
                                 mutation_scale=14, color=C_GRAY, lw=1.3))
    ax.text(3.9, 3.35, "Rth(core-case)", fontsize=8.2, ha="center", color=C_GRAY)
    ax.text(8.3, 3.35, "Rth(case-amb)", fontsize=8.2, ha="center", color=C_GRAY)
    ax.add_patch(FancyArrowPatch((1.7, 4.6), (1.7, 3.7), arrowstyle="-|>",
                                 mutation_scale=14, color=C_RED, lw=1.6))
    ax.text(1.7, 5.0, "P = I_ripple^2 x ESR(f,T)", fontsize=9, ha="center", color=C_RED)
    ax.text(7.0, 1.2, "T_hot = T_amb + P x (Rth_core-case + Rth_case-amb)   ->   positive ESR-heat feedback",
            fontsize=8.8, ha="center", color="#333333",
            bbox=dict(boxstyle="round", fc="#eef3f8", ec=C_GRAY, lw=0.7))
    ax.set_title("Thermo-electric self-heating model (lumped thermal network)", fontsize=10)
    return _save(fig, "fig_thermal.png")


def fig_test_map():
    """Accelerated-test condition map in T-RH plane with standard points."""
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    pts = [(85, 85, "THB 85/85", C_BLUE),
           (110, 85, "110/85 (CALCE)", C_GREEN),
           (130, 85, "HAST 130/85", C_RED),
           (125, 0, "High-T 125C", "#8e44ad"),
           (105, 0, "Endurance 105C", "#e67e22"),
           (60, 60, "Use (example)", C_GRAY)]
    for T, RH, lab, col in pts:
        ax.scatter([T], [RH], s=90, color=col, edgecolor="k", zorder=3)
        ax.annotate(lab, (T, RH), textcoords="offset points", xytext=(6, 6),
                    fontsize=8.2, color=col)
    ax.set_xlabel("Temperature (C)", fontsize=10)
    ax.set_ylabel("Relative humidity (%RH)", fontsize=10)
    ax.set_xlim(40, 145); ax.set_ylim(-8, 100)
    ax.set_title("Accelerated-test condition map (temperature-humidity-bias)", fontsize=10)
    ax.grid(alpha=0.25)
    ax.annotate("", xy=(120, 92), xytext=(70, 65),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2))
    ax.text(86, 70, "increasing acceleration", rotation=22, fontsize=8.0, color=C_GRAY)
    return _save(fig, "fig_test_map.png")


def fig_fishbone():
    """Ishikawa cause-effect for SAPC ESR rise / leakage increase."""
    fig, ax = plt.subplots(figsize=(10.2, 5.0))
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")
    ax.add_patch(FancyArrowPatch((0.6, 4.5), (12.8, 4.5), arrowstyle="-|>",
                                 mutation_scale=18, color="k", lw=2.0))
    _box(ax, 12.9, 3.9, 3.0, 1.2, "ESR rise /\nLC increase\n(EOL)", "#f6c6c6", fs=9)
    bones = [
        (2.4, 7.8, "Material", ["PEDOT oxidation", "de-doping", "grain shrinkage"], True),
        (6.0, 7.8, "Environment", ["humidity (RH)", "temperature", "thermal cycling"], True),
        (9.6, 7.8, "Electrical", ["DC bias", "ripple self-heat", "surge/over-voltage"], True),
        (2.4, 1.2, "Process", ["Fe particles", "etch/forming quality", "encapsulation seal"], False),
        (6.0, 1.2, "Interface", ["delamination", "contact-R rise", "swelling/debond"], False),
        (9.6, 1.2, "Mechanical", ["vibration", "CTE mismatch", "solder fatigue"], False),
    ]
    for bx, by, title, subs, up in bones:
        ix = bx + 2.6
        ax.add_patch(FancyArrowPatch((bx, by), (ix, 4.5), arrowstyle="-",
                                     color=C_GRAY, lw=1.4))
        ax.text(bx - 0.1, by + (0.25 if up else -0.25), title, fontsize=9,
                weight="bold", ha="center", va="bottom" if up else "top",
                color=C_BLUE)
        for k, s in enumerate(subs):
            fx = bx + 0.55 * (k + 1)
            fy = by - (k + 1) * 0.62 if up else by + (k + 1) * 0.62
            ax.text(fx, fy, s, fontsize=7.6, ha="left",
                    va="center", color="#444444")
    ax.set_title("Ishikawa (cause-effect) diagram for SAPC degradation drivers", fontsize=10)
    return _save(fig, "fig_fishbone.png")


def fig_rul():
    """RUL prediction: observed degradation + predicted band + threshold + RUL pdf."""
    rng = np.random.default_rng(5)
    t = np.linspace(0, 1.6, 320)
    tp = 0.8
    true = 1.0 + 0.2 * t + 1.4 * t**4
    obs_t = t[t <= tp]
    obs = (1.0 + 0.2 * obs_t + 1.4 * obs_t**4) + rng.normal(0, 0.03, obs_t.size)
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    ax.scatter(obs_t, obs, s=10, color=C_GRAY, label="observed ESR/ESR0")
    fut = t[t >= tp]
    mean = 1.0 + 0.2 * fut + 1.4 * fut**4
    band = 0.05 + 0.9 * (fut - tp) ** 2
    ax.plot(fut, mean, color=C_BLUE, lw=2.0, label="predicted mean")
    ax.fill_between(fut, mean - band, mean + band, color="#cde1f3", alpha=0.6,
                    label="confidence band")
    ax.axhline(2.0, color=C_RED, ls="--", lw=1.4)
    ax.axvline(tp, color="k", ls=":", lw=1.0)
    ax.text(0.02, 2.05, "EOL threshold (ESR = 2x)", fontsize=8.2, color=C_RED)
    ax.text(tp + 0.01, 0.4, "t_p (prediction time)", fontsize=8.0, rotation=90, va="bottom")
    ax.set_xlabel("Time", fontsize=10); ax.set_ylabel("ESR / ESR0", fontsize=10)
    ax.set_ylim(0, 3.2)
    ax.set_title("RUL prediction with uncertainty: degradation trajectory vs failure threshold",
                 fontsize=9.6)
    ax.legend(fontsize=8.2, loc="upper left"); ax.grid(alpha=0.2)
    return _save(fig, "fig_rul.png")


def fig_fa_workflow():
    """Failure-analysis workflow flowchart."""
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    ax.set_xlim(0, 17); ax.set_ylim(0, 5); ax.axis("off")
    steps = [
        ("Electrical test\nC, ESR, LC, |Z|", "#cde1f3"),
        ("Non-destructive\nX-ray, C-SAM", "#cfead0"),
        ("Decapsulation\n/ cross-section", "#f6d9b8"),
        ("Microscopy\nSEM / TEM", "#f6c6c6"),
        ("Composition\nEDS / XPS", "#e8d4f0"),
        ("Chemical\nFTIR / Raman", "#fde9c8"),
        ("Mechanism +\nEIS modeling", "#cde1f3"),
    ]
    x = 0.3
    for i, (txt, col) in enumerate(steps):
        _box(ax, x, 1.9, 2.0, 1.4, txt, col, fs=8.0)
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((x + 2.0, 2.6), (x + 2.35, 2.6),
                                         arrowstyle="-|>", mutation_scale=12,
                                         color=C_GRAY, lw=1.2))
        x += 2.35
    ax.set_title("Failure-analysis workflow for SAPC (non-destructive to mechanism)", fontsize=10)
    return _save(fig, "fig_fa_workflow.png")


def fig_timeline():
    """Technology-evolution timeline of conductive-polymer electrolytic capacitors."""
    fig, ax = plt.subplots(figsize=(10.0, 3.6))
    ax.set_xlim(1988, 2028); ax.set_ylim(0, 4); ax.axis("off")
    ax.add_patch(FancyArrowPatch((1989, 2.0), (2027, 2.0), arrowstyle="-|>",
                                 mutation_scale=16, color="k", lw=2.0))
    events = [
        (1991, "Conducting-polymer\ne-cap (PPy)", 1),
        (1998, "PEDOT:PSS\nelectrolyte", -1),
        (2005, "Polymer Ta /\nlow-ESR chips", 1),
        (2010, "Hybrid polymer\nAl (liquid+polymer)", -1),
        (2016, "Multilayer\nstacked SAPC", 1),
        (2024, "High-reliability\nprocess / space eval.", -1),
    ]
    for yr, txt, up in events:
        ax.scatter([yr], [2.0], s=70, color=C_BLUE, edgecolor="k", zorder=3)
        ax.plot([yr, yr], [2.0, 2.0 + 0.5 * up], color=C_GRAY, lw=1.0)
        ax.text(yr, 2.0 + 0.62 * up, f"{yr}\n{txt}", ha="center",
                va="bottom" if up > 0 else "top", fontsize=8.0,
                color="#333333", linespacing=1.2)
    ax.set_title("Technology evolution of conductive-polymer (aluminum) electrolytic capacitors",
                 fontsize=10)
    return _save(fig, "fig_timeline.png")


def fig_bibliometric():
    """Curated-reference publication-year trend (real counts from this chapter's set)."""
    years = list(range(2008, 2026))
    # approximate distribution of dated references used in this chapter
    counts = {2008: 1, 2009: 1, 2010: 1, 2011: 2, 2013: 3, 2014: 3, 2015: 4,
              2016: 5, 2017: 4, 2018: 4, 2019: 4, 2020: 7, 2021: 4, 2022: 4,
              2023: 4, 2024: 8, 2025: 2}
    vals = [counts.get(y, 0) for y in years]
    cum = np.cumsum(vals)
    fig, ax = plt.subplots(figsize=(7.8, 4.0))
    ax.bar(years, vals, color=C_BLUE, alpha=0.8, edgecolor="k", label="per year")
    ax2 = ax.twinx()
    ax2.plot(years, cum, color=C_RED, lw=2.2, marker="o", ms=3.5, label="cumulative")
    ax.set_xlabel("Publication year", fontsize=10)
    ax.set_ylabel("Curated references (per year)", fontsize=9.5, color=C_BLUE)
    ax2.set_ylabel("Cumulative", fontsize=9.5, color=C_RED)
    ax.set_title("Publication-year trend of the curated reference set (dated entries)", fontsize=9.8)
    ax.grid(axis="y", alpha=0.2)
    return _save(fig, "fig_bibliometric.png")


def fig_cv_temp():
    """C and ESR vs temperature/frequency: SAPC stability vs liquid Al (schematic)."""
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.9))
    T = np.linspace(-55, 125, 80)
    ax = axes[0]
    ax.plot(T, 100 + 0.02 * T, color=C_BLUE, lw=2.2, label="SAPC (polymer)")
    ax.plot(T, 100 + 0.05 * T - 0.0016 * (T - 20) ** 2, color=C_RED, lw=2.0,
            ls="--", label="liquid Al (ref.)")
    ax.set_xlabel("Temperature (C)", fontsize=10)
    ax.set_ylabel("Capacitance retention (%)", fontsize=9.5)
    ax.set_title("Capacitance vs temperature", fontsize=9.8)
    ax.legend(fontsize=8.2); ax.grid(alpha=0.25); ax.set_ylim(85, 110)
    ax2 = axes[1]
    f = np.logspace(2, 6, 80)
    ax2.semilogx(f, 12 + 60 / (1 + (f / 3e3)), color=C_BLUE, lw=2.2, label="SAPC")
    ax2.semilogx(f, 60 + 240 / (1 + (f / 1e3)), color=C_RED, lw=2.0, ls="--",
                 label="liquid Al (ref.)")
    ax2.set_xlabel("Frequency (Hz)", fontsize=10)
    ax2.set_ylabel("ESR (mohm, a.u.)", fontsize=9.5)
    ax2.set_title("ESR vs frequency", fontsize=9.8)
    ax2.legend(fontsize=8.2); ax2.grid(which="both", alpha=0.2)
    fig.suptitle("SAPC: flatter C(T) and lower/flatter ESR(f) than liquid Al (schematic)",
                 fontsize=9.6, y=1.02)
    return _save(fig, "fig_cv_temp.png")


def fig_derating():
    """Failure-rate acceleration vs applied/rated voltage ratio at several temperatures."""
    r = np.linspace(0.2, 1.0, 50)
    fig, ax = plt.subplots(figsize=(7.0, 4.1))
    for T, col in [(55, C_GREEN), (85, C_BLUE), (105, C_RED)]:
        af = (r / 0.5) ** 3 * np.exp((0.7 / 8.617e-5) * (1 / 358 - 1 / (273 + T)))
        ax.plot(r, af, color=col, lw=2.2, label=f"{T} C")
    ax.axvline(0.5, color=C_GRAY, ls=":", lw=1.2)
    ax.text(0.51, ax.get_ylim()[1] * 0.6, "50% derating\n(typical design point)",
            fontsize=8.2, color=C_GRAY)
    ax.set_xlabel("Applied / rated voltage", fontsize=10)
    ax.set_ylabel("Relative failure-rate factor (a.u.)", fontsize=9.5)
    ax.set_title("Voltage / temperature derating effect on relative failure rate (schematic)",
                 fontsize=9.6)
    ax.legend(title="ambient", fontsize=8.4); ax.grid(alpha=0.25)
    return _save(fig, "fig_derating.png")


def fig_activation():
    """Arrhenius extraction: ln(rate) vs 1000/T -> slope = -Ea/kB (schematic)."""
    Tk = np.array([358, 383, 398, 423])      # 85,110,125,150 C
    invT = 1000.0 / Tk
    Ea = 0.8
    lnk = 12 - (Ea / 8.617e-5) * (1.0 / Tk)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.scatter(invT, lnk, s=55, color=C_RED, zorder=3, label="ALT data (example)")
    cf = np.polyfit(invT, lnk, 1)
    xx = np.linspace(invT.min() * 0.99, invT.max() * 1.01, 40)
    ax.plot(xx, np.polyval(cf, xx), color=C_BLUE, lw=2.0,
            label=f"fit: Ea ~ {Ea:.2f} eV")
    for x, y, Tc in zip(invT, lnk, [85, 110, 125, 150]):
        ax.annotate(f"{Tc}C", (x, y), textcoords="offset points", xytext=(6, -4),
                    fontsize=8.0, color=C_GRAY)
    ax.set_xlabel("1000 / T  (1/K)", fontsize=10)
    ax.set_ylabel("ln(degradation rate)", fontsize=10)
    ax.set_title("Arrhenius activation-energy extraction from accelerated tests",
                 fontsize=9.6)
    ax.legend(fontsize=8.6); ax.grid(alpha=0.25)
    return _save(fig, "fig_activation.png")


def fig_migration():
    """Electrochemical / silver migration schematic across an interface under bias+humidity."""
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
    _box(ax, 0.4, 1.8, 1.7, 1.6, "Anode\n(+)", "#f6c6c6", fs=9)
    _box(ax, 9.9, 1.8, 1.7, 1.6, "Cathode\n(-)", "#cde1f3", fs=9)
    ax.add_patch(FancyBboxPatch((2.3, 1.7), 7.4, 1.8, boxstyle="round,pad=0.02",
                                facecolor="#eef3f8", edgecolor=C_GRAY, lw=0.8))
    ax.text(6.0, 3.2, "adsorbed moisture film (humid + bias)", fontsize=8.2,
            ha="center", color=C_GRAY)
    for i in range(5):
        x = 3.0 + i * 1.4
        ax.add_patch(plt.Circle((x, 2.6), 0.16, color="#888888"))
        ax.add_patch(FancyArrowPatch((x, 2.6), (x + 0.9, 2.6), arrowstyle="-|>",
                                     mutation_scale=9, color=C_GREEN, lw=1.1))
    ax.text(6.0, 1.95, "Ag+ ions migrate -> dendrite growth -> leakage / short",
            fontsize=8.0, ha="center", color=C_GREEN)
    ax.set_title("Electrochemical (silver) migration under humidity + bias (schematic)",
                 fontsize=9.8)
    return _save(fig, "fig_migration.png")


def fig_mission():
    """Mission profile -> hotspot temperature -> incremental life consumption."""
    t = np.linspace(0, 24, 240)
    load = 0.3 + 0.7 * (np.sin(t / 24 * 2 * np.pi - 1.3) > 0.2) * np.abs(np.sin(t / 3))
    Thot = 40 + 55 * load
    damage = np.cumsum(np.exp((0.8 / 8.617e-5) * (1 / 358 - 1 / (273 + Thot))) * (t[1] - t[0]))
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 5.0), sharex=True)
    axes[0].plot(t, Thot, color=C_RED, lw=1.8)
    axes[0].fill_between(t, 40, Thot, color="#f6d9b8", alpha=0.5)
    axes[0].set_ylabel("Hotspot T (C)", fontsize=9.5)
    axes[0].set_title("Mission profile: load-driven hotspot temperature", fontsize=9.6)
    axes[0].grid(alpha=0.2)
    axes[1].plot(t, damage / damage[-1], color=C_BLUE, lw=2.0)
    axes[1].set_ylabel("Cumulative life\nconsumption (norm.)", fontsize=9.0)
    axes[1].set_xlabel("Time (h, illustrative cycle)", fontsize=10)
    axes[1].set_title("Miner-type cumulative life consumption (Arrhenius-weighted)",
                      fontsize=9.6)
    axes[1].grid(alpha=0.2)
    return _save(fig, "fig_mission.png")


def build_all():
    funcs = [fig_structure, fig_taxonomy, fig_param_trends, fig_pedot_grain,
             fig_moisture, fig_model_map, fig_arrhenius_peck, fig_weibull,
             fig_gap_map, fig_litdist,
             # revision 3 additions
             fig_anodize, fig_pedot_chem, fig_vrh, fig_impedance, fig_nyquist,
             fig_bathtub, fig_competing, fig_stochastic, fig_thermal, fig_test_map,
             fig_fishbone, fig_rul, fig_fa_workflow, fig_timeline, fig_bibliometric,
             # revision 3 second-pass additions
             fig_cv_temp, fig_derating, fig_activation, fig_migration, fig_mission]
    paths = []
    for f in funcs:
        paths.append(f())
        print("built", f.__name__)
    return paths


if __name__ == "__main__":
    build_all()
