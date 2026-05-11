# -*- coding: utf-8 -*-
"""Front matter + 绪论 + 结构原理 + 制造工艺 (前半部分)"""
from docx_utils import (add_heading, add_body, add_page_break, add_figure,
                         add_formula, add_table, add_quote, set_cn_font)
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm


def build_cover(doc):
    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("学 术 综 述")
    set_cn_font(r, font_name="黑体", size_pt=30, bold=True)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("叠层铝固态聚合物电容器")
    set_cn_font(r, font_name="黑体", size_pt=24, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("制造工艺、失效行为与可靠性建模研究进展")
    set_cn_font(r, font_name="黑体", size_pt=18, bold=True)
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Stacked Aluminum Polymer Capacitors:")
    set_cn_font(r, font_name="Times New Roman", size_pt=14, bold=False)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("A Review of Manufacturing, Failure Behavior and Reliability Modeling")
    set_cn_font(r, font_name="Times New Roman", size_pt=14, bold=False)
    for _ in range(6):
        doc.add_paragraph()
    labels = [
        ("综述类别", "被动元器件专题综述"),
        ("研究领域", "电子元器件可靠性工程 · 导电聚合物材料"),
        ("关键词", "叠层铝聚合物电容器;PEDOT;失效机理;可靠性建模;寿命预测"),
        ("版本", "v1.0"),
        ("完成时间", "2026 年 5 月"),
    ]
    for k, v in labels:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"{k}：{v}")
        set_cn_font(r, font_name="宋体", size_pt=13)
    add_page_break(doc)


