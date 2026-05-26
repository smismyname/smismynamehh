# -*- coding: utf-8 -*-
"""
Generate figures for SAPC (Stacked Aluminum Polymer Capacitor) literature review.
All figures redrawn schematically based on data and concepts reported in
peer-reviewed literature (citations given in captions of the Word report).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyBboxPatch, Patch
from matplotlib.patches import Circle, Polygon
import matplotlib.patches as mpatches

# Use English-only labels in figures to avoid font issues
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.linewidth"] = 0.8

OUT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(OUT, "images")
os.makedirs(IMG, exist_ok=True)


# ------------------------------------------------------------------------
# Figure 1. Schematic cross-section of a stacked aluminum polymer capacitor
# Concept based on: Liu & Sampson (NASA NEPP, 2010); Sankaran (UMD, 2010);
# Du et al., Liquid electrolyte-free cylindrical Al polymer capacitor review (2015).
# ------------------------------------------------------------------------
def fig_structure():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8)
    ax.axis("off")

    # --- left side: stacked element ---
    # 4 anode foils stacked, separated by polymer cathode + dielectric
    base_x = 0.6
    base_y = 0.8
    layer_h = 0.18
    gap_polymer = 0.55
    n_layer = 4

    y = base_y
    for i in range(n_layer):
        # bottom polymer cathode (PEDOT)
        ax.add_patch(Rectangle((base_x, y), 4.5, gap_polymer,
                               facecolor="#5b8def", edgecolor="black", lw=0.6))
        y += gap_polymer
        # Al2O3 dielectric (very thin)
        ax.add_patch(Rectangle((base_x, y), 4.5, 0.07,
                               facecolor="#ffd966", edgecolor="black", lw=0.4))
        y += 0.07
        # Al anode etched foil
        ax.add_patch(Rectangle((base_x, y), 4.5, layer_h,
                               facecolor="#bfbfbf", edgecolor="black", lw=0.6))
        # tabs
        ax.add_patch(Rectangle((base_x + 4.5, y), 0.5, layer_h,
                               facecolor="#7f7f7f", edgecolor="black", lw=0.5))
        y += layer_h
        # Al2O3 dielectric on top
        ax.add_patch(Rectangle((base_x, y), 4.5, 0.07,
                               facecolor="#ffd966", edgecolor="black", lw=0.4))
        y += 0.07
    # top final polymer
    ax.add_patch(Rectangle((base_x, y), 4.5, gap_polymer,
                           facecolor="#5b8def", edgecolor="black", lw=0.6))
    y_top = y + gap_polymer

    # silver paste layer + cathode terminal
    ax.add_patch(Rectangle((base_x, y_top), 4.5, 0.15,
                           facecolor="#cccccc", edgecolor="black", lw=0.5))
    ax.add_patch(Rectangle((base_x, base_y - 0.15), 4.5, 0.15,
                           facecolor="#cccccc", edgecolor="black", lw=0.5))

    # encapsulation outline
    ax.add_patch(Rectangle((base_x - 0.25, base_y - 0.30), 5.2, y_top - base_y + 0.65,
                           fill=False, edgecolor="black", lw=1.2, linestyle="-"))

    # cathode terminal
    ax.add_patch(Rectangle((base_x - 0.55, base_y - 0.30), 0.30, y_top - base_y + 0.65,
                           facecolor="#404040", edgecolor="black"))
    # anode terminal
    ax.add_patch(Rectangle((base_x + 5.0, base_y - 0.30), 0.30, y_top - base_y + 0.65,
                           facecolor="#404040", edgecolor="black"))

    ax.text(base_x - 0.40, (base_y + y_top) / 2 + 0.2, "Cathode\nterminal (-)",
            ha="center", va="center", fontsize=9, color="white", rotation=90)
    ax.text(base_x + 5.15, (base_y + y_top) / 2 + 0.2, "Anode\nterminal (+)",
            ha="center", va="center", fontsize=9, color="white", rotation=90)

    # callouts
    ax.annotate("Etched aluminum anode foil\n(thickness ~80–110 µm)",
                xy=(base_x + 2.3, base_y + 0.55 + 0.07 + layer_h / 2),
                xytext=(7.0, 6.6), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate(r"Al$_2$O$_3$ dielectric (5–500 nm)",
                xy=(base_x + 2.3, base_y + 0.55 + 0.04),
                xytext=(7.0, 5.7), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("Conductive polymer cathode\n(PEDOT:PSS or PEDOT/TOS, in situ\nor pre-polymerized dispersion)",
                xy=(base_x + 2.3, base_y + 0.27),
                xytext=(7.0, 4.4), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("Silver paste / cathode collector",
                xy=(base_x + 2.3, base_y - 0.07),
                xytext=(7.0, 2.8), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("Epoxy or resin encapsulation",
                xy=(base_x + 4.7, y_top + 0.20),
                xytext=(7.0, 1.7), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))

    # legend block
    legend_elems = [
        Patch(facecolor="#bfbfbf", edgecolor="black", label="Etched Al foil (anode)"),
        Patch(facecolor="#ffd966", edgecolor="black", label=r"Al$_2$O$_3$ dielectric"),
        Patch(facecolor="#5b8def", edgecolor="black", label="PEDOT (polymer cathode)"),
        Patch(facecolor="#cccccc", edgecolor="black", label="Silver paste collector"),
        Patch(facecolor="#404040", edgecolor="black", label="Lead frame terminal"),
    ]
    ax.legend(handles=legend_elems, loc="lower right", fontsize=8.5,
              frameon=True, edgecolor="gray")

    ax.set_title("Cross-sectional schematic of a stacked aluminum polymer capacitor (SAPC)",
                 fontsize=11, pad=8)
    fig.tight_layout()
    fp = os.path.join(IMG, "fig1_structure.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


# ------------------------------------------------------------------------
# Figure 2. Failure-mode taxonomy of SAPC under different stress conditions
# Concept based on: Murata Failure Mode document; Shrivastava et al. 2017;
# Romero et al. 2020; Liu/Sampson NEPP 2010.
# ------------------------------------------------------------------------
def fig_failure_modes():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7)
    ax.axis("off")

    # central node
    cx, cy = 5, 5.7
    ax.add_patch(FancyBboxPatch((cx - 1.7, cy - 0.45), 3.4, 0.9,
                                boxstyle="round,pad=0.05",
                                facecolor="#1f4e79", edgecolor="black"))
    ax.text(cx, cy, "SAPC failure modes", ha="center", va="center",
            color="white", fontsize=11, fontweight="bold")

    # three stress branches
    branches = [
        (1.5, 3.7, "Humidity-driven\n(85 °C / 85 % RH HAST)", "#5b8def",
         ["ESR rise (PEDOT swelling)",
          "Leakage current rise\n(oxide hydration)",
          "Capacitance loss < ESR effect",
          "Encapsulation delamination"]),
        (5.0, 3.7, "Thermal aging\n(125–150 °C storage)", "#e07b39",
         ["ESR rise dominant",
          "PEDOT thermal-oxidative\nde-doping",
          "Capacitance gradual decline",
          "Open-mode end-of-life"]),
        (8.5, 3.7, "Electro-thermal\n(ripple + bias)", "#7aa055",
         ["Self-heating ΔT 10–30 K",
          "Field-induced\noxide thickening",
          "Catastrophic short\n(rare, surge events)",
          "Solder-reflow stress"]),
    ]

    for x, y, label, color, items in branches:
        ax.add_patch(FancyBboxPatch((x - 1.2, y - 0.35), 2.4, 0.7,
                                    boxstyle="round,pad=0.04",
                                    facecolor=color, edgecolor="black"))
        ax.text(x, y, label, ha="center", va="center", color="white",
                fontsize=9.5, fontweight="bold")
        # connect to center
        ax.add_patch(FancyArrowPatch((cx, cy - 0.45), (x, y + 0.35),
                                     arrowstyle="-|>", lw=1.2,
                                     mutation_scale=12, color="black"))
        # bullets
        for i, txt in enumerate(items):
            yy = y - 0.85 - 0.65 * i
            ax.text(x - 1.15, yy, "•  " + txt, ha="left", va="center",
                    fontsize=8.5)

    ax.text(0.1, 0.35,
            "Sources: Murata Failure-Mode Document (2024); Shrivastava et al., IEEE TCPMT 7(11), 2017; "
            "Romero et al., Microelectronics Reliability 110, 2020; "
            "Liu & Sampson, NASA NEPP 2010; KEMET Technical Note 2019.",
            fontsize=7.5, color="#444444", wrap=True)
    ax.set_title("Stress–failure-mode mapping for stacked aluminum polymer capacitors",
                 fontsize=11, pad=8)
    fp = os.path.join(IMG, "fig2_failure_modes.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


# ------------------------------------------------------------------------
# Figure 3. Schematic of moisture-driven degradation pathway in SAPC
# Concept based on: KEMET (Young et al., 2020) and Sankaran/Pecht UMD theses.
# ------------------------------------------------------------------------
def fig_humidity_mechanism():
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.0))
    titles = ["t = 0 h (pristine)",
              "Moisture ingress (HAST)",
              "Long-time degradation"]
    colors_polymer = ["#5b8def", "#7aa3eb", "#a4c0e8"]
    moisture_dots = [0, 30, 90]

    for ax, title, c, n_dot in zip(axes, titles, colors_polymer, moisture_dots):
        ax.set_xlim(0, 6); ax.set_ylim(0, 5)
        ax.axis("off")

        # encapsulation
        ax.add_patch(Rectangle((0.15, 0.15), 5.7, 4.7, fill=False,
                               edgecolor="black", lw=1.0))
        # silver paste cathode
        ax.add_patch(Rectangle((0.4, 0.4), 5.2, 0.25, facecolor="#cccccc", edgecolor="k", lw=0.5))
        # PEDOT cathode
        ax.add_patch(Rectangle((0.4, 0.65), 5.2, 1.4, facecolor=c, edgecolor="k", lw=0.5))
        # Al2O3 dielectric
        ax.add_patch(Rectangle((0.4, 2.05), 5.2, 0.10, facecolor="#ffd966", edgecolor="k", lw=0.5))
        # Al anode
        ax.add_patch(Rectangle((0.4, 2.15), 5.2, 0.7, facecolor="#bfbfbf", edgecolor="k", lw=0.5))
        # tunnels (etch pits)
        for x in np.linspace(0.7, 5.1, 16):
            ax.add_patch(Rectangle((x, 2.18), 0.10, 0.55, facecolor="white", edgecolor="none"))
        # top epoxy
        ax.add_patch(Rectangle((0.4, 2.85), 5.2, 1.85, facecolor="#f4e3c1", edgecolor="k", lw=0.5))

        # moisture dots
        rng = np.random.default_rng(42 + n_dot)
        if n_dot > 0:
            xs = rng.uniform(0.45, 5.55, n_dot)
            ys = rng.uniform(0.7, 4.7, n_dot)
            ax.scatter(xs, ys, s=8, color="#1565c0", alpha=0.55,
                       edgecolor="white", linewidth=0.2)

        # delamination crack (only for last)
        if title.startswith("Long"):
            ax.plot([1.0, 1.5, 2.2, 3.0, 3.6, 4.4],
                    [0.65, 0.62, 0.66, 0.60, 0.65, 0.62],
                    color="red", lw=2)
            ax.text(2.7, 0.32, "Delamination at PEDOT / silver interface",
                    ha="center", color="red", fontsize=8)

        ax.set_title(title, fontsize=10)

    fig.suptitle("Moisture-driven degradation pathway of conductive-polymer aluminum capacitors",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    fp = os.path.join(IMG, "fig3_humidity.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


# ------------------------------------------------------------------------
# Figure 4. Arrhenius plot of PEDOT:PSS conductivity vs 1/T
# Conceptually reproduced after the qualitative behaviour reported in:
# Vitoratos et al., Organic Electronics 10 (2009) 61–66; and the
# discussion in Friedel et al., 2020 (ACS Applied Materials & Interfaces).
# Numerical points are illustrative only.
# ------------------------------------------------------------------------
def fig_arrhenius():
    fig, ax = plt.subplots(figsize=(7, 4.6))
    # Temperature range 25 - 200 °C
    T_C = np.array([25, 60, 80, 100, 120, 140, 160, 180, 200])
    T = T_C + 273.15
    # Two scenarios: nitrogen vs air
    Ea_air = 0.55  # eV (illustrative)
    Ea_N2  = 0.20  # eV
    sigma0 = 1000.0
    kB = 8.617e-5
    sigma_air = sigma0 * np.exp(-Ea_air * (1/T - 1/T[0]) / kB) * 0.05
    sigma_N2  = sigma0 * np.exp(-Ea_N2  * (1/T - 1/T[0]) / kB) * 0.5

    ax.semilogy(1000 / T, sigma_air, "o-", color="#c0392b",
                label=f"In ambient air, Ea ≈ {Ea_air:.2f} eV")
    ax.semilogy(1000 / T, sigma_N2, "s-", color="#2980b9",
                label=f"In N$_2$ atmosphere, Ea ≈ {Ea_N2:.2f} eV")
    ax.set_xlabel("1000/T (1/K)")
    ax.set_ylabel("Normalized conductivity σ (S/cm)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)
    ax.set_title("Arrhenius dependence of PEDOT:PSS film conductivity\n"
                 "(qualitative reproduction after Vitoratos et al., 2009; Friedel et al., 2020)",
                 fontsize=10)
    fig.tight_layout()
    fp = os.path.join(IMG, "fig4_arrhenius.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


# ------------------------------------------------------------------------
# Figure 5. Evolution of ESR and capacitance during 85 °C / 85 % RH HAST
# Qualitatively reproduced after Shrivastava, Azarian, Pecht, IEEE TCPMT 2017
# and Romero, Azarian, Pecht, Microelectronics Reliability 2020.
# ------------------------------------------------------------------------
def fig_hast_evolution():
    fig, ax1 = plt.subplots(figsize=(7.5, 4.6))
    t = np.array([0, 50, 100, 200, 300, 500, 700, 900, 1100])
    # ESR normalized rise (manufacturer A: stable, B: severe)
    esr_A = 1 + 0.05 * (t / 1100)
    esr_B = 1 + 0.1 + 1.4 * (t / 1100) ** 2
    # Capacitance
    cap_A = 1 - 0.02 * (t / 1100)
    cap_B = 1 - 0.06 * (t / 1100)

    ax1.plot(t, esr_A, "o-", color="#1976d2", label="ESR / ESR$_0$, supplier A")
    ax1.plot(t, esr_B, "s-", color="#d32f2f", label="ESR / ESR$_0$, supplier B")
    ax1.set_xlabel("Time at 85 °C / 85 % RH (hours)")
    ax1.set_ylabel("Normalized ESR (–)")
    ax1.axhline(2.0, color="gray", lw=1, linestyle=":")
    ax1.text(60, 2.05, "Failure threshold (2× ESR$_0$)", color="gray", fontsize=8.5)
    ax1.grid(alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(t, cap_A, "v--", color="#1976d2", alpha=0.6, label="C / C$_0$, supplier A")
    ax2.plot(t, cap_B, "^--", color="#d32f2f", alpha=0.6, label="C / C$_0$, supplier B")
    ax2.set_ylabel("Normalized capacitance (–)")
    ax2.set_ylim(0.8, 1.05)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8.5)
    ax1.set_title("ESR and capacitance evolution of two SAPC suppliers under HAST\n"
                  "(qualitative reproduction after Shrivastava et al. 2017 and Romero et al. 2020)",
                  fontsize=10)
    fig.tight_layout()
    fp = os.path.join(IMG, "fig5_hast_evolution.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


# ------------------------------------------------------------------------
# Figure 6. Closed-loop electro-thermal coupling block diagram of SAPC
# Concept based on: Wang & Blaabjerg IEEE TPE 2014; Ebel et al. PCIM 2019;
# Lu et al. Sci. Rep. 2025.
# ------------------------------------------------------------------------
def fig_electro_thermal():
    fig, ax = plt.subplots(figsize=(9.5, 4.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.axis("off")

    boxes = [
        (1.0, 4.5, "Ripple current\nI$_{rms}$"),
        (3.7, 4.5, "Power dissipation\nP = I$_{rms}^2$ · ESR(T)"),
        (6.6, 4.5, "Hot-spot temperature\nT$_h$ = T$_a$ + Rθ · P"),
        (6.6, 2.0, "PEDOT de-doping +\nAl$_2$O$_3$ thickening"),
        (3.7, 2.0, "ESR(T) rise +\nC drop"),
        (1.0, 2.0, "End-of-life\n(ΔESR ≥ 2 × ESR$_0$)"),
    ]
    colors = ["#1976d2", "#1976d2", "#d32f2f",
              "#7b1fa2", "#7b1fa2", "#388e3c"]

    for (x, y, txt), c in zip(boxes, colors):
        ax.add_patch(FancyBboxPatch((x - 1.0, y - 0.55), 2.0, 1.1,
                                    boxstyle="round,pad=0.05",
                                    facecolor=c, edgecolor="black"))
        ax.text(x, y, txt, ha="center", va="center", color="white",
                fontsize=9.5, fontweight="bold")

    # arrows (top row)
    ax.add_patch(FancyArrowPatch((2.0, 4.5), (2.7, 4.5), arrowstyle="-|>",
                                 mutation_scale=15, lw=1.5))
    ax.add_patch(FancyArrowPatch((4.7, 4.5), (5.6, 4.5), arrowstyle="-|>",
                                 mutation_scale=15, lw=1.5))
    # vertical arrow
    ax.add_patch(FancyArrowPatch((6.6, 3.95), (6.6, 2.55), arrowstyle="-|>",
                                 mutation_scale=15, lw=1.5))
    # bottom row
    ax.add_patch(FancyArrowPatch((5.6, 2.0), (4.7, 2.0), arrowstyle="-|>",
                                 mutation_scale=15, lw=1.5))
    ax.add_patch(FancyArrowPatch((2.7, 2.0), (2.0, 2.0), arrowstyle="-|>",
                                 mutation_scale=15, lw=1.5))
    # closing feedback (back to top)
    ax.add_patch(FancyArrowPatch((1.0, 2.55), (1.0, 3.95),
                                 arrowstyle="-|>", mutation_scale=15, lw=1.5,
                                 color="darkred", connectionstyle="arc3,rad=0.0"))
    ax.text(0.6, 3.25, "End of life\nresets clock", color="darkred", fontsize=8.5,
            rotation=90)

    # external T_a annotation
    ax.text(8.6, 4.5, "+ ambient T$_a$", fontsize=9.5, va="center")

    # Sources
    ax.text(0.0, 0.4,
            "Sources of model: Wang & Blaabjerg, IEEE Trans. Power Electron. 29(11), 2014; "
            "Ebel, Klingshirn & Hammerl, PCIM 2019; Lu et al., Sci. Rep. 15, 2025.",
            fontsize=7.8, color="#444")

    ax.set_title("Closed-loop electro-thermal coupling chain in SAPC reliability",
                 fontsize=11, pad=6)
    fp = os.path.join(IMG, "fig6_electro_thermal.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


# ------------------------------------------------------------------------
# Figure 7. Weibull plot of time-to-failure under HAST
# Qualitatively reproduced after Romero, Azarian, Pecht, Microelectronics
# Reliability 110, 2020.
# ------------------------------------------------------------------------
def fig_weibull():
    fig, ax = plt.subplots(figsize=(7, 4.6))
    rng = np.random.default_rng(7)
    # supplier A at 85/85
    beta_A, eta_A = 2.5, 1500
    n = 30
    t_A = eta_A * (-np.log(1 - rng.uniform(0.01, 0.99, n))) ** (1 / beta_A)
    beta_B, eta_B = 1.6, 600
    t_B = eta_B * (-np.log(1 - rng.uniform(0.01, 0.99, n))) ** (1 / beta_B)
    beta_C, eta_C = 2.0, 220
    t_C = eta_C * (-np.log(1 - rng.uniform(0.01, 0.99, n))) ** (1 / beta_C)

    def weibull_plot(t, label, color):
        t_sorted = np.sort(t)
        F = (np.arange(1, len(t_sorted) + 1) - 0.3) / (len(t_sorted) + 0.4)
        x = np.log(t_sorted)
        y = np.log(-np.log(1 - F))
        ax.plot(t_sorted, np.log(-np.log(1 - F)), "o", color=color, label=label, ms=5)

    weibull_plot(t_A, "85 °C / 85 % RH, supplier A (η ≈ 1500 h, β ≈ 2.5)", "#1976d2")
    weibull_plot(t_B, "85 °C / 85 % RH, supplier B (η ≈ 600 h, β ≈ 1.6)", "#d32f2f")
    weibull_plot(t_C, "110 °C / 85 % RH, supplier B (η ≈ 220 h, β ≈ 2.0)", "#388e3c")

    ax.set_xscale("log")
    ax.set_xlabel("Time-to-failure (hours)")
    ax.set_ylabel("ln(-ln(1-F))")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8.5, loc="lower right")
    ax.set_title("Illustrative Weibull plot of SAPC time-to-failure under HAST\n"
                 "(qualitative reproduction after Romero et al., Microelectronics Reliability 2020)",
                 fontsize=10)
    fig.tight_layout()
    fp = os.path.join(IMG, "fig7_weibull.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


# ------------------------------------------------------------------------
# Figure 8. Acceleration-factor surface (T, RH) for SAPC life model
# Eyring T-H model after Hallberg-Peck conventions and IEC 60384 guidelines;
# also discussed in Romero et al. (2020) for PAE capacitors.
# ------------------------------------------------------------------------
def fig_eyring_surface():
    fig = plt.figure(figsize=(7.5, 5.0))
    ax = fig.add_subplot(111, projection="3d")
    T_C = np.linspace(40, 105, 40)
    RH = np.linspace(30, 95, 40)
    Tg, RHg = np.meshgrid(T_C, RH)
    # Eyring-like AF: AF = exp[Ea/k(1/T_use - 1/T_test)] * (RH_test/RH_use)^n
    Ea = 0.9
    n = 3.0
    kB = 8.617e-5
    T_use = 40 + 273.15
    RH_use = 50
    AF = np.exp(Ea / kB * (1 / T_use - 1 / (Tg + 273.15))) * (RHg / RH_use) ** n
    surf = ax.plot_surface(Tg, RHg, np.log10(AF), cmap="viridis", edgecolor="none", alpha=0.9)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Relative humidity (%)")
    ax.set_zlabel("log10(AF) vs 40 °C / 50 % RH")
    ax.view_init(elev=22, azim=-115)
    fig.colorbar(surf, shrink=0.6, label="log10(Acceleration Factor)")
    ax.set_title("Eyring temperature–humidity acceleration factor surface\n"
                 "(Ea = 0.9 eV, n = 3.0, after Romero et al. 2020 and IEC 60384 conventions)",
                 fontsize=10)
    fig.tight_layout()
    fp = os.path.join(IMG, "fig8_eyring.png")
    fig.savefig(fp, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return fp


def main():
    files = []
    for fn in (fig_structure, fig_failure_modes, fig_humidity_mechanism,
               fig_arrhenius, fig_hast_evolution, fig_electro_thermal,
               fig_weibull, fig_eyring_surface):
        f = fn()
        files.append(f)
        print("Generated:", f)
    return files


if __name__ == "__main__":
    main()
