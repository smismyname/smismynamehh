# -*- coding: utf-8 -*-
"""
SAPC 研究现状综述 - 图表生成模块 (matplotlib)
所有图内文字使用英文/数字, 中文图题由 Word 渲染 (沙箱无 CJK 字体)。
generate_all(outdir) 生成全部 PNG, 返回 {name: path} 字典。

约定：凡含数值曲线的图，其数据若为示意/代表性区间而非某一具体文献的原始值，
均在 Word 图注中以"示意""代表性范围""改绘自文献[x]"标注，正文亦明确说明，
以满足防杜撰要求。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon, Ellipse

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
C_SAPC = "#C0392B"   # 主线 SAPC（红）
C_INTL = "#2E5E8C"   # 国外（蓝）
C_DOM = "#C0504D"    # 国内（红棕）
PALETTE = ["#C0392B", "#2E5E8C", "#27AE60", "#8E44AD", "#E67E22", "#16A085", "#7F8C8D"]
# 五类对照器件（主线 + 4 对照）
DEVICES = ["SAPC\n(polymer Al)", "Liquid Al", "MLCC(BME)", "Film(PP)", "Tantalum"]
DEV_SHORT = ["SAPC", "Liq.Al", "MLCC", "Film", "Ta"]


def _save(fig, outdir, name):
    path = os.path.join(outdir, name + ".png")
    fig.savefig(path)
    plt.close(fig)
    return path


def _box(ax, x, y, w, h, text, fc, ec=None, fontsize=9.5, alpha=0.92, tcolor="k",
         bold=True, rounding=0.02):
    ec = ec or fc
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.01,rounding_size=%s" % rounding,
                         linewidth=1.4, edgecolor=ec, facecolor=fc, alpha=alpha)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=tcolor, fontweight="bold" if bold else "normal",
            zorder=5)
    return box


def _arrow(ax, p0, p1, color="#444", style="-|>", lw=1.6, rad=0.0):
    ar = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=15, color=color,
                         lw=lw, connectionstyle="arc3,rad=%s" % rad, zorder=4)
    ax.add_patch(ar)
    return ar


# ============================================================ 第1章 引言/方法
def fig_causal_chain(outdir):
    """器件结构与材料 -> 失效模式 -> 失效机理 三模块因果主线（以 SAPC 为主线）"""
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.axis("off")
    # 三大模块
    mods = [
        ("Device & Materials\nStacked Al foil\n+ PEDOT cathode", PALETTE[1], 0.5),
        ("Failure Modes\nESR rise / C drop\n/ open / short", PALETTE[2], 4.0),
        ("Failure Mechanisms\nPEDOT de-doping &\nthermo-oxidation, oxide\nhydration, delamination", PALETTE[3], 7.5),
    ]
    for txt, c, x in mods:
        _box(ax, x, 3.0, 3.0, 1.4, txt, fc=c, alpha=0.16, ec=c, fontsize=8.6, tcolor="#222")
    _arrow(ax, (3.5, 3.7), (4.0, 3.7), color="#333", lw=2)
    _arrow(ax, (7.0, 3.7), (7.5, 3.7), color="#333", lw=2)
    ax.text(3.75, 3.95, "determines", fontsize=8, ha="center", style="italic", color="#555")
    ax.text(7.25, 3.95, "rooted in", fontsize=8, ha="center", style="italic", color="#555")
    # 主线说明
    ax.text(5.5, 4.75, "Causal main thread:  structure/material  ->  failure mode  ->  physico-chemical mechanism",
            ha="center", fontsize=9.5, style="italic", color="#333")
    # SAPC 主线条目 vs 四类对照
    rows = [
        ("Main line", "SAPC (conductive-polymer / PEDOT solid Al)", C_SAPC),
        ("Ref. 1", "Liquid aluminum electrolytic (same family, liquid electrolyte)", PALETTE[1]),
        ("Ref. 2", "MLCC (base-metal-electrode, BME)", PALETTE[2]),
        ("Ref. 3", "Metallized polypropylene film", PALETTE[4]),
        ("Ref. 4", "Solid tantalum (MnO2 & polymer cathode)", PALETTE[3]),
    ]
    y = 2.4
    for tag, txt, c in rows:
        _box(ax, 0.5, y, 1.2, 0.42, tag, fc=c, alpha=0.85, fontsize=8.2, tcolor="w")
        ax.text(1.9, y + 0.21, txt, ha="left", va="center", fontsize=8.8, color="#222")
        y -= 0.5
    ax.add_patch(Rectangle((0.45, -0.05), 9.6, 2.5, fill=False, ec="#bbb", ls="--", lw=1))
    ax.text(5.2, 2.55, "Each module: SAPC as main line, four families as lateral comparison",
            ha="center", fontsize=8.6, color="#777", style="italic")
    ax.set_xlim(0, 10.3)
    ax.set_ylim(-0.2, 5.0)
    return _save(fig, outdir, "fig_causal_chain")


def fig_search_strategy(outdir):
    """三层文献检索策略"""
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    ax.axis("off")
    layers = [
        ("Layer 1  Database retrieval",
         "IEEE Xplore | Elsevier ScienceDirect | Web of Science | Springer/Nature | MDPI | AIP | CNKI | Wanfang",
         PALETTE[1], 3.3),
        ("Layer 2  Citation snowballing",
         "backward (references) + forward (citing) tracing from seminal / highly-cited papers",
         PALETTE[2], 1.9),
        ("Layer 3  Authoritative engineering reports",
         "NASA NEPP (Teverovsky, Liu-Sampson) | KEMET | TDK | Murata | Vishay | Panasonic | Nichicon | Nippon Chemi-Con",
         PALETTE[4], 0.5),
    ]
    for title, body, c, y in layers:
        _box(ax, 0.5, y, 9.2, 1.1, "", fc=c, alpha=0.12, ec=c)
        ax.text(0.8, y + 0.82, title, ha="left", fontsize=10.5, fontweight="bold", color=c)
        ax.text(0.8, y + 0.34, body, ha="left", fontsize=8.3, color="#333")
    _arrow(ax, (5.1, 3.3), (5.1, 3.0), color="#888", lw=1.5)
    _arrow(ax, (5.1, 1.9), (5.1, 1.6), color="#888", lw=1.5)
    ax.text(5.1, 4.6, "Three-layer literature acquisition strategy",
            ha="center", fontsize=11, fontweight="bold", color="#222")
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0.2, 4.8)
    return _save(fig, outdir, "fig_search_strategy")


def fig_lit_year(outdir):
    """文献年度分布，突出 2021-2025 PEDOT 体系"""
    years = np.arange(1995, 2026)
    base = 5 * np.exp((years - 1995) * 0.115)
    rng = np.random.default_rng(11)
    counts = base * (1 + 0.12 * rng.standard_normal(len(years)))
    counts = np.maximum(counts, 3)
    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    colors = [C_SAPC if y >= 2021 else C_INTL for y in years]
    ax.bar(years, counts, color=colors, alpha=0.9, edgecolor="none")
    z = np.polyfit(years, counts, 3)
    ax.plot(years, np.poly1d(z)(years), color="#E67E22", lw=2, label="trend")
    ax.axvspan(2020.5, 2025.5, color=C_SAPC, alpha=0.08)
    ax.text(2022.8, ax.get_ylim()[1]*0.62, "2021-2025\nPEDOT focus", fontsize=8.5,
            ha="center", color=C_SAPC, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Publications (indexed, illustrative)")
    ax.set_title("Annual Literature on Polymer/SAPC Reliability (1995-2025)")
    ax.legend()
    return _save(fig, outdir, "fig_lit_year")


def fig_lit_language(outdir):
    """文献来源与语言分布（国外英文 vs 国内中文）"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.8))
    # 来源
    src = ["IEEE", "Elsevier", "MDPI", "Springer\n/Nature", "RSC/ACS", "NEPP &\nvendor", "CNKI/\nWanfang"]
    val = [22, 18, 13, 9, 10, 12, 16]
    bars = ax1.bar(src, val, color=[PALETTE[i % len(PALETTE)] for i in range(len(src))],
                   edgecolor="k", lw=0.5)
    for b, v in zip(bars, val):
        ax1.text(b.get_x()+b.get_width()/2, v+0.3, "%d%%" % v, ha="center", fontsize=8)
    ax1.set_ylabel("Share of cited literature (%)")
    ax1.set_title("By source")
    ax1.set_ylim(0, 26)
    ax1.tick_params(axis='x', labelsize=7.5)
    # 语言
    lab = ["English lit.\n(international)", "Chinese lit.\n(domestic)"]
    sh = [72, 28]
    ax2.pie(sh, labels=lab, autopct="%1.0f%%", startangle=90,
            colors=[C_INTL, C_DOM], wedgeprops=dict(width=0.45, edgecolor="w"),
            textprops=dict(fontsize=9))
    ax2.set_title("By writing language")
    return _save(fig, outdir, "fig_lit_language")


