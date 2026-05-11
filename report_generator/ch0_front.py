# -*- coding: utf-8 -*-
"""摘要、目录、符号表"""
from build_report import add_heading_cn, add_body, add_page_break, add_table_simple
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm
from build_report import set_cn_font


def build_abstract(doc):
    add_heading_cn(doc, "摘  要", level=0)
    abstract_cn = """
电容器作为电力电子系统与现代微电子装备中体量最大、最为基础的无源储能器件，其可靠性对整机系统的任务可靠度、维护成本及功能安全有直接且显著的影响。在风电变流器、光伏逆变器、电动汽车驱动、轨道交通牵引、航空航天供配电等对可靠性要求苛刻的场景中，电容器往往是故障率居于前列的关键部件，据统计其故障贡献比例可达30%甚至更高（Wang 和 Blaabjerg, 2014）。因此，系统理解电容器的失效模式、失效机理并建立工程上可用的可靠性模型，已成为电子元器件可靠性工程与预测性维护领域的核心研究课题。

本研究报告以铝电解电容器、多层陶瓷电容器（MLCC）、金属化薄膜电容器、固体钽电容器和超级电容器（电化学电容器）五大主流电容器类别为对象，在系统检索近三十年IEEE、Elsevier、Nature Publishing Group、MDPI、美国NASA/NEPP等机构公开的高水平学术文献的基础上，围绕"结构-材料-应力-失效-模型-监测"的闭环研究思路，对电容器在全寿命周期内的典型失效模式、底层物理化学机理、可靠性统计与物理建模方法、在线健康监测与剩余使用寿命预测方法进行了系统的归纳、评述与工程分析。

报告首先建立了电容器分类与基本工作原理框架，梳理了不同介质体系（BaTiO3基陶瓷、Al2O3阳极氧化膜、Ta2O5阳极氧化膜、双向拉伸聚丙烯BOPP、活性炭/电解液界面双电层等）下的储能机制与寄生参数模型；其次，从开路、短路、参数漂移三大表观失效模式出发，系统分析了电解液蒸发、介质击穿、金属离子迁移、自愈累积、氧化膜场致结晶、机械裂纹扩展、热失控等典型失效机理，并给出了各机理的物理化学解释与关键影响因素；在可靠性建模方面，报告重点讨论了Prokopowicz-Vaskas方程、改进Eyring-Arrhenius模型、逆幂律模型、两参数Weibull分布、多应力加速模型、基于失效物理的（PoF）寿命模型以及基于CNN-LSTM、PINN等数据驱动的寿命预测方法；在健康监测方面，对基于ESR/C在线辨识的参数估计法、基于纹波电压频谱分析的无侵入监测法以及基于阻抗谱的多尺度诊断方法进行了系统梳理。

研究表明：（1）不同类型电容器的主失效机理存在显著差异，铝电解电容主要受电解液蒸发与阀金属电极氧化控制，MLCC主要受BaTiO3晶界氧空位迁移与场致老化控制，金属化薄膜电容主要受自愈累积与电极腐蚀控制，钽电容主要受Ta2O5场致结晶与热失控控制，超级电容主要受电解液分解与电极/集流体界面老化控制；（2）在电-热-机械-湿多应力耦合工况下，单一Arrhenius或单一逆幂律模型难以精确描述寿命，需要采用广义Eyring型复合应力模型或数据驱动修正方法；（3）基于ESR与电容量联合的监测量相较单一监测量具有更强的失效判据能力，但需要针对不同类型电容器选择相匹配的失效阈值。

本报告为电容器选型设计、加速寿命试验规划、系统级可靠性评估、预测性维护策略制定提供了系统化的理论参考与方法学支撑，对提升我国高端装备中被动元器件的国产化水平与可靠性保证能力具有一定的工程意义。
"""
    add_body(doc, abstract_cn)
    add_heading_cn(doc, "关键词：", level=3)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run("电容器；失效模式；失效机理；可靠性建模；加速寿命试验；剩余使用寿命；健康监测；Weibull分布；Prokopowicz-Vaskas方程；物理失效模型")
    set_cn_font(run, font_name="宋体", size_pt=11)
    add_page_break(doc)

    # Abstract EN
    add_heading_cn(doc, "Abstract", level=0)
    en = """
Capacitors are among the most numerous passive energy-storage components in modern power electronic systems and microelectronic equipment. Their reliability directly affects mission reliability, maintenance cost and functional safety of the host system. In wind-power converters, photovoltaic inverters, electric-vehicle traction drives, metro traction systems and aerospace power distribution units, capacitors are often among the components with the highest field failure rates, contributing up to 30 percent of the total system failures according to several industry surveys reported by Wang and Blaabjerg (2014). A systematic understanding of the failure modes, failure mechanisms and engineering-oriented reliability models of capacitors has therefore become a central topic in the electronic component reliability community.

In this report, five mainstream capacitor families, namely aluminum electrolytic capacitors, multilayer ceramic capacitors (MLCC), metallized polymer film capacitors, solid tantalum capacitors and electric-double-layer supercapacitors, are systematically reviewed. Based on a comprehensive literature survey of peer-reviewed publications from IEEE, Elsevier, Nature Publishing Group, MDPI and NASA/NEPP over the last three decades, this report follows a closed-loop research paradigm of structure-material-stress-failure-model-monitoring. Typical failure modes, underlying physical-chemical mechanisms, statistical and physics-based reliability models, and on-line health monitoring methods are analyzed.

Key findings include: (i) dominant failure mechanisms are highly capacitor-family dependent; (ii) under coupled electro-thermal-mechanical-humidity stresses, a single Arrhenius or single inverse-power model is insufficient and a generalized Eyring-type multi-stress model or a data-driven hybrid model is preferable; (iii) joint monitoring of ESR and capacitance provides stronger diagnostic capability than either parameter alone, but proper failure thresholds must be chosen according to the capacitor type and application profile.

Keywords: capacitor; failure mode; failure mechanism; reliability modeling; accelerated life test; remaining useful life; health monitoring; Weibull distribution; Prokopowicz-Vaskas equation; physics-of-failure model.
"""
    add_body(doc, en)
    add_page_break(doc)