def build_abstract(doc):
    add_heading(doc, "摘  要", level=0)
    add_body(doc, """
叠层铝固态聚合物电容器 (Stacked Aluminum Polymer Capacitor, SAPC) 采用多片蚀刻铝阳极箔共模叠层、以 PEDOT 等导电聚合物作为阴极、铜引线框架封装而成，是近二十年伴随 CPU/GPU 电压调节模块 (VRM)、5G 通信电源、AI 服务器供电与电动汽车低压域而兴起的高端被动元件。相较于传统的液态铝电解电容器，SAPC 以"去电解液、低 ESR、高纹波电流承载能力、无干涸寿命限制"为核心竞争力；相较于贴片型钽聚合物电容器，SAPC 以"无浪涌燃烧风险、体积比容量更高、成本更低"为技术优势；相较于大容量 MLCC，SAPC 以"无 DC 偏置效应、无压电噪声、容量密度更高"为差异化定位。正因具备上述优点，Panasonic SP-Cap、Nichicon LV、Sun Electronic Industries (Sanyo/POSCAP 系列)、KEMET A700/A750、Kyocera-AVX APV、Chemi-Con PSG/PSF 等系列已在全球高端供电系统中广泛铺设。

然而，在其商用化进程中，SAPC 的可靠性表现出明显不同于液态电解电容的新型失效行为：2017 年 CALCE 实验室 Liu 与 Pecht 发表于 IEEE Transactions on Components, Packaging and Manufacturing Technology 的工作首次系统报告了在 85°C/85%RH 高温高湿偏压下，不同制造商 SAPC 分别表现出 "ESR 急剧上升" 与 "漏电流 (LC) 跑飞" 两种主导退化模式；2020 年马里兰大学博士论文进一步证实封装几何结构（分层数、密封胶覆盖度、引线框开口度）对水汽驱动退化具有一阶影响；2024 年 NASA NEPP 实验室 Teverovsky 博士发表的 Stress Testing of Chip Aluminum Polymer Capacitors (HALT) 报告给出了 85°C、125°C 下 1.2~1.9 倍额定电压的激活能与电压指数估计；KEMET、Nichicon、Panasonic 等厂商的白皮书进一步揭示了 PEDOT 阴极在 85°C/85%RH 下的热氧化分解、PSS 酸性水解、涂层与 Al₂O₃ 界面热机械分层等核心机理。

本综述以 SAPC 器件为主线，围绕"制造工艺 — 表征方法 — 失效模式 — 失效机理 — 可靠性建模 — 工艺改进"的研究链条，系统梳理了近二十年国内外的代表性工作并结合最新的 2023—2025 年研究进展展开评述。全文分为 8 章：第 1 章 绪论给出 SAPC 的演化脉络与其在电力电子体系中的定位；第 2 章 结构、材料与基本原理阐明 SAPC 各功能层的物理化学角色与等效电路模型；第 3 章 制造工艺详细分析了蚀刻、化成、聚合物阴极沉积 (在位化学聚合 in-situ、预聚合分散 pre-polymerized dispersion、气相聚合 vapor-phase polymerization VPP)、叠层烧结、封装密封等关键工序的工艺参数与可靠性耦合；第 4 章 表征方法系统总结了电学参数 (C / ESR / DF / LC)、EIS 阻抗谱、X 射线 CT、SEM/TEM/EDS、DSC/TGA、FT-IR/XPS 等手段在 SAPC 上的应用特点；第 5 章 失效模式将 SAPC 的失效按 "开路/短路/参数漂移/外观" 四个维度进行系统分类；第 6 章 失效机理深入讨论了 PEDOT 热氧化、PSS 水解、界面分层、Al₂O₃ 阳极膜场致破坏、自愈/反向自愈、浪涌击穿等物理化学机理；第 7 章 可靠性建模评述了 Weibull/对数正态统计模型、Arrhenius/逆幂律/广义 Eyring 加速模型、Physics-of-Failure 模型以及最新的 CNN-LSTM、PINN 等数据驱动方法；第 8 章 工艺改进则从材料、工艺、封装、系统层级给出具有定量指导意义的可靠性增强策略。

本综述的主要观点包括：(1) SAPC 的两种主导失效模式——ESR 上升型与 LC 跑飞型——并不是随机发生的，而是与制造商的 PEDOT 沉积工艺路线具有紧密的耦合；(2) 湿度应力并非通过简单的吸水膨胀引起 SAPC 退化，而是通过"PEDOT 去掺杂 + PSS 水解 + Al₂O₃ 界面羟基化"三种协同机理共同驱动；(3) 经典 Prokopowicz–Vaskas 方程已不能准确外推现代 SAPC 的寿命，需要采用带湿度项的广义 Eyring 模型；(4) 基于 C/ESR 在线监测的统计模型结合 CNN-LSTM 等机器学习方法，可在小样本条件下实现前 20% 老化循环下的 RUL 预测；(5) SAPC 的可靠性提升需要"材料级" (如 PEDOT:Tos/Hybrid)、"工艺级" (如 VPP、多层锥台叠堆)、"封装级" (如低吸湿环氧 + 热可塑弹性体双密封) 以及"系统级" (如电压降额 + 低温工作) 的共同优化。

本综述为 SAPC 的选型设计、加速寿命试验规划、预测性维护策略制定以及新一代导电聚合物电容器的研发提供了系统化的理论参考与方法学支撑。
""")
    add_heading(doc, "关键词：", level=3)
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run("叠层铝聚合物电容器；PEDOT；导电聚合物阴极；失效模式；失效机理；"
                    "可靠性建模；加速寿命试验；剩余使用寿命；CNN-LSTM；Physics-of-Failure")
    set_cn_font(run, font_name="宋体", size_pt=10.5)
    add_page_break(doc)

    add_heading(doc, "Abstract", level=0)
    add_body(doc, """
Stacked Aluminum Polymer Capacitors (SAPC) are a class of solid-electrolyte surface-mount capacitors that integrate multiple etched aluminum anode foils with a conductive polymer cathode (typically PEDOT or PEDOT:PSS) and a Cu lead-frame. Emerging over the past two decades in response to the demanding low-ESR, high ripple-current requirements of central processing unit (CPU) and graphics processing unit (GPU) voltage regulator modules (VRM), 5G base stations, AI accelerators, and electric vehicle low-voltage domains, SAPC has become a strategically important passive component. Compared with liquid aluminum electrolytic capacitors, SAPC eliminates electrolyte dry-out; compared with tantalum polymer capacitors, SAPC avoids surge-induced ignition and offers better cost and volumetric efficiency; compared with large-capacitance MLCC, SAPC is free from DC-bias de-rating and piezoelectric acoustic noise.

Nevertheless, a substantial body of work from the Center for Advanced Life Cycle Engineering (CALCE) at the University of Maryland (Liu, Azarian & Pecht, 2015–2020), the NASA NEPP laboratory (Teverovsky, 2020–2024), and leading manufacturers (Panasonic, KEMET, Nichicon, Kyocera-AVX) has revealed that SAPC exhibits qualitatively new failure behaviors under elevated-temperature-humidity-bias (THB) stress, including (i) ESR runaway and (ii) leakage-current (LC) runaway modes that correlate strongly with PEDOT deposition technology.

This review systematically surveys the past two decades of SAPC research along a closed loop of manufacturing → characterization → failure modes → failure mechanisms → reliability modeling → process improvement, with more than 55 peer-reviewed citations. The review presents the device structure, etching / formation / cathode-deposition / stacking / encapsulation process flows, laboratory characterization techniques (electrical, EIS, X-ray CT, SEM/TEM/EDS, TGA/DSC, FT-IR/XPS), failure-mode taxonomy, underlying physicochemical mechanisms (PEDOT thermo-oxidation, PSS hydrolysis, interfacial delamination, anodic oxide breakdown, reverse self-healing), reliability models (Weibull, Arrhenius, inverse-power law, generalized Eyring, physics-of-failure, CNN-LSTM and PINN), and quantitative improvement strategies at material, process, package and system levels.

Keywords: stacked aluminum polymer capacitor; PEDOT; conducting polymer cathode; failure mode; failure mechanism; reliability modeling; accelerated life test; remaining useful life; CNN-LSTM; physics-of-failure.
""")
    add_page_break(doc)