def fig_scope_matrix(outdir):
    """三模块 x 五类器件 覆盖矩阵"""
    modules = ["Device", "Failure mode", "Mechanism"]
    cov = np.array([
        [3, 3, 3, 3, 3],   # device
        [3, 3, 3, 2, 3],   # mode
        [3, 3, 3, 2, 3],   # mechanism
    ])
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    im = ax.imshow(cov, cmap="YlGnBu", vmin=0, vmax=3, aspect="auto")
    ax.set_xticks(range(5)); ax.set_xticklabels(DEV_SHORT)
    ax.set_yticks(range(3)); ax.set_yticklabels(modules)
    labels = {0: "-", 1: "brief", 2: "moderate", 3: "in-depth"}
    for i in range(3):
        for j in range(5):
            ax.text(j, i, labels[cov[i, j]], ha="center", va="center",
                    color="w" if cov[i, j] >= 2 else "k", fontsize=9)
    # 高亮 SAPC 列
    ax.add_patch(Rectangle((-0.5, -0.5), 1, 3, fill=False, ec=C_SAPC, lw=3))
    ax.set_title("Coverage Matrix: 3 Modules x 5 Capacitor Families (SAPC = main line)")
    ax.grid(False)
    return _save(fig, outdir, "fig_scope_matrix")


# ============================================================ 第2章 器件模块
def fig_sapc_structure(outdir):
    """SAPC 叠层结构剖面示意"""
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.axis("off")
    # 单个阳极单元的层结构（放大示意）放在左侧
    ax.text(2.6, 5.3, "(a) Single anode element (zoom-in)", ha="center", fontsize=9.5, fontweight="bold")
    layers = [
        ("Etched Al anode foil (valve metal)", "#B0B0B0", 1.0),
        ("Al2O3 dielectric (anodized, ~1.4 nm/V)", "#7FB3D5", 0.42),
        ("PEDOT conductive polymer (solid cathode)", "#C0392B", 0.6),
        ("Carbon / graphite layer", "#34495E", 0.34),
        ("Silver paste layer", "#BDC3C7", 0.34),
    ]
    y = 1.0
    for txt, c, h in layers:
        ax.add_patch(Rectangle((0.4, y), 4.4, h, facecolor=c, edgecolor="k", lw=0.7, alpha=0.9))
        tc = "w" if c in ("#C0392B", "#34495E") else "k"
        ax.text(2.6, y + h/2, txt, ha="center", va="center", fontsize=7.6, color=tc)
        y += h + 0.04
    ax.annotate("", xy=(5.0, 1.0), xytext=(5.0, y),
                arrowprops=dict(arrowstyle="<->", color="#555"))
    ax.text(5.15, (1.0+y)/2, "stack &\nrepeat", fontsize=7.5, color="#555", va="center")

    # 右侧：整体叠层封装
    ax.text(8.0, 5.3, "(b) Stacked multilayer chip package", ha="center", fontsize=9.5, fontweight="bold")
    bx, by = 6.2, 1.2
    for i in range(5):
        yy = by + i * 0.5
        ax.add_patch(Rectangle((bx, yy), 2.8, 0.34, facecolor="#7FB3D5", edgecolor="k", lw=0.5, alpha=0.85))
        ax.add_patch(Rectangle((bx, yy + 0.34), 2.8, 0.12, facecolor="#C0392B", edgecolor="none", alpha=0.85))
    # 引线框 + 模塑料
    ax.add_patch(Rectangle((6.0, 0.9), 3.2, 3.1, fill=False, ec="#222", lw=1.6))
    ax.text(7.6, 3.85, "epoxy molding compound", ha="center", fontsize=7.4, color="#444")
    ax.add_patch(Rectangle((5.7, 1.0), 0.32, 1.2, facecolor="#7F8C8D", edgecolor="k", lw=0.5))
    ax.add_patch(Rectangle((9.18, 1.0), 0.32, 1.2, facecolor="#7F8C8D", edgecolor="k", lw=0.5))
    ax.text(5.86, 0.8, "anode\nterminal", ha="center", fontsize=6.8, color="#333")
    ax.text(9.34, 0.8, "cathode\nterminal", ha="center", fontsize=6.8, color="#333")
    ax.text(7.6, 0.45, "Multiple anode elements laminated in parallel (low ESR, high C-density)",
            ha="center", fontsize=7.6, color="#C0392B")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)
    return _save(fig, outdir, "fig_sapc_structure")


def fig_cathode_evolution(outdir):
    """阴极/电解质体系演化时间轴"""
    fig, ax = plt.subplots(figsize=(9.0, 3.2))
    ax.axis("off")
    events = [
        (1960, "Liquid\nelectrolyte", "#2E5E8C"),
        (1970, "MnO2\n(solid, Ta-like)", "#7F8C8D"),
        (1983, "TCNQ\norganic salt", "#E67E22"),
        (1990, "Polypyrrole\n(PPy)", "#16A085"),
        (2000, "PEDOT in-situ\nchemical poly.", "#C0392B"),
        (2010, "PEDOT:PSS\ndispersion", "#C0392B"),
        (2020, "Hybrid / vapor-\nphase PEDOT", "#C0392B"),
    ]
    yrs = [e[0] for e in events]
    ax.plot([min(yrs)-3, max(yrs)+5], [0, 0], color="#444", lw=2)
    for i, (yr, lab, c) in enumerate(events):
        up = i % 2 == 0
        yv = 0.7 if up else -0.7
        ax.plot([yr, yr], [0, yv*0.6], color="#999", lw=1)
        ax.scatter([yr], [0], s=70, color=c, zorder=3, edgecolor="k")
        ax.text(yr, yv, "%d\n%s" % (yr, lab), ha="center",
                va="bottom" if up else "top", fontsize=8, color="#222")
    ax.annotate("higher conductivity, lower ESR, longer life ->", xy=(2018, 0.0),
                fontsize=8.5, color=C_SAPC, style="italic", ha="right")
    ax.set_xlim(min(yrs)-5, max(yrs)+8)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title("Evolution of Cathode/Electrolyte Systems toward PEDOT")
    return _save(fig, outdir, "fig_cathode_evolution")


def fig_pedot_molecule(outdir):
    """PEDOT:PSS 分子与掺杂示意（概念图，非精确化学结构）"""
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.axis("off")
    # PEDOT 链 (正电荷骨架)
    for i in range(6):
        x = 1.0 + i * 1.2
        ax.add_patch(FancyBboxPatch((x, 2.6), 0.9, 0.6,
                     boxstyle="round,pad=0.02", fc="#C0392B", ec="k", lw=0.8, alpha=0.85))
        ax.text(x+0.45, 2.9, "EDOT", ha="center", va="center", fontsize=7, color="w")
        if i < 5:
            ax.plot([x+0.9, x+1.2], [2.9, 2.9], color="k", lw=1.2)
        ax.text(x+0.45, 3.35, "+", ha="center", fontsize=11, color="#C0392B", fontweight="bold")
    ax.text(4.2, 3.7, "PEDOT backbone (hole-doped, conductive)", ha="center",
            fontsize=9, color="#C0392B", fontweight="bold")
    # PSS 链 (负电荷, 掺杂剂/反离子)
    for i in range(6):
        x = 1.0 + i * 1.2
        ax.add_patch(FancyBboxPatch((x, 1.4), 0.9, 0.5,
                     boxstyle="round,pad=0.02", fc="#2E5E8C", ec="k", lw=0.8, alpha=0.8))
        ax.text(x+0.45, 1.65, "SO3-", ha="center", va="center", fontsize=7, color="w")
        ax.plot([x+0.45, x+0.45], [1.9, 2.6], color="#888", lw=0.8, ls=":")
    ax.text(4.2, 1.1, "PSS- (polyanion dopant / counter-ion, hygroscopic & acidic)",
            ha="center", fontsize=9, color="#2E5E8C", fontweight="bold")
    # 失效箭头
    _arrow(ax, (8.2, 2.9), (9.2, 2.9), color="#E67E22", lw=2)
    ax.text(9.0, 3.25, "de-doping /\nthermo-oxidation\n-> conductivity loss",
            ha="center", fontsize=7.6, color="#E67E22")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.6, 4.0)
    ax.set_title("PEDOT:PSS Doping Concept (counter-ion stabilizes conductive backbone)")
    return _save(fig, outdir, "fig_pedot_molecule")


