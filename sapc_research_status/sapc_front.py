# -*- coding: utf-8 -*-
"""前置：中/英文摘要 + 缩略语与术语表"""
from sapc_common import add_heading_cn, add_body, add_page_break, set_cn_font
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt


def build_abstract(doc):
    add_heading_cn(doc, "摘  要", level=0)
    cn = """
叠层铝固态电容器（Stacked Aluminium solid Polymer Capacitor，SAPC；以松下SP-Cap为代表）是以高比表面积铝阳极箔及其阳极氧化Al2O3膜为介质、以导电高分子（主要为聚3,4-乙撑二氧噻吩，PEDOT）取代液态电解质作为阴极、并以多片阳极箔叠层后由引线框架键合与树脂模塑封装而成的片式表面贴装电容器。相较于传统液态铝电解电容器，其等效串联电阻（ESR）可降低一个数量级以上，等效串联电感（ESL）显著减小，温度与频率特性平坦，且不存在电解液干涸问题；相较于多层陶瓷电容器（MLCC），其在直流偏压下容值稳定、单体容量大、无压电啸叫与微裂纹短路风险。正因如此，SAPC已成为CPU/GPU供电、人工智能服务器、5G通信、车载电子等低压大电流、高纹波场景中的关键无源元件，并在相当范围内对MLCC与钽电容形成替代。系统梳理SAPC的国内外研究现状，对支撑相关博士学位论文的选题定位与研究设计具有重要意义。
本报告刻意避免"按时间罗列"与"国内国外两张皮"的低效写法，沿"材料与结构—制备工艺—电气性能—失效模式—失效机理—可靠性建模—状态监测—应用需求"的逻辑主线，对国内外研究进行对照式、量化化的系统评述，并在每一环节设"评述"凝练共性不足。报告首先建立综述的范围、文献检索策略与组织主线（立坐标）；继而沿主线逐环节展开：在材料与结构环节厘清阳极箔/氧化膜/导电高分子三元体系与叠层、卷绕、钽聚合物三类构型的演化谱系；在工艺环节深入对比原位化学聚合与预聚合PEDOT:PSS分散液两条阴极成型路线的覆盖率、电导率、漏电流与耐湿性此消彼长的关系；在性能环节量化ESR/容值/纹波/温度/偏压特性；在失效模式环节确立"ESR上升为主、漏电流增大为辅、容值相对稳定、终态以开路为主"的SAPC失效模式谱；在失效机理环节深入评述PEDOT热氧化与去掺杂导致电导率衰减（激活能约1.0–1.4 eV）、氧化膜缺陷与杂质（如铁颗粒）诱发漏电、湿热协同氧化、以及不同于液态体系的"退化型自愈"等核心机理；在建模环节对比统计分布、Arrhenius/Eyring加速、纹波—热耦合寿命、失效物理（PoF）与数据驱动/物理信息神经网络（PINN）混合五类方法；在监测环节对比ESR/容值在线辨识与机器学习剩余寿命（RUL）预测的进展。
通过文献计量、技术成熟度（TRL）与能力雷达的多视角对比，报告得出总体判断：国内外呈"国外引领材料—工艺—机理范式、国内深化箔材与工程制造并加速追赶"的格局，差距集中在导电高分子原材料与原创聚合工艺、强物理嵌入的退化机理定量模型、以及跨工况泛化的寿命预测三个方面。在此基础上，报告凝练出四条研究空白（失效率基准与失效阈值缺位、湿—热—电多应力耦合机理缺乏定量理论、PEDOT去掺杂动力学缺乏可外推的失效物理模型、数据驱动RUL可解释性弱与泛化差），并以"研究空白—量化证据—研究去向"三位一体的方式逐条对接到学位论文的研究内容与章节。本报告兼具领域综述（SAPC可靠性现状）与写作范式示范（如何撰写优秀的国内外研究现状）双重价值。
"""
    add_body(doc, cn)
    add_heading_cn(doc, "关键词：", level=4)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Cm(0.82)
    run = p.add_run("叠层铝固态电容器；导电高分子；PEDOT；等效串联电阻；失效机理；可靠性建模；"
                    "状态监测；剩余使用寿命；国内外研究现状；物理信息神经网络")
    set_cn_font(run, font_name="宋体", size_pt=11)
    add_page_break(doc)

    add_heading_cn(doc, "Abstract", level=0)
    en = """
The stacked aluminium solid polymer capacitor (SAPC; typified by Panasonic's SP-Cap) is a chip-type surface-mount capacitor in which a high-surface-area etched aluminium anode foil and its anodic Al2O3 oxide form the dielectric, a conductive polymer (mainly poly(3,4-ethylenedioxythiophene), PEDOT) replaces the liquid electrolyte as the cathode, and several anode foils are stacked, bonded to a lead frame and resin-moulded. Compared with conventional wet aluminium electrolytic capacitors, the SAPC offers an equivalent series resistance (ESR) lower by more than an order of magnitude, much smaller equivalent series inductance (ESL), flat temperature/frequency behaviour, and freedom from electrolyte dry-out. Compared with multilayer ceramic capacitors (MLCCs), it offers stable capacitance under DC bias, large single-unit capacitance, and no acoustic noise or micro-crack short risk. Consequently, SAPCs have become key passive components in low-voltage high-current, high-ripple applications such as CPU/GPU power delivery, AI servers, 5G communication and automotive electronics, partially replacing MLCCs and tantalum capacitors.
This report deliberately avoids chronological listing and the separation of domestic and international work into two disjoint parts. It organizes the review along a single logical thread of Materials and Structure - Process - Electrical Performance - Failure Mode - Failure Mechanism - Reliability Modeling - Condition Monitoring - Application Requirements, providing a contrastive and quantitative review with a critical commentary at the end of each thread. It first establishes the scope, search strategy and organizing thread; it then proceeds thread by thread: clarifying the foil/oxide/polymer ternary system and the stacked/wound/tantalum-polymer construction families; comparing the in-situ chemical polymerization and the pre-polymerized PEDOT:PSS dispersion routes with their trade-offs in coverage, conductivity, leakage and humidity robustness; quantifying ESR/capacitance/ripple/temperature/bias behaviour; establishing the SAPC failure-mode spectrum dominated by ESR rise; analyzing core mechanisms such as PEDOT thermal oxidation/de-doping (activation energy about 1.0 to 1.4 eV), oxide-defect and impurity-induced leakage, humid-thermal synergy, and a degradation-type self-healing distinct from wet systems; comparing statistical, Arrhenius/Eyring, ripple-thermal, physics-of-failure and data-driven/physics-informed (PINN) modeling; and comparing on-line C/ESR identification and machine-learning remaining-useful-life (RUL) prediction.
Through bibliometrics, technology-readiness assessment and capability radar comparison, the report concludes that international groups lead the materials-process-mechanism paradigm while domestic (Chinese) groups deepen foil and manufacturing engineering and are catching up rapidly, with gaps concentrated in conductive-polymer raw materials and original polymerization processes, strongly physics-embedded quantitative degradation models, and cross-condition generalization of lifetime prediction. Four research gaps are distilled and mapped, in a gap-evidence-direction manner, onto the dissertation research contents. The report serves both as a substantive review of SAPC reliability and as a methodological demonstration of how to write an excellent research-status review.

Keywords: stacked aluminium solid polymer capacitor; conductive polymer; PEDOT; equivalent series resistance; failure mechanism; reliability modeling; condition monitoring; remaining useful life; research status; physics-informed neural network.
"""
    add_body(doc, en)
    add_page_break(doc)


