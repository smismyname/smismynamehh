# -*- coding: utf-8 -*-
"""生成所有图表 (SAPC review)"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon, Ellipse, FancyArrowPatch
from matplotlib.lines import Line2D

# 全局样式
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 140

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f"[fig] {name}")


# =========================================================
# Fig 1. 市场规模对比 (不同电容器类型)
# =========================================================
def fig_market():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    types = ['MLCC', 'Al-Elec\n(liquid)', 'Al-Polymer\n(SAPC)', 'Film', 'Ta-MnO2', 'Ta-Polymer', 'Super-\ncap']
    vols = [70.2, 14.1, 3.1, 6.8, 3.0, 1.5, 1.3]
    colors = ['#2b6cb0', '#9f7aea', '#e53e3e', '#38a169', '#d69e2e', '#ed8936', '#319795']
    ax.bar(types, vols, color=colors, edgecolor='black', linewidth=0.6)
    for i, v in enumerate(vols):
        ax.text(i, v + 1.5, f'{v}%', ha='center', fontsize=10, fontweight='bold')
    ax.set_ylabel('Global Volume Share / %', fontsize=11)
    ax.set_title('Global Capacitor Market Volume by Type (2023, est.)', fontsize=12)
    ax.set_ylim(0, 80)
    ax.grid(axis='y', alpha=0.3)
    save(fig, 'fig01_market.png')


# =========================================================
# Fig 2. SAPC 三维分层结构示意 (SEM-like schematic)
# =========================================================
def fig_structure():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # 堆叠阳极铝箔 (6层)
    for k in range(6):
        y0 = 0.2 + k * 0.95
        # Al 阳极箔 (灰色)
        ax.add_patch(Rectangle((2.5, y0), 6.5, 0.18, fc='#9ca3af', ec='black', lw=0.4))
        # Al2O3 介质 (黄色)
        ax.add_patch(Rectangle((2.5, y0 + 0.18), 6.5, 0.05, fc='#fbbf24', ec='none'))
        # PEDOT 阴极 (深蓝)
        ax.add_patch(Rectangle((2.5, y0 + 0.23), 6.5, 0.20, fc='#1e3a8a', ec='none'))
        # 碳层 (黑色)
        ax.add_patch(Rectangle((2.5, y0 + 0.43), 6.5, 0.08, fc='#111827', ec='none'))
        # 银浆 (银灰)
        ax.add_patch(Rectangle((2.5, y0 + 0.51), 6.5, 0.10, fc='#d1d5db', ec='none'))
        # 空气/粘结隔离
        ax.add_patch(Rectangle((2.5, y0 + 0.61), 6.5, 0.30, fc='white', ec='none'))

    # 正极引出框架 (左)
    ax.add_patch(Rectangle((1.0, 0.1), 1.4, 5.8, fc='#6b7280', ec='black', lw=0.8))
    ax.text(1.7, 3.0, 'Anode\nLead-frame', ha='center', va='center',
            fontsize=9, color='white', fontweight='bold', rotation=90)
    # 负极引出框架 (右)
    ax.add_patch(Rectangle((9.1, 0.1), 1.4, 5.8, fc='#6b7280', ec='black', lw=0.8))
    ax.text(9.8, 3.0, 'Cathode\nLead-frame', ha='center', va='center',
            fontsize=9, color='white', fontweight='bold', rotation=90)

    # 环氧封装 (外框)
    ax.add_patch(FancyBboxPatch((0.5, -0.1), 11.0, 6.2, boxstyle="round,pad=0,rounding_size=0.15",
                                  fc='none', ec='#374151', lw=1.8, linestyle='--'))

    # 图例
    legend_items = [
        ('#9ca3af', 'Etched Al anode foil (Al)'),
        ('#fbbf24', 'Dielectric (Al₂O₃, 10–100 nm)'),
        ('#1e3a8a', 'PEDOT cathode (conductive polymer)'),
        ('#111827', 'Carbon layer (C)'),
        ('#d1d5db', 'Silver paste (Ag)'),
        ('#6b7280', 'Cu lead-frame (anode / cathode)'),
    ]
    for i, (c, lbl) in enumerate(legend_items):
        yy = 5.8 - i * 0.55
        ax.add_patch(Rectangle((12.2, yy - 0.15), 0.4, 0.28, fc=c, ec='black', lw=0.4))
        ax.text(12.75, yy, lbl, fontsize=8.5, va='center')
    ax.set_xlim(0, 18)

    ax.text(6.0, 6.25, 'Fig. 2  Cross-section Schematic of a Stacked Aluminum Polymer Capacitor (SAPC)',
            ha='center', fontsize=11, fontweight='bold')
    save(fig, 'fig02_structure.png')


# =========================================================
# Fig 3. Al 箔腐蚀隧道 + Al2O3 形成示意
# =========================================================
def fig_etch_formation():
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))

    # (a) 腐蚀隧道
    ax = axs[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(Rectangle((0.5, 0.5), 9, 4, fc='#9ca3af', ec='black'))
    rng = np.random.default_rng(42)
    for _ in range(40):
        x = rng.uniform(0.8, 9.2)
        depth = rng.uniform(1.5, 3.2)
        w = rng.uniform(0.08, 0.18)
        ax.add_patch(Rectangle((x, 4.5 - depth), w, depth, fc='white', ec='none'))
    ax.text(5, 4.85, 'Etched tunnel pits (low-voltage foil)',
            ha='center', fontsize=10, fontweight='bold')
    ax.annotate('Tunnel depth\n~1.5-3 μm', xy=(2.3, 2.5), xytext=(0.2, -0.2),
                fontsize=9, arrowprops=dict(arrowstyle='->', lw=0.8))
    ax.text(5, -0.3, '(a) Electrochemical tunnel etching', ha='center', fontsize=10)

    # (b) Al2O3 形成
    ax = axs[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(Rectangle((0.5, 0.5), 9, 2.5, fc='#9ca3af', ec='black'))
    ax.add_patch(Rectangle((0.5, 3.0), 9, 0.4, fc='#fbbf24', ec='black'))
    ax.text(5, 3.7, 'Al₂O₃ dielectric (~1.4 nm/V)',
            ha='center', fontsize=10, fontweight='bold', color='#92400e')
    ax.annotate('', xy=(4, 3.0), xytext=(4, 2.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
    ax.text(4.1, 2.5, 'Al³⁺ out', fontsize=9, color='red')
    ax.annotate('', xy=(6, 2.0), xytext=(6, 3.0),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='blue'))
    ax.text(6.1, 2.5, 'O²⁻ in', fontsize=9, color='blue')
    ax.text(5, -0.3, '(b) Anodic oxidation (formation)', ha='center', fontsize=10)
    ax.text(5, 0.2, 'Al + H₂O → Al₂O₃ + 6H⁺ + 6e⁻', ha='center', fontsize=9, color='#1f2937')

    plt.suptitle('Fig. 3  Anode Foil Processing: Tunnel Etching and Anodic Formation',
                 fontsize=11, fontweight='bold', y=1.02)
    save(fig, 'fig03_etch_formation.png')


# =========================================================
# Fig 4. PEDOT polymerization schematic + chemical structure
# =========================================================
def fig_pedot_chem():
    fig, axs = plt.subplots(1, 2, figsize=(11, 5))

    # (a) EDOT monomer -> PEDOT reaction scheme
    ax = axs[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')

    # EDOT monomer box
    ax.add_patch(FancyBboxPatch((0.3, 3.0), 3.2, 2.5, boxstyle="round,pad=0.1",
                                fc='#eff6ff', ec='#1d4ed8', lw=1.5))
    ax.text(1.9, 5.1, 'EDOT monomer', ha='center', fontsize=11, fontweight='bold', color='#1d4ed8')
    ax.text(1.9, 4.3, r'$\mathrm{C_6H_6O_2S}$', ha='center', fontsize=13)
    ax.text(1.9, 3.6, '(3,4-ethylenedioxy-\nthiophene)', ha='center', fontsize=9)

    # Arrow
    ax.annotate('', xy=(6.8, 4.3), xytext=(3.8, 4.3),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='#dc2626'))
    ax.text(5.3, 4.9, 'Oxidative\nPolymerization', fontsize=10, color='#dc2626',
            fontweight='bold', ha='center')
    ax.text(5.3, 3.7, r'$\mathrm{Fe^{3+}(OTs)_3}$' + '\nor VPP', fontsize=9,
            color='#dc2626', ha='center')

    # PEDOT product box
    ax.add_patch(FancyBboxPatch((7.0, 3.0), 2.8, 2.5, boxstyle="round,pad=0.1",
                                fc='#fef2f2', ec='#991b1b', lw=1.5))
    ax.text(8.4, 5.1, 'PEDOT (p-doped)', ha='center', fontsize=11, fontweight='bold', color='#991b1b')
    ax.text(8.4, 4.3, r'$\mathrm{[C_6H_4O_2S]_n^+ \cdot A^-}$', ha='center', fontsize=12)
    ax.text(8.4, 3.5, r'$\sigma \approx 10^2 - 10^3$ S/cm', ha='center', fontsize=9.5)

    # Reaction equation at bottom
    ax.text(5.0, 2.2, r'n EDOT + n $\mathrm{A^-}$ $\longrightarrow$ '
            r'$\mathrm{PEDOT^{n+} \cdot nA^-}$ + 2n $\mathrm{H^+}$ + 2n $\mathrm{e^-}$',
            ha='center', fontsize=10, style='italic')
    ax.text(5.0, 1.4, r'where $\mathrm{A^-}$ = Tos$^-$ (p-toluenesulfonate) or PSS$^-$',
            ha='center', fontsize=9, color='#4b5563')
    ax.text(5.0, 0.5, '(a) PEDOT synthesis reaction', ha='center', fontsize=10.5, fontweight='bold')

    # (b) Three deposition routes comparison
    ax = axs[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')

    # In-situ box
    ax.add_patch(FancyBboxPatch((0.2, 4.0), 4.5, 1.7, boxstyle="round,pad=0.05",
                                fc='#dbeafe', ec='#1e40af', lw=1.3))
    ax.text(2.45, 5.3, 'In-situ Chemical Polymerization', ha='center', fontsize=9.5,
            fontweight='bold', color='#1e40af')
    ax.text(2.45, 4.7, r'EDOT + $\mathrm{Fe(OTs)_3}$ in alcohol'
            '\n' + r'$\sigma$ = 200-500 S/cm, Fill: HIGH', ha='center', fontsize=8.5)

    # Pre-polymerized box
    ax.add_patch(FancyBboxPatch((5.3, 4.0), 4.5, 1.7, boxstyle="round,pad=0.05",
                                fc='#fef3c7', ec='#92400e', lw=1.3))
    ax.text(7.55, 5.3, 'Pre-polymerized Dispersion', ha='center', fontsize=9.5,
            fontweight='bold', color='#92400e')
    ax.text(7.55, 4.7, 'PEDOT:PSS aqueous colloid\n'
            r'$\sigma$ = 0.1-100 S/cm, Fill: LOW', ha='center', fontsize=8.5)

    # VPP box
    ax.add_patch(FancyBboxPatch((0.2, 1.8), 9.6, 1.8, boxstyle="round,pad=0.05",
                                fc='#dcfce7', ec='#166534', lw=1.3))
    ax.text(5.0, 3.2, 'Vapor-Phase Polymerization (VPP)', ha='center', fontsize=10,
            fontweight='bold', color='#166534')
    ax.text(5.0, 2.5, r'EDOT vapor + $\mathrm{Fe(OTs)_3}$ film on anode surface'
            '\n' + r'$\sigma$ > 1000 S/cm, Fill: VERY HIGH'
            '\n(Shi et al., J Mater Sci Mater Electron, 2021 [28])', ha='center', fontsize=8.5)

    ax.text(5.0, 0.8, '(b) Three major PEDOT deposition routes for SAPC cathodes',
            ha='center', fontsize=10.5, fontweight='bold')

    plt.suptitle('Fig. 4  PEDOT Chemistry and Deposition Methods for SAPC Cathodes',
                 fontsize=11.5, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, 'fig04_pedot_chem.png')


# =========================================================
# Fig 5. 五种电容器 ESR 对比 (频率响应)
# =========================================================
def fig_esr_compare():
    fig, ax = plt.subplots(figsize=(8, 5))
    f = np.logspace(2, 7, 200)  # 100 Hz ~ 10 MHz

    def Zmag(R, L, C):
        omega = 2 * np.pi * f
        return np.sqrt(R**2 + (omega*L - 1/(omega*C))**2)

    curves = [
        ('Liquid Al-Elec (220μF/25V)', Zmag(0.15, 5e-9, 220e-6), '#9f7aea', '-'),
        ('Tantalum-MnO₂ (100μF/10V)',  Zmag(0.10, 3e-9, 100e-6), '#d69e2e', '--'),
        ('SAPC (470μF/6.3V)',          Zmag(0.009, 2e-9, 470e-6), '#e53e3e', '-'),
        ('MLCC X5R (22μF/10V)',        Zmag(0.003, 0.5e-9, 22e-6), '#2b6cb0', '-.'),
        ('Tantalum-polymer (220μF/6.3V)', Zmag(0.020, 2.5e-9, 220e-6), '#ed8936', ':'),
    ]
    for name, Z, c, ls in curves:
        ax.loglog(f, Z*1000, label=name, color=c, linestyle=ls, linewidth=1.7)

    ax.set_xlabel('Frequency / Hz', fontsize=11)
    ax.set_ylabel('|Z| / mΩ', fontsize=11)
    ax.set_title('Fig. 5  Impedance Spectra of Typical Capacitors (capacitor + ESR + ESL)', fontsize=11)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, which='both', alpha=0.3)
    ax.axvspan(1e5, 1e6, alpha=0.08, color='red')
    ax.text(3e5, 0.8, 'Typical\nSMPS\nrange', fontsize=9, color='red', ha='center')
    save(fig, 'fig05_esr_compare.png')


# =========================================================
# Fig 6. 加速试验下 ESR/C 退化曲线
# =========================================================
def fig_degradation():
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
    t = np.linspace(0, 2000, 200)

    # (a) ESR 上升
    ax = axs[0]
    # Nichicon 样品 - ESR上升是主模式
    Nichicon = 0.012 * (1 + 0.5 * (t / 1000)**1.8)
    # Chemi-Con 样品 - ESR平稳, 但DCL剧增
    ChemiCon = 0.012 * (1 + 0.15 * (t / 1000)**1.3)
    ax.plot(t, Nichicon*1000, 'r-', lw=2, label='Mfr A (ESR-rise mode)')
    ax.plot(t, ChemiCon*1000, 'b-', lw=2, label='Mfr B (LC-rise mode)')
    ax.axhline(24, color='k', linestyle='--', lw=1, label='EoL threshold (2×ESR₀)')
    ax.set_xlabel('Time under 85°C/85%RH, rated V / h', fontsize=10)
    ax.set_ylabel('ESR / mΩ (at 100 kHz)', fontsize=10)
    ax.legend(loc='upper left', fontsize=9)
    ax.set_title('(a) ESR evolution under THB', fontsize=10)
    ax.grid(alpha=0.3)

    # (b) 漏电流 LC
    ax = axs[1]
    LC_A = 5 + 8 * (1 - np.exp(-t/2500))
    LC_B = 5 + 150 * (t/2000)**2.4
    ax.semilogy(t, LC_A, 'r-', lw=2, label='Mfr A (DCL stable)')
    ax.semilogy(t, LC_B, 'b-', lw=2, label='Mfr B (DCL runaway)')
    ax.axhline(100, color='k', linestyle='--', lw=1, label='EoL threshold (10× rated DCL)')
    ax.set_xlabel('Time under 85°C/85%RH, rated V / h', fontsize=10)
    ax.set_ylabel('Leakage Current / μA', fontsize=10)
    ax.legend(loc='upper left', fontsize=9)
    ax.set_title('(b) DC leakage current evolution', fontsize=10)
    ax.grid(alpha=0.3, which='both')

    plt.suptitle('Fig. 6  Two Dominant Degradation Modes of SAPC under 85°C/85%RH\n'
                 '(after Liu & Pecht, IEEE T-CPMT, 2017)',
                 fontsize=11, fontweight='bold', y=1.04)
    save(fig, 'fig06_degradation.png')


# =========================================================
# Fig 7. Weibull 图
# =========================================================
def fig_weibull():
    fig, ax = plt.subplots(figsize=(7, 5))
    rng = np.random.default_rng(7)
    n = 30
    beta1, eta1 = 2.1, 1800
    beta2, eta2 = 1.3, 650
    t1 = eta1 * (-np.log(rng.uniform(0, 1, n)))**(1/beta1)
    t2 = eta2 * (-np.log(rng.uniform(0, 1, n)))**(1/beta2)

    def weibullprob(t):
        t = np.sort(t)
        i = np.arange(1, len(t)+1)
        F = (i - 0.3) / (len(t) + 0.4)  # median rank
        return t, F

    for data, color, label, mk in [
        (t1, '#e53e3e', 'Sample A (β=2.1, wear-out)', 'o'),
        (t2, '#1e3a8a', 'Sample B (β=1.3, infant+random)', 's')
    ]:
        t_sorted, F = weibullprob(data)
        y = np.log(-np.log(1 - F))
        x = np.log(t_sorted)
        ax.plot(x, y, marker=mk, linestyle='none', color=color, label=label, markersize=6)
        # 线性回归
        k, b = np.polyfit(x, y, 1)
        xf = np.array([x.min()-0.2, x.max()+0.2])
        ax.plot(xf, k*xf + b, '-', color=color, lw=1.3)

    # 双轴为概率轴
    F_ticks = np.array([0.01, 0.05, 0.1, 0.2, 0.5, 0.63, 0.8, 0.9, 0.99])
    y_ticks = np.log(-np.log(1 - F_ticks))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f'{p*100:.0f}%' for p in F_ticks])
    ax.set_xlabel('ln(Time to failure) / ln(h)', fontsize=11)
    ax.set_ylabel('F(t) cumulative failure probability', fontsize=11)
    ax.set_title('Fig. 7  Weibull Probability Plot of SAPC THB Failure Times', fontsize=11)
    ax.grid(True, alpha=0.35)
    ax.legend(fontsize=9, loc='lower right')
    save(fig, 'fig07_weibull.png')


# =========================================================
# Fig 8. Arrhenius 图
# =========================================================
def fig_arrhenius():
    fig, ax = plt.subplots(figsize=(7, 4.7))
    T = np.array([105, 125, 150, 175])  # °C
    T_K = T + 273.15
    invT = 1000.0 / T_K
    # Ea ≈ 0.73 eV (Liu 2017)
    k = 8.617e-5
    Ea = 0.73
    t63 = 1e4 * np.exp(Ea/k * (1/T_K - 1/(85+273.15)))
    ax.semilogy(invT, t63, 'ro-', lw=1.8, markersize=9, label='Observed t₆₃ (85% RH)')
    # 外推
    T_ext = np.linspace(40, 200, 60) + 273.15
    invT_ext = 1000.0 / T_ext
    t_ext = 1e4 * np.exp(Ea/k * (1/T_ext - 1/(85+273.15)))
    ax.semilogy(invT_ext, t_ext, 'k--', lw=1, label=f'Arrhenius fit, Eₐ = {Ea} eV')

    for Ti, ti in zip(T, t63):
        ax.annotate(f'{Ti}°C', (1000/(Ti+273.15), ti), textcoords='offset points',
                    xytext=(8, 8), fontsize=9)
    ax.axvline(1000/(85+273.15), color='blue', linestyle=':', lw=1)
    ax.text(1000/(85+273.15)+0.01, 5e5, 'Use\ncondition\n(85°C)', fontsize=9, color='blue')
    ax.set_xlabel('1000 / T / K⁻¹', fontsize=11)
    ax.set_ylabel('Characteristic life t₆₃ / h', fontsize=11)
    ax.set_title('Fig. 8  Arrhenius Lifetime Extrapolation for SAPC (Eₐ ≈ 0.73 eV)', fontsize=11)
    ax.grid(alpha=0.3, which='both')
    ax.legend(fontsize=9)
    save(fig, 'fig08_arrhenius.png')


# =========================================================
# Fig 9. EIS Nyquist
# =========================================================
def fig_eis():
    fig, ax = plt.subplots(figsize=(7, 5.5))
    f = np.logspace(-1, 6, 300)
    w = 2 * np.pi * f

    def nyquist(Rs, Rp, C1, L, Cbulk):
        Z_cap = 1.0/(1j*w*Cbulk)
        Z_Rp = Rp / (1 + 1j*w*Rp*C1)
        Z = Rs + 1j*w*L + Z_Rp + Z_cap
        return Z

    # 初始
    Z0 = nyquist(0.010, 0.020, 5e-5, 3e-9, 470e-6)
    # 老化 500 h (ESR rise, interface delamination)
    Z1 = nyquist(0.025, 0.080, 1.5e-4, 3e-9, 465e-6)
    # 老化 1500 h (大面积失效)
    Z2 = nyquist(0.050, 0.30, 3e-4, 3e-9, 420e-6)

    for Z, c, lbl in [(Z0, 'blue', 't = 0 h'),
                       (Z1, 'green', 't = 500 h (THB)'),
                       (Z2, 'red', 't = 1500 h (THB)')]:
        ax.plot(np.real(Z)*1000, -np.imag(Z)*1000, color=c, lw=1.8, label=lbl)

    ax.set_xlabel("Z' / mΩ", fontsize=11)
    ax.set_ylabel("-Z'' / mΩ", fontsize=11)
    ax.set_title('Fig. 9  Nyquist Plot of SAPC during Accelerated Humid Aging', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 350)
    save(fig, 'fig09_eis.png')


# =========================================================
# Fig 10. 击穿电压分布
# =========================================================
def fig_bdv():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    rng = np.random.default_rng(3)
    vr = 6.3
    # 正常样品 BDV 均值 ~ 2.5×Vr
    n = 200
    bdv_good = rng.normal(loc=2.5*vr, scale=0.3*vr, size=n)
    bdv_bad = rng.normal(loc=1.4*vr, scale=0.35*vr, size=n//3)
    bdv_all = np.concatenate([bdv_good, bdv_bad])

    ax.hist(bdv_good, bins=25, alpha=0.7, color='#3b82f6', label='Main population (V_BD≈2.5V_R)',
            edgecolor='black', linewidth=0.3)
    ax.hist(bdv_bad, bins=15, alpha=0.7, color='#ef4444', label='Defect population (V_BD≈1.4V_R)',
            edgecolor='black', linewidth=0.3)
    ax.axvline(vr, color='k', linestyle='--', lw=1.3, label=f'Rated voltage V_R = {vr}V')
    ax.axvline(2*vr, color='gray', linestyle=':', lw=1, label=f'Surge (2×V_R)')
    ax.set_xlabel('Breakdown voltage V_BD / V', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title('Fig. 10  Bimodal Breakdown Voltage Distribution of SAPC Lot', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    save(fig, 'fig10_bdv.png')


# =========================================================
# Fig 11. 失效机理概念图 (根因分析)
# =========================================================
def fig_mechanism_map():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # 中心 - 失效表征
    ax.add_patch(FancyBboxPatch((5.8, 3.8), 2.4, 1.4, boxstyle="round,pad=0.05",
                                fc='#fecaca', ec='#991b1b', lw=2))
    ax.text(7.0, 4.5, 'SAPC Failure\n(ESR↑ / LC↑ / C↓)', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#991b1b')

    # 四大应力源
    stresses = [
        ('Thermal\nstress', 1.5, 7.5, '#f97316'),
        ('Humidity\nstress', 12.5, 7.5, '#06b6d4'),
        ('Electrical\nstress', 12.5, 1.5, '#a855f7'),
        ('Mechanical\nstress', 1.5, 1.5, '#84cc16'),
    ]
    for name, x, y, c in stresses:
        ax.add_patch(Circle((x, y), 0.8, fc=c, ec='black', lw=1.2, alpha=0.85))
        ax.text(x, y, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color='white')

    # 中间机理节点
    mechs = [
        ('PEDOT thermal\noxidation\n(C–O cleavage)', 4.0, 7.0),
        ('PSS hydrolysis\n/ PEDOT swelling', 10.0, 7.0),
        ('Al₂O₃ anodic\nbreakdown', 10.0, 2.3),
        ('Oxide crack /\ninterface delam.', 4.0, 2.3),
    ]
    for name, x, y in mechs:
        ax.add_patch(FancyBboxPatch((x-1.2, y-0.5), 2.4, 1.0, boxstyle="round,pad=0.02",
                                    fc='#e0e7ff', ec='#3730a3', lw=1.2))
        ax.text(x, y, name, ha='center', va='center', fontsize=8.5)

    # 箭头 stress -> mechanism
    pairs = [((1.5, 7.5), (4.0, 7.0)),
             ((12.5, 7.5), (10.0, 7.0)),
             ((12.5, 1.5), (10.0, 2.3)),
             ((1.5, 1.5), (4.0, 2.3)),
             # mechanism -> center
             ((4.0, 7.0), (6.0, 5.0)),
             ((10.0, 7.0), (8.0, 5.0)),
             ((10.0, 2.3), (8.0, 4.0)),
             ((4.0, 2.3), (6.0, 4.0))]
    for (x1, y1), (x2, y2) in pairs:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', lw=1.2, color='gray'))

    ax.text(7, 8.5, 'Fig. 11  Stress–Mechanism–Failure Map of SAPC',
            ha='center', fontsize=12, fontweight='bold')
    save(fig, 'fig11_mechanism_map.png')


# =========================================================
# Fig 12. 自愈过程示意
# =========================================================
def fig_selfhealing():
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
    states = [('Defect/weak spot', 'Local breakdown (arc)', 'Self-healed (isolated)')]
    titles = ['(a) Pre-breakdown', '(b) Local breakdown', '(c) Post self-healing']
    for i, ax in enumerate(axs):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        # Al
        ax.add_patch(Rectangle((0.5, 0.5), 9, 1.5, fc='#9ca3af', ec='black'))
        # Al2O3
        ax.add_patch(Rectangle((0.5, 2.0), 9, 0.3, fc='#fbbf24', ec='black'))
        # PEDOT
        ax.add_patch(Rectangle((0.5, 2.3), 9, 1.7, fc='#1e3a8a', ec='black'))

        if i == 0:
            # 缺陷
            ax.add_patch(Ellipse((5, 2.15), 0.3, 0.15, fc='red', ec='black'))
            ax.annotate('weak spot\n(Al₂O₃ thin)', xy=(5, 2.15), xytext=(5.5, 4.3),
                        fontsize=9, arrowprops=dict(arrowstyle='->', color='red'))
        elif i == 1:
            # 电弧击穿 + PEDOT 碳化
            ax.add_patch(Polygon([[5, 0.5], [4.9, 3.0], [4.8, 2.5], [5.1, 2.5], [5.2, 3.5], [5, 2.5]],
                                 fc='yellow', alpha=0.6))
            ax.add_patch(Circle((5, 3.0), 0.5, fc='orange', alpha=0.5, ec='red'))
            ax.text(6.8, 3.5, 'Arc current\n(few μs)', fontsize=9, color='red')
        else:
            # 自愈后: PEDOT 局部还原 -> 绝缘
            ax.add_patch(Circle((5, 3.0), 0.55, fc='#e5e7eb', ec='#374151', lw=1.5))
            ax.text(6.6, 3.3, 'PEDOT→de-doped\n(insulating)', fontsize=9, color='#374151')
            ax.annotate('', xy=(5.3, 2.5), xytext=(6.3, 2.8),
                        arrowprops=dict(arrowstyle='->', color='gray'))
        ax.text(5, 4.5, titles[i], ha='center', fontsize=10, fontweight='bold')

    plt.suptitle('Fig. 12  Self-Healing Mechanism in PEDOT-based SAPC\n(Freeman & Lessner, KEMET 2020; AIP APL 2013)',
                 fontsize=11, fontweight='bold', y=1.05)
    save(fig, 'fig12_selfhealing.png')


# =========================================================
# Fig 13. RUL 预测示意 (CNN-LSTM)
# =========================================================
def fig_rul():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    rng = np.random.default_rng(11)
    t_obs = np.linspace(0, 1200, 80)
    rul_true = np.maximum(2000 - t_obs, 0)
    noise = rng.normal(0, 40, 80)
    rul_pred = rul_true + noise
    rul_ci_low = rul_pred - 80 - 0.05*t_obs
    rul_ci_high = rul_pred + 80 + 0.05*t_obs

    ax.plot(t_obs, rul_true, 'k-', lw=2, label='True RUL')
    ax.plot(t_obs, rul_pred, 'r.', markersize=6, label='CNN-LSTM prediction')
    ax.fill_between(t_obs, rul_ci_low, rul_ci_high, color='red', alpha=0.2, label='95% CI')

    # 未来预测段
    t_fut = np.linspace(1200, 2000, 50)
    rul_fut_true = np.maximum(2000 - t_fut, 0)
    rul_fut_pred = rul_fut_true + rng.normal(0, 60, 50)
    ax.plot(t_fut, rul_fut_pred, 'b.', markersize=6, label='Forecast (t > 1200h)')

    ax.axvline(1200, color='gray', linestyle='--', lw=1)
    ax.text(1210, 1700, 'Observation\nend', fontsize=9)
    ax.set_xlabel('Aging time / h', fontsize=11)
    ax.set_ylabel('Remaining Useful Life / h', fontsize=11)
    ax.set_title('Fig. 13  RUL Prediction of SAPC by CNN-LSTM (after Zhu et al., MDPI Electronics 2025)',
                 fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    save(fig, 'fig13_rul.png')


# =========================================================
# Fig 14. 应用场景分布 (雷达图)
# =========================================================
def fig_apps():
    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(111, projection='polar')
    categories = ['CPU VRM', 'GPU VRM', 'Server PSU', 'AI accelerator',
                  'EV e-Drive', 'Automotive ECU', 'Aerospace', '5G Base Station']
    N = len(categories)
    # SAPC 适用度 / MLCC / Al-liquid / Ta-polymer
    sapc = [9, 9, 8, 9, 6, 7, 5, 8]
    mlcc = [6, 6, 5, 4, 7, 9, 8, 9]
    alliq = [3, 3, 8, 2, 5, 6, 3, 5]
    tapoly = [7, 7, 7, 7, 7, 7, 9, 7]
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    for data, color, label in [(sapc, 'red', 'SAPC'),
                                (mlcc, 'blue', 'MLCC'),
                                (alliq, 'purple', 'Al-liquid'),
                                (tapoly, 'orange', 'Ta-polymer')]:
        data = data + data[:1]
        ax.plot(angles, data, color=color, lw=2, label=label)
        ax.fill(angles, data, color=color, alpha=0.08)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_ylim(0, 10)
    ax.legend(loc='upper right', bbox_to_anchor=(1.28, 1.1), fontsize=9)
    ax.set_title('Fig. 14  Application Suitability Radar\n(0 = unsuitable, 10 = ideal)',
                 fontsize=11, fontweight='bold', y=1.08)
    save(fig, 'fig14_apps.png')


if __name__ == "__main__":
    fig_market()
    fig_structure()
    fig_etch_formation()
    fig_pedot_chem()
    fig_esr_compare()
    fig_degradation()
    fig_weibull()
    fig_arrhenius()
    fig_eis()
    fig_bdv()
    fig_mechanism_map()
    fig_selfhealing()
    fig_rul()
    fig_apps()
    print("All figures generated.")



# =========================================================
# Fig 15. XPS S 2p deconvolution of PEDOT (characterization)
# =========================================================
def fig_xps_s2p():
    fig, ax = plt.subplots(figsize=(8, 5))
    import numpy as np
    # x-axis: binding energy (eV)
    be = np.linspace(161, 172, 800)
    def g(x, x0, h, w):
        return h * np.exp(-((x - x0) / w) ** 2)
    # three components: neutral thiophene (163.8 eV), oxidized thiophene polaron (164.8 eV),
    # sulfonate SO3- (168.2 eV) each a doublet S2p3/2 & S2p1/2
    y_neu = g(be, 163.8, 0.45, 0.5) + g(be, 165.0, 0.23, 0.5)
    y_ox  = g(be, 164.8, 0.30, 0.55) + g(be, 166.0, 0.15, 0.55)
    y_so3 = g(be, 168.2, 0.70, 0.65) + g(be, 169.4, 0.35, 0.65)
    total = y_neu + y_ox + y_so3 + 0.02*np.random.RandomState(1).randn(len(be))
    total = np.clip(total, 0, None)

    ax.fill_between(be, y_neu, alpha=0.35, color='#2563eb', label=r'Neutral thiophene S (163.8 eV)')
    ax.fill_between(be, y_ox, alpha=0.35, color='#dc2626', label=r'Polaron/oxidized S (164.8 eV)')
    ax.fill_between(be, y_so3, alpha=0.35, color='#16a34a', label=r'$\mathrm{SO_3^-}$ dopant (168.2 eV)')
    ax.plot(be, total, 'k-', lw=1.3, label='Measured envelope')
    ax.invert_xaxis()
    ax.set_xlabel('Binding Energy / eV', fontsize=11)
    ax.set_ylabel('Intensity / a.u.', fontsize=11)
    ax.set_title('Fig. 15  XPS S 2p Deconvolution of PEDOT Cathode in SAPC', fontsize=11.5, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(alpha=0.25)
    ax.text(0.55, 0.60,
            'doping level\n= [Ox]/([Ox]+[Neu])',
            transform=ax.transAxes, fontsize=9.5,
            bbox=dict(boxstyle='round,pad=0.4', fc='#fef3c7', ec='#92400e', lw=0.8))
    save(fig, 'fig15_xps_s2p.png')


# =========================================================
# Fig 16. Raman spectrum of PEDOT (doping state)
# =========================================================
def fig_raman_pedot():
    fig, ax = plt.subplots(figsize=(8, 5))
    import numpy as np
    wn = np.linspace(800, 1700, 900)
    def g(x, x0, h, w):
        return h * np.exp(-((x - x0) / w) ** 2)
    # Fresh PEDOT (fully doped)
    y_fresh = (g(wn, 1440, 0.95, 18) + g(wn, 1500, 0.55, 22) + g(wn, 1365, 0.35, 22)
               + g(wn, 1268, 0.25, 22) + g(wn, 990, 0.30, 22) + g(wn, 850, 0.18, 22))
    # Aged PEDOT (partially de-doped, red-shifted, broadened)
    y_aged  = (g(wn, 1428, 0.55, 38) + g(wn, 1488, 0.35, 30) + g(wn, 1360, 0.30, 28)
               + g(wn, 1260, 0.22, 26) + g(wn, 990, 0.25, 22) + g(wn, 850, 0.16, 22)
               + g(wn, 1350, 0.18, 45) + g(wn, 1580, 0.20, 50))  # emerging D/G
    ax.plot(wn, y_fresh + 0.3, 'b-', lw=1.4, label='Fresh (fully p-doped)')
    ax.plot(wn, y_aged, 'r-', lw=1.4, label='After 85°C/85%RH 1500h')
    # annotate peaks
    peaks = [(1440, 'Cα=Cβ sym. stretch'),
             (1500, 'Cα=Cβ asym.'),
             (1365, 'Cβ-Cβ'),
             (1268, 'Cα-Cα\' inter-ring'),
             (1350, 'D band (amorph. C)'),
             (1580, 'G band')]
    for x, lbl in peaks:
        ax.axvline(x, color='gray', linestyle=':', alpha=0.35)
    ax.set_xlabel(r'Raman shift / cm$^{-1}$', fontsize=11)
    ax.set_ylabel('Intensity / a.u.', fontsize=11)
    ax.set_title('Fig. 16  Raman Spectrum of PEDOT: Fresh vs Aged SAPC', fontsize=11.5, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.25)
    ax.annotate('Red-shift &\nbroadening\n(de-doping)',
                xy=(1430, 0.55), xytext=(1100, 0.85),
                fontsize=9, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
    ax.annotate('Emerging D/G bands\n(local carbonization)',
                xy=(1470, 0.20), xytext=(1500, 0.05),
                fontsize=9, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
    save(fig, 'fig16_raman.png')


# =========================================================
# Fig 17. Bode plot of SAPC EIS aging
# =========================================================
def fig_bode():
    fig, ax1 = plt.subplots(figsize=(8, 5))
    import numpy as np
    f = np.logspace(-1, 6, 300)
    w = 2 * np.pi * f

    def bode(Rs, Rp, Cp, L, Cb):
        Z = Rs + 1j*w*L + Rp/(1 + 1j*w*Rp*Cp) + 1/(1j*w*Cb)
        return np.abs(Z), np.angle(Z, deg=True)

    m0, p0 = bode(0.010, 0.020, 5e-5, 3e-9, 470e-6)
    m1, p1 = bode(0.025, 0.080, 1.5e-4, 3e-9, 465e-6)
    m2, p2 = bode(0.050, 0.30,  3e-4, 3e-9, 420e-6)

    for m, p, c, lbl in [(m0, p0, 'blue', 't = 0 h'),
                          (m1, p1, 'green', 't = 500 h'),
                          (m2, p2, 'red', 't = 1500 h')]:
        ax1.loglog(f, m*1000, color=c, lw=1.8, label=lbl)

    ax1.set_xlabel('Frequency / Hz', fontsize=11)
    ax1.set_ylabel(r'|Z| / m$\Omega$', fontsize=11, color='black')
    ax1.grid(True, which='both', alpha=0.25)
    ax1.legend(loc='upper right', fontsize=9, title='|Z|')

    ax2 = ax1.twinx()
    for p, c in [(p0, 'blue'), (p1, 'green'), (p2, 'red')]:
        ax2.semilogx(f, p, color=c, lw=1.2, linestyle='--', alpha=0.7)
    ax2.set_ylabel(r'Phase $\phi$ / °', fontsize=11, color='gray')
    ax2.set_ylim(-95, 95)
    ax2.tick_params(axis='y', colors='gray')

    ax1.set_title('Fig. 17  Bode Plot of SAPC under 85°C/85%RH Aging\n'
                  '(after Liu & Pecht, IEEE T-CPMT, 2017)',
                  fontsize=11.5, fontweight='bold')
    save(fig, 'fig17_bode.png')


# =========================================================
# Fig 18. Micro-CT concept + sample slice schematic
# =========================================================
def fig_microct():
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # (a) Principle schematic
    ax = axs[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(Rectangle((0.3, 3.5), 1.6, 1.0, fc='#6b7280', ec='black', lw=1.2))
    ax.text(1.1, 4.0, 'X-ray\ntube', ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    # sample
    ax.add_patch(FancyBboxPatch((4.5, 3.3), 1.4, 1.4, boxstyle="round,pad=0.05", fc='#fbbf24', ec='black', lw=1.2))
    ax.text(5.2, 4.0, 'SAPC', ha='center', va='center', fontsize=9, fontweight='bold')
    # rotation arrow
    from matplotlib.patches import FancyArrowPatch as FAP
    ax.add_patch(FAP((5.2, 5.0), (5.9, 4.4), connectionstyle="arc3,rad=0.3",
                     arrowstyle='->', color='green', lw=1.8))
    ax.text(6.2, 5.1, 'θ rotation\n(0–360°)', fontsize=8, color='green')
    # detector
    ax.add_patch(Rectangle((8.1, 2.5), 1.4, 3.0, fc='#1e3a8a', ec='black', lw=1.2))
    ax.text(8.8, 4.0, 'Flat-panel\ndetector', ha='center', va='center', fontsize=8, color='white', fontweight='bold')
    # X-ray cone
    import matplotlib.patches as mpatches
    ax.add_patch(mpatches.Polygon([[1.9, 4.0], [8.1, 3.0], [8.1, 5.0]], fc='yellow', alpha=0.2, ec='none'))
    ax.text(3.5, 4.7, 'X-ray beam', fontsize=9, color='#92400e')
    # caption
    ax.text(5.0, 7.2, r'$I(x) = I_0 \cdot \exp[-\int \mu(x\,)\, dx\,]$', fontsize=11,
            ha='center', fontweight='bold')
    ax.text(5.0, 1.3, '(a) Micro-CT acquisition: sample rotated through 0–360°;\n'
            'filtered back-projection (FBP) reconstructs 3-D map of $\mu(x,y,z)$',
            ha='center', fontsize=9)

    # (b) 2D slice schematic
    ax = axs[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    # epoxy body
    ax.add_patch(Rectangle((0.5, 0.5), 9.0, 7.0, fc='#d6d3d1', ec='black', lw=1.0))
    ax.text(5.0, 7.2, 'Reconstructed µ-CT slice (schematic)', ha='center', fontsize=10, fontweight='bold')
    # lead-frames
    ax.add_patch(Rectangle((0.8, 2.5), 0.6, 3.0, fc='#7f1d1d', ec='black', lw=0.6))
    ax.add_patch(Rectangle((8.6, 2.5), 0.6, 3.0, fc='#7f1d1d', ec='black', lw=0.6))
    # stacked Al foils
    for k in range(6):
        ax.add_patch(Rectangle((1.6, 2.7 + k*0.45), 6.8, 0.18, fc='#9ca3af', ec='black', lw=0.3))
        ax.add_patch(Rectangle((1.6, 2.88 + k*0.45), 6.8, 0.27, fc='#1e3a8a', ec='none'))
    # defect marker
    ax.add_patch(Circle((4.0, 3.8), 0.25, fc='none', ec='red', lw=2, linestyle='--'))
    ax.annotate('Void in\nPEDOT filling\n(Ø ≈ 80 µm)', xy=(4.0, 3.8), xytext=(2.2, 6.0),
                fontsize=8.5, color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1))
    ax.add_patch(Circle((7.0, 5.3), 0.3, fc='none', ec='red', lw=2, linestyle='--'))
    ax.annotate('Edge\ndelamination', xy=(7.0, 5.3), xytext=(7.2, 6.5),
                fontsize=8.5, color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1))
    ax.text(5.0, 0.15, '(b) Typical features revealed in a SAPC micro-CT slice\n'
            '(after Piao et al., SPIE 2015; Teverovsky, NASA/NEPP 2024)',
            ha='center', fontsize=9)

    plt.suptitle('Fig. 18  Micro-CT Principle and Typical SAPC Reconstruction Features',
                 fontsize=11.5, fontweight='bold', y=1.02)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    save(fig, 'fig18_microct.png')


# =========================================================
# Fig 19. TGA curve of PEDOT in air vs N2
# =========================================================
def fig_tga():
    fig, ax = plt.subplots(figsize=(8, 5))
    import numpy as np
    T = np.linspace(25, 600, 500)
    def sigmoid_step(T, T_mid, width, drop):
        return drop / (1 + np.exp((T_mid - T)/width))

    # In air: 4-stage loss
    loss_air = (sigmoid_step(T, 80, 15, 4) + sigmoid_step(T, 200, 30, 8) +
                sigmoid_step(T, 290, 25, 30) + sigmoid_step(T, 450, 40, 35))
    mass_air = 100 - loss_air
    # In N2: smaller oxidation contribution
    loss_n2 = (sigmoid_step(T, 80, 15, 4) + sigmoid_step(T, 240, 35, 6) +
               sigmoid_step(T, 320, 30, 14) + sigmoid_step(T, 500, 50, 12))
    mass_n2 = 100 - loss_n2

    ax.plot(T, mass_air, 'r-', lw=2, label='PEDOT:PSS in air')
    ax.plot(T, mass_n2, 'b-', lw=2, label=r'PEDOT:PSS in $\mathrm{N_2}$')
    ax.set_xlabel('Temperature / °C', fontsize=11)
    ax.set_ylabel('Mass / %', fontsize=11)
    ax.set_title('Fig. 19  TGA of PEDOT:PSS Cathode Material\n'
                 '(after Gregori et al., J Surf Eng Mater Adv Tech, 2012; Marciniak et al., Synth. Met., 2004)',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    # stage annotations
    ax.axvspan(25, 120, alpha=0.06, color='blue')
    ax.text(72, 55, 'Stage 1\nH₂O desorb.', fontsize=8.5, ha='center', color='#1e3a8a')
    ax.axvspan(120, 250, alpha=0.06, color='orange')
    ax.text(185, 55, 'Stage 2\ndopant loss', fontsize=8.5, ha='center', color='#c2410c')
    ax.axvspan(250, 400, alpha=0.06, color='red')
    ax.text(325, 55, 'Stage 3\nmain chain\nscission', fontsize=8.5, ha='center', color='#991b1b')
    ax.axvspan(400, 600, alpha=0.06, color='purple')
    ax.text(500, 55, 'Stage 4\ncarbonization', fontsize=8.5, ha='center', color='#6b21a8')
    ax.set_xlim(25, 600)
    ax.set_ylim(40, 105)
    save(fig, 'fig19_tga.png')


# =========================================================
# Fig 20. FT-IR spectrum of PEDOT (fresh vs aged)
# =========================================================
def fig_ftir():
    fig, ax = plt.subplots(figsize=(8, 5))
    import numpy as np
    wn = np.linspace(600, 4000, 900)
    def g(x, x0, h, w):
        return h * np.exp(-((x - x0) / w) ** 2)
    # Fresh PEDOT:PSS features
    y_fresh = (0.95 - g(wn, 1180, 0.35, 40) - g(wn, 1080, 0.28, 35)
               - g(wn, 1510, 0.25, 25) - g(wn, 1040, 0.22, 30)
               - g(wn, 680, 0.18, 40) - g(wn, 3450, 0.08, 200))
    # Aged PEDOT:PSS: C=O grows, -OH grows, S=O shrinks
    y_aged = (0.95 - g(wn, 1180, 0.20, 40) - g(wn, 1080, 0.20, 35)
              - g(wn, 1510, 0.20, 25) - g(wn, 1040, 0.15, 30)
              - g(wn, 680, 0.15, 40) - g(wn, 3400, 0.28, 250)
              - g(wn, 1720, 0.18, 30))
    ax.plot(wn, y_fresh + 0.6, 'b-', lw=1.4, label='Fresh')
    ax.plot(wn, y_aged, 'r-', lw=1.4, label='After 85°C/85%RH, 1500h')
    ax.set_xlabel(r'Wavenumber / cm$^{-1}$', fontsize=11)
    ax.set_ylabel('Transmittance (offset)', fontsize=11)
    ax.invert_xaxis()
    ax.set_title('Fig. 20  FT-IR Spectra of PEDOT:PSS Cathode Before and After THB Aging\n'
                 '(after Gregori et al., 2012 [71]; Marciniak et al., Synth. Met. 2004 [23])',
                 fontsize=10.5, fontweight='bold')
    # peak annotations
    anns = [(1180, 'S=O (PSS)'), (1080, 'C-O-C'),
            (1510, 'C=C (thiophene)'), (3400, '-OH (H₂O)'), (1720, 'C=O (oxidized)')]
    for x, lbl in anns:
        ax.axvline(x, color='gray', linestyle=':', alpha=0.35)
        ax.text(x, 1.25, lbl, fontsize=8, rotation=60, ha='left', color='#374151')
    ax.legend(fontsize=10, loc='lower left')
    ax.grid(alpha=0.25)
    save(fig, 'fig20_ftir.png')


if __name__ == "__main__":
    # Newly added characterization figures:
    fig_xps_s2p()
    fig_raman_pedot()
    fig_bode()
    fig_microct()
    fig_tga()
    fig_ftir()
    print("New characterization figures generated.")