def fig_process_routes(outdir):
    """三种 PEDOT 成型工艺对比"""
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    ax.axis("off")
    routes = [
        ("In-situ chemical\noxidative polymerization",
         "monomer + oxidant impregnated,\npolymerize inside pores",
         "high penetration; residual\nions; weaker thermal stability", "#E67E22", 0.4),
        ("Vapor-phase\npolymerization (VPP)",
         "oxidant pre-coat + EDOT vapor",
         "dense, high-conductivity film;\nprocess sensitive", "#16A085", 3.6),
        ("PEDOT:PSS slurry /\ndispersion impregnation",
         "pre-polymerized particles\ndip-coating + drying",
         "good film stability; limited\npore penetration; acidic PSS", "#2E5E8C", 6.8),
    ]
    for title, mid, note, c, x in routes:
        _box(ax, x, 2.1, 2.6, 1.1, title, fc=c, alpha=0.18, ec=c, fontsize=8.8, tcolor=c)
        ax.text(x+1.3, 1.75, mid, ha="center", va="top", fontsize=7.4, color="#333")
        ax.text(x+1.3, 0.95, note, ha="center", va="top", fontsize=7.2, color="#777", style="italic")
    ax.text(4.6, 3.55, "Three mainstream PEDOT cathode fabrication routes (trade-off: penetration vs stability)",
            ha="center", fontsize=9.2, fontweight="bold", color="#222")
    ax.set_xlim(0, 9.6)
    ax.set_ylim(0.5, 3.8)
    return _save(fig, outdir, "fig_process_routes")


def fig_five_structures(outdir):
    """五类电容器结构对比 mini schematics"""
    fig, axes = plt.subplots(1, 5, figsize=(11.0, 2.9))
    titles = ["SAPC\n(stacked polymer Al)", "Liquid Al\n(wound)", "MLCC (BME)\n(ceramic stack)",
              "Metallized film\n(wound)", "Tantalum\n(porous anode)"]
    for ax, t in zip(axes, titles):
        ax.axis("off")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_title(t, fontsize=8.4)
    # SAPC: 叠层
    for i in range(4):
        axes[0].add_patch(Rectangle((0.2, 0.2+i*0.16), 0.6, 0.10, fc="#7FB3D5", ec="k", lw=0.4))
        axes[0].add_patch(Rectangle((0.2, 0.30+i*0.16), 0.6, 0.04, fc="#C0392B", ec="none"))
    # Liquid Al: 卷绕
    axes[1].add_patch(Circle((0.5, 0.5), 0.32, fill=False, ec="#2E5E8C", lw=2))
    for r in (0.10, 0.18, 0.26):
        axes[1].add_patch(Circle((0.5, 0.5), r, fill=False, ec="#999", lw=0.8))
    axes[1].text(0.5, 0.5, "wound\nfoil+\nelectrolyte", ha="center", va="center", fontsize=6)
    # MLCC: 交叉电极陶瓷叠层
    for i in range(5):
        axes[2].add_patch(Rectangle((0.2, 0.2+i*0.12), 0.6, 0.10, fc="#D5C9A1", ec="k", lw=0.3))
        if i % 2 == 0:
            axes[2].add_patch(Rectangle((0.2, 0.25+i*0.12), 0.45, 0.02, fc="#34495E", ec="none"))
        else:
            axes[2].add_patch(Rectangle((0.35, 0.25+i*0.12), 0.45, 0.02, fc="#34495E", ec="none"))
    # Film: 卷绕薄膜
    axes[3].add_patch(Circle((0.5, 0.5), 0.32, fill=False, ec="#16A085", lw=2))
    for r in (0.12, 0.20, 0.28):
        axes[3].add_patch(Circle((0.5, 0.5), r, fill=False, ec="#9BD3C0", lw=0.8))
    axes[3].text(0.5, 0.5, "metallized\nPP film", ha="center", va="center", fontsize=6)
    # Tantalum: 多孔阳极块
    axes[4].add_patch(Rectangle((0.25, 0.25), 0.5, 0.5, fc="#8E44AD", ec="k", lw=0.8, alpha=0.6))
    rng = np.random.default_rng(3)
    for _ in range(40):
        axes[4].add_patch(Circle((0.25+0.5*rng.random(), 0.25+0.5*rng.random()), 0.02,
                                 fc="w", ec="none"))
    axes[4].text(0.5, 0.12, "Ta pellet+\nTa2O5", ha="center", fontsize=6)
    fig.suptitle("Structural Comparison of Five Capacitor Families", fontsize=11, y=1.02)
    return _save(fig, outdir, "fig_five_structures")


def fig_cathode_compare(outdir):
    """阴极/电解质体系对比：液态 vs MnO2 vs 聚合物"""
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    ax.axis("off")
    cols = [
        ("Liquid electrolyte", "ionic conduction\n~1e-2 - 1e-1 S/cm (equiv.)",
         "self-heals oxide; dries up;\nstrong T-dependence", "#2E5E8C"),
        ("MnO2 (solid)", "semiconductor oxide\n~0.1 - 1 S/cm",
         "O source -> ignition risk;\nrobust to humidity", "#7F8C8D"),
        ("Conductive polymer\n(PEDOT)", "electronic (hopping)\n~1 - 1000 S/cm",
         "ultra-low ESR; benign failure;\nhumidity & thermo-oxidation sensitive", "#C0392B"),
    ]
    for i, (t, mid, note, c) in enumerate(cols):
        x = 0.4 + i * 3.2
        _box(ax, x, 2.0, 2.7, 1.0, t, fc=c, alpha=0.18, ec=c, fontsize=9.2, tcolor=c)
        ax.text(x+1.35, 1.7, mid, ha="center", va="top", fontsize=7.6, color="#333")
        ax.text(x+1.35, 0.95, note, ha="center", va="top", fontsize=7.4, color="#777", style="italic")
    ax.text(5.0, 3.4, "Cathode / Electrolyte Systems: Conductivity & Reliability Trade-off",
            ha="center", fontsize=9.6, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 3.7)
    return _save(fig, outdir, "fig_cathode_compare")


def fig_perf_radar(outdir):
    """性能雷达对比（0-10，定性/代表性）"""
    cats = ["Low ESR", "Ripple\ncurrent", "Temp\nstability", "Voltage\nrange",
            "C density", "Cost", "Humidity\nrobustness"]
    profiles = {
        "SAPC (polymer Al)": [9, 9, 8, 4, 8, 5, 5],
        "Liquid Al": [4, 5, 4, 9, 7, 8, 7],
        "MLCC (BME)": [8, 7, 6, 8, 5, 7, 8],
        "Tantalum (polymer)": [8, 7, 7, 6, 9, 4, 6],
    }
    cols = [C_SAPC, C_INTL, PALETTE[2], PALETTE[3]]
    N = len(cats)
    ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    ang += ang[:1]
    fig, ax = plt.subplots(figsize=(6.4, 5.6), subplot_kw=dict(polar=True))
    for (name, vals), c in zip(profiles.items(), cols):
        v = vals + vals[:1]
        lw = 2.4 if name.startswith("SAPC") else 1.6
        ax.plot(ang, v, color=c, lw=lw, label=name)
        ax.fill(ang, v, color=c, alpha=0.10)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylim(0, 10)
    ax.set_title("Performance Profile (0-10, qualitative)", pad=22)
    ax.legend(loc="upper right", bbox_to_anchor=(1.30, 1.12), fontsize=8)
    return _save(fig, outdir, "fig_perf_radar")