def build_toc(doc):
    add_heading(doc, "目  录", level=0)
    items = [
        ("摘 要", "I"),
        ("Abstract", "II"),
        ("第一章 绪论", "1"),
        ("    1.1 SAPC 的起源与定义", "1"),
        ("    1.2 历史演化与技术代际", "3"),
        ("    1.3 在电力电子系统中的地位", "6"),
        ("    1.4 国内外研究现状综述", "8"),
        ("    1.5 本综述的范围、方法与组织", "11"),
        ("第二章 结构、材料与基本原理", "13"),
        ("    2.1 总体结构与各功能层功能", "13"),
        ("    2.2 蚀刻铝阳极箔", "16"),
        ("    2.3 Al₂O₃ 阳极氧化膜介质", "19"),
        ("    2.4 PEDOT 类导电聚合物阴极", "22"),
        ("    2.5 碳/银浆过渡层与引线框架", "25"),
        ("    2.6 等效电路模型", "27"),
        ("第三章 制造工艺与工艺-可靠性耦合", "30"),
        ("    3.1 工艺流程总览", "30"),
        ("    3.2 阳极箔蚀刻工艺", "32"),
        ("    3.3 阳极氧化 (化成) 工艺", "35"),
        ("    3.4 PEDOT 阴极沉积工艺", "38"),
        ("    3.5 多层叠堆与压紧烧结", "42"),
        ("    3.6 端电极与封装密封", "44"),
        ("    3.7 筛选与老炼工艺", "46"),
        ("第四章 表征与检测方法", "48"),
        ("    4.1 电学参数表征", "48"),
        ("    4.2 电化学阻抗谱 (EIS)", "51"),
        ("    4.3 X 射线显微 CT 与 C-SAM", "54"),
        ("    4.4 SEM / TEM / EDS 微结构分析", "56"),
        ("    4.5 TGA / DSC 热分析", "58"),
        ("    4.6 FT-IR / Raman / XPS 化学分析", "60"),
        ("第五章 SAPC 典型失效模式", "62"),
        ("    5.1 失效模式分类框架", "62"),
        ("    5.2 参数漂移模式 (ESR / C / DF)", "64"),
        ("    5.3 漏电流跑飞与短路模式", "67"),
        ("    5.4 开路模式 (端电极与内部连接失效)", "70"),
        ("    5.5 外观与密封失效", "72"),
        ("    5.6 失效模式与应用工况的映射", "74"),
        ("第六章 SAPC 失效机理", "76"),
        ("    6.1 PEDOT 阴极的热氧化降解", "76"),
        ("    6.2 PSS 水解与酸性腐蚀", "80"),
        ("    6.3 界面分层与热机械失效", "83"),
        ("    6.4 Al₂O₃ 介质场致击穿与老化", "86"),
        ("    6.5 自愈机理与其有限性", "88"),
        ("    6.6 多应力耦合下的机理交互", "90"),
        ("第七章 可靠性建模方法", "92"),
        ("    7.1 Weibull 与对数正态统计模型", "92"),
        ("    7.2 Arrhenius-逆幂律双应力模型", "95"),
        ("    7.3 Prokopowicz-Vaskas 方程的局限性", "97"),
        ("    7.4 广义 Eyring 多应力模型", "99"),
        ("    7.5 Physics-of-Failure 模型", "101"),
        ("    7.6 数据驱动与 PINN 混合模型", "103"),
        ("第八章 工艺改进与可靠性提升策略", "106"),
        ("    8.1 材料级改进", "106"),
        ("    8.2 工艺级改进", "108"),
        ("    8.3 封装级改进", "110"),
        ("    8.4 应用与系统级改进", "112"),
        ("    8.5 未来发展与挑战", "114"),
        ("结 论", "116"),
        ("附录 A  符号与缩略语表", "118"),
        ("附录 B  加速试验设计范例", "120"),
        ("附录 C  典型案例分析", "122"),
        ("参考文献", "126"),
    ]
    for item, page in items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.25
        r = p.add_run(item + "  " + "·" * max(3, 80-len(item)-len(page)) + "  " + page)
        set_cn_font(r, font_name="宋体", size_pt=10.5)
    add_page_break(doc)


