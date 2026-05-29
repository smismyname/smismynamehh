# -*- coding: utf-8 -*-
"""
Builds the Word (.docx) literature-review chapter (Rev.3, greatly expanded ~100 pages):
"SAPC（叠层铝固态电容器）可靠性研究的国内外研究现状"

Rev.3 changes vs Rev.2:
- Deepened survey: expanded every section into multiple technical subsections; added
  device/material physics, transport theory (VRH), EIS/impedance, stochastic-process
  degradation models (Wiener/Gamma/IG), competing risks, PHM/PINN, thermal self-heating,
  thermomechanical (Coffin-Manson), failure-analysis methodology, application domains,
  and bibliometric analysis.
- 25 original schematic figures, ~16 comparison tables, ~45 equations.
- References expanded to 94 verifiable entries; integrity policy unchanged.
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import figs
from refs import REFERENCES, format_ieee

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
OUT_DOCX = os.path.abspath(os.path.join(HERE, "..", "SAPC可靠性研究现状_20260529.docx"))

CN_BODY = "宋体"
CN_HEAD = "黑体"
EN_FONT = "Times New Roman"


# ---------------- low-level helpers ----------------
def set_cn(run, cn=CN_BODY, en=EN_FONT, size=12, bold=False, italic=False, color=None):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = en
    r = run._element
    rpr = r.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), en)
    rfonts.set(qn("w:hAnsi"), en)
    rfonts.set(qn("w:eastAsia"), cn)
    if color is not None:
        run.font.color.rgb = color


def para(doc, text="", *, size=12, cn=CN_BODY, bold=False, align=None,
         line=1.5, first_indent_chars=0, space_after=6, space_before=0, italic=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    if align is not None:
        p.alignment = align
    if first_indent_chars:
        pf.first_line_indent = Pt(size * first_indent_chars)
    if text:
        run = p.add_run(text)
        set_cn(run, cn=cn, size=size, bold=bold, italic=italic)
    return p


def body(doc, text, size=12):
    return para(doc, text, size=size, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                first_indent_chars=2, line=1.5, space_after=6)


def bullet(doc, text, size=12):
    """Indented list-style paragraph (hanging) for enumerated points."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.space_after = Pt(4)
    pf.left_indent = Pt(size * 2)
    pf.first_line_indent = Pt(-size)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    set_cn(run, size=size)
    return p


def heading(doc, text, level=1):
    sizes = {1: 16, 2: 14, 3: 13, 4: 12.5}
    p = doc.add_heading(level=min(level, 4))
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    set_cn(run, cn=CN_HEAD, size=sizes.get(level, 12), bold=True, color=RGBColor(0, 0, 0))
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    return p


