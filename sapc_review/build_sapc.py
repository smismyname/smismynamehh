# -*- coding: utf-8 -*-
"""
Builds the Word (.docx) literature-review chapter (Rev.2, expanded):
"SAPC（叠层铝固态电容器）可靠性研究的国内外研究现状"

Rev.2 changes:
- Substantially expanded, more technical and densely-cited text (no filler)
- Added model EQUATIONS (Arrhenius / Peck / Eyring / Weibull / competing-risk / VRH)
- Added comparison TABLES (failure modes; device families; reliability models; standards)
- More references cited in-text; figures rebuilt without text collisions
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
         line=1.5, first_indent_chars=0, space_after=6, space_before=0):
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
        set_cn(run, cn=cn, size=size, bold=bold)
    return p


def body(doc, text, size=12):
    return para(doc, text, size=size, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                first_indent_chars=2, line=1.5, space_after=6)


def heading(doc, text, level=1):
    sizes = {1: 16, 2: 14, 3: 13}
    p = doc.add_heading(level=level)
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


def add_figure(doc, filename, fig_no, caption_cn, source_cn):
    path = os.path.join(ASSETS, filename)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(path, width=Cm(14.5))
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


# ---------------- document content ----------------
def build():
    figs.build_all()

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = EN_FONT
    normal.font.size = Pt(12)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), CN_BODY)

    for sec in doc.sections:
        sec.page_height = Cm(29.7)
        sec.page_width = Cm(21.0)
        sec.top_margin = Cm(2.54)
        sec.bottom_margin = Cm(2.54)
        sec.left_margin = Cm(2.54)
        sec.right_margin = Cm(2.54)

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
    para(doc, "A Review of Failure Modes, Mechanisms and Reliability Modeling",
         size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    para(doc, "作者：（请填写）", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "导师：（请填写）", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "日期：2026 年 5 月", size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    # ---------- 编制与诚信说明 ----------
    heading(doc, "编制与文献诚信说明", level=1)
    body(doc,
         "本章为博士论文“国内外研究现状”章节的可直接编辑初稿。为保障学术诚信，全部参考文献均经检索后纳入，"
         "可经文末所给链接溯源；凡未能确证的 DOI、卷期或作者信息，均以“[DOI待核验]”或“建议核验”明确标注，"
         "未作虚构。提交前请务必在 Web of Science / Scopus / IEEE Xplore 及出版商页面逐条复核。")
    body(doc,
         "配图：正文图1–图10 为作者基于公开原理自行绘制的原创示意图，不含任何受版权保护的他人图件，可直接使用。"
         "对 SEM/TEM 形貌、XPS/EDS 成分及实测 I–V/C–V 曲线等需引自原始论文的图件，本文不直接嵌入受版权保护的原图，"
         "而在附录 A“建议引用图表索引”中给出可溯源的真实出处（含 DOI），便于在取得授权后引用。")
    body(doc,
         "术语约定：SAPC（Stacked Aluminum Polymer/Solid Capacitor）指以导电聚合物（多为 PEDOT 或 PEDOT:PSS 体系）"
         "为固态电解质、由多片蚀刻阳极铝箔叠层并联、经塑封封装而成的叠层（多层）铝固态电解电容器；文献中常以"
         "“polymer aluminum (PA) / multilayer polymer aluminum (PAE) / aluminum polymer capacitor (APC)”指代同类器件[9]–[16]。"
         "为与之区分，本章对“混合型聚合物铝电容（hybrid polymer aluminum electrolytic capacitor）”——即同时含液态电解质与导电聚合物者[55],[56]——单独讨论。")
    page_break(doc)

    # ---------- 摘要 ----------
    heading(doc, "摘要", level=1)
    body(doc,
         "叠层铝固态电容器（SAPC）以导电聚合物替代传统液态电解质，兼具低等效串联电阻（ESR）、优良高频与温度特性、"
         "以及失效良性（不易燃爆）等优点[1],[14],[59]，已成为高功率密度电源、汽车电子与消费电子中片式钽电容与液态铝电解电容的重要替代器件。"
         "然而，导电聚合物对湿、热、电应力敏感，其长期可靠性尚未被充分认识[15],[16]。本章按“器件—失效模式—失效机理—可靠性建模—状态监测”主线，"
         "系统梳理国内外研究现状并给出量化对比：在失效模式层面，归纳了湿热、高温与热-电耦合三类典型模式，其退化以 ESR 上升、漏电流（LC）增大为主、"
         "电容量相对稳定[9],[10],[13]；在机理层面，基于 PEDOT 颗粒金属（granular-metal）导电模型阐明了晶粒收缩、去掺杂/氧化、吸湿溶胀、界面分层与氧化膜自愈等关键过程[17],[18],[25],[51],[52]；"
         "在建模层面，比较了统计/经验（Arrhenius、Peck、Eyring、Weibull）、失效物理（PoF）与数据驱动三类方法的数学形式、适用边界与局限[29],[30],[35]–[39]。"
         "最后凝练出现有研究的四点不足并据此提出本文切入点。")
    p = para(doc, "关键词：", size=12, bold=True, space_after=2)
    set_cn(p.add_run("叠层铝固态电容器；导电聚合物（PEDOT）；失效模式；失效机理；可靠性建模；剩余寿命预测"), size=12)

    heading(doc, "Abstract", level=1)
    body(doc,
         "Stacked aluminum polymer solid capacitors (SAPC) replace the liquid electrolyte of conventional aluminum "
         "electrolytic capacitors with a solid conductive polymer (typically a PEDOT-based system), combining low equivalent "
         "series resistance (ESR), good high-frequency and temperature stability and a benign (non-ignition) failure behavior. "
         "However, the conductive polymer is sensitive to humidity, temperature and electrical stress, and the long-term "
         "reliability of SAPC is not yet fully understood. Following a device-failure mode-mechanism-modeling-monitoring thread, "
         "this chapter reviews the state of the art and provides quantitative comparisons. It classifies three failure-mode families "
         "(humid-heat, high-temperature and thermo-electric coupling), characterized mainly by ESR rise and leakage-current increase "
         "with comparatively stable capacitance; analyzes the key mechanisms (PEDOT grain shrinkage and de-doping/oxidation, "
         "moisture-induced swelling, interfacial delamination and oxide self-healing) under the granular-metal conduction picture; and "
         "compares statistical/empirical (Arrhenius, Peck, Eyring, Weibull), physics-of-failure and data-driven reliability-modeling "
         "approaches with their governing equations and applicability. Four research gaps are distilled to motivate the dissertation.")
    p = para(doc, "Keywords: ", size=12, bold=True, space_after=2)
    set_cn(p.add_run("stacked aluminum polymer capacitor; conductive polymer (PEDOT); failure modes; failure mechanisms; "
                     "reliability modeling; remaining useful life"), size=12, en=EN_FONT)
    page_break(doc)

    # ---------- 目录 ----------
    heading(doc, "目录", level=1)
    add_toc(doc)
    page_break(doc)

    # ============ 第2章 ============
    heading(doc, "第2章  SAPC 可靠性研究的国内外研究现状", level=1)

    # 2.1
    heading(doc, "2.1  研究范围、文献来源与综述方法", level=2)
    body(doc,
         "本章聚焦以导电聚合物为固态电解质的叠层（多层）铝固态电解电容器（SAPC）。文献检索以 Web of Science、Scopus、IEEE Xplore 为主，"
         "辅以 RSC、Springer、MDPI、Frontiers 等出版商数据库，并以 NASA 技术报告服务器（NTRS）与 KEMET、Murata、Panasonic、TDK 等厂商技术资料补充工程证据，"
         "检索词包括 “polymer aluminum (electrolytic) capacitor”“multilayer/stacked polymer aluminum capacitor”“PEDOT(:PSS) degradation/conductivity”"
         "“ESR / leakage current reliability”“temperature humidity bias (THB) / HAST”“remaining useful life (RUL) capacitor” 等。"
         "围绕可靠性，相关研究可归入器件结构与材料、失效模式、失效机理、可靠性建模与寿命预测、状态监测五个相互关联的方向[1]–[3]。")
    body(doc,
         "本章采用“按科学问题分块、对比—评判—收口”的综述方法：每一主题先归纳主流技术路线，再对比代表性工作的差异与定量结果，"
         "最后点明其共性局限并过渡到下一主题，从而把零散结论组织为“前人做到何处—尚存何种缺口—故本文研究必要”的逻辑主线。"
         "权威综述[1],[2]与专著[3]从功率电子用电容器整体出发，建立了失效机理—失效模式—寿命模型的分析框架；CALCE（美国马里兰大学）、"
         "NASA NEPP 及主流厂商的实证研究[9]–[16],[55],[56],[59]构成了 SAPC 可靠性的核心证据来源。聚合物钽电容因机理相近，亦被用作重要类比[26],[42],[43],[57]–[60]。")
    body(doc,
         "总体而言，现有文献呈现三点特征：其一，专门针对 SAPC 这一“较新器件”的系统可靠性研究数量仍然有限，且高度集中于湿度（湿热）影响，"
         "纯高温与多应力耦合下的长周期数据相对稀缺[15],[16]；其二，机理研究多借鉴 PEDOT 薄膜与聚合物钽电容的成果[17]–[28],[51],[52]，"
         "向器件级寿命模型的定量映射尚不充分；其三，建模方法正由经验统计模型向失效物理（PoF）与数据驱动方法演进[35]–[39]。图1给出本章纳入文献的主题分布。")
    add_figure(doc, "fig_litdist.png", 1,
               "本章纳入文献的主题分布（基于真实检索结果的统计，共 62 条）",
               "来源：作者根据本章参考文献[1]–[62]自行统计绘制（原创图）。")

    # 2.2
    heading(doc, "2.2  SAPC 器件结构、工作原理与技术演进", level=2)
    body(doc,
         "SAPC 的基本电容单元由“高比表面积蚀刻铝阳极箔—阳极氧化形成的 Al₂O₃ 介质膜—导电聚合物阴极—石墨层—银浆引出层”构成；"
         "多片单元并联叠层并以环氧塑封封装，形成低矮、适于表面贴装的片式结构（图2）。其工作原理仍属阀金属电解电容范畴：电容由阳极金属表面经"
         "阳极氧化（forming）生成的致密 Al₂O₃ 薄膜充当介质，电容值近似由平行板关系给出：")
    equation(doc, "C = ε₀ εr A / d", "2-1")
    body(doc,
         "式中 εr 为 Al₂O₃ 相对介电常数（约 8–10），d 为氧化膜厚度（与化成电压近似成正比，约 1.0–1.4 nm/V），A 为有效电极面积。"
         "蚀刻使阳极箔获得约两个数量级的有效面积增益，从而在小体积内实现高电容[5],[45],[46]。与液态体系不同，SAPC 用导电聚合物作为“真正的阴极”，"
         "其高电子电导（PEDOT 体系可达 10²–10³ S·cm⁻¹ 量级[21],[62]）显著降低 ESR、改善高频特性，并因不存在电解液蒸发而具有更稳定的温度特性[1],[5],[61]。"
         "器件 ESR 可近似分解为聚合物体电阻、聚合物/氧化膜界面与层间接触电阻、电极及引出端电阻之和：")
    equation(doc, "ESR ≈ R_polymer + R_interface/contact + R_electrode + R_termination", "2-2")
    body(doc,
         "其中聚合物体电阻与界面/接触电阻对湿、热应力最为敏感，是 SAPC 退化的主要电学表现来源（详见 2.3、2.4）。")
    add_figure(doc, "fig_structure.png", 2,
               "SAPC 单元结构与叠层封装示意（横截面）",
               "来源：作者基于公开器件原理自行绘制（原创图）；结构要素参见[4]–[7],[13]。")
    body(doc,
         "从技术演进看，导电聚合物电解电容器自 20 世纪 90 年代起步[4]，电解质体系历经聚吡咯、聚噻吩到 PEDOT:PSS 的迭代；"
         "近年通过电极蚀刻形貌优化、分散液配方与去质子（中和 PSS 酸性）等手段持续改善耐湿热性能[6]–[8],[22]，并借助提高 PEDOT 分子量、二次掺杂等提升电导与稳定性[20],[21],[62]。"
         "封装方面，叠层塑封结构相较卷绕结构更低矮、利于密封，但环氧封装并非绝对阻湿，水分随时间扩散进入器件内部，成为湿热失效的前提[10],[13]。"
         "面向高可靠应用，已出现专门的高可靠叠层固态铝电容制备工艺[50]。为厘清器件谱系，表1对四类相关器件进行对比。")
    add_table(doc, 1, "SAPC 与相关电解电容器件的对比",
              ["器件类型", "电解质/阴极", "ESR/高频", "主导失效模式", "失效特性", "温/湿敏感性", "代表文献"],
              [["液态铝电解电容", "液态电解液", "ESR 较高", "电解液蒸发→C下降、ESR上升", "可能鼓胀/泄漏", "对温度敏感", "[1],[53],[54]"],
               ["混合型聚合物铝电容", "液态电解液+导电聚合物", "ESR 低、纹波能力强", "兼具蒸发与聚合物退化、具自愈", "良性、长寿命", "中等", "[55],[56],[61]"],
               ["SAPC（叠层固态）", "导电聚合物(PEDOT)", "ESR 低、高频优", "ESR 上升、LC 增大(C 稳定)", "良性、不易燃爆", "对湿热敏感", "[9],[10],[13]–[16]"],
               ["聚合物钽电容", "Ta₂O₅/导电聚合物", "ESR 低", "ESR 上升、LC/击穿", "良性、无磨损型失效", "对湿热/电场敏感", "[26],[42],[57]–[60]"]],
              widths=[2.6, 2.6, 1.8, 3.2, 2.2, 1.6, 2.0], fs=8.8,
              source_cn="注：表中定性比较综合自[1],[9],[10],[13]–[16],[26],[42],[53]–[61]，定量参数请以具体型号规格书为准。")

    # 2.3 failure modes
    heading(doc, "2.3  失效模式研究现状", level=2)
    body(doc,
         "与液态铝电解电容以电解液干涸、容量下降为主导的磨损失效（其寿命近似遵循 Arrhenius“10°C 法则”，见 2.5.1）不同，"
         "SAPC 的失效以 ESR 上升与漏电流（LC）增大为主，而电容量在多数试验中相对稳定[9],[13],[53],[54]。CALCE 在不同厂商 PEDOT 体系聚合物铝电容上的研究表明，"
         "ESR 上升与 LC 增大两类模式在不同厂商样品中占比不同，且电容量在试验期间保持稳定[9]；厂商资料亦指出高温下聚合物退化导致容量偏离规格、最终趋于开路（开路型寿命终止）[13]。"
         "按主导应力，可将其失效模式归为湿热、高温与热-电耦合三类（图3）；三类模式在参数退化上表现为图4所示的典型趋势：ESR 单调上升并在寿命末期加速、LC 在某些批次显著抬升、电容量缓变。表2进一步给出三类模式的对比。")
    add_figure(doc, "fig_taxonomy.png", 3,
               "SAPC 失效模式分类（按主导应力）",
               "来源：作者综合[9]–[16]归纳并自行绘制（原创图）。")
    add_figure(doc, "fig_param_trends.png", 4,
               "SAPC 关键参数（ESR/C/LC）随应力时间的典型退化趋势（示意）",
               "来源：作者据[9],[10],[13]所述规律绘制的概念示意图（原创图，非实测数据）。")
    add_table(doc, 2, "SAPC 三类失效模式对比",
              ["失效模式", "典型应力条件", "主导退化参数", "关键微观机理", "代表试验/文献"],
              [["湿热环境", "85°C/85%RH 等 THB；HAST", "ESR↑、LC↑（C 稳定）", "聚合物吸湿溶胀/氧化去掺杂、界面腐蚀与分层", "[9],[10],[12],[13]"],
               ["高温环境", "≥105–125°C、高温存储", "ESR↑（C 漂移→开路）", "PEDOT 热氧老化、晶粒收缩、接触退化", "[13],[17],[20],[42],[43]"],
               ["热-电耦合", "纹波自热+直流偏置", "ESR↑、LC↑、局部温升", "焦耳热正反馈、偏压加速退化、热-机分层", "[25],[28],[55],[56]"]],
              widths=[2.0, 3.0, 2.6, 4.0, 2.4], fs=9.0,
              source_cn="注：归纳自[9]–[28],[42],[43],[55],[56]；定量阈值依标准[31]–[34]与具体型号而定。")

    heading(doc, "2.3.1  湿热环境失效模式", level=3)
    body(doc,
         "湿热是 SAPC 研究最充分、也最受关注的应力。CALCE 在 85°C/85%RH 等条件（含额定偏压）下对不同厂商 PEDOT 体系聚合物铝电容的研究表明，"
         "其主导失效为 ESR 上升与漏电流增大两类，两类模式在不同厂商样品中占比不同，而电容量保持稳定[9]。针对叠层（多层）封装器件，文献[10]在"
         "85°C/85%RH 与 110°C/85%RH（额定偏压）双条件下记录失效时间并建立温度相关寿命模型，指出水分透过塑封层向内扩散是湿热退化的前提；"
         "封装几何对水分驱动退化的影响则被专门研究[10]。厂商资料进一步印证：老化使有效电极面积与层间接触面积下降，从而 C 下降、ESR 上升[13]。"
         "就物理本质，湿热失效可分解为三条机理链（详见 2.4）：①导电聚合物吸湿溶胀与氧化/去掺杂导致体电导下降；②聚合物/氧化膜界面在热-机械与电应力下的腐蚀与分层，使接触电阻增大；"
         "③界面腐蚀与漏电通道形成——CALCE 还在个别批次中发现制造引入的金属（铁）颗粒嵌入介质层，形成此前文献未报道的高漏电“新机理”[9],[12]。")

    heading(doc, "2.3.2  高温环境失效模式", level=3)
    body(doc,
         "在高温（≥105–125°C）或高温存储条件下，SAPC 退化以导电聚合物的热（氧）老化为核心。Vitoratos 等指出，PEDOT:PSS 在热与氧作用下电导随时间下降，"
         "宏观表现为 ESR 上升[17]；气氛对比研究表明空气（氧）气氛显著加速老化[18]。厂商资料明确：高温下电解质（聚合物）退化导致电容量偏离标准值，"
         "最终趋于开路模式，对应器件寿命终止[13]。聚合物钽电容的高温存储研究[42],[43]显示了相似的 ESR 退化规律，可为铝固态体系提供机理类比。"
         "此外，高温会加剧封装与界面的热-机械应力，并可能影响 Al₂O₃ 介质膜稳定性，进而影响漏电流水平[28]。需强调的是，相比湿热，"
         "针对 SAPC 在纯高温/高温存储下的系统寿命数据仍较少，NASA NEPP 明确指出该类器件可靠性数据稀缺、已有文献多集中于湿度影响[15],[16]，"
         "这是当前研究的明显缺口之一。")

    heading(doc, "2.3.3  热-电耦合失效模式", level=3)
    body(doc,
         "在实际工况中，纹波电流自发热与外加偏压共同作用形成热-电耦合失效。一方面，ESR 上升导致焦耳热（约 P = I_ripple² · ESR）增加，"
         "局部温升又进一步加速聚合物退化，构成正反馈；混合型器件的纹波电流能力与自热问题在工程上被高度关注[54],[55],[56]。"
         "另一方面，直流偏置电压对退化速率有显著影响[28]。在介质层面，铝氧化膜在电场下存在击穿—自愈行为：文献[25]在铝氧化膜-聚合物体系中观测到“可逆的击穿后导通”，"
         "并将自愈与界面缺陷的阻变机制相联系；这与聚合物阴极相较 MnO₂“失效更良性、不易燃爆”的工程经验一致[14],[59],[60]。"
         "热-电-机械多场耦合下的界面分层与漏电演化，是当前定量描述最为薄弱、却对寿命预测最关键的环节。")

    # 2.4 mechanisms
    heading(doc, "2.4  失效机理研究现状", level=2)
    body(doc,
         "SAPC 的失效机理可归纳为三条相互交织的链条：导电聚合物本征退化、界面退化与分层、介质氧化膜损伤与自愈，三者共同决定 ESR 与 LC 的演化。"
         "下文逐一评述，并尽量给出可量化的机理描述。")

    heading(doc, "2.4.1  导电聚合物（PEDOT）本征退化", level=3)
    body(doc,
         "Vitoratos 等的经典工作[17]以“颗粒金属（granular-metal）”模型解释 PEDOT:PSS 的电导：导电 PEDOT 富集相形成纳米晶粒，"
         "载流子以跳跃（hopping）方式越过晶粒间势垒输运，电导对温度的依赖常用变程跳跃（VRH）形式描述：")
    equation(doc, "σ(T) = σ₀ · exp[ −(T₀ / T)^p ]   (p = 1/2 为 ES-VRH，p = 1/(d+1) 为 Mott-VRH)", "2-3")
    body(doc,
         "老化过程中导电晶粒收缩、晶界（势垒宽度）增大，使式(2-3)中的特征温度 T₀ 升高、电导随时间下降，这正是 ESR 上升的微观根源（图5）[17],[62]。"
         "气氛对比研究表明，空气（氧）显著加速老化，提示氧化是主导退化途径之一[18]；PEDOT:PSS 中 PSS 的酸性会损害器件并限制稳定性[22]，"
         "吸湿与氧化、去质子/去掺杂会改变掺杂水平与微结构[8],[21]。在湿气作用下，水通过孔道渗入 PEDOT 与 PSS 相，使层状晶区变小、更无序、间距增大，从而降低电导[51]；"
         "电-光研究显示薄膜从 9%RH 升至 80%RH 时光学厚度增加约 150%（显著溶胀），并存在“低 RH 表面吸附—中 RH 扩散溶胀—高 RH 饱和”的三段吸水机制[52]。"
         "ATR-FTIR/DFT 等手段被用于揭示其热力学与动力学过程[23]，长期老化还伴随界面重组等不可逆变化[48],[49]。这些材料层面的定量规律为器件级 PoF 建模（2.5.2）提供了输入。")
    add_figure(doc, "fig_pedot_grain.png", 5,
               "PEDOT 颗粒金属导电模型：晶粒收缩使跳跃势垒变宽，导致 ESR 上升（示意）",
               "来源：作者据颗粒金属模型[17],[18],[62]绘制的机理示意图（原创图）。")

    heading(doc, "2.4.2  界面退化与分层", level=3)
    body(doc,
         "在叠层塑封器件中，水分透过封装向内扩散，到达聚合物/氧化膜界面后引发氧化与界面黏附退化；在热-机械与电应力作用下界面发生分层（delamination），"
         "使层间接触电阻增大、有效阴极面积减小，宏观表现为 ESR 上升乃至漏电通道形成（图6）。水分扩散过程可由 Fick 第二定律描述：")
    equation(doc, "∂C_w/∂t = D ∇²C_w", "2-4")
    body(doc,
         "式中 C_w 为水分浓度、D 为封装材料的扩散系数；封装阻湿能力（D 与厚度）与界面黏附决定了湿热失效的时间尺度，封装几何对湿致退化的影响因而被专门研究[10]。"
         "KEMET 将热-机械与电应力诱发的分层视为高湿环境下电导退化的主要原因之一[12]；PEDOT:PSS 薄膜的湿致溶胀、降解与分层在材料层面亦被广泛报道[24],[51],[52]。"
         "该机理链条把“封装阻湿能力—界面黏附—接触电阻—ESR/LC”串联起来，是湿热与热-电耦合失效的共同枢纽，也是建立 PoF 竞争失效模型时必须刻画的核心环节。")
    add_figure(doc, "fig_moisture.png", 6,
               "水分侵入、聚合物溶胀与聚合物/氧化膜界面分层机理（示意）",
               "来源：作者据[10],[12],[24],[51],[52]所述机理绘制（原创图）。")

    heading(doc, "2.4.3  介质氧化膜与自愈", level=3)
    body(doc,
         "Al₂O₃ 介质膜的完整性决定漏电流水平。局部缺陷或场致结晶可形成漏电通道；而导电聚合物阴极在缺陷处的高阻化可“隔离”击穿点，实现自愈，"
         "从而抑制漏电并避免热失控，这也是聚合物器件失效“更良性”的物理原因[25],[26],[59],[60]。文献[25]在铝氧化膜-聚合物体系中观测到可逆的击穿后导通，并将自愈与界面缺陷的阻变机制相联系。"
         "然而自愈能力有限：当缺陷密度过高或界面已分层时，漏电会持续增大。值得注意的是，文献[9]在个别批次中发现源自制造过程的金属（铁）颗粒嵌入介质层、形成高漏电的“新失效机理”，"
         "提示工艺洁净度对 LC 失效的重要影响。在材料源头，国内对阳极铝箔氧化膜与烧结铝箔的微结构演变持续关注[45],[46]，为改善介质质量、降低初始缺陷密度提供了依据。")

    # 2.5 modeling
    heading(doc, "2.5  可靠性评估与建模方法研究现状", level=2)
    body(doc,
         "围绕 SAPC/铝电解电容的可靠性评估，方法可分为统计/经验、失效物理（PoF）与数据驱动三类（图7），三者并非互斥，近年呈融合趋势[1],[35]–[39]。"
         "表3从数学形式、适用应力、优点与局限四个维度对主要模型进行对比。")
    add_figure(doc, "fig_model_map.png", 7,
               "可靠性建模方法图谱：统计/经验、失效物理(PoF)与数据驱动",
               "来源：作者综合[1],[29]–[39]绘制（原创图）。")
    add_table(doc, 3, "SAPC 可靠性/寿命模型对比",
              ["模型", "数学形式（要点）", "适用应力", "优点", "局限", "文献"],
              [["Arrhenius(10°C 法则)", "L = L₀·2^((T₀−Tₐ)/10)", "温度", "简单、工程通用", "仅单一热应力，难描述聚合物机理", "[53],[54]"],
               ["Peck(温-湿-偏)", "t_f = A·RH^(−n)·exp(Eₐ/kT)", "温度+湿度", "适配 THB/HAST，含湿度因子", "参数需大量数据标定", "[29],[30]"],
               ["Eyring(温-湿)", "含 T、RH 交互项的广义形式", "温度+湿度", "可表达湿度敏感随温度变化", "形式复杂、过拟合风险", "[29],[30]"],
               ["Weibull/对数正态", "F(t)=1−exp[−(t/η)^β]", "失效时间分布", "刻画早期/磨损型失效", "需较充分失效样本", "[37],[57]"],
               ["失效物理(PoF)", "去掺杂动力学+Fick 扩散+断裂力学", "多机理耦合", "物理可解释、可外推", "面向 SAPC 尚不成熟", "[10],[17],[35]"],
               ["数据驱动(PHM)", "LSTM/集成/PINN 等", "多源监测数据", "高精度、可在线", "依赖数据、可解释性弱", "[36],[38],[39]"]],
              widths=[2.6, 4.2, 1.8, 2.6, 3.0, 1.6], fs=8.6,
              source_cn="注：综合自[10],[17],[29],[30],[35]–[39],[53],[54],[57]；式中 n 为湿度指数、Eₐ 为激活能、k 为玻尔兹曼常数、β 为 Weibull 形状参数。")

    heading(doc, "2.5.1  加速寿命试验与相关标准", level=3)
    body(doc,
         "加速寿命试验（ALT）是获取寿命数据的基础。对湿热敏感的 SAPC，温-湿-偏（THB，典型 85°C/85%RH）与高加速温湿（HAST，如 130°C/85%RH）是常用方案，"
         "相应标准包括 JEDEC JESD22-A101、JESD22-A110，以及器件通用规范 IEC 60384-1 与车规 AEC-Q200[31]–[34]。温度对反应速率的加速可由 Arrhenius 关系刻画，其加速因子为：")
    equation(doc, "AF_T = exp[ (Eₐ/k) · (1/T_use − 1/T_test) ]", "2-5")
    body(doc,
         "对液态铝电解电容，常用工程化的“10°C 法则”近似（温度每升高 10°C，寿命约减半）[53],[54]：")
    equation(doc, "L = L₀ · 2^((T₀ − Tₐ)/10)", "2-6")
    body(doc,
         "对湿热主导的失效，Peck 模型在 Arrhenius 基础上引入湿度因子，是 THB/HAST 数据外推的经典形式[29],[30]：")
    equation(doc, "t_f = A · (RH)^(−n) · exp( Eₐ / kT ) ;   AF = (RH_test/RH_use)^n · exp[(Eₐ/k)(1/T_use − 1/T_test)]", "2-7")
    body(doc,
         "文献中湿度指数 n 多取约 2.5–3、激活能 Eₐ 多在约 0.7–0.9 eV 量级（具体值依失效机理与材料体系而定，需由多应力试验标定）[29],[30]；"
         "当湿度敏感性随温度变化时，可采用含温-湿交互项的 Eyring 形式。CALCE 对聚合物铝电容正是采用 85°C/85%RH 与 110°C/85%RH 双条件以分离温度效应并建立寿命模型[9],[10]。"
         "图8、图9分别给出 Arrhenius–Peck 寿命模型（等温度线随湿度平移）与 Weibull 概率作图的概念示意。")
    add_figure(doc, "fig_arrhenius_peck.png", 8,
               "Arrhenius–Peck 寿命模型：等温度线随湿度平移（示意）",
               "来源：作者据 Peck/THB 模型[29],[30]绘制的概念图（原创图，非实测数据）。")

    heading(doc, "2.5.2  统计可靠性（Weibull）与寿命分布", level=3)
    body(doc,
         "失效时间常用 Weibull 分布拟合，其累积失效概率与可靠度为：")
    equation(doc, "F(t) = 1 − exp[ −(t/η)^β ] ,   R(t) = exp[ −(t/η)^β ]", "2-8")
    body(doc,
         "式中 η 为特征寿命、β 为形状参数：β<1 表征早期失效、β≈1 表征随机失效、β>1 表征磨损型失效。"
         "在聚合物钽电容中，击穿电压 V_cr 相对额定电压 V_R 被报道服从 Weibull 分布（示例形状参数 β≈5）[57]；"
         "可靠性评估常以“高电场+温度”加速试验获得失效时间，拟合失效模型后再外推到使用条件[58],[59]。"
         "对多机理同时作用的 SAPC，可采用竞争失效（competing-risk）框架：若各机理相互独立，则系统可靠度为各机理可靠度之积、系统失效概率为：")
    equation(doc, "R(t) = ∏ᵢ Rᵢ(t) ,   F(t) = 1 − ∏ᵢ [ 1 − Fᵢ(t) ]", "2-9")
    body(doc,
         "该框架可自然刻画“ESR 上升”“LC 增大”等并行失效路径，但目前面向 SAPC 的竞争失效定量模型仍较缺乏。")
    add_figure(doc, "fig_weibull.png", 9,
               "Weibull 概率作图（不同形状参数 β）示意",
               "来源：作者绘制的方法示意图（原创图）。")

    heading(doc, "2.5.3  失效物理（PoF）与数据驱动方法", level=3)
    body(doc,
         "PoF 方法从退化机理出发建立寿命模型。对 SAPC，关键在于把“PEDOT 去掺杂/氧化动力学（式2-3）—水分扩散（式2-4）—界面断裂力学—氧化膜场致退化”等过程"
         "与器件级 ESR/LC 演化相联系[1],[10],[17]。文献[10]建立了温度相关的失效时间模型，文献[35]在任务剖面与热点温度计算基础上进行寿命预测。"
         "整体上，面向 SAPC、能够刻画多机理竞争失效的 PoF 模型仍不成熟。数据驱动（PHM）方法近年快速发展：基于 LSTM 的剩余寿命（RUL）预测在动态工况电解电容上取得较好效果[36]；"
         "面向小样本，集成学习（如 bagging 决策树）与合成数据被用于温度-电压复合应力下的 RUL 预测[38]；电解电容的预测性维护（粒子滤波等）亦有较早探索[39]。"
         "其共性局限在于物理可解释性不足、对训练数据分布敏感，在叠层封装 SAPC 的小样本场景下泛化能力仍待验证；由此，物理-数据融合（physics-informed）成为趋势。")

    heading(doc, "2.6  状态监测与寿命预测", level=2)
    body(doc,
         "在线状态监测以 ESR 与电容量为主要健康指标[2]。文献[2]系统综述了功率电子用电容器的状态监测方法，"
         "包括基于纹波电流/电压、阻抗估计与模型辨识的多种途径；结合数据驱动模型可实现 RUL 估计[36],[39]。"
         "对 SAPC 而言，由于其以 ESR 上升为主导退化，ESR 在线辨识对状态评估尤为关键；但叠层封装、毫欧量级的低 ESR 与测量噪声给高精度在线监测带来挑战，"
         "如何在低 ESR 基线上稳定提取退化趋势仍是工程难题。")

    heading(doc, "2.7  国内外研究对比", level=2)
    body(doc,
         "总体而言，国外（尤以美国 CALCE、NASA NEPP 及日、欧厂商）在 SAPC 器件级失效模式与机理的实证研究上起步早、证据链完整，"
         "形成了以湿热失效为核心的认识[9]–[16]；在材料层面，欧洲、东亚团队对 PEDOT:PSS 体系的降解机理与改性贡献突出[6]–[8],[17]–[24],[51],[52]。"
         "国内研究近年增长迅速，既有面向材料源头的阳极/烧结铝箔氧化膜微结构研究[45],[46]，也在数据驱动寿命预测与状态监测方向持续推进，"
         "并在专利层面提出高可靠叠层固态铝电容制备工艺[50]。差距主要体现在：面向 SAPC 的多应力耦合、长周期系统试验数据与公开数据集仍较缺乏，"
         "机理到器件级寿命模型的定量贯通不足——这与国际上的整体短板一致[15],[16]。")

    heading(doc, "2.8  现有研究的不足与本文切入点", level=2)
    body(doc,
         "综合上述评述，现有研究存在四点主要不足，并与本文拟开展的工作一一对应（图10）：")
    body(doc, "（1）失效模式分类多为定性描述，缺乏统一、可量化的多参数判定框架——本文拟建立面向 SAPC 的量化失效模式表征体系；")
    body(doc, "（2）寿命模型多针对单一应力（式2-5–2-7），对“湿热—高温—热电耦合”下多机理竞争失效缺乏定量刻画——本文拟基于式(2-9)构建竞争失效可靠性模型；")
    body(doc, "（3）PEDOT 去掺杂/氧化等微观退化动力学（式2-3）尚未与器件级 ESR/LC 寿命模型有效贯通——本文拟建立连接聚合物退化与 ESR/LC 的 PoF 模型；")
    body(doc, "（4）叠层封装 SAPC 小样本下 RUL 预测精度受限——本文拟发展物理-数据融合（physics-informed）的 RUL 方法并量化不确定性。")
    add_figure(doc, "fig_gap_map.png", 10,
               "现有研究不足与本文研究内容的对应关系",
               "来源：作者归纳绘制（原创图）。")

    heading(doc, "本章小结", level=2)
    body(doc,
         "本章按“器件—失效模式—失效机理—建模—监测”主线，系统梳理了 SAPC 可靠性的国内外研究现状，并以表1–表3与式(2-1)–(2-9)给出量化对比与数学描述。"
         "现有工作已较清晰地刻画了以 ESR 上升、漏电流增大为主、电容量相对稳定的湿热失效图景，并在 PEDOT 颗粒金属退化、吸湿溶胀、界面分层与氧化膜自愈等机理上取得共识；"
         "但在多应力耦合、多机理竞争、机理到器件寿命的定量贯通以及小样本 RUL 预测方面仍存明显不足。这些不足构成了本文研究的逻辑起点与切入点。")
    page_break(doc)

    # ---------- 参考文献 ----------
    heading(doc, "参考文献", level=1)
    body(doc,
         "说明：以下文献均经检索后纳入并给出可溯源链接；标注“[DOI待核验]”者表示其 DOI/卷期/作者信息需在提交前于 "
         "Web of Science / Scopus / IEEE Xplore 或出版商页面再行确认。本列表为真实可核验的精选集（共 "
         f"{len(REFERENCES)} 条），未以虚构条目凑数。", size=10.5)
    for ref in REFERENCES:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = 1.3
        pf.space_after = Pt(4)
        pf.left_indent = Pt(24)
        pf.first_line_indent = Pt(-24)
        set_cn(p.add_run(format_ieee(ref)), size=10, en=EN_FONT)
    page_break(doc)

    # ---------- 附录A ----------
    heading(doc, "附录 A  建议引用图表索引（用于获取 SEM/TEM/实测曲线等版权图件）", level=1)
    body(doc,
         "本附录列出可作为 SEM/TEM 形貌、成分分析与实测特性曲线来源的真实文献，供作者在取得出版商授权后引用。"
         "本文不直接嵌入上述受版权保护的原图。表中 DOI 标注规则同参考文献。", size=10.5)
    fig_index = [
        ("器件结构/截面（实物）", "[14] NASA, Physical and Electrical Characterization of Aluminum Polymer Capacitors, 2018", "NTRS 20180000037"),
        ("湿热失效形貌/界面（SEM）", "[9] Shrivastava et al., IEEE TCPMT, 2017", "DOI待核验"),
        ("叠层器件失效分析（SEM/截面）", "[10] Romero et al., Microelectronics Reliability, 2020", "DOI待核验"),
        ("高湿下电导退化/分层", "[12] KEMET, Conducting Polymer Capacitors in High Humidity, 2020", "厂商资料"),
        ("ESR/C 随老化变化（实测曲线）", "[13] Murata, Polymer Aluminum — Failure Mode", "厂商资料"),
        ("PEDOT:PSS 热降解电导曲线", "[17] Vitoratos et al., Organic Electronics, 10(1):61-66, 2009", "10.1016/j.orgel.2008.10.008 [待核验]"),
        ("PEDOT 老化气氛对比", "[18] Sakkopoulos & Vitoratos, OJOPM, 4(1), 2014", "10.4236/ojopm.2014.41001"),
        ("水-PEDOT:PSS 微结构（模拟）", "[51] J. Mater. Chem. C, 2024", "10.1039/d4tc03066d"),
        ("PEDOT:PSS 湿致溶胀（电-光）", "[52] electro-optical humidity study, 2017", "DOI待核验"),
        ("铝氧化膜击穿/自愈（I-V）", "[25] Appl. Phys. Lett., 102, 2013", "10.1063/1.4802485"),
        ("阳极/烧结铝箔氧化膜（SEM/TEM）", "[45]/[46] J. Alloys Compd. 2020 / J. Electron. Mater. 2024", "DOI待核验"),
        ("THB/HAST 加速寿命数据", "[30] IET Power Electronics, 2016", "10.1049/iet-pel.2015.0031"),
        ("Weibull 击穿分布（聚合物钽）", "[57] Teverovsky, Surge Current Testing, CARTS", "DOI待核验"),
        ("RUL 预测曲线（LSTM/集成）", "[36]/[38] SAGE 2022 / Springer 2024", "10.1177/1748006X221087503 / 10.1007/978-981-99-9518-9_40"),
    ]
    add_table(doc, "A-1", "建议引用图表索引",
              ["图件类型（建议）", "建议来源文献", "DOI / 出处标注"],
              fig_index, widths=[4.6, 7.8, 4.2], fs=9.0)
    para(doc, "", size=8)
    body(doc,
         "提示：正文图1–图10 为原创示意图，可直接使用；如需在论文中加入上表所列实测/形貌图件，请向相应出版商申请授权，"
         "或使用开放获取（如[6],[7],[18],[35],[51],[62]）版本中允许重用的图件，并按 GB/T 7714 或 IEEE 规范标注出处。", size=10)

    doc.save(OUT_DOCX)
    print("SAVED:", OUT_DOCX)
    return OUT_DOCX


if __name__ == "__main__":
    build()
