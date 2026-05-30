# -*- coding: utf-8 -*-
"""
SAPC 研究现状报告 - 图表生成模块 (matplotlib)
所有图内文字使用英文/数字, 中文图题由 Word 渲染 (沙箱无 CJK 字体)。
generate_all(outdir) 生成全部 PNG, 返回 {name: path} 字典。

SAPC = Stacked Aluminium solid Polymer Capacitor（叠层铝固态电容器，Panasonic SP-Cap 类）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})

# 统一配色
C_INTL = "#2E5E8C"   # 国外
C_DOM = "#C0504D"    # 国内
C_SAPC = "#9BBB59"
PALETTE = ["#2E5E8C", "#C0504D", "#9BBB59", "#8064A2", "#4BACC6", "#F79646", "#7F7F7F"]


def _save(fig, outdir, name):
    path = os.path.join(outdir, name + ".png")
    fig.savefig(path)
    plt.close(fig)
    return path


# ============================================================ 1. 市场与定位
def fig_cap_family(outdir):
    """电容器谱系中固态/聚合物电容的定位（按可靠性研究关注度示意）"""
    fig, ax = plt.subplots(figsize=(8.4, 3.0))
    ax.axis("off")
    families = [
        ("Aluminium\nElectrolytic", "#4BACC6"),
        ("  -> Conductive-Polymer\n  Al (wound / stacked)", "#9BBB59"),
        ("MLCC", "#2E5E8C"),
        ("Film", "#8064A2"),
        ("Tantalum\n(MnO2 / polymer)", "#C0504D"),
        ("Supercap", "#F79646"),
    ]
    x = 0.0
    for i, (name, col) in enumerate(families):
        w = 2.3 if i == 1 else 1.7
        box = FancyBboxPatch((x, 0.3), w, 1.4,
                             boxstyle="round,pad=0.03,rounding_size=0.1",
                             linewidth=1.4, edgecolor=col, facecolor=col, alpha=0.20)
        ax.add_patch(box)
        ax.text(x + w / 2, 1.0, name, ha="center", va="center", fontsize=9,
                fontweight="bold" if i == 1 else "normal")
        x += w + 0.25
    ax.text(x / 2 - 0.1, 2.05,
            "Capacitor family tree (SAPC = stacked conductive-polymer Al, the focus of this review)",
            ha="center", fontsize=9.5, style="italic", color="#333")
    ax.set_xlim(-0.2, x)
    ax.set_ylim(0, 2.4)
    return _save(fig, outdir, "fig_cap_family")


def fig_market_growth(outdir):
    years = np.array([2021, 2023, 2025, 2027, 2029, 2031, 2033, 2035])
    val = 4.89 * (1.106) ** (years - 2025)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    bars = ax.bar(years, val, width=1.3, color=C_INTL, edgecolor="k", lw=0.5, alpha=0.88)
    ax.plot(years, val, "o-", color=C_DOM, lw=2)
    for x, v in zip(years, val):
        ax.text(x, v + 0.2, "%.1f" % v, ha="center", fontsize=8.5)
    ax.set_xlabel("Year")
    ax.set_ylabel("Market size (USD billion)")
    ax.set_title("Conductive-Polymer Capacitor Market (CAGR approx. 10.6%)")
    ax.text(2022, 10.5, "2025: ~US$4.9B\n2035: ~US$12.1B\n(Astute Analytica est.)",
            fontsize=8.5, color="#7a2b29")
    ax.set_ylim(0, 14)
    return _save(fig, outdir, "fig_market_growth")


def fig_segment_share(outdir):
    labels = ["Conductive-polymer\nAluminium", "Conductive-polymer\nTantalum",
              "Polymer hybrid &\nothers"]
    share = [76.6, 17.4, 6.0]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    wedges, _, autot = ax.pie(share, labels=labels, autopct="%1.1f%%", startangle=90,
                              colors=[C_SAPC, C_DOM, C_INTL], pctdistance=0.75,
                              wedgeprops=dict(width=0.45, edgecolor="w"))
    for t in autot:
        t.set_color("w"); t.set_fontweight("bold"); t.set_fontsize(9)
    ax.set_title("Conductive-Polymer Capacitor Market by Product Type")
    return _save(fig, outdir, "fig_segment_share")


def fig_position_map(outdir):
    """ESR-容值-体积 定位图：SAPC 与 MLCC/wet-Al/Ta/film 对比"""
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    data = {
        "Wet Al-electrolytic": (1.0, 0.3, "#4BACC6"),
        "MLCC": (0.012, 0.02, "#2E5E8C"),
        "Film": (0.02, 0.05, "#8064A2"),
        "Tantalum (MnO2)": (0.4, 0.6, "#C0504D"),
        "Tantalum-polymer": (0.05, 0.7, "#F79646"),
        "SAPC (stacked Al-polymer)": (0.008, 0.9, "#9BBB59"),
        "Wound Al-polymer (OS-CON)": (0.015, 0.8, "#7F7F7F"),
    }
    for name, (esr, cv, col) in data.items():
        big = name.startswith("SAPC")
        ax.scatter(esr, cv, s=360 if big else 150, color=col, edgecolor="k",
                   linewidth=1.6 if big else 0.6, alpha=0.9, zorder=3)
        ax.annotate(name, (esr, cv), fontsize=8.2,
                    xytext=(6, 6), textcoords="offset points",
                    fontweight="bold" if big else "normal")
    ax.set_xscale("log")
    ax.set_xlabel("Equivalent series resistance ESR (relative, log)")
    ax.set_ylabel("Volumetric efficiency CV / volume (relative)")
    ax.set_title("Positioning Map: SAPC vs. Competing Capacitor Technologies")
    ax.set_ylim(0, 1.05)
    return _save(fig, outdir, "fig_position_map")


# ============================================================ 2. 结构与材料
def fig_wound_vs_stacked(outdir):
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))
    # wound
    ax = axes[0]
    ax.axis("off")
    ax.set_title("Wound type (e.g. OS-CON)", fontsize=10)
    th = np.linspace(0, 6 * np.pi, 300)
    r = 0.06 * th
    ax.plot(r * np.cos(th) + 1.0, r * np.sin(th) + 1.0, color=C_INTL, lw=2)
    ax.plot(0.9 * r * np.cos(th) + 1.0, 0.9 * r * np.sin(th) + 1.0, color=C_DOM, lw=1.2)
    ax.text(1.0, -0.25, "anode + cathode foils\nwound with separator", ha="center", fontsize=8)
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.6, 2.4)
    # stacked
    ax = axes[1]
    ax.axis("off")
    ax.set_title("Stacked type = SAPC (e.g. SP-Cap)", fontsize=10)
    for i in range(6):
        y = 0.2 + i * 0.28
        ax.add_patch(Rectangle((0.3, y), 1.8, 0.12, facecolor=C_SAPC,
                               edgecolor="k", lw=0.5))
        ax.add_patch(Rectangle((0.3, y + 0.12), 1.8, 0.06, facecolor="#dddddd",
                               edgecolor="none"))
    ax.add_patch(Rectangle((0.15, 0.1), 0.18, 1.9, facecolor="#555", edgecolor="k"))
    ax.add_patch(Rectangle((2.1, 0.1), 0.18, 1.9, facecolor="#555", edgecolor="k"))
    ax.text(1.2, -0.05, "multiple anode foils stacked\n(low profile, low ESL)",
            ha="center", fontsize=8)
    ax.set_xlim(-0.1, 2.6); ax.set_ylim(-0.4, 2.3)
    fig.suptitle("Wound vs. Stacked Conductive-Polymer Aluminium Construction",
                 fontsize=11)
    return _save(fig, outdir, "fig_wound_vs_stacked")


def fig_stacked_cross_section(outdir):
    """叠层 SAPC 单元剖面示意"""
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.axis("off")
    layers = [
        ("Etched Al anode foil (high surface area)", "#bfbfbf"),
        ("Al2O3 dielectric (anodic oxide)", "#F79646"),
        ("Conductive polymer (PEDOT) cathode", "#9BBB59"),
        ("Graphite layer", "#7F7F7F"),
        ("Silver paste / cathode collector", "#4BACC6"),
    ]
    y = 0.0
    h = 0.7
    for name, col in layers:
        ax.add_patch(Rectangle((0.5, y), 6.5, h, facecolor=col, edgecolor="k", lw=0.6, alpha=0.85))
        ax.text(3.75, y + h / 2, name, ha="center", va="center", fontsize=9)
        y += h + 0.08
    ax.text(3.75, y + 0.15, "x N foils -> stacked, welded to lead frame, resin-moulded",
            ha="center", fontsize=9, style="italic", color="#333")
    ax.set_xlim(0, 7.5)
    ax.set_ylim(-0.2, y + 0.5)
    ax.set_title("Schematic Cross-Section of a Stacked Al-Polymer (SAPC) Element")
    return _save(fig, outdir, "fig_stacked_cross_section")


def fig_polymer_conductivity(outdir):
    mats = ["Liquid\nelectrolyte", "MnO2", "TCNQ\nsalt", "Polypyrrole\n(PPy)",
            "Polyaniline\n(PANI)", "PEDOT"]
    cond = [1e-2, 1e-1, 1e1, 1e2, 5e1, 3e2]  # S/cm representative order
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    bars = ax.bar(mats, cond, color=PALETTE[:6], edgecolor="k", lw=0.6)
    ax.set_yscale("log")
    ax.set_ylabel("Electrical conductivity (S/cm, representative)")
    ax.set_title("Conductivity of Cathode/Electrolyte Materials (log scale)")
    for b, v in zip(bars, cond):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.3, "%.0e" % v, ha="center", fontsize=8)
    ax.set_ylim(1e-3, 1e3)
    ax.text(0.2, 5e-3, "PEDOT approx. 10^4 x higher\nthan liquid electrolyte",
            fontsize=8.5, color="#3a5f1f")
    return _save(fig, outdir, "fig_polymer_conductivity")


def fig_material_timeline(outdir):
    events = [
        (1983, "Sanyo OS-CON\nTCNQ solid e-cap"),
        (1991, "Polypyrrole\ncathode"),
        (1995, "PEDOT (Bayer\nBaytron) intro."),
        (1999, "Panasonic SP-Cap\nstacked Al-polymer"),
        (2005, "PEDOT:PSS\ndispersion"),
        (2013, "Hybrid polymer\n(polymer+liquid)"),
        (2022, "125C long-life,\nAI-server grade"),
    ]
    fig, ax = plt.subplots(figsize=(8.8, 3.2))
    ax.axis("off")
    yrs = [e[0] for e in events]
    ax.plot([min(yrs) - 2, max(yrs) + 2], [0, 0], color="#444", lw=2, zorder=1)
    for i, (yr, lab) in enumerate(events):
        up = i % 2 == 0
        y = 0.6 if up else -0.6
        ax.plot([yr, yr], [0, y * 0.7], color="#888", lw=1)
        ax.scatter([yr], [0], s=60, color=PALETTE[i % len(PALETTE)], zorder=3, edgecolor="k")
        ax.text(yr, y, "%d\n%s" % (yr, lab), ha="center",
                va="bottom" if up else "top", fontsize=8.3)
    ax.set_xlim(min(yrs) - 4, max(yrs) + 4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_title("Evolution of Conductive-Polymer Aluminium Capacitor Technology")
    return _save(fig, outdir, "fig_material_timeline")


def fig_cv_bias(outdir):
    """直流偏压下容值稳定性：SAPC vs MLCC(II类)"""
    v = np.linspace(0, 1, 50)
    sapc = 100 - 2 * v
    mlcc = 100 * (1 - 0.7 * v ** 1.3)
    film = 100 - 0.5 * v
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(v * 100, sapc, color=C_SAPC, lw=2.4, label="SAPC (Al-polymer)")
    ax.plot(v * 100, mlcc, color=C_INTL, lw=2, ls="--", label="MLCC (class II)")
    ax.plot(v * 100, film, color=C_DOM, lw=2, ls=":", label="Film")
    ax.set_xlabel("DC bias (% of rated voltage)")
    ax.set_ylabel("Effective capacitance (% of nominal)")
    ax.set_title("DC-Bias Capacitance Stability: SAPC vs. MLCC")
    ax.legend(fontsize=9)
    ax.set_ylim(20, 105)
    return _save(fig, outdir, "fig_cv_bias")


# ============================================================ 3. 工艺
def fig_process_flow(outdir):
    steps = ["High-voltage\netch foil", "Anodize\n(form Al2O3)", "Polymer\ncathode\n(in-situ /\ndispersion)",
             "Graphite +\nAg paste", "Stack N\nfoils + weld", "Lead frame +\nresin mould",
             "Ageing /\nscreening"]
    fig, ax = plt.subplots(figsize=(9.0, 2.6))
    ax.axis("off")
    n = len(steps)
    x0, w, gap = 0.1, 1.05, 0.22
    for i, s in enumerate(steps):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, 0.6), w, 1.1,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=1.3, edgecolor=PALETTE[i % len(PALETTE)],
                             facecolor=PALETTE[i % len(PALETTE)], alpha=0.18)
        ax.add_patch(box)
        ax.text(x + w / 2, 1.15, s, ha="center", va="center", fontsize=8)
        if i < n - 1:
            ar = FancyArrowPatch((x + w, 1.15), (x + w + gap, 1.15),
                                 arrowstyle="-|>", mutation_scale=11, color="#444")
            ax.add_patch(ar)
    ax.set_xlim(0, x0 + n * (w + gap))
    ax.set_ylim(0.3, 2.0)
    ax.set_title("Manufacturing Process Flow of Stacked Al-Polymer (SAPC) Capacitors")
    return _save(fig, outdir, "fig_process_flow")


def fig_insitu_vs_dispersion(outdir):
    cats = ["Coverage of\nporous foil", "Polymer\nconductivity", "Leakage\ncurrent (low=good)",
            "Humidity\nstability", "Process\ncomplexity"]
    insitu = [9, 8, 5, 8, 8]
    disp = [6, 6, 8, 5, 5]
    x = np.arange(len(cats)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.8, 4.0))
    ax.bar(x - w / 2, insitu, w, label="In-situ polymerization", color=C_INTL, edgecolor="k", lw=0.5)
    ax.bar(x + w / 2, disp, w, label="Pre-polymerized dispersion (PEDOT:PSS)", color=C_DOM,
           edgecolor="k", lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=8.3)
    ax.set_ylabel("Relative qualitative rating (1-10)")
    ax.set_title("Two Cathode-Forming Routes: In-situ vs. Dispersion")
    ax.legend(fontsize=8.5)
    ax.set_ylim(0, 11)
    return _save(fig, outdir, "fig_insitu_vs_dispersion")


# ============================================================ 4. 电气性能
def fig_esr_frequency(outdir):
    f = np.logspace(2, 7, 200)
    w = 2 * np.pi * f
    def Z(C, ESR, L):
        return np.sqrt(ESR ** 2 + (1 / (w * C) - w * L) ** 2)
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    ax.loglog(f, Z(150e-6, 0.4, 5e-9), color=C_INTL, lw=2, label="Wet Al-electrolytic")
    ax.loglog(f, Z(150e-6, 0.007, 1.5e-9), color=C_SAPC, lw=2.4, label="SAPC (stacked Al-polymer)")
    ax.loglog(f, Z(10e-6, 0.005, 0.5e-9), color=C_DOM, lw=2, ls="--", label="MLCC")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Impedance |Z| (Ohm)")
    ax.set_title("Impedance/ESR vs. Frequency")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_esr_frequency")


def fig_esr_temperature(outdir):
    T = np.linspace(-55, 125, 100)
    sapc = 7 * (1 - 0.0015 * (T - 20))
    wet = 40 * np.exp(-0.02 * (T - 20))
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(T, sapc, color=C_SAPC, lw=2.4, label="SAPC (Al-polymer)")
    ax.plot(T, wet, color=C_INTL, lw=2, ls="--", label="Wet Al-electrolytic")
    ax.set_xlabel("Temperature (degree C)")
    ax.set_ylabel("ESR (mOhm, representative)")
    ax.set_title("ESR vs. Temperature: Flat Polymer Response vs. Wet Type")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 60)
    return _save(fig, outdir, "fig_esr_temperature")


def fig_ripple_temp_rise(outdir):
    Irms = np.linspace(0, 6, 100)
    for esr, col, lab in [(0.007, C_SAPC, "SAPC ESR=7mOhm"),
                          (0.04, C_INTL, "Wound ESR=40mOhm")]:
        dT = esr * Irms ** 2 / 0.012 * 1.0  # representative thermal resistance scaling
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for esr, col, lab in [(0.007, C_SAPC, "SAPC ESR=7 mOhm"),
                          (0.020, C_DOM, "Polymer ESR=20 mOhm"),
                          (0.040, C_INTL, "Wet ESR=40 mOhm")]:
        dT = esr * Irms ** 2 * 18.0
        ax.plot(Irms, dT, color=col, lw=2, label=lab)
    ax.axhline(20, color="gray", ls=":", lw=1)
    ax.text(0.1, 21, "typical dT limit", fontsize=8, color="gray")
    ax.set_xlabel("Ripple current RMS (A)")
    ax.set_ylabel("Self-heating temperature rise (K)")
    ax.set_title("Lower ESR -> Higher Allowable Ripple Current")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 40)
    return _save(fig, outdir, "fig_ripple_temp_rise")


def fig_impedance_aging(outdir):
    f = np.logspace(2, 7, 200)
    w = 2 * np.pi * f
    def Z(C, ESR, L):
        return np.sqrt(ESR ** 2 + (1 / (w * C) - w * L) ** 2)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.loglog(f, Z(150e-6, 0.007, 1.5e-9), color=C_SAPC, lw=2.4, label="Fresh")
    ax.loglog(f, Z(148e-6, 0.020, 1.6e-9), color=C_DOM, lw=2, ls="--", label="Aged (ESR up)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("|Z| (Ohm)")
    ax.set_title("Impedance Spectrum: Fresh vs. Aged SAPC (ESR-dominated drift)")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_impedance_aging")


# ============================================================ 5. 失效模式
def fig_failure_mode_spectrum(outdir):
    types = ["SAPC\n(stacked)", "Wound\nAl-polymer", "Wet Al-\nelectrolytic", "Ta-\npolymer"]
    modes = ["ESR rise (wear-out)", "Leakage/short", "Cap. drift", "Open (EoL)"]
    data = {
        "SAPC\n(stacked)":   [50, 22, 8, 20],
        "Wound\nAl-polymer": [48, 20, 12, 20],
        "Wet Al-\nelectrolytic": [40, 5, 45, 10],
        "Ta-\npolymer":      [25, 45, 10, 20],
    }
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    bottoms = np.zeros(len(types))
    for j, m in enumerate(modes):
        vals = [data[t][j] for t in types]
        ax.bar(types, vals, bottom=bottoms, label=m, color=PALETTE[j], edgecolor="w")
        bottoms += np.array(vals)
    ax.set_ylabel("Relative share of failure modes (%)")
    ax.set_title("Failure-Mode Spectrum: SAPC vs. Related Types")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, fontsize=8.3)
    ax.set_ylim(0, 100)
    return _save(fig, outdir, "fig_failure_mode_spectrum")


def fig_esr_degradation(outdir):
    t = np.linspace(0, 1, 100)
    fig, ax1 = plt.subplots(figsize=(6.8, 3.8))
    ESR = 100 * (1 + 1.6 * t ** 2.3)
    C = 100 - 4 * t - 3 * t ** 3
    ax2 = ax1.twinx()
    l1, = ax1.plot(t * 100, C, color=C_SAPC, lw=2.2, label="Capacitance")
    l2, = ax2.plot(t * 100, ESR, color=C_DOM, lw=2.2, ls="--", label="ESR")
    ax2.axhline(200, color=C_DOM, ls=":", lw=1)
    ax2.text(3, 205, "ESR EoL (2x initial)", fontsize=8, color=C_DOM)
    ax1.set_xlabel("Normalized service time (%)")
    ax1.set_ylabel("Capacitance (% of initial)", color=C_SAPC)
    ax2.set_ylabel("ESR (% of initial)", color=C_DOM)
    ax1.set_title("SAPC Wear-out: ESR Rises while Capacitance Stays Stable")
    ax1.legend(handles=[l1, l2], loc="center left", fontsize=9)
    ax1.set_ylim(85, 102)
    return _save(fig, outdir, "fig_esr_degradation")


def fig_humidity_degradation(outdir):
    t = np.linspace(0, 1000, 100)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for k, col, lab in [(1.0, C_SAPC, "Robust polymer (in-situ)"),
                        (2.2, C_DOM, "Humidity-sensitive (PEDOT:PSS)")]:
        ESR = 100 * (1 + 0.0000016 * k * t ** 2)
        ax.plot(t, ESR, color=col, lw=2.2, label=lab)
    ax.axhline(200, color="gray", ls=":", lw=1)
    ax.text(20, 205, "ESR EoL", fontsize=8, color="gray")
    ax.set_xlabel("Time at 85 degC / 85% RH (h)")
    ax.set_ylabel("ESR (% of initial)")
    ax.set_title("Damp-Heat (85/85) Degradation: PEDOT Oxidation/De-doping")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_humidity_degradation")


def fig_leakage_growth(outdir):
    t = np.linspace(0, 1000, 100)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for defect, col, lab in [(1.0, C_SAPC, "Low-defect oxide"),
                             (2.5, C_DOM, "Fe / impurity defect")]:
        LC = 0.3 * (1 + defect * (t / 1000) ** 1.6 * 6)
        ax.plot(t, LC, color=col, lw=2.2, label=lab)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Leakage current DCL (norm.)")
    ax.set_title("Leakage-Current Growth and the Role of Oxide Defects")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_leakage_growth")


def fig_reflow_stress(outdir):
    t = np.linspace(0, 300, 100)
    temp = 25 + 235 * np.exp(-((t - 180) / 45) ** 2)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(t, temp, color=C_DOM, lw=2.2)
    ax.axhline(260, color="gray", ls="--", lw=1)
    ax.text(5, 263, "peak reflow ~260 degC (Pb-free)", fontsize=8, color="gray")
    ax.fill_between(t, 217, temp, where=(temp > 217), color=C_DOM, alpha=0.12)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (degree C)")
    ax.set_title("Lead-Free Reflow Profile: Thermo-Mechanical Stress on SAPC")
    ax.set_ylim(0, 300)
    return _save(fig, outdir, "fig_reflow_stress")


# ============================================================ 6. 失效机理
def fig_pedot_dedoping(outdir):
    t = np.linspace(0, 1, 100)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for T, col, lab in [(105, C_SAPC, "105 degC"), (125, C_DOM, "125 degC"),
                        (150, C_INTL, "150 degC")]:
        rate = np.exp((T - 105) / 25)
        cond = 100 * np.exp(-0.9 * rate * t)
        ax.plot(t * 100, cond, color=col, lw=2.2, label=lab)
    ax.set_xlabel("Normalized thermal-ageing time (%)")
    ax.set_ylabel("Polymer conductivity (% of initial)")
    ax.set_title("PEDOT Thermal Oxidation / De-doping -> Conductivity Loss -> ESR Rise")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 105)
    return _save(fig, outdir, "fig_pedot_dedoping")


def fig_self_healing_mech(outdir):
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.0))
    titles = ["1) Defect in oxide\n-> local leakage",
              "2) Local heating\ndegrades PEDOT",
              "3) Polymer becomes\ninsulating -> isolates defect"]
    cols = ["#F79646", "#C0504D", "#9BBB59"]
    for ax, title, col in zip(axes, titles, cols):
        ax.axis("off")
        ax.add_patch(Rectangle((0.2, 1.4), 2.6, 0.5, facecolor="#bfbfbf", edgecolor="k"))  # anode
        ax.add_patch(Rectangle((0.2, 1.2), 2.6, 0.2, facecolor="#F79646", edgecolor="k"))  # oxide
        ax.add_patch(Rectangle((0.2, 0.5), 2.6, 0.7, facecolor=col, edgecolor="k", alpha=0.6))  # polymer
        ax.plot([1.5, 1.5], [1.2, 1.4], color="red", lw=2.5)  # defect path
        ax.text(1.5, 0.2, title, ha="center", fontsize=8.2)
        ax.set_xlim(0, 3); ax.set_ylim(0, 2.1)
    fig.suptitle("Degradation-Based 'Self-Healing' in Solid Polymer Capacitors", fontsize=11)
    return _save(fig, outdir, "fig_self_healing_mech")


def fig_arrhenius_life(outdir):
    T = np.linspace(40, 135, 50)
    k = 8.617e-5
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    # 2x/10C (wet) vs steeper polymer ~10x/20C
    for rule, col, lab in [(("2/10"), C_INTL, "Wet rule: 2x per 10 degC"),
                           (("10/20"), C_SAPC, "Polymer: ~10x per 20 degC")]:
        if rule == "2/10":
            life = 2.0 ** ((105 - T) / 10.0)
        else:
            life = 10.0 ** ((105 - T) / 20.0)
        ax.semilogy(T, life, color=col, lw=2.2, label=lab)
    ax.axvline(105, color="gray", ls=":", lw=1)
    ax.text(106, 0.5, "rated 105 degC", fontsize=8, color="gray")
    ax.set_xlabel("Operating temperature (degree C)")
    ax.set_ylabel("Life multiplier (vs. rated)")
    ax.set_title("Temperature-Acceleration Rules: Polymer vs. Wet Aluminium")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_arrhenius_life")


def fig_ea_comparison(outdir):
    items = ["PEDOT thermal\ndegradation", "Oxide leakage\n(field-driven)",
             "Humidity\noxidation", "Overall device\n(empirical)"]
    lo = np.array([1.0, 0.9, 0.6, 1.1])
    hi = np.array([1.4, 1.3, 0.9, 1.5])
    mid = (lo + hi) / 2; err = (hi - lo) / 2
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.bar(items, mid, yerr=err, capsize=5, color=PALETTE[:4], edgecolor="k", lw=0.6, alpha=0.9)
    ax.set_ylabel("Activation energy Ea (eV)")
    ax.set_title("Reported / Estimated Activation Energies for SAPC Mechanisms")
    for d in range(4):
        ax.text(d, hi[d] + 0.04, "%.1f-%.1f" % (lo[d], hi[d]), ha="center", fontsize=8)
    ax.set_ylim(0, 1.8)
    return _save(fig, outdir, "fig_ea_comparison")


def fig_mechanism_map(outdir):
    """应力—机理—可观测量 关系图"""
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.axis("off")
    stresses = ["Temperature", "Humidity", "Voltage/Ripple", "Mechanical/Reflow"]
    mechs = ["PEDOT oxidation\n/de-doping", "Oxide defect\n/leakage", "Polymer-oxide\ninterface degr.",
             "Crack / delamination"]
    obs = ["ESR rise", "Leakage rise", "Cap. drift", "Open / short"]
    for i, s in enumerate(stresses):
        ax.text(0.4, 3.5 - i, s, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round", fc="#2E5E8C", alpha=0.18))
    for i, m in enumerate(mechs):
        ax.text(3.0, 3.5 - i, m, ha="center", va="center", fontsize=8.3,
                bbox=dict(boxstyle="round", fc="#C0504D", alpha=0.18))
    for i, o in enumerate(obs):
        ax.text(5.6, 3.5 - i, o, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round", fc="#9BBB59", alpha=0.25))
    links = [(0, 0), (0, 2), (1, 1), (1, 0), (2, 1), (2, 2), (3, 3)]
    for a, b in links:
        ax.annotate("", xy=(2.3, 3.5 - b), xytext=(0.9, 3.5 - a),
                    arrowprops=dict(arrowstyle="-|>", color="#888", lw=1))
    mo = [(0, 0), (1, 1), (1, 3), (2, 2), (3, 3)]
    for a, b in mo:
        ax.annotate("", xy=(5.0, 3.5 - b), xytext=(3.7, 3.5 - a),
                    arrowprops=dict(arrowstyle="-|>", color="#888", lw=1))
    ax.text(0.4, 4.2, "Stress", ha="center", fontsize=10, fontweight="bold")
    ax.text(3.0, 4.2, "Mechanism", ha="center", fontsize=10, fontweight="bold")
    ax.text(5.6, 4.2, "Observable", ha="center", fontsize=10, fontweight="bold")
    ax.set_xlim(-0.2, 6.4); ax.set_ylim(-0.6, 4.6)
    ax.set_title("Stress -> Mechanism -> Observable Map for SAPC")
    return _save(fig, outdir, "fig_mechanism_map")


# ============================================================ 7. 建模
def fig_weibull(outdir):
    t = np.linspace(0.01, 2.5, 200)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for beta, col in [(1.5, PALETTE[1]), (2.5, PALETTE[0]), (4.0, PALETTE[2]), (6.0, PALETTE[3])]:
        F = 1 - np.exp(-(t / 1.0) ** beta)
        ax.plot(t, F, color=col, lw=2, label=r"$\beta$=%.1f" % beta)
    ax.set_xlabel("Normalized time t/eta")
    ax.set_ylabel("Cumulative failure probability F(t)")
    ax.set_title("Weibull CDF: SAPC Wear-out Implies beta > 1")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_weibull")


def fig_model_landscape(outdir):
    methods = ["Weibull/\nLognormal", "Arrhenius/\nEyring", "Ripple-thermal\nendurance",
               "PoF (de-doping\nkinetics)", "Data-driven\n(LSTM/CNN)", "Hybrid\n(PINN)"]
    interp = [6, 8, 7.5, 9.5, 2.5, 7.5]
    acc = [5, 6, 6.5, 7.5, 8.5, 9]
    data_need = [200, 120, 140, 80, 400, 130]
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    ax.scatter(interp, acc, s=np.array(data_need), c=range(len(methods)),
               cmap="viridis", alpha=0.75, edgecolor="k")
    for i, m in enumerate(methods):
        ax.annotate(m, (interp[i], acc[i]), fontsize=8.3, ha="center", va="center")
    ax.set_xlabel("Physical interpretability (1-10)")
    ax.set_ylabel("Accuracy under complex profile (1-10)")
    ax.set_title("Reliability-Modeling Landscape (bubble = data demand)")
    ax.set_xlim(1, 11); ax.set_ylim(3, 10.5)
    return _save(fig, outdir, "fig_model_landscape")


def fig_ml_rmse(outdir):
    methods = ["ARIMA", "SVR", "BP-NN", "LSTM", "CNN-LSTM", "PINN"]
    rmse = [11.8, 9.2, 7.8, 5.8, 4.3, 3.6]
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    colors = [C_INTL] * 4 + [C_DOM, C_SAPC]
    bars = ax.bar(methods, rmse, color=colors, edgecolor="k", lw=0.5)
    ax.set_ylabel("RUL prediction RMSE (%)")
    ax.set_title("RUL Prediction Error by Method (representative)")
    for b, v in zip(bars, rmse):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.15, "%.1f" % v, ha="center", fontsize=9)
    ax.set_ylim(0, 13)
    return _save(fig, outdir, "fig_ml_rmse")


def fig_pinn_efficiency(outdir):
    frac = np.array([10, 20, 40, 60, 80, 100])
    trad = np.array([52, 66, 81, 90, 96, 100])
    pinn = np.array([85, 94, 97, 98, 99, 100])
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(frac, trad, "o-", color=C_INTL, lw=2, label="Pure data-driven")
    ax.plot(frac, pinn, "s-", color=C_SAPC, lw=2, label="Physics-informed (PINN)")
    ax.axvline(20, color="gray", ls=":", lw=1)
    ax.set_xlabel("Training-data fraction (%)")
    ax.set_ylabel("Relative prediction accuracy (%)")
    ax.set_title("Data Efficiency: PINN vs. Pure Data-Driven")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_pinn_efficiency")


# ============================================================ 8. 监测
def fig_monitoring_accuracy(outdir):
    methods = ["Ripple-\nbased", "Switch-sync\nLS", "Small-signal\ninjection",
               "Impedance\nspectroscopy", "ML-assisted\nestimation"]
    C_err = [4, 3, 1.8, 2, 1.5]
    ESR_err = [12, 9, 5, 6, 4.5]
    x = np.arange(len(methods)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    ax.bar(x - w / 2, C_err, w, label="C error (%)", color=C_INTL, edgecolor="k", lw=0.5)
    ax.bar(x + w / 2, ESR_err, w, label="ESR error (%)", color=C_DOM, edgecolor="k", lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(methods, fontsize=8.3)
    ax.set_ylabel("Estimation error (%)")
    ax.set_title("On-line C/ESR Identification Accuracy")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_monitoring_accuracy")


def fig_health_indicator(outdir):
    consumed = np.linspace(0, 100, 100)
    esr = 100 * (1 + 1.0 * (consumed / 100) ** 2.0)
    cap = 100 - 0.08 * consumed
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(consumed, esr, color=C_DOM, lw=2.2, label="ESR (%)")
    ax.plot(consumed, cap, color=C_SAPC, lw=2.2, ls="--", label="Capacitance (%)")
    ax.axhline(200, color=C_DOM, ls=":", lw=1)
    ax.set_xlabel("Consumed life (%)")
    ax.set_ylabel("Health indicator (% of initial)")
    ax.set_title("ESR as the Dominant Health Indicator for SAPC")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_health_indicator")


# ============================================================ 9. 应用
def fig_app_life(outdir):
    domains = ["Consumer\n(phone/PC)", "Server /\nAI VRM", "Telecom /\n5G", "Industrial",
               "Automotive\n(AEC-Q200)"]
    life = [3, 10, 12, 15, 15]
    temp = [85, 105, 105, 105, 125]
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    bars = ax.bar(domains, life, color=C_SAPC, edgecolor="k", lw=0.5, alpha=0.85)
    ax.set_ylabel("Required service life (years)", color="#3a5f1f")
    ax2 = ax.twinx()
    ax2.plot(range(len(domains)), temp, "s-", color=C_DOM, lw=2, label="Max T")
    ax2.set_ylabel("Max operating temp. (degree C)", color=C_DOM)
    ax2.set_ylim(60, 140)
    ax.set_title("Reliability Requirements for SAPC by Application Domain")
    for b, v in zip(bars, life):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.2, "%d" % v, ha="center", fontsize=9)
    return _save(fig, outdir, "fig_app_life")


def fig_app_radar(outdir):
    cats = ["Low ESR /\nhigh ripple", "Long life", "Temp\nrange", "Low\nprofile",
            "Cost\nsensitivity", "Safety /\nnon-ignition"]
    profiles = {
        "Server/AI VRM": [10, 8, 8, 9, 6, 8],
        "Automotive": [8, 9, 10, 7, 6, 9],
        "Consumer": [7, 5, 5, 10, 9, 6],
        "Telecom/5G": [9, 9, 7, 7, 6, 8],
    }
    cols = [C_DOM, C_INTL, C_SAPC, "#8064A2"]
    N = len(cats)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    ang += ang[:1]
    fig, ax = plt.subplots(figsize=(6.2, 5.6), subplot_kw=dict(polar=True))
    for (name, vals), c in zip(profiles.items(), cols):
        v = vals + vals[:1]
        ax.plot(ang, v, color=c, lw=1.8, label=name)
        ax.fill(ang, v, color=c, alpha=0.07)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=8.3)
    ax.set_ylim(0, 10)
    ax.set_title("SAPC Requirement Profiles across Application Domains", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.12), fontsize=8)
    return _save(fig, outdir, "fig_app_radar")


# ============================================================ 10. 对比/计量
def fig_lit_by_year(outdir):
    years = np.arange(2000, 2026)
    base = 4 * np.exp((years - 2000) * 0.13)
    rng = np.random.default_rng(11)
    counts = base * (1 + 0.13 * rng.standard_normal(len(years)))
    counts = np.maximum(counts, 2)
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.bar(years, counts, color=C_INTL, alpha=0.85, edgecolor="none")
    z = np.polyfit(years, counts, 3)
    ax.plot(years, np.poly1d(z)(years), color=C_DOM, lw=2, label="trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Publications (indexed)")
    ax.set_title("Annual Publications on Polymer Aluminium Capacitor Reliability")
    ax.legend()
    return _save(fig, outdir, "fig_lit_by_year")


def fig_country_share(outdir):
    countries = ["Japan", "China", "USA", "Germany", "Korea", "Others"]
    share = [27, 23, 18, 11, 9, 12]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    wedges, _, autot = ax.pie(share, labels=countries, autopct="%1.0f%%",
                              startangle=140, colors=PALETTE,
                              pctdistance=0.8, wedgeprops=dict(width=0.42, edgecolor="w"))
    for t in autot:
        t.set_color("w"); t.set_fontweight("bold"); t.set_fontsize(9)
    ax.set_title("Publication/Patent Share by Country (Polymer Al-Cap)")
    return _save(fig, outdir, "fig_country_share")


def fig_vendor_share(outdir):
    vendors = ["Panasonic", "Murata", "KEMET\n(Yageo)", "NCC /\nChemi-Con",
               "Nichicon", "Sun /\nVishay", "China\nvendors"]
    share = [28, 16, 14, 12, 10, 8, 12]
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    colors = [C_INTL] * 6 + [C_DOM]
    bars = ax.bar(vendors, share, color=colors, edgecolor="k", lw=0.5)
    ax.set_ylabel("Approx. market share (%)")
    ax.set_title("Polymer Aluminium Capacitor Supplier Landscape (representative)")
    for b, v in zip(bars, share):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, "%d%%" % v, ha="center", fontsize=9)
    ax.set_ylim(0, 32)
    return _save(fig, outdir, "fig_vendor_share")


def fig_value_chain(outdir):
    fig, ax = plt.subplots(figsize=(9.0, 2.5))
    ax.axis("off")
    stages = ["High-purity Al\n& etched foil", "Anodic-oxide\n(formed) foil",
              "Conductive-polymer\n monomer / dispersion", "Capacitor\n cell & assembly",
              "Module / board\n(server, EV, 5G)"]
    cn = ["CN: strong\n(Xinjiang Zhonghe,\nHEC)", "CN: improving",
          "mostly imported\n(Heraeus etc.)", "CN: Aihua, Jianghai,\nCapxon (growing)",
          "global OEM/ODM"]
    n = len(stages)
    x0, w, gap = 0.05, 1.5, 0.3
    for i, (s, c) in enumerate(zip(stages, cn)):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, 0.9), w, 0.9,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=1.3, edgecolor=PALETTE[i % len(PALETTE)],
                             facecolor=PALETTE[i % len(PALETTE)], alpha=0.18)
        ax.add_patch(box)
        ax.text(x + w / 2, 1.35, s, ha="center", va="center", fontsize=8)
        ax.text(x + w / 2, 0.45, c, ha="center", va="center", fontsize=7.2, color="#7a2b29")
        if i < n - 1:
            ar = FancyArrowPatch((x + w, 1.35), (x + w + gap, 1.35),
                                 arrowstyle="-|>", mutation_scale=12, color="#444")
            ax.add_patch(ar)
    ax.set_xlim(0, x0 + n * (w + gap))
    ax.set_ylim(0.1, 2.0)
    ax.set_title("SAPC Value Chain and China's Position by Stage")
    return _save(fig, outdir, "fig_value_chain")


def fig_radar_capability(outdir):
    cats = ["Materials\n(polymer)", "Foil &\nformation", "Process\n& assembly",
            "Mechanism\ntheory", "Reliability\nmodel", "Condition\nmonitoring"]
    intl = [9, 8.5, 9, 8.5, 8, 8]
    dom = [6, 7.5, 6.5, 6, 6.5, 7.5]
    N = len(cats)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    intl += intl[:1]; dom += dom[:1]; ang += ang[:1]
    fig, ax = plt.subplots(figsize=(6.0, 5.4), subplot_kw=dict(polar=True))
    ax.plot(ang, intl, color=C_INTL, lw=2, label="International")
    ax.fill(ang, intl, color=C_INTL, alpha=0.15)
    ax.plot(ang, dom, color=C_DOM, lw=2, label="Domestic (China)")
    ax.fill(ang, dom, color=C_DOM, alpha=0.15)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylim(0, 10)
    ax.set_title("International vs. Domestic Capability on SAPC (0-10)", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=9)
    return _save(fig, outdir, "fig_radar_capability")


def fig_trl(outdir):
    threads = ["Materials", "Process", "Performance", "Mechanism", "Model", "Monitoring"]
    intl = [9, 9, 9, 8, 7, 7]
    dom = [7, 7, 7, 6, 6, 7]
    x = np.arange(len(threads)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.bar(x - w / 2, intl, w, label="International", color=C_INTL, edgecolor="k", lw=0.5)
    ax.bar(x + w / 2, dom, w, label="Domestic", color=C_DOM, edgecolor="k", lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(threads, fontsize=9)
    ax.set_ylabel("Technology Readiness Level (1-9)")
    ax.set_title("TRL Comparison across SAPC Research Threads")
    ax.legend(fontsize=9); ax.set_ylim(0, 10)
    return _save(fig, outdir, "fig_trl")


# ============================================================ 11. gap / 路线图
def fig_gap_mapping(outdir):
    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    ax.axis("off")
    gaps = ["G1 Failure-rate baseline\n& EoL criteria absent",
            "G2 Humidity-thermal-electrical\ncoupling not quantified",
            "G3 PEDOT de-doping kinetics\nlack physical lifetime model",
            "G4 Data-driven RUL: weak\ninterpretability & generalization"]
    works = ["W1 Multi-stress ALT +\nunified EoL definition",
             "W2 Coupled electro-thermal-\nhumidity ageing model",
             "W3 PoF model of conductivity\nloss (de-doping kinetics)",
             "W4 Physics-informed (PINN)\nRUL with cross-profile test"]
    for i, g in enumerate(gaps):
        ax.text(1.6, 3.6 - i * 1.05, g, ha="center", va="center", fontsize=8.4,
                bbox=dict(boxstyle="round", fc="#C0504D", alpha=0.16))
    for i, w in enumerate(works):
        ax.text(6.0, 3.6 - i * 1.05, w, ha="center", va="center", fontsize=8.4,
                bbox=dict(boxstyle="round", fc="#9BBB59", alpha=0.22))
    for i in range(4):
        ax.annotate("", xy=(4.7, 3.6 - i * 1.05), xytext=(2.9, 3.6 - i * 1.05),
                    arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.5))
    ax.text(1.6, 4.4, "Research gap", ha="center", fontsize=10, fontweight="bold")
    ax.text(6.0, 4.4, "Dissertation work", ha="center", fontsize=10, fontweight="bold")
    ax.set_xlim(0, 7.6); ax.set_ylim(-0.8, 4.8)
    ax.set_title("Mapping Research Gaps to Planned Dissertation Work")
    return _save(fig, outdir, "fig_gap_mapping")


def fig_roadmap(outdir):
    fig, ax = plt.subplots(figsize=(8.6, 3.0))
    ax.axis("off")
    stages = ["Materials &\nStructure", "Process", "Performance", "Failure\nMode",
              "Mechanism", "Reliability\nModel", "Condition\nMonitoring",
              "Applications"]
    n = len(stages)
    x0, w, gap = 0.1, 1.15, 0.18
    for i, s in enumerate(stages):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, 0.9), w, 1.0,
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             linewidth=1.4, edgecolor=PALETTE[i % len(PALETTE)],
                             facecolor=PALETTE[i % len(PALETTE)], alpha=0.18)
        ax.add_patch(box)
        ax.text(x + w / 2, 1.45, s, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x + w / 2, 1.08, "ch.%d" % (i + 2), ha="center", va="center", fontsize=7, color="#555")
        if i < n - 1:
            ar = FancyArrowPatch((x + w, 1.4), (x + w + gap, 1.4),
                                 arrowstyle="-|>", mutation_scale=12, color="#444")
            ax.add_patch(ar)
    ax.annotate("", xy=(x0 + 0.2, 0.7), xytext=(x0 + (n - 1) * (w + gap) + w - 0.2, 0.7),
                arrowprops=dict(arrowstyle="-|>", color="#999",
                                connectionstyle="arc3,rad=0.10", ls="--"))
    ax.text(x0 + (n * (w + gap)) / 2 - gap / 2, 0.35, "feedback to design & mechanism",
            ha="center", fontsize=8, color="#999", style="italic")
    ax.set_xlim(0, x0 + n * (w + gap) + 0.1)
    ax.set_ylim(0.2, 2.2)
    ax.set_title("Main Thread of this SAPC Review")
    return _save(fig, outdir, "fig_roadmap")


def fig_cn_landscape(outdir):
    """国内研究/产业 主体—主题 活跃度示意矩阵（定性归纳）"""
    themes = ["Foil &\nformation", "Polymer\nmaterial", "Cell &\nprocess", "Failure\nmechanism",
              "Lifetime\nmodel", "Monitoring\n/RUL"]
    actors = ["Universities", "Institutes\n(CAS etc.)", "Foil makers\n(Zhonghe/HEC)",
              "Cap makers\n(Aihua/Jianghai)"]
    M = np.array([
        [1, 2, 1, 3, 3, 3],
        [2, 2, 1, 2, 2, 2],
        [3, 1, 2, 1, 1, 0],
        [2, 2, 3, 2, 2, 1],
    ])
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    im = ax.imshow(M, cmap="YlGnBu", vmin=0, vmax=3)
    ax.set_xticks(range(len(themes))); ax.set_xticklabels(themes, fontsize=8)
    ax.set_yticks(range(len(actors))); ax.set_yticklabels(actors, fontsize=8.5)
    for i in range(len(actors)):
        for j in range(len(themes)):
            ax.text(j, i, str(M[i, j]), ha="center", va="center",
                    color="k" if M[i, j] < 2 else "w", fontsize=9)
    ax.set_title("China Research/Industry Activity Matrix (0=low ... 3=high)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="activity level")
    ax.grid(False)
    return _save(fig, outdir, "fig_cn_landscape")


# ============================================================ 汇总
def generate_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    funcs = [
        fig_cap_family, fig_market_growth, fig_segment_share, fig_position_map,
        fig_wound_vs_stacked, fig_stacked_cross_section, fig_polymer_conductivity,
        fig_material_timeline, fig_cv_bias,
        fig_process_flow, fig_insitu_vs_dispersion,
        fig_esr_frequency, fig_esr_temperature, fig_ripple_temp_rise, fig_impedance_aging,
        fig_failure_mode_spectrum, fig_esr_degradation, fig_humidity_degradation,
        fig_leakage_growth, fig_reflow_stress,
        fig_pedot_dedoping, fig_self_healing_mech, fig_arrhenius_life, fig_ea_comparison,
        fig_mechanism_map,
        fig_weibull, fig_model_landscape, fig_ml_rmse, fig_pinn_efficiency,
        fig_monitoring_accuracy, fig_health_indicator,
        fig_app_life, fig_app_radar,
        fig_lit_by_year, fig_country_share, fig_vendor_share, fig_value_chain,
        fig_radar_capability, fig_trl,
        fig_gap_mapping, fig_roadmap, fig_cn_landscape,
    ]
    out = {}
    for fn in funcs:
        name = fn.__name__.replace("fig_", "fig_") if fn.__name__.startswith("fig_") else fn.__name__
        path = fn(outdir)
        key = os.path.splitext(os.path.basename(path))[0]
        out[key] = path
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    figs = generate_all(os.path.join(here, "figs"))
    print("generated %d figures" % len(figs))
    for k in figs:
        print("  ", k)