def build_glossary(doc):
    add_heading_cn(doc, "缩略语与主要术语", level=0)
    add_body(doc, """
为便于阅读，现将本报告频繁出现的缩略语与主要术语集中说明如下（按英文字母与主题归类）。正文首次出现时一般给出中英文对照，此处提供统一索引。
""")
    items = [
        ("SAPC", "Stacked Aluminium solid Polymer Capacitor，叠层铝固态（聚合物）电容器，本报告核心对象"),
        ("SP-Cap", "Panasonic 叠层型导电高分子铝电容器商品名，SAPC 的典型代表"),
        ("OS-CON", "卷绕型导电高分子铝固态电容器商品名（原Sanyo，后归Panasonic）"),
        ("POSCAP", "导电高分子钽电容器商品名（KEMET/Sanyo）"),
        ("PEDOT", "Poly(3,4-ethylenedioxythiophene)，聚3,4-乙撑二氧噻吩，主流导电高分子阴极材料"),
        ("PSS", "Poly(styrene sulfonate)，聚苯乙烯磺酸，PEDOT 的常用聚阴离子掺杂剂/分散剂"),
        ("PEDOT:PSS", "PEDOT 与 PSS 的复合分散体系（预聚合分散液路线）"),
        ("PPy", "Polypyrrole，聚吡咯，早期导电高分子阴极材料"),
        ("PANI", "Polyaniline，聚苯胺，导电高分子之一"),
        ("TCNQ", "Tetracyanoquinodimethane 络合盐，早期OS-CON采用的有机半导体电解质"),
        ("Al2O3", "氧化铝，铝阳极箔阳极氧化形成的介质氧化膜"),
        ("ESR", "Equivalent Series Resistance，等效串联电阻（SAPC核心健康指标）"),
        ("ESL", "Equivalent Series Inductance，等效串联电感"),
        ("DCL / LC", "DC Leakage current，直流漏电流"),
        ("C", "Capacitance，电容量"),
        ("tanδ", "Loss tangent，损耗角正切（介质/等效损耗指标）"),
        ("CV", "Capacitance-Voltage 乘积，衡量箔材/器件体积容量效率的指标"),
        ("EoL", "End of Life，寿命终点（失效阈值判据，如ESR升至初值2倍、容值降5%–20%）"),
        ("ALT / HALT", "Accelerated / Highly Accelerated Life Test，加速/高加速寿命试验"),
        ("THB / 85-85", "Temperature-Humidity-Bias / 85°C-85%RH，温湿度偏压（湿热）试验"),
        ("TC", "Temperature Cycling，温度循环试验"),
        ("Ea", "Activation energy，激活能（温度敏感性参数）"),
        ("AF", "Acceleration Factor，加速因子"),
        ("β / η", "Weibull分布的形状参数 / 尺度（特征寿命）参数"),
        ("PoF", "Physics-of-Failure，失效物理"),
        ("PHM", "Prognostics and Health Management，故障预测与健康管理"),
        ("RUL", "Remaining Useful Life，剩余使用寿命"),
        ("HI", "Health Indicator，健康指标"),
        ("EIS", "Electrochemical/Electrical Impedance Spectroscopy，阻抗谱"),
        ("LSTM / CNN", "长短期记忆网络 / 卷积神经网络（数据驱动RUL方法）"),
        ("PINN", "Physics-Informed Neural Network，物理信息神经网络"),
        ("VRM / VRD", "Voltage Regulator Module / Down，处理器供电的电压调节模块"),
        ("De-doping", "去掺杂，导电高分子失去掺杂态、电导率下降的过程"),
        ("Self-healing", "自愈；在SAPC中表现为缺陷处高分子退化绝缘化以隔离漏电点的退化型自愈"),
        ("Field crystallization", "场致结晶，钽电容Ta2O5非晶向晶态转变（此处作机理类比）"),
        ("Mission profile", "任务剖面，真实运行工况的应力时间序列"),
        ("AEC-Q200", "汽车电子委员会被动元件应力鉴定标准"),
        ("MnO2", "二氧化锰，传统钽电容阴极材料（与聚合物阴极对照）"),
    ]
    for k, v in items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(2.4)
        p.paragraph_format.first_line_indent = Cm(-2.4)
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run("%s　" % k)
        set_cn_font(run, font_name="黑体", size_pt=10.5, bold=True)
        run2 = p.add_run(v)
        set_cn_font(run2, font_name="宋体", size_pt=10.5)
    add_page_break(doc)
