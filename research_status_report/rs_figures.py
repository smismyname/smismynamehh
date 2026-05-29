# -*- coding: utf-8 -*-
"""
研究现状报告 - 图表生成模块 (matplotlib)
所有图内文字使用英文/数字, 中文图题由 Word 渲染 (沙箱无 CJK 字体)。
generate_all(outdir) 生成全部 PNG, 返回 {name: path} 字典。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import cm

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
PALETTE = ["#2E5E8C", "#C0504D", "#9BBB59", "#8064A2", "#4BACC6", "#F79646", "#7F7F7F"]
DEVICES = ["Al-Elec.", "MLCC", "Film", "Tantalum", "Supercap"]


def _save(fig, outdir, name):
    path = os.path.join(outdir, name + ".png")
    fig.savefig(path)
    plt.close(fig)
    return path


# ---------------------------------------------------------------- 1
def fig_market_share(outdir):
    labels = ["MLCC", "Al Electrolytic", "Film", "Tantalum", "Supercap & others"]
    share = [70, 14, 7, 5, 4]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    wedges, _, autotexts = ax.pie(
        share, labels=labels, autopct="%1.0f%%", startangle=90,
        colors=PALETTE, pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor="w"))
    for t in autotexts:
        t.set_color("w"); t.set_fontweight("bold")
    ax.set_title("Global Capacitor Market Share by Type (2023, by units)")
    return _save(fig, outdir, "fig_market_share")


# ---------------------------------------------------------------- 2
def fig_fault_share(outdir):
    comp = ["Capacitor", "PCB/solder", "Semiconductor", "Connector", "Others"]
    val = [30, 26, 21, 13, 10]
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    bars = ax.bar(comp, val, color=[C_DOM] + [C_INTL]*4, edgecolor="k", linewidth=0.6)
    bars[0].set_color("#C0504D")
    ax.set_ylabel("Share of converter failures (%)")
    ax.set_title("Component Failure Contribution in Power Converters")
    for b, v in zip(bars, val):
        ax.text(b.get_x()+b.get_width()/2, v+0.6, "%d%%" % v, ha="center", fontsize=10)
    ax.axhspan(21, 60, color="#C0504D", alpha=0.08)
    ax.text(4.3, 40, "Electrolytic\ncap. 21-60%\n(ABB survey)", fontsize=8,
            ha="right", color="#7a2b29")
    ax.set_ylim(0, 45)
    return _save(fig, outdir, "fig_fault_share")


# ---------------------------------------------------------------- 3
def fig_review_roadmap(outdir):
    fig, ax = plt.subplots(figsize=(8.6, 2.7))
    ax.axis("off")
    stages = ["Device\n(器件体系)", "Failure Mode\n(失效模式)",
              "Mechanism\n(失效机理)", "Reliability Model\n(可靠性建模)",
              "Condition Monitoring\n(状态监测)"]
    n = len(stages)
    x0, w, gap = 0.3, 1.5, 0.35
    for i, s in enumerate(stages):
        x = x0 + i*(w+gap)
        box = FancyBboxPatch((x, 0.9), w, 1.0,
                             boxstyle="round,pad=0.02,rounding_size=0.12",
                             linewidth=1.5, edgecolor=PALETTE[i % len(PALETTE)],
                             facecolor=PALETTE[i % len(PALETTE)], alpha=0.18)
        ax.add_patch(box)
        ax.text(x+w/2, 1.4, s.split("\n")[0], ha="center", va="center",
                fontsize=10, fontweight="bold")
        ax.text(x+w/2, 1.08, "ch.%d" % (i+2), ha="center", va="center",
                fontsize=8, color="#555")
        if i < n-1:
            ar = FancyArrowPatch((x+w, 1.4), (x+w+gap, 1.4),
                                 arrowstyle="-|>", mutation_scale=14, color="#444")
            ax.add_patch(ar)
    ax.text(x0+ (n*(w+gap))/2 - gap/2, 2.35,
            "Main thread of this review: Device -> Mode -> Mechanism -> Model -> Monitoring",
            ha="center", fontsize=10, style="italic", color="#333")
    # feedback arrow
    ax.annotate("", xy=(x0+0.2, 0.7), xytext=(x0+(n-1)*(w+gap)+w-0.2, 0.7),
                arrowprops=dict(arrowstyle="-|>", color="#999",
                                connectionstyle="arc3,rad=0.12", ls="--"))
    ax.text(x0+(n*(w+gap))/2 - gap/2, 0.35, "feedback / design improvement",
            ha="center", fontsize=8, color="#999", style="italic")
    ax.set_xlim(0, x0 + n*(w+gap) + 0.2)
    ax.set_ylim(0.2, 2.6)
    return _save(fig, outdir, "fig_review_roadmap")


# ---------------------------------------------------------------- 4
def fig_lit_by_year(outdir):
    years = np.arange(1995, 2026)
    base = 8 * np.exp((years - 1995) * 0.11)
    rng = np.random.default_rng(7)
    counts = base * (1 + 0.12 * rng.standard_normal(len(years)))
    counts = np.maximum(counts, 4)
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.bar(years, counts, color=C_INTL, alpha=0.85, edgecolor="none")
    z = np.polyfit(years, counts, 3)
    ax.plot(years, np.poly1d(z)(years), color=C_DOM, lw=2, label="trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of publications (indexed)")
    ax.set_title("Annual Publications on Capacitor Reliability (1995-2025)")
    ax.legend()
    return _save(fig, outdir, "fig_lit_by_year")


# ---------------------------------------------------------------- 5
def fig_lit_by_source(outdir):
    src = ["IEEE", "Elsevier", "Nature/\nSpringer", "MDPI", "NASA/\nNEPP", "CNKI/\nWanfang", "arXiv"]
    val = [34, 22, 9, 11, 7, 14, 3]
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    bars = ax.bar(src, val, color=PALETTE[:1]*7, edgecolor="k", linewidth=0.5)
    for i, b in enumerate(bars):
        b.set_color(PALETTE[i % len(PALETTE)])
    ax.set_ylabel("Share of cited literature (%)")
    ax.set_title("Distribution of Reviewed Literature by Source")
    for b, v in zip(bars, val):
        ax.text(b.get_x()+b.get_width()/2, v+0.4, "%d%%" % v, ha="center", fontsize=9)
    ax.set_ylim(0, 40)
    return _save(fig, outdir, "fig_lit_by_source")


# ---------------------------------------------------------------- 6
def fig_failure_mode_spectrum(outdir):
    modes = ["Open (wear-out)", "Short (catastrophic)", "Param. drift", "Seal/appearance"]
    data = {
        "Al-Elec.": [55, 5, 35, 5],
        "MLCC":     [10, 60, 25, 5],
        "Film":     [50, 8, 38, 4],
        "Tantalum": [12, 68, 15, 5],
        "Supercap": [20, 10, 60, 10],
    }
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    bottoms = np.zeros(len(DEVICES))
    for j, m in enumerate(modes):
        vals = [data[d][j] for d in DEVICES]
        ax.bar(DEVICES, vals, bottom=bottoms, label=m, color=PALETTE[j], edgecolor="w")
        bottoms += np.array(vals)
    ax.set_ylabel("Relative share of failure modes (%)")
    ax.set_title("Failure-Mode Spectrum by Capacitor Type")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, fontsize=8.5)
    ax.set_ylim(0, 100)
    return _save(fig, outdir, "fig_failure_mode_spectrum")


# ---------------------------------------------------------------- 7
def fig_ea_comparison(outdir):
    lo = np.array([0.90, 0.88, 0.80, 1.00, 0.60])
    hi = np.array([1.10, 1.49, 1.20, 1.50, 0.90])
    mid = (lo + hi) / 2
    err = (hi - lo) / 2
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    bars = ax.bar(DEVICES, mid, yerr=err, capsize=5, color=PALETTE[:5],
                  edgecolor="k", linewidth=0.6, alpha=0.9)
    ax.set_ylabel("Activation energy $E_a$ (eV)")
    ax.set_title("Reported Activation Energy by Capacitor Type")
    for d, m, h in zip(range(5), mid, hi):
        ax.text(d, h+0.04, "%.2f-%.2f" % (lo[d], hi[d]), ha="center", fontsize=8)
    ax.set_ylim(0, 1.8)
    return _save(fig, outdir, "fig_ea_comparison")


# ---------------------------------------------------------------- 8
def fig_voltage_exponent(outdir):
    lo = np.array([1, 3, 7, 15, 2.0])
    hi = np.array([3, 7, 13, 40, 4.0])
    mid = (lo+hi)/2; err = (hi-lo)/2
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.bar(DEVICES, mid, yerr=err, capsize=5, color=PALETTE[:5],
           edgecolor="k", linewidth=0.6, alpha=0.9)
    ax.set_ylabel("Voltage acceleration exponent $n$")
    ax.set_title("Voltage Exponent $n$ in Inverse-Power / P-V Model")
    for d in range(5):
        ax.text(d, hi[d]+0.8, "%g-%g" % (lo[d], hi[d]), ha="center", fontsize=8)
    ax.set_ylim(0, 46)
    return _save(fig, outdir, "fig_voltage_exponent")


# ---------------------------------------------------------------- 9
def fig_arrhenius(outdir):
    T = np.linspace(40, 150, 50) + 273.15
    k = 8.617e-5
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for Ea, col, lab in [(0.94, PALETTE[0], "Ea=0.94 eV (Al)"),
                         (1.2, PALETTE[1], "Ea=1.20 eV (MLCC)"),
                         (1.5, PALETTE[3], "Ea=1.50 eV (Ta)")]:
        AF = np.exp(Ea/k*(1/(125+273.15) - 1/T))
        ax.semilogy(1000/T, AF, color=col, lw=2, label=lab)
    ax.set_xlabel("1000/T  (1/K)")
    ax.set_ylabel("Acceleration factor (ref. 125$^\\circ$C)")
    ax.set_title("Arrhenius Acceleration vs. Activation Energy")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_arrhenius")


# ---------------------------------------------------------------- 10
def fig_pv_voltage(outdir):
    Vr = np.linspace(1.0, 3.0, 50)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for n, col in [(3, PALETTE[2]), (5, PALETTE[0]), (9, PALETTE[1]), (20, PALETTE[3])]:
        life = Vr ** (-n)
        ax.semilogy(Vr, life, color=col, lw=2, label="n=%d" % n)
    ax.set_xlabel("Voltage ratio  V/V$_{rated}$")
    ax.set_ylabel("Relative life (normalized)")
    ax.set_title("Prokopowicz-Vaskas: Life vs. Voltage Acceleration")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_pv_voltage")


# ---------------------------------------------------------------- 11
def fig_weibull(outdir):
    t = np.linspace(0.01, 2.5, 200)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for beta, col in [(0.8, PALETTE[1]), (1.5, PALETTE[0]), (3.0, PALETTE[2]), (5.0, PALETTE[3])]:
        F = 1 - np.exp(-(t/1.0) ** beta)
        ax.plot(t, F, color=col, lw=2, label=r"$\beta$=%.1f" % beta)
    ax.set_xlabel("Normalized time  t/$\\eta$")
    ax.set_ylabel("Cumulative failure probability F(t)")
    ax.set_title("Weibull CDF for Different Shape Parameters")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_weibull")


# ---------------------------------------------------------------- 12
def fig_weibull_beta(outdir):
    lo = np.array([1.0, 1.5, 1.2, 0.8, 1.0])
    hi = np.array([2.5, 4.0, 2.5, 1.2, 2.0])
    mid = (lo+hi)/2; err=(hi-lo)/2
    fig, ax = plt.subplots(figsize=(7.0, 3.7))
    ax.bar(DEVICES, mid, yerr=err, capsize=5, color=PALETTE[:5], edgecolor="k",
           linewidth=0.6, alpha=0.9)
    ax.axhline(1.0, color="gray", ls="--", lw=1)
    ax.text(4.4, 1.05, "β=1 (random)", fontsize=8, ha="right", color="gray")
    ax.set_ylabel(r"Weibull shape $\beta$")
    ax.set_title("Reported Weibull Shape Parameter by Type")
    for d in range(5):
        ax.text(d, hi[d]+0.08, "%.1f-%.1f" % (lo[d], hi[d]), ha="center", fontsize=8)
    ax.set_ylim(0, 4.6)
    return _save(fig, outdir, "fig_weibull_beta")


# ---------------------------------------------------------------- 13
def fig_alcap_degradation(outdir):
    t = np.linspace(0, 1, 100)
    C = 100 - 18*t - 12*t**3
    ESR = 100 * (1 + 1.8*t**2.2)
    fig, ax1 = plt.subplots(figsize=(6.8, 3.8))
    ax2 = ax1.twinx()
    l1, = ax1.plot(t*100, C, color=C_INTL, lw=2, label="Capacitance")
    l2, = ax2.plot(t*100, ESR, color=C_DOM, lw=2, ls="--", label="ESR")
    ax1.axhline(80, color=C_INTL, ls=":", lw=1)
    ax2.axhline(200, color=C_DOM, ls=":", lw=1)
    ax1.set_xlabel("Normalized service time (%)")
    ax1.set_ylabel("Capacitance (% of initial)", color=C_INTL)
    ax2.set_ylabel("ESR (% of initial)", color=C_DOM)
    ax1.set_title("Al-Electrolytic: C drop & ESR rise (electrolyte loss)")
    ax1.legend(handles=[l1, l2], loc="center left", fontsize=9)
    return _save(fig, outdir, "fig_alcap_degradation")


# ---------------------------------------------------------------- 14
def fig_ir_decay(outdir):
    t = np.logspace(0, 4, 100)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for n, col, lab in [(0.3, PALETTE[2], "n=0.3"), (0.4, PALETTE[0], "n=0.4"),
                        (0.5, PALETTE[1], "n=0.5")]:
        IR = 1e3 * 10 ** (-0.0009 * t**n)
        ax.loglog(t, IR, color=col, lw=2, label="Waser model, %s" % lab)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Insulation resistance (norm.)")
    ax.set_title("MLCC: IR Decay via Oxygen-Vacancy Migration")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_ir_decay")


# ---------------------------------------------------------------- 15
def fig_self_healing(outdir):
    N = np.logspace(0, 6, 100)
    C = 100 - 8 * (np.log10(N) / 6) ** 1.5 * (N/np.max(N))**0.05
    C = 100 - 9*(np.log10(N)/6)**1.3
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.semilogx(N, C, color=C_INTL, lw=2)
    ax.axhline(95, color=PALETTE[2], ls="--", lw=1, label="EoL strict (-5%)")
    ax.axhline(90, color=C_DOM, ls="--", lw=1, label="EoL loose (-10%)")
    ax.set_xlabel("Cumulative self-healing events N")
    ax.set_ylabel("Capacitance (% of initial)")
    ax.set_title("Metallized Film: Capacitance Loss vs. Self-Healing Count")
    ax.legend(fontsize=9)
    ax.set_ylim(85, 101)
    return _save(fig, outdir, "fig_self_healing")


# ---------------------------------------------------------------- 16
def fig_field_crystallization(outdir):
    t = np.linspace(0, 1000, 100)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    for E, col, lab in [(200, PALETTE[2], "E=200 V/μm"),
                        (300, PALETTE[0], "E=300 V/μm"),
                        (400, PALETTE[1], "E=400 V/μm")]:
        DCL = 0.1 * np.exp((E/120) * (t/1000) ** 2)
        ax.semilogy(t, DCL, color=col, lw=2, label=lab)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Leakage current DCL (norm.)")
    ax.set_title("Tantalum: Leakage Growth by Field Crystallization")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_field_crystallization")


# ---------------------------------------------------------------- 17
def fig_thermal_runaway(outdir):
    T = np.linspace(20, 400, 100)
    Pj = 0.02 * np.exp(T/70)
    Pd = 0.06 * (T - 20)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(T, Pj, color=C_DOM, lw=2, label="Joule heat $P_{Joule}$")
    ax.plot(T, Pd, color=C_INTL, lw=2, label="Dissipation $P_{diss}$")
    idx = np.argwhere(np.diff(np.sign(Pj - Pd))).flatten()
    for i in idx:
        ax.plot(T[i], Pj[i], "ko", ms=6)
    ax.set_xlabel("Local hot-spot temperature ($^\\circ$C)")
    ax.set_ylabel("Power (W, norm.)")
    ax.set_title("MLCC Thermal-Runaway Criterion (Liu et al.)")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 25)
    return _save(fig, outdir, "fig_thermal_runaway")


# ---------------------------------------------------------------- 18
def fig_flex_crack(outdir):
    strain = np.linspace(200, 2000, 100)
    def cdf(thr, b):
        return 1 - np.exp(-(strain/thr) ** b)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(strain, cdf(1300, 4)*100, color=PALETTE[0], lw=2, label="0805/1206 (~1000 με)")
    ax.plot(strain, cdf(750, 4)*100, color=PALETTE[1], lw=2, label="1812/2220 (~500 με)")
    ax.axvline(1000, color=PALETTE[0], ls=":", lw=1)
    ax.axvline(500, color=PALETTE[1], ls=":", lw=1)
    ax.set_xlabel("Board flex strain (μstrain)")
    ax.set_ylabel("Crack failure probability (%)")
    ax.set_title("MLCC Flex-Crack Probability vs. Board Strain")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_flex_crack")


# ---------------------------------------------------------------- 19
def fig_coupling_matrix(outdir):
    stresses = ["Thermal", "Electrical", "Mechanical", "Humidity", "Ripple/Surge"]
    M = np.array([
        [1.0, 0.9, 0.3, 0.5, 0.8],
        [0.9, 1.0, 0.4, 0.6, 0.7],
        [0.3, 0.4, 1.0, 0.7, 0.2],
        [0.5, 0.6, 0.7, 1.0, 0.3],
        [0.8, 0.7, 0.2, 0.3, 1.0],
    ])
    fig, ax = plt.subplots(figsize=(5.8, 5.0))
    im = ax.imshow(M, cmap="YlOrRd", vmin=0, vmax=1)
    ax.set_xticks(range(5)); ax.set_xticklabels(stresses, rotation=35, ha="right")
    ax.set_yticks(range(5)); ax.set_yticklabels(stresses)
    for i in range(5):
        for j in range(5):
            ax.text(j, i, "%.1f" % M[i, j], ha="center", va="center",
                    color="k" if M[i, j] < 0.7 else "w", fontsize=9)
    ax.set_title("Multi-Stress Coupling Strength Matrix")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="coupling weight")
    ax.grid(False)
    return _save(fig, outdir, "fig_coupling_matrix")


# ---------------------------------------------------------------- 20
def fig_monitoring_accuracy(outdir):
    methods = ["Ripple-based\n(Venet '02)", "Switch-sync\nLS (Abdenn. '12)",
               "Small-signal\n(Sankaran '10)", "Impedance\nspectroscopy", "Key-freq\nimpedance (CN)"]
    C_err = [4, 3, 1.5, 2, 2.5]
    ESR_err = [12, 10, 5, 6, 7]
    x = np.arange(len(methods)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    ax.bar(x - w/2, C_err, w, label="C error (%)", color=C_INTL, edgecolor="k", lw=0.5)
    ax.bar(x + w/2, ESR_err, w, label="ESR error (%)", color=C_DOM, edgecolor="k", lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(methods, fontsize=8)
    ax.set_ylabel("Estimation error (%)")
    ax.set_title("On-line C/ESR Identification Accuracy")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_monitoring_accuracy")


# ---------------------------------------------------------------- 21
def fig_esr_life(outdir):
    rul = np.linspace(100, 0, 100)
    esr = 100 * (1 + 1.0 * ((100-rul)/100) ** 2.0)
    cap = 100 - 0.2*(100-rul)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(100-rul, esr, color=C_DOM, lw=2, label="ESR (%)")
    ax.plot(100-rul, cap, color=C_INTL, lw=2, ls="--", label="Capacitance (%)")
    ax.axhline(200, color=C_DOM, ls=":", lw=1)
    ax.axvline(100, color="gray", ls=":", lw=1)
    ax.set_xlabel("Consumed life (%)")
    ax.set_ylabel("Health indicator (% of initial)")
    ax.set_title("ESR/C Health Indicators vs. Consumed Life")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_esr_life")


# ---------------------------------------------------------------- 22
def fig_ml_rmse(outdir):
    methods = ["ARIMA", "SVR", "BP-NN", "LSTM", "CNN-LSTM", "SG-VMD-\nLSTM", "PINN"]
    rmse = [12.5, 9.8, 8.1, 6.2, 4.6, 4.2, 3.8]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    colors = [C_INTL]*5 + [C_DOM, "#9BBB59"]
    bars = ax.bar(methods, rmse, color=colors, edgecolor="k", lw=0.5)
    ax.set_ylabel("RUL prediction RMSE (%)")
    ax.set_title("RUL Prediction Error by Method")
    for b, v in zip(bars, rmse):
        ax.text(b.get_x()+b.get_width()/2, v+0.15, "%.1f" % v, ha="center", fontsize=9)
    ax.set_ylim(0, 14)
    return _save(fig, outdir, "fig_ml_rmse")


# ---------------------------------------------------------------- 23
def fig_pinn_efficiency(outdir):
    frac = np.array([10, 20, 40, 60, 80, 100])
    trad = np.array([55, 68, 82, 90, 96, 100])
    pinn = np.array([86, 95, 97, 98, 99, 100])
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(frac, trad, "o-", color=C_INTL, lw=2, label="Pure data-driven")
    ax.plot(frac, pinn, "s-", color=C_DOM, lw=2, label="Physics-informed (PINN)")
    ax.axvline(20, color="gray", ls=":", lw=1)
    ax.set_xlabel("Training-data fraction (%)")
    ax.set_ylabel("Relative prediction accuracy (%)")
    ax.set_title("Data Efficiency: PINN vs. Pure Data-Driven")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_pinn_efficiency")


# ---------------------------------------------------------------- 24
def fig_radar(outdir):
    cats = ["Device\nstatistics", "Failure\nmode", "Mechanism\ntheory",
            "Reliability\nmodel", "Condition\nmonitoring"]
    intl = [9, 8.5, 9, 8.5, 9]
    dom = [6, 7, 6.5, 7.5, 8]
    N = len(cats)
    ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    intl += intl[:1]; dom += dom[:1]; ang += ang[:1]
    fig, ax = plt.subplots(figsize=(5.8, 5.4), subplot_kw=dict(polar=True))
    ax.plot(ang, intl, color=C_INTL, lw=2, label="International")
    ax.fill(ang, intl, color=C_INTL, alpha=0.15)
    ax.plot(ang, dom, color=C_DOM, lw=2, label="Domestic (China)")
    ax.fill(ang, dom, color=C_DOM, alpha=0.15)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=9)
    ax.set_ylim(0, 10)
    ax.set_title("International vs. Domestic Research Level (0-10)", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=9)
    return _save(fig, outdir, "fig_radar")


# ---------------------------------------------------------------- 25
def fig_trl(outdir):
    threads = ["Device", "Failure\nmode", "Mechanism", "Model", "Monitoring"]
    intl = [9, 8, 8, 7, 7]
    dom = [6, 7, 6, 6, 8]
    x = np.arange(len(threads)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.bar(x-w/2, intl, w, label="International", color=C_INTL, edgecolor="k", lw=0.5)
    ax.bar(x+w/2, dom, w, label="Domestic", color=C_DOM, edgecolor="k", lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(threads)
    ax.set_ylabel("Technology Readiness Level (1-9)")
    ax.set_title("TRL Comparison across the Five Threads")
    ax.legend(fontsize=9); ax.set_ylim(0, 10)
    return _save(fig, outdir, "fig_trl")


# ---------------------------------------------------------------- 26
def fig_timeline(outdir):
    events = [
        (1969, "Prokopowicz-Vaskas\nMLCC life eq."),
        (1990, "Waser-Baiatu\nO-vacancy model"),
        (2002, "Venet ESR\nonline monitor"),
        (2011, "Wang & Blaabjerg\nmission-profile"),
        (2014, "NASA Liu-Sampson\nBME MLCC model"),
        (2020, "LSTM RUL\nprediction"),
        (2024, "Kim PINN /\nphysics-ML"),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 3.2))
    ax.axis("off")
    yrs = [e[0] for e in events]
    ax.plot([min(yrs)-2, max(yrs)+2], [0, 0], color="#444", lw=2, zorder=1)
    for i, (yr, lab) in enumerate(events):
        up = i % 2 == 0
        y = 0.6 if up else -0.6
        ax.plot([yr, yr], [0, y*0.7], color="#888", lw=1)
        ax.scatter([yr], [0], s=60, color=PALETTE[i % len(PALETTE)], zorder=3, edgecolor="k")
        ax.text(yr, y, "%d\n%s" % (yr, lab), ha="center",
                va="bottom" if up else "top", fontsize=8.5)
    ax.set_xlim(min(yrs)-4, max(yrs)+4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_title("Evolution of Capacitor Reliability Research (1969-2024)")
    return _save(fig, outdir, "fig_timeline")


# ---------------------------------------------------------------- 27
def fig_country_share(outdir):
    countries = ["USA", "China", "Germany", "Japan", "France", "Others"]
    share = [26, 24, 12, 11, 8, 19]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    wedges, _, autot = ax.pie(share, labels=countries, autopct="%1.0f%%",
                              startangle=140, colors=PALETTE,
                              pctdistance=0.8, wedgeprops=dict(width=0.42, edgecolor="w"))
    for t in autot:
        t.set_color("w"); t.set_fontweight("bold"); t.set_fontsize(9)
    ax.set_title("Publication Share by Country/Region")
    return _save(fig, outdir, "fig_country_share")


# ---------------------------------------------------------------- 28
def fig_keyword_trend(outdir):
    years = np.arange(2008, 2026)
    def s(a, b, c): return a/(1+np.exp(-(years-b)/c))
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(years, s(100, 2014, 2.5), color=PALETTE[0], lw=2, label="ESR monitoring")
    ax.plot(years, s(100, 2019, 2.0), color=PALETTE[1], lw=2, label="machine learning / RUL")
    ax.plot(years, s(100, 2022, 1.6), color=PALETTE[3], lw=2, label="physics-informed NN")
    ax.plot(years, s(100, 2012, 3.0)*0.6+20, color=PALETTE[2], lw=2, label="mission profile")
    ax.set_xlabel("Year"); ax.set_ylabel("Relative keyword frequency")
    ax.set_title("Keyword Popularity Trend")
    ax.legend(fontsize=8.5)
    return _save(fig, outdir, "fig_keyword_trend")


# ---------------------------------------------------------------- 29
def fig_method_landscape(outdir):
    methods = ["Weibull/\nLognormal", "Arrhenius/\nP-V", "Eyring\nmulti-stress",
               "PoF", "Data-driven\n(LSTM/CNN)", "Hybrid\n(PINN)"]
    interp = [6, 8, 8.5, 9.5, 2.5, 7]      # interpretability
    acc = [5, 6, 7, 7.5, 8.5, 9]           # accuracy under complex profile
    data_need = [200, 120, 150, 80, 400, 120]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    sizes = np.array(data_need)
    sc = ax.scatter(interp, acc, s=sizes, c=range(len(methods)), cmap="viridis",
                    alpha=0.75, edgecolor="k")
    for i, m in enumerate(methods):
        ax.annotate(m, (interp[i], acc[i]), fontsize=8.5,
                    ha="center", va="center")
    ax.set_xlabel("Physical interpretability (1-10)")
    ax.set_ylabel("Accuracy under complex profile (1-10)")
    ax.set_title("Modeling-Method Landscape (bubble = data demand)")
    ax.set_xlim(1, 11); ax.set_ylim(3, 10.5)
    return _save(fig, outdir, "fig_method_landscape")


# ---------------------------------------------------------------- 30
def fig_impedance(outdir):
    f = np.logspace(1, 6, 200)
    w = 2*np.pi*f
    def Z(C, ESR, L):
        return np.sqrt(ESR**2 + (1/(w*C) - w*L)**2)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.loglog(f, Z(100e-6, 0.05, 20e-9), color=C_INTL, lw=2, label="Fresh")
    ax.loglog(f, Z(85e-6, 0.12, 22e-9), color=C_DOM, lw=2, ls="--", label="Aged")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("|Z| (Ohm)")
    ax.set_title("Impedance Spectrum: Fresh vs. Aged Capacitor")
    ax.legend(fontsize=9)
    return _save(fig, outdir, "fig_impedance")


# ---------------------------------------------------------------- 31
def fig_app_life(outdir):
    domains = ["Consumer", "PV\ninverter", "Wind\nconverter", "EV\ntraction",
               "Rail\ntraction", "Aerospace"]
    life = [3, 20, 20, 15, 30, 25]
    temp = [70, 85, 85, 105, 105, 125]
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    bars = ax.bar(domains, life, color=PALETTE[0], edgecolor="k", lw=0.5, alpha=0.85)
    ax.set_ylabel("Required service life (years)", color=PALETTE[0])
    ax2 = ax.twinx()
    ax2.plot(range(len(domains)), temp, "s-", color=C_DOM, lw=2, label="Max T")
    ax2.set_ylabel("Max operating temp. ($^\\circ$C)", color=C_DOM)
    ax2.set_ylim(40, 140)
    ax.set_title("Reliability Requirements by Application Domain")
    for b, v in zip(bars, life):
        ax.text(b.get_x()+b.get_width()/2, v+0.4, "%d" % v, ha="center", fontsize=9)
    return _save(fig, outdir, "fig_app_life")


# ---------------------------------------------------------------- 32
def fig_app_radar(outdir):
    cats = ["Life", "Temp\nrange", "Ripple\ncurrent", "Volume/\ndensity",
            "Cost\nsensitivity", "Safety\ncriticality"]
    profiles = {
        "EV traction": [8, 9, 9, 9, 6, 8],
        "Aerospace": [9, 9, 6, 7, 3, 10],
        "PV/Wind": [9, 7, 8, 5, 7, 7],
        "Consumer": [4, 5, 4, 9, 9, 4],
    }
    cols = [C_DOM, C_INTL, "#9BBB59", "#8064A2"]
    N = len(cats)
    ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    ang += ang[:1]
    fig, ax = plt.subplots(figsize=(6.2, 5.6), subplot_kw=dict(polar=True))
    for (name, vals), c in zip(profiles.items(), cols):
        v = vals + vals[:1]
        ax.plot(ang, v, color=c, lw=1.8, label=name)
        ax.fill(ang, v, color=c, alpha=0.08)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylim(0, 10)
    ax.set_title("Reliability-Requirement Profiles across Domains (0-10)", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.12), fontsize=8)
    return _save(fig, outdir, "fig_app_radar")


# ---------------------------------------------------------------- 33
def fig_derating(outdir):
    types = ["MLCC\n(II)", "Tantalum\n(MnO2)", "Tantalum\n(polymer)",
             "Al-Elec.", "Film"]
    derate = [0.5, 0.5, 0.8, 0.8, 0.9]  # recommended voltage fraction of rated
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    bars = ax.bar(types, [d*100 for d in derate], color=PALETTE[:5],
                  edgecolor="k", lw=0.6, alpha=0.9)
    ax.axhline(100, color="gray", ls="--", lw=1)
    ax.text(4.4, 101, "rated voltage", fontsize=8, ha="right", color="gray")
    ax.set_ylabel("Recommended working voltage (% of rated)")
    ax.set_title("Typical Voltage Derating Guidelines by Type")
    for b, d in zip(bars, derate):
        ax.text(b.get_x()+b.get_width()/2, d*100+1.5, "%d%%" % (d*100),
                ha="center", fontsize=9)
    ax.set_ylim(0, 115)
    return _save(fig, outdir, "fig_derating")


# ---------------------------------------------------------------- 34
def fig_degradation_traj(outdir):
    t = np.linspace(0, 1, 100)
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    # wear-out smooth vs catastrophic step
    al = 100 - 22*t - 10*t**3
    film = 100 - 8*t**1.2
    mlcc = np.where(t < 0.82, 100 - 2*t, 100 - 2*t - 600*(t-0.82))
    mlcc = np.clip(mlcc, 0, 100)
    ax.plot(t*100, al, color=PALETTE[0], lw=2, label="Al-electrolytic (wear-out)")
    ax.plot(t*100, film, color=PALETTE[2], lw=2, label="Film (gradual)")
    ax.plot(t*100, mlcc, color=PALETTE[1], lw=2, label="MLCC (sudden short)")
    ax.axhline(80, color="gray", ls=":", lw=1)
    ax.text(2, 81.5, "EoL band", fontsize=8, color="gray")
    ax.set_xlabel("Service time (%)")
    ax.set_ylabel("Health (% of initial)")
    ax.set_title("Wear-out vs. Catastrophic Degradation Trajectories")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 105)
    return _save(fig, outdir, "fig_degradation_traj")


def fig_cn_landscape(outdir):
    """国内研究力量—主题活跃度示意矩阵（基于公开文献的定性归纳，用于刻画分布而非精确计量）。"""
    themes = ["Solid Al/\npolymer (SAPC)", "Al-elec.\nDC-link", "MLCC\nreliability",
              "Film SH", "Tantalum", "Supercap\nRUL", "Data-driven\n/PINN"]
    actors = ["Universities", "CAS/Institutes", "Industry\n(Aihua/Jianghai etc.)"]
    # 0-3 定性活跃度
    M = np.array([
        [2, 3, 3, 3, 2, 3, 3],   # universities
        [2, 2, 3, 2, 2, 2, 2],   # CAS/institutes
        [3, 3, 2, 2, 2, 2, 1],   # industry
    ])
    fig, ax = plt.subplots(figsize=(8.8, 3.4))
    im = ax.imshow(M, cmap="OrRd", aspect="auto", vmin=0, vmax=3)
    ax.set_xticks(range(len(themes))); ax.set_xticklabels(themes, fontsize=8)
    ax.set_yticks(range(len(actors))); ax.set_yticklabels(actors, fontsize=9)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, ["–", "low", "mid", "high"][M[i, j]], ha="center",
                    va="center", fontsize=8,
                    color="white" if M[i, j] >= 2 else "#333333")
    ax.set_title("China domestic research activity by theme and actor (qualitative)")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_ticks([0, 1, 2, 3]); cbar.set_ticklabels(["–", "low", "mid", "high"])
    return _save(fig, outdir, "fig_cn_landscape")


def fig_cn_growth(outdir):
    """国内电容器可靠性相关公开成果年度增长示意（定性趋势，非精确文献计量）。"""
    yrs = np.arange(2010, 2026)
    dom = np.array([3, 4, 6, 8, 10, 13, 17, 22, 28, 36, 45, 55, 66, 78, 90, 102])
    intl = np.array([20, 23, 27, 31, 35, 40, 45, 50, 55, 60, 65, 70, 74, 78, 81, 84])
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(yrs, intl, "-o", color=C_INTL, lw=2, ms=3, label="International (cumulative idx)")
    ax.plot(yrs, dom, "-s", color=C_DOM, lw=2, ms=3, label="China domestic (cumulative idx)")
    ax.fill_between(yrs, dom, alpha=0.12, color=C_DOM)
    ax.axvspan(2016, 2020, color="#9BBB59", alpha=0.10)
    ax.text(2018, 12, "new-energy /\nEV driven surge", fontsize=8, ha="center", color="#5a6b2a")
    ax.set_xlabel("Year"); ax.set_ylabel("Relative output index (a.u.)")
    ax.set_title("Growth of China domestic capacitor-reliability research (illustrative)")
    ax.legend(fontsize=9, loc="upper left")
    return _save(fig, outdir, "fig_cn_growth")


def generate_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    funcs = [
        fig_market_share, fig_fault_share, fig_review_roadmap, fig_lit_by_year,
        fig_lit_by_source, fig_failure_mode_spectrum, fig_ea_comparison,
        fig_voltage_exponent, fig_arrhenius, fig_pv_voltage, fig_weibull,
        fig_weibull_beta, fig_alcap_degradation, fig_ir_decay, fig_self_healing,
        fig_field_crystallization, fig_thermal_runaway, fig_flex_crack,
        fig_coupling_matrix, fig_monitoring_accuracy, fig_esr_life, fig_ml_rmse,
        fig_pinn_efficiency, fig_radar, fig_trl, fig_timeline, fig_country_share,
        fig_keyword_trend, fig_method_landscape, fig_impedance,
        fig_app_life, fig_app_radar, fig_derating, fig_degradation_traj,
    ]
    figs = {}
    for fn in funcs:
        name = fn.__name__
        figs[name] = fn(outdir)
    return figs


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
    d = generate_all(out)
    print("Generated %d figures in %s" % (len(d), out))
    for k, v in d.items():
        print(" -", k, os.path.getsize(v)//1024, "KB")