def build_chapter1(doc):
    add_heading(doc, "第一章 绪论", level=1)

    add_heading(doc, "1.1 SAPC 的起源与定义", level=2)
    add_body(doc, """
电容器是现代电子信息产业与电力电子工业中用量最大、品类最丰富的无源元件之一。按阴极电解质的形态划分，铝电容器可分为三大类：以硼酸铵、己二酸铵等溶质与 γ-丁内酯、乙二醇为溶剂的液态铝电解电容器 (liquid aluminum electrolytic capacitor, L-Alcap)，以聚吡咯 (PPy)、聚噻吩衍生物 (PEDOT / PEDOT:PSS) 等导电聚合物为阴极的固态聚合物铝电容器 (solid polymer aluminum capacitor, SP-Alcap)，以及同时使用液态电解液与固态导电聚合物的混合型铝电容器 (hybrid aluminum capacitor, H-Alcap) [1][2][3]。

叠层铝固态聚合物电容器 (stacked aluminum polymer capacitor, SAPC) 是固态聚合物铝电容器的一个重要分支，其关键特征在于：(1) 采用多片蚀刻铝阳极箔堆叠而成，介质层为薄型 Al₂O₃ 阳极氧化膜，阴极为 PEDOT 或 PEDOT:PSS 等导电聚合物；(2) 通过 Cu 引线框架代替传统的卷绕结构与铝外壳；(3) 整体以环氧树脂模塑成型，并以 AEC-Q200 或 IPC-9592 为主要认证基准；(4) 额定电压通常处于 2~35 V 之间，单体容量 10~1000 μF，典型 ESR 仅 3~15 mΩ，纹波电流承载能力达 2~8 A。典型商用系列包括 Panasonic SP-Cap (EEF 系列)、Sanyo/Panasonic POSCAP (TP/TQ 系列，铝型号又名 SP-Cap)、Nichicon LV/LX/LZ 系列、KEMET A700/A750/A780 系列、Kyocera-AVX APV/RPA 系列以及 Chemi-Con PSG/PSF 系列 [4][5][6][7]。

从功能角度，SAPC 可视为一种"低 ESR、低 ESL、高纹波耐受、无电解液蒸发寿命瓶颈"的中高容量 SMT 电容器，其主要竞争对手是 CPU/GPU 供电环节使用的钽聚合物电容器 (Ta-polymer capacitor) 与大容量 MLCC。在 Panasonic 官方技术文献中，SP-Cap 被明确定位为"针对 DC-DC 转换器输入输出滤波的高端 SMT 电容"，并推荐用于对电压稳定度、低纹波、耐回流焊温度有严格要求的场景 [4]。
""")
    add_figure(doc, 'fig02_structure.png',
               '图 2-1  SAPC 典型横截面分层结构示意图（蚀刻铝阳极 + Al₂O₃ 介质 + PEDOT 阴极 + 碳/银浆过渡层 + Cu 引线框架 + 环氧封装）')

    add_heading(doc, "1.2 历史演化与技术代际", level=2)
    add_body(doc, """
SAPC 的技术演化可大致划分为以下五个阶段：

(1) 萌芽阶段 (1983—1990 年)。1983 年 Sanyo 公司率先基于 TCNQ 电荷转移络合盐开发了 OS-CON 系列固态铝电容器，但因 TCNQ 的热不稳定性与成本问题而未能大规模推广。Aoki 等 (1990) 系统报告了以聚吡咯替代 TCNQ 的初步探索 [8]。该阶段的 SAPC 仍以单片或卷绕结构为主，叠层工艺尚未成熟。

(2) PEDOT 阴极引入阶段 (1990—2000 年)。1988 年 Bayer AG 公司合成了 EDOT 单体，并于 1992 年申请了 PEDOT 作为导电聚合物的专利。PEDOT 相较 PPy 具有更高的热稳定性 (分解温度 > 250°C)、更好的电导率稳定性以及更低的环境敏感性，迅速成为 SAPC 阴极材料的首选 [9][10]。1998—2000 年间，Sanyo POSCAP 与 Panasonic SP-Cap 开始将 PEDOT 阴极导入叠层结构，标志着现代 SAPC 雏形的形成。

(3) 商用大规模普及阶段 (2000—2010 年)。随着 Intel Pentium 4 处理器核电压降至 1.5 V 以下、峰值电流突破 50 A，对 CPU VRM 的电容器 ESR 提出了新要求。SAPC 凭借 5~15 mΩ 的典型 ESR 和数安培级别的纹波电流承载能力，快速占据主板 VRM 输出滤波电容位置。这一阶段日本企业 (Sanyo、Panasonic、NEC Tokin、Nichicon) 占据了全球 80% 以上的 SAPC 市场份额 [11]。

(4) 性能与工艺精细化阶段 (2010—2020 年)。此阶段以 Panasonic SP-Cap KX/JX 系列、KEMET A700H/A750 系列为代表，实现了 125°C 工作温度下 5000~7000 小时的 endurance 指标，耐回流焊温度稳定在 260°C [4][12]。与此同时，学术界开始系统开展 SAPC 失效机理研究：Liu 等在 CALCE 实验室发表了一系列高温高湿环境下 PA 电容失效的论文 [13][14][15]；KEMET 的 Freeman 等对 PEDOT 阴极在 85°C/85%RH 下的电导率退化行为开展了深入研究 [16]。

(5) 新材料与智能化阶段 (2020 年以来)。伴随 AI 服务器、电动汽车与 5G/6G 基站对电容器高温可靠性提出的新要求，Panasonic 于 2022 年发布了 KX 系列"125°C/5500h"长寿命 SP-Cap，号称行业最长耐久性 [17]；与此同时 NASA NEPP 的 Teverovsky 博士于 2024 年发布了《Stress Testing of Chip Aluminum Polymer Capacitors》报告，首次系统给出了 SAPC 在 125°C/1.9 倍额定电压下的 HALT 数据与激活能估计 [18]；机器学习方法也开始被引入 SAPC 的 RUL 预测。
""")
    add_figure(doc, 'fig01_market.png',
               '图 1-1  2023 年全球电容器出货量按类型分布示意图（SAPC 占约 3%，但在高端 VRM 场景中占比显著更高）')

    add_heading(doc, "1.3 在电力电子系统中的地位", level=2)
    add_body(doc, """
尽管 SAPC 在全球电容器出货量中的份额仅约 3%（图 1-1），但在高端电力电子装备中，其地位远超这一比例所能反映。这是因为 SAPC 专门定位于"高纹波、低 ESR、抗回流焊"的中高端应用，其替代对象——大容量 MLCC 与钽聚合物电容——都存在明确的技术边界。

具体地：
第一，在 CPU/GPU/FPGA 的核心电压供电模块 (VRM) 中，1 V 级别以下的低压大电流输出对电容器 ESR 提出了极致要求。以典型 AMD/Intel 服务器 CPU 的核电压 VDDQ 为例，在 200 A 负载下，输出滤波电容的 ESR 每升高 1 mΩ 意味着稳态电压降 0.2 V，对应数百瓦功耗损失。SAPC 典型 5~15 mΩ 的 ESR 使其成为 VRM 输出滤波的理想选择。Panasonic 官方文献指出，SP-Cap 在 VRM 场景的典型配置是"2~4 只 470 μF/2.5 V + 并联 MLCC" [4]。

第二，在 5G 基站与 AI 服务器的 48 V 母线转中间母线 (MBC) 转换中，纹波电流常达数安培。大容量钽聚合物电容虽然 ESR 更低，但其单位容量成本是 SAPC 的 2~4 倍；大容量 MLCC 则存在 DC 偏置下严重的容量损失（X5R 介质在额定电压下容量可能下降 40~70%）。SAPC 在此场景具有最优的性价比。

第三，在 EV 的 48 V 辅助域、车载以太网与充电控制器中，SAPC 凭借 AEC-Q200 合规性与优异的温度特性，已成为 Tier 1 供应商的常用选择。尽管其应用仍受"湿度敏感"制约（多数厂家推荐工作湿度 < 85%RH），但与 MLCC 相比，SAPC 不存在压电噪声问题，更适合用作音频前级与精密测量前端的供电滤波。

第四，在对信号完整性要求苛刻的高速串行总线 (PCIe Gen5/6、112 Gb/s SerDes) 设计中，SAPC 凭借 2~3 nH 的典型 ESL 与平坦的中高频阻抗，成为局部旁路网络 (local decoupling network, LDN) 的重要组成部分。
""")
    add_figure(doc, 'fig05_esr_compare.png',
               '图 1-2  五类主流电容器的阻抗频率响应对比（SAPC 在 10 kHz ~ 1 MHz 范围内具有最低的 |Z|）')

    add_heading(doc, "1.4 国内外研究现状综述", level=2)
    add_body(doc, """
针对 SAPC 的学术研究可大致归为四条主线。

第一条主线是失效物理与可靠性。美国马里兰大学 CALCE 团队的 Liu、Azarian、Pecht 等自 2013 年起系统开展了 SAPC 在高温高湿偏压下的失效研究 [13][14][15]。其代表性成果包括：2015 年博士论文 "Reliability Evaluation of Liquid and Polymer Aluminum Electrolytic Capacitors" 给出了 SAPC 与液态铝电容器在寿命建模维度上的对比 [13]；2016 年工作首次提出"封装几何影响水汽驱动退化"的定量观测 [19]；2017 年发表于 IEEE Transactions on CPMT 的文章报告了两家不同厂商 SAPC 分别呈现 ESR 跑飞和 LC 跑飞两种主导模式 [14]；2020 年 CALCE CWS 系列报告进一步扩展到叠层多片结构 PA 电容的可靠性评估 [15]。这一系列工作奠定了当前学术界对 SAPC 可靠性的基本认识框架。

NASA 元器件可靠性项目 NEPP 的 Teverovsky 博士自 2016 年起持续跟踪钽聚合物电容与聚合物铝电容的空间应用可靠性 [20][21][22]。其 2024 年发表的 Stress Testing of Chip Aluminum Polymer Capacitors 报告基于 85°C 与 125°C、1.2~1.9 倍额定电压的 HALT 实验，拟合得到激活能约 0.7 eV、电压指数约 3~4，为航天应用的 SAPC 寿命外推提供了可信依据 [18]。

第二条主线是导电聚合物阴极材料。Bayer (现 Heraeus) 公司对 PEDOT/PSS 体系的长期研究形成了 CLEVIOS™ 系列产品 [9]。学术界对 PEDOT 热稳定性 [23]、PSS 酸性水解 [24]、PEDOT:PSS 的吸湿膨胀行为 [25][26]、PEDOT 在光/氧/水共同作用下的降解 [27] 都开展了系统的分子尺度研究。Shi 等 2021 年在 J Mater Sci: Mater Electron 上发表的气相聚合 (VPP) PEDOT 薄膜制备工艺对叠层固态电容器给出了新的工艺路线 [28]。

第三条主线是工艺与器件设计。日本企业、KEMET 与 Kyocera-AVX 长期主导叠层结构、引线框架布局、多层端电极沉积等工艺改进。Freeman (KEMET) 等指出，相较于 in-situ 聚合的 PEDOT:Tos，采用预聚合 PEDOT:PSS 分散液在高湿条件下稳定性显著更优 [16]。Panasonic 2022 年 KX 系列白皮书披露了其在"端电极双层密封 + 低吸湿环氧"方面的工艺改进 [17]。

第四条主线是数据驱动预测。Zhu 等 2025 年在 MDPI Electronics 发表的 CNN-LSTM 模型考虑了参数离散度的影响，对聚合物铝电容和钽电容的 RUL 给出了较传统 LSTM 更高的预测精度 [29]。此外，基于物理信息神经网络 (PINN) 的方法正在快速发展，可望在小样本条件下获得更好的外推性。

然而，截至 2025 年中，SAPC 领域仍有若干重要问题悬而未决：(1) PEDOT 阴极在高湿下的去掺杂与 PSS 水解机理在分子尺度上尚缺乏定量统一描述；(2) 叠层结构中每一层 Al₂O₃/PEDOT 界面的独立寿命分布与并联/串联统计模型仍待完善；(3) 多应力耦合（温度 × 电压 × 湿度 × 纹波电流 × 振动）下的加速等效关系仍缺少实验验证；(4) 基于机器学习的 RUL 预测在工业现场的部署仍处于示范阶段，尚未大规模商用。
""")

    add_heading(doc, "1.5 本综述的范围、方法与组织", level=2)
    add_body(doc, """
本综述聚焦于叠层铝固态聚合物电容器 (SAPC)，不深入讨论卷绕式铝聚合物电容器、钽聚合物电容器、液态铝电解电容器与超级电容器；但在需要对比的语境下会简要提及上述器件。综述的文献范围为：IEEE Transactions on CPMT / Dielectrics and Electrical Insulation / Industry Applications、Elsevier Microelectronics Reliability / Journal of Power Sources / Journal of Applied Polymer Science、Nature Communications、RSC Journal of Materials Chemistry / Energy & Environmental Science、Springer Journal of Materials Science: Materials in Electronics、MDPI Electronics / Materials / Polymers、AIP Applied Physics Letters / Journal of Applied Physics 以及 NASA NEPP、KEMET、Panasonic、Nichicon、Murata 等权威机构的白皮书。

本综述采用"纵向链 + 横向比较"的二维组织方法：纵向链指的是"材料与结构 → 制造工艺 → 表征方法 → 失效模式 → 失效机理 → 可靠性建模 → 工艺改进"的研究闭环；横向比较则针对不同制造商 (Panasonic/Nichicon/KEMET/Chemi-Con/AVX) 、不同工艺路线 (in-situ/pre-polymerized/VPP) 、不同介质厚度与电压等级进行跨对象分析。

全综述共包含 8 个主要章节与 3 个附录：
第 1 章 绪论，确立研究背景；
第 2 章 结构、材料与基本原理；
第 3 章 制造工艺与工艺-可靠性耦合；
第 4 章 表征与检测方法；
第 5 章 典型失效模式；
第 6 章 失效机理；
第 7 章 可靠性建模方法；
第 8 章 工艺改进与可靠性提升策略；
附录 A 符号与缩略语表；
附录 B 加速试验设计范例；
附录 C 典型案例分析；
参考文献。

希望本综述能够为电容器材料学家、可靠性工程师、电源系统设计者以及质量保证专业人员提供一份体系化的、具有代表性的参考文献。
""")
    add_page_break(doc)