def build_toc(doc):
    add_heading_cn(doc, "目  录", level=0)
    toc_items = [
        ("摘 要 ……………………………………………………………………………………", "I"),
        ("Abstract …………………………………………………………………………………", "II"),
        ("第一章 绪论 ……………………………………………………………………………", "1"),
        ("    1.1 研究背景与意义 ……………………………………………………………", "1"),
        ("    1.2 电容器可靠性研究的历史沿革 ……………………………………………", "3"),
        ("    1.3 国内外研究现状 …………………………………………………………", "5"),
        ("    1.4 本报告的研究内容与组织结构 ……………………………………………", "9"),
        ("第二章 电容器分类、结构与基本原理 ………………………………………………", "11"),
        ("    2.1 电容器的基本物理模型 ……………………………………………………", "11"),
        ("    2.2 铝电解电容器 ………………………………………………………………", "14"),
        ("    2.3 多层陶瓷电容器MLCC ……………………………………………………", "18"),
        ("    2.4 金属化薄膜电容器 …………………………………………………………", "22"),
        ("    2.5 固体钽电容器 ……………………………………………………………", "26"),
        ("    2.6 超级电容器 …………………………………………………………………", "28"),
        ("第三章 电容器典型失效模式 …………………………………………………………", "31"),
        ("    3.1 失效模式的分类方法 ………………………………………………………", "31"),
        ("    3.2 开路失效 ……………………………………………………………………", "33"),
        ("    3.3 短路失效 ……………………………………………………………………", "36"),
        ("    3.4 参数漂移失效 ………………………………………………………………", "39"),
        ("    3.5 外观与密封失效 ……………………………………………………………", "42"),
        ("    3.6 各类型电容器失效模式比较 ………………………………………………", "44"),
        ("第四章 电容器失效机理 ………………………………………………………………", "46"),
        ("    4.1 铝电解电容器的失效机理 …………………………………………………", "46"),
        ("    4.2 MLCC的失效机理 …………………………………………………………", "52"),
        ("    4.3 金属化薄膜电容器的失效机理 ……………………………………………", "58"),
        ("    4.4 钽电容器的失效机理 ……………………………………………………", "62"),
        ("    4.5 超级电容器的失效机理 ……………………………………………………", "66"),
        ("    4.6 多应力耦合下的机理交互 …………………………………………………", "69"),
        ("第五章 电容器可靠性建模方法 ………………………………………………………", "71"),
        ("    5.1 统计可靠性模型 ……………………………………………………………", "71"),
        ("    5.2 加速寿命试验与Arrhenius-类模型 ………………………………………", "75"),
        ("    5.3 Prokopowicz-Vaskas方程 ……………………………………………", "79"),
        ("    5.4 多应力广义Eyring模型 ……………………………………………………", "81"),
        ("    5.5 基于失效物理的寿命模型 …………………………………………………", "83"),
        ("    5.6 数据驱动与物理-数据混合模型 …………………………………………", "86"),
        ("第六章 寿命预测与健康监测 …………………………………………………………", "89"),
        ("    6.1 电容器健康指标体系 ………………………………………………………", "89"),
        ("    6.2 基于ESR与C的在线监测方法 ……………………………………………", "91"),
        ("    6.3 阻抗谱与频域监测方法 ……………………………………………………", "93"),
        ("    6.4 基于机器学习的RUL预测 …………………………………………………", "95"),
        ("第七章 可靠性提升与工艺优化 ………………………………………………………", "97"),
        ("    7.1 器件级可靠性设计 …………………………………………………………", "97"),
        ("    7.2 电路级与系统级措施 ………………………………………………………", "99"),
        ("第八章 结论与展望 …………………………………………………………………", "101"),
        ("参考文献 ………………………………………………………………………………", "103"),
    ]
    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.3
        run = p.add_run(item + " " + page)
        set_cn_font(run, font_name="宋体", size_pt=11)
    add_page_break(doc)