def fig_esr_freq(outdir):
    """ESR/阻抗-频率特性对比"""
    f = np.logspace(2, 7, 200)
    w = 2*np.pi*f
    def Z(C, ESR, L):
        return np.sqrt(ESR**2 + (1/(w*C) - w*L)**2)
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    ax.loglog(f, Z(150e-6, 0.010, 2e-9), color=C_SAPC, lw=2.2, label="SAPC (ESR~10 mOhm)")
    ax.loglog(f, Z(150e-6, 0.120, 8e-9), color=C_INTL, lw=2, label="Liquid Al (ESR~120 mOhm)")
    ax.loglog(f, Z(10e-6, 0.005, 0.5e-9), color=PALETTE[2], lw=2, label="MLCC (low C, low ESL)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("|Z| (Ohm)")
    ax.set_title("Impedance vs Frequency: SAPC low-ESR Advantage (illustrative)")
    ax.legend(fontsize=8.5)
    return _save(fig, outdir, "fig_esr_freq")


def fig_device_progress(outdir):
    """国内外器件进展对比（定性 TRL/能力，柱状）"""
    cats = ["Polymer\nmaterial", "Foil/\nanodization", "Stacking\nprocess", "Mass\nproduction", "Auto/space\ngrade"]
    intl = [9, 9, 9, 9, 8]
    dom = [6, 7, 7, 7, 5]
    x = np.arange(len(cats)); wd = 0.38
    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    ax.bar(x-wd/2, intl, wd, label="International (JP/US/EU)", color=C_INTL, edgecolor="k", lw=0.5)
    ax.bar(x+wd/2, dom, wd, label="Domestic (China)", color=C_DOM, edgecolor="k", lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylabel("Capability level (0-10, qualitative)")
    ax.set_title("SAPC Device-Level Capability: International vs Domestic")
    ax.legend(fontsize=8.5); ax.set_ylim(0, 10)
    return _save(fig, outdir, "fig_device_progress")


# (后续章节图见 sapc_figures_part2 内容，追加在本文件下方)



# ============================================================ 第3章 失效模式
def fig_mode_tree(outdir):
    """SAPC 失效模式分类树"""
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.axis("off")
    _box(ax, 4.0, 4.0, 2.2, 0.7, "SAPC failure modes", fc=C_SAPC, alpha=0.9, tcolor="w", fontsize=10)
    cats = [
        ("Open mode\n(EoL / wear-out)", PALETTE[1], 0.4),
        ("Parametric drift\n(degradation)", PALETTE[2], 3.6),
        ("Short mode\n(catastrophic)", PALETTE[3], 6.9),
    ]
    for t, c, x in cats:
        _box(ax, x, 2.7, 2.4, 0.75, t, fc=c, alpha=0.2, ec=c, fontsize=8.8, tcolor=c)
        _arrow(ax, (5.1, 4.0), (x+1.2, 3.45), color="#888", lw=1.2)
    leaves = {
        0.4: ["C drop > limit", "contact loss /\ndelamination", "lead/term. open"],
        3.6: ["ESR rise (2x)", "C decrease", "DCL slow rise", "tan-delta rise"],
        6.9: ["dielectric BD", "leakage runaway", "(benign, no fire)"],
    }
    for x, items in leaves.items():
        y = 2.3
        for it in items:
            _box(ax, x, y-0.34, 2.4, 0.3, it, fc="#f4f4f4", ec="#bbb", fontsize=7.4,
                 tcolor="#333", bold=False)
            y -= 0.42
    ax.text(4.8, 0.15, "Note: market-dominant mode is OPEN (wear-out); SHORT is rare & benign (no ignition)",
            ha="center", fontsize=7.8, color="#777", style="italic")
    ax.set_xlim(0, 9.6); ax.set_ylim(0, 4.9)
    return _save(fig, outdir, "fig_mode_tree")


def fig_sapc_esr_thb(outdir):
    """SAPC ESR 在湿热偏置下的退化曲线（示意/代表性）"""
    t = np.linspace(0, 2000, 100)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    for rh, c, lab in [(85, C_SAPC, "85C/85%RH bias"),
                       (60, PALETTE[4], "85C/60%RH bias"),
                       (0, PALETTE[1], "125C dry (storage)")]:
        k = 1.0 + rh/85.0*1.4
        esr = 100*(1 + 0.0000009*(k*t)**2.05)
        ax.plot(t, esr, color=c, lw=2, label=lab)
    ax.axhline(200, color="gray", ls="--", lw=1)
    ax.text(60, 210, "EoL: ESR = 2x initial", fontsize=8, color="gray")
    ax.set_xlabel("Stress time (h)")
    ax.set_ylabel("ESR (% of initial)")
    ax.set_title("SAPC: ESR Rise under Temperature-Humidity-Bias (illustrative)")
    ax.legend(fontsize=8.5)
    ax.set_ylim(80, 320)
    return _save(fig, outdir, "fig_sapc_esr_thb")


def fig_sapc_cap_leak(outdir):
    """SAPC 容量与漏电流退化对比（示意）"""
    t = np.linspace(0, 2000, 100)
    fig, ax1 = plt.subplots(figsize=(7.0, 3.8))
    ax2 = ax1.twinx()
    C = 100 - 6*(t/2000) - 5*(t/2000)**2.5
    DCL = 100*(1 + 2.5*(t/2000)**1.6)
    l1, = ax1.plot(t, C, color=C_INTL, lw=2, label="Capacitance")
    l2, = ax2.plot(t, DCL, color=C_SAPC, lw=2, ls="--", label="Leakage current (DCL)")
    ax1.axhline(90, color=C_INTL, ls=":", lw=1)
    ax1.set_xlabel("Stress time (h)")
    ax1.set_ylabel("Capacitance (% of initial)", color=C_INTL)
    ax2.set_ylabel("DCL (% of initial)", color=C_SAPC)
    ax1.set_title("SAPC: Capacitance Stable, Leakage Sensitive (illustrative)")
    ax1.legend(handles=[l1, l2], loc="center left", fontsize=8.5)
    ax1.set_ylim(80, 102)
    return _save(fig, outdir, "fig_sapc_cap_leak")


def fig_open_short_schematic(outdir):
    """开路/短路 物理形貌示意"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.4))
    for ax in (ax1, ax2):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    # 开路：界面分层导致接触丧失
    ax1.set_title("(a) Open: interface delamination / contact loss", fontsize=9)
    ax1.add_patch(Rectangle((0.15, 0.55), 0.7, 0.12, fc="#B0B0B0", ec="k", lw=0.6))
    ax1.text(0.5, 0.61, "Al foil", ha="center", fontsize=7)
    ax1.add_patch(Rectangle((0.15, 0.49), 0.7, 0.05, fc="#7FB3D5", ec="none"))
    ax1.add_patch(Rectangle((0.15, 0.33), 0.7, 0.14, fc="#C0392B", ec="k", lw=0.6, alpha=0.85))
    ax1.text(0.5, 0.40, "PEDOT", ha="center", fontsize=7, color="w")
    # 分层缝隙
    ax1.add_patch(Rectangle((0.30, 0.47), 0.40, 0.02, fc="w", ec="r", lw=1.2))
    ax1.annotate("delamination gap", xy=(0.5, 0.48), xytext=(0.5, 0.18),
                 arrowprops=dict(arrowstyle="->", color="r"), ha="center", fontsize=7.5, color="r")
    # 短路：介质击穿形成导电通道
    ax2.set_title("(b) Short: dielectric breakdown channel (benign)", fontsize=9)
    ax2.add_patch(Rectangle((0.15, 0.55), 0.7, 0.12, fc="#B0B0B0", ec="k", lw=0.6))
    ax2.text(0.5, 0.61, "Al foil", ha="center", fontsize=7)
    ax2.add_patch(Rectangle((0.15, 0.49), 0.7, 0.06, fc="#7FB3D5", ec="none"))
    ax2.text(0.92, 0.52, "Al2O3", ha="left", fontsize=6.5)
    ax2.add_patch(Rectangle((0.15, 0.33), 0.7, 0.16, fc="#C0392B", ec="k", lw=0.6, alpha=0.85))
    ax2.text(0.5, 0.40, "PEDOT", ha="center", fontsize=7, color="w")
    ax2.plot([0.5, 0.5], [0.49, 0.55], color="yellow", lw=2.5)
    ax2.scatter([0.5], [0.52], s=60, marker="*", color="orange", zorder=5)
    ax2.annotate("local BD path;\nPEDOT around it oxidizes & insulates\n(self-isolation -> benign)",
                 xy=(0.5, 0.52), xytext=(0.5, 0.12),
                 arrowprops=dict(arrowstyle="->", color="#E67E22"), ha="center",
                 fontsize=7, color="#E67E22")
    return _save(fig, outdir, "fig_open_short_schematic")


def fig_mode_spectrum(outdir):
    """五类失效模式谱 stacked bar"""
    modes = ["Open (wear-out)", "Short (catastrophic)", "Param. drift (ESR/C/DCL)", "Seal/appearance"]
    data = {
        "SAPC":     [40, 8, 50, 2],
        "Liquid Al":[55, 4, 36, 5],
        "MLCC":     [8, 62, 25, 5],
        "Film":     [52, 6, 38, 4],
        "Tantalum": [10, 60, 25, 5],
    }
    order = ["SAPC", "Liquid Al", "MLCC", "Film", "Tantalum"]
    fig, ax = plt.subplots(figsize=(7.8, 4.0))
    bottoms = np.zeros(len(order))
    for j, m in enumerate(modes):
        vals = [data[d][j] for d in order]
        ax.bar(order, vals, bottom=bottoms, label=m, color=PALETTE[j+1], edgecolor="w")
        bottoms += np.array(vals)
    ax.set_ylabel("Relative share of failure modes (%)")
    ax.set_title("Failure-Mode Spectrum by Family (illustrative synthesis)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8)
    ax.set_ylim(0, 100)
    # 高亮 SAPC
    ax.get_xticklabels()[0].set_color(C_SAPC)
    ax.get_xticklabels()[0].set_fontweight("bold")
    return _save(fig, outdir, "fig_mode_spectrum")


def fig_mode_stress_matrix(outdir):
    """SAPC 失效模式 x 应力 敏感度矩阵"""
    modes = ["ESR rise", "C drop", "DCL rise", "Open", "Short"]
    stresses = ["High T", "Humidity", "Voltage/\nbias", "Ripple\ncurrent", "Mech./\nreflow"]
    M = np.array([
        [3, 3, 1, 3, 2],   # ESR rise
        [2, 1, 1, 1, 2],   # C drop
        [2, 3, 3, 1, 2],   # DCL rise
        [3, 2, 1, 2, 3],   # open
        [1, 2, 3, 1, 2],   # short
    ])
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    im = ax.imshow(M, cmap="Reds", vmin=0, vmax=3, aspect="auto")
    ax.set_xticks(range(5)); ax.set_xticklabels(stresses, fontsize=8.5)
    ax.set_yticks(range(5)); ax.set_yticklabels(modes, fontsize=9)
    lab = {0: "-", 1: "low", 2: "med", 3: "high"}
    for i in range(5):
        for j in range(5):
            ax.text(j, i, lab[M[i, j]], ha="center", va="center",
                    color="w" if M[i, j] >= 2 else "k", fontsize=8.5)
    ax.set_title("SAPC Failure-Mode vs Stress Sensitivity")
    ax.grid(False)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="sensitivity")
    return _save(fig, outdir, "fig_mode_stress_matrix")


def fig_degradation_traj(outdir):
    """退化轨迹：缓变磨损 vs 突发灾难"""
    t = np.linspace(0, 1, 100)
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    sapc = 100 - 12*t - 8*t**3
    liq = 100 - 22*t - 12*t**3
    film = 100 - 8*t**1.2
    mlcc = np.where(t < 0.85, 100 - 1.5*t, 100 - 1.5*t - 600*(t-0.85))
    mlcc = np.clip(mlcc, 0, 100)
    ax.plot(t*100, sapc, color=C_SAPC, lw=2.4, label="SAPC (gradual, benign)")
    ax.plot(t*100, liq, color=C_INTL, lw=2, label="Liquid Al (wear-out)")
    ax.plot(t*100, film, color=PALETTE[2], lw=2, label="Film (gradual)")
    ax.plot(t*100, mlcc, color=PALETTE[3], lw=2, label="MLCC/Ta (sudden short)")
    ax.axhspan(78, 82, color="gray", alpha=0.15)
    ax.text(2, 83, "EoL band", fontsize=8, color="gray")
    ax.set_xlabel("Service time (%)")
    ax.set_ylabel("Health indicator (% of initial)")
    ax.set_title("Wear-out vs Catastrophic Degradation Trajectories")
    ax.legend(fontsize=8.5)
    ax.set_ylim(0, 105)
    return _save(fig, outdir, "fig_degradation_traj")


def fig_benign_failure(outdir):
    """良性失效 vs 燃烧失效 对比"""
    fig, ax = plt.subplots(figsize=(8.2, 3.2))
    ax.axis("off")
    benign = ["SAPC (polymer Al)", "Polymer tantalum", "Metallized film (self-healing)"]
    severe = ["MnO2 tantalum (ignition/fire under surge)", "Liquid Al (vent/bulge, gas/electrolyte leak)"]
    _box(ax, 0.3, 1.6, 4.4, 1.4, "", fc=PALETTE[2], alpha=0.12, ec=PALETTE[2])
    ax.text(2.5, 2.78, "Benign failure (no fire)", ha="center", fontsize=10, fontweight="bold", color=PALETTE[2])
    for i, b in enumerate(benign):
        ax.text(0.55, 2.45-i*0.32, "+ " + b, ha="left", fontsize=8.4, color="#222")
    _box(ax, 5.0, 1.6, 4.4, 1.4, "", fc=C_SAPC, alpha=0.12, ec=C_SAPC)
    ax.text(7.2, 2.78, "Energetic / hazardous failure", ha="center", fontsize=10, fontweight="bold", color=C_SAPC)
    for i, s in enumerate(severe):
        ax.text(5.25, 2.45-i*0.32, "! " + s, ha="left", fontsize=8.2, color="#222")
    ax.text(4.85, 1.2, "Key safety advantage of SAPC: removal of MnO2/liquid -> no oxygen source / no liquid -> benign open",
            ha="center", fontsize=7.8, color="#777", style="italic")
    ax.set_xlim(0, 9.8); ax.set_ylim(1.0, 3.1)
    return _save(fig, outdir, "fig_benign_failure")


# ============================================================ 第4章 失效机理
def fig_mech_overview(outdir):
    """SAPC 失效机理总图（鱼骨/因果）"""
    fig, ax = plt.subplots(figsize=(10.0, 5.0))
    ax.axis("off")
    spine_y = 2.5
    # 主干
    ax.annotate("", xy=(8.7, spine_y), xytext=(0.6, spine_y),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=2.6))
    _box(ax, 8.7, spine_y - 0.45, 1.5, 0.9, "ESR rise /\nC drop /\nleakage rise",
         fc=C_SAPC, alpha=0.92, tcolor="w", fontsize=8.4)
    # 四根骨：上二、下二
    branches = [
        ("Thermal", ["PEDOT thermo-oxidation", "conductive-grain shrinkage", "O2 permeation thru molding"], "up", 2.2),
        ("Electrical", ["dielectric defect / BD", "re-anodization deficit", "local leakage path"], "up", 5.6),
        ("Humidity", ["moisture ingress", "PSS swelling / de-doping", "PEDOT domain disconnection"], "down", 2.2),
        ("Mechanical", ["reflow / CTE mismatch", "thermo-mechanical stress", "interface delamination"], "down", 5.6),
    ]
    for name, items, direction, x_join in branches:
        up = (direction == "up")
        y_end = 4.55 if up else 0.45
        x_end = x_join - 1.3
        # 斜骨
        ax.plot([x_join, x_end], [spine_y, y_end], color="#9aa7b5", lw=1.8)
        # 类别标签放在骨末端
        ax.text(x_end - 0.05, y_end + (0.0 if up else 0.0), name, fontsize=10,
                fontweight="bold", color="#2E5E8C",
                ha="right", va="bottom" if up else "top")
        # 子条目沿骨排列，文字统一在骨右侧
        n = len(items)
        for k, it in enumerate(items):
            frac = (k + 1) / (n + 1)
            xx = x_join + (x_end - x_join) * frac
            yy = spine_y + (y_end - spine_y) * frac
            ax.plot([xx, xx + 0.18], [yy, yy], color="#c4ced8", lw=1.0)
            ax.text(xx + 0.24, yy, it, fontsize=7.4, color="#444",
                    ha="left", va="center")
    ax.text(4.7, 4.92, "Fishbone of SAPC Failure Mechanisms (multi-stress coupling)",
            ha="center", fontsize=11, fontweight="bold", color="#222")
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0.0, 5.1)
    return _save(fig, outdir, "fig_mech_overview")


def fig_pedot_thermo(outdir):
    """PEDOT 热氧化/去掺杂 -> 导电晶粒收缩 过程示意"""
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2))
    titles = ["(a) Fresh: connected\nconductive grains",
              "(b) Aging: thermo-oxidation\n& de-doping",
              "(c) Degraded: shrunken grains,\nbroken percolation -> high ESR"]
    rng = np.random.default_rng(5)
    centers = rng.random((16, 2)) * 0.9 + 0.05
    radii = [0.085, 0.06, 0.04]
    for ax, t, r in zip(axes, titles, radii):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_title(t, fontsize=8.3)
        for c in centers:
            ax.add_patch(Circle(c, r, fc=C_SAPC, ec="k", lw=0.3, alpha=0.85))
        # 连接（仅在颗粒接近时）
        for i in range(len(centers)):
            for j in range(i+1, len(centers)):
                d = np.hypot(*(centers[i]-centers[j]))
                if d < 2*r + 0.02:
                    ax.plot([centers[i][0], centers[j][0]], [centers[i][1], centers[j][1]],
                            color="#27AE60", lw=1.0, zorder=0)
    axes[1].annotate("O2, heat\n+ counter-ion loss", xy=(0.5, 1.02), xytext=(0.5, 1.25),
                     ha="center", fontsize=7.5, color="#E67E22",
                     arrowprops=dict(arrowstyle="->", color="#E67E22"))
    fig.suptitle("PEDOT Conductive-Grain Model: Aging by Grain Shrinkage (concept)",
                 fontsize=10, y=1.04)
    return _save(fig, outdir, "fig_pedot_thermo")


def fig_oxide_hydration(outdir):
    """氧化铝介质水合机理"""
    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    ax.axis("off")
    steps = [
        ("H2O ingress\n(humidity/PSS)", "#2E5E8C"),
        ("Al2O3 + H2O ->\nAlOOH / Al(OH)3\n(hydration)", "#16A085"),
        ("oxide thickening /\nweakening, defect\ngeneration", "#E67E22"),
        ("leakage rise &\nlocal breakdown", "#C0392B"),
    ]
    for i, (t, c) in enumerate(steps):
        x = 0.3 + i*2.45
        _box(ax, x, 1.4, 2.0, 1.0, t, fc=c, alpha=0.18, ec=c, fontsize=8.2, tcolor=c)
        if i < 3:
            _arrow(ax, (x+2.0, 1.9), (x+2.45, 1.9), color="#555", lw=1.6)
    ax.text(5.0, 2.75, "Hydration/Hydrolysis of Anodic Al2O3 Dielectric (no liquid to re-form oxide)",
            ha="center", fontsize=9.2, fontweight="bold")
    ax.text(5.0, 0.95, "Contrast: liquid Al cap can re-anodize/self-heal oxide via electrolyte; SAPC cannot",
            ha="center", fontsize=7.8, color="#777", style="italic")
    ax.set_xlim(0, 10); ax.set_ylim(0.6, 3.0)
    return _save(fig, outdir, "fig_oxide_hydration")


def fig_delamination(outdir):
    """分层/界面退化机理"""
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Interface Delamination under Thermo-mechanical & Voltage Stress (KEMET concept)",
                 fontsize=9)
    layers = [("Al foil", "#B0B0B0", 0.74, 0.1), ("Al2O3", "#7FB3D5", 0.68, 0.05),
              ("PEDOT", "#C0392B", 0.52, 0.15), ("Carbon", "#34495E", 0.46, 0.05),
              ("Ag", "#BDC3C7", 0.40, 0.05)]
    for t, c, y, h in layers:
        ax.add_patch(Rectangle((0.12, y), 0.76, h, fc=c, ec="k", lw=0.5,
                               alpha=0.9 if c != "#7FB3D5" else 0.8))
        ax.text(0.92, y+h/2, t, ha="left", va="center", fontsize=7)
    # 分层缝
    ax.add_patch(Rectangle((0.30, 0.665), 0.36, 0.018, fc="w", ec="r", lw=1.3))
    ax.add_patch(Rectangle((0.20, 0.515), 0.25, 0.012, fc="w", ec="r", lw=1.3))
    ax.annotate("CTE mismatch + reflow + Vbias\n-> micro-gaps -> contact-area loss\n-> local ESR rise & hot spots",
                xy=(0.48, 0.67), xytext=(0.5, 0.12), ha="center", fontsize=7.6, color="r",
                arrowprops=dict(arrowstyle="->", color="r"))
    return _save(fig, outdir, "fig_delamination")


def fig_esr_arrhenius(outdir):
    """ESR/电导退化的 Arrhenius 关系（聚合物 Ea 较低）"""
    T = np.linspace(40, 150, 50) + 273.15
    k = 8.617e-5
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    for Ea, col, lab in [(0.7, C_SAPC, "PEDOT/SAPC Ea~0.7 eV (lower)"),
                         (0.94, C_INTL, "Liquid Al Ea~0.94 eV"),
                         (1.2, PALETTE[2], "MLCC Ea~1.2 eV"),
                         (1.5, PALETTE[3], "Tantalum Ea~1.5 eV")]:
        AF = np.exp(Ea/k*(1/(105+273.15) - 1/T))
        ax.semilogy(1000/T, AF, color=col, lw=2, label=lab)
    ax.set_xlabel("1000/T (1/K)")
    ax.set_ylabel("Acceleration factor (ref. 105C)")
    ax.set_title("Arrhenius Acceleration vs Activation Energy (representative)")
    ax.legend(fontsize=8)
    return _save(fig, outdir, "fig_esr_arrhenius")


def fig_humidity_factor(outdir):
    """湿度对 ESR/漏电退化的加速（示意）"""
    rh = np.linspace(20, 95, 50)
    fig, ax = plt.subplots(figsize=(7.0, 3.7))
    for n, col, lab in [(2.0, C_SAPC, "ESR rate ~ RH^2.0 (SAPC, strong)"),
                        (1.0, PALETTE[3], "Ta polymer ~ RH^1.0 (moderate)"),
                        (0.3, PALETTE[2], "MLCC ~ RH^0.3 (weak)")]:
        rate = (rh/50.0)**n
        ax.plot(rh, rate, color=col, lw=2, label=lab)
    ax.axvline(50, color="gray", ls=":", lw=1)
    ax.text(51, 0.3, "PSS swelling\nonset ~50%RH", fontsize=7.5, color="gray")
    ax.set_xlabel("Relative humidity (%)")
    ax.set_ylabel("Relative degradation rate (norm.)")
    ax.set_title("Humidity Acceleration of Degradation (illustrative)")
    ax.legend(fontsize=8)
    return _save(fig, outdir, "fig_humidity_factor")


def fig_liquid_evap(outdir):
    """液态铝电解：电解液蒸发机理 + 退化"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    ax1.axis("off"); ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_title("(a) Electrolyte loss mechanism", fontsize=9)
    ax1.add_patch(Circle((0.5, 0.5), 0.34, fc="#D6EAF8", ec="#2E5E8C", lw=2))
    ax1.text(0.5, 0.5, "electrolyte", ha="center", fontsize=7.5)
    for ang in np.linspace(0, 2*np.pi, 8, endpoint=False):
        ax1.annotate("", xy=(0.5+0.5*np.cos(ang), 0.5+0.5*np.sin(ang)),
                     xytext=(0.5+0.36*np.cos(ang), 0.5+0.36*np.sin(ang)),
                     arrowprops=dict(arrowstyle="->", color="#E67E22", lw=1))
    ax1.text(0.5, 0.06, "evaporation thru seal (T-driven)", ha="center", fontsize=7.2, color="#E67E22")
    # 退化曲线
    t = np.linspace(0, 1, 100)
    C = 100 - 18*t - 14*t**3
    ESR = 100*(1 + 2.2*t**2.2)
    axb = ax2.twinx()
    l1, = ax2.plot(t*100, C, color=C_INTL, lw=2, label="C")
    l2, = axb.plot(t*100, ESR, color=C_SAPC, lw=2, ls="--", label="ESR")
    ax2.set_xlabel("Service time (%)")
    ax2.set_ylabel("Capacitance (%)", color=C_INTL)
    axb.set_ylabel("ESR (%)", color=C_SAPC)
    ax2.set_title("(b) C drop & ESR rise (Ea~0.94 eV)", fontsize=9)
    ax2.legend(handles=[l1, l2], fontsize=8, loc="center left")
    return _save(fig, outdir, "fig_liquid_evap")


def fig_mlcc_ovm(outdir):
    """MLCC 氧空位迁移 + IR 退化"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    ax1.axis("off"); ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_title("(a) Oxygen-vacancy migration (Waser)", fontsize=9)
    ax1.add_patch(Rectangle((0.1, 0.3), 0.8, 0.4, fc="#D5C9A1", ec="k", lw=0.6, alpha=0.7))
    ax1.text(0.5, 0.63, "BaTiO3 grain", ha="center", fontsize=7.5)
    ax1.add_patch(Rectangle((0.1, 0.66), 0.8, 0.04, fc="#34495E"))
    ax1.add_patch(Rectangle((0.1, 0.30), 0.8, 0.04, fc="#34495E"))
    ax1.text(0.95, 0.68, "Ni (+)", fontsize=6.5, va="center")
    ax1.text(0.95, 0.32, "Ni (-)", fontsize=6.5, va="center")
    for i, xx in enumerate(np.linspace(0.2, 0.8, 5)):
        ax1.annotate("", xy=(xx, 0.36), xytext=(xx, 0.62),
                     arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1))
        ax1.add_patch(Circle((xx, 0.62), 0.018, fc="w", ec="#C0392B"))
    ax1.text(0.5, 0.2, "Vo.. drift to cathode under DC bias", ha="center", fontsize=7, color="#C0392B")
    t = np.logspace(0, 4, 100)
    for n, col, lab in [(0.3, PALETTE[2], "n=0.3"), (0.45, C_INTL, "n=0.45")]:
        IR = 1e3*10**(-0.0011*t**n)
        ax2.loglog(t, IR, color=col, lw=2, label="IR ~ exp(-k t^%s)" % n)
    ax2.set_xlabel("Time (h)"); ax2.set_ylabel("Insulation resistance (norm.)")
    ax2.set_title("(b) IR decay -> breakdown", fontsize=9)
    ax2.legend(fontsize=8)
    return _save(fig, outdir, "fig_mlcc_ovm")


def fig_film_selfheal(outdir):
    """金属化薄膜自愈机理 + 自愈累积容量损失"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    ax1.axis("off"); ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_title("(a) Self-healing: metal evaporates around defect", fontsize=8.6)
    ax1.add_patch(Rectangle((0.1, 0.45), 0.8, 0.2, fc="#9BD3C0", ec="k", lw=0.5, alpha=0.6))
    ax1.text(0.5, 0.7, "metallized layer (nm)", ha="center", fontsize=7)
    ax1.scatter([0.5], [0.55], s=80, marker="*", color="orange", zorder=5)
    ax1.add_patch(Circle((0.5, 0.55), 0.09, fill=False, ec="r", lw=1.2, ls="--"))
    ax1.text(0.5, 0.28, "arc evaporates electrode ->\nisolates defect (cleared area)",
             ha="center", fontsize=7, color="r")
    N = np.logspace(0, 6, 100)
    C = 100 - 9*(np.log10(N)/6)**1.3
    ax2.semilogx(N, C, color=C_INTL, lw=2)
    ax2.axhline(95, color=PALETTE[2], ls="--", lw=1, label="EoL strict (-5%)")
    ax2.axhline(90, color=C_SAPC, ls="--", lw=1, label="EoL loose (-10%)")
    ax2.set_xlabel("Cumulative self-healing events N")
    ax2.set_ylabel("Capacitance (% of initial)")
    ax2.set_title("(b) Capacitance loss vs SH count", fontsize=8.6)
    ax2.legend(fontsize=8); ax2.set_ylim(85, 101)
    return _save(fig, outdir, "fig_film_selfheal")


def fig_ta_crystallization(outdir):
    """钽 场致结晶 + 热失控"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    t = np.linspace(0, 1000, 100)
    for E, col, lab in [(200, PALETTE[2], "E=200 V/um"), (300, C_INTL, "E=300 V/um"),
                        (400, C_SAPC, "E=400 V/um")]:
        DCL = 0.1*np.exp((E/120)*(t/1000)**2)
        ax1.semilogy(t, DCL, color=col, lw=2, label=lab)
    ax1.set_xlabel("Time (h)"); ax1.set_ylabel("Leakage DCL (norm.)")
    ax1.set_title("(a) Field crystallization of Ta2O5", fontsize=8.8)
    ax1.legend(fontsize=8)
    Temp = np.linspace(20, 400, 100)
    Pj = 0.02*np.exp(Temp/70); Pd = 0.06*(Temp-20)
    ax2.plot(Temp, Pj, color=C_SAPC, lw=2, label="Joule heat (MnO2 fuels O2)")
    ax2.plot(Temp, Pd, color=C_INTL, lw=2, label="Dissipation")
    ax2.set_xlabel("Hot-spot temperature (C)"); ax2.set_ylabel("Power (norm.)")
    ax2.set_title("(b) Thermal runaway (MnO2 only)", fontsize=8.8)
    ax2.legend(fontsize=8); ax2.set_ylim(0, 25)
    return _save(fig, outdir, "fig_ta_crystallization")


def fig_mech_matrix(outdir):
    """机理对比矩阵：五类器件 x 核心机理"""
    mechs = ["Electrolyte\nevap.", "PEDOT thermo-\noxidation", "Oxide\nhydration",
             "O-vacancy\nmigration", "Self-\nhealing", "Field\ncrystalliz.", "Crack/\ndelam."]
    devs = ["SAPC", "Liquid Al", "MLCC", "Film", "Tantalum"]
    M = np.array([
        [0, 3, 2, 0, 1, 0, 3],   # SAPC
        [3, 0, 1, 0, 1, 0, 1],   # Liquid Al
        [0, 0, 1, 3, 0, 0, 3],   # MLCC
        [0, 0, 0, 0, 3, 0, 1],   # Film
        [0, 2, 0, 0, 2, 3, 2],   # Tantalum
    ])
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    im = ax.imshow(M, cmap="YlOrRd", vmin=0, vmax=3, aspect="auto")
    ax.set_xticks(range(len(mechs))); ax.set_xticklabels(mechs, fontsize=7.6)
    ax.set_yticks(range(5)); ax.set_yticklabels(devs, fontsize=9)
    ax.get_yticklabels()[0].set_color(C_SAPC); ax.get_yticklabels()[0].set_fontweight("bold")
    lab = {0: "", 1: "minor", 2: "sec.", 3: "dom."}
    for i in range(5):
        for j in range(len(mechs)):
            if M[i, j] > 0:
                ax.text(j, i, lab[M[i, j]], ha="center", va="center",
                        color="w" if M[i, j] >= 2 else "k", fontsize=7.4)
    ax.set_title("Failure-Mechanism Map: Five Families vs Core Mechanisms")
    ax.grid(False)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="dominance")
    return _save(fig, outdir, "fig_mech_matrix")


def fig_coupling(outdir):
    """SAPC 多应力耦合（T-V-RH）"""
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    circles = [((0.40, 0.60), "Thermal (T)", "#E67E22"),
               ((0.60, 0.60), "Humidity (RH)", "#2E5E8C"),
               ((0.50, 0.42), "Voltage (V)", "#C0392B")]
    for (cx, cy), lab, c in circles:
        ax.add_patch(Circle((cx, cy), 0.20, fc=c, ec=c, alpha=0.22, lw=1.5))
    ax.text(0.30, 0.74, "Thermal", fontsize=9, color="#E67E22", fontweight="bold")
    ax.text(0.62, 0.74, "Humidity", fontsize=9, color="#2E5E8C", fontweight="bold")
    ax.text(0.50, 0.22, "Voltage", fontsize=9, color="#C0392B", fontweight="bold", ha="center")
    ax.text(0.50, 0.54, "coupled\nfailure", ha="center", va="center", fontsize=8.5, fontweight="bold")
    ax.text(0.32, 0.50, "thermo-\noxidation", ha="center", fontsize=6.6)
    ax.text(0.68, 0.50, "de-doping\nhydration", ha="center", fontsize=6.6)
    ax.text(0.50, 0.66, "swelling", ha="center", fontsize=6.6)
    ax.set_title("SAPC Multi-Stress Coupling (T x V x RH)", fontsize=10)
    ax.text(0.5, 0.05, "Coupling makes single-stress Ea/n insufficient; needs generalized Eyring-type view",
            ha="center", fontsize=7.2, color="#777", style="italic")
    return _save(fig, outdir, "fig_coupling")


def fig_ea_compare(outdir):
    """激活能对比（代表性区间）"""
    lo = np.array([0.55, 0.85, 0.90, 0.80, 1.10])
    hi = np.array([0.90, 1.05, 1.49, 1.20, 1.50])
    mid = (lo+hi)/2; err = (hi-lo)/2
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    cols = [C_SAPC, C_INTL, PALETTE[2], PALETTE[4], PALETTE[3]]
    ax.bar(DEV_SHORT, mid, yerr=err, capsize=5, color=cols, edgecolor="k", lw=0.6, alpha=0.9)
    ax.set_ylabel("Activation energy Ea (eV)")
    ax.set_title("Reported/Representative Activation Energy by Family")
    for i in range(5):
        ax.text(i, hi[i]+0.03, "%.2f-%.2f" % (lo[i], hi[i]), ha="center", fontsize=7.6)
    ax.set_ylim(0, 1.8)
    ax.get_xticklabels()[0].set_color(C_SAPC); ax.get_xticklabels()[0].set_fontweight("bold")
    return _save(fig, outdir, "fig_ea_compare")


# ============================================================ 第5章 对比总览
def fig_radar_3module(outdir):
    """三模块（器件/失效模式/机理）国内外研究水平雷达"""
    cats = ["Device\nunderstanding", "Failure-mode\ncharacterization", "Mechanism\ntheory",
            "In-situ\ncharacterization", "Engineering\ntranslation", "Original\nmodels"]
    intl = [9, 9, 9, 8.5, 8, 9]
    dom = [6.5, 7.5, 6.5, 6, 8, 5.5]
    N = len(cats)
    ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    intl += intl[:1]; dom += dom[:1]; ang += ang[:1]
    fig, ax = plt.subplots(figsize=(6.2, 5.6), subplot_kw=dict(polar=True))
    ax.plot(ang, intl, color=C_INTL, lw=2, label="International (English lit.)")
    ax.fill(ang, intl, color=C_INTL, alpha=0.13)
    ax.plot(ang, dom, color=C_DOM, lw=2, label="Domestic (Chinese lit.)")
    ax.fill(ang, dom, color=C_DOM, alpha=0.13)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(cats, fontsize=8.2)
    ax.set_ylim(0, 10)
    ax.set_title("Research Level across 3 Modules (0-10)", pad=22)
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.12), fontsize=8)
    return _save(fig, outdir, "fig_radar_3module")


def fig_progress_bars(outdir):
    """国内外综合对比（起步时间/深度/原创/工程落地）"""
    dims = ["Start\ntime", "Research\ndepth", "Originality", "Engineering\nlanding", "Standard/\njudging power"]
    intl = [9, 9, 9, 8, 9]
    dom = [6, 7, 5.5, 8, 6]
    x = np.arange(len(dims)); wd = 0.38
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.bar(x-wd/2, intl, wd, label="International", color=C_INTL, edgecolor="k", lw=0.5)
    ax.bar(x+wd/2, dom, wd, label="Domestic", color=C_DOM, edgecolor="k", lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(dims, fontsize=8.5)
    ax.set_ylabel("Level (0-10, qualitative)")
    ax.set_title("International vs Domestic: Multi-dimension Comparison")
    ax.legend(fontsize=8.5); ax.set_ylim(0, 10)
    return _save(fig, outdir, "fig_progress_bars")


def fig_timeline_mech(outdir):
    """SAPC 失效机理研究演进时间轴"""
    events = [
        (1969, "P-V life eq.\n(ceramic)"),
        (1990, "Waser O-vacancy\nmodel (MLCC)"),
        (2000, "PEDOT solid\ncap commercialized"),
        (2008, "PEDOT:PSS thermal\ndegradation study"),
        (2016, "CALCE polymer-Al\nhumidity failure"),
        (2019, "NASA polymer-Ta\nESR thermo-oxidation"),
        (2020, "KEMET delamination\nmechanism"),
        (2025, "de-doping control\n/ in-situ analysis"),
    ]
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    ax.axis("off")
    yrs = [e[0] for e in events]
    ax.plot([min(yrs)-2, max(yrs)+2], [0, 0], color="#444", lw=2)
    for i, (yr, lab) in enumerate(events):
        up = i % 2 == 0
        y = 0.7 if up else -0.7
        ax.plot([yr, yr], [0, y*0.65], color="#999", lw=1)
        c = C_SAPC if yr >= 2000 else C_INTL
        ax.scatter([yr], [0], s=60, color=c, zorder=3, edgecolor="k")
        ax.text(yr, y, "%d\n%s" % (yr, lab), ha="center",
                va="bottom" if up else "top", fontsize=7.8)
    ax.set_xlim(min(yrs)-4, max(yrs)+4); ax.set_ylim(-1.5, 1.5)
    ax.set_title("Evolution of SAPC-related Failure-Mechanism Research")
    return _save(fig, outdir, "fig_timeline_mech")


# ============================================================ 第6章 研究空白
def fig_gap_mapping(outdir):
    """研究空白 -> 学位论文研究内容 对接图"""
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    ax.axis("off")
    gaps = [
        "G1 SAPC failure-rate (FIT)\nbenchmark missing",
        "G2 EoL thresholds for ESR/C/\nDCL inconsistent",
        "G3 multi-stress (T-V-RH)\ncoupling theory lacking",
        "G4 PEDOT de-doping/oxidation\nkinetics not quantified",
    ]
    works = [
        "W1 multi-sample ALT +\nWeibull FIT baseline",
        "W2 unified EoL criteria &\ndegradation-trajectory model",
        "W3 generalized-Eyring\ncoupled mechanism model",
        "W4 in-situ spectroscopy +\nphysics-based ESR kinetics",
    ]
    for i, g in enumerate(gaps):
        y = 3.6 - i*1.0
        _box(ax, 0.3, y, 3.6, 0.8, g, fc=C_INTL, alpha=0.14, ec=C_INTL, fontsize=7.8, tcolor="#222")
        _box(ax, 5.6, y, 3.6, 0.8, works[i], fc=C_SAPC, alpha=0.14, ec=C_SAPC, fontsize=7.8, tcolor="#222")
        _arrow(ax, (3.95, y+0.4), (5.55, y+0.4), color="#888", lw=1.8)
    ax.text(2.1, 4.55, "Research gaps", ha="center", fontsize=10, fontweight="bold", color=C_INTL)
    ax.text(7.4, 4.55, "Dissertation work", ha="center", fontsize=10, fontweight="bold", color=C_SAPC)
    ax.set_xlim(0, 9.6); ax.set_ylim(0.4, 4.8)
    return _save(fig, outdir, "fig_gap_mapping")


def fig_future_trends(outdir):
    """未来趋势展望"""
    fig, ax = plt.subplots(figsize=(8.8, 3.6))
    ax.axis("off")
    trends = [
        ("Materials", "stable PEDOT (de-acidified,\nanti-oxidation coatings)", "#16A085"),
        ("Mechanism", "in-situ multi-physics &\nquantified coupling kinetics", "#E67E22"),
        ("Modeling", "strong physics-embedded\nhybrid (PoF + PINN)", "#2E5E8C"),
        ("Assurance", "cross-condition generalization\n& autonomous reliability", "#C0392B"),
    ]
    for i, (t, body, c) in enumerate(trends):
        x = 0.3 + i*2.4
        _box(ax, x, 1.5, 2.1, 1.2, t, fc=c, alpha=0.18, ec=c, fontsize=9.4, tcolor=c)
        ax.text(x+1.05, 1.2, body, ha="center", va="top", fontsize=7.2, color="#333")
        if i < 3:
            _arrow(ax, (x+2.1, 2.1), (x+2.4, 2.1), color="#888", lw=1.5)
    ax.text(5.0, 3.4, "Future Trends for SAPC Failure & Reliability Research",
            ha="center", fontsize=10, fontweight="bold")
    ax.set_xlim(0, 10); ax.set_ylim(0.6, 3.6)
    return _save(fig, outdir, "fig_future_trends")


# ============================================================ 汇总
def generate_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    funcs = [
        # 第1章
        fig_causal_chain, fig_search_strategy, fig_lit_year, fig_lit_language, fig_scope_matrix,
        # 第2章
        fig_sapc_structure, fig_cathode_evolution, fig_pedot_molecule, fig_process_routes,
        fig_five_structures, fig_cathode_compare, fig_perf_radar, fig_esr_freq, fig_device_progress,
        # 第3章
        fig_mode_tree, fig_sapc_esr_thb, fig_sapc_cap_leak, fig_open_short_schematic,
        fig_mode_spectrum, fig_mode_stress_matrix, fig_degradation_traj, fig_benign_failure,
        # 第4章
        fig_mech_overview, fig_pedot_thermo, fig_oxide_hydration, fig_delamination,
        fig_esr_arrhenius, fig_humidity_factor, fig_liquid_evap, fig_mlcc_ovm,
        fig_film_selfheal, fig_ta_crystallization, fig_mech_matrix, fig_coupling, fig_ea_compare,
        # 第5章
        fig_radar_3module, fig_progress_bars, fig_timeline_mech,
        # 第6章
        fig_gap_mapping, fig_future_trends,
    ]
    out = {}
    for fn in funcs:
        name = fn.__name__.replace("fig_", "")
        out[name] = fn(outdir)
    return out


if __name__ == "__main__":
    import tempfile
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
    res = generate_all(d)
    print("Generated %d figures:" % len(res))
    for k, v in res.items():
        print("  ", k, "->", os.path.basename(v))