def build_chapter2(doc):
    add_heading(doc, "第二章 结构、材料与基本原理", level=1)

    add_heading(doc, "2.1 总体结构与各功能层功能", level=2)
    add_body(doc, """
如图 2-1 所示，典型的 SAPC 沿垂直方向由 3~12 片蚀刻铝阳极箔堆叠而成，每片阳极箔在蚀刻后表面呈现致密的隧道状微孔，之后通过阳极氧化在箔表面生成约 10~100 nm 的 Al₂O₃ 薄层作为介质；接下来在 Al₂O₃ 表面沉积导电聚合物 PEDOT 作为阴极，其上再依次沉积碳浆层 (为 PEDOT 与银浆层之间的欧姆接触过渡) 和银浆层 (用于将阴极电流引至 Cu 阴极引线框架)；阳极箔的一端通过激光焊接或超声焊接与 Cu 阳极引线框架连接；最外层为环氧树脂模塑封装。

各功能层的物理化学角色如下：
(1) 阳极 Al 箔：既是电子导体又是介质的形成基体，其表面积的放大倍率 (通常 20~100×) 决定了电容密度的上限；
(2) Al₂O₃ 介质：真正的电场承载层，其厚度与阳极氧化电压近似成正比 (约 1.4 nm/V)；
(3) PEDOT 阴极：作为电子/离子混合导体完成阴极电流的引出；
(4) 碳浆过渡层：为解决 PEDOT 与银浆层之间欧姆接触不良的问题；
(5) 银浆层：低电阻电流汇集层；
(6) Cu 引线框架：提供电极与外部系统的电连接，同时作为散热路径；
(7) 环氧封装：提供机械支撑、绝缘以及有限的湿度屏障。

相较于传统的卷绕式液态铝电容器，SAPC 的结构优势主要体现在三个方面：(1) 叠层结构比卷绕结构具有更短的电流路径，从而拥有更低的 ESL 和 ESR；(2) 无液态电解液意味着无电解液蒸发与干涸失效模式；(3) 引线框架 + 环氧封装相较于铝壳 + 橡胶密封塞，在 SMT 回流焊温度 (260°C) 下的热稳定性更好。然而，该结构也带来了新的失效模式，特别是 PEDOT 阴极的高温高湿退化以及引线框架与陶瓷封装之间的 CTE 失配导致的层间分层——这些将在第 6 章进一步分析 [14][16]。
""")

    add_heading(doc, "2.2 蚀刻铝阳极箔", level=2)
    add_body(doc, """
铝阳极箔是 SAPC 的核心。其基底通常采用纯度 ≥99.99% 的低压电子级铝箔 (high-purity aluminum foil)，典型厚度 80~130 μm。根据额定电压等级的不同，蚀刻工艺可分为低压型 (直流蚀刻 DC etching，用于 Vr ≤ 10 V) 与中压型 (交流蚀刻 AC etching，用于 10 < Vr ≤ 50 V)。SAPC 由于典型额定电压只有 2~35 V，主要采用低压直流蚀刻工艺 [30][31][32]。

直流蚀刻的典型工艺参数：电解液为 HCl + H₂SO₄ 混合溶液，浓度约 1~3 mol/L；蚀刻电流密度约 0.2~1.0 A/cm²；温度 75~85°C；蚀刻时间数十秒至数分钟。其核心反应是以下的电化学腐蚀：
""")
    add_formula(doc, "Al + 3Cl⁻ → AlCl₃ + 3e⁻ (anodic)")
    add_formula(doc, "2H⁺ + 2e⁻ → H₂↑ (cathodic)")
    add_body(doc, """
上述反应并非均匀腐蚀，而是沿 Al (100) 晶面优先蚀刻形成直径约 0.2~2 μm、深度 10~40 μm 的隧道状孔 (tunnel pits)。蚀刻隧道的密度、直径与深度分布直接决定了阳极箔的有效表面积放大倍率，从而决定单位面积电容。Du 等 (2019) 系统研究了隧道侧向分支层 (branched layer) 对比表面积的影响，指出过度的分支层反而会减小有效表面积，其关键是在主隧道伸长与分支生成之间的精确平衡 [32]。MDPI Metals (2025) 最新报道了通过控制痕量杂质元素 (Cu, Fe) 的钝化作用精确调控坑隙起始与生长的方法 [33]。
""")
    add_figure(doc, 'fig03_etch_formation.png',
               '图 2-2  铝阳极箔蚀刻 (tunnel pitting) 与阳极氧化 (formation) 工艺示意')

    add_heading(doc, "2.3 Al₂O₃ 阳极氧化膜介质", level=2)
    add_body(doc, """
阳极氧化 (formation / anodization) 是在蚀刻好的铝箔表面通过电化学氧化生成 Al₂O₃ 介质层的工艺。电解液通常为硼酸铵、己二酸铵或磷酸铵水溶液，pH 中性或弱酸性；工艺电压 V_form 约为 1.2~1.5 倍工作电压 V_R，反应时间约数分钟到数十分钟，温度 85~95°C。其总反应可写为：
""")
    add_formula(doc, "2Al + 3H₂O → Al₂O₃ + 6H⁺ + 6e⁻")
    add_body(doc, """
Al₂O₃ 氧化膜呈非晶态，其厚度 d 与化成电压 V_form 之间遵循经验关系 d ≈ 1.4 nm/V (即"anodic ratio")。SAPC 额定电压 6.3 V 对应的介质厚度约 9~10 nm；25 V 对应约 35 nm。Al₂O₃ 的相对介电常数 ε_r 约为 8.5~10，击穿场强 E_BD 可达 7~10 MV/cm。

值得强调的是，Al₂O₃ 介质层的物理完整性高度依赖于阳极箔表面的平整度和蚀刻隧道的形貌。在隧道锐角处、微夹杂处或残余应力集中处，阳极氧化膜容易出现"化成缺陷"——薄弱点或未完全化成的区域，这些缺陷是 SAPC 早期失效与浪涌击穿的主要诱因 [34][35]。为此，业界普遍采用"再化成" (reformation) 工艺，即在蚀刻-化成基础上再经过一次低电流密度下的电化学修复，以弥合微观缺陷。

对于液态铝电容器，电解液中的水分可以持续对缺陷区域进行"在线再化成"，形成电容器的经典自愈机制。而对于 SAPC，固态 PEDOT 阴极基本不含游离水，使得这种自愈机制大大减弱，成为 SAPC 对化成质量要求更严格的根本原因之一 [36]。
""")

    add_heading(doc, "2.4 PEDOT 类导电聚合物阴极", level=2)
    add_body(doc, """
PEDOT (poly-3,4-ethylenedioxythiophene) 是 SAPC 阴极最主流的导电聚合物。其分子结构来源于 EDOT (3,4-乙撑二氧噻吩) 单体的氧化聚合反应：
""")
    add_formula(doc, "n EDOT + n A⁻ → PEDOTⁿ⁺·nA⁻ + 2n H⁺ + 2n e⁻")
    add_body(doc, """
其中 A⁻ 可为对甲基苯磺酸根 (Tos⁻)、聚苯乙烯磺酸根 (PSS⁻)、氯离子等掺杂反阴离子 [9][37][38]。PEDOT 在 p-型掺杂状态下具有极高的电导率 (100~10³ S/cm) 与良好的热稳定性 (分解温度 > 250°C)，是目前工业界最成熟的有机导电聚合物。

从器件角度讲，SAPC 对 PEDOT 阴极的关键要求包括：(1) 高电导率——直接决定 ESR；(2) 对 Al₂O₃ 介质的优良润湿性与孔隙填充能力——决定有效接触面积；(3) 良好的热稳定性——耐受 260°C 回流焊和 125°C 长期工作；(4) 低吸湿性——决定高湿环境可靠性；(5) 化学惰性——不与 Al₂O₃ 发生反应。

图 2-3 汇总了 PEDOT 的分子结构与三种主要沉积路线：
""")
    add_figure(doc, 'fig04_pedot_chem.png',
               '图 2-3  PEDOT 的化学结构及其在 SAPC 中的三种主要沉积工艺')

    add_body(doc, """
(1) 在位化学聚合 (in-situ polymerization)：将 EDOT 单体与氧化剂 Fe(OTs)₃ 依次浸渍到蚀刻好的阳极箔上，在 50~80°C 下反应 0.5~2 小时生成 PEDOT:Tos。其优点是工艺成熟、电导率高 (200~500 S/cm)、对微孔填充能力好；缺点是反应过程伴随 Fe 残留与多次浸渍所带来的工艺变异性 [16][37]。

(2) 预聚合分散液 (pre-polymerized dispersion)：直接浸渍已经聚合好的 PEDOT:PSS 水溶液分散液 (商品名 CLEVIOS™ P)。其优点是工艺简单、批次稳定性好；缺点是 PEDOT:PSS 胶体颗粒尺寸 (30~100 nm) 大于大部分蚀刻隧道 (< 1 μm 时)，对微孔的渗入能力有限，导致电导率偏低 (1~100 S/cm) 以及孔隙填充率偏低 [16][24]。

(3) 气相聚合 (vapor-phase polymerization, VPP)：首先将 Fe(OTs)₃ 的甲醇溶液涂布在阳极箔上作为氧化剂层，然后放入 EDOT 蒸汽环境中气相反应。VPP 的优点是得到的 PEDOT 薄膜具有最高的电导率 (> 10³ S/cm)、最好的孔隙填充和最均匀的厚度分布；缺点是设备成本高、工艺窗口窄、要求严格的温度与湿度控制 [28][39][40]。

许多厂商已采用"混合工艺"——预先 VPP 沉积一层 PEDOT 进入微孔深处，再用预聚合分散液填充外层，以兼顾电导率和宏观稳定性。Panasonic 在 SP-Cap KX 系列白皮书中暗示采用了类似的复合工艺 [17]。
""")

    add_heading(doc, "2.5 碳/银浆过渡层与引线框架", level=2)
    add_body(doc, """
在 PEDOT 阴极与 Ag 浆层之间，通常需要沉积一层 1~10 μm 厚的碳浆过渡层 (carbon paint)。其作用包括：(1) 改善 PEDOT/Ag 界面的欧姆接触，避免 Ag 向 PEDOT 扩散引起高阻抗界面；(2) 提供电化学惰性屏障，防止 Ag 在湿度下的离子迁移；(3) 作为柔性应力缓冲层，抵消 PEDOT 与 Ag 之间的 CTE 失配。

银浆层 (silver paint) 厚度通常 10~50 μm，由环氧树脂基体中的银薄片 (flake) 填充而成。其电阻率约 10⁻⁴~10⁻³ Ω·cm，远低于 PEDOT 层，确保了阴极侧的低电阻汇流。Cu 引线框架是 SAPC 的机械骨架，通常采用镀 Sn、镀 Ni/Pd/Au 或多层复合镀层以保证焊接可靠性。框架的厚度典型 0.2~0.5 mm，对应了 SAPC 的整机 SMT 厚度 (如 A 类 7.3×4.3×1.9 mm 或 D 类 7.3×4.3×2.8 mm) [4][5]。
""")

    add_heading(doc, "2.6 等效电路模型", level=2)
    add_body(doc, """
SAPC 的 ACV 等效电路可以由如下的集总参数模型描述：
""")
    add_formula(doc, "Z(jω) = ESR + jωESL + 1/(jωC) + R_p ∥ 1/(jωC_p)")
    add_body(doc, """
其中 C 为主电容 (由 Al₂O₃ 介质决定)、ESR 为综合欧姆损耗、ESL 为寄生串联电感、R_p 与 C_p 分别为 PEDOT/Al₂O₃ 界面的等效电荷转移阻抗与双电层电容。

从物理角度，ESR 可以分解为：
""")
    add_formula(doc, "ESR = R_Al + R_oxide + R_PEDOT + R_C/Ag + R_frame + R_solder")
    add_body(doc, """
其中 R_Al 为铝箔欧姆电阻、R_oxide 为 Al₂O₃ 介质损耗换算电阻、R_PEDOT 为 PEDOT 阴极欧姆电阻、R_C/Ag 为碳/银浆层欧姆电阻、R_frame 为引线框架电阻、R_solder 为焊接接触电阻。在室温下、100 kHz 频率处，对于 6.3V/470μF 的典型 SAPC，各贡献约为：R_Al ≈ 1.5 mΩ、R_oxide ≈ 1.5 mΩ、R_PEDOT ≈ 4 mΩ、R_C/Ag ≈ 2 mΩ、R_frame ≈ 1 mΩ、R_solder ≈ 0.5 mΩ，合计约 10 mΩ，与厂家规格吻合 [4][6][14]。

可以看到，PEDOT 阴极的欧姆电阻是 ESR 的最大单项贡献，这是为什么 PEDOT 材料的电导率退化几乎等价于 SAPC 的 ESR 退化。这一点在第 6 章失效机理中会进一步展开讨论。

SAPC 的自谐振频率 f_SR = 1/(2π√(ESL·C))，典型值为 1~10 MHz。超过自谐振频率后，SAPC 表现为感性，不再具备电容滤波作用——这也解释了为什么在 100 MHz 以上的高频退耦环节仍需要并联 MLCC [4][5][41]。
""")
    add_figure(doc, 'fig05_esr_compare.png',
               '图 2-4  不同类型电容器的 |Z|-f 曲线对比（SAPC 在 10 kHz ~ 1 MHz 区间具有最低 |Z|）')
    add_page_break(doc)