def equation(doc, text, number=None):
    """Centered italic equation line (with optional right-aligned number)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(4)
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.3
    r = p.add_run(text)
    set_cn(r, size=12, italic=True, en=EN_FONT, cn=CN_BODY)
    if number:
        tab = p.add_run("    （" + number + "）")
        set_cn(tab, size=11, cn=CN_BODY)
    return p


_FIG_NO = 0
FIG_LIST = []
TAB_LIST = []


def add_figure(doc, filename, fig_no, caption_cn, source_cn, width_cm=14.5):
    global _FIG_NO
    _FIG_NO += 1
    fig_no = _FIG_NO
    FIG_LIST.append((str(fig_no), caption_cn))
    path = os.path.join(ASSETS, filename)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(f"图 {fig_no}  {caption_cn}")
    set_cn(r, cn=CN_HEAD, size=10.5, bold=True)
    src = doc.add_paragraph()
    src.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = src.add_run(source_cn)
    set_cn(r2, cn=CN_BODY, size=9, color=RGBColor(0x55, 0x55, 0x55))
    src.paragraph_format.space_after = Pt(8)


def add_table(doc, table_no, caption_cn, header, rows, widths=None, fs=9.5, source_cn=None):
    TAB_LIST.append((str(table_no), caption_cn))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(f"表 {table_no}  {caption_cn}")
    set_cn(r, cn=CN_HEAD, size=10.5, bold=True)
    cap.paragraph_format.space_before = Pt(8)
    cap.paragraph_format.space_after = Pt(4)

    table = doc.add_table(rows=1, cols=len(header))
    table.style = "Light Grid Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for c, t in zip(hdr, header):
        c.text = ""
        rr = c.paragraphs[0].add_run(t)
        set_cn(rr, cn=CN_HEAD, size=fs, bold=True)
    for row in rows:
        cells = table.add_row().cells
        for c, t in zip(cells, row):
            c.text = ""
            rr = c.paragraphs[0].add_run(t)
            set_cn(rr, size=fs)
    if widths:
        for col, w in zip(table.columns, widths):
            for cell in col.cells:
                cell.width = Cm(w)
    if source_cn:
        s = doc.add_paragraph()
        s.alignment = WD_ALIGN_PARAGRAPH.LEFT
        rr = s.add_run(source_cn)
        set_cn(rr, size=8.5, color=RGBColor(0x55, 0x55, 0x55))
        s.paragraph_format.space_after = Pt(8)
    return table


def add_toc(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), r'TOC \o "1-3" \h \z \u')
    run._r.addprevious(fld)
    t = doc.add_paragraph()
    rr = t.add_run("（提示：在 Word 中按 Ctrl+A 后按 F9，选择“更新整个目录”即可生成带页码的目录。）")
    set_cn(rr, size=9, color=RGBColor(0x80, 0x80, 0x80))


def page_break(doc):
    doc.add_page_break()



# ================= FRONT MATTER =================
def s_front(doc):
    # ---------- COVER ----------
    for _ in range(3):
        para(doc, "", size=12)
    para(doc, "博士学位论文（章节稿）", size=14, cn=CN_HEAD, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    para(doc, "叠层铝固态电容器（SAPC）可靠性研究",
         size=24, cn=CN_HEAD, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    para(doc, "——失效模式、失效机理与可靠性建模的国内外研究现状",
         size=15, cn=CN_HEAD, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    para(doc, "Stacked Aluminum Polymer Solid Capacitors (SAPC):",
         size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    para(doc, "A Comprehensive Review of Failure Modes, Mechanisms and Reliability Modeling",
         size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    para(doc, "作者：（请填写）", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "导师：（请填写）", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "学科 / 专业：（请填写）", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "日期：2026 年 5 月", size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    # ---------- 编制与诚信说明 ----------
    heading(doc, "编制与文献诚信说明", level=1)
    body(doc,
         "本章为博士论文“国内外研究现状”章节的可直接编辑初稿（修订版三，已在前一稿基础上加深调研、扩充内容）。"
         "为保障学术诚信，全部参考文献均经检索后纳入，可经文末所给链接溯源；凡未能确证的 DOI、卷期或作者信息，"
         "均以“[DOI待核验]”或“建议核验”明确标注，未作虚构。提交前请务必在 Web of Science / Scopus / IEEE Xplore "
         "及出版商页面逐条复核，并按目标期刊或学位论文规范（GB/T 7714 或 IEEE）统一著录格式。")
    body(doc,
         "配图：正文图1–图30 为作者基于公开原理自行绘制的原创示意图（matplotlib 矢量化渲染），不含任何受版权保护的他人图件，可直接使用。"
         "对 SEM/TEM 形貌、XPS/EDS 成分及实测 I–V/C–V、阻抗谱等需引自原始论文的图件，本文不直接嵌入受版权保护的原图，"
         "而在附录 A“建议引用图表索引”中给出可溯源的真实出处（含 DOI），便于在取得授权后引用。")
    body(doc,
         "术语约定：SAPC（Stacked Aluminum Polymer/Solid Capacitor）指以导电聚合物（多为 PEDOT 或 PEDOT:PSS 体系）"
         "为固态电解质、由多片蚀刻阳极铝箔叠层并联、经塑封封装而成的叠层（多层）铝固态电解电容器；文献中常以"
         "“polymer aluminum (PA) / multilayer polymer aluminum (PAE) / aluminum polymer capacitor (APC)”指代同类器件[9]–[16]。"
         "为与之区分，本章对“混合型聚合物铝电容（hybrid polymer aluminum electrolytic capacitor）”——即同时含液态电解质与导电聚合物者[55],[56],[91]——单独讨论。"
         "全章主要符号与缩略语见附录 B。")
    page_break(doc)

    # ---------- 摘要 ----------
    heading(doc, "摘要", level=1)
    body(doc,
         "叠层铝固态电容器（SAPC）以导电聚合物替代传统液态电解质，兼具低等效串联电阻（ESR）、优良高频与温度特性、"
         "以及失效良性（不易燃爆）等优点[1],[14],[59],[88]，已成为高功率密度电源、汽车电子、固态硬盘与消费电子中片式钽电容与液态铝电解电容的重要替代器件[5],[15],[89]。"
         "然而，导电聚合物对湿、热、电应力敏感，其长期可靠性尚未被充分认识[15],[16]。本章按“器件—材料—失效模式—失效机理—可靠性建模—状态监测—应用需求”主线，"
         "系统梳理国内外研究现状并给出量化对比。在材料层面，基于颗粒金属（granular-metal）导电模型与变程跳跃（VRH）输运理论阐明 PEDOT 体系的电导起源及其热、湿、氧敏感性[17],[18],[67]–[70]；"
         "在失效模式层面，归纳湿热、高温、热-电耦合与热-机械四类典型模式，其退化以 ESR 上升、漏电流（LC）增大为主、电容量相对稳定[9],[10],[13]；"
         "在机理层面，阐明晶粒收缩、去掺杂/氧化、吸湿溶胀、界面分层与氧化膜自愈等关键过程[17],[25],[51],[52]；"
         "在建模层面，比较统计/经验（Arrhenius、Peck、Eyring、Weibull）、退化随机过程（Wiener、Gamma、逆高斯）、失效物理（PoF）与数据驱动/物理-数据融合（粒子滤波、LSTM、PINN）等方法的数学形式、适用边界与局限[29],[30],[35]–[39],[71]–[84],[93],[94]。"
         "最后凝练出现有研究的五点不足并据此提出本文切入点。本章共纳入可核验文献 94 条、原创图 30 幅、表格 31 张（正文 26 张、附录 5 张）、关键公式 24 式（编号 2-1~2-24）。")
    p = para(doc, "关键词：", size=12, bold=True, space_after=2)
    set_cn(p.add_run("叠层铝固态电容器；导电聚合物（PEDOT）；失效模式；失效机理；可靠性建模；退化随机过程；剩余寿命预测"), size=12)

    heading(doc, "Abstract", level=1)
    body(doc,
         "Stacked aluminum polymer solid capacitors (SAPC) replace the liquid electrolyte of conventional aluminum "
         "electrolytic capacitors with a solid conductive polymer (typically a PEDOT-based system), combining low equivalent "
         "series resistance (ESR), good high-frequency and temperature stability and a benign (non-ignition) failure behavior. "
         "However, the conductive polymer is sensitive to humidity, temperature and electrical stress, and the long-term "
         "reliability of SAPC is not yet fully understood. Following a device-material-failure mode-mechanism-modeling-monitoring-application "
         "thread, this chapter comprehensively reviews the state of the art and provides quantitative comparisons. At the material level it "
         "explains the conductivity of PEDOT through the granular-metal picture and variable-range-hopping (VRH) transport, together with its "
         "thermal, humid and oxidative sensitivities. It classifies four failure-mode families (humid-heat, high-temperature, thermo-electric "
         "and thermo-mechanical), characterized mainly by ESR rise and leakage-current increase with comparatively stable capacitance; analyzes "
         "the key mechanisms (PEDOT grain shrinkage and de-doping/oxidation, moisture-induced swelling, interfacial delamination and oxide "
         "self-healing); and compares statistical/empirical (Arrhenius, Peck, Eyring, Weibull), stochastic-process degradation (Wiener, Gamma, "
         "inverse-Gaussian), physics-of-failure and data-driven / physics-informed (particle filter, LSTM, PINN) reliability-modeling approaches "
         "with their governing equations and applicability. Five research gaps are distilled to motivate the dissertation. The chapter cites 94 "
         "verifiable references and contains 30 original figures, 31 tables and 24 numbered equations.")
    p = para(doc, "Keywords: ", size=12, bold=True, space_after=2)
    set_cn(p.add_run("stacked aluminum polymer capacitor; conductive polymer (PEDOT); failure modes; failure mechanisms; "
                     "reliability modeling; stochastic degradation process; remaining useful life"), size=12, en=EN_FONT)
    page_break(doc)

    # ---------- 目录 ----------
    heading(doc, "目录", level=1)
    add_toc(doc)
    page_break(doc)



# ================= 2.1 引言、范围与方法 =================
def s_intro(doc):
    heading(doc, "第2章  SAPC 可靠性研究的国内外研究现状", level=1)

    heading(doc, "2.1  引言、研究范围、文献来源与综述方法", level=2)

    heading(doc, "2.1.1  研究背景与意义", level=3)
    body(doc,
         "电容器是电力电子变换器、电源与电子整机中数量最多、却也最易成为可靠性短板的无源元件之一。权威综述指出，"
         "在功率变换装置的现场失效统计中，电容器与功率半导体、焊点并列为三大薄弱环节，电容器对系统的成本、体积与失效率均有可观贡献[1],[2]。"
         "在直流支撑（DC-link）、输出滤波与去耦等场合，电容器需在纹波电流自热、宽温度区间、湿度与机械振动的综合作用下长期稳定工作，"
         "其参数漂移与突发失效会直接影响电源效率、纹波抑制与整机寿命[1],[3],[47]。因此，准确认识电容器的失效模式、失效机理与寿命规律，"
         "并发展可外推的可靠性模型与状态监测方法，是提升电力电子系统可靠性的关键基础工作。")
    body(doc,
         "在各类电容器中，铝电解电容器以单位体积电容量高、价格低、耐压范围宽而长期占据大容量储能与滤波市场；"
         "但传统液态铝电解电容以电解液蒸发干涸为主导的磨损型失效限制了其在高温、长寿命场景中的应用[53],[54],[86]。"
         "导电聚合物固态电解质的引入从根本上改变了这一局面：以 PEDOT（聚 3,4-乙撑二氧噻吩）体系为代表的导电聚合物兼具高电子电导与固态稳定性，"
         "使聚合物铝电容获得极低的 ESR、优良的高频特性、稳定的温度特性以及失效良性（短路/过流时不起火、不爆炸）的安全特征[5],[14],[59],[61],[88]。"
         "叠层（多层并联）封装进一步提升了体积效率并降低了 ESL，使片式 SAPC 成为在高功率密度 DC-DC、汽车电子与固态硬盘等场景替代片式钽电容与液态铝电解电容的有力候选[15],[16],[89]。")
    body(doc,
         "然而，正是“以导电聚合物替代液态电解质”这一核心创新带来了新的可靠性问题：导电聚合物对湿、热、氧与电应力敏感，"
         "其退化以 ESR 上升、漏电流增大为主要表现，且缺乏液态体系那种依靠电解液持续供氧的强自愈能力[9],[12],[13]。"
         "更为关键的是，SAPC 作为相对较新的器件，其系统性的长周期、多应力可靠性数据仍然稀缺，公开文献高度集中于湿度（湿热）影响，"
         "对纯高温、热-电-机械耦合的认识相对薄弱[15],[16]。这使得“准确刻画 SAPC 的失效行为并建立可外推的寿命模型”既具有重要的工程价值，也是一个尚未充分解决的科学问题。"
         "本章的意义在于：以系统的文献综述厘清这一器件可靠性研究的全貌、共识与缺口，为后续章节的失效模式表征、机理建模与寿命预测奠定基础。")

    heading(doc, "2.1.2  研究范围界定", level=3)
    body(doc,
         "本章聚焦以导电聚合物为固态电解质的叠层（多层）铝固态电解电容器（SAPC）。在器件谱系上，与之密切相关、并在机理上可互为借鉴的器件包括："
         "①传统液态铝电解电容（液态电解质，磨损型蒸发失效）[53],[54],[87]；②混合型聚合物铝电容（液态电解质与导电聚合物并存，兼具低 ESR 与液态体系的自愈与温度寿命特征）[55],[56],[91]；"
         "③聚合物钽电容（Ta/Ta₂O₅ 介质 + 导电聚合物阴极，机理高度相似，数据较充分，是重要类比对象）[26],[42],[57]–[60],[64],[65],[76]。"
         "本章以 SAPC 为核心，对上述相关器件仅在“可迁移机理与方法”意义上引用，并在 2.2.6 与表1中明确其异同，避免将不同器件的结论不加区分地混用。")
    body(doc,
         "在内容范围上，本章覆盖：器件结构与制造工艺、导电聚合物材料物理化学、失效模式与判据、失效机理、加速试验与可靠性建模、"
         "状态监测与剩余寿命（RUL）预测、典型应用领域的可靠性要求，以及国内外研究对比与缺口分析。对单纯的材料合成与器件电气设计（如分散液配方细节、蚀刻工艺参数优化）"
         "仅在与可靠性直接相关时展开。时间范围以 2008 年至 2026 年的代表性文献为主，并向前追溯 Peck（1986）等奠基性工作[29]。")

    heading(doc, "2.1.3  文献来源与检索策略", level=3)
    body(doc,
         "文献检索以 Web of Science 核心合集、Scopus 与 IEEE Xplore 为主，辅以 RSC、Springer、Nature、Science、MDPI、Frontiers、ACS、AIP 等出版商数据库，"
         "并以 NASA 技术报告服务器（NTRS）、CALCE（美国马里兰大学先进生命周期工程中心）出版列表，以及 KEMET、Murata、Panasonic、TDK、Nippon Chemi-Con、CDE 等厂商技术资料补充工程证据。"
         "检索采用主题词与同义词组合，主要包括：“polymer aluminum (electrolytic) capacitor”“multilayer/stacked polymer aluminum capacitor”“aluminum polymer capacitor (APC)”"
         "“PEDOT(:PSS) degradation / conductivity / thermal ageing”“ESR / leakage current reliability”“temperature humidity bias (THB) / HAST”“self-healing oxide”"
         "“remaining useful life (RUL) / prognostics capacitor”“Weibull / Gamma process / particle filter capacitor”等，并对关键文献进行参考文献回溯与施引追踪（雪球法）。")
    body(doc,
         "围绕可靠性，相关研究可归入器件结构与材料、失效模式、失效机理、可靠性建模与寿命预测、状态监测五个相互关联的方向[1]–[3]。"
         "权威综述[1],[2]与专著[3],[94]从功率电子用电容器整体出发，建立了失效机理—失效模式—寿命模型的分析框架；"
         "CALCE、NASA NEPP 及主流厂商的实证研究[9]–[16],[55],[56],[59],[63],[75]–[77]构成了 SAPC 可靠性的核心证据来源；"
         "PEDOT 材料物理与降解机理的研究[17]–[24],[51],[52],[66]–[70],[92]提供了机理层面的微观依据；"
         "退化建模与 PHM 的方法学文献[35]–[39],[71]–[74],[78]–[84],[93]则支撑了寿命预测与状态监测部分。")

    heading(doc, "2.1.4  综述方法与本章结构", level=3)
    body(doc,
         "本章采用“按科学问题分块、对比—评判—收口”的综述方法：每一主题先归纳主流技术路线，再对比代表性工作的差异与定量结果，"
         "最后点明其共性局限并过渡到下一主题，从而把零散结论组织为“前人做到何处—尚存何种缺口—故本文研究必要”的逻辑主线，避免“文献罗列”式的平铺。"
         "为增强可读性与可核验性，全章以图、表、公式系统化呈现：失效模式与机理以分类图、机理示意图与对比表呈现；"
         "建模方法以方法图谱、数学公式与适用性对比表呈现；并在每节末以小结句承上启下。")
    body(doc,
         "本章其余部分组织如下：2.2 介绍 SAPC 器件结构、制造工艺、电气特性与技术演进；2.3 深入导电聚合物材料的物理化学基础（结构、掺杂、输运理论、热/湿/氧稳定性）；"
         "2.4 评述失效模式研究现状（判据与四类模式）；2.5 评述失效机理（聚合物本征退化、界面与分层、氧化膜与自愈、工艺缺陷、多机理耦合、失效分析方法）；"
         "2.6 系统比较可靠性评估与建模方法（加速试验与标准、经验模型、统计分布、退化随机过程、PoF、数据驱动与物理-数据融合、竞争失效与不确定性量化）；"
         "2.7 评述状态监测与 RUL 预测；2.8 梳理典型应用领域的可靠性要求；2.9 剖析代表性研究案例与方法学；2.10 进行国内外研究对比与文献计量；2.11 凝练不足并提出本文切入点；最后给出本章小结。"
         "图1与图2分别给出本章纳入文献的主题分布与发表年度趋势。")
    add_figure(doc, "fig_litdist.png", 1,
               "本章纳入文献的主题分布（基于真实检索结果的统计，共 94 条）",
               "来源：作者根据本章参考文献[1]–[94]自行统计绘制（原创图）。")
    add_figure(doc, "fig_bibliometric.png", 2,
               "本章纳入文献的发表年度分布与累积趋势（有明确年份的条目）",
               "来源：作者根据本章参考文献年份自行统计绘制（原创图）。")
    body(doc,
         "由图1、图2可见，本章证据来源在主题上覆盖均衡，既包含器件与材料、湿热与高温失效等实证研究，也涵盖建模、监测与标准；"
         "在时间上自 2008 年持续增长，并在 2016 年（多层 SAPC、CALCE 系列工作）与 2024 年（NASA 航天评估、PEDOT 机理新进展）出现两个高峰，"
         "反映出该领域近年活跃度上升、但仍以材料与单应力研究为主、器件级长周期数据相对滞后的总体态势[15],[16]。")



# ================= 2.2 器件结构、原理、工艺与演进 =================
def s_device(doc):
    heading(doc, "2.2  SAPC 器件结构、工作原理、制造工艺与技术演进", level=2)

    heading(doc, "2.2.1  阀金属电解电容器的基本原理", level=3)
    body(doc,
         "SAPC 仍属阀金属（valve-metal）电解电容范畴。其电容由阳极金属（铝）表面经阳极氧化（化成，forming）生成的致密 Al₂O₃ 薄膜充当介质，"
         "电容值近似遵循平行板关系：")
    equation(doc, "C = ε₀ · εr · A / d", "2-1")
    body(doc,
         "式中 ε₀ 为真空介电常数，εr 为 Al₂O₃ 相对介电常数（约 8–10），A 为有效电极面积，d 为氧化膜厚度。"
         "阀金属体系的关键特征在于：阳极氧化膜具有单向阻挡（整流）特性，仅在阳极正偏下保持高阻，因而器件为有极性元件；"
         "氧化膜厚度 d 近似与化成电压 V_f 成正比（约 1.0–1.4 nm/V），故较高的额定电压需要更厚的氧化膜，"
         "由式(2-1)可知这将以牺牲单位面积电容为代价（图3）[5],[45],[86]。")
    add_figure(doc, "fig_anodize.png", 3,
               "阳极氧化（化成）：氧化膜厚度随化成电压近似线性增长、单位面积电容随之下降",
               "来源：作者据阀金属电解电容化成原理[5],[45]绘制（原创概念图，非实测数据）。")
    body(doc,
         "为在有限体积内获得高电容，工业上对阳极铝箔进行电化学蚀刻（etching），形成密集的隧道孔或海绵状多孔结构，使有效表面积 A 较几何面积提升约一到两个数量级[45],[46]。"
         "蚀刻形貌与化成质量直接决定了初始电容、漏电流水平与介质缺陷密度，是器件可靠性的“先天”基础；国内学者对高压阳极铝箔与烧结铝箔氧化膜的微结构演变开展了持续研究[45],[46]，"
         "为降低初始缺陷密度、提升介质均一性提供了材料学依据。")

    heading(doc, "2.2.2  SAPC 单元结构与导电聚合物阴极", level=3)
    body(doc,
         "SAPC 的基本电容单元由“高比表面积蚀刻铝阳极箔—阳极氧化形成的 Al₂O₃ 介质膜—导电聚合物阴极—石墨层—银浆引出层”构成（图4）。"
         "与液态体系不同，SAPC 用导电聚合物作为“真正的阴极”，其高电子电导（PEDOT 体系可达 10²–10³ S·cm⁻¹ 量级[21],[62],[68]）显著降低 ESR、改善高频特性，"
         "并因不存在电解液蒸发而具有更稳定的温度特性[1],[5],[61],[88]。石墨层用于改善聚合物与银浆之间的接触并阻挡银迁移，银浆层则实现低阻引出。")
    add_figure(doc, "fig_structure.png", 4,
               "SAPC 单元结构与叠层封装示意（横截面）",
               "来源：作者基于公开器件原理自行绘制（原创图）；结构要素参见[4]–[7],[13],[14]。")
    body(doc,
         "导电聚合物阴极是 SAPC 区别于其它电解电容的核心。早期采用聚吡咯（PPy），随后过渡到聚噻吩衍生物，目前主流为 PEDOT 与其与聚苯乙烯磺酸（PSS）的复合体系 PEDOT:PSS[4],[6]–[8]。"
         "聚合物可经化学氧化原位聚合或分散液浸渍—干燥两类工艺填充进多孔阳极的孔道中，与氧化膜形成大面积、保形的电学接触。"
         "聚合物对多孔阳极的“浸润—填充—覆盖”完整性，决定了有效阴极面积与层间接触电阻，进而决定 ESR 的初始值与退化裕度（详见 2.3、2.5）[7],[12]。")

    heading(doc, "2.2.3  叠层封装结构与制造工艺", level=3)
    body(doc,
         "在单元基础上，多片单元并联叠层并以环氧塑封封装，形成低矮、适于表面贴装（SMD）的片式结构。并联叠层在不增加高度的前提下提升总电容、"
         "降低 ESR 与等效串联电感（ESL），是 SAPC 在高纹波、高频去耦场景的结构优势所在[5],[15],[89]。表2概括了 SAPC 的典型制造工艺流程与各工序对可靠性的影响。")
    add_table(doc, 2, "SAPC 典型制造工艺流程及其对可靠性的影响",
              ["工序", "工艺要点", "对可靠性的主要影响", "相关文献"],
              [["阳极蚀刻", "电化学蚀刻形成多孔结构", "决定有效面积、孔道可填充性与机械强度", "[45],[46]"],
               ["化成（阳极氧化）", "形成 Al₂O₃ 介质，厚度∝化成电压", "决定耐压、漏电与初始缺陷密度", "[5],[45]"],
               ["聚合物填充", "原位聚合或分散液浸渍—干燥", "决定阴极覆盖率、接触电阻与 ESR 裕度", "[6],[7],[12]"],
               ["石墨/银浆", "涂覆石墨层与银浆引出", "决定引出电阻、阻挡银迁移", "[13],[14]"],
               ["叠层并联", "多单元堆叠、阴阳极汇流", "决定总 C/ESR/ESL 与层间接触一致性", "[10],[15]"],
               ["塑封封装", "环氧模塑成型", "决定阻湿能力与热-机械应力（界面分层）", "[10],[12]"],
               ["老化/筛选", "加电老化、分选", "修复弱点、剔除早期失效（降低婴儿期）", "[50],[75]"]],
              widths=[2.0, 3.4, 5.2, 1.8], fs=8.8,
              source_cn="注：综合自[5]–[15],[45],[46],[50]；具体工艺参数依厂商与型号而异。")
    body(doc,
         "需特别强调，环氧塑封并非绝对阻湿屏障：水分会随时间通过封装体与引出端界面向器件内部扩散，这是湿热失效的前提条件[10],[12]。"
         "面向高可靠应用，文献提出了专门的高可靠叠层固态铝电容制备工艺（如优化聚合物分散液配方、强化界面黏附与封装密封、引入去质子化处理以中和 PSS 酸性等）[8],[50]，"
         "其目标正是抑制水分驱动的界面退化与聚合物去掺杂。")

    heading(doc, "2.2.4  电气特性与等效电路", level=3)
    body(doc,
         "SAPC 的电气行为可由串联 RLC 等效电路近似描述：理想电容 C 与等效串联电阻 ESR、等效串联电感 ESL 串联。其阻抗模值为：")
    equation(doc, "|Z(ω)| = sqrt( ESR² + ( 1/(ωC) − ωL )² ) ,   ω = 2πf", "2-2")
    body(doc,
         "由式(2-2)，阻抗谱呈“低频容性—中频电阻性（ESR 决定的谷底）—高频感性（ESL 主导）”三段特征，自谐振频率为 f₀ = 1/(2π√(ESL·C))（图5）。"
         "SAPC 的核心优势即在于其极低的 ESR 谷底与较高的 f₀，使其在高频纹波吸收与瞬态响应中明显优于液态铝电解电容[2],[61],[89]。"
         "器件 ESR 可近似分解为聚合物体电阻、聚合物/氧化膜界面与层间接触电阻、电极与引出端电阻之和：")
    equation(doc, "ESR ≈ R_polymer + R_interface/contact + R_electrode + R_termination", "2-3")
    add_figure(doc, "fig_impedance.png", 5,
               "SAPC 阻抗—频率特性与串联 RLC 等效电路（容性/电阻性/感性三段）",
               "来源：作者据电容器阻抗模型[2],[61]绘制（原创概念图，参数为示意值）。")
    body(doc,
         "其中聚合物体电阻与界面/接触电阻对湿、热应力最为敏感，是 SAPC 退化的主要电学表现来源（详见 2.3、2.5）。"
         "除 C、ESR、ESL 外，漏电流（LC）、损耗角正切（tanδ）、纹波电流额定值与温度/频率特性也是关键参数。"
         "漏电流反映介质完整性，受氧化膜缺陷、聚合物覆盖与电场—温度共同影响；液态铝电解电容因电解液持续供氧而具有强“再形成（reforming）”能力，漏电可被持续修复[3],[87]，"
         "而固态聚合物体系的修复能力相对有限，这是 SAPC 漏电失效需重点关注的原因之一[13],[59]。表3对比了三类铝/聚合物电容的典型电气特性。")
    add_table(doc, 3, "液态铝电解、SAPC 与聚合物钽电容的典型电气特性定性对比",
              ["参数", "液态铝电解", "SAPC（聚合物铝）", "聚合物钽", "说明/文献"],
              [["ESR", "较高", "很低（毫欧级）", "低", "聚合物阴极电导高[61],[89]"],
               ["高频/自谐振", "较差", "优", "优", "叠层降低 ESL[5],[15]"],
               ["温度特性", "受电解液影响大", "稳定", "稳定", "无电解液蒸发[88]"],
               ["漏电流自愈", "强（电解液供氧）", "有限", "有限", "固态体系修复弱[13],[59],[87]"],
               ["失效安全性", "可能鼓胀/喷液", "良性（不燃爆）", "良性（优于MnO₂）", "过流为良性失效[14],[59],[64]"],
               ["耐压范围", "宽（可达数百V）", "中（SMD约≤50–100V）", "中低", "聚合物耐压受限[91]"],
               ["对湿热敏感性", "中", "较高", "较高", "聚合物吸湿/去掺杂[9],[16]"]],
              widths=[2.0, 2.6, 2.8, 2.4, 2.6], fs=8.8,
              source_cn="注：定性对比综合自[3],[5],[9],[13]–[16],[59],[61],[64],[87]–[91]；定量值以具体型号规格书为准。")

    heading(doc, "2.2.5  技术演进与器件谱系", level=3)
    body(doc,
         "导电聚合物电解电容器自 20 世纪 90 年代起步[4]，其电解质体系历经聚吡咯、聚噻吩到 PEDOT:PSS 的迭代（图6）。"
         "PEDOT 因其在掺杂态下兼具高电导与较好的环境稳定性而成为主流；近年通过提高 PEDOT 分子量与结晶度、二次掺杂（如极性溶剂、离子液体处理）、"
         "优化分散液配方与去质子（中和 PSS 酸性）等手段持续改善电导与耐湿热性能[6]–[8],[20],[21],[62],[66],[68]。"
         "在器件形态上，则由卷绕结构演进到更低矮、利于密封的叠层塑封结构，并出现混合型（液态+聚合物）方案以兼顾低 ESR 与液态体系的自愈与温度寿命特征[55],[56],[91]。")
    add_figure(doc, "fig_timeline.png", 6,
               "导电聚合物（铝）电解电容器的技术演进时间线",
               "来源：作者综合[4]–[8],[15],[16],[50],[55]归纳绘制（原创图，年份为代表性节点）。")
    body(doc,
         "为厘清器件谱系并避免机理误用，表1对四类相关器件从电解质/阴极、ESR/高频、主导失效模式、失效特性与温/湿敏感性等维度进行对比。"
         "可见 SAPC 与聚合物钽电容在“低 ESR、良性失效、以 ESR 上升/漏电增大为主导退化、对湿热敏感”等方面高度相似，故聚合物钽的丰富可靠性数据常被用作 SAPC 的重要类比[26],[42],[57]–[60],[64],[65]；"
         "而与液态铝电解、混合型器件的差异，则集中体现在自愈能力、温度寿命机制与失效安全性上。")
    add_table(doc, 1, "SAPC 与相关电解电容器件的对比",
              ["器件类型", "电解质/阴极", "ESR/高频", "主导失效模式", "失效特性", "温/湿敏感性", "代表文献"],
              [["液态铝电解电容", "液态电解液", "ESR 较高", "电解液蒸发→C下降、ESR上升", "可能鼓胀/泄漏", "对温度敏感", "[1],[53],[54]"],
               ["混合型聚合物铝电容", "液态电解液+导电聚合物", "ESR 低、纹波能力强", "兼具蒸发与聚合物退化、具自愈", "良性、长寿命", "中等", "[55],[56],[91]"],
               ["SAPC（叠层固态）", "导电聚合物(PEDOT)", "ESR 低、高频优", "ESR 上升、LC 增大(C 稳定)", "良性、不易燃爆", "对湿热敏感", "[9],[10],[13]–[16]"],
               ["聚合物钽电容", "Ta₂O₅/导电聚合物", "ESR 低", "ESR 上升、LC/击穿", "良性、无磨损型失效", "对湿热/电场敏感", "[26],[42],[57]–[60]"]],
              widths=[2.6, 2.6, 1.8, 3.2, 2.2, 1.6, 2.0], fs=8.8,
              source_cn="注：表中定性比较综合自[1],[9],[10],[13]–[16],[26],[42],[53]–[61],[88]–[91]，定量参数请以具体型号规格书为准。")
    body(doc,
         "小结：SAPC 以蚀刻铝阳极/Al₂O₃ 介质提供高体积电容、以导电聚合物阴极提供低 ESR 与高频性能、以叠层塑封实现高体积效率与 SMD 兼容；"
         "其结构与材料创新带来的可靠性新问题，正是后续各节的主题。下一节首先深入导电聚合物材料的物理化学基础，因为 SAPC 多数退化模式的微观根源都可追溯至此。")



# ================= 2.3 导电聚合物材料物理化学基础 =================
def s_material(doc):
    heading(doc, "2.3  导电聚合物（PEDOT）材料的物理化学基础", level=2)
    body(doc,
         "SAPC 的多数退化模式（ESR 上升、漏电演化）在微观上都可追溯到导电聚合物阴极的材料行为。"
         "本节从化学结构与掺杂、电荷输运理论、形貌与相分离、热/氧稳定性、湿度响应、酸性与改性六个方面，系统梳理 PEDOT 体系的物理化学基础，"
         "为后续机理（2.5）与失效物理建模（2.6.5）提供材料学输入。")

    heading(doc, "2.3.1  PEDOT 的化学结构与掺杂机制", level=3)
    body(doc,
         "PEDOT（聚 3,4-乙撑二氧噻吩）是以噻吩环为主链、3,4 位被乙撑二氧基团桥接的共轭聚合物。其本征态电导很低，需通过氧化掺杂（p 型）在主链上形成正极化子/双极化子，"
         "由对阴离子（counter-anion）补偿电荷后才具有高电导[17],[67],[92]。在 PEDOT:PSS 体系中，PSS（聚苯乙烯磺酸）既作为水相分散剂，又以其磺酸根（SO₃⁻）作为对阴离子稳定 PEDOT⁺ 的正电荷（图9）[8],[22],[69]。"
         "因此 PEDOT:PSS 的电学与稳定性高度依赖 PEDOT 与 PSS 的比例、相分离结构以及对阴离子的种类与稳定性。")
    add_figure(doc, "fig_pedot_chem.png", 7,
               "PEDOT:PSS 结构示意：掺杂态 PEDOT⁺ 共轭主链由 PSS⁻ 对阴离子补偿电荷",
               "来源：作者据 PEDOT:PSS 化学结构[8],[22],[69]绘制（原创示意图）。")
    body(doc,
         "掺杂水平直接决定载流子浓度与电导：氧化（去电子）提高 p 型掺杂度，而还原/去掺杂（de-doping）则降低之。"
         "环境因素（热、氧、湿、UV）可通过改变掺杂水平、对阴离子分布与共轭长度而显著影响电导[18],[92]，这一“掺杂—电导”耦合是 PEDOT 退化的化学本质（详见 2.3.4–2.3.6）。"
         "研究还表明，counter-anion 的种类对薄膜稳定性影响显著，不同对阴离子主导的退化路径不同[92]。")

    heading(doc, "2.3.2  颗粒金属导电模型与变程跳跃输运", level=3)
    body(doc,
         "Vitoratos 等的经典工作[17]以“颗粒金属（granular-metal）”模型解释 PEDOT:PSS 的电导：导电的、富 PEDOT 的纳米晶粒嵌入相对绝缘的富 PSS 基体中，"
         "载流子在晶粒内呈金属性输运，而跨越晶粒间势垒时则以跳跃（hopping）方式进行。电导对温度的依赖常用变程跳跃（VRH）形式描述：")
    equation(doc, "σ(T) = σ₀ · exp[ −(T₀ / T)^p ]", "2-4")
    body(doc,
         "其中 p 取决于态密度与维度：Mott-VRH 在三维下 p = 1/4、二维下 p = 1/3；当库仑相互作用打开软隙时退化为 Efros–Shklovskii（ES）-VRH，p = 1/2。"
         "特征温度 T₀ 反映定域长度与态密度（T₀ 越大、势垒越高、电导越低）。对交联与不同浓度 PEDOT:PSS 薄膜的实验分析表明，其电导随温度的变化与 VRH 模型一致，"
         "并可据此提取跳跃温度、电子定域长度与载流子迁移率等参数[70]。统一的电荷输运模型进一步将“跳跃—迁移率边”机制纳入同一框架以描述从弱到强导电态的连续过渡[67]。")
    body(doc,
         "在此图像下，老化（热、氧、湿）使导电晶粒收缩、晶界（势垒宽度）增大，等效于式(2-4)中 T₀ 升高、σ 随时间下降，这正是器件 ESR 上升的微观根源（图10、图11）[17],[18],[62],[68]。"
         "高电导自掺杂 PEDOT 的研究[68]从反面印证了该机制：提高分子量可增加纳米晶数量、缩短相邻晶粒间距并降低跳跃激活能，从而把体电导提升至 >1000 S·cm⁻¹；"
         "反之，退化过程降低结晶度、拉大晶粒间距，必然抬高 ESR。表4汇总了 VRH 模型的主要形式与物理含义。")
    add_figure(doc, "fig_pedot_grain.png", 8,
               "PEDOT 颗粒金属导电模型：晶粒收缩使跳跃势垒变宽，导致 ESR 上升（示意）",
               "来源：作者据颗粒金属模型[17],[18],[62],[68]绘制的机理示意图（原创图）。")
    add_figure(doc, "fig_vrh.png", 9,
               "VRH 输运：老化抬高特征温度 T₀（ln σ 对 T^(−1/4) 与 T^(−1/2) 作图，新/老对比）",
               "来源：作者据 VRH 理论[17],[67],[70]绘制（原创概念图，非实测数据）。")
    add_table(doc, 4, "导电聚合物变程跳跃（VRH）模型的主要形式",
              ["模型", "指数 p", "适用条件", "T₀ 的物理含义", "文献"],
              [["Mott-VRH（3D）", "1/4", "费米面附近态密度近似常数、无库仑隙", "∝ 1/[N(E_F)·ξ³]", "[17],[70]"],
               ["Mott-VRH（2D）", "1/3", "二维输运（薄膜/界面）", "与定域长度、面态密度相关", "[70]"],
               ["ES-VRH", "1/2", "库仑相互作用打开软隙", "∝ e²/(εξ)", "[17],[67]"],
               ["近邻跳跃（NNH）", "—", "高温、热激活主导", "对应活化能 Eₐ（Arrhenius）", "[18],[67]"]],
              widths=[3.0, 1.6, 4.6, 3.4, 1.6], fs=8.8,
              source_cn="注：综合自[17],[67],[70]；实际体系常在不同温区间发生 p 值过渡。")

    heading(doc, "2.3.3  形貌、相分离与电导", level=3)
    body(doc,
         "PEDOT:PSS 的电导不仅取决于掺杂水平，更强烈依赖其层级结构（hierarchical structure）：富 PEDOT 晶粒的结晶度与取向、绝缘 PSS 壳层的厚度、以及颗粒的聚集状态共同决定颗粒内与颗粒间的输运[62],[69]。"
         "研究表明，减薄 PSS 壳层、促进 PEDOT 结晶并使颗粒聚集，可同时改善颗粒内与颗粒间输运、显著提升电导[69]；薄膜形貌（晶粒尺寸/相分离）对 PEDOT 电导的影响亦被系统研究[62]。"
         "极性溶剂、表面活性剂（如 Tween 80）与退火等后处理通过重排相分离结构降低电阻率——退火温度与时间的优化可使电阻率下降达约 85%，且热致结构重排（而非单纯失水）是降阻的关键驱动[66]。")
    body(doc,
         "从可靠性角度看，这一“形貌—电导”强相关意味着：任何导致结晶度下降、相分离粗化或颗粒间距增大的过程（吸湿溶胀、热氧老化、界面应力），都会直接表现为电导下降与 ESR 上升。"
         "因此，SAPC 的 ESR 退化本质上是聚合物阴极微结构在多场作用下退化的宏观映射，这为 2.6.5 中“以聚合物电导动力学驱动器件级 ESR 寿命模型”的失效物理思路提供了依据。")

    heading(doc, "2.3.4  热稳定性与热氧老化", level=3)
    body(doc,
         "热（氧）老化是 PEDOT 体系在高温场景下的主要退化途径。Vitoratos 等[17]发现 PEDOT:PSS 电导随时间呈指数式下降，符合颗粒收缩的颗粒金属图像；"
         "Sakkopoulos、Vitoratos 等[18]通过惰性氦气与空气气氛的对比实验证明，氧（空气）气氛显著加速老化，提示氧化是主导退化途径之一。"
         "聚合物钽电容的高温存储研究进一步将 ESR 退化归因于导电聚合物的热-氧化过程，并观察到电阻率随老化时间近似指数增长[42],[43]——这一规律对 SAPC 的高温失效具有直接的类比意义（详见 2.4.3、2.5.1）。")
    body(doc,
         "热老化的动力学常以 Arrhenius 形式刻画其速率常数 k 对温度的依赖：")
    equation(doc, "k(T) = A · exp( −Eₐ / (k_B · T) )", "2-5")
    body(doc,
         "式中 Eₐ 为激活能、k_B 为玻尔兹曼常数。若以电导（或 ESR）的相对变化作为退化量，则可由不同温度下的退化速率提取 Eₐ，并据此外推使用温度下的寿命（见 2.6.2）。"
         "需注意，PEDOT 的热氧老化往往是“掺杂水平下降 + 微结构粗化”的叠加，单一活化能仅是工程近似；气氛（氧分压）、湿度与对阴离子稳定性都会改变表观 Eₐ[18],[42],[92]。")

    heading(doc, "2.3.5  湿度响应与吸湿溶胀", level=3)
    body(doc,
         "PSS 具有强吸湿性，使 PEDOT:PSS 对环境湿度高度敏感。电-光研究显示，薄膜从约 9%RH 升至 80%RH 时光学厚度增加约 150%（显著溶胀），"
         "并存在“低 RH 表面吸附—中 RH 体相扩散溶胀—高 RH 饱和”的三段吸水机制[52]。计算模拟表明，水通过孔道渗入 PEDOT 与 PSS 相后，使层状晶区变小、更无序、间距增大，从而降低电导[51]。"
         "吸湿一方面通过溶胀拉大颗粒间距、增大跳跃势垒而降低电导；另一方面为去掺杂、对阴离子迁移与界面腐蚀提供介质，是湿热失效的物理化学起点（图12，详见 2.5.2）[24],[51],[52]。")
    body(doc,
         "湿气在器件内部的输运可由 Fick 第二定律描述（见式 2-9），其时间尺度由封装阻湿能力（扩散系数与厚度）与界面黏附决定[10],[12]。"
         "因此，SAPC 的湿热可靠性是“材料吸湿敏感性”与“封装/界面阻隔能力”共同作用的结果，单纯改善其一并不足以根治湿热失效。")
    add_figure(doc, "fig_moisture.png", 10,
               "水分侵入、聚合物溶胀与聚合物/氧化膜界面分层机理（示意）",
               "来源：作者据[10],[12],[24],[51],[52]所述机理绘制（原创图）。")

    heading(doc, "2.3.6  酸性、去掺杂与改性策略", level=3)
    body(doc,
         "PEDOT:PSS 中 PSS 的强酸性（磺酸基）会腐蚀相邻材料、损害器件并限制长期稳定性[22]。针对这一问题，文献提出多条改性路线："
         "①去质子/中和——以弱碱去除质子化掺杂，降低酸性并改善铝固态电容性能[8]；②非酸性替代或界面阻挡层——以减弱酸性对介质与界面的侵蚀[22]；"
         "③二次掺杂与配方优化——通过极性溶剂、离子液体、表面活性剂处理提升电导与稳定性[20],[21],[66]；④提高分子量/结晶度——增加纳米晶数量、降低跳跃激活能[68]。"
         "这些策略的共同目标是“在保持高电导的同时，抑制去掺杂与界面退化”，从材料源头改善 SAPC 的湿热与高温可靠性。")
    body(doc,
         "小结：PEDOT 体系的电导源于掺杂态共轭主链与颗粒金属/VRH 输运，其对热、氧、湿、酸高度敏感；"
         "晶粒收缩、去掺杂、溶胀与相分离粗化构成了“电导下降→ESR 上升”的统一材料学链条。这一认识是理解 SAPC 失效模式与机理（2.4、2.5）以及建立失效物理模型（2.6.5）的基础。")



# ================= 2.4 失效模式研究现状 =================
def s_modes(doc):
    heading(doc, "2.4  失效模式研究现状", level=2)
    body(doc,
         "失效模式描述器件“如何表现为失效”，是连接外部应力与内部机理的中间层。本节先界定 SAPC 的失效判据与参数表征，"
         "再按主导应力评述湿热、高温、热-电耦合与热-机械四类失效模式，最后给出失效模式的分类与统计对比。")

    heading(doc, "2.4.1  失效判据与参数表征", level=3)
    body(doc,
         "电解电容的失效通常分为“突发失效（catastrophic，短路/开路）”与“退化失效（degradation/parametric，参数超限）”两类。"
         "对 SAPC，工程上以电容量变化、ESR 与漏电流（LC）作为主要健康指标，常用失效判据示例为：电容量变化 |ΔC/C₀| 超过 ±20%、ESR 超过初值的 2 倍、或 LC 超过规格上限[2],[13],[80]。"
         "与液态铝电解电容以电解液干涸、容量下降为主导的磨损失效（其寿命近似遵循 Arrhenius“10°C 法则”，见 2.6.2）不同，"
         "SAPC 的退化以 ESR 上升与 LC 增大为主，而电容量在多数试验中相对稳定[9],[13],[53],[54]。图14给出三类参数随应力时间的典型退化趋势示意。")
    add_figure(doc, "fig_param_trends.png", 11,
               "SAPC 关键参数（ESR/C/LC）随应力时间的典型退化趋势（示意）",
               "来源：作者据[9],[10],[13]所述规律绘制的概念示意图（原创图，非实测数据）。")
    body(doc,
         "在指标选择上，研究普遍认为 ESR 较电容量更适合作为 SAPC/铝电解电容的健康指标：其一，ESR 随退化单调上升、灵敏度高；其二，ESR 与失效物理（聚合物电导、界面接触）直接相关；"
         "其三，ESR 可由纹波电压/电流或阻抗辨识在线获取[2],[80]。漏电流则对介质缺陷、工艺杂质（见 2.5.4）与电场—温度更敏感，是突发短路型失效的前兆指标[9],[75]。"
         "需要强调，ESR 具有显著的频率与温度依赖性，比较退化数据时须在统一频率（如 100 kHz）与温度下进行，否则易产生误判[2]。")

    heading(doc, "2.4.2  湿热环境失效模式", level=3)
    body(doc,
         "湿热是 SAPC 研究最充分、也最受关注的应力。CALCE 在 85°C/85%RH 等条件（含额定偏压）下对不同厂商（如 Nichicon、Nippon Chemi-Con）PEDOT 体系聚合物铝电容的研究表明，"
         "其主导失效为 ESR 上升与漏电流增大两类，两类模式在不同厂商样品中占比不同，而电容量保持稳定[9]；CALCE 还发展了“快速评估测试”以缩短湿热可靠性评价周期[63]。"
         "针对叠层（多层）封装器件，文献[10]在 85°C/85%RH 与 110°C/85%RH（额定偏压）双条件下记录失效时间并建立温度相关寿命模型，指出水分透过塑封层向内扩散是湿热退化的前提；封装几何对水分驱动退化的影响被专门研究[10]。"
         "厂商资料进一步印证：老化使有效电极面积与层间接触面积下降，从而 C 下降、ESR 上升[13]。")
    body(doc,
         "就物理本质，湿热失效可分解为三条机理链（详见 2.5）：①导电聚合物吸湿溶胀与氧化/去掺杂导致体电导下降；"
         "②聚合物/氧化膜界面在热-机械与电应力下的腐蚀与分层，使接触电阻增大；③界面腐蚀与漏电通道形成。"
         "值得注意的是，CALCE 在个别批次中还发现制造引入的金属（铁）颗粒嵌入介质层、形成此前文献未报道的高漏电“新机理”[9],[12]（见 2.5.4），提示湿热失效与工艺缺陷可能叠加。"
         "总体而言，湿热失效兼具“退化型（ESR/LC 缓升）”与“突发型（漏电骤增→短路）”双重特征，是 SAPC 在非密封、潮湿环境应用的首要约束。")

    heading(doc, "2.4.3  高温环境失效模式", level=3)
    body(doc,
         "在高温（≥105–125°C）或高温存储条件下，SAPC 退化以导电聚合物的热（氧）老化为核心。Vitoratos 等指出 PEDOT:PSS 在热与氧作用下电导随时间下降，宏观表现为 ESR 上升[17]；"
         "气氛对比研究表明空气（氧）气氛显著加速老化[18]。厂商资料明确：高温下电解质（聚合物）退化导致电容量偏离标准值，最终趋于开路模式，对应器件寿命终止[13]。"
         "聚合物钽电容的高温存储研究[42],[43]显示了相似的 ESR 退化规律（电阻率随老化近指数增长），可为铝固态体系提供机理类比。"
         "此外，高温会加剧封装与界面的热-机械应力，并可能影响 Al₂O₃ 介质膜稳定性，进而影响漏电流水平[28]。")
    body(doc,
         "需强调，相比湿热，针对 SAPC 在纯高温/高温存储下的系统寿命数据仍较少。NASA NEPP 明确指出该类器件（APC）可靠性数据稀缺、已有文献多集中于湿度影响，"
         "并据此对片式铝聚合物电容开展了专门的应力测试与航天适用性评估[15],[16]。这一“高温长周期数据缺口”是当前研究的明显短板之一，也是本文拟补强的方向（见 2.10）。")

    heading(doc, "2.4.4  热-电耦合失效模式", level=3)
    body(doc,
         "在实际工况中，纹波电流自发热与外加偏压共同作用形成热-电耦合失效。一方面，ESR 上升导致焦耳热增加：")
    equation(doc, "P = I_ripple² · ESR(f, T) ,   T_hot = T_amb + P · (R_th,core-case + R_th,case-amb)", "2-6")
    body(doc,
         "由式(2-6)，局部温升又进一步加速聚合物退化、抬高 ESR，构成正反馈（图15）；混合型与固态器件的纹波电流能力与自热问题在工程上被高度关注[54],[55],[56],[85]。"
         "另一方面，直流偏置电压对退化速率有显著影响——偏压加速了去掺杂、界面电化学过程与介质场致退化[28]。"
         "在介质层面，铝氧化膜在电场下存在击穿—自愈行为：文献[25]在铝氧化膜-聚合物体系中观测到“可逆的击穿后导通”，并将自愈与界面缺陷的阻变机制相联系；"
         "这与聚合物阴极相较 MnO₂“失效更良性、不易燃爆”的工程经验一致[14],[59],[64]。热-电-机械多场耦合下的界面分层与漏电演化，是当前定量描述最为薄弱、却对寿命预测最关键的环节。")
    add_figure(doc, "fig_thermal.png", 12,
               "热-电自热模型：纹波焦耳热经热阻网络抬升热点温度，形成 ESR—温升正反馈",
               "来源：作者据电容器自热/热阻模型[54],[85]绘制（原创示意图）。")

    heading(doc, "2.4.5  热-机械应力与温度循环失效模式", level=3)
    body(doc,
         "SAPC 为片式 SMD 器件，在装配（回流焊）与服役（温度循环、振动）中承受热-机械应力。环氧塑封、铝箔、聚合物与焊点之间存在热膨胀系数（CTE）失配，"
         "温度循环引起的交变应变会导致两类损伤：其一为器件内部聚合物/氧化膜界面的分层与脱黏，表现为 ESR 上升（与湿热失效的界面机理相通，见 2.5.2）；"
         "其二为外部焊点的疲劳开裂，表现为接触电阻增大乃至开路[81],[82]。焊点温度循环疲劳寿命常以 Coffin–Manson 关系描述：")
    equation(doc, "N_f = C · (Δε_p)^(−m) ;   AF = ( ΔT_test / ΔT_use )^m · f(t_dwell, T_max)", "2-7")
    body(doc,
         "式中 N_f 为失效循环数、Δε_p 为塑性应变幅、m 为疲劳指数、C 为材料常数；工程上常以温度循环幅 ΔT 近似驱动应变并结合对数正态分布建模失效[81],[82]。"
         "对贴片无源器件焊点疲劳的对比研究表明，器件尺寸、焊点高度与焊料体积对寿命有显著影响（器件越大、CTE 失配下应变越大，寿命往往越短）[81]。"
         "高可靠/航天应用对此尤为关注，因为温度循环与振动叠加会加速分层与焊点失效；KEMET 指出，恰当封装的固态聚合物铝电容具有较好的抗振性能，因为固态电解质不存在液体晃动[88]。"
         "目前，将 SAPC 内部界面分层与外部焊点疲劳统一纳入寿命模型的工作仍较缺乏，多数研究将二者分别处理。")

    heading(doc, "2.4.6  浪涌、过压与过流失效模式", level=3)
    body(doc,
         "在上电瞬间、负载突变或异常工况下，SAPC 可能承受浪涌电流、过压或过流。聚合物阴极器件在此类时变应力下的突出优点是失效良性："
         "NASA 的破坏性过流试验表明，聚合物铝电容在大电流过应力下均以良性模式失效，未出现起火、燃烧或其它灾难性后果[14]；"
         "这与导电聚合物在缺陷处高阻化（自愈）、隔离击穿点的机制有关（见 2.5.3），也是其相较 MnO₂ 钽电容的安全优势[59],[64]。"
         "针对时变应力，NASA 采用浪涌阶梯应力试验（SSST）识别批次的临界应力水平并研究上电失效机制[75]；干燥环境下聚合物钽电容还可能出现异常充电电流（ACC），其评判尚无统一标准[77]。"
         "对 SAPC 而言，浪涌/过压失效更多体现为漏电增大与局部介质损伤，而非灾难性爆炸，这一良性特征在安全关键应用中具有重要价值。")

    heading(doc, "2.4.7  失效模式的分类与统计对比", level=3)
    body(doc,
         "综合上述，按主导应力可将 SAPC 失效模式归为湿热、高温、热-电耦合与热-机械四类（图16），其参数退化总体表现为 ESR 单调上升并在寿命末期加速、"
         "LC 在某些批次显著抬升、电容量缓变[9],[10],[13]。表5以类 FMEA（失效模式与影响分析）的方式，归纳各失效模式的应力条件、主导退化参数、关键机理、检测指标与代表文献，"
         "便于在后续机理（2.5）与建模（2.6）中逐项对应。")
    add_figure(doc, "fig_taxonomy.png", 13,
               "SAPC 失效模式分类（按主导应力）",
               "来源：作者综合[9]–[16],[81]归纳并自行绘制（原创图）。")
    add_table(doc, 5, "SAPC 失效模式的类 FMEA 归纳",
              ["失效模式", "典型应力条件", "主导退化参数", "关键微观机理", "检测/前兆指标", "代表文献"],
              [["湿热环境", "85/85 THB；HAST", "ESR↑、LC↑（C 稳定）", "吸湿溶胀、氧化去掺杂、界面腐蚀/分层", "ESR、LC、EIS 弧增大", "[9],[10],[12],[63]"],
               ["高温环境", "≥105–125°C、高温存储", "ESR↑（C 漂移→开路）", "PEDOT 热氧老化、晶粒收缩、接触退化", "ESR、tanδ", "[13],[17],[42],[43]"],
               ["热-电耦合", "纹波自热+直流偏置", "ESR↑、LC↑、局部温升", "焦耳热正反馈、偏压加速、热-机分层", "ESR、热点温度、LC", "[25],[28],[55],[56]"],
               ["热-机械", "回流焊、温度循环、振动", "ESR↑→开路（焊点/界面）", "CTE 失配、界面分层、焊点疲劳", "接触电阻、X-ray/C-SAM", "[81],[82],[88]"],
               ["浪涌/过流", "上电浪涌、过压、SSST", "LC↑、局部介质损伤", "场致击穿与自愈、隔离击穿点", "SSST 临界应力、LC", "[14],[59],[75],[77]"]],
              widths=[1.8, 2.8, 2.4, 3.8, 2.4, 1.6], fs=8.6,
              source_cn="注：归纳自[9]–[28],[42],[43],[55],[56],[63],[75],[77],[81],[82],[88]；定量阈值依标准[31]–[34]与具体型号而定。")
    body(doc,
         "需要指出，上述分类是“按主导应力”的工程划分，实际服役中各应力往往同时存在、相互耦合（如湿热+偏压、高温+纹波+温度循环），"
         "对应多机理竞争失效（见 2.6.7）。现有失效模式研究多为定性描述与单应力实证，缺乏统一、可量化的多参数判定框架，这是本文拟改进之处（见 2.10）。")



# ================= 2.5 失效机理研究现状 =================
def s_mech(doc):
    heading(doc, "2.5  失效机理研究现状", level=2)
    body(doc,
         "失效机理解释“为何会退化”，是从材料/界面过程到器件参数演化的因果链条。SAPC 的失效机理可归纳为三条相互交织的主链——导电聚合物本征退化、界面退化与分层、介质氧化膜损伤与自愈，"
         "并叠加制造缺陷与多机理耦合。本节逐一评述，并尽量给出可量化的机理描述，最后介绍支撑机理研究的失效分析方法。")

    heading(doc, "2.5.1  导电聚合物本征退化（去掺杂、氧化与晶粒收缩）", level=3)
    body(doc,
         "如 2.3 所述，PEDOT 的电导源于掺杂态共轭主链与颗粒金属/VRH 输运。本征退化表现为三个相互关联的过程："
         "①去掺杂——还原或对阴离子迁移使载流子浓度下降；②氧化老化——氧/UV 等破坏共轭、改变对阴离子稳定性[18],[92]；③晶粒收缩与相分离粗化——导电晶粒变小、晶界变宽、颗粒间距增大[17],[51]。"
         "三者共同降低体电导 σ，并按式(2-3)抬升 ESR 的体电阻分量。工程上常以指数型衰减近似聚合物电导（或等效地以 ESR 增长）随时间的演化：")
    equation(doc, "σ(t) = σ₀ · exp( −t / τ ) ,   ESR_polymer(t) ∝ 1/σ(t) ⇒ ESR(t) ≈ ESR₀ · exp( t / τ )", "2-8")
    body(doc,
         "式中时间常数 τ 由温度、氧分压与湿度共同决定，可经式(2-5)的 Arrhenius 关系与温度相联系。"
         "聚合物钽电容高温存储中观察到的“电阻率随老化近指数增长”[42],[43]为式(2-8)提供了实验支持。"
         "由于本征退化把“分子—晶粒—薄膜—器件”各尺度串联起来，建立连接 σ(t) 与器件级 ESR(t)/LC(t) 的定量映射，是失效物理建模（2.6.5）的核心任务，而目前面向 SAPC 的此类定量贯通仍不充分。")

    heading(doc, "2.5.2  水分扩散、界面退化与分层", level=3)
    body(doc,
         "在叠层塑封器件中，水分透过封装向内扩散，到达聚合物/氧化膜界面后引发氧化与界面黏附退化；在热-机械与电应力作用下界面发生分层（delamination），"
         "使层间接触电阻增大、有效阴极面积减小，宏观表现为 ESR 上升乃至漏电通道形成（见图12）。水分在封装/界面中的输运可由 Fick 第二定律描述：")
    equation(doc, "∂C_w/∂t = D · ∇²C_w ,   D(T) = D₀ · exp( −E_D / (k_B T) )", "2-9")
    body(doc,
         "式中 C_w 为水分浓度、D 为扩散系数（亦服从 Arrhenius 温度依赖）。封装阻湿能力（D 与厚度）与界面黏附决定了湿热失效的时间尺度，封装几何对湿致退化的影响因而被专门研究[10]。"
         "KEMET 将热-机械与电压诱发的分层视为高湿环境下电导退化的主要原因之一[12]；PEDOT:PSS 薄膜的湿致溶胀、降解与分层在材料层面亦被广泛报道[24],[51],[52]。"
         "界面退化是“封装阻湿能力—界面黏附—接触电阻—ESR/LC”链条的枢纽，是湿热、热-电与热-机械失效的共同环节，也是建立 PoF 竞争失效模型时必须刻画的核心。")

    heading(doc, "2.5.3  介质氧化膜损伤、场致退化与自愈", level=3)
    body(doc,
         "Al₂O₃ 介质膜的完整性决定漏电流水平。局部缺陷、场致结晶或界面应力可形成漏电通道，其漏电常表现出场致增强特征，可用 Poole–Frenkel 型关系近似描述：")
    equation(doc, "J_LC ∝ E · exp[ ( β_PF · sqrt(E) − φ ) / (k_B T) ]", "2-10")
    body(doc,
         "式中 E 为介质电场、φ 为陷阱势垒、β_PF 为 Poole–Frenkel 系数。导电聚合物阴极在缺陷处的高阻化可“隔离”击穿点，实现自愈，从而抑制漏电并避免热失控，"
         "这也是聚合物器件失效“更良性”的物理原因[25],[26],[59],[60]。文献[25]在铝氧化膜-聚合物体系中观测到可逆的击穿后导通，并将自愈与界面缺陷的阻变机制相联系；"
         "聚合物钽电容的自愈效率被证明直接决定其可靠性与失效模式[27]。")
    body(doc,
         "然而，固态体系的自愈能力有限：当缺陷密度过高或界面已分层时，漏电会持续增大并可能发展为短路。与液态铝电解电容依靠电解液持续供氧、对介质进行“再形成（reforming）”的强自愈不同[3],[87]，"
         "SAPC 缺乏持续供氧通道，其漏电修复主要依赖聚合物高阻化的“隔离”机制，因而漏电型失效的可逆裕度较小。这一差异是 SAPC 漏电可靠性需重点关注的根本原因。")

    heading(doc, "2.5.4  制造缺陷与杂质", level=3)
    body(doc,
         "工艺洁净度与一致性对 SAPC 的漏电可靠性有重要影响。CALCE 在个别批次样品中发现源自制造过程的金属（铁）颗粒嵌入介质层、形成高漏电的“新失效机理”，此前文献未有报道[9]，"
         "提示原材料与产线污染可显著抬高 LC 并诱发早期失效。除金属颗粒外，蚀刻/化成不均、聚合物填充不完全、石墨/银浆界面缺陷与封装密封不良等，都会在器件中引入“弱点”，"
         "成为早期失效（婴儿期，见图—2.6.3）的根源。加电老化与筛选正是为剔除这类弱点而设[50],[75]。"
         "从材料源头看，国内对阳极/烧结铝箔氧化膜微结构的研究[45],[46]，为降低介质初始缺陷密度、提升一致性提供了途径，间接改善漏电可靠性。")

    heading(doc, "2.5.5  多机理耦合与失效链", level=3)
    body(doc,
         "上述机理在实际服役中并非孤立，而是耦合演化、相互促进的。以湿热+偏压+纹波的典型工况为例，可梳理出如下失效链："
         "水分扩散（式2-9）→聚合物吸湿溶胀与去掺杂/氧化（式2-8）+界面腐蚀分层→体电阻与接触电阻同时上升（式2-3）→ESR 上升→纹波焦耳热增加（式2-6）→局部温升加速聚合物退化与界面分层（正反馈）；"
         "与此并行，界面腐蚀与介质缺陷→漏电通道（式2-10）→若自愈不足则 LC 持续增大→趋于短路。图17以鱼骨（Ishikawa）图归纳驱动 SAPC 退化的材料、环境、电、工艺、界面与机械六类因素。")
    add_figure(doc, "fig_fishbone.png", 14,
               "SAPC 退化驱动因素的因果（鱼骨）图：材料/环境/电/工艺/界面/机械",
               "来源：作者综合[9]–[28],[42],[51],[52],[81]归纳绘制（原创图）。")
    body(doc,
         "这一耦合特征意味着：单应力试验得到的机理与速率，未必能简单线性叠加到多应力工况；正确的做法是以竞争失效框架（2.6.7）把并行失效路径统一建模。"
         "然而，目前面向 SAPC、能定量刻画多机理竞争与耦合反馈的机理模型仍属空白，这是机理研究向寿命预测转化的主要瓶颈。")

    heading(doc, "2.5.6  失效分析方法学", level=3)
    body(doc,
         "机理研究依赖系统的失效分析（FA）。SAPC 的 FA 通常遵循“电学表征→无损检测→解剖/截面→显微形貌→成分分析→化学表征→机理建模”的递进流程（图18）："
         "电学上以 C/ESR/LC 与阻抗谱（EIS）定位退化类型；无损上以 X 射线与 C 扫描声学显微镜（C-SAM）探测分层与空洞；"
         "解剖后以 SEM/TEM 观察聚合物/界面/介质形貌，以 EDS/XPS 分析成分与掺杂态（如 PEDOT 氧化态、对阴离子分布），以 FTIR/Raman 表征聚合物化学键与降解产物[23],[40],[41]。"
         "其中，电化学阻抗谱（EIS）兼具无损与机理诊断能力：Nyquist 谱中高频实轴截距对应 ESR、界面弧的增大反映接触/界面退化，是连接器件参数与界面机理的有力工具（图19）[2]。")
    add_figure(doc, "fig_fa_workflow.png", 15,
               "SAPC 失效分析工作流（从无损电学到机理建模）",
               "来源：作者综合[23],[40],[41]与通用 FA 实践绘制（原创流程图）。")
    add_figure(doc, "fig_nyquist.png", 16,
               "EIS（Nyquist）谱随老化的演化：ESR 实轴截距右移、界面弧增大（示意）",
               "来源：作者据电容器阻抗诊断原理[2]绘制（原创概念图，非实测数据）。")
    add_table(doc, 6, "SAPC 常用失效分析技术及其作用",
              ["技术", "类别", "主要获取信息", "在 SAPC 机理研究中的作用", "文献"],
              [["C/ESR/LC、阻抗谱(EIS)", "电学/无损", "参数退化、ESR、界面弧", "定位退化类型、区分体/界面贡献", "[2],[80]"],
               ["X 射线 / C-SAM", "无损", "内部空洞、分层、裂纹", "探测界面分层与焊点缺陷", "[81]"],
               ["SEM / TEM", "形貌", "聚合物/界面/介质微观形貌", "观察晶粒、分层、氧化膜缺陷", "[9],[10],[45]"],
               ["EDS / XPS", "成分", "元素分布、PEDOT 氧化态", "识别杂质(Fe)、掺杂/去掺杂", "[9],[92]"],
               ["FTIR / Raman", "化学", "化学键、降解产物、掺杂", "表征氧化/去掺杂与电解质残留", "[23],[40]"]],
              widths=[3.0, 1.6, 3.6, 4.0, 1.6], fs=8.8,
              source_cn="注：综合自[2],[9],[10],[23],[40],[41],[45],[80],[81],[92]。")
    body(doc,
         "小结：SAPC 失效机理以“聚合物本征退化—界面分层—氧化膜损伤/自愈”三链为主、叠加工艺缺陷与多机理耦合；"
         "其中界面退化是各失效模式的共同枢纽，自愈能力有限是漏电失效裕度小的根本原因。机理认识已较丰富，但向器件级寿命模型的定量映射仍是瓶颈，引出下一节的建模评述。")



# ================= 2.6 可靠性评估与建模方法（上） =================
def s_model_a(doc):
    heading(doc, "2.6  可靠性评估与建模方法研究现状", level=2)
    body(doc,
         "围绕 SAPC/铝电解电容的可靠性评估，方法可分为统计/经验、退化随机过程、失效物理（PoF）与数据驱动四大类（图21），它们并非互斥，近年呈深度融合趋势[1],[35]–[39],[71]–[84]。"
         "本节先介绍加速寿命试验与标准，再依次评述经验模型、寿命分布与统计推断、退化随机过程、PoF 模型、数据驱动/PHM、竞争失效与不确定性量化，并以对比表给出适用边界。")
    add_figure(doc, "fig_model_map.png", 17,
               "可靠性建模方法图谱：统计/经验、失效物理(PoF)与数据驱动/PHM",
               "来源：作者综合[1],[29]–[39],[71]–[84]绘制（原创图）。")

    heading(doc, "2.6.1  加速寿命试验与相关标准", level=3)
    body(doc,
         "加速寿命试验（ALT）通过提高温度、湿度、电压、纹波或温度循环等应力，在可接受时间内激发与使用条件相同的失效机理，再借寿命模型外推到使用条件。"
         "对湿热敏感的 SAPC，温-湿-偏（THB，典型 85°C/85%RH）与高加速温湿（HAST，如 130°C/85%RH）是常用方案；高温耐久（105/125°C）、高温存储与温度循环用于评价热与热-机械失效（图22）。"
         "相应标准包括 JEDEC JESD22-A101（稳态温湿偏）、JESD22-A110（HAST），以及器件通用规范 IEC 60384-1 与车规 AEC-Q200[31]–[34]。表7汇总主要加速试验类型、典型条件、目标失效机理与对应标准。")
    add_figure(doc, "fig_test_map.png", 18,
               "加速试验条件图（温度—湿度平面）与典型试验点（THB/HAST/高温耐久/使用点）",
               "来源：作者据标准[31]–[34]与文献[9],[10]绘制（原创图，使用点为示意）。")
    add_table(doc, 7, "SAPC 常用加速寿命试验与相关标准",
              ["试验类型", "典型条件", "目标失效机理", "对应标准/文献"],
              [["稳态温湿偏 THB", "85°C/85%RH + 额定偏压", "湿热：去掺杂、界面腐蚀/分层", "JESD22-A101 [31];[9],[10]"],
               ["高加速温湿 HAST", "130°C/85%RH（加压）", "加速湿热（缩短周期）", "JESD22-A110 [32];[63]"],
               ["高温耐久/存储", "105 / 125°C", "聚合物热氧老化、ESR 上升", "IEC 60384-1 [33];[13],[42]"],
               ["温度循环", "−55~+125°C 循环", "CTE 失配、界面分层、焊点疲劳", "AEC-Q200 [34];[81],[82]"],
               ["浪涌/阶梯应力", "上电浪涌、SSST", "场致击穿、上电失效、自愈", "[14],[75]"],
               ["纹波/自热耐久", "额定纹波 + 高温", "热-电耦合、ESR—温升正反馈", "[54],[55],[85]"]],
              widths=[2.6, 3.2, 4.6, 2.6], fs=8.8,
              source_cn="注：综合自标准[31]–[34]与文献[9],[10],[13],[14],[42],[54],[55],[63],[75],[81],[82],[85]。")

    heading(doc, "2.6.2  经验/统计加速模型", level=3)
    body(doc,
         "经验模型以应力—寿命的解析关系刻画加速效应。温度对反应速率的加速可由 Arrhenius 关系给出，其加速因子为：")
    equation(doc, "AF_T = exp[ (Eₐ/k_B) · ( 1/T_use − 1/T_test ) ]", "2-11")
    body(doc,
         "对液态铝电解电容，工程上常用“10°C 法则”近似（温度每升高 10°C，寿命约减半），等价于把式(2-11)在使用温区线性化[53],[54],[85]：")
    equation(doc, "L = L₀ · 2^( (T₀ − Tₐ) / 10 )", "2-12")
    body(doc,
         "需强调，10°C 法则源于液态电解液蒸发机理，直接套用于以聚合物退化为主的 SAPC 并不严格；这是现有寿命外推的一个常见误区。"
         "对湿热主导的失效，Peck 模型在 Arrhenius 基础上引入湿度因子，是 THB/HAST 数据外推的经典形式[29],[30]：")
    equation(doc, "t_f = A · (RH)^(−n) · exp( Eₐ / k_B T ) ;   AF = (RH_test/RH_use)^n · exp[(Eₐ/k_B)(1/T_use − 1/T_test)]", "2-13")
    body(doc,
         "文献中湿度指数 n 多取约 2.5–3、激活能 Eₐ 多在约 0.7–0.9 eV 量级（具体值依失效机理与材料体系而定，需由多应力试验标定）[29],[30]。"
         "当湿度敏感性随温度变化、或需同时表达温度与湿度交互时，可采用广义 Eyring 形式：")
    equation(doc, "t_f = A · T^(−b) · exp( Eₐ / k_B T ) · exp[ ( C + D / T ) · f(RH) ]", "2-14")
    body(doc,
         "CALCE 对聚合物铝电容正是采用 85°C/85%RH 与 110°C/85%RH 双条件以分离温度效应并建立寿命模型[9],[10]；厂商寿命计算工具亦多以 Arrhenius/纹波自热模型为内核[85]。"
         "图23给出 Arrhenius–Peck 寿命模型的概念示意：在 ln(寿命)–1/T 平面上，不同湿度对应一组近平行直线，湿度升高使直线整体下移（寿命缩短）。"
         "经验模型的优点是简单、工程通用，局限在于参数需大量数据标定、且难以反映聚合物多机理耦合的物理本质。")
    add_figure(doc, "fig_arrhenius_peck.png", 19,
               "Arrhenius–Peck 寿命模型：等温度线随湿度平移（示意）",
               "来源：作者据 Peck/THB 模型[29],[30]绘制的概念图（原创图，非实测数据）。")

    heading(doc, "2.6.3  寿命分布与统计推断", level=3)
    body(doc,
         "失效时间的分散性需用概率分布刻画。Weibull 分布因能统一描述早期、随机与磨损型失效而被广泛采用，其累积失效概率与可靠度为：")
    equation(doc, "F(t) = 1 − exp[ −(t/η)^β ] ,   R(t) = exp[ −(t/η)^β ] ,   h(t) = (β/η)(t/η)^(β−1)", "2-15")
    body(doc,
         "式中 η 为特征寿命、β 为形状参数：β<1 表征早期失效（递减风险）、β≈1 表征随机失效（恒定风险）、β>1 表征磨损型失效（递增风险），三者拼接即“浴盆曲线”（图24）。"
         "对数正态分布则常用于刻画由乘性损伤累积（如疲劳、腐蚀）主导的失效时间[82]。参数估计多采用极大似然（MLE）或概率作图（图25），并需正确处理截尾（censoring）数据；"
         "在聚合物钽电容中，击穿电压 V_cr 相对额定电压 V_R 被报道服从 Weibull 分布（示例形状参数 β≈5）[57]，可靠性评估常以“高电场+温度”加速获得失效时间后拟合外推[58]。")
    add_figure(doc, "fig_bathtub.png", 20,
               "浴盆曲线与 Weibull 形状参数区段（早期/随机/磨损）",
               "来源：作者据可靠性理论[3],[94]绘制（原创概念图）。")
    add_figure(doc, "fig_weibull.png", 21,
               "Weibull 概率作图（不同形状参数 β）示意",
               "来源：作者绘制的方法示意图（原创图）。")
    body(doc,
         "寿命分布方法的优点是成熟、标准化，能给出失效概率与置信区间；局限在于需要较充分的失效样本，且仅描述“失效时间”而不利用退化过程的中间信息——"
         "这正是退化建模（2.6.4）试图弥补的：通过对 ESR/LC 等可测退化量的连续观测，即使在尚无失效发生时也能推断寿命。")

    heading(doc, "2.6.4  退化随机过程模型", level=3)
    body(doc,
         "退化建模以可观测健康指标（如 ESR/ESR₀）的演化轨迹推断剩余寿命，特别适合 SAPC 这类“退化型、磨损主导、突发失效较少”的器件。三类随机过程应用最广："
         "Wiener 过程适于非单调（可上下波动）的退化，其退化量与首达时（first-passage time）分布为：")
    equation(doc, "X(t) = x₀ + μ·t + σ_B·B(t) ;   T = inf{ t: X(t) ≥ D } ~ Inverse-Gaussian", "2-16")
    body(doc,
         "Gamma 过程适于严格单调累积的退化（如腐蚀、磨损、不可逆氧化），其独立增量服从 Gamma 分布：")
    equation(doc, "ΔX ~ Gamma( α·Δt, β ) ,   E[X(t)] = α t / β ,   Var[X(t)] = α t / β²", "2-17")
    body(doc,
         "由首达失效阈值 D 可导出剩余寿命（RUL）分布，对 Wiener 过程其首达时近似服从逆高斯（Inverse-Gaussian）分布：")
    equation(doc, "f_RUL(ℓ) = sqrt( λ / (2π ℓ³) ) · exp[ −λ (ℓ − ν)² / (2 ν² ℓ) ]", "2-18")
    body(doc,
         "图26左给出 Wiener（非单调）与 Gamma（单调）退化样本轨迹及失效阈值，右给出由首达时得到的 RUL 概率密度。"
         "研究表明，对电容器这类不可逆退化，Gamma 过程的单调性常更符合物理实际，可得到更稳健的 RUL[73]；而当测量噪声不可忽略时，含测量误差的 Wiener 模型更合适。"
         "针对参数估计，基于共轭先验的在线贝叶斯方法可随监测数据递推更新 Gamma 过程参数并给出 RUL 后验[74]；考虑两阶段/多源变异（时间、个体、测量）的非线性退化模型进一步提升了异质总体下的预测精度[73]。表8对三类退化随机过程进行对比。")
    add_figure(doc, "fig_stochastic.png", 22,
               "退化随机过程：Wiener/Gamma 样本轨迹与失效阈值（左）及首达 RUL 分布（右）",
               "来源：作者据随机过程退化建模[73],[74]绘制（原创概念图，非实测数据）。")
    add_table(doc, 8, "三类退化随机过程模型对比",
              ["模型", "增量性质", "适用退化", "RUL 分布", "优点 / 局限", "文献"],
              [["Wiener 过程", "高斯增量、可非单调", "可逆波动 + 漂移", "逆高斯（首达时）", "可含测量误差；不保证单调", "[73]"],
               ["Gamma 过程", "独立正增量、单调", "不可逆累积（氧化/腐蚀）", "由阈值首达导出", "物理贴切、稳健；参数估计较难", "[73],[74]"],
               ["逆高斯过程", "正增量、灵活", "单调且方差可调", "解析 RUL", "灵活；解释性弱于 Gamma", "[73]"]],
              widths=[2.4, 2.8, 3.0, 2.4, 3.4, 1.4], fs=8.6,
              source_cn="注：综合自[73],[74]与统计退化建模一般理论；针对 SAPC 的退化过程建模公开数据仍有限。")



# ================= 2.6 可靠性评估与建模方法（下） =================
def s_model_b(doc):
    heading(doc, "2.6.5  失效物理（PoF）模型", level=3)
    body(doc,
         "失效物理（Physics-of-Failure, PoF）模型以失效机理的物理化学动力学为基础，建立应力—机理—参数—寿命的因果链，相比经验模型具有更强的外推与跨工况迁移能力[1],[3],[94]。"
         "对 SAPC，PoF 建模的核心思路是：以聚合物电导动力学（式2-8）与水分扩散（式2-9）为内层过程，经 ESR 分解（式2-3）映射到器件级 ESR(t)，"
         "并以漏电场致模型（式2-10）描述 LC(t)，最终以失效判据（如 ESR=2×ESR₀）确定寿命。"
         "温度、湿度、电压、纹波等外部应力通过 Arrhenius（式2-5/2-11）、Peck（式2-13）等关系进入各内层过程的速率常数，从而把多应力工况统一到一个物理框架内。")
    body(doc,
         "PoF 思路在相关器件上已有成功实践：液态铝电解电容以电解液蒸发动力学+自热模型建立寿命预测，并被厂商寿命计算工具采用[53],[54],[85]；"
         "NASA/CALCE 对电解电容则发展了基于电应力/热过应力加速老化的模型化预测方法（model-based prognostics），以退化状态方程驱动寿命估计[71],[72]。"
         "对 SAPC，PoF 的难点在于“多机理耦合反馈”（2.5.5）尚缺乏经实验标定的定量本构，且器件级长周期数据稀缺[15],[16]；"
         "因此，发展面向 SAPC、以聚合物电导动力学贯通器件 ESR 寿命、并能纳入湿-热-电耦合的 PoF 模型，是本文的重点研究方向之一（见 2.10）。")

    heading(doc, "2.6.6  数据驱动与 PHM 方法", level=3)
    body(doc,
         "当机理复杂、解析模型难以建立而监测数据较充分时，数据驱动方法成为有力补充。其谱系包括："
         "①滤波类——粒子滤波/扩展卡尔曼滤波，将退化状态方程与观测融合、在线估计状态并外推 RUL，已用于电解电容热过应力下的退化跟踪[36],[72]；"
         "②机器学习/深度学习——支持向量回归、随机森林、以及 LSTM/GRU 等循环网络与注意力模型，从历史退化序列学习映射并预测 RUL[37],[38]；"
         "③集成与混合——多模型集成以降低方差、提升鲁棒性[35],[39]。统计数据驱动 RUL 方法已有系统综述[93]，PHM 体系亦有经典专著支撑[94]。"
         "数据驱动方法的优点是无需精确机理、能处理高维非线性；局限是依赖大量代表性数据、外推与可解释性较弱、对分布漂移敏感。")
    body(doc,
         "为兼顾物理可解释性与数据拟合能力，物理-数据融合成为前沿方向。物理信息神经网络（PINN）将控制方程/退化动力学作为约束嵌入网络损失，"
         "在小样本下提升外推能力与物理一致性[83]；混合 PINN 已用于锂离子电池的建模与寿命预测，其“物理项+数据项”范式可迁移至电容器退化预测[84]。"
         "对 SAPC，PINN/混合模型有望以式(2-8)–(2-10)等退化动力学为物理先验、以 ESR/LC 监测序列为数据驱动，缓解“长周期数据稀缺”与“纯数据外推不可靠”的双重困难，是颇具潜力但尚待开展的方向。表9对主要数据驱动/融合方法进行对比。")
    add_table(doc, 9, "面向电容器 RUL 的数据驱动与物理-数据融合方法对比",
              ["方法", "代表技术", "数据需求", "可解释/外推", "在(类)电容器上的应用", "文献"],
              [["滤波类", "粒子滤波、EKF", "中（需状态方程）", "较好/中", "电解电容热过应力退化跟踪", "[36],[72]"],
               ["机器学习", "SVR、随机森林", "中—大", "中/弱", "退化序列回归预测", "[37],[39]"],
               ["深度学习", "LSTM/GRU、注意力", "大", "弱/弱", "长序列 RUL 预测", "[38]"],
               ["集成/混合", "多模型集成", "大", "中/中", "降方差、提鲁棒", "[35],[39]"],
               ["物理-数据融合", "PINN、混合模型", "中（物理约束降需求）", "好/较好", "电池/器件建模(可迁移)", "[83],[84]"]],
              widths=[2.0, 2.6, 2.6, 2.2, 3.6, 1.6], fs=8.6,
              source_cn="注：综合自[35]–[39],[72],[83],[84],[93],[94]；面向 SAPC 的公开数据驱动研究仍较少，多为可迁移方法。")

    heading(doc, "2.6.7  竞争失效与系统可靠性", level=3)
    body(doc,
         "如 2.5.5 所述，SAPC 同时存在 ESR 上升、漏电增大与界面/焊点失效等多条并行失效路径。在竞争失效（competing risk）框架下，若各路径相互独立，则系统可靠度为各路径可靠度之积：")
    equation(doc, "R_sys(t) = ∏_i R_i(t) ,   器件失效 = 任一路径首先到达其失效判据", "2-19")
    body(doc,
         "图27给出 ESR、漏电与界面分层三条路径及系统可靠度的关系：系统寿命由最先到达阈值的路径主导，且各路径权重随应力条件而变（高湿下漏电/界面路径权重上升、高温下 ESR 路径主导）。"
         "竞争失效建模可与退化随机过程（2.6.4）结合（多元退化/多阈值），也可与 Weibull 混合分布结合；其难点在于路径间的相关性（非独立竞争）与共因失效，"
         "这要求把 2.5.5 的耦合反馈纳入联合模型。目前面向 SAPC 的竞争失效定量研究尚不多见，是机理与寿命预测之间的关键桥梁。")
    add_figure(doc, "fig_competing.png", 23,
               "竞争失效：系统可靠度为各独立失效路径可靠度之积（示意）",
               "来源：作者据竞争失效理论[3]绘制（原创概念图，非实测数据）。")

    heading(doc, "2.6.8  不确定性量化与贝叶斯方法", level=3)
    body(doc,
         "可靠性预测必须给出不确定性，否则难以支撑维修决策与安全裕度设计。不确定性来源包括个体差异（unit-to-unit）、时间随机性（temporal）与测量误差（measurement）三类[73]。"
         "贝叶斯方法以先验分布表达已有知识、以监测数据更新后验，天然适合在线、小样本与异质总体场景：")
    equation(doc, "p(θ | D) ∝ p(D | θ) · p(θ) ;   p(RUL | D) = ∫ p(RUL | θ) · p(θ | D) dθ", "2-20")
    body(doc,
         "基于共轭先验的 Gamma 过程在线贝叶斯方法可解析或半解析地递推更新参数并给出 RUL 后验，兼顾计算效率与不确定性表达[74]；"
         "粒子滤波则以蒙特卡洛粒子近似后验，适合非线性/非高斯退化[36],[72]。在多源变异并存时，分层贝叶斯与考虑三源变异的两阶段非线性模型能更真实地刻画分散性[73]。"
         "对 SAPC，结合“物理先验（PoF 动力学）+ 贝叶斯更新 + 在线监测”的框架，有望在长周期数据稀缺条件下给出带置信区间的 RUL，这与本文的研究目标高度契合。")
    body(doc,
         "小结：SAPC 可靠性建模正从“经验/统计外推”走向“退化随机过程 + 失效物理 + 数据/物理融合 + 不确定性量化”的综合范式。"
         "经验模型通用但物理性弱、易误用（如 10°C 法则）；退化随机过程能利用中间信息但缺 SAPC 专用数据；PoF 物理性强但缺标定本构；数据驱动能力强但可解释/外推弱。"
         "四类方法的融合、以及面向 SAPC 多机理竞争的联合建模，是当前最值得突破的方向。")



# ================= 2.7 状态监测与寿命预测 =================
def s_monitor(doc):
    heading(doc, "2.7  状态监测与剩余寿命预测", level=2)
    body(doc,
         "状态监测（condition monitoring, CM）在线获取健康指标，是预测性维护与 RUL 预测的数据基础。Wang/Blaabjerg 等对功率电子用电容器的状态监测进行了系统综述[2]，"
         "指出电容量与 ESR 是两大核心健康指标，并梳理了各类在线辨识方法的原理与实现。")

    heading(doc, "2.7.1  健康指标与在线辨识", level=3)
    body(doc,
         "对 SAPC/铝电解电容，ESR 通常优于电容量作为健康指标：其退化单调、灵敏度高、且与失效物理（聚合物电导、界面接触）直接相关[2],[80]。"
         "在线辨识的基本思路是由可测电气量反演 ESR/C：在已知纹波电流的前提下，可由纹波电压与电流的同频分量估计阻抗，进而分离 ESR 与 C；"
         "对 Buck 等变换器，可从“电容视角”设计 ESR 估计方案并论证 ESR 作为监测参量的优越性[80]。短时最小二乘 Prony（STLSP）等方法可在少量样本下在线辨识 ESR 与 C，用于容错 LED 驱动等低功率系统[79]。"
         "电化学阻抗谱（EIS）则提供更丰富的机理信息：高频实轴截距给出 ESR、界面弧反映接触/界面退化（图19），是离线/准在线诊断的有力手段[2]。")

    heading(doc, "2.7.2  监测技术与电路实现", level=3)
    body(doc,
         "按实现方式，状态监测可分为：①基于电路的在线辨识——利用变换器自身的电压/电流传感与控制算法估计 ESR/C，硬件代价低、适合嵌入式部署[78],[80]；"
         "②专用激励/阻抗测量——注入小信号并测量阻抗谱，精度高但需附加电路；③数据智能方法——以学习模型从运行数据中提取健康特征，已用于三相逆变器 DC-link 电容的智能监测[78]。"
         "三相逆变器、LED 驱动、Buck 变换器等场景均已有相应的在线监测方案[78],[79],[80]。对 SAPC 而言，由于其 ESR 极低，对辨识精度与噪声抑制提出了更高要求，这是工程实现上的难点。")

    heading(doc, "2.7.3  RUL 预测方法与评价指标", level=3)
    body(doc,
         "RUL 预测在监测得到的退化轨迹基础上，结合退化模型（2.6.4）、PoF（2.6.5）或数据驱动（2.6.6）方法，外推至失效阈值并给出带不确定性的剩余寿命（图28）。"
         "评价 RUL 预测优劣的常用指标包括：均方根误差（RMSE）、平均绝对误差（MAE）、考虑“早预测优于晚预测”的非对称评分，以及收敛性（随监测推进预测应收敛于真值）与 α–λ 精度（预测落入真值 ±α 带的能力）等[93],[94]。"
         "在 SAPC 上，RUL 预测的挑战集中在：长周期退化数据稀缺、ESR 辨识噪声大、以及多机理竞争导致的退化非平稳——这些都指向“物理先验 + 在线贝叶斯更新”的融合路线（2.6.8）。")
    add_figure(doc, "fig_rul.png", 24,
               "RUL 预测：退化轨迹外推至失效阈值并给出不确定性带与 RUL 分布（示意）",
               "来源：作者据 PHM/RUL 一般框架[93],[94]绘制（原创概念图，非实测数据）。")
    add_table(doc, 10, "电容器状态监测方法对比",
              ["方法", "监测量", "实现方式", "精度/代价", "适用场景", "文献"],
              [["纹波电压/电流辨识", "ESR、C", "复用变换器传感", "中/低代价", "逆变器、Buck", "[2],[80]"],
               ["STLSP/参数辨识", "ESR、C", "在线算法", "中/低代价", "容错 LED 驱动", "[79]"],
               ["阻抗谱(EIS)", "ESR、界面弧", "小信号激励", "高/较高代价", "离线/准在线诊断", "[2]"],
               ["数据智能监测", "健康特征", "学习模型", "依数据/中代价", "三相逆变器 DC-link", "[78]"]],
              widths=[2.6, 2.0, 2.6, 2.4, 3.0, 1.4], fs=8.8,
              source_cn="注：综合自[2],[78],[79],[80]。")
    body(doc,
         "小结：ESR 是 SAPC 状态监测与 RUL 预测的核心健康指标，在线辨识与 EIS 提供了从工程实现到机理诊断的手段；"
         "但面向 SAPC 极低 ESR 的高精度辨识、以及多机理竞争下的稳健 RUL 预测，仍是开放问题。")


# ================= 2.8 应用领域与可靠性要求 =================
def s_app(doc):
    heading(doc, "2.8  典型应用领域与可靠性要求", level=2)
    body(doc,
         "SAPC 的可靠性要求高度依赖应用领域。本节简述汽车电子、航天/高可靠与消费/工业电源三类典型场景的要求与约束，以明确研究的工程牵引。")

    heading(doc, "2.8.1  汽车电子（AEC-Q200）", level=3)
    body(doc,
         "汽车电子要求元件在宽温（−55~+125/150°C）、强振动、温度循环与潮湿盐雾等严苛环境下长期可靠工作，无源元件须通过 AEC-Q200 认证[34]。"
         "SAPC 因低 ESR、抗振（固态电解质无晃动）与失效良性而适于车载 DC-DC、域控制器与电源去耦[5],[88],[89]；"
         "但其湿热敏感性要求在封装密封、降额与热设计上格外谨慎。降额对聚合物钽电容失效率的显著影响[65]提示，SAPC 在车规应用中同样需要充分的电压/温度降额与失效率评估。")

    heading(doc, "2.8.2  航天与高可靠（NASA NEPP）", level=3)
    body(doc,
         "航天应用对元件的筛选、批次一致性与失效模式有最严格要求。NASA NEPP 指出，叠层铝聚合物电容（APC）因更低 ESR、更轻、更小，有望替代片式钽电容，"
         "但其可靠性数据稀缺、已有文献多集中于湿度影响，为此 NASA 对其开展了专门的应力测试与航天适用性评估[15],[16]；"
         "并对聚合物钽电容研究了上电失效、浪涌阶梯应力（SSST）与干燥环境下的异常充电电流（ACC）等问题[75],[76],[77]。"
         "NPSL/NEPAG 的选用要求强调以 DPA、失效史与可靠性趋势为依据进行评估。航天场景对“纯高温长周期数据”与“突发失效裕度”的需求，恰是当前 SAPC 数据缺口最突出之处。")

    heading(doc, "2.8.3  消费与工业电源（DC-link / 去耦）", level=3)
    body(doc,
         "在消费电子（固态硬盘、主板供电）、工业电源与 LED 驱动等场景，SAPC 主要用于高频去耦、输出滤波与纹波吸收，强调低 ESR、高纹波能力与小型化[5],[89],[90]。"
         "在功率变换的 DC-link 应用中，电容器的失效机理、失效模式与寿命模型是系统可靠性设计的基础，并需结合任务剖面（mission profile）进行寿命评估与状态监测[1],[47],[78]。"
         "对电动汽车充电模块等场景，已有基于任务剖面的铝电解电容寿命预测与可靠性分析方法[47]，其热点温度计算与寿命模型的精度是预测准确性的关键，这一思路同样适用于 SAPC。"
         "表11概括三类应用的环境、关键要求与对 SAPC 的主要约束。")
    add_table(doc, 11, "SAPC 典型应用领域的可靠性要求与约束",
              ["应用领域", "典型环境", "关键可靠性要求", "对 SAPC 的主要约束", "文献"],
              [["汽车电子", "宽温、振动、温度循环、潮湿", "AEC-Q200、长寿命、低失效率", "湿热敏感、需降额与密封", "[34],[65],[88]"],
               ["航天/高可靠", "真空、辐射、热循环、严筛选", "批次一致性、突发失效裕度", "高温长周期数据稀缺、ACC", "[15],[16],[75]–[77]"],
               ["消费/工业电源", "高频纹波、自热、量产成本", "低 ESR、高纹波、小型化、成本", "极低 ESR 监测难、自热反馈", "[5],[47],[78],[89]"]],
              widths=[2.2, 3.2, 3.4, 3.2, 1.6], fs=8.8,
              source_cn="注：综合自[1],[5],[15],[16],[34],[47],[65],[75]–[78],[88],[89]。")



# ================= 2.9 国内外研究对比 =================
def s_compare(doc):
    heading(doc, "2.10  国内外研究对比与文献计量", level=2)
    body(doc,
         "从研究力量与侧重看，国际上以 CALCE（美国马里兰大学）、NASA NEPP，以及 KEMET、Murata、Panasonic、TDK、Nippon Chemi-Con 等厂商研究机构为代表，"
         "在器件级湿热可靠性、加速试验方法、失效分析与航天适用性评估方面积累深厚、数据系统[2],[9],[10],[12]–[16],[63],[75]–[77],[88],[89]；"
         "在 PEDOT 材料降解机理（热氧老化、吸湿、酸性、对阴离子稳定性）方面，欧洲与亚洲多所高校与研究组贡献了大量物理化学层面的工作[17],[18],[22],[24],[51],[52],[66]–[70],[92]。"
         "国内研究在阳极/烧结铝箔氧化膜材料、导电聚合物分散液与高可靠固态铝电容制备工艺方面持续推进[8],[45],[46],[50]，"
         "在退化建模、随机过程与 PHM 方法学（Wiener/Gamma 过程、贝叶斯、PINN 等）方面亦有较强积累[73],[74],[83]，但面向 SAPC 器件本体的系统性长周期、多应力可靠性实验数据仍相对有限。")
    body(doc,
         "从主题侧重看（图30），国际器件级研究高度集中于湿度（湿热）影响，对纯高温、热-电-机械耦合的系统数据相对薄弱[15],[16]；"
         "材料机理研究虽深入，但与器件级寿命模型的定量贯通不足；建模与 PHM 方法虽成熟，却普遍缺乏 SAPC 专用退化数据集来标定与验证。"
         "这种“材料机理深、器件数据浅、方法工具全、专用数据缺”的格局，是把握 SAPC 可靠性研究现状的关键判断。表12从多维度给出国内外研究的对比。")
    add_figure(doc, "fig_gap_map.png", 25,
               "SAPC 可靠性研究的主题热度与研究缺口示意",
               "来源：作者综合全章文献归纳绘制（原创图，热度为定性示意）。")
    add_table(doc, 12, "国内外 SAPC（及相关器件）可靠性研究对比",
              ["维度", "国际（CALCE/NASA/厂商/高校）", "国内（高校/院所/企业）", "共性缺口"],
              [["器件级湿热数据", "系统、充分（85/85、HAST）", "逐步开展、相对有限", "纯高温长周期数据均不足"],
               ["材料降解机理", "深入（PEDOT 热/氧/湿/酸）", "材料与工艺并重、有特色", "机理与器件寿命定量贯通不足"],
               ["加速试验/标准", "成熟、与标准结合紧密", "跟进标准、积累中", "缺 SAPC 专用多应力规程"],
               ["建模/PHM 方法", "完整（统计/PoF/数据驱动）", "随机过程/PINN 较强", "缺 SAPC 专用数据集标定"],
               ["失效安全性评估", "充分（过流良性、SSST）", "关注、数据较少", "多机理竞争定量化不足"]],
              widths=[2.6, 4.6, 4.2, 3.0], fs=8.8,
              source_cn="注：定性对比综合自本章全部文献[1]–[94]，意在反映总体格局而非穷举具体团队。")


# ================= 2.10 不足与切入点 =================
def s_gap(doc):
    heading(doc, "2.11  现有研究的不足与本文切入点", level=2)
    body(doc, "综合 2.2–2.10，现有 SAPC 可靠性研究主要存在以下五点不足：")
    bullet(doc, "（1）应力覆盖不均衡：器件级研究高度集中于湿热（85/85、HAST），对纯高温、热-电-机械耦合及多应力交互的系统数据明显不足[9],[10],[15],[16]，"
                "导致高温与耦合工况下的寿命外推缺乏实测支撑。")
    bullet(doc, "（2）机理—模型脱节：PEDOT 本征退化、界面分层与氧化膜自愈等机理已较清晰，但缺乏把“聚合物电导动力学（式2-8）—界面接触—器件 ESR/LC”定量贯通的失效物理模型[17],[25],[42]，"
                "机理认识难以转化为可外推的寿命预测。")
    bullet(doc, "（3）多机理竞争未定量：实际服役为湿-热-电-机械多机理耦合与竞争（2.5.5、2.6.7），现有工作多为单应力、单机理的定性描述，缺乏经实验标定的竞争失效联合模型。")
    bullet(doc, "（4）经验模型易误用：以液态电解液蒸发为基础的 10°C 法则等被不加区分地套用于聚合物体系[53],[54]，"
                "而 Peck/Eyring 等湿热模型的参数（n、Eₐ）在 SAPC 上缺乏统一标定，外推可信度存疑。")
    bullet(doc, "（5）专用数据与监测不足：缺乏面向 SAPC 的公开退化数据集与高精度（极低 ESR）在线监测方案，"
                "使退化随机过程、数据驱动与 PINN 等先进方法难以在 SAPC 上充分标定与验证[73],[74],[83],[93]。")
    body(doc, "针对上述不足，本文拟从以下方面切入（与后续各章对应）：")
    bullet(doc, "①多应力加速试验体系：设计覆盖湿热、纯高温、热-电（纹波+偏压）与温度循环的多应力加速试验，"
                "以 ESR/C/LC 与 EIS 为多参数监测，构建 SAPC 专用退化数据集，补强高温与耦合工况的数据缺口（对应 2.4、2.6.1）。")
    bullet(doc, "②机理贯通的失效物理模型：以聚合物电导动力学（式2-8）与水分扩散（式2-9）为内层、经 ESR 分解（式2-3）与漏电场致模型（式2-10）映射到器件级，"
                "建立可纳入湿-热-电耦合的 PoF 寿命模型（对应 2.5、2.6.5）。")
    bullet(doc, "③竞争失效联合建模：在退化随机过程（Gamma/Wiener）与竞争失效框架下，把 ESR、漏电与界面/焊点路径统一建模，并刻画路径相关性（对应 2.6.4、2.6.7）。")
    bullet(doc, "④物理-数据融合的 RUL 预测：以 PoF 动力学为物理先验、以监测序列为数据、以贝叶斯在线更新给出带置信区间的 RUL，缓解长周期数据稀缺（对应 2.6.6、2.6.8、2.7）。")
    bullet(doc, "⑤面向应用的验证：结合汽车/航天/电源任务剖面，验证模型在降额与实际工况下的预测精度与工程可用性（对应 2.8）。")


# ================= 本章小结 =================
def s_summary(doc):
    heading(doc, "本章小结", level=2)
    body(doc,
         "本章按“器件—材料—失效模式—失效机理—可靠性建模—状态监测—应用需求”的主线，系统评述了 SAPC 可靠性研究的国内外现状。"
         "在器件与材料层面，阐明了 SAPC 以蚀刻铝阳极/Al₂O₃ 介质提供高体积电容、以导电聚合物（PEDOT）阴极提供低 ESR 与高频性能的原理，"
         "并基于颗粒金属/VRH 输运理论揭示了其电导对热、氧、湿、酸的敏感性。")
    body(doc,
         "在失效模式与机理层面，归纳了湿热、高温、热-电耦合与热-机械四类失效模式（以 ESR 上升、漏电增大为主、电容量相对稳定），"
         "并阐明了聚合物本征退化（去掺杂/氧化/晶粒收缩）、水分扩散与界面分层、氧化膜损伤与有限自愈、工艺缺陷与多机理耦合等关键机理及其失效链。"
         "在建模与监测层面，系统比较了经验/统计、退化随机过程、失效物理与数据驱动/物理-数据融合四类方法的数学形式、适用边界与局限，"
         "并评述了以 ESR 为核心健康指标的状态监测与 RUL 预测，以及汽车、航天与电源等应用的可靠性要求。")
    body(doc,
         "在此基础上，本章凝练出现有研究在“应力覆盖、机理-模型贯通、多机理竞争、经验模型误用、专用数据与监测”五个方面的不足，并据此提出了本文的五点切入与后续章节安排。"
         "总体而言，SAPC 可靠性研究呈“材料机理深、器件数据浅、方法工具全、专用数据缺”的格局，"
         "发展面向 SAPC、机理贯通且能纳入多机理竞争与不确定性量化的可靠性模型与预测方法，既是学术前沿，也是工程急需，构成本文研究的出发点。")



# ================= 参考文献 =================
def s_references(doc):
    page_break(doc)
    heading(doc, "参考文献", level=1)
    body(doc,
         "说明：以下文献均经检索后纳入，可经所附链接溯源。凡标注“[DOI待核验]”者表示该条目暂未获得正式 DOI（如部分会议论文、技术报告与厂商资料）或 DOI 尚需核验，"
         "提交前请在 Web of Science / Scopus / IEEE Xplore 及出版商页面逐条复核，并按目标规范（GB/T 7714 或 IEEE）统一著录。", size=10)
    for ref in REFERENCES:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = 1.25
        pf.space_after = Pt(3)
        pf.left_indent = Pt(24)
        pf.first_line_indent = Pt(-24)
        run = p.add_run(format_ieee(ref))
        set_cn(run, size=10)


# ================= 附录 =================
def s_appendix(doc):
    page_break(doc)
    heading(doc, "附录 A  建议引用图表索引（需引用原图者）", level=1)
    body(doc,
         "对需引自原始论文的 SEM/TEM 形貌、XPS/EDS 成分、FTIR/Raman 谱、实测 I–V/C–V 及阻抗谱等图件，本文不直接嵌入受版权保护的原图，"
         "而在此给出可溯源的真实出处（含文献编号与 DOI/链接），供取得授权后引用。正文图1–图30 均为作者原创示意图，可直接使用。")
    add_table(doc, "A-1", "建议引用的原始图表及其出处",
              ["拟引用内容", "建议出处（文献编号）", "可获取信息", "DOI/链接见参考文献"],
              [["PEDOT 热氧老化电导下降曲线", "[17],[18]", "电导随时间/气氛变化", "[17],[18]"],
               ["聚合物钽电容高温存储 ESR/电阻率增长", "[42],[43]", "电阻率近指数增长", "[42],[43]"],
               ["85/85 THB 下 ESR/LC 退化与 FA 形貌", "[9],[10]", "ESR/LC 退化、界面/分层 SEM", "[9],[10]"],
               ["PEDOT:PSS 吸湿溶胀（光学厚度）", "[52]", "RH 升高的溶胀曲线", "[52]"],
               ["水分对 PEDOT 晶区影响（模拟）", "[51]", "晶区变小/无序", "[51]"],
               ["VRH 输运 lnσ–T^(−p) 拟合", "[70]", "跳跃温度/定域长度", "[70]"],
               ["PEDOT:PSS 层级结构与电导关联", "[69]", "PSS 壳/结晶/聚集", "[69]"],
               ["铝氧化膜-聚合物自愈/阻变", "[25]", "可逆击穿后导通", "[25]"],
               ["EIS Nyquist 谱随老化演化", "[2]", "ESR 截距/界面弧", "[2]"],
               ["过流良性失效（无燃爆）形貌", "[14]", "破坏性过流结果", "[14]"]],
              widths=[5.0, 2.6, 4.2, 2.2], fs=8.8,
              source_cn="注：所有出处均见参考文献[1]–[94]，请按授权与规范引用原图。")

    heading(doc, "附录 B  主要符号与缩略语表", level=1)
    add_table(doc, "B-1", "主要符号表",
              ["符号", "含义", "符号", "含义"],
              [["C / C₀", "电容量 / 初始电容量", "ESR", "等效串联电阻"],
               ["ESL", "等效串联电感", "LC", "漏电流"],
               ["|Z|, f₀", "阻抗模值、自谐振频率", "tanδ", "损耗角正切"],
               ["εr, d, A", "介电常数、氧化膜厚、有效面积", "V_f", "化成（阳极氧化）电压"],
               ["σ, σ₀", "电导率、初始电导率", "T₀, p", "VRH 特征温度、指数"],
               ["Eₐ, k_B", "激活能、玻尔兹曼常数", "AF", "加速因子"],
               ["η, β", "Weibull 特征寿命、形状参数", "h(t), R(t)", "风险率、可靠度"],
               ["μ, σ_B", "Wiener 漂移、扩散系数", "α, β(Γ)", "Gamma 形状、尺度"],
               ["D, C_w", "扩散系数、水分浓度", "β_PF", "Poole–Frenkel 系数"],
               ["N_f, Δε_p", "失效循环数、塑性应变幅", "RUL", "剩余使用寿命"]],
              widths=[2.2, 5.4, 2.0, 4.4], fs=8.8)
    add_table(doc, "B-2", "主要缩略语表",
              ["缩略语", "全称/含义", "缩略语", "全称/含义"],
              [["SAPC", "叠层铝固态(聚合物)电容器", "PEDOT", "聚3,4-乙撑二氧噻吩"],
               ["PSS", "聚苯乙烯磺酸", "PPy", "聚吡咯"],
               ["VRH", "变程跳跃输运", "ES-VRH", "Efros–Shklovskii VRH"],
               ["THB", "温-湿-偏试验", "HAST", "高加速温湿应力试验"],
               ["ALT", "加速寿命试验", "PoF", "失效物理"],
               ["PHM", "故障预测与健康管理", "RUL", "剩余使用寿命"],
               ["EIS", "电化学阻抗谱", "FA", "失效分析"],
               ["SEM/TEM", "扫描/透射电子显微镜", "XPS/EDS", "X射线光电子能谱/能谱"],
               ["FTIR", "傅里叶变换红外光谱", "C-SAM", "C扫描声学显微镜"],
               ["PINN", "物理信息神经网络", "AEC-Q200", "车规无源元件认证"]],
              widths=[2.2, 5.4, 2.2, 4.2], fs=8.8)

    heading(doc, "附录 C  加速试验标准与条件汇总", level=1)
    add_table(doc, "C-1", "相关标准与典型加速条件汇总",
              ["标准/规范", "名称/范围", "典型条件", "针对失效"],
              [["JESD22-A101", "稳态温湿偏(THB)", "85°C/85%RH+偏压", "湿热退化"],
               ["JESD22-A110", "高加速温湿(HAST)", "130°C/85%RH 加压", "加速湿热"],
               ["IEC 60384-1", "固定电容器通用规范", "耐久/高温存储 105/125°C", "热氧老化"],
               ["AEC-Q200", "车规无源元件应力认证", "温度循环 −55~+125°C 等", "热-机械、综合"],
               ["(SSST)", "浪涌阶梯应力试验", "阶梯升压至击穿", "上电/浪涌失效"]],
              widths=[2.6, 4.4, 4.0, 2.6], fs=8.8,
              source_cn="注：标准条款以官方最新版本为准[31]–[34]；SSST 为研究性试验[75]。")

    heading(doc, "附录 D  关键公式汇总", level=1)
    add_table(doc, "D-1", "本章关键公式一览",
              ["式号", "名称", "表达式（要点）", "用途"],
              [["2-1", "平行板电容", "C = ε₀εrA/d", "电容与介质/面积关系"],
               ["2-2", "阻抗模值", "|Z| = √(ESR²+(1/ωC−ωL)²)", "频率特性、f₀"],
               ["2-4", "VRH 电导", "σ=σ₀exp[−(T₀/T)^p]", "聚合物输运/老化"],
               ["2-5/2-11", "Arrhenius (率/AF)", "k=A·exp(−Eₐ/k_BT)", "温度加速"],
               ["2-12", "10°C 法则", "L=L₀·2^((T₀−Tₐ)/10)", "液态铝近似(慎用)"],
               ["2-13", "Peck (湿热)", "t_f=A·RH^(−n)·exp(Eₐ/k_BT)", "THB/HAST 外推"],
               ["2-14", "广义 Eyring", "含 T 与 RH 交互项", "温-湿耦合"],
               ["2-15", "Weibull", "F=1−exp[−(t/η)^β]", "寿命分布/浴盆"],
               ["2-8", "聚合物退化", "ESR(t)≈ESR₀·exp(t/τ)", "本征退化动力学"],
               ["2-9", "Fick 扩散", "∂C_w/∂t=D∇²C_w", "水分输运"],
               ["2-10", "Poole–Frenkel", "J∝E·exp[(β√E−φ)/k_BT]", "漏电场致"],
               ["2-7", "Coffin–Manson", "N_f=C·(Δε_p)^(−m)", "焊点/界面疲劳"],
               ["2-16", "Wiener 过程", "X=x₀+μt+σ_BB(t)", "非单调退化/RUL"],
               ["2-17", "Gamma 过程", "ΔX~Gamma(αΔt,β)", "单调退化/RUL"],
               ["2-18", "逆高斯 RUL", "首达时分布", "RUL 概率密度"],
               ["2-19", "竞争失效", "R_sys=∏R_i", "多路径系统可靠度"],
               ["2-20", "贝叶斯更新", "p(θ|D)∝p(D|θ)p(θ)", "在线 RUL/不确定性"]],
              widths=[1.4, 2.4, 4.6, 3.0], fs=8.6,
              source_cn="注：式号与正文一致；完整推导与参数标定见正文相应小节与参考文献。")
    body(doc,
         "（全文完。本章为修订版三，已在前稿基础上加深调研、系统扩充内容，"
         "共纳入可核验文献 94 条、原创图 30 幅、表格 31 张、关键公式 24 式（编号 2-1~2-24）。提交前请按目标规范统一著录并复核全部 DOI/卷期。）",
         size=10)


# ================= ORCHESTRATION =================
def set_page(doc):
    sec = doc.sections[0]
    sec.page_height = Cm(29.7)
    sec.page_width = Cm(21.0)
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)
    # page number in footer
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fldb = OxmlElement("w:fldChar"); fldb.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = "PAGE"
    flde = OxmlElement("w:fldChar"); flde.set(qn("w:fldCharType"), "end")
    run._r.append(fldb); run._r.append(instr); run._r.append(flde)
    set_cn(run, size=9)


def build():
    figs.build_all()
    doc = Document()
    set_page(doc)
    s_front(doc)
    s_intro(doc)
    ext_intro2(doc)
    ext_intro3(doc)
    s_device(doc)
    ext_device(doc)
    ext_device2(doc)
    ext_device3(doc)
    ext_device4(doc)
    ext_device5(doc)
    ext_device6(doc)
    s_material(doc)
    ext_material(doc)
    ext_material2(doc)
    ext_material3(doc)
    ext_material4(doc)
    ext_material5(doc)
    ext_material6(doc)
    ext_material7(doc)
    ext_material8(doc)
    ext_material9(doc)
    ext_material10(doc)
    s_modes(doc)
    ext_modes(doc)
    ext_modes2(doc)
    ext_modes3(doc)
    ext_modes4(doc)
    ext_modes5(doc)
    ext_modes6(doc)
    ext_modes7(doc)
    ext_modes8(doc)
    ext_modes9(doc)
    s_mech(doc)
    ext_mech(doc)
    ext_mech2(doc)
    ext_mech3(doc)
    ext_mech4(doc)
    ext_mech5(doc)
    ext_mech6(doc)
    ext_mech7(doc)
    ext_mech8(doc)
    ext_mech9(doc)
    ext_mech10(doc)
    s_model_a(doc)
    s_model_b(doc)
    ext_model(doc)
    ext_model2(doc)
    ext_model3(doc)
    ext_model4(doc)
    ext_model5(doc)
    ext_model6(doc)
    ext_model7(doc)
    ext_model8(doc)
    ext_model9(doc)
    ext_model10(doc)
    ext_model11(doc)
    s_monitor(doc)
    ext_monitor(doc)
    ext_monitor2(doc)
    ext_monitor3(doc)
    ext_monitor4(doc)
    ext_monitor5(doc)
    ext_monitor6(doc)
    ext_monitor7(doc)
    ext_monitor8(doc)
    ext_monitor9(doc)
    s_app(doc)
    ext_app(doc)
    ext_app2(doc)
    ext_app3(doc)
    ext_app4(doc)
    ext_app5(doc)
    ext_app6(doc)
    ext_app7(doc)
    ext_app8(doc)
    ext_app9(doc)
    s_cases(doc)
    ext_cases2(doc)
    s_compare(doc)
    ext_cases3(doc)
    s_gap(doc)
    s_questions(doc)
    s_outlook(doc)
    ext_outlook2(doc)
    ext_outlook3(doc)
    s_summary(doc)
    s_recap(doc)
    s_references(doc)
    s_appendix(doc)
    s_lists(doc)
    doc.save(OUT_DOCX)
    print("SAVED:", OUT_DOCX)


def s_lists(doc):
    page_break(doc)
    heading(doc, "附录 E  图目录", level=1)
    body(doc, "（页码请在 Word 中据实补全；下表按正文出现顺序列出全部图。）", size=10)
    for no, cap in FIG_LIST:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = 1.2
        pf.space_after = Pt(2)
        pf.left_indent = Pt(40)
        pf.first_line_indent = Pt(-40)
        r = p.add_run(f"图 {no}　{cap}")
        set_cn(r, size=10)
    heading(doc, "附录 F  表目录", level=1)
    body(doc, "（页码请在 Word 中据实补全；下表按正文出现顺序列出全部表。）", size=10)
    for no, cap in TAB_LIST:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = 1.2
        pf.space_after = Pt(2)
        pf.left_indent = Pt(40)
        pf.first_line_indent = Pt(-40)
        r = p.add_run(f"表 {no}　{cap}")
        set_cn(r, size=10)


# (main entry point is defined at the very end of this module, after all
#  extension subsection functions have been declared)



# ================= 2.2 扩展（电气参数、降额、混合型） =================
def ext_device(doc):
    heading(doc, "2.2.7  关键电气参数的温度/频率特性与降额", level=3)
    body(doc,
         "SAPC 的工程价值集中体现在其电气参数的稳定性上。与液态铝电解电容相比，SAPC 因不存在电解液蒸发与电导率的强温度依赖，"
         "其电容量随温度的变化更平缓、ESR 随频率的下降更早趋于低平台（图7）。这意味着 SAPC 在宽温区与高频段都能维持较好的滤波与去耦性能，"
         "尤其适合高频开关电源与处理器供电的瞬态响应需求[5],[61],[89]。然而，正是这种“出厂即优”的特性，使得任何由退化引起的 ESR 抬升都更易被监测识别（2.7），"
         "因为其初始基线低而稳定。")
    add_figure(doc, "fig_cv_temp.png", 26,
               "SAPC 与液态铝电解电容的电容—温度、ESR—频率特性对比（示意）",
               "来源：作者据[5],[61],[89]所述定性规律绘制（原创概念图，非实测数据）。")
    body(doc,
         "纹波电流额定是 SAPC 的重要规格。允许纹波电流由可耗散功率与 ESR 共同决定：在给定热阻与允许温升 ΔT 下，最大允许纹波电流近似为 "
         "I_ripple,max ≈ sqrt( ΔT / (ESR · R_th) )。可见 ESR 越低、热阻越小，纹波能力越强；这正是叠层固态结构（低 ESR、低 ESL、良好散热路径）的优势所在[54],[85],[88]。"
         "由于退化会同时抬升 ESR 与热阻（界面分层），纹波能力随寿命下降，设计时须留足裕度。")
    body(doc,
         "降额（derating）是保障可靠性的基本手段。电压降额通过降低介质电场抑制场致退化与击穿，温度降额通过降低反应速率延缓聚合物老化（图8）。"
         "对聚合物钽电容的研究表明，失效率对降额高度敏感，适当降额可显著降低失效率[65]；这一规律对 SAPC 同样适用，工程上常取约 50% 的电压降额作为设计点[34],[65]。"
         "需要强调，降额的定量效果依赖于具体的失效物理模型（如式2-10、式2-11），不应简单照搬其它器件的降额曲线。")
    add_figure(doc, "fig_derating.png", 27,
               "电压/温度降额对相对失效率的影响（示意）",
               "来源：作者据降额—失效率关系[34],[65]绘制（原创概念图，非实测数据）。")

    heading(doc, "2.2.8  混合型聚合物铝电容与器件选型权衡", level=3)
    body(doc,
         "混合型聚合物铝电容（hybrid polymer aluminum electrolytic capacitor）在同一器件中并用液态电解质与导电聚合物：聚合物提供低 ESR 与高纹波能力，"
         "液态电解质则保留对介质缺陷的持续供氧自愈能力，从而兼具低漏电、抗瞬态与较好的温度寿命特征，但其寿命仍呈现类似非固态电容的温度依赖[55],[56],[91]。"
         "这一“折中方案”在汽车电子等既要求低 ESR、又强调长寿命与鲁棒性的场景中颇受欢迎。")
    body(doc,
         "从选型权衡看，纯固态 SAPC 以最低 ESR、最佳高频性能与失效良性见长，但漏电自愈裕度小、对湿热敏感；混合型在自愈与温度寿命上更稳健、但 ESR 略高、含液态体系；"
         "液态铝电解电容成本最低、耐压最高，但 ESR 高、存在蒸发磨损失效。表13从可靠性视角总结三者的权衡，供后续研究与工程选型参考。"
         "需要指出，这种权衡本质上反映了“低 ESR（聚合物）”与“强自愈（液态供氧）”之间的物理取舍，是理解 SAPC 可靠性短板（漏电自愈不足）的关键背景。")
    add_table(doc, 13, "纯固态 SAPC、混合型与液态铝电解电容的可靠性权衡",
              ["维度", "纯固态 SAPC", "混合型聚合物铝", "液态铝电解"],
              [["ESR / 高频", "最低 / 最优", "低 / 优", "高 / 一般"],
               ["漏电自愈", "有限（聚合物隔离）", "强（液态供氧）", "强（液态供氧）"],
               ["温度寿命机制", "聚合物热氧老化", "兼具蒸发与聚合物退化", "电解液蒸发(10°C法则)"],
               ["湿热敏感性", "较高", "中", "中"],
               ["失效安全性", "良性（不燃爆）", "良性", "可能鼓胀/喷液"],
               ["成本/耐压", "中 / 中", "中 / 中", "低 / 高"],
               ["典型取舍", "性能优先、需密封降额", "性能与寿命折中", "成本/耐压优先"]],
              widths=[2.6, 3.4, 3.6, 3.2], fs=8.8,
              source_cn="注：综合自[53]–[56],[61],[65],[87]–[91]，定量参数以具体型号为准。")


# ================= 2.3 扩展（制备路线、电导证据、其它环境因素） =================
def ext_material(doc):
    heading(doc, "2.3.7  聚合物制备/填充路线对可靠性的影响", level=3)
    body(doc,
         "导电聚合物阴极的制备/填充方式直接影响阴极覆盖完整性、相分离结构与界面黏附，进而决定 ESR 初值与退化裕度。主流路线有二："
         "①原位化学/电化学聚合——单体（EDOT）与氧化剂在多孔阳极内反应生成 PEDOT，能较好填充深孔、获得保形接触，但对工艺窗口（氧化剂、温度、时间）敏感，残留氧化剂可能加速老化；"
         "②分散液浸渍—干燥——以 PEDOT:PSS 水分散液浸渍后干燥成膜，工艺简单、可控性好，但对深孔的填充与界面接触较依赖分散液配方与润湿性[6]–[8]。"
         "两类路线在“填充深度—接触质量—残留物—酸性”之间各有取舍，是器件一致性与湿热可靠性的“先天”来源。")
    body(doc,
         "在配方与后处理层面，二次掺杂（极性溶剂如 DMSO/EG、离子液体）、表面活性剂（如 Tween 80）与退火可重排相分离、减薄 PSS 壳、促进 PEDOT 结晶，从而提升电导并改善稳定性[20],[21],[66],[69]；"
         "去质子（中和 PSS 酸性）则能减弱酸性对铝介质与界面的侵蚀，对铝固态电容尤为重要[8],[22]。这些“材料级”手段与“器件级”封装/降额措施共同决定 SAPC 的最终可靠性，"
         "提示可靠性提升应是“材料—界面—封装—应用”协同优化，而非单点改进。")

    heading(doc, "2.3.8  电导—温度实验证据与活化能", level=3)
    body(doc,
         "PEDOT 体系电导对温度的依赖是其可靠性建模的微观基础。在较高温区，电导（或退化速率）常表现为热激活（Arrhenius）行为，可由不同温度下的电导/ESR 数据在 ln(速率)–1/T 平面拟合提取表观激活能 Eₐ（图13）；"
         "在低温区则更符合 VRH（式2-4）。Vitoratos 等[17]与气氛对比研究[18]给出了电导随时间下降、且空气气氛加速的实验证据；聚合物钽高温存储[42],[43]观察到电阻率近指数增长。"
         "这些证据共同支持式(2-8)的指数型退化近似，并表明表观 Eₐ 受氧分压、湿度与对阴离子稳定性调制，故须在目标气氛/湿度下标定，而非沿用文献缺省值。")
    add_figure(doc, "fig_activation.png", 28,
               "由多温度加速试验提取表观激活能 Eₐ（Arrhenius 作图，示意）",
               "来源：作者据 Arrhenius 方法[17],[42]绘制（原创概念图，数据为示意）。")
    body(doc,
         "需注意，表观激活能往往是多过程（去掺杂、氧化、晶粒收缩、界面退化）的“混合”结果，单一 Eₐ 仅在有限温区与机理不变的前提下成立；"
         "当温区跨越机理转变（如从 VRH 主导转为热激活主导）时，Arrhenius 直线会出现折点，外推须格外谨慎。这是经验加速模型在 SAPC 上易失准的重要原因之一（见 2.6.2、2.10）。")

    heading(doc, "2.3.9  UV、氧分压与其它环境因素", level=3)
    body(doc,
         "除热与湿外，氧分压与紫外（UV）也显著影响 PEDOT 稳定性。研究指出，UV 辐照会改变导电聚合物结构、降低电学性能，且不同对阴离子主导的薄膜其退化敏感因素不同[92]；"
         "在封装器件内部，UV 影响通常不显著，但氧分压（封装透氧性与内部残氧）是热氧老化速率的关键变量[18]。"
         "PEDOT:PSS 的强酸性还会在湿热下加剧对铝/氧化膜的腐蚀，形成“酸性—吸湿—腐蚀—去掺杂”的耦合退化[22],[24]。"
         "因此，封装的阻湿与阻氧能力、以及材料的去质子改性，构成抑制环境驱动退化的两条互补途径。综合 2.3 各节，可将影响 PEDOT 电导稳定性的因素及其作用机制归纳为表14。")
    add_table(doc, 14, "影响 PEDOT 阴极电导稳定性的主要因素及作用机制",
              ["因素", "作用机制", "对 ESR/LC 的影响", "缓解途径", "文献"],
              [["温度", "热激活去掺杂、晶粒收缩", "ESR↑", "温度降额、配方优化", "[17],[42]"],
               ["氧分压", "氧化破坏共轭/对阴离子", "ESR↑", "阻氧封装、惰性工艺", "[18],[92]"],
               ["湿度", "吸湿溶胀、界面腐蚀", "ESR↑、LC↑", "阻湿封装、强界面黏附", "[24],[51],[52]"],
               ["酸性(PSS)", "腐蚀介质/界面、去掺杂", "ESR↑、LC↑", "去质子/非酸性替代", "[8],[22]"],
               ["UV/辐照", "改变结构、降电导", "ESR↑", "封装遮蔽", "[92]"],
               ["电场/偏压", "场致退化、去掺杂加速", "LC↑、ESR↑", "电压降额", "[28]"]],
              widths=[1.8, 3.8, 2.4, 3.0, 1.6], fs=8.8,
              source_cn="注：综合自[8],[17],[18],[22],[24],[28],[42],[51],[52],[92]。")



# ================= 2.4 扩展（判据标准、数据归纳） =================
def ext_modes(doc):
    heading(doc, "2.4.8  失效判据的标准化与多参数判定", level=3)
    body(doc,
         "失效判据的统一是可比研究的前提。不同标准与厂商对“失效”的定义存在差异：电容量判据多取 |ΔC/C₀|≥20%（部分高可靠场景取 10%）；"
         "ESR 判据多取 ESR≥2×ESR₀（亦有取 1.5× 或绝对阈值者）；漏电流判据多以是否超过规格上限或出现骤增为准；此外短路/开路属突发失效，直接判失效[2],[13],[31]–[34],[80]。"
         "由于 ESR 具有显著的频率与温度依赖，比较时必须在统一频率（常用 100 kHz）与统一温度（常用 25°C 或工作温度）下进行，否则不同文献的“2 倍 ESR”可能并不等价[2]。")
    body(doc,
         "对 SAPC 这类多机理竞争器件，单参数判据往往不足以刻画其健康状态：ESR 反映聚合物/界面退化，LC 反映介质完整性，二者在不同应力下的相对快慢不同（2.4.7）。"
         "因此，发展“ESR–LC–（必要时）阻抗谱特征”的多参数联合判定，是提升失效判定准确性与 RUL 预测稳健性的方向之一；本文在 2.10 将其列为切入点之一。"
         "在判据落地时，还须区分“参数失效（功能尚可但超规格）”与“功能失效（电路无法正常工作）”，二者对系统的影响与维修决策不同。")

    heading(doc, "2.4.9  加速试验失效行为的归纳与比较", level=3)
    body(doc,
         "为便于横向比较，表15归纳了公开文献中代表性加速试验的应力条件、观测到的主导失效行为与关键结论。"
         "可见：①湿热（85/85、HAST）下普遍以 ESR 上升与 LC 增大为主、C 稳定，部分批次出现金属颗粒导致的高漏电[9],[10],[63]；"
         "②高温/高温存储下以 ESR 上升为主、寿命末期趋于开路[13],[42],[43]；③过流/浪涌下以良性失效为特征（不燃爆）[14],[75]；"
         "④温度循环下以界面分层与焊点疲劳导致的 ESR 上升/开路为主[81],[82]。这些归纳印证了 2.4.7 的失效模式分类，也直观暴露了“纯高温长周期数据偏少、耦合工况数据缺乏”的现状。")
    add_table(doc, 15, "代表性加速试验的应力条件、主导失效行为与关键结论（文献归纳）",
              ["试验/来源", "应力条件", "主导失效行为", "关键结论", "文献"],
              [["CALCE PA 电容", "85/85 + 偏压", "ESR↑、LC↑（C 稳定）", "两类模式并存、机理含界面与杂质", "[9]"],
               ["多层 PA 电容", "85/85、110/85", "失效时间随温度缩短", "建立温度相关寿命模型", "[10]"],
               ["快速评估", "提升 T/RH", "湿度降解聚合物", "缩短评价周期的方法", "[63]"],
               ["高温存储(钽)", "高温存储", "电阻率近指数增长", "热-氧化导致 ESR 退化", "[42],[43]"],
               ["过流(铝聚合物)", "破坏性大电流", "良性失效（无燃爆）", "聚合物隔离击穿点", "[14]"],
               ["SSST(钽)", "阶梯升压", "上电/击穿失效", "识别批次临界应力", "[75]"],
               ["温度循环", "−55~+125°C", "分层/焊点疲劳→ESR↑", "尺寸/焊点影响寿命", "[81],[82]"]],
              widths=[2.4, 2.4, 2.8, 3.4, 1.6], fs=8.6,
              source_cn="注：归纳自[9],[10],[14],[42],[43],[63],[75],[81],[82]；多为 SAPC 或高度类比的聚合物钽器件。")
    body(doc,
         "进一步看，上述试验的可比性受限于：失效判据不统一（2.4.8）、测试频率/温度不一致、样本量与置信水平差异，以及厂商批次与配方差异。"
         "这使得跨文献的定量外推（如统一的 Eₐ、湿度指数 n）仍需谨慎；建立统一规程下的 SAPC 专用多应力数据集，是消除这些可比性障碍的根本途径（2.10）。")


# ================= 2.5 扩展（定量动力学、迁移、映射） =================
def ext_mech(doc):
    heading(doc, "2.5.7  退化动力学的定量描述", level=3)
    body(doc,
         "把机理转化为可标定的动力学，是机理研究服务于寿命预测的关键。对聚合物本征退化，常以电导的一阶动力学近似："
         "dσ/dt = −σ/τ(T,RH,pO₂)，积分得式(2-8)的指数衰减；其时间常数 τ 经 Arrhenius/Peck 关系与应力相联系，τ⁻¹ ∝ exp(−Eₐ/k_BT)·RH^{m}。"
         "对界面接触退化，可设接触电阻随分层面积比 a(t) 增大：R_c ∝ 1/(1−a(t))，而 a(t) 由水分到达界面后的腐蚀/脱黏动力学驱动（与式2-9耦合）。"
         "将体电阻与接触电阻按式(2-3)相加，即得器件级 ESR(t) 的半解析表达，可与监测数据拟合标定[17],[42]。")
    body(doc,
         "对漏电退化，可在式(2-10)的 Poole–Frenkel 框架下，引入缺陷密度 N_t(t) 的演化（缺陷生成与自愈隔离的竞争）：dN_t/dt = g(E,T) − r(自愈)·N_t；"
         "当生成快于自愈时 LC 持续增大并可能突变为短路。这一“生成—自愈”竞争定量地解释了 2.5.3 所述“自愈裕度有限”的现象，也为竞争失效建模（2.6.7）提供了 LC 路径的动力学基础。"
         "需要强调，上述动力学的参数（τ、Eₐ、m、g、r）目前缺乏面向 SAPC 的系统标定，这是本文实验与建模工作的重点之一。")

    heading(doc, "2.5.8  电化学迁移与银迁移", level=3)
    body(doc,
         "在湿热+偏压下，SAPC 的银浆引出层与界面金属可能发生电化学迁移（electrochemical migration, ECM）：金属（如 Ag）在阳极被氧化为离子，"
         "在吸附水膜中沿电场迁移到阴极还原析出，形成枝晶（dendrite），最终导致漏电增大乃至短路（图20）。器件结构中设置石墨层的目的之一即为阻挡银向聚合物/介质的迁移[13]。"
         "ECM 的发生需要“可迁移金属离子 + 连续水膜 + 电位差”三要素同时具备，因而与湿热失效（水分侵入）和偏压（电位差）强耦合，是湿热突发短路的潜在机理之一。")
    add_figure(doc, "fig_migration.png", 29,
               "湿热+偏压下的电化学（银）迁移与枝晶生长机理（示意）",
               "来源：作者据电化学迁移原理与器件结构[13]绘制（原创示意图）。")
    body(doc,
         "ECM 与前述聚合物退化、界面分层、介质缺陷共同构成 SAPC 在湿热偏压下的失效机理集合；其相对重要性取决于材料体系、银浆/石墨阻挡设计与封装阻湿能力。"
         "在失效分析中，可通过 EDS/XPS 检出迁移金属、以截面 SEM 观察枝晶形貌加以识别（2.5.6）。把 ECM 纳入竞争失效模型，有助于更完整地刻画湿热突发失效裕度。")

    heading(doc, "2.5.9  机理—参数—应力映射", level=3)
    body(doc,
         "为把分散的机理整合为建模可用的结构，表16给出“应力—机理—退化参数—模型环节”的映射关系，作为连接 2.5（机理）与 2.6（建模）的桥梁。"
         "该映射的价值在于：它把每一种外部应力明确地落到具体机理与可测参数上，并指向相应的数学模型环节（式号），从而使失效物理模型（2.6.5）与竞争失效模型（2.6.7）的构建有据可循。")
    add_table(doc, 16, "SAPC 的“应力—机理—参数—模型环节”映射",
              ["主导应力", "关键机理", "退化参数", "对应模型环节(式)", "文献"],
              [["高温", "去掺杂/氧化、晶粒收缩", "ESR↑", "σ(t) 指数退化(2-8)+Arrhenius(2-5)", "[17],[18],[42]"],
               ["湿度", "吸湿溶胀、界面腐蚀/分层", "ESR↑、LC↑", "Fick 扩散(2-9)+Peck(2-13)", "[10],[24],[51]"],
               ["电场/偏压", "场致退化、自愈竞争、ECM", "LC↑", "Poole–Frenkel(2-10)+缺陷动力学", "[25],[28]"],
               ["纹波自热", "焦耳热正反馈", "ESR↑、温升", "自热模型(2-6)+Arrhenius", "[54],[85]"],
               ["温度循环", "CTE 失配、分层、焊点疲劳", "ESR↑→开路", "Coffin–Manson(2-7)", "[81],[82]"],
               ["多应力耦合", "上述并行竞争", "ESR/LC 联合", "竞争失效(2-19)+随机过程(2-16/17)", "[3],[73]"]],
              widths=[1.8, 3.4, 1.8, 4.2, 1.6], fs=8.6,
              source_cn="注：映射综合自 2.5 各节与[3],[10],[17],[18],[24],[25],[28],[42],[51],[54],[73],[81],[82],[85]。")



# ================= 2.6 扩展（算例、估计、验证、综合对比） =================
def ext_model(doc):
    heading(doc, "2.6.9  加速因子计算的工程算例", level=3)
    body(doc,
         "为说明经验模型的工程用法与误用风险，给出两则算例（参数取文献常见量级，仅作方法示范，具体值须由 SAPC 试验标定）。")
    body(doc,
         "【算例一·温度加速】设聚合物热氧老化的表观激活能 Eₐ=0.8 eV（k_B=8.617×10⁻⁵ eV/K）。由式(2-11)，125°C（398 K）相对 85°C（358 K）的加速因子为 "
         "AF_T=exp[(0.8/8.617e-5)(1/358−1/398)]。计算 1/358−1/398≈2.806×10⁻⁴ K⁻¹，乘以 0.8/8.617e-5≈9284，得指数 ≈2.605，故 AF_T≈e^2.605≈13.5。"
         "即 125°C 下 1 千小时的老化效果约相当于 85°C 下 1.35 万小时。若误用“10°C 法则”（式2-12）则得 2^((125−85)/10)=2^4=16，二者量级相近但并不相等——"
         "差异随 Eₐ 与温区放大，凸显以实测 Eₐ 替代经验法则的必要性。")
    body(doc,
         "【算例二·湿度加速】设 Peck 模型（式2-13）湿度指数 n=3、Eₐ=0.8 eV。由 130°C/85%RH（HAST）外推到 65°C/60%RH（使用）："
         "湿度项 (85/60)^3≈2.84；温度项 exp[(0.8/8.617e-5)(1/338−1/403)]，其中 1/338−1/403≈4.77×10⁻⁴，乘 9284≈4.43，得 e^4.43≈84。"
         "故总加速因子 AF≈2.84×84≈239，即 HAST 下约 500 小时可代表使用条件下约 12 万小时（约 13.6 年）。"
         "此类外推对 n 与 Eₐ 极为敏感（n 或 Eₐ 的小幅变化即引起数倍差异），因此必须以多条件试验联合标定并给出置信区间，切忌单点外推。")

    heading(doc, "2.6.10  退化参数估计与不确定性", level=3)
    body(doc,
         "参数估计是把数据转化为模型的桥梁。对寿命分布（式2-15），常用极大似然估计（MLE）并正确处理右截尾（试验结束时未失效样本）："
         "对数似然由失效样本的密度项与截尾样本的可靠度项相加构成，数值最优化求解 (η,β) 并由 Fisher 信息或自助法（bootstrap）给出置信区间。"
         "对退化随机过程（式2-16/2-17），可由增量的高斯/Gamma 分布写出似然并以 MLE/贝叶斯估计漂移、扩散或形状/尺度参数；含测量误差时引入状态空间模型与卡尔曼/粒子滤波估计[36],[73],[74]。")
    body(doc,
         "对加速模型（式2-11/2-13/2-14），通常采用“先在各应力水平下拟合退化/寿命，再回归应力—参数关系”的两步法，或直接对全部数据做加速失效时间（AFT）联合极大似然。"
         "无论何法，关键是报告参数的置信区间与外推的预测区间，并进行残差诊断与拟合优度检验（如概率作图相关系数、K–S 检验）。"
         "对 SAPC，由于样本与机理的分散性较大，分层贝叶斯能更自然地表达批次间差异并融合先验（式2-20），是较优选择。")

    heading(doc, "2.6.11  模型选择、验证与外推风险", level=3)
    body(doc,
         "面对统计、随机过程、PoF 与数据驱动等多类候选模型，模型选择应兼顾拟合优度与复杂度，常用赤池信息准则（AIC）、贝叶斯信息准则（BIC）或交叉验证；"
         "对预测任务，更应以“留出/时间序列交叉验证”评估外推能力，而非仅看训练拟合。验证须区分内插（在试验应力范围内）与外推（向使用条件外推）——后者风险显著更高。")
    body(doc,
         "外推风险的根源在于“机理不变假设”：加速模型默认加速应力下的失效机理与使用条件相同。若加速应力过高引入了新机理（如过高温度引发封装或介质的额外失效、过高湿度改变腐蚀路径），"
         "则外推系统性偏差。对 SAPC，这一风险尤为现实，因其多机理竞争且各机理对应力的敏感性不同（2.4.7、2.6.7）。"
         "因此，稳健做法是：①控制加速应力不越过机理转变阈值；②以失效分析确认加速与使用条件机理一致；③以 PoF/竞争失效模型显式表达各机理，从结构上降低外推风险；④给出预测区间而非点估计。"
         "这些原则共同构成本文建模工作的方法学约束。")

    heading(doc, "2.6.12  四类建模方法的综合对比", level=3)
    body(doc,
         "综合 2.6.2–2.6.11，表17从物理基础、数据需求、外推能力、不确定性表达、对 SAPC 的适用性与主要局限六个维度，对四类方法进行综合对比，作为方法选择的总览。"
         "总体判断是：没有单一方法可独占优势，融合（PoF 提供结构与外推、随机过程刻画分散与 RUL、数据驱动补足复杂非线性、贝叶斯统一不确定性）是面向 SAPC 的最优路线。")
    add_table(doc, 17, "四类可靠性建模方法的综合对比",
              ["方法类", "物理基础", "数据需求", "外推能力", "不确定性表达", "对 SAPC 适用性/局限"],
              [["经验/统计", "弱（解析关系）", "中", "中（机理不变时）", "分布/置信区间", "通用但易误用(10°C法则)"],
               ["退化随机过程", "中（唯象）", "中（需退化轨迹）", "中—好", "天然（首达分布）", "缺 SAPC 专用数据标定"],
               ["失效物理(PoF)", "强（机理动力学）", "中（标定本构）", "好", "需结合统计/贝叶斯", "耦合本构待实验标定"],
               ["数据驱动/融合", "弱—强（PINN可强）", "大（PINN可降）", "弱—较好(PINN)", "需贝叶斯/集成", "可解释/数据是瓶颈"]],
              widths=[2.2, 2.6, 2.0, 2.4, 2.8, 4.0], fs=8.6,
              source_cn="注：综合自[1],[29]–[39],[71]–[74],[83],[84],[93],[94]。")


# ================= 2.7 扩展（特征工程、维护决策） =================
def ext_monitor(doc):
    heading(doc, "2.7.4  健康指标的特征工程与数据预处理", level=3)
    body(doc,
         "高质量的健康指标是稳健 RUL 预测的前提。原始 ESR/C/LC 与阻抗数据通常含测量噪声、温度漂移与工况扰动，须经预处理与特征工程："
         "①温度归一化——将 ESR 折算到统一参考温度/频率，消除工况引起的可逆变化，仅保留不可逆退化（2.4.8）；②去噪与平滑——滑动平均、卡尔曼滤波抑制随机噪声；"
         "③特征提取——除 ESR/C 绝对值外，提取其变化率、阻抗谱特征（界面弧半径、特征频率）等作为更敏感的早期退化指标；④异常剔除与缺失处理。"
         "良好的特征工程能显著提升退化轨迹的单调性与信噪比，使随机过程/数据驱动模型更易标定[2],[80]。")
    body(doc,
         "对 SAPC 而言，因 ESR 基线极低（毫欧级），测量与折算误差对相对退化量的影响被放大，特征工程的重要性更为突出；"
         "将可逆（温度/频率）效应与不可逆（退化）效应严格分离，是避免“伪退化/伪健康”误判的关键。这一要求也反过来对监测电路的精度与温度补偿提出了更高标准（2.7.2）。")

    heading(doc, "2.7.5  预测性维护决策与经济性", level=3)
    body(doc,
         "RUL 预测的最终价值在于支撑维修决策。基于 RUL 后验分布（式2-18/2-20）与失效后果，可在“过早更换（浪费寿命）”与“过晚更换（失效风险）”之间优化维护时机，"
         "常用方法包括基于风险阈值（如可靠度低于某下限即维护）或基于期望成本最小化的决策规则。对安全关键系统（航天、汽车），决策更偏保守、强调失效概率上界；"
         "对成本敏感系统（消费/工业），则在可接受风险下最大化寿命利用。")
    body(doc,
         "预测性维护相对“定期更换”与“事后维修”的经济优势，取决于 RUL 预测的精度与置信度：预测越准、不确定性越小，越能压缩安全裕度、延长更换周期而不增加风险。"
         "因此，提升 SAPC 的 RUL 预测精度（2.6、2.7）不仅是学术目标，也直接转化为系统级的可用性与经济性收益，这构成本文研究的应用价值落点。")


# ================= 2.8 扩展（任务剖面、失效率预计） =================
def ext_app(doc):
    heading(doc, "2.8.4  任务剖面与寿命消耗", level=3)
    body(doc,
         "实际服役应力随时间变化，单点应力的寿命评估难以反映真实工况。任务剖面（mission profile）方法将随时间变化的负载/环境转化为器件热点温度等应力序列，"
         "再以累积损伤（如 Miner 线性累积或 Arrhenius 加权的损伤率积分）评估寿命消耗（图29）：D=∫ (1/L(T(t),RH(t))) dt，当 D 达 1 时判寿命终止[47]。"
         "对电动汽车充电模块等场景，已有基于任务剖面的铝电解电容寿命预测方法，并指出热点温度计算与寿命模型精度是预测准确性的瓶颈[47]——这一思路与精度约束同样适用于 SAPC。")
    add_figure(doc, "fig_mission.png", 30,
               "任务剖面驱动的热点温度与累积寿命消耗（示意）",
               "来源：作者据任务剖面寿命评估方法[47]绘制（原创概念图，非实测数据）。")
    body(doc,
         "任务剖面方法把“器件级寿命模型（2.6）”与“系统级工况”衔接起来，是可靠性研究服务于工程设计的关键环节。"
         "其准确性依赖三方面：热点温度估计（热阻网络，式2-6）、应力—寿命模型（式2-11/2-13）与损伤累积假设；"
         "对 SAPC，由于 ESR 退化会反过来改变自热（正反馈，2.4.4），严格的任务剖面评估应是“退化—自热”耦合的动态过程，而非静态加权，这对建模提出了更高要求。")

    heading(doc, "2.8.5  失效率预计、FIT 与系统级影响", level=3)
    body(doc,
         "在系统可靠性设计中，常以失效率 λ（单位 FIT，1 FIT=10⁻⁹/h）量化元件可靠性，并据此进行系统可靠性预计与冗余设计。"
         "失效率预计可基于手册（如 MIL-HDBK-217、IEC 62380 等的应力模型）或基于厂商/实测数据，并随温度、电压降额而变（2.2.7、图8）。"
         "对 SAPC，由于其失效以退化为主、突发失效良性，恒定失效率假设（指数分布）仅在“有用寿命期”（浴盆曲线中段，图24）近似成立；"
         "进入磨损期后须改用 Weibull/退化模型。系统层面，电容退化（ESR 上升）会降低滤波效果、增大纹波与温升，可能诱发对其它元件（功率器件、控制电路）的二次应力，"
         "因此 SAPC 的可靠性不仅关乎自身寿命，也通过纹波与热耦合影响整机可靠性，这进一步凸显了准确建模与监测的系统价值。")



# NOTE: module entry point is appended at the very end of the file.



# ================= 2.9 代表性研究案例剖析 =================
def s_cases(doc):
    heading(doc, "2.9  代表性研究案例剖析与方法学评述", level=2)
    body(doc,
         "为把前述分散结论落到具体研究上，本节遴选若干代表性工作进行剖析，重点解析其试验设计、关键发现、方法学价值与局限，并在末尾给出方法学评述。"
         "需说明，以下剖析均为对公开文献的归纳与转述（已做改写以符合引用规范），具体数据与结论请以原文为准。")

    heading(doc, "2.9.1  案例一：CALCE 对 PEDOT 聚合物铝电容的湿热失效研究", level=3)
    body(doc,
         "CALCE 团队对两家厂商（Nichicon、Nippon Chemi-Con）的 PEDOT 体系聚合物铝电容开展了高温高湿（含偏压）试验，是 SAPC 湿热可靠性的奠基性器件级工作之一[9]。"
         "其试验设计的要点在于：以额定偏压下的稳态温湿（如 85°C/85%RH）激发使用相关机理，并对失效样品进行系统失效分析。关键发现有三："
         "①主导失效为 ESR 上升与漏电流增大两类，且不同厂商样品的两类模式占比不同，反映材料/工艺差异；②电容量在试验中相对稳定，区别于液态铝电解的容量衰退；"
         "③在个别批次中发现源自制造的金属（铁）颗粒嵌入介质、形成此前未报道的高漏电机理[9]。")
    body(doc,
         "其方法学价值在于：把“器件级加速试验 + 多参数监测 + 深入失效分析”三者结合，既给出失效模式的统计，又揭示了机理（含工艺缺陷）。"
         "局限在于：应力条件集中于湿热、温区有限，难以外推到纯高温与耦合工况；样本与批次有限，统计置信受限。CALCE 后续以“快速评估测试”缩短评价周期[63]，"
         "并将研究扩展到多层结构（案例二）。该案例确立了“ESR/LC 为主、C 稳定”的 SAPC 湿热失效基本图景，是本章 2.4.2 的主要证据。")

    heading(doc, "2.9.2  案例二：多层聚合物铝电容的温度相关寿命模型", level=3)
    body(doc,
         "针对多层（叠层）聚合物铝电容，研究者在 85°C/85%RH 与 110°C/85%RH（额定偏压）两组条件下记录失效时间，并建立关联温度与失效时间的寿命模型[10]。"
         "其设计巧思在于：固定湿度、改变温度，以分离温度的加速效应，从而在 Peck/Arrhenius 框架下估计温度相关参数；同时关注封装几何对水分驱动退化的影响。"
         "关键贡献是：为多层 SAPC 提供了可外推的温度—寿命关系，并指出水分透过塑封向内扩散是湿热退化的前提（与式2-9一致）。")
    body(doc,
         "其方法学价值在于示范了“双条件分离变量 + 寿命建模”的范式；局限在于湿度维度仅单一水平，湿度指数 n 难以独立标定，且仍未覆盖纯高温与热-电耦合。"
         "该案例直接支撑本章 2.6.2 关于 Peck/Eyring 模型应用的论述，也凸显了“多应力多水平联合标定”的必要性（2.10 切入点①）。")

    heading(doc, "2.9.3  案例三：NASA 对片式铝聚合物电容的航天适用性评估", level=3)
    body(doc,
         "NASA NEPP 针对层叠铝聚合物电容（APC）作为片式钽电容替代品的可能性，开展了物理/电学表征与应力测试，并评估其航天适用性[15],[16]。"
         "其出发点是 APC 的低 ESR、轻量与小型化优势；但 NASA 明确指出该类器件可靠性数据稀缺、已有文献多集中于湿度影响，因而需要专门评估[15],[16]。"
         "在破坏性过流试验中，铝聚合物电容均以良性模式失效（无起火/燃烧/爆炸），印证了聚合物阴极相对 MnO₂ 的安全优势[14]。")
    body(doc,
         "其方法学价值在于：从高可靠/航天选用的严格视角，系统评估器件的电学、结构与失效安全性，并明确指出“数据缺口”这一现状判断（本章 2.4.3、2.8.2 的核心依据）。"
         "局限在于：航天评估样本与条件特定，结论向消费/工业宽场景外推需谨慎。该案例与本章“纯高温长周期数据不足”的判断高度一致，是 2.10 不足分析的直接来源之一。")

    heading(doc, "2.9.4  案例四：聚合物钽电容高温存储的 ESR 退化", level=3)
    body(doc,
         "聚合物钽电容（CPTC）与 SAPC 在“导电聚合物阴极 + 阀金属氧化膜介质”上高度同构，其高温存储研究对 SAPC 具有直接类比价值[42],[43]。"
         "研究通过高温存储后测量交流特性，观察到 ESR 随老化显著上升，并将其归因于导电聚合物的热-氧化过程，电阻率随老化时间近似指数增长[42]——这正是式(2-8)指数退化的实验支撑。"
         "其方法学价值在于：以可控的高温存储分离“热-氧化”单机理，给出清晰的 ESR–时间规律与机理归因。")
    body(doc,
         "局限在于：器件体系为钽而非铝，介质与界面细节不同，定量参数不可直接照搬；且高温存储不含偏压与湿度，未覆盖耦合效应。"
         "尽管如此，该案例为 SAPC 的高温失效机理（2.5.1）与 PoF 建模（2.6.5）提供了可迁移的动力学形式与机理依据，是本章在“高温数据偏少”背景下的重要类比证据。")

    heading(doc, "2.9.5  案例五：PEDOT:PSS 热老化的颗粒金属机理研究", level=3)
    body(doc,
         "Vitoratos、Sakkopoulos 等的材料级研究为 SAPC 的退化提供了微观机理基础[17],[18]。其核心发现是：PEDOT:PSS 的电导随时间下降，且该下降与“导电晶粒收缩”的颗粒金属图像一致；"
         "通过对比惰性（氦）与空气气氛，证明氧（空气）显著加速老化，提示氧化是主导途径之一[18]。这把“分子—晶粒—薄膜”尺度的退化与器件 ESR 上升联系起来。")
    body(doc,
         "其方法学价值在于：以电导—温度/时间/气氛的系统测量，锁定颗粒收缩与氧化两大机理，并为 VRH（式2-4）与指数退化（式2-8）提供物理依据。"
         "局限在于：研究对象为薄膜而非器件，未含器件级界面/封装效应；但其机理结论被聚合物钽高温存储（案例四）在器件层面间接印证。该案例是本章 2.3、2.5.1 的理论基石。")

    heading(doc, "2.9.6  案例六：高湿环境下分层主导的电导退化", level=3)
    body(doc,
         "厂商研究（KEMET）对高湿环境下导电聚合物电容的可靠性给出了重要机理判断：热-机械与电压诱发的应力所导致的分层（delamination），是高湿下电导退化的主要原因之一[12]。"
         "这把“湿度”这一外因，落到了“界面分层导致接触电阻增大”这一内因上（与本章 2.5.2 一致），并提示改善界面黏附与封装是抑制湿热退化的关键。")
    body(doc,
         "其方法学价值在于：从工程实证角度指认了界面分层这一“枢纽机理”，呼应了 2.5.2 的论述与表16的映射。"
         "局限在于：作为厂商技术资料，其试验细节与统计深度有限。综合案例一至案例六，可见 SAPC 失效是“聚合物本征退化（热/氧）”与“界面/封装相关退化（湿/机械）”两条主线的交织，"
         "且后者在湿热场景中往往起枢纽作用。表18汇总六个案例的要点。")
    add_table(doc, 18, "代表性研究案例剖析要点汇总",
              ["案例", "对象/应力", "关键发现", "方法学价值", "主要局限", "文献"],
              [["一·CALCE湿热", "PA电容/85-85", "ESR↑、LC↑；Fe颗粒新机理", "试验+FA结合", "应力单一、样本有限", "[9],[63]"],
               ["二·多层寿命模型", "多层PA/双温度", "温度相关寿命模型", "分离变量建模", "湿度单水平", "[10]"],
               ["三·NASA航天评估", "APC/应力+过流", "良性失效；数据稀缺", "高可靠视角评估", "条件特定", "[14]-[16]"],
               ["四·钽高温存储", "CPTC/高温", "ESR近指数增长(热氧化)", "单机理分离", "器件为钽、无湿/偏压", "[42],[43]"],
               ["五·PEDOT热老化", "PEDOT:PSS薄膜", "电导降、氧加速、颗粒收缩", "微观机理锁定", "薄膜非器件", "[17],[18]"],
               ["六·高湿分层", "聚合物电容/高湿", "分层为电导退化主因", "指认枢纽机理", "厂商资料、细节少", "[12]"]],
              widths=[2.2, 2.2, 3.0, 2.4, 2.6, 1.4], fs=8.4,
              source_cn="注：均为对公开文献的归纳转述，详见对应参考文献。")

    heading(doc, "2.9.7  方法学评述", level=3)
    body(doc,
         "综观上述案例，可对 SAPC 可靠性研究的方法学作如下评述：①“器件级加速试验 + 多参数监测 + 系统失效分析”是最有效的研究范式（案例一、三），能同时给出模式统计与机理归因；"
         "②“单机理分离 + 动力学建模”（案例四、五）是连接机理与模型的有效路径，但需注意从薄膜/异类器件向 SAPC 迁移的适用性；"
         "③“双/多条件分离变量 + 寿命建模”（案例二）是参数标定的基础，但当前普遍存在“湿度或应力维度单一”的不足，导致 n、Eₐ 等参数难以独立、稳健地标定；"
         "④厂商工程证据（案例六）有助于指认枢纽机理，但统计深度与可复现性有限。")
    body(doc,
         "这些评述共同指向一个结论：要把 SAPC 可靠性研究推进到“可外推、可监测、含不确定性”的新阶段，必须在方法学上实现"
         "“多应力多水平统一规程的器件级数据集 + 机理贯通的失效物理模型 + 竞争失效与不确定性量化 + 物理-数据融合的 RUL 预测”的整体升级。这正是本文研究设计的方法学依据（详见 2.11）。")


# ================= 2.6 扩展二（算法流程、RUL 推导） =================
def ext_model2(doc):
    heading(doc, "2.6.13  贝叶斯滤波 RUL 估计的算法流程", level=3)
    body(doc,
         "以粒子滤波（PF）为例，说明“状态空间退化模型 + 在线贝叶斯更新”的 RUL 估计流程，其可处理非线性、非高斯退化，适合 SAPC 的 ESR 退化跟踪[36],[72]。"
         "设退化状态 x_k（如折算后的 ESR），状态方程 x_k=f(x_{k-1},θ)+w_k 表达退化动力学（如式2-8的离散化），观测方程 z_k=h(x_k)+v_k 表达带噪声的监测。算法步骤为：")
    bullet(doc, "①初始化：由先验 p(x₀,θ) 采样 N 个粒子 {x₀^i,θ^i} 及权重 1/N。")
    bullet(doc, "②预测：按状态方程将每个粒子推进一步，得 x_k^i。")
    bullet(doc, "③更新：按观测似然 p(z_k|x_k^i) 更新权重 w_k^i ∝ w_{k-1}^i·p(z_k|x_k^i)，归一化。")
    bullet(doc, "④重采样：当有效粒子数过低时按权重重采样，缓解粒子退化。")
    bullet(doc, "⑤RUL 外推：以当前粒子集为初值，按状态方程持续外推至各粒子首次越过失效阈值 D，得首达时刻集合，统计其分布即 RUL 后验（式2-18框架）。")
    body(doc,
         "PF 的优点是通用、能在线融合监测数据并自然给出 RUL 不确定性；难点是粒子退化、计算量与对状态/观测模型的依赖。"
         "扩展卡尔曼滤波（EKF）在近高斯情形下更高效；二者均已用于电解电容的退化跟踪与 RUL 预测[36],[72]。对 SAPC，状态方程可由 2.5.7 的退化动力学给出，从而把 PoF 与滤波融合。")

    heading(doc, "2.6.14  Gamma 过程 RUL 与在线贝叶斯更新", level=3)
    body(doc,
         "对单调不可逆退化（如氧化、腐蚀），Gamma 过程（式2-17）是首选。给定阈值 D 与当前退化量 x_t，剩余寿命 L 满足 x_{t+L}−x_t≥D−x_t，"
         "其分布可由 Gamma 过程增量的分布导出（无简单初等闭式，常用数值积分或鞍点/Birnbaum–Saunders 近似）。其期望 RUL 近似为 E[L]≈(D−x_t)·β/α（由 E[ΔX]=αΔt/β 反解）。")
    body(doc,
         "在线估计方面，基于共轭先验的贝叶斯方法可随监测增量递推更新形状/尺度参数的后验，并据此给出 RUL 后验，兼顾效率与不确定性表达[74]；"
         "当存在个体差异时，采用分层先验（不同个体共享超参数）可在“总体信息”与“个体观测”间自适应折中，提升小样本/早期预测的稳健性[73]。"
         "这一“Gamma 过程 + 共轭贝叶斯 + 分层先验”的组合，契合 SAPC“退化为主、批次分散、长周期数据稀缺”的特点，是本文 RUL 方法的候选核心（2.11 切入点④）。")



# NOTE: module entry point appended at end after all functions are defined.
# __MAIN_END__



# ================= 深化批次一：器件/材料/模式/机理 =================
def ext_device2(doc):
    heading(doc, "2.2.9  ESR/ESL 的频率分解与等效电路细化", level=3)
    body(doc,
         "为支撑状态监测与失效物理建模，需对 ESR 的频率行为作更细致的分解。SAPC 的 ESR 并非常数，而是频率与温度的函数："
         "在低频段，介质损耗（与 tanδ 相关）与聚合物体电阻共同贡献；在中频段（约 1–100 kHz），聚合物体电阻与界面/接触电阻主导，呈现相对平坦的低谷；"
         "在高频段（>1 MHz），趋肤效应与引出端电阻使 ESR 略升，同时 ESL 主导阻抗。因此规格书常以 100 kHz 作为 ESR 标称频率，监测与退化比较亦应固定于此（2.4.8）[2],[61]。")
    body(doc,
         "更完备的等效电路可在串联 RLC 基础上引入分布参数：以传输线（梯形 RC 网络）描述多孔阳极内聚合物—氧化膜界面沿孔道的分布阻抗，"
         "从而解释阻抗谱在中高频的渐变特征与 EIS 弧的形状（图19）。退化（界面分层、聚合物体电阻上升）会改变该分布网络的参数，"
         "在 Nyquist 谱上表现为高频实轴截距右移与界面弧增大，这正是以 EIS 作机理诊断的物理基础（2.5.6、2.7.1）。"
         "建立“分布等效电路—退化参数”的定量对应，是把器件电学测量反演为内部机理状态的关键，也是本文监测与建模衔接的技术路线之一。")
    body(doc,
         "ESL 主要由叠层几何、汇流路径与引出端结构决定。叠层并联在降低 ESR 的同时也降低 ESL，从而提升自谐振频率 f₀，改善高频去耦能力[5],[15]。"
         "在高频供电（如处理器核心电压）场景，低 ESL 意味着更小的瞬态电压跌落，这是 SAPC 相对液态铝电解电容的关键优势之一；"
         "而退化引起的接触电阻增大虽主要影响 ESR，但界面分层在极端情形下也可能改变电流路径而轻微影响 ESL。综合而言，ESR 仍是 SAPC 退化最敏感、最可监测的电学指标。")


def ext_material2(doc):
    heading(doc, "2.3.10  PEDOT、PEDOT:PSS 与聚吡咯体系的对比", level=3)
    body(doc,
         "导电聚合物阴极体系的选择直接影响 SAPC 的电导、稳定性与工艺性。聚吡咯（PPy）是最早用于电解电容的导电聚合物，电导尚可、可电化学聚合，"
         "但热稳定性与长期稳定性相对较弱；PEDOT（尤其经二次掺杂的高电导 PEDOT）兼具高电导与较好的环境稳定性，是当前主流；"
         "PEDOT:PSS 以水分散、易加工见长，但 PSS 的强酸性与吸湿性带来稳定性隐患，需通过去质子、配方优化加以抑制（2.3.6、2.3.9）[4],[8],[22],[66]。表19从可靠性视角对三者进行对比。")
    add_table(doc, 19, "PPy、PEDOT 与 PEDOT:PSS 导电聚合物体系的可靠性视角对比",
              ["体系", "电导水平", "热/氧稳定性", "湿/酸敏感性", "工艺性", "可靠性要点"],
              [["聚吡咯 PPy", "中", "较弱", "中", "可电化学聚合", "热稳定性限制长期可靠性"],
               ["PEDOT(高电导)", "高", "较好", "中（依对阴离子）", "原位聚合/处理", "主流；需控氧化与对阴离子"],
               ["PEDOT:PSS", "中—高(可提升)", "中", "较高(PSS酸/吸湿)", "水分散、易涂覆", "需去质子/配方优化抑制退化"]],
              widths=[2.6, 2.0, 2.4, 2.6, 2.6, 3.4], fs=8.6,
              source_cn="注：综合自[4],[8],[17],[18],[20]–[22],[62],[66]–[70]，定量电导依配方与后处理差异显著。")
    body(doc,
         "从失效机理看，三类体系的共性是“掺杂态电导对热/氧/湿敏感、退化表现为电导下降/ESR 上升”，差异主要在敏感程度与主导退化途径："
         "PPy 偏热稳定性短板，PEDOT:PSS 偏酸性/吸湿短板，高电导 PEDOT 则在二者之间取得较好平衡。这一对比解释了产业向 PEDOT 体系收敛的可靠性动因，"
         "也提示 SAPC 可靠性研究应针对所用具体体系标定其退化动力学参数（2.3.8、2.5.7），而非笼统套用“导电聚合物”的通用结论。")

    heading(doc, "2.3.11  合成化学、氧化剂残留与杂质控制", level=3)
    body(doc,
         "原位化学聚合制备 PEDOT 时，单体 EDOT 在氧化剂（常用 Fe(III) 盐等）作用下聚合，反应后体系中可能残留铁等金属离子与副产物。"
         "若清洗与后处理不充分，残留金属/离子不仅可能催化聚合物的氧化老化，还可能在湿热偏压下成为漏电通道或电化学迁移源（2.5.4、2.5.8）。"
         "CALCE 在器件中发现的铁颗粒高漏电机理[9]，与这一合成化学背景相呼应——它提示“产线洁净度与杂质控制”是 SAPC 漏电可靠性的重要工程变量。")
    body(doc,
         "因此，材料级可靠性改进应同时关注：①对阴离子的选择与稳定性（影响热/氧老化路径，2.3.1、2.3.4）；②氧化剂/副产物的去除（影响漏电与老化催化）；"
         "③PSS 酸性的中和（影响界面腐蚀，2.3.6）；④分散液配方与润湿性（影响深孔填充与接触，2.3.7）。这些“化学源头”的控制与“器件封装/降额”的工程措施相结合，"
         "构成 SAPC 可靠性提升的完整链条，也界定了材料—器件协同优化的研究空间。")


def ext_modes2(doc):
    heading(doc, "2.4.10  容量退化与开路失效机理的再讨论", level=3)
    body(doc,
         "尽管 SAPC 退化以 ESR 上升与漏电增大为主、电容量相对稳定，但在高温或长周期下，电容量仍会缓慢偏离并最终趋于开路，这一过程值得单独讨论。"
         "电容量取决于有效电极面积与介质完整性（式2-1）；当聚合物阴极因热氧老化、界面分层或脱黏导致有效接触面积下降时，参与储能的面积减小，电容量随之下降[13]。"
         "在极端退化下，聚合物—氧化膜接触大面积失效，等效于阴极“断连”，器件趋于开路——这是高温失效的终态（2.4.3）。")
    body(doc,
         "与液态铝电解电容“电解液干涸→容量显著下降”的磨损失效不同，SAPC 的容量退化更多源于“接触/界面退化导致的有效面积损失”，而非介质本身的大幅变化。"
         "因此，电容量在 SAPC 中往往是“滞后且非线性”的健康指标：早期变化小（故对早期退化不敏感），晚期加速（接近开路）。"
         "这从指标选择上进一步支持以 ESR（早期即敏感、单调）为主、辅以 LC 与必要时电容量/阻抗谱的多参数监测策略（2.4.8、2.7.4）。"
         "理解容量—开路的机理，对正确设定失效判据与避免“仅看容量而漏判 ESR 失效”的误区具有实际意义。")


def ext_mech2(doc):
    heading(doc, "2.5.10  介质氧化膜的场致结晶与击穿统计", level=3)
    body(doc,
         "Al₂O₃ 介质的非晶态在高电场、高温或长期偏压下可能发生场致结晶（field crystallization）：局部由非晶转为晶态，晶界与相界处的漏电与缺陷增多，"
         "削弱介质阻挡能力、抬高漏电并降低击穿裕度[28]。这一过程在液态铝电解电容中可由电解液供氧再形成而部分抑制[3],[87]，而在固态 SAPC 中缺乏持续供氧，"
         "其抑制主要依赖聚合物在缺陷处的高阻隔离（自愈，2.5.3）。当结晶/缺陷的生成快于隔离时，漏电持续增大并可能发展为击穿。")
    body(doc,
         "从统计角度，介质击穿具有“最弱环节（weakest-link）”特征：器件由大量并联微元构成，整体击穿由缺陷最严重的微元触发，故击穿电压/寿命常服从 Weibull 分布（式2-15）。"
         "聚合物钽电容中击穿电压相对额定电压服从 Weibull 分布的报道[57]即为此例。理解场致结晶与最弱环节统计，有助于解释漏电型失效的分散性与降额（降低介质电场）的有效性（2.2.7、式2-10）。"
         "这也提示，漏电路径的竞争失效建模（2.6.7）应采用 Weibull/极值统计而非正态假设。")

    heading(doc, "2.5.11  失效率的批次分散与质量一致性", level=3)
    body(doc,
         "SAPC 的可靠性不仅由“平均”退化决定，更受批次分散与质量一致性影响。蚀刻/化成的均一性、聚合物填充的完整性、杂质控制与封装密封的稳定性，"
         "都会在器件间引入差异，表现为失效时间的分散（Weibull 形状参数）与早期失效（婴儿期，图24）。CALCE 观察到不同厂商样品失效模式占比不同[9]，即反映了材料/工艺差异导致的批次特性。")
    body(doc,
         "在可靠性工程上，应对批次分散的手段包括：加电老化/筛选剔除早期失效（2.5.4、[50],[75]）、统计过程控制保障一致性、以及在建模中显式表达个体差异（分层贝叶斯，2.6.8、2.6.14）。"
         "对研究而言，这意味着 SAPC 的可靠性结论必须标注样本来源与批次信息，跨批次/跨厂商的外推须谨慎；建立统一规程下、含批次标识的 SAPC 数据集（2.11 切入点①），"
         "正是为了让分散性可被量化与建模，而非被平均掩盖。")



# ================= 深化批次二：建模/监测/应用/展望 =================
def ext_model3(doc):
    heading(doc, "2.6.15  多元退化与多阈值竞争失效建模", level=3)
    body(doc,
         "SAPC 同时存在 ESR 与 LC 两条主要退化路径（必要时再加界面/焊点路径），二者并非独立：共同的水分、温度与界面状态使其相关。"
         "因此，单变量退化模型不足以刻画其健康状态，需发展多元退化模型。一种思路是以多元随机过程（如多元 Wiener/Gamma，或以 Copula 联结边缘退化分布）联合建模 ESR(t) 与 LC(t)，"
         "各自设定失效阈值（ESR≥2×ESR₀、LC≥LC_max），器件失效为任一变量首达其阈值（多阈值竞争）。系统可靠度由式(2-19)在相关情形下推广为联合首达概率。")
    body(doc,
         "建模的关键与难点在于：①刻画路径间相关性（共因：水分/温度/界面），Copula 或共享随机效应是常用手段；②阈值的物理设定与统一（2.4.8）；"
         "③参数的联合标定与可辨识性。相比把各路径独立处理，多元/相关竞争模型能避免高估可靠度（独立假设通常乐观），给出更真实的失效概率。"
         "目前面向 SAPC 的多元退化数据与模型仍属空白，这是本文在竞争失效方向的具体切入（2.11 切入点③）。")

    heading(doc, "2.6.16  加速试验的统计设计与最优应力分配", level=3)
    body(doc,
         "加速试验的信息量取决于应力水平、样本分配与试验时长的设计。统计上，加速寿命试验设计（ALT design）以“在试验资源约束下最小化使用条件寿命分位数估计方差”为目标，"
         "给出最优应力水平数、各水平样本量与截尾时间。经验表明：①至少需 2–3 个应力水平以标定应力—寿命关系（单点无法估计斜率，故案例二的单湿度水平限制了 n 的标定，2.9.2）；"
         "②高应力多投样本以加速获得失效、低应力少投样本以锚定外推，常优于均匀分配；③应避免应力过高引入新机理（2.6.11）。")
    body(doc,
         "对 SAPC 这类多机理、湿-热-电多维应力器件，试验设计还需考虑应力维度的交互（如温度×湿度、温度×偏压），宜采用析因或最优设计（D-/c-最优）在多维应力空间布点，"
         "以同时标定 Arrhenius 的 Eₐ、Peck 的 n 与可能的交互项（式2-13/2-14）。良好的统计设计是“以最少试验获得最可靠外推”的前提，"
         "也是本文构建 SAPC 专用多应力数据集时的方法学依据（2.11 切入点①）。")

    heading(doc, "2.6.17  不确定性传播与敏感性分析", level=3)
    body(doc,
         "寿命/RUL 预测的不确定性来自参数估计误差与模型形式不确定性，需经不确定性传播量化到预测量。常用方法包括："
         "解析传播（一阶 delta 法，由参数协方差近似预测方差）、蒙特卡洛抽样（从参数后验抽样并传播）、以及贝叶斯预测分布（式2-20，直接给出预测后验）。"
         "以算例二的 Peck 外推为例（2.6.9 算例二），若 n 的估计标准差为 ±0.3、Eₐ 为 ±0.05 eV，则加速因子 AF 的相对不确定性可达数十个百分点——"
         "这定量说明了“单点外推+点估计”的危险，以及报告预测区间的必要性。")
    body(doc,
         "敏感性分析则识别哪些参数对预测影响最大，从而指导试验资源投放（优先精确标定高敏感参数）。对 SAPC，敏感性通常集中于激活能 Eₐ 与湿度指数 n（指数项放大其影响），"
         "其次为失效阈值设定与初始分散。把不确定性量化与敏感性分析纳入建模流程，是从“给出一个寿命数字”升级为“给出带置信、可决策的可靠性评估”的必要步骤，"
         "贯穿本文建模与预测工作（2.6.8、2.6.14）。")


def ext_monitor2(doc):
    heading(doc, "2.7.6  监测方法的精度、成本与适用性比较", level=3)
    body(doc,
         "状态监测方法的工程选择需在精度、成本、侵入性与适用工况间权衡。基于变换器自身传感的纹波辨识法成本最低、易嵌入，但精度受传感与算法限制，"
         "对 SAPC 极低 ESR 的辨识尤具挑战（2.7.2）；专用阻抗/EIS 测量精度高、可作机理诊断，但需附加激励电路、多为离线或准在线；"
         "数据智能方法依赖数据质量与代表性，适合已有大量运行数据的系统[2],[78],[79],[80]。表20从多维度给出定性比较，供监测方案设计参考。")
    add_table(doc, 20, "SAPC 状态监测方法的精度/成本/适用性比较",
              ["方法", "ESR 精度", "硬件成本", "侵入性", "在线能力", "对极低 ESR 适用性"],
              [["纹波电压/电流辨识", "中", "低", "低（复用传感）", "在线", "受限（需高精度/补偿）"],
               ["参数辨识(STLSP/Prony)", "中—高", "低", "低", "在线", "中"],
               ["阻抗谱(EIS)", "高", "较高", "中（需激励）", "离线/准在线", "好（机理级）"],
               ["数据智能/学习", "依数据", "中（算力）", "低", "在线", "依特征工程"]],
              widths=[3.0, 1.8, 1.8, 2.2, 2.0, 3.0], fs=8.6,
              source_cn="注：综合自[2],[78],[79],[80]；SAPC 因 ESR 基线极低，对精度与温度补偿要求更高（2.7.4）。")
    body(doc,
         "对 SAPC 的实践建议是：以低成本纹波辨识作常态在线监测、以阻抗谱作周期性深度诊断、并辅以数据智能融合多源信息；"
         "同时，必须配合严格的温度/频率折算与特征工程（2.7.4），方能在极低 ESR 基线上可靠识别退化。监测精度的提升将直接转化为 RUL 预测置信度与维护经济性的改善（2.7.5）。")


def ext_app2(doc):
    heading(doc, "2.8.6  各应用的失效判据、降额准则与标准映射", level=3)
    body(doc,
         "不同应用对失效判据与降额的要求差异显著，须与相应标准映射。汽车电子以 AEC-Q200 为核心，强调宽温、温度循环与振动下的参数稳定与低失效率，电压降额常取约 50%[34],[65]；"
         "航天/高可靠以严格筛选、批次一致性与突发失效裕度为重，判据更保守、并关注 ACC 等特殊现象[15],[16],[75]–[77]；"
         "消费/工业电源以低 ESR、高纹波与成本为先，判据多以 ESR/容量超限为准，并结合任务剖面评估寿命（2.8.4）[5],[47]。表21给出三类应用的判据/降额/标准映射概览。")
    add_table(doc, 21, "典型应用的失效判据、降额准则与标准映射",
              ["应用", "主要失效判据", "降额准则(典型)", "对应标准/方法", "文献"],
              [["汽车电子", "ESR↑、参数超限、低 FIT", "电压~50%、温度留裕", "AEC-Q200、任务剖面", "[34],[47],[65]"],
               ["航天/高可靠", "保守阈值、突发裕度、ACC", "严格降额+筛选", "NASA NEPP/NPSL、SSST", "[15],[16],[75]–[77]"],
               ["消费/工业电源", "ESR/容量超限", "按成本/寿命权衡", "IEC 60384-1、寿命计算", "[5],[33],[47],[85]"]],
              widths=[2.2, 3.4, 3.0, 3.2, 1.6], fs=8.6,
              source_cn="注：综合自[5],[15],[16],[33],[34],[47],[65],[75]–[77],[85]；具体阈值以项目规范为准。")
    body(doc,
         "这一映射表明：SAPC 的“可靠性”并非单一指标，而是随应用而变的判据集合与降额策略；脱离应用谈寿命缺乏意义。"
         "因此，本文在建模与验证中将结合具体应用的判据与任务剖面（2.8.4），使可靠性结论具备工程可用性（2.11 切入点⑤）。")


def s_outlook(doc):
    heading(doc, "2.12  研究趋势与未来展望", level=2)
    body(doc,
         "在系统梳理现状与不足的基础上，本节展望 SAPC 可靠性研究的发展趋势，作为对前文的前瞻性补充与对本文工作的定位。")

    heading(doc, "2.12.1  材料与器件：稳定化与高可靠化", level=3)
    body(doc,
         "材料层面的趋势是“在保持高电导的同时提升环境稳定性”：通过去质子化中和 PSS 酸性、选择稳定对阴离子、提高分子量与结晶度、二次掺杂与界面阻挡层设计，"
         "抑制去掺杂、氧化与吸湿溶胀（2.3.6、2.3.9）[8],[20],[22],[66],[68]。器件层面则朝高可靠工艺（强界面黏附、优封装阻湿、严杂质控制）与高可靠/航天适用方向发展[15],[16],[50]，"
         "并以混合型方案兼顾低 ESR 与自愈/温度寿命（2.2.8）。这些趋势的共同目标是缩小 SAPC 相对成熟器件的可靠性差距，扩大其在严苛环境的应用边界。")

    heading(doc, "2.12.2  试验与数据：多应力、长周期、标准化", level=3)
    body(doc,
         "针对“器件数据浅、专用数据缺”的现状（2.10），趋势是建立统一规程下的多应力（湿-热-电-机械）、长周期、含批次标识的 SAPC 专用可靠性数据集，"
         "并以统计试验设计优化应力布点与样本分配（2.6.16）。数据共享与基准化（benchmark）将使退化随机过程、数据驱动与 PINN 等方法得以公平比较与可复现验证，"
         "这是把方法学优势转化为 SAPC 实效的前提，也是本文的基础性工作之一。")

    heading(doc, "2.12.3  建模与人工智能：物理-数据融合与不确定性", level=3)
    body(doc,
         "建模趋势是“物理与数据深度融合”：以失效物理（PoF）提供机理结构与外推骨架、以退化随机过程刻画分散与 RUL、以数据驱动/PINN 补足复杂非线性、以贝叶斯统一不确定性（2.6.5–2.6.8、2.6.17）。"
         "PINN 等物理信息学习方法在小样本下的外推与物理一致性优势[83],[84]，对“长周期数据稀缺”的 SAPC 尤具吸引力。"
         "竞争失效与多元退化建模（2.6.15）将使“多机理耦合”从定性走向定量，是连接机理与寿命预测的关键突破口。")

    heading(doc, "2.12.4  监测与运维：在线 PHM 与数字孪生", level=3)
    body(doc,
         "监测与运维趋势是从离线评估走向在线 PHM 乃至数字孪生：以嵌入式在线监测（2.7）持续获取 ESR/LC，以物理-数据融合模型在线更新健康状态与 RUL（2.6.14），"
         "并在系统层面以数字孪生整合任务剖面、退化—自热耦合（2.8.4）与维护决策（2.7.5）。其价值在于把“元件可靠性”嵌入“系统可用性与经济性”的闭环，"
         "实现预测性维护。实现这一愿景的瓶颈仍是 SAPC 极低 ESR 的高精度在线辨识与稳健 RUL 预测，正是本文力图突破之处。")

    heading(doc, "2.12.5  小结性展望", level=3)
    body(doc,
         "综观之，SAPC 可靠性研究正从“单应力实证 + 经验外推”迈向“多应力数据 + 机理贯通 + 物理-数据融合 + 在线 PHM”的新阶段。"
         "本文的研究设计——多应力加速试验与专用数据集、机理贯通的失效物理与竞争失效模型、物理-数据融合的 RUL 预测、面向应用的验证——正是对上述趋势的积极回应（详见 2.11 与后续各章）。")



# __MAIN_RE_ADDED__



# ================= 深化批次三：定位/选型/多物理/阶段/多尺度/统一模型/可观测性/系统后果 =================
def ext_intro2(doc):
    heading(doc, "2.1.5  相关综述的对比与本综述的定位", level=3)
    body(doc,
         "已有若干与本主题相关的综述或评述性文献，厘清其侧重有助于界定本章的增量价值。功率电子用电容器可靠性的整体综述[1]建立了失效机理—失效模式—寿命模型的总框架，"
         "但以液态铝电解、薄膜与 MLCC 为主，对 SAPC 着墨有限；电容器状态监测综述[2]系统梳理了 ESR/C 在线辨识方法，但聚焦监测而非失效物理；"
         "DC-link 电容可靠性综述则从应用与监测两方面评述了可靠性提升路径[1]。在材料侧，PEDOT(:PSS) 的电导与降解机理已有大量专门研究与综述[17],[18],[51],[52],[66]–[70],[92]，但多停留在薄膜/材料层面。")
    body(doc,
         "相较之下，本章的定位与增量在于：①以 SAPC（叠层铝固态）这一具体器件为核心，而非泛论电容器；②贯通“器件—材料—失效模式—机理—建模—监测—应用”全链条，"
         "尤其强调把材料级机理（PEDOT 退化）与器件级寿命（ESR/LC）定量衔接；③系统对比统计/随机过程/PoF/数据驱动四类建模方法并指出对 SAPC 的适用性与缺口；"
         "④以案例剖析（2.9）与文献计量（2.10）支撑“材料机理深、器件数据浅、方法工具全、专用数据缺”的总体判断，并据此凝练切入点（2.11）。"
         "这一“器件聚焦 + 全链条贯通 + 机理-建模衔接 + 缺口导向”的组织，是本章区别于既有综述的特色。")


def ext_device3(doc):
    heading(doc, "2.2.10  SAPC 与 MLCC、薄膜电容的互补与选型", level=3)
    body(doc,
         "在实际电源与电路设计中，SAPC 常与多层陶瓷电容（MLCC）、薄膜电容协同使用，理解其互补关系有助于把 SAPC 的可靠性置于系统语境。"
         "MLCC 以极低 ESL、宽频带与高可靠见长，但 II 类介质存在直流偏压下容量大幅衰减（DC-bias derating）、压电啸叫与机械裂纹风险；"
         "薄膜电容自愈性好、可靠性高、耐纹波，但体积大、容量密度低；SAPC 则以“大容量密度 + 低 ESR + 失效良性”填补二者之间的空档，"
         "适合需要较大容量且低 ESR 的去耦/滤波[2],[5],[89]。")
    body(doc,
         "从可靠性视角，三者的失效机理各异：MLCC 以介质裂纹/绝缘退化与机械应力为主，薄膜电容以金属化层自愈消耗与卷绕老化为主，SAPC 以聚合物退化与界面/湿热失效为主（本章主体）。"
         "因此，系统可靠性设计常以并联组合兼顾各自优势并分散风险（如 MLCC 提供高频去耦、SAPC 提供中频大容量）。"
         "这一互补关系说明：SAPC 的可靠性研究不仅服务于其自身选用，也影响多电容协同架构的整体裕度分配，具有系统层面的意义（2.8.5）。")


def ext_material3(doc):
    heading(doc, "2.3.12  导电聚合物的电-热-湿-机多物理耦合本构", level=3)
    body(doc,
         "SAPC 的退化本质上是多物理场耦合过程，建立耦合本构是失效物理建模的材料学前提。其耦合关系可概括为：温度场经 Arrhenius（式2-5）调制聚合物退化与扩散速率；"
         "湿度场经 Fick 扩散（式2-9）改变含水量，进而经溶胀（力学）拉大颗粒间距、经电化学促进去掺杂/腐蚀（化学）；电场（偏压）经 Poole–Frenkel（式2-10）与电化学过程影响漏电与去掺杂；"
         "力学场（CTE 失配、溶胀应力）驱动界面分层（式2-7类比）。这些场通过聚合物电导 σ（式2-4/2-8）与界面接触电阻汇聚到器件 ESR/LC。")
    body(doc,
         "完整的耦合本构需联立：水分扩散方程、热传导/自热方程（式2-6）、聚合物电导的温-湿-氧依赖、以及界面力学—损伤演化方程，并以器件几何为边界。"
         "求解可采用有限元多物理场仿真，输出 ESR(t)/LC(t) 的时空演化。其难点在于本构参数（扩散系数 D、激活能 Eₐ、溶胀系数、界面黏附强度、损伤动力学常数）的实验标定，"
         "目前面向 SAPC 的此类参数集尚不完整。建立“多物理耦合本构 + 参数标定 + 器件级验证”的链条，是把机理认识升级为预测能力的根本途径，也是本文失效物理建模的方法学骨架（2.6.5、2.11 切入点②）。")


def ext_modes3(doc):
    heading(doc, "2.4.11  退化的阶段划分与时间演化", level=3)
    body(doc,
         "SAPC 的 ESR 退化在时间上常呈现可识别的阶段：①潜伏期——水分扩散/掺杂态轻微变化，ESR 几乎不变或缓升；②稳定退化期——聚合物体电阻与界面接触电阻稳步上升，ESR 近线性或缓加速增长；"
         "③加速期——界面分层扩展、自热正反馈（式2-6）介入，ESR 加速上升直至越过失效阈值（图14、图28）。漏电则可能在稳定期保持低位、在缺陷/迁移触发后骤升（突发特征）。"
         "这种“缓变—加速”的两段/三段特征，正是采用两阶段非线性退化模型（2.6.4、[73]）的物理依据。")
    body(doc,
         "阶段划分对监测与预测具有实际意义：潜伏期与稳定期的早期识别依赖高灵敏指标（ESR 变化率、阻抗谱特征，2.7.4），而加速期的及时预警决定维护窗口（2.7.5）。"
         "若以单一线性外推贯穿全程，将在加速期严重低估退化速率、高估剩余寿命。因此，识别退化阶段、采用分段或非线性退化模型，是提升 SAPC 寿命预测准确性的关键之一，"
         "也呼应了 2.6.17 关于外推风险的讨论。准确刻画各阶段的转折点（拐点）及其与应力的关系，是本文退化建模拟解决的具体问题。")


def ext_mech3(doc):
    heading(doc, "2.5.12  失效机理的多尺度建模思路", level=3)
    body(doc,
         "SAPC 的失效机理跨越分子、纳米晶/界面、器件三个尺度，单一尺度模型难以兼顾机理保真与工程可用。多尺度建模思路是把各尺度模型分层耦合："
         "分子/纳米尺度——以掺杂态化学与颗粒金属/VRH（式2-4）描述电导起源及其对氧/湿/温的响应；介观尺度——以相分离形貌、晶粒间距与界面接触描述电导与接触电阻的演化（式2-3、2-8）；"
         "器件尺度——以分布等效电路（2.2.9）与多物理耦合（2.3.12）把内部状态映射为 ESR/LC，并接入寿命/竞争失效模型（2.6）。")
    body(doc,
         "多尺度耦合的价值在于：既保留机理可解释性与外推能力（来自微观物理），又能输出工程可测的器件参数（用于标定与监测）。"
         "其挑战是跨尺度参数传递与计算代价，常需以“代理模型/降阶模型”在器件级近似微观结果，或以物理信息神经网络（PINN，2.6.6）学习跨尺度映射并嵌入物理约束[83],[84]。"
         "对 SAPC，多尺度建模与物理-数据融合的结合，有望在“机理保真”与“数据可用”之间取得平衡，是机理研究面向预测应用的前沿方向。")


def ext_model4(doc):
    heading(doc, "2.6.18  温-湿-电三应力统一加速模型", level=3)
    body(doc,
         "SAPC 的实际加速试验常同时施加温度、湿度与电压，需要能统一表达三应力及其交互的模型。在广义 Eyring 框架下，可写出失效时间（或退化速率）的统一形式：")
    equation(doc, "ln t_f = a + Eₐ/(k_B T) − n·ln(RH) − γ·V + δ·(1/T)·g(RH,V)", "2-21")
    body(doc,
         "式中前几项分别对应 Arrhenius（温度）、Peck（湿度）与电压加速，末项表达应力间交互（如温度对湿度敏感性的调制）。"
         "该统一模型可由多维应力的析因/最优试验（2.6.16）联合标定，避免逐应力单独标定时忽略交互导致的外推偏差。"
         "需注意，三应力模型参数更多、对数据量与试验设计要求更高，且仍受“机理不变”假设约束（2.6.11）；其价值在于更真实地表达 SAPC 多应力服役条件，是经验模型走向工程实用的必要扩展。")
    body(doc,
         "在与失效物理结合时，式(2-21)的各应力项可由 PoF 内层过程（式2-8/2-9/2-10）导出而非纯经验拟合，从而获得物理约束的参数与更稳健的外推。"
         "这种“经验形式 + 物理约束 + 联合标定”的混合策略，是本文加速建模的候选方案，兼顾工程可用性与机理可信度。")

    heading(doc, "2.6.19  可靠性建模的总体流程", level=3)
    body(doc,
         "综合 2.6 各节，可把面向 SAPC 的可靠性建模整理为一条可操作的总体流程：①失效模式与机理辨识（2.4、2.5，确定退化变量 ESR/LC 与机理）；"
         "②加速试验设计与数据采集（2.6.1、2.6.16，多应力多水平 + 多参数监测）；③退化/寿命模型选择（统计/随机过程/PoF/数据驱动，2.6.2–2.6.6）；"
         "④参数估计与不确定性量化（2.6.10、2.6.17，含批次分散的分层贝叶斯）；⑤竞争失效集成（2.6.7、2.6.15，多路径联合）；"
         "⑥模型验证与外推风险控制（2.6.11，内插/外推区分、机理一致性确认）；⑦面向应用的寿命/RUL 评估（2.7、2.8，任务剖面 + 在线更新）。")
    body(doc,
         "该流程把分散的方法组织为闭环：数据→模型→不确定性→验证→应用→（监测反馈再更新）。其核心理念是“物理为骨、数据为肉、统计为度”——"
         "以失效物理保证结构与外推、以数据保证拟合与适配、以统计/贝叶斯保证不确定性与决策。本文后续章节即沿此流程展开，针对 SAPC 的具体特点逐环节落实并验证。")


def ext_monitor3(doc):
    heading(doc, "2.7.7  传感器配置、可观测性与折算", level=3)
    body(doc,
         "在线监测的有效性首先取决于“可观测性”：在给定传感配置下，健康指标是否可由可测量唯一、稳健地反演。对 SAPC，ESR/C 的辨识依赖纹波电压与电流的同步测量与相位分辨，"
         "传感器带宽、采样率、同步精度与抗噪能力直接决定辨识精度（2.7.2、2.7.6）。在变换器中复用既有传感时，还需考虑开关噪声、寄生参数与工况扰动对辨识的干扰。")
    body(doc,
         "温度/频率折算是另一关键：由于 ESR 随温度与频率变化（2.2.9），监测得到的原始 ESR 必须折算到统一参考条件，才能分离可逆（工况）效应与不可逆（退化）效应（2.4.8、2.7.4）。"
         "这要求同时获取或估计器件温度（或热点温度，式2-6），并已知测量频率。可观测性与折算的不足是 SAPC 在线监测“伪退化/伪健康”误判的主要来源；"
         "提升传感配置与折算精度、必要时引入冗余测量与软测量（状态观测器），是保障 RUL 预测可信度的工程基础。")


def ext_app3(doc):
    heading(doc, "2.8.7  典型电路中的 SAPC 失效后果分析", level=3)
    body(doc,
         "把器件失效置于电路语境，有助于评估 SAPC 退化的系统后果与安全等级。在开关电源输出滤波/去耦中，ESR 上升会增大输出纹波与瞬态压降、加剧自身与邻近器件的温升，"
         "可能触发控制环路裕度下降乃至振荡；漏电增大则增加静态损耗、抬高待机功耗，极端时短路导致供电中断。在 DC-link 中，电容退化会削弱母线电压支撑能力、增大母线纹波，"
         "对功率半导体与负载形成二次应力（2.8.5）。")
    body(doc,
         "从失效安全性看，SAPC 的良性失效特征（不燃爆，2.4.6）使其在过应力下的系统后果通常可控，这是其相对 MnO₂ 钽电容的安全优势[14],[59],[64]。"
         "但“良性”不等于“无后果”：参数退化引起的纹波/温升耦合仍可能诱发系统级故障。因此，系统级 FMEA 应把 SAPC 的 ESR 上升、LC 增大与开路/短路分别评估其对电路功能、效率与安全的影响，"
         "并据此设定监测阈值与冗余策略。这一“器件失效—电路后果—系统决策”的贯通，是 SAPC 可靠性研究服务于整机可靠性的落点（2.7.5、2.8.5）。")


def ext_cases2(doc):
    heading(doc, "2.9.8  文献定量结果的对照与解读", level=3)
    body(doc,
         "为便于横向把握量级，表22对若干公开研究中报道的定性/半定量结果作对照解读（具体数值以原文为准，此处仅作量级与趋势的归纳，并已改写表述）。"
         "需特别提醒：由于失效判据、测试频率/温度、样本与批次不一致（2.4.8、2.5.11），跨研究的数值不可直接相互换算，对照仅用于把握总体趋势与机理一致性。")
    add_table(doc, 22, "代表性研究的定性/半定量结果对照（量级与趋势）",
              ["研究/对象", "应力", "观测趋势（改写转述）", "机理归因", "文献"],
              [["PA 电容(湿热)", "85/85+偏压", "ESR 升高、LC 增大、C 稳定", "去掺杂+界面+杂质", "[9]"],
               ["多层 PA(双温)", "85/85、110/85", "失效时间随温度升高而缩短", "温度加速湿热退化", "[10]"],
               ["CPTC(高温存储)", "高温", "电阻率随老化近指数增长", "热-氧化", "[42],[43]"],
               ["PEDOT:PSS 膜", "热+气氛", "电导随时间指数下降、氧加速", "颗粒收缩+氧化", "[17],[18]"],
               ["PEDOT:PSS 膜", "湿度", "光学厚度随 RH 大幅增加(溶胀)", "吸湿溶胀", "[52]"],
               ["聚合物钽(过流)", "破坏性过流", "良性失效、无燃爆", "聚合物隔离击穿点", "[14],[59]"]],
              widths=[2.6, 2.0, 3.6, 2.6, 1.6], fs=8.4,
              source_cn="注：均为对公开文献的改写转述，数值与条件以原文为准；不同研究间不可直接换算。")
    body(doc,
         "对照可见三点一致性：①湿热下普遍“ESR↑、LC↑、C 稳定”，且温度加速失效（[9],[10]）；②高温/热老化下 ESR 随时间近指数增长，指向热-氧化机理（[17],[18],[42]）；"
         "③过流下良性失效，体现聚合物自愈隔离的安全优势（[14]）。这些一致性强化了本章对失效模式与机理的判断（2.4、2.5）；"
         "而数值的不可直接换算，则再次印证了“统一规程下 SAPC 专用数据集”的必要（2.11 切入点①）。")



# __MAIN_RESTORED__



# ================= 深化批次四：表征/封装/界面/自愈/数据/推导/指标/相关性/空白 =================
def ext_material4(doc):
    heading(doc, "2.3.13  导电聚合物老化的光谱学表征与指认", level=3)
    body(doc,
         "把“退化”落到可测的化学/结构变化上，需要光谱学表征的明确指认。对 PEDOT 体系，常用三类光谱互为印证："
         "①拉曼光谱（Raman）——噻吩环对称伸缩等特征峰的位置与相对强度对掺杂态敏感，去掺杂/氧化会引起特征峰位移与极化子/双极化子带相对强度变化，可用于判别掺杂水平的下降；"
         "②红外光谱（FTIR/ATR-FTIR）——可追踪乙撑二氧基团、磺酸基与可能的氧化产物（如羰基）的生成，指认氧化降解；"
         "③X 射线光电子能谱（XPS）——S 2p、O 1s 等谱峰可区分 PEDOT 与 PSS 的硫物种比例与氧化态，量化对阴离子分布与去掺杂程度[23],[40],[92]。")
    body(doc,
         "在器件失效分析中（2.5.6），这些光谱学手段与 SEM/TEM 形貌、EDS 成分互补：形貌给出“在哪退化”（界面/晶粒），光谱给出“如何退化”（氧化/去掺杂），"
         "EDS/XPS 给出“何物参与”（杂质/对阴离子）。通过老化前后光谱的对照，可把宏观 ESR/LC 退化与具体化学过程关联起来，为退化动力学（式2-8）与多物理本构（2.3.12）提供标定证据。"
         "需要指出，光谱指认须谨慎排除制样与环境干扰，并以多手段交叉验证，避免单一谱学的过度解读——这也是 SAPC 机理研究中保证结论可靠性的方法学要求。")


def ext_modes4(doc):
    heading(doc, "2.4.12  封装形式与尺寸对失效行为的影响", level=3)
    body(doc,
         "SAPC 的失效行为不仅取决于材料，也受封装形式与器件尺寸调制。封装的阻湿能力（环氧体系、密封工艺、引出端结构）直接决定水分扩散的时间尺度（式2-9），"
         "是湿热失效快慢的关键外因（2.5.2）[10],[12]；封装与内部各材料的 CTE 失配程度则决定温度循环下的界面应力与分层倾向（式2-7）。"
         "器件尺寸方面，较大尺寸在温度循环下焊点承受更大 CTE 失配应变，焊点疲劳寿命往往更短[81]；而较大体积也意味着更长的水分扩散路径，可能延缓湿热退化——两种尺寸效应方向相反，需具体权衡。")
    body(doc,
         "叠层片数与几何还影响热阻网络（式2-6）与自热：片数增多提升容量但也可能改变散热路径与热点分布，进而影响热-电耦合退化。"
         "因此，SAPC 的可靠性数据须标注封装与尺寸信息，跨封装/跨尺寸的结论不可简单外推（与 2.5.11 批次分散的提醒一致）。"
         "从设计角度，封装阻湿强化、界面黏附改善与合理的尺寸/片数选择，是与材料改性、降额并列的器件级可靠性手段；本文在数据集构建时将把封装/尺寸作为重要协变量记录与分析。")


def ext_mech4(doc):
    heading(doc, "2.5.13  水分—电场—应力的界面协同电化学", level=3)
    body(doc,
         "湿热偏压下，聚合物/氧化膜界面是多因素协同的电化学反应场。水分到达界面后形成连续水膜，使界面具备电解质环境；直流偏压在界面建立电场与电位差；"
         "热与溶胀应力则改变界面接触状态与缺陷分布。三者协同可驱动：①阳极侧的金属氧化与离子化（为电化学迁移提供离子源，2.5.8）；②PEDOT 的电化学去掺杂（还原使载流子减少）；"
         "③Al₂O₃ 的局部溶解/水合与缺陷生成（抬高漏电）。这些过程相互促进，构成湿热偏压失效的“界面电化学引擎”。")
    body(doc,
         "该协同机制解释了为何“湿 + 偏压”的组合远比单独湿或单独偏压更具破坏性：水膜提供介质、偏压提供驱动、温度提供活化，缺一则反应受限。"
         "它也解释了降额（降低界面电场）、阻湿封装（切断水膜）与去质子（降低酸性催化）三类措施的有效性各自针对协同链条的不同环节。"
         "对建模而言，界面电化学协同意味着 ESR 路径（界面接触退化）与 LC 路径（介质缺陷/迁移）存在共同的界面诱因，故二者相关（2.6.15 多元退化相关性的物理来源），"
         "这为竞争失效的相关性建模提供了机理依据。")

    heading(doc, "2.5.14  自愈机制的物理模型与极限", level=3)
    body(doc,
         "导电聚合物的自愈是 SAPC 失效良性与漏电抑制的关键，但其能力有限，需理解其物理模型与极限。自愈的基本机制是：当某缺陷处漏电增大、局部发热时，"
         "该处的导电聚合物因热分解/氧化而高阻化，从而“断开”并隔离该缺陷，阻止漏电进一步扩大（2.5.3）[25],[59]。这一“热触发的局部高阻化”可建模为："
         "缺陷处功率密度超过阈值时聚合物电导骤降，等效于在漏电通道串入高阻，使该通道电流自限。")
    body(doc,
         "其极限在于：①隔离以牺牲局部阴极面积为代价，多次自愈累积会减小有效面积、抬高 ESR（自愈与 ESR 退化此消彼长）；"
         "②当缺陷密度过高或界面已大面积分层时，可隔离的“孤立缺陷”假设失效，漏电连成片而无法自限，趋于短路；"
         "③固态体系缺乏液态电解液的持续供氧再形成，介质本身的修复能力弱于液态铝电解（2.5.3）[3],[87]。因此，SAPC 的自愈是“有限、消耗性”的，"
         "其裕度取决于缺陷密度与界面完整性。把自愈的“生成—隔离”竞争纳入 LC 路径动力学（2.5.7），是定量预测漏电型失效与失效安全性的关键，也是本文机理建模的组成部分。")


def ext_model5(doc):
    heading(doc, "2.6.20  数据驱动建模的特征构造与标签", level=3)
    body(doc,
         "数据驱动/物理-数据融合方法的效果在很大程度上取决于特征与标签的构造。对 SAPC 的 RUL 预测，输入特征通常包括：折算后的 ESR/C/LC 及其变化率、"
         "阻抗谱派生特征（界面弧半径、特征频率、相位）、工况变量（温度、纹波、偏压）及其统计量（均值、方差、峰值）、以及时间/累积应力（累积热当量、累积湿当量）。"
         "标签（监督目标）则可为 RUL 真值（试验中已知失效时刻时）或健康指标的未来值（用于先预测退化再外推至阈值）。良好的特征工程（2.7.4）能显著降低对数据量的需求并提升泛化。")
    body(doc,
         "针对“长周期数据稀缺”的核心困难（2.10），可行策略包括：①以物理特征（来自 PoF/退化动力学）替代部分纯统计特征，提升小样本泛化；"
         "②数据增强与仿真数据预训练（以多物理仿真，2.3.12，生成退化轨迹预训练模型，再以少量实测微调）；③物理约束正则（PINN，把式2-8/2-9 作为损失项约束网络，2.6.6）[83],[84]。"
         "这些策略的共同点是“以物理知识弥补数据不足”，契合 SAPC 的现状，是本文物理-数据融合路线的具体技术手段。")

    heading(doc, "2.6.21  迁移学习与小样本 RUL 预测", level=3)
    body(doc,
         "SAPC 缺乏大规模专用退化数据，但相关器件（聚合物钽、液态/混合铝电解）与相近工况存在可迁移知识，迁移学习因而具有吸引力。"
         "其思路是：在数据较充分的源域（如聚合物钽高温老化[42]、或多物理仿真数据）训练退化/RUL 模型，再以少量 SAPC 实测数据做域适配（微调、特征对齐或参数先验迁移）。"
         "物理-数据融合天然支持迁移：物理部分（机理动力学）跨器件可迁移性强，数据部分负责适配器件特异性。")
    body(doc,
         "迁移的风险在于源域与目标域机理差异（如钽与铝的介质/界面不同，2.9.4），盲目迁移可能引入偏差；稳健做法是迁移“机理形式”（如指数退化、VRH、竞争失效结构）而审慎迁移“数值参数”，"
         "并以目标域数据验证。分层贝叶斯（2.6.8、2.6.14）提供了一种自然的迁移框架：以源域信息构造先验、以目标域数据更新后验，在“借力”与“适配”间自动权衡。"
         "对 SAPC，迁移学习与物理先验、分层贝叶斯的结合，是在小样本下获得可信 RUL 的现实路径，也是本文方法的候选要素。")

    heading(doc, "2.6.22  Gamma 过程首达与逆高斯 RUL 的推导要点", level=3)
    body(doc,
         "为增强可操作性，简述两类退化过程 RUL 的推导要点。对 Wiener 过程（式2-16），退化 X(t)=x₀+μt+σ_B B(t) 首次到达阈值 D 的时间 T 服从逆高斯分布，其密度为式(2-18)，"
         "均值 ν=(D−x₀)/μ、参数 λ=(D−x₀)²/σ_B²。给定当前时刻 t_p 的退化量 x_p，剩余寿命 L=T−t_p 的密度可由把阈值改为 D−x_p、起点设为 0 重新代入式(2-18)得到：")
    equation(doc, "f_L(ℓ) = (D−x_p) / sqrt(2π σ_B² ℓ³) · exp[ −( (D−x_p) − μℓ )² / (2 σ_B² ℓ) ]", "2-22")
    body(doc,
         "对 Gamma 过程（式2-17），由于增量严格为正且独立，剩余退化 X(t_p+ℓ)−X(t_p) 服从形状 αℓ、尺度 1/β 的 Gamma 分布，"
         "故 RUL 的累积分布为 P(L≤ℓ)=P(剩余退化≥D−x_p)=1−G(D−x_p; αℓ, β)，其中 G 为 Gamma 累积分布函数。该式无初等闭式，"
         "实际中以数值积分、Birnbaum–Saunders 或鞍点近似求解，并可在共轭先验下做在线贝叶斯更新（2.6.14）[74]。"
         "两类推导表明：RUL 本质上是“首达时分布”，其不确定性（分布宽度）随退化随机性（σ_B 或 α,β）与剩余裕度（D−x_p）而定——这为不确定性量化（2.6.17）提供了解析支撑。")


def ext_monitor4(doc):
    heading(doc, "2.7.8  RUL 预测评价指标的数学定义", level=3)
    body(doc,
         "为使 RUL 预测可量化比较，需明确评价指标的数学定义。设第 k 次预测时刻 t_k 的 RUL 预测为 r̂_k、真值为 r_k，误差 Δ_k=r̂_k−r_k。常用指标包括：")
    bullet(doc, "均方根误差 RMSE = sqrt( (1/N) Σ Δ_k² )、平均绝对误差 MAE = (1/N) Σ |Δ_k|，刻画总体精度。")
    bullet(doc, "预测时域(Prognostic Horizon, PH)：自预测首次稳定落入真值 ±α 容差带起，到失效的提前量；PH 越长越好。")
    bullet(doc, "α–λ 精度：在各预测时刻，预测是否落入真值的 ±α(相对)带内；以满足比例衡量随寿命推进的可靠性。")
    bullet(doc, "收敛性(Convergence)：误差随预测推进收敛于 0 的速度，常以误差曲线下面积的质心量化。")
    body(doc,
         "此外，考虑“晚预测（高估 RUL）比早预测更危险”的非对称性，可用非对称评分（如指数惩罚晚预测重于早预测）：S=Σ [exp(a·Δ_k)−1]（对 Δ_k>0 取较大 a）。"
         "对 SAPC 这类安全相关器件，应综合 RMSE/MAE（精度）、PH 与 α–λ（及时性与持续可靠性）、以及非对称评分（安全偏好）多指标评价，而非单一 RMSE[93],[94]。"
         "明确这些定义，既便于本文与文献方法的公平比较，也为工程上设定“何时预警、何时维护”的阈值（2.7.5）提供量化依据。")


def ext_app4(doc):
    heading(doc, "2.8.8  加速试验与现场可靠性的相关性", level=3)
    body(doc,
         "加速试验的最终目的是预测现场（field）可靠性，二者的相关性是方法可信度的试金石。建立相关性的前提是“失效机理一致”（2.6.11）："
         "只有当加速条件激发的机理与现场相同时，加速因子（式2-11/2-13/2-21）才有意义。验证机理一致性的手段包括：对加速与现场失效样品做对照失效分析（2.5.6），"
         "比较失效模式占比、形貌与化学指认（2.3.13）是否吻合；以及检验加速数据外推与现场返修/退役数据是否统计一致。")
    body(doc,
         "现实困难在于：现场数据往往稀缺、噪声大、工况多变且记录不全（任务剖面未知或粗略，2.8.4），使相关性验证困难。应对策略包括："
         "①以任务剖面把现场变应力折算为等效应力，再与加速条件比较；②以贝叶斯方法融合加速试验先验与少量现场数据更新可靠性后验（2.6.8）；"
         "③以在线监测（2.7）获取现场退化轨迹，直接验证/校正寿命模型。对 SAPC，建立“加速—现场”相关性是把实验室结论转化为工程置信的关键一环，"
         "也是本文“面向应用验证”（2.11 切入点⑤）的核心内容之一。")


def ext_cases3(doc):
    heading(doc, "2.10.1  研究空白的结构化映射", level=3)
    body(doc,
         "为使“缺口”可操作，表23以“研究维度 × 成熟度”的结构化矩阵呈现 SAPC 可靠性研究的空白分布，作为 2.11 不足分析的量化支撑。"
         "矩阵把现状判断从文字归纳提升为可视的优先级地图：成熟度低且重要性高的格子，即为最值得投入的研究空白。")
    add_table(doc, 23, "SAPC 可靠性研究的空白结构化映射（成熟度自评：低/中/高）",
              ["研究维度", "材料机理", "器件级数据", "建模方法", "监测/RUL", "标准/应用"],
              [["湿热", "中—高", "中", "中", "中", "中"],
               ["纯高温/长周期", "中", "低", "中", "低", "低"],
               ["热-电-机械耦合", "中", "低", "低", "低", "低"],
               ["多机理竞争", "中", "低", "低", "低", "低"],
               ["不确定性量化", "—", "低", "中", "低", "低"]],
              widths=[2.8, 2.2, 2.2, 2.2, 2.2, 2.2], fs=8.6,
              source_cn="注：成熟度为基于本章文献的定性自评，用于指示优先级，非严格计量。")
    body(doc,
         "由表23可见，成熟度“低”集中于“纯高温/长周期、热-电-机械耦合、多机理竞争”三行与“器件级数据、监测/RUL、标准/应用”三列的交叉区——"
         "这正是 SAPC 可靠性研究最迫切的空白，与 2.11 凝练的五点不足高度一致，也直接界定了本文的优先研究方向与资源投放重点。"
         "需说明，该矩阵为基于本章证据的定性自评，旨在提供优先级地图而非精确计量；随着更多研究出现，应动态更新。")



# __MAIN_RESTORED5__



# ================= 深化批次五：工艺/二次掺杂/可逆性/杂质/验证/融合/异常/LCC =================
def ext_device4(doc):
    heading(doc, "2.2.11  制造工艺的关键控制点、良率与可靠性筛选", level=3)
    body(doc,
         "SAPC 的可靠性在很大程度上是“制造出来的”，工艺一致性直接决定批次的失效分布（2.5.11）。从可靠性角度，制造链上的关键控制点包括："
         "①蚀刻——隧道孔/海绵孔的密度与均一性决定有效面积与孔道可填充性，过度蚀刻会削弱机械强度、欠蚀刻则限制容量与填充深度；"
         "②化成——氧化膜厚度与缺陷密度决定耐压与漏电基线，化成不充分会留下薄弱点（漏电与击穿源）；"
         "③聚合物填充——深孔填充完整性与界面接触质量决定 ESR 基线与退化裕度，填充不良在深孔处留下高阻/空洞；"
         "④石墨/银浆与封装——决定引出电阻、银迁移阻挡与阻湿能力。")
    body(doc,
         "上述控制点的波动会沿“缺陷→早期失效”链条放大，表现为浴盆曲线的婴儿期（图24）。工程上以统计过程控制（SPC）约束关键参数波动、以加电老化（burn-in）与电气分选剔除早期失效弱点[50],[75]，"
         "并以破坏性物理分析（DPA）抽检验证内部质量。NASA NEPP 在高可靠选用中正是以 DPA、失效史与可靠性趋势作为评估依据（2.8.2）[15]。"
         "对研究而言，理解工艺控制点—缺陷—失效的对应，有助于在数据集中把“工艺/批次”作为协变量显式建模（2.5.11、2.4.12），从而区分“器件本征退化”与“工艺缺陷诱发失效”，"
         "避免把可筛除的早期失效误当作本征磨损规律。")
    body(doc,
         "良率与可靠性并非独立：高良率往往对应低缺陷密度与窄分布，进而对应更长、更一致的寿命。因此，可靠性提升与良率提升在“缺陷控制”这一共同根因上是统一的。"
         "这也提示，SAPC 可靠性研究若脱离对制造一致性的把握，将难以解释批次间差异、亦难以把实验室结论稳健外推到量产器件——这是 2.11 强调“含批次标识数据集”的工程理由。")


def ext_material5(doc):
    heading(doc, "2.3.14  二次掺杂与电导增强的机理细化", level=3)
    body(doc,
         "PEDOT:PSS 的初始电导有限，二次掺杂（secondary doping）是大幅提升电导的关键，其机理与 SAPC 的 ESR 基线及稳定性密切相关。"
         "常用手段包括：①极性有机溶剂（如二甲基亚砜 DMSO、乙二醇 EG）处理——通过屏蔽/重排 PEDOT⁺ 与 PSS⁻ 间的库仑作用、促进 PEDOT 链的构象由卷曲转为扩展、并诱导相分离与结晶，"
         "从而缩短颗粒间跳跃距离、降低跳跃势垒（式2-4），电导可提升一到两个数量级[20],[21]；②酸处理/后处理——部分去除绝缘 PSS 壳、富集导电 PEDOT；"
         "③离子液体与表面活性剂——调控形貌与界面[21],[66]。其共同机理可统一到 2.3.2 的颗粒金属/VRH 图像：增强电导即“增大导电晶粒、减薄绝缘壳、缩短间距、降低 T₀”。")
    body(doc,
         "高电导自掺杂 PEDOT 的研究进一步揭示，提高分子量可增加纳米晶数量、缩短相邻晶粒间距并降低跳跃激活能，使体电导超过 1000 S·cm⁻¹[68]；"
         "层级结构研究亦表明减薄 PSS 壳、促进结晶与颗粒聚集可同时改善颗粒内/间输运[69]。这些机理对 SAPC 的可靠性具有双重含义："
         "一方面，更高、更稳定的初始电导意味着更低的 ESR 基线与更大的退化裕度；另一方面，二次掺杂带来的形貌/结晶态在热、湿、氧作用下若发生回复（去结晶、相分离粗化、再吸湿），"
         "则电导会回落、ESR 上升——即“增强”与“退化”是同一形貌自由度的正反两面。")
    body(doc,
         "因此，从可靠性设计看，理想的聚合物阴极不仅要“初始电导高”，更要“形貌/掺杂态在服役应力下稳定”。这把材料优化目标从单纯“提电导”转向“电导—稳定性协同”，"
         "并解释了去质子、稳定对阴离子、强界面黏附等措施的价值（2.3.6、2.3.9）。把二次掺杂机理与退化动力学（式2-8）统一在形貌自由度下，是 SAPC 失效物理建模的材料学闭环，"
         "也是材料—器件协同优化的理论依据。")


def ext_modes5(doc):
    heading(doc, "2.4.13  失效的可逆性、恢复与再形成", level=3)
    body(doc,
         "并非所有参数漂移都是不可逆退化，区分可逆与不可逆变化对正确判定失效与设定监测折算至关重要（2.7.4）。可逆变化主要包括："
         "①温度/频率引起的 ESR、C 变化——随工况恢复（2.2.9），应折算消除；②适度吸湿引起的部分电导下降——在干燥后可部分恢复（溶胀部分可逆）；"
         "③轻度去掺杂在一定条件下的部分回复。不可逆变化则包括：聚合物氧化降解、晶粒收缩、界面分层、介质缺陷生成与电化学迁移等（2.5）。"
         "把可逆分量误判为退化（伪退化）或反之（伪健康），都会损害寿命预测的准确性。")
    body(doc,
         "在介质层面，液态铝电解电容依靠电解液持续供氧实现氧化膜的“再形成（reforming）”，使存储期漏电增大可被加电恢复[3],[87]；"
         "而固态 SAPC 缺乏此通道，其漏电恢复主要依赖聚合物在缺陷处的高阻隔离（自愈，2.5.3、2.5.14），可逆裕度小。"
         "这一差异意味着 SAPC 的漏电一旦显著增大，往往难以通过简单加电恢复，更接近不可逆失效——这是其漏电可靠性需重点监测的原因（2.4.1）。"
         "理解可逆/不可逆的边界，既指导失效判据的设定（应基于不可逆分量，2.4.8），也指导监测数据的预处理与折算（2.7.4、2.7.7），是连接“测量”与“健康状态”的认识基础。")


def ext_mech5(doc):
    heading(doc, "2.5.15  杂质与缺陷的来源、检测与控制", level=3)
    body(doc,
         "杂质与缺陷是 SAPC 漏电与早期失效的重要诱因，其来源贯穿原材料与制造全程：原材料带入（铝箔夹杂、聚合物单体/氧化剂杂质）、"
         "工艺引入（蚀刻/化成残留、聚合物聚合副产物与残留金属离子、环境颗粒污染）、以及装配引入（焊接/搬运污染）。"
         "CALCE 在器件中发现的铁颗粒高漏电机理[9]即为原材料/工艺金属污染的典型例证（2.5.4、2.3.11）。这些杂质或直接成为漏电/迁移源，或催化聚合物氧化老化，从而抬高 LC 与加速 ESR 退化。")
    body(doc,
         "检测手段上，杂质与缺陷可通过：漏电流筛选（识别异常高漏电个体）、X 射线/C-SAM（探测颗粒、空洞、分层）、SEM/EDS 与 XPS（定位并鉴别杂质元素与化学态，2.5.6、2.3.13）等加以识别。"
         "控制手段则包括：原材料纯度管控、聚合后充分清洗去除残留氧化剂/离子、洁净产线与环境控制、以及加电老化/分选剔除高漏电弱点（2.2.11）。")
    body(doc,
         "从研究方法看，杂质/缺陷的随机性是失效分散与早期失效的重要来源（2.5.11），应以极值/最弱环节统计（Weibull，2.5.10）而非均值描述其影响。"
         "在建模中，可把“缺陷诱发的漏电路径”作为竞争失效的一条独立路径（2.6.15），其触发具有随机性与批次依赖性。"
         "因此，杂质控制既是工程上降低早期失效的手段，也是研究上正确解释漏电分散、避免把“可控缺陷失效”误作“本征机理”的认识前提。")


def ext_model6(doc):
    heading(doc, "2.6.23  模型验证、基准与可复现性", level=3)
    body(doc,
         "可靠性模型的可信度取决于验证的严格性与结果的可复现性。验证应遵循若干原则：①数据划分须防泄漏——退化序列按“器件/单元”而非按“样本点”划分训练/测试，"
         "避免同一器件的早晚数据分别进入训练与测试而高估性能；②以时间因果方式评估——仅用 t_p 之前的数据预测之后的 RUL，模拟真实在线场景；"
         "③区分内插与外推——重点报告向使用条件外推的性能（2.6.11）；④多指标评价——综合精度、预测时域与不确定性校准（2.7.8）。")
    body(doc,
         "基准化（benchmark）与可复现性是领域成熟的标志。锂电池领域因有公开退化数据集而方法可比、进展迅速；SAPC 则因缺乏公开数据集而难以横向比较（2.10、2.12.2）。"
         "因此，建立公开、标注完备（应力、批次、判据、频率/温度）的 SAPC 退化基准数据集，并配套统一的评价协议与代码，是推动方法可复现、可比较的基础工作。"
         "本文在构建专用数据集时将遵循上述验证与可复现原则，并尽可能开放数据与评价协议，以利后续研究在同一基准上改进。")

    heading(doc, "2.6.24  经验—物理—数据三类模型的融合架构", level=3)
    body(doc,
         "综合 2.6 全节，可提出一种面向 SAPC 的三层融合架构，作为方法论的收口：底层为失效物理（PoF）层——以多物理耦合本构（2.3.12）与退化动力学（式2-8/2-9/2-10）描述机理，提供结构与外推骨架；"
         "中层为统计/随机过程层——以退化随机过程（式2-16/2-17）与竞争失效（式2-19、2.6.15）刻画分散性、相关性与 RUL 分布，并以分层贝叶斯（式2-20）表达个体差异与不确定性；"
         "上层为数据驱动层——以机器学习/PINN（2.6.6）拟合残差与复杂非线性、并以物理约束保持一致性（2.6.20）。")
    body(doc,
         "三层之间双向耦合：物理层为数据层提供特征与约束、为统计层提供模型结构；数据层与统计层则以观测校正物理层参数（在线贝叶斯更新，2.6.14）。"
         "这一架构的优势是“物理保外推、统计保分散、数据保拟合”，恰好弥补单一方法的短板（表17），尤其契合 SAPC“机理较清、数据稀缺、分散较大”的特点。"
         "本文后续建模即以此融合架构为蓝本，分层实现并以专用数据集验证，力求在可解释性、外推能力与预测精度之间取得平衡。")


def ext_monitor5(doc):
    heading(doc, "2.7.9  监测不确定性、异常检测与鲁棒性", level=3)
    body(doc,
         "在线监测面临测量噪声、工况扰动、传感漂移与异常事件，监测系统的鲁棒性直接影响 RUL 预测的可信度。监测不确定性可分为："
         "随机噪声（可由滤波/平滑抑制，2.7.4）、系统偏差（需校准与折算，2.7.7）与异常/离群（需检测并隔离）。异常检测可基于统计阈值（如残差超过若干倍标准差）、"
         "基于模型（预测值与观测值偏差）或基于学习（无监督离群检测），用于区分“真实突变退化（如缺陷触发漏电骤升）”与“测量异常/工况扰动”。")
    body(doc,
         "鲁棒性策略包括：冗余测量与传感器融合、软测量（状态观测器估计不可直接测量的内部状态）、以及对模型与数据的一致性检查（物理约束可作为异常判据，如 ESR 不应随时间下降，违背则提示测量异常）。"
         "对 SAPC 极低 ESR 的监测（2.7.2、2.7.6），噪声与漂移对相对退化量的影响被放大，鲁棒的异常检测与不确定性管理尤为重要。"
         "把监测不确定性显式传播到 RUL（2.6.17），并以异常检测保障输入数据质量，是实现可信在线 PHM（2.12.4）的前提，也是本文监测—预测一体化设计的要求。")


def ext_app5(doc):
    heading(doc, "2.8.9  全生命周期成本与可持续性考量", level=3)
    body(doc,
         "可靠性最终服务于全生命周期价值，故需把成本与可持续性纳入视野。从全生命周期成本（LCC）看，电容器的总成本不仅是采购价，还包括失效导致的停机、维修与召回成本；"
         "SAPC 虽单价高于液态铝电解，但其低 ESR（降低损耗与温升）、长寿命与失效良性可降低运行与失效成本，在数据中心、汽车等高可用场景往往具有更优的 LCC[5],[88],[89]。"
         "准确的可靠性/RUL 预测（2.6、2.7）通过支撑预测性维护（2.7.5）进一步压缩维护成本与停机损失，是 LCC 优化的关键杠杆。")
    body(doc,
         "从可持续性看，更长的寿命意味着更少的更换与电子废弃物；更低的 ESR 与损耗意味着更高的能效。固态聚合物体系不含液态电解液，避免了泄漏与干涸相关的环境与安全问题（2.2.8）。"
         "但聚合物与封装材料的可回收性、以及制造过程的环境足迹仍需关注。把可靠性、成本与可持续性统一考量，意味着 SAPC 研究的价值不止于“延长单个器件寿命”，"
         "而在于“以可信的可靠性预测优化整机的全生命周期价值与环境影响”。这一更宏观的定位，为本文的工程意义提供了更完整的注脚（2.7.5、2.8.5）。")



# __MAIN_RESTORED6__



# ================= 深化批次六：边界/板级/热机械/工况矩阵/FTA/敏感性/删失/边缘/标准/研究问题 =================
def ext_intro3(doc):
    heading(doc, "2.1.6  研究边界、排除项与本综述的限制", level=3)
    body(doc,
         "为使综述结论的适用范围明确，须界定研究边界与排除项。本章聚焦“以导电聚合物为固态电解质的叠层铝固态电容器（SAPC）”的可靠性，"
         "重点为失效模式、机理、建模与监测；对以下内容仅在必要时触及而不展开：①导电聚合物的合成工艺优化与电化学催化等纯材料化学细节；"
         "②器件的纯电气设计与电路应用拓扑（仅在影响可靠性时讨论，如纹波自热、降额）；③与可靠性弱相关的封装机械结构设计；"
         "④非铝体系（钽、铌、陶瓷、薄膜）仅作可迁移机理/方法的类比对象（2.1.2、2.2.10）。")
    body(doc,
         "本综述自身亦存在限制，需诚实说明：①公开文献对 SAPC 的器件级长周期、多应力数据本就稀缺（2.10），故部分判断借助高度同构的聚合物钽器件类比，存在迁移误差风险（2.6.21、2.9.4）；"
         "②厂商技术资料虽提供工程证据，但其试验细节与统计深度有限，引用时已注明（如[12],[13],[88],[89]）；"
         "③本章未纳入需授权的原始图件，相关形貌/谱学证据以附录 A 的可溯源出处替代（编制说明）；"
         "④文献计量（2.10、图1/图2）基于本章精选集而非全库检索，意在反映总体格局而非穷举。明确这些边界与限制，有助于读者恰当理解本章结论的强度与适用范围，"
         "也提示后续工作应以一手实验数据补强类比与厂商证据的不足。")


def ext_device5(doc):
    heading(doc, "2.2.12  引出端、可焊性与板级可靠性", level=3)
    body(doc,
         "SAPC 作为 SMD 器件，其可靠性不止于元件本体，还包括引出端与板级互连。引出端结构（端电极材料、镀层、与银浆/石墨的连接）决定引出电阻（ESR 的一部分，式2-3）与长期接触稳定性；"
         "镀层的可焊性与抗氧化性影响焊接质量，进而影响焊点可靠性。板级方面，回流焊的热冲击、焊点的 CTE 失配与温度循环疲劳（式2-7、2.4.5）是失效的重要来源，"
         "贴片无源器件焊点疲劳寿命受器件尺寸、焊点高度与焊料体积影响[81]。")
    body(doc,
         "板级可靠性与元件可靠性相互耦合：焊点退化（接触电阻增大）会叠加到器件 ESR 上，难以在电学上简单区分二者；而器件内部界面分层与外部焊点疲劳的失效表现（ESR 上升→开路）相似，"
         "需借助 X 射线/C-SAM 与截面分析加以区分（2.5.6）。因此，SAPC 的可靠性评估应在“元件级 + 板级”两个层面协同进行，加速试验（尤其温度循环）需在代表性板级组装条件下开展，"
         "方能反映真实失效。这一“元件—板级”耦合也提示，状态监测（2.7）所测 ESR 实为“器件本体 + 引出 + 焊点”的串联结果，解释退化时须考虑各贡献项。")


def ext_material6(doc):
    heading(doc, "2.3.15  导电聚合物的热—机械特性与界面应力", level=3)
    body(doc,
         "SAPC 的界面分层（2.5.2）根植于材料的热—机械特性失配，故有必要审视导电聚合物及相邻材料的热膨胀、模量与玻璃化转变。"
         "导电聚合物（含 PSS）的热膨胀系数（CTE）通常显著大于 Al₂O₃ 与铝，且其模量较低、对温度与含水量敏感（吸湿增塑、升温软化）。"
         "在温度变化或吸湿溶胀时，聚合物相对刚性介质/金属发生差异变形，在聚合物/氧化膜界面积累剪切与法向应力；当应力超过界面黏附强度或经循环累积疲劳时，即引发脱黏与分层（式2-7类比）。")
    body(doc,
         "这一热—机械视角解释了多类失效的共同机械根因：温度循环（CTE 失配交变应变）、湿热（吸湿溶胀应力）与高温（软化与应力松弛）都最终汇聚到“界面应力—分层—接触电阻上升”的链条（2.5.2、2.5.13）。"
         "它也指明了缓解途径：选择 CTE 更匹配、黏附更强的聚合物/界面体系，引入应力缓冲或偶联层，控制吸湿（封装阻湿）以减小溶胀应力。"
         "在建模上，界面应力—损伤—接触电阻的本构是多物理耦合模型（2.3.12）的力学环节；其参数（界面黏附强度、损伤演化律）需经热—机械试验与界面表征标定，是当前 SAPC 机理建模较薄弱、却对热-机械与湿热失效预测至关重要的一环。")


def ext_modes6(doc):
    heading(doc, "2.4.14  失效模式的工况依赖性矩阵", level=3)
    body(doc,
         "失效模式的相对重要性强烈依赖工况，建立“工况→主导模式”的依赖性矩阵有助于按应用预判风险。表24以典型工况组合为行、以失效模式为列，"
         "定性标注各模式在该工况下的相对显著性（强/中/弱），综合自 2.4 各节与文献证据。")
    add_table(doc, 24, "工况组合与主导失效模式的依赖性矩阵（相对显著性：强/中/弱）",
              ["工况组合", "ESR 上升", "漏电增大", "界面分层", "焊点/开路", "突发短路"],
              [["高湿+偏压(85/85)", "强", "强", "强", "弱", "中"],
               ["纯高温(125°C)", "强", "中", "中", "弱", "弱"],
               ["高温+纹波自热", "强", "中", "中", "中", "弱"],
               ["温度循环(−55~125)", "中", "弱", "强", "强", "弱"],
               ["浪涌/过流", "弱", "中", "弱", "弱", "中(良性)"],
               ["干燥+偏压", "中", "中(ACC)", "弱", "弱", "弱"]],
              widths=[3.0, 2.0, 2.0, 2.0, 2.0, 2.2], fs=8.6,
              source_cn="注：相对显著性为基于 2.4、2.5 与文献[9],[10],[14],[42],[75]–[77],[81]的定性判断，具体依材料/封装而异。")
    body(doc,
         "该矩阵的工程价值在于：按应用的主导工况，可优先关注相应的失效模式与监测指标。例如，湿热为主的应用应重点监测 ESR 与 LC 并强化阻湿封装；"
         "温度循环为主的应用应重点关注界面/焊点（X 射线、接触电阻）；浪涌频繁的应用则受益于聚合物良性失效特征但需关注 LC。"
         "矩阵还揭示了多应力工况下模式的并存与竞争（2.6.7、2.6.15）：如“高湿+偏压”同时强化 ESR、漏电与界面分层三路径，正是竞争失效建模最需要的场景。"
         "因此，工况依赖性矩阵不仅是工程预判工具，也为按应用设计加速试验与竞争失效模型提供了结构化输入（2.6.16、2.11）。")


def ext_mech6(doc):
    heading(doc, "2.5.16  失效树分析与失效物理的结合", level=3)
    body(doc,
         "失效树分析（FTA）以“顶事件—中间事件—基本事件”的逻辑结构自上而下分解失效，适合把 SAPC 的多机理失效组织为可推理的因果网络。"
         "以“SAPC 功能失效”为顶事件，可经“或门”分解为 ESR 超限、LC 超限与开路三类中间事件；各中间事件再向下分解为基本事件，"
         "如 ESR 超限←（聚合物体电阻上升 或 界面接触电阻上升），其中聚合物体电阻上升←（热氧老化 或 去掺杂 或 晶粒收缩），界面接触电阻上升←（吸湿溶胀 或 分层 或 焊点退化）。"
         "若各基本事件概率与门逻辑已知，可自下而上计算顶事件概率：")
    equation(doc, "P(OR) = 1 − ∏_i (1 − p_i) ,   P(AND) = ∏_i p_i", "2-23")
    body(doc,
         "FTA 与失效物理（PoF）结合的价值在于：FTA 提供逻辑结构与定性因果，PoF（式2-8/2-9/2-10）为基本事件提供随应力变化的发生概率/速率，"
         "二者结合即得“随工况变化的定量失效树”，与竞争失效模型（式2-19、2.6.15）在数学上一致（“或门”对应竞争失效的任一路径触发）。"
         "这种结合既保留了 FTA 的可解释性与系统性（便于工程评审与薄弱环节识别），又获得了 PoF 的定量与外推能力。"
         "对 SAPC，构建“PoF 驱动的失效树/竞争失效模型”，是把分散机理整合为系统失效概率、并识别主导路径（薄弱环节）的有效途径，也是本文机理—建模衔接的方法之一。")


def ext_model7(doc):
    heading(doc, "2.6.25  全局敏感性分析与试验信息量", level=3)
    body(doc,
         "局部敏感性（2.6.17）仅在参考点附近有效，当参数不确定性较大或模型非线性较强时，需全局敏感性分析（GSA）。基于方差分解的 Sobol 指数把输出方差归因到各输入及其交互："
         "总方差 V(Y)=Σ V_i + Σ V_{ij} + …，一阶 Sobol 指数 S_i=V_i/V(Y) 度量单个参数的主效应，总效应指数 S_Ti 含其全部交互贡献。")
    equation(doc, "S_i = V[ E(Y | θ_i) ] / V(Y) ,   S_Ti = 1 − V[ E(Y | θ_{~i}) ] / V(Y)", "2-24")
    body(doc,
         "对 SAPC 的寿命/RUL 模型，GSA 可识别哪些参数（如激活能 Eₐ、湿度指数 n、失效阈值、初始分散）主导预测不确定性，从而指导“把有限试验资源优先用于精确标定高敏感参数”（与 2.6.16 试验设计呼应）。"
         "GSA 还能揭示参数间交互（如温度×湿度对寿命的交互），为三应力统一模型（式2-21）的交互项是否必要提供依据。"
         "把 GSA 纳入建模流程（2.6.19），使“不确定性来自何处、应如何减小”变得可量化，是从“给出预测”迈向“可信、可优化预测”的方法学保障，贯穿本文建模与试验设计。")

    heading(doc, "2.6.26  删失数据与竞争风险的统计处理", level=3)
    body(doc,
         "可靠性试验数据普遍含删失（censoring）：试验结束时未失效（右删失）、仅知失效发生在某区间（区间删失）、或因竞争失效而被其它模式“移除”（竞争风险删失）。正确处理删失是无偏估计的前提。"
         "对右删失，似然由失效样本的密度项与删失样本的可靠度项构成（2.6.10）；对竞争风险，需区分“原因别风险（cause-specific hazard）”与“子分布风险”，"
         "以正确估计在其它模式存在下某一模式的失效概率，避免把竞争失效样本简单当作随机删失而产生偏差。")
    body(doc,
         "对 SAPC 这类多模式竞争器件（2.6.7、2.6.15），竞争风险处理尤为重要：若仅关注 ESR 失效而把 LC 失效样本当作普通删失，会高估 ESR 模式的可靠度。"
         "正确做法是以竞争风险模型联合估计各模式的原因别风险，并据此计算系统可靠度（式2-19）。这要求试验中记录每个失效样本的失效模式（而非仅记录失效时间），"
         "并在数据集中标注模式标签（2.11 切入点①）。删失与竞争风险的规范统计处理，是 SAPC 可靠性数据“可建模、可比较”的统计基础，也是本文数据分析的方法学要求。")


def ext_monitor6(doc):
    heading(doc, "2.7.10  边缘计算与在线 PHM 的工程部署", level=3)
    body(doc,
         "把 RUL 预测从离线分析推向在线 PHM（2.12.4），需考虑工程部署约束。在电源/变换器等嵌入式平台，算力、内存与功耗有限，复杂模型（深度网络、大量粒子的粒子滤波）难以实时运行；"
         "因此常采用“边缘—云”协同：边缘端执行轻量的健康指标提取（ESR/C 辨识、特征工程、异常检测，2.7.4/2.7.9）与简化模型的快速更新，云端执行计算密集的模型再训练、批量分析与基准比较。"
         "模型压缩（降阶物理模型、蒸馏后的轻量网络）与高效在线更新（共轭贝叶斯递推，式2-20、2.6.14）是边缘部署的关键技术。")
    body(doc,
         "部署还需考虑：实时性（监测—预测的延迟需与维护决策周期匹配）、鲁棒性（对传感故障与工况漂移的容错，2.7.9）、以及可维护性（模型版本管理与现场再标定）。"
         "对 SAPC，边缘端的核心挑战仍是极低 ESR 的高精度在线辨识（2.7.2、2.7.6）；一旦健康指标可靠，轻量的物理-数据融合模型（2.6.24）配合云端更新即可实现实用的在线 PHM。"
         "这一“轻量边缘 + 智能云端”的架构，是把本文方法落地为工程系统的现实路径，也呼应了数字孪生与预测性维护的发展趋势（2.12.4、2.7.5）。")


def ext_app6(doc):
    heading(doc, "2.8.10  标准与认证体系概览", level=3)
    body(doc,
         "SAPC 的可靠性评价依托一系列标准与认证体系，理清其层次有助于把研究与工程规范对接。表25概览主要标准的层次与适用范围："
         "从通用元件规范、加速试验方法、到行业（汽车/航天）认证，构成由通用到专用的标准链。")
    add_table(doc, 25, "SAPC 相关标准与认证体系概览",
              ["层次", "代表标准/体系", "适用范围", "在 SAPC 评价中的作用"],
              [["通用元件规范", "IEC 60384-1 等", "固定电容器通用要求", "参数、耐久、判据基线"],
               ["加速试验方法", "JESD22-A101/A110", "THB / HAST", "湿热可靠性评价方法"],
               ["汽车认证", "AEC-Q200", "车规无源元件应力序列", "温度循环/振动/湿热综合"],
               ["航天/高可靠", "NASA NEPP / NPSL", "选用、筛选、DPA", "批次一致性与适用性评估"],
               ["研究性试验", "SSST 等", "浪涌/时变应力", "临界应力与上电失效研究"]],
              widths=[2.4, 3.0, 3.2, 3.6], fs=8.6,
              source_cn="注：综合自[31]–[34],[15],[16],[75]；标准条款以官方最新版本为准。")
    body(doc,
         "标准体系对研究的意义有二：其一，规定了可比的试验条件与判据，使不同研究的结果具备可比性基础（前提是统一执行，2.4.8）；"
         "其二，行业认证（如 AEC-Q200）规定了器件进入特定应用的“及格线”，为可靠性研究设定了工程目标。"
         "然而，现行标准多为面向通用电容器的通用方法，缺乏针对 SAPC 多机理、低 ESR 特性的专用规程（2.10、表23）。"
         "因此，在遵循现有标准的同时，发展 SAPC 专用的多应力试验与判据规程（2.11 切入点①），是把研究成果反哺标准化、提升领域成熟度的重要方向。")


def s_questions(doc):
    heading(doc, "2.11.1  研究问题、假设与预期贡献", level=3)
    body(doc,
         "基于 2.11 凝练的不足，本文拟回答的核心研究问题可表述为：在湿-热-电-机械多应力服役条件下，如何定量刻画 SAPC 的多机理竞争退化，"
         "并建立机理贯通、含不确定性、可在线更新的寿命/RUL 预测方法？该总问题可分解为四个子问题："
         "①SAPC 在纯高温与多应力耦合下的失效模式与退化规律如何（补强数据缺口）？"
         "②如何把 PEDOT 电导动力学与界面退化定量映射到器件 ESR/LC（机理—参数贯通）？"
         "③如何在竞争失效框架下联合建模 ESR 与 LC 路径并刻画其相关性（多机理竞争）？"
         "④如何以物理-数据融合与贝叶斯更新，在小样本下给出含置信区间的 RUL（可信预测）？")
    body(doc,
         "围绕上述问题，本文提出若干可检验的研究假设：H1——SAPC 在纯高温下的 ESR 退化主导于聚合物热氧老化，可由指数型动力学（式2-8）描述且活化能可标定；"
         "H2——湿热偏压下 ESR 与 LC 路径因共同的界面电化学诱因（2.5.13）而正相关，独立竞争假设将高估可靠度；"
         "H3——以 PoF 为物理先验的物理-数据融合模型，其外推精度与不确定性校准优于纯经验或纯数据方法，尤其在小样本下；"
         "H4——多应力统一模型（式2-21）的温-湿交互项对 SAPC 显著，忽略将导致外推偏差。")
    body(doc,
         "据此，本文的预期贡献包括：①构建统一规程下、含批次/封装/模式标签的 SAPC 多应力退化数据集（补数据缺口）；"
         "②建立 PEDOT 电导动力学贯通器件 ESR/LC 的失效物理模型（贯通机理与参数）；③发展含相关性的多机理竞争失效与退化随机过程联合模型（量化竞争）；"
         "④提出物理-数据融合 + 贝叶斯在线更新的 RUL 方法并以应用任务剖面验证（可信预测与工程落地）。"
         "这些贡献与 2.11 的五点切入一一对应，共同构成本文相对现有研究的增量，并直接回应了本章 2.9.7 方法学评述所指出的整体升级需求。")



# __MAIN_RESTORED7__



# ================= 深化批次七：电压/容量/对阴离子/失效期/反馈/阈值/置信/系统/新器件/路线图 =================
def ext_device6(doc):
    heading(doc, "2.2.13  电压等级与容量段对可靠性的影响", level=3)
    body(doc,
         "SAPC 的可靠性随额定电压与容量段而变，理解这一依赖有助于按规格预判风险。由式(2-1)与化成关系（图3），较高额定电压需要更厚的氧化膜，"
         "在相同使用电压下电场更低、漏电与击穿裕度更大；但更厚介质以牺牲单位面积电容为代价，且高压器件的工艺缺陷在高场下更易显现，故高压段对化成质量与缺陷控制更敏感（2.5.10、2.5.15）。"
         "容量段方面，大容量器件通常意味着更多/更深的孔道与更大的聚合物填充面积，对填充完整性与界面接触的一致性要求更高，ESR 退化的绝对裕度与分散也随之变化。")
    body(doc,
         "在电压降额（2.2.7）的语境下，低压器件（如 SMD 2.5–6.3 V）因介质薄、场强相对高，对降额与浪涌更敏感；而 SAPC 整体耐压受聚合物体系限制（SMD 多在数十伏以内，2.2.5）[91]，"
         "这界定了其适用电压范围并影响选型。从研究角度，可靠性结论须标注电压等级与容量段——不同规格的退化速率、失效模式占比与降额敏感性可能不同，"
         "跨规格外推需谨慎（与 2.4.12 封装/尺寸、2.5.11 批次的提醒一致）。这也提示 SAPC 专用数据集应覆盖代表性的电压/容量组合，以支持按规格的寿命建模（2.11）。")


def ext_material7(doc):
    heading(doc, "2.3.16  电化学稳定性窗口与对阴离子工程", level=3)
    body(doc,
         "PEDOT 的掺杂态稳定性可由电化学稳定性窗口刻画：在一定电位/电场与化学环境内，掺杂态可保持；超出则发生去掺杂（还原）或过氧化（over-oxidation），二者都降低电导。"
         "在 SAPC 中，直流偏压、界面电位与湿热环境共同决定了聚合物实际所处的电化学条件（2.5.13）；当偏压或界面电位使聚合物趋向去掺杂/过氧化区时，电导下降、ESR 上升。"
         "因此，把器件工作点设计在聚合物的稳定窗口内（通过降额、界面设计与对阴离子选择），是抑制电化学退化的材料—器件协同策略。")
    body(doc,
         "对阴离子工程是稳定窗口调控的核心。PSS 作为高分子对阴离子兼具分散与掺杂功能，但其酸性与吸湿性带来稳定性隐患（2.3.6、2.3.9）；"
         "选择更稳定、迁移性更低的对阴离子（或自掺杂体系[68]），可减少对阴离子迁移导致的去掺杂、提升热/电化学稳定性。研究表明不同对阴离子主导的 PEDOT 薄膜其退化敏感因素不同[92]，"
         "印证了对阴离子对稳定性的决定性作用。把“稳定窗口 + 对阴离子工程”纳入材料选择准则，意味着 SAPC 的可靠性优化不仅关注初始电导（2.3.14），更关注掺杂态在服役电化学条件下的保持能力，"
         "这是材料层面提升 SAPC 耐久性的关键认识，也为失效物理模型的“去掺杂”环节提供了机理边界（式2-8、2.5.1）。")


def ext_modes7(doc):
    heading(doc, "2.4.15  早期、随机与磨损失效的识别", level=3)
    body(doc,
         "把观测到的失效归入浴盆曲线（图24）的正确区段，是可靠性判断与建模选择的前提。早期失效（婴儿期，β<1）多由工艺缺陷与杂质诱发（2.5.4、2.5.15），表现为加电初期的高漏电或异常 ESR，"
         "可经加电老化/分选剔除（2.2.11）；随机失效（有用寿命期，β≈1）多由偶发过应力（浪涌、瞬态）触发，发生率近恒定；磨损失效（β>1）则源于聚合物本征退化与界面分层的累积（2.5.1、2.5.2），是 SAPC 寿命的主导终态。")
    body(doc,
         "识别区段的方法包括：Weibull 形状参数 β 的估计（式2-15）、失效时间分布的形态、以及失效分析对失效根因的判别（缺陷诱发 vs 本征磨损）。"
         "区段识别直接影响建模选择：早期失效宜以筛选与质量控制应对、不应纳入磨损寿命外推；随机失效适用恒定失效率（指数分布、FIT，2.8.5）；"
         "磨损失效则适用 Weibull/退化随机过程（2.6.3、2.6.4）。常见误区是把未筛除的早期失效混入磨损数据，导致 β 与寿命估计失真。"
         "因此，SAPC 数据分析须先做区段甄别、剔除或单独处理早期失效，再对磨损段建模——这是 2.6.26 删失/竞争风险处理之外的另一数据规范要点。")


def ext_mech7(doc):
    heading(doc, "2.5.17  多机理耦合的反馈回路与临界行为", level=3)
    body(doc,
         "SAPC 失效的一个深层特征是存在正反馈回路，可能导致退化在寿命末期的非线性加速（临界/拐点行为，2.4.11）。最典型的回路是热-电自热反馈（式2-6）："
         "ESR 上升→纹波焦耳热增加→局部温升→聚合物退化与界面分层加速（式2-8）→ESR 进一步上升。该回路在增益足够时使退化由“缓变”转入“加速”，"
         "对应退化曲线的拐点与寿命末期的快速劣化。类似地，漏电—发热回路（漏电增大→局部发热→介质/聚合物退化→漏电再增大）也具正反馈性质，可能导致漏电的骤升（2.5.14 自愈失效）。")
    body(doc,
         "从动力学系统视角，这些正反馈意味着 SAPC 的退化是非线性的，存在“稳定缓变区”与“失稳加速区”，二者之间的转变具有临界特征。"
         "这解释了为何线性外推在寿命末期严重失准（2.6.17），以及为何两阶段/非线性退化模型（2.6.4、[73]）更贴合实际。"
         "在工程上，识别临界拐点的早期征兆（如 ESR 变化率的加速、热点温度的异常上升）对及时预警至关重要（2.7.4、2.7.8）。"
         "把正反馈回路显式纳入退化模型（如使退化速率依赖于当前退化量与自热），是刻画 SAPC 末期加速、提升 RUL 末段精度的关键，也是本文动力学建模需处理的非线性来源。")


def ext_model8(doc):
    heading(doc, "2.6.27  失效阈值的设定及其对寿命估计的影响", level=3)
    body(doc,
         "失效阈值（如 ESR=2×ESR₀、LC 上限）是把连续退化转化为“失效/未失效”的关键约定，其设定直接影响寿命与 RUL 估计。阈值偏严（如 1.5×）会缩短估计寿命、提高安全裕度但增加更换频次；"
         "阈值偏宽（如 3×）则相反。由于退化在末期加速（2.4.11、2.5.17），阈值在“加速区”的小幅变动对寿命的影响相对较小，而在“缓变区”的变动则影响较大——这要求阈值设定与退化曲线形态相匹配。")
    body(doc,
         "阈值还应与失效后果（电路功能/安全，2.8.7）和应用判据（2.4.8、2.8.6）一致，而非任意取值。对多参数（ESR/LC）情形，需为各参数分别设定阈值并以竞争失效（多阈值首达，2.6.15）综合。"
         "在不确定性量化（2.6.17）中，阈值本身的不确定性（测量基线 ESR₀ 的误差、判据的工程容差）也应纳入传播。"
         "因此，阈值不是一个“拍定的数字”，而是连接物理退化、应用需求与统计估计的接口；规范地设定、标注并对其做敏感性分析（2.6.25），是 SAPC 寿命评估可信、可比的必要条件。")

    heading(doc, "2.6.28  外推到使用条件的置信评估", level=3)
    body(doc,
         "可靠性预测的落脚点是使用条件下带置信的寿命/失效概率。把加速试验标定的模型外推到使用条件时，预测的不确定性来自参数后验与模型形式（2.6.17、2.6.25），"
         "应以预测区间（而非点估计）报告，例如给出使用条件下 B10 寿命（10% 失效分位）的置信下限，作为保守的设计依据。其计算可由参数后验抽样并经寿命模型传播（蒙特卡洛），或由贝叶斯预测分布（式2-20）直接获得。")
    body(doc,
         "以 2.6.9 算例为基础，若把 Eₐ 与 n 的估计不确定性（来自有限试验）纳入传播，则使用条件寿命的置信区间可能跨越数倍——这定量地警示“单点外推”的风险，并说明为何多应力多水平试验（2.6.16）与全局敏感性分析（2.6.25）对收窄置信区间至关重要。"
         "对 SAPC，由于机理多、数据少，外推置信评估尤需谨慎：宜结合 PoF 物理约束（限制外推形态）、竞争失效（避免单模式乐观）与贝叶斯不确定性（量化置信），"
         "给出“带置信、可决策”的使用条件可靠性结论。这正是本文区别于“仅给寿命数字”的传统做法、追求工程可信度的体现。")


def ext_monitor7(doc):
    heading(doc, "2.7.11  多器件与系统级健康管理", level=3)
    body(doc,
         "实际系统常并联或分布使用多只 SAPC（如多相变换器、并联滤波组），健康管理需从单器件扩展到器件群与系统级。多器件场景带来新问题："
         "①并联器件的电流/热分担不均会导致退化不同步，最弱器件可能加速劣化并拖累整体；②单只器件退化（ESR 上升）会改变电流分配，形成器件间的相互影响；"
         "③系统级健康指标（如总纹波、母线阻抗）是各器件状态的聚合，需从聚合量反演个体或群体健康（可观测性挑战，2.7.7）。")
    body(doc,
         "系统级健康管理策略包括：以冗余设计容忍个别器件退化、以均流/均热设计减小退化不同步、以及以系统级监测（母线纹波/阻抗）结合模型推断群体健康并触发维护（2.7.5）。"
         "在可靠性建模上，多器件系统可用系统可靠性方法（串并联、k-out-of-n）结合各器件的退化/竞争失效模型（2.6.7、2.6.15）评估系统寿命，并考虑共因失效（共同的环境/工况，2.5.13）。"
         "对 SAPC，从“单器件 RUL”到“系统级健康与可用性”的扩展，是其可靠性研究服务于整机的必然延伸（2.8.5、2.8.7），也对监测的可观测性与建模的系统化提出了更高要求。")


def ext_app7(doc):
    heading(doc, "2.8.11  典型应用的可靠性指标对照", level=3)
    body(doc,
         "为把应用需求具体化，表26对三类典型应用的关键可靠性指标与对 SAPC 的设计含义作对照（指标量级为工程语境的定性概括，具体以项目规范为准）。")
    add_table(doc, 26, "典型应用的可靠性指标与对 SAPC 的设计含义",
              ["应用", "寿命/可用性目标", "关键环境应力", "对 SAPC 的设计含义"],
              [["数据中心/SSD 供电", "高可用、长在线", "高频纹波、自热", "极低 ESR、热设计、在线监测"],
               ["汽车电子(域控/DC-DC)", "长寿命、低 FIT、车规", "宽温、振动、温度循环、湿", "降额、密封、抗振封装、AEC-Q200"],
               ["工业/通信电源", "长寿命、可维护", "纹波、温升、连续运行", "纹波裕度、寿命预测、预测维护"],
               ["航天/高可靠", "高可靠、严筛选", "真空/热循环、严苛筛选", "批次一致性、突发裕度、DPA"]],
              widths=[2.8, 2.8, 3.0, 3.6], fs=8.6,
              source_cn="注：综合自[5],[15],[16],[34],[47],[88],[89]；指标为定性概括，具体以项目规范与器件规格书为准。")
    body(doc,
         "对照表明：不同应用对 SAPC 的“可靠性”诉求各异——数据中心重在线可用与热管理、汽车重车规与降额、工业重可维护与寿命预测、航天重一致性与突发裕度。"
         "这要求可靠性研究产出“可按应用裁剪”的模型与判据，而非单一结论（2.8.6）。本文以多应力数据集、机理贯通模型与含置信的 RUL 预测为基础，"
         "正是为了支持这种按应用的可靠性评估与设计权衡（2.11 切入点⑤），使研究成果具备跨应用的工程适配能力。")


def ext_outlook2(doc):
    heading(doc, "2.12.6  与宽禁带器件、新型电容技术的关系", level=3)
    body(doc,
         "SAPC 的发展与电力电子的整体演进相互牵引。宽禁带半导体（SiC、GaN）推动开关频率提升与功率密度增大，对电容器提出“更低 ESR/ESL、更高频、更耐温、更小体积”的要求——"
         "这恰是 SAPC 的优势方向，也对其高温与高频纹波可靠性提出更高挑战（2.4.4、2.2.4）。因此，宽禁带时代的 SAPC 可靠性研究需更关注高温、高频自热与快速瞬态下的退化。")
    body(doc,
         "在器件谱系上，硅电容（trench/3D 硅基电容）、新型多层金属化薄膜电容等新技术也在低 ESR/高可靠细分市场与 SAPC 竞争或互补（2.2.10、[44]）。"
         "SAPC 的差异化价值在于其“高容量密度 + 低 ESR + 失效良性”的综合平衡；保持这一优势的关键，正是解决其湿热与高温可靠性短板（本章主体）。"
         "从趋势看，SAPC 与宽禁带器件、新型电容技术的协同与竞争，将持续牵引其向“更稳定材料、更可靠界面、更智能监测”演进，这为本文研究提供了长期的技术背景与应用前景。")

    heading(doc, "2.12.7  研究路线图", level=3)
    body(doc,
         "综合全章，可勾勒 SAPC 可靠性研究的路线图：近期（基础补强）——建立统一规程下的多应力、含标签 SAPC 退化数据集，标定关键机理动力学参数（Eₐ、n、扩散与界面参数），"
         "明确纯高温与耦合工况的失效模式与规律；中期（机理—模型贯通）——建立 PEDOT 电导动力学贯通器件 ESR/LC 的失效物理模型，发展含相关性的多机理竞争失效与退化随机过程联合模型，并以贝叶斯量化不确定性；"
         "远期（智能预测与应用）——实现物理-数据融合的在线 PHM 与数字孪生，支持按应用的预测性维护与全生命周期优化，并反哺 SAPC 专用标准化。")
    body(doc,
         "这一路线图把本章凝练的不足（2.11）与切入点、研究问题/假设（2.11.1）、以及发展趋势（2.12）统一为可执行的阶段目标，"
         "其内在逻辑是“数据—机理—模型—预测—应用”的逐级递进与闭环反馈。本文的工作定位于近期与中期的关键环节（数据集、机理贯通模型、竞争失效与不确定性、RUL 方法），"
         "并为远期的智能预测与标准化奠定基础。以此，本章不仅完成了对国内外研究现状的系统梳理，也为全文研究确立了清晰的坐标与路径。")



# __MAIN_RESTORED8__



# ================= 深化批次八：含水耦合/可检测/证据链/可辨识/协变量/基线/维修/开放数据 =================
def ext_material8(doc):
    heading(doc, "2.3.17  含水率—电导—力学的定量耦合", level=3)
    body(doc,
         "湿度对 SAPC 的影响是“含水率—电导—力学”三者耦合的结果，定量刻画这一耦合是湿热失效物理建模的核心。含水率 w（由 Fick 扩散决定，式2-9）通过两条途径影响电导："
         "①溶胀（力学）——吸水使聚合物体积膨胀（光学厚度可增约 150%[52]），颗粒间距增大、跳跃势垒升高，由 VRH（式2-4）导致电导下降；"
         "②增塑与去掺杂（化学/电化学）——水降低玻璃化温度、促进对阴离子迁移与去掺杂，进一步降低载流子浓度与电导。二者可唯象地合写为电导对含水率的递减函数 σ(w)=σ₀·exp(−κ·w)，"
         "其中 κ 综合了溶胀与去掺杂的敏感性。")
    body(doc,
         "力学方面，溶胀在受约束的器件内部产生溶胀应力，叠加 CTE 失配应力（2.3.15），共同驱动界面分层（2.5.2）。因此，含水率不仅直接降低体电导，还经溶胀应力间接增大界面接触电阻——"
         "两条路径都使 ESR 上升，且在“湿+热+偏压”下相互强化（2.5.13）。把 σ(w)、溶胀应变 ε(w) 与界面损伤 D(应力) 联立，并以 Fick 扩散提供 w(x,t)，即构成湿热退化的多物理耦合子模型（2.3.12 的湿度环节）。"
         "其参数（扩散系数 D、敏感系数 κ、溶胀系数、界面损伤律）需经吸湿—电导—力学联合试验标定，目前面向 SAPC 的此类定量数据仍不足，是本文拟以专门试验补强的方向之一（2.11）。")


def ext_modes8(doc):
    heading(doc, "2.4.16  失效的可检测性与潜伏失效", level=3)
    body(doc,
         "并非所有退化都能被及时检测，可检测性（detectability）是状态监测与失效预防的重要维度。SAPC 的 ESR/LC 退化在多数情况下可由在线监测捕捉（2.7），属可检测失效；"
         "但某些退化具有“潜伏”特征：如界面分层在 X 射线/C-SAM 下可见、却未必显著反映在常态电学测量中（早期分层对 ESR 影响小）；又如缺陷诱发的漏电可能在特定温度/偏压下才显现（如干燥环境的异常充电电流 ACC[77]）。"
         "潜伏失效在条件改变（如温度、湿度、偏压跃变）时可能突然显性化，构成“看似健康、实则隐患”的风险。")
    body(doc,
         "提升可检测性的途径包括：①多参数监测（ESR + LC + 阻抗谱特征，对不同潜伏机理互补敏感，2.4.8、2.7.4）；②激励诊断（在特定应力下激发潜伏缺陷，如周期性 EIS 或受控应力扫描）；"
         "③无损检测的定期介入（X 射线/C-SAM 探测分层，2.5.6）。在失效模式与影响分析（FMEA/类 FMEA，表5）中，可检测性常与严重度、发生度共同构成风险优先数（RPN），指导监测资源分配。"
         "对 SAPC，识别哪些失效是潜伏的、并设计能激发/捕捉潜伏失效的监测，是把“可检测性”纳入可靠性设计的关键，也是降低“突发显性化”风险的有效手段。")


def ext_mech8(doc):
    heading(doc, "2.5.18  老化机理的微观证据链综合", level=3)
    body(doc,
         "把分散的微观证据整合为自洽的机理证据链，是机理研究可信度的体现。对 SAPC 的 ESR 退化，可综合如下证据链：宏观上 ESR 随老化（尤其热/氧）近指数上升（器件级[42],[43]）；"
         "材料级电导随时间指数下降且空气加速（薄膜级[17],[18]）；微观形貌上导电晶粒收缩、相分离粗化、PSS 壳变化（[51],[62],[69]）；化学态上 XPS/Raman 显示去掺杂/氧化（[23],[92]）。"
         "四个层级（器件—材料—形貌—化学）的证据彼此印证，共同支持“热氧老化→去掺杂+晶粒收缩→电导下降→ESR 上升”的机理链（2.5.1）。")
    body(doc,
         "对湿热失效，证据链为：宏观 ESR/LC 上升且 C 稳定（[9],[10]）；机理上分层为主因（[12]）；材料上吸湿溶胀显著（[52]）、水使晶区变小无序（[51]）；"
         "并伴随杂质（Fe）诱发的高漏电（[9]）。这些证据支持“水分扩散→溶胀/去掺杂+界面腐蚀分层→ESR/LC 上升”的链条（2.5.2、2.5.13）。"
         "构建多层级证据链的价值在于：单一证据可能有歧义（如 ESR 上升既可源于体电阻也可源于界面），而多层级、多手段的交叉印证能锁定主导机理、排除替代解释，"
         "是 SAPC 机理研究从“现象描述”走向“机理确证”的方法学要求，也为失效物理建模（2.6.5）提供可信的机理输入。")


def ext_model9(doc):
    heading(doc, "2.6.29  模型可辨识性与参数耦合", level=3)
    body(doc,
         "复杂模型（多物理、多参数）面临可辨识性（identifiability）问题：有限、含噪的数据可能无法唯一确定全部参数，不同参数组合给出相近拟合（参数耦合/抵偿）。"
         "例如，在式(2-13)的 Peck 模型中，若试验仅在单一湿度水平，则湿度指数 n 与常数项耦合而不可分（2.9.2 案例的局限）；在退化随机过程中，漂移与扩散、形状与尺度也可能耦合。"
         "可辨识性不足会导致参数估计不稳定、置信区间过宽、外推不可靠。")
    body(doc,
         "改善可辨识性的途径包括：①试验设计——通过多应力多水平布点打破参数耦合（2.6.16）；②物理约束——以 PoF 关系固定或约束部分参数（减少自由度，2.6.5）；"
         "③贝叶斯先验——以合理先验正则化弱辨识参数（2.6.8）；④可辨识性分析——以 Fisher 信息矩阵的条件数或剖面似然事前评估哪些参数可辨识。"
         "对 SAPC 的多机理、多参数模型，可辨识性分析应作为建模的前置步骤，避免“拟合很好但参数无意义”的陷阱。把可辨识性纳入建模流程（2.6.19），"
         "是保证 SAPC 可靠性模型参数具有物理意义、外推可信的统计学基础。")

    heading(doc, "2.6.30  协变量与加速变量的回归处理", level=3)
    body(doc,
         "SAPC 的失效受多种协变量影响：加速变量（温度、湿度、电压、纹波）与非加速协变量（批次、封装、尺寸、电压等级，2.4.12、2.5.11、2.2.13）。"
         "把这些变量纳入模型，常用加速失效时间（AFT）回归或比例风险（PH）回归：AFT 设协变量经一个加速因子作用于时间尺度（ln t_f = β₀ + Σ β_j x_j + 误差），"
         "PH 设协变量乘性作用于风险率。加速变量的系数对应物理加速关系（如 Eₐ、n，式2-11/2-13），非加速协变量的系数则量化批次/封装等的影响。")
    body(doc,
         "正确处理协变量的意义在于：①把批次/封装等“干扰”从加速效应中分离，避免混淆（2.5.11）；②实现“按规格/批次”的差异化寿命预测；③在数据集有限时，通过共享加速参数、分别估计协变量效应来提升统计效率（与分层贝叶斯一致，2.6.8）。"
         "对 SAPC，建议在数据集中系统记录加速变量与协变量（2.11 切入点①），并以 AFT/分层模型联合分析，从而把“一群异质器件在多应力下的失效”统一建模。"
         "这既是统计方法问题，也是数据采集规范问题——二者共同决定了 SAPC 可靠性结论的可靠性与可推广性。")


def ext_monitor8(doc):
    heading(doc, "2.7.12  健康指标基线漂移的补偿", level=3)
    body(doc,
         "长期监测中，健康指标的“基线”可能因可逆因素（温度季节性、工况中心点变化）或传感器老化而漂移，若不补偿会与真实退化混淆（伪退化/伪健康，2.4.13、2.7.7）。"
         "对 SAPC 的 ESR 监测，基线漂移主要来自温度/频率折算不完全与传感漂移。补偿策略包括：①以同步测量的温度对 ESR 做实时折算到参考温度（需准确的 ESR–T 模型，2.2.9）；"
         "②以静止/轻载时段的“准基线”定期校准；③以状态空间模型把缓慢漂移建模为可估计的随机游走，与退化信号分离。")
    body(doc,
         "基线漂移补偿的本质是把“可逆/系统性变化”与“不可逆退化”分离，使监测量真正反映健康状态。这对 SAPC 极低 ESR 的监测尤为关键，因为微小的折算误差或漂移即可掩盖或夸大退化（2.7.6）。"
         "在 RUL 预测中，未补偿的漂移会引入偏差并恶化预测；而过度补偿又可能滤除真实退化。因此，补偿需以物理模型（ESR–T/f 关系）为依据、以异常检测（2.7.9）为防护，"
         "在“去除漂移”与“保留退化”之间取得平衡。这是把原始监测数据转化为可信健康指标的“最后一公里”，直接影响在线 PHM 的实用性（2.12.4）。")


def ext_app8(doc):
    heading(doc, "2.8.12  维修策略与备件管理", level=3)
    body(doc,
         "可靠性与 RUL 预测的工程价值，最终通过维修策略与备件管理兑现。维修策略沿“事后维修—定期维修—视情维修（CBM）—预测性维修（PdM）”演进："
         "事后维修成本与风险最高；定期维修按固定周期更换、可能过早或过晚；CBM 依据实时状态（如 ESR 超过预警阈值）触发；PdM 进一步依据 RUL 预测（2.7.5）在最优时机维护。"
         "SAPC 的低 ESR 可监测性（一旦解决精度问题）与退化主导的失效特性，使其适合 CBM/PdM。")
    body(doc,
         "备件管理则依赖对器件群体寿命分布与失效率的预测（2.8.5）：准确的寿命/RUL 分布可优化备件库存（既避免缺件停机，又避免过量库存），并支持基于可靠性的维修计划与排程。"
         "在系统层面，结合多器件健康管理（2.7.11）与全生命周期成本（2.8.9），可把“何时维护、维护哪只、备多少件”转化为可优化的决策问题。"
         "因此，SAPC 可靠性研究的下游价值链是“退化建模→RUL 预测→维修决策→备件优化→全生命周期成本”，本文的方法（含置信的 RUL）正是这一价值链的关键上游输入，"
         "其精度与置信度直接决定下游决策的质量（2.6.28、2.7.8）。")


def ext_outlook3(doc):
    heading(doc, "2.12.8  开放数据、基准与协同研究", level=3)
    body(doc,
         "领域的快速进步往往依赖开放数据与公认基准（2.6.23）。SAPC 可靠性研究当前的一个结构性短板，是缺乏公开、标注完备的退化数据集与统一评价协议，"
         "致使不同团队的模型难以公平比较、难以累积性进步（2.10、表23）。借鉴锂电池等领域的经验，推动“开放退化数据集 + 标准评价协议 + 开源参考实现”的基准化建设，"
         "将显著加速 SAPC 可靠性方法的迭代与验证。")
    body(doc,
         "协同研究亦不可或缺：器件制造商掌握材料/工艺与批次信息、用户/集成商掌握现场任务剖面与失效返修数据、高校/院所掌握机理与建模方法——三方数据与知识的协同，"
         "才能把“材料机理深、器件数据浅、方法工具全、专用数据缺”的格局（2.10）转变为“数据—机理—方法”协同推进。"
         "本文在条件允许时将尽量以开放、可复现的方式发布 SAPC 退化数据与评价协议（2.6.23），既服务于本研究的验证，也为后续研究提供可累积的基础。"
         "以开放科学的姿态推动 SAPC 可靠性研究的协同与基准化，是本章展望的落点，也是把个体研究汇聚为领域进步的必由之路。")



# __MAIN_RESTORED9__



# ================= 深化批次九：接触界面/占比演化/温湿谱/退化-寿命衔接/计量/DfR =================
def ext_material9(doc):
    heading(doc, "2.3.18  导电聚合物与石墨/银浆的接触界面", level=3)
    body(doc,
         "SAPC 的 ESR 不仅来自聚合物体电阻与聚合物/氧化膜界面，还包含聚合物阴极向外引出的“聚合物—石墨—银浆—端电极”一系列接触界面（式2-3）。"
         "石墨层的作用是改善聚合物与银浆的接触并阻挡银向内迁移（2.5.8）；银浆层提供低阻引出。每一接触界面都存在接触电阻，且对热、湿、机械应力敏感："
         "热-机械循环可使界面微裂/脱黏，湿气可引起界面腐蚀与银迁移，从而抬高接触电阻、贡献 ESR 退化。")
    body(doc,
         "这些“引出侧”界面的退化与“介质侧”聚合物/氧化膜界面退化（2.5.2）在电学上叠加，难以仅凭 ESR 直接区分，需借助阻抗谱分段（2.2.9）与失效分析（截面观察各界面，2.5.6）加以分辨。"
         "从设计看，优化石墨/银浆配方与界面黏附、强化银迁移阻挡，是降低引出侧接触电阻退化的手段；从建模看，应在 ESR 分解（式2-3）中显式区分介质侧与引出侧界面，"
         "以正确归因退化来源。忽视引出侧界面，可能把焊点/引出退化误归为聚合物本征退化，导致机理判断与寿命外推偏差——这与 2.2.12 板级耦合的提醒一脉相承。")


def ext_modes9(doc):
    heading(doc, "2.4.17  失效模式占比随时间与应力的演化", level=3)
    body(doc,
         "失效模式的相对占比并非固定，而随时间与应力演化，理解这一演化有助于动态把握风险。在早期（婴儿期，2.4.15），缺陷诱发的高漏电/突发失效占比相对较高；"
         "进入有用寿命期后，随机过应力失效为主；进入磨损期，聚合物退化与界面分层导致的 ESR 上升型失效占比上升并最终主导（2.4.11、2.4.15）。"
         "在应力维度上，湿热条件下漏电与界面路径占比高，纯高温下 ESR 路径占比高，温度循环下界面/焊点路径占比高（2.4.14 矩阵）。")
    body(doc,
         "占比演化对监测与建模有直接含义：监测策略应随寿命阶段调整侧重（早期重 LC/突发、晚期重 ESR/趋势）；竞争失效模型（2.6.15）中各路径的权重应是时间/应力的函数，而非常数。"
         "若以固定占比或单一模式建模，将在某些阶段/工况下失准。因此，准确刻画失效模式占比的时变与应力依赖，是竞争失效联合建模的精细化要求，"
         "也要求数据集中记录每个失效样本的模式与时刻（2.6.26、2.6.30），以支持占比演化的统计估计。这进一步说明了“带模式标签的 SAPC 数据集”（2.11）的必要性。")


def ext_mech9(doc):
    heading(doc, "2.5.19  失效机理的温度—湿度依赖性谱", level=3)
    body(doc,
         "不同机理在温-湿平面上的活跃区不同，绘制“机理依赖性谱”有助于理解多机理的此消彼长。定性而言：高温低湿区，热氧老化与去掺杂（聚合物本征退化，2.5.1）主导，表现为 ESR 上升；"
         "高温高湿区，水分扩散、溶胀、界面腐蚀分层与电化学迁移（2.5.2、2.5.8、2.5.13）协同活跃，ESR 与 LC 同时恶化；低温区，VRH 输运的温度依赖显现但退化速率低；"
         "温度循环（跨越宽温区）则突出 CTE 失配驱动的界面/焊点疲劳（2.5.15 力学）。这一谱图与加速试验条件图（图22）相对应：选择加速点即选择激活哪些机理。")
    body(doc,
         "机理依赖性谱的关键启示是“加速条件决定主导机理”，因而外推必须确保加速与使用条件落在同一机理区（机理不变假设，2.6.11、2.8.8）。"
         "若加速点（如 HAST 高温高湿）激活了使用条件（如温和环境）下不显著的机理（如剧烈界面腐蚀），则外推系统偏差。"
         "因此，绘制并验证 SAPC 的机理依赖性谱（通过在温-湿平面多点试验 + 失效分析确认主导机理），是设计可信加速试验与外推的前提，"
         "也是把单应力机理结论安全推广到多应力工况的依据。这一谱图的建立，正是本文多应力试验设计（2.6.16、2.11 切入点①）的目标产物之一。")


def ext_model10(doc):
    heading(doc, "2.6.31  退化建模与寿命分布的衔接", level=3)
    body(doc,
         "退化建模（2.6.4）与寿命分布建模（2.6.3）并非对立，而可相互衔接：退化随机过程隐含了寿命（失效时间）分布，反之失效时间分布可视为退化过程首达阈值的边缘结果。"
         "例如，Wiener 过程首达给出逆高斯寿命分布（式2-16/2-18），Gamma 过程首达给出相应的寿命分布（2.6.22）。这种衔接的价值在于：当退化数据可得时，用退化模型可利用全部中间信息、即使无失效也能推断寿命；"
         "当仅有失效时间数据时，用寿命分布模型直接建模——二者在“退化→失效”的物理图像下统一。")
    body(doc,
         "对 SAPC，由于失效以退化为主、突发较少且 ESR/LC 可监测，退化建模通常比纯寿命分布建模更高效（更早、更准、所需样本更少）。"
         "但二者衔接的好处是：可用历史失效时间数据（若有）为退化模型提供先验或验证（贝叶斯，2.6.8），也可由标定的退化模型反推寿命分布用于系统可靠性预计（FIT，2.8.5）。"
         "理解并利用这种衔接，使 SAPC 可靠性建模能灵活适配“有退化数据”“有失效数据”“二者皆有”的不同数据情形，提升方法的通用性与数据利用效率——这也是 2.6.24 融合架构中统计层的职责所在。")


def ext_monitor9(doc):
    heading(doc, "2.7.13  监测系统的验证、标定与计量溯源", level=3)
    body(doc,
         "监测系统输出的可信度依赖其验证、标定与计量溯源，这是常被忽视却至关重要的环节。验证回答“监测系统能否准确测得 ESR/C”：需以高精度阻抗分析仪等参考仪器对比，"
         "评估在 SAPC 极低 ESR 量程下的准确度、重复性与温度/频率响应（2.7.6）。标定则建立监测系统读数与真值的修正关系，并定期复校以补偿传感漂移（2.7.12）。"
         "计量溯源要求标定链可追溯至更高等级标准，确保不同系统/时间的测量可比。")
    body(doc,
         "对 SAPC，毫欧级 ESR 的准确测量本身具有挑战：引线电阻、接触电阻、温度与频率都会引入误差，需采用四端（Kelvin）测量、温度补偿与统一频率（2.4.8）。"
         "若监测系统未经严格验证/标定，其“退化趋势”可能混入系统误差，导致 RUL 预测偏差。因此，把监测系统的计量质量作为 PHM 可信度的一部分加以保证，"
         "是从实验室走向工程部署（2.7.10）的必要条件。本文在以监测数据驱动建模时，将明确监测系统的不确定度并纳入预测不确定性传播（2.6.17），避免“以不可靠测量得出貌似精确预测”的误区。")


def ext_app9(doc):
    heading(doc, "2.8.13  可靠性增长与面向可靠性的设计（DfR）", level=3)
    body(doc,
         "可靠性不仅靠“测量与预测”，更靠“设计与改进”实现。面向可靠性的设计（Design for Reliability, DfR）把可靠性要求前置到设计阶段：基于失效物理（2.6.5）识别潜在失效机理，"
         "通过材料选择（稳定对阴离子、去质子，2.3.16）、界面与封装设计（强黏附、阻湿，2.3.15、2.2.3）、降额与热设计（2.2.7、2.4.4）从源头抑制退化。"
         "可靠性增长（reliability growth）则通过“试验—分析—改进（TAAF）”循环，在开发中逐步暴露并消除薄弱环节，使可靠性随迭代提升。")
    body(doc,
         "对 SAPC，DfR 与可靠性增长的有效性高度依赖对失效机理的准确认识（本章主体）：只有明确“为何失效、何处薄弱”，才能有的放矢地改进。"
         "本章梳理的机理（2.5）、模型（2.6）与监测（2.7）正是 DfR 的知识基础——机理指明改进方向，模型评估改进效果，监测验证现场表现。"
         "因此，本文的研究不仅产出“评估与预测”能力，也为 SAPC 的 DfR 与可靠性增长提供机理与方法支撑，使可靠性研究闭环于“认识—预测—改进”。"
         "这一闭环定位，呼应了 2.12 的趋势展望与研究路线图，标志着 SAPC 可靠性研究从“被动评估”向“主动设计”的演进。")



# __MAIN_RESTORED10__



# ================= 深化批次十：老化等效/失效物理化学统一/工程实现/结论要点 =================
def ext_material10(doc):
    heading(doc, "2.3.19  加速老化与自然老化的等效性", level=3)
    body(doc,
         "加速老化要代表自然（使用）老化，须满足“等效性”：不仅失效时间可经加速因子换算（2.6.28），更要求退化路径与机理在两者间一致（2.6.11、2.8.8）。"
         "对 PEDOT 体系，加速温度/湿度若过高，可能引发自然条件下不显著的过程（如剧烈过氧化、封装额外失效、对阴离子的不同迁移路径），破坏等效性。"
         "因此，加速条件的上限应受“机理不变”约束，可通过对加速与自然（或温和长期）老化样品的光谱学/形貌对照（2.3.13、2.5.18）验证退化产物与结构变化是否一致。")
    body(doc,
         "等效性验证的实践意义在于：它把“加速试验快”与“结论可信”统一起来——只有等效，加速结论才能外推。对 SAPC，由于多机理且各机理温-湿敏感性不同（2.5.19），"
         "等效性并非自动成立，须逐工况验证。一种稳健策略是“分级加速”：在多个温和-中等-强应力水平上试验，检验退化曲线是否可经加速因子重叠（time-temperature/humidity superposition），"
         "若能重叠则支持等效与外推，若出现分叉则提示机理转变。把等效性作为加速试验设计与外推的前置检验，是保证 SAPC 寿命预测可信的又一方法学要点（2.11）。")


def ext_mech10(doc):
    heading(doc, "2.5.20  失效物理与失效化学的统一视角", level=3)
    body(doc,
         "SAPC 的退化兼具“物理”（输运、力学、热）与“化学”（氧化、去掺杂、腐蚀、迁移）属性，统一视角有助于避免机理认识的片面。"
         "物理过程（颗粒收缩、溶胀、分层、自热）改变载流子输运与界面接触，化学过程（氧化、去掺杂、对阴离子迁移、介质水合）改变材料组成与掺杂态；二者通过“形貌—掺杂—电导”这一共同枢纽相互耦合（2.3.2、2.3.3）。"
         "例如，氧化（化学）导致共轭破坏与对阴离子失稳，进而引起晶粒收缩（物理）；溶胀（物理）拉大间距同时为去掺杂（化学）提供水介质。")
    body(doc,
         "统一视角的价值在于建模：失效物理（PoF）模型若仅含物理项而忽略化学动力学（如去掺杂、氧化的化学反应速率），将无法解释气氛/酸性/对阴离子的影响（2.3.4、2.3.6、2.3.16）；"
         "反之亦然。因此，面向 SAPC 的“失效物理”实为“失效物理化学”，其本构应同时包含输运/力学方程与化学反应动力学，并以 Arrhenius（式2-5）统一其温度依赖。"
         "这一统一视角与多物理耦合本构（2.3.12）、多尺度建模（2.5.12）一致，共同构成本文机理建模的认识论基础：把 SAPC 退化理解为多物理场与多化学过程在多尺度上的耦合演化，"
         "而非单一“物理”或“化学”过程。")


def ext_model11(doc):
    heading(doc, "2.6.32  模型的工程实现与计算复杂度", level=3)
    body(doc,
         "可靠性/RUL 模型最终需在工程系统中实现，计算复杂度与实现代价是落地的现实约束（与 2.7.10 边缘部署呼应）。各类方法的计算特征不同："
         "经验/统计模型（式2-11~2-15）计算极轻、可解析或查表，适合任何平台；退化随机过程的 RUL（式2-18/2-22）部分需数值积分但仍可接受；"
         "粒子滤波（2.6.13）计算量随粒子数线性增长，实时性受限；深度网络/PINN 训练昂贵但推理可优化；多物理有限元仿真（2.3.12）计算最重，多用于离线分析与生成训练数据。")
    body(doc,
         "工程实现的策略是“离线重、在线轻”：把昂贵的多物理仿真与模型训练放在离线/云端（生成降阶模型或训练网络），把轻量的在线更新（共轭贝叶斯递推、降阶模型推理）放在边缘（2.7.10、2.6.14）。"
         "模型降阶（用低维代理近似高维物理）、参数化（把仿真结果拟合为解析/查表形式）与硬件加速是关键技术。"
         "对 SAPC 的在线 PHM，推荐以“轻量退化随机过程 + 共轭贝叶斯在线更新”为在线核心、以 PoF/仿真为离线先验来源——兼顾物理可信、不确定性表达与实时可行。"
         "把计算复杂度作为方法选择的显式维度（补充表17），是确保研究成果可工程落地而非仅停留于论文的务实考量。")


def s_recap(doc):
    heading(doc, "本章主要结论要点", level=2)
    body(doc, "为便于查阅，将本章主要结论凝练为以下要点：")
    bullet(doc, "（1）器件与材料：SAPC 以蚀刻铝阳极/Al₂O₃ 介质提供高体积电容、以导电聚合物（PEDOT）阴极提供低 ESR 与高频性能；"
                "其电导源于掺杂态共轭主链与颗粒金属/VRH 输运，对热、氧、湿、酸高度敏感（2.2、2.3）。")
    bullet(doc, "（2）失效模式：以 ESR 上升、漏电（LC）增大为主、电容量相对稳定；按主导应力分为湿热、高温、热-电耦合与热-机械四类，并随时间/应力演化（2.4）。")
    bullet(doc, "（3）失效机理：以聚合物本征退化（去掺杂/氧化/晶粒收缩）、水分扩散与界面分层、氧化膜损伤与有限自愈三链为主，叠加工艺缺陷、电化学迁移与多机理耦合反馈（2.5）。")
    bullet(doc, "（4）建模方法：经验/统计、退化随机过程、失效物理与数据驱动四类各有适用边界，融合（物理为骨、数据为肉、统计为度）是面向 SAPC 的最优路线（2.6）。")
    bullet(doc, "（5）监测与应用：ESR 是核心健康指标，极低 ESR 的高精度在线辨识是难点；可靠性要求随汽车/航天/电源应用而异，需按应用裁剪判据与降额（2.7、2.8）。")
    bullet(doc, "（6）现状与缺口：呈“材料机理深、器件数据浅、方法工具全、专用数据缺”格局；纯高温/长周期、多应力耦合与多机理竞争是最迫切的空白（2.9、2.10、表23）。")
    bullet(doc, "（7）本文切入：以多应力专用数据集、机理贯通的失效物理模型、含相关性的竞争失效与不确定性量化、物理-数据融合的 RUL 预测、面向应用验证五点切入（2.11、2.11.1、2.12）。")
    body(doc,
         "上述要点构成本章对 SAPC 可靠性研究现状的总体判断与本文研究的逻辑起点。后续各章将围绕这些要点，按“数据—机理—模型—预测—应用”的路线图（2.12.7）逐步展开并验证。")



if __name__ == "__main__":
    build()
