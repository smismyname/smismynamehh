# -*- coding: utf-8 -*-
"""可靠性建模 + 工艺改进 + 结论 + 附录 + 参考文献"""
from docx_utils import (add_heading, add_body, add_page_break, add_figure,
                         add_formula, add_table, add_quote, add_reference_item,
                         set_cn_font)


def build_chapter7(doc):
    add_heading(doc, "第七章 可靠性建模方法", level=1)

    add_body(doc, """
SAPC 的可靠性建模在过去 10 年经历了从统计模型 → 物理失效模型 → 数据驱动模型的演进。本章按照这一脉络系统评述主要建模方法、各自适用范围、局限以及最新进展。
""")

    add_heading(doc, "7.1 Weibull 与对数正态统计模型", level=2)
    add_body(doc, """
Weibull 分布是电容器寿命数据分析的最主流工具。对 SAPC 的 THB 加速老化数据，两参数 Weibull 分布：
""")
    add_formula(doc, "F(t) = 1 - exp[-(t/η)^β]")
    add_body(doc, """
中的形状参数 β 通常为 1.2-2.5，对应耗损型失效；尺度参数 η 为特征寿命 (63.2% 失效时间)。

CALCE 的 Liu 等 (2017) [14] 对 Nichicon 220μF/20V SAPC 在 85°C/85%RH/V_R 下的 Weibull 拟合给出 β = 2.1, η = 1800 h；对 Chemi-Con 同规格产品给出 β = 1.3, η = 650 h——两者的显著差异反映了制造工艺对寿命分布的根本性影响。图 7-1 展示了典型的 Weibull 概率图。
""")
    add_figure(doc, 'fig07_weibull.png',
               '图 7-1  两厂商 SAPC 产品 THB 试验失效时间的 Weibull 概率图')

    add_body(doc, """
除两参数 Weibull 外，对数正态分布 (lognormal) 也常用于 SAPC 寿命拟合，特别是当失效机理涉及多步扩散过程 (如水分扩散→PSS 水解→Al₂O₃ 腐蚀) 时。一般规律是：若 β > 1.5 则 Weibull 更合适；若分布严重偏正则 lognormal 更合适。实用上常同时拟合两种分布并根据 K-S 检验或 Anderson-Darling 检验选择更合适的分布 [58]。

NASA NEPP 的 Teverovsky 进一步提出混合 Weibull 模型，即用两组 Weibull 参数分别描述"早期缺陷型失效"和"耗损型失效"，混合形式为：
""")
    add_formula(doc, "F(t) = p·F₁(t; β₁, η₁) + (1-p)·F₂(t; β₂, η₂)")
    add_body(doc, """
其中 p 为早期失效占比。该模型对于经过老炼筛选的 SAPC 数据拟合尤其合适——p 通常在 1-5% 之间 [18]。
""")

    add_heading(doc, "7.2 Arrhenius-逆幂律双应力模型", level=2)
    add_body(doc, """
温度与电压是 SAPC 最主要的两个加速应力。对温度，加速因子 AF_T 遵循 Arrhenius 方程：
""")
    add_formula(doc, "AF_T = exp[(E_a/k)(1/T_use - 1/T_stress)]")
    add_body(doc, """
其中 k = 8.617×10⁻⁵ eV/K 为玻尔兹曼常数。对 SAPC，PEDOT 降解的 E_a 经 Teverovsky 2024 [18] 的 HALT 数据拟合约为 0.73 eV。图 7-2 展示了基于此激活能的寿命外推：在 85°C 使用条件下外推的 t₆₃ 约为 10⁴ h；在 65°C 则延长至约 5×10⁴ h (约 5.7 年)。
""")
    add_figure(doc, 'fig08_arrhenius.png',
               '图 7-2  基于 E_a = 0.73 eV 的 SAPC Arrhenius 寿命外推曲线')

    add_body(doc, """
对电压，加速因子 AF_V 通常遵循逆幂律 (inverse power law)：
""")
    add_formula(doc, "AF_V = (V_stress/V_use)^n")
    add_body(doc, """
对 SAPC，n 约为 3-5 [14][18]。对比：MLCC n ≈ 4-7，钽电容 n ≈ 15-40。SAPC 的 n 较低说明其寿命对电压相对不那么敏感，这是因为 SAPC 中 Al₂O₃ 介质层远低于本征击穿极限。

综合温度与电压的双应力加速因子为：
""")
    add_formula(doc, "AF = AF_T · AF_V = (V_s/V_u)^n · exp[(E_a/k)(1/T_u - 1/T_s)]")

    add_heading(doc, "7.3 Prokopowicz-Vaskas 方程的局限性", level=2)
    add_body(doc, """
Prokopowicz-Vaskas (PV) 方程是陶瓷电容器行业经典的双应力加速方程，已有 50 余年的应用历史：
""")
    add_formula(doc, "t₁/t₂ = (V₂/V₁)^n · exp[(E_a/k)(1/T₁ - 1/T₂)]")
    add_body(doc, """
然而对 SAPC 而言，PV 方程的直接应用存在如下局限：
(1) PV 方程假设失效机理在应力范围内不变，而 SAPC 在 < 85°C 下主要为 PEDOT 降解、> 125°C 则可能出现 Al₂O₃ 界面失稳，机理切换使 PV 方程外推失效；
(2) PV 方程不含湿度项，而对 SAPC 湿度是一阶应力；
(3) PV 方程的 n 值在不同电压区间可能不同——低电压 (< V_R) 下 n 较小 (3-4)，高电压 (≥ 1.5 V_R) 下 n 变大 (5-8)；
(4) PV 方程不能描述机械/振动应力。

因此对 SAPC 的准确外推，PV 方程只能作为温度-电压两应力下的第一近似，必须结合湿度 Eyring 项使用 [14][18]。
""")

    add_heading(doc, "7.4 广义 Eyring 多应力模型", level=2)
    add_body(doc, """
广义 Eyring 模型是 Arrhenius-逆幂律模型的推广形式，可同时容纳温度、电压、湿度、振动等多个应力：
""")
    add_formula(doc, "t_f = A · (V)^(-n) · exp(E_a/kT + b·RH + c·g)")
    add_body(doc, """
其中 RH 为相对湿度 (%)，g 为振动加速度水平，b、c 为经验系数。

Liu 等在 CALCE (2017) [14] 与 Teverovsky 在 NASA NEPP (2024) [18] 的加速试验数据联合拟合给出 SAPC 的典型 Eyring 参数：
- E_a ≈ 0.70-0.80 eV；
- n ≈ 3-5；
- b ≈ 0.02-0.04 (每 10% RH 使寿命下降 20-40%)；
- c ≈ 0.05-0.10 (每 g 使寿命下降 50-100%)。

基于这些参数，可以对 SAPC 在任意给定工况下进行寿命外推。例如：对比 85°C/85%RH/V_R 与 65°C/40%RH/0.8V_R 的两种工况，后者的寿命约为前者的 50 倍。

然而广义 Eyring 模型的弱点是：系数 b、c 的拟合需要大量多应力组合试验，成本高昂；且对应力耦合项 (如 T × RH) 的描述仍嫌粗糙。文献中已有工作尝试引入二阶相互作用项，但实证数据尚不充分 [58]。
""")

    add_heading(doc, "7.5 Physics-of-Failure 模型", level=2)
    add_body(doc, """
Physics-of-Failure (PoF) 模型基于对失效微观机理的直接建模，而不依赖于加速因子经验拟合。其一般框架是：识别失效关键变量 (如 PEDOT 电导率 σ_PEDOT)，建立其演化方程，设定失效阈值，求解寿命分布。

对 SAPC 的 ESR 上升模式，PoF 模型可写作：
""")
    add_formula(doc, "dσ/dt = -k₁·σ·exp(-E_a/kT) - k₂·σ·f(RH)")
    add_body(doc, """
其中第一项为 PEDOT 的 Arrhenius 热氧化，第二项为湿度驱动降解。对此微分方程求解可得 σ(t) 的解析表达式，结合失效阈值 σ_crit = σ_0 / 2 即可得到器件寿命。

对 LC 跑飞模式，PoF 模型需要考虑 Al₂O₃ 介质层的缺陷演化：
""")
    add_formula(doc, "dN_defect/dt = α · exp(β·E) · exp(-E_a/kT) · (1 + γ·RH)")
    add_body(doc, """
其中 N_defect 为介质缺陷密度。当 N_defect 超过击穿阈值时 LC 跑飞发生。

PoF 模型的优点在于物理可解释性强，可以外推到 HALT 范围之外的工况；缺点是对各参数 (k₁、k₂、α、β、γ) 的物理意义识别与独立测量要求高。文献中针对 SAPC 的 PoF 模型仍处于探索阶段，尚未形成工业标准 [16][43][57]。
""")

    add_heading(doc, "7.6 数据驱动与 PINN 混合模型", level=2)
    add_body(doc, """
近年来，基于机器学习的 RUL 预测方法在电容器可靠性领域迅速发展。主要方法包括：

(1) LSTM 与 CNN-LSTM 网络：利用时间序列特性预测未来的 C、ESR、LC 走势。Soualhi 等 (2022) [59] 首次将 LSTM 应用于电解电容器 RUL 预测；Zhu 等 (2025) 发表于 MDPI Electronics [29] 的 CNN-LSTM 方法进一步考虑了参数离散度。

(2) 物理信息神经网络 (Physics-Informed Neural Network, PINN)：将 PoF 模型中的微分方程作为损失函数的正则化项，强制神经网络输出满足物理约束。这类方法对小样本具有显著优势。最新 (2025) 的一项工作提出了将 LSTM 骨架与物理约束结合的超级电容 RUL 预测模型，在 20% 训练数据条件下即可获得较好的预测精度 [60]。

(3) Transformer 与注意力机制：长依赖建模能力强，适合长时间跨度 (> 1 年) 的 SAPC 寿命预测，但训练数据要求高。

图 7-3 展示了基于 CNN-LSTM 的 SAPC RUL 预测示例。前 60% 观测期为训练数据，后 40% 为预测段；95% 置信区间随时间扩大，反映不确定性累积。
""")
    add_figure(doc, 'fig13_rul.png',
               '图 7-3  基于 CNN-LSTM 的 SAPC RUL 预测示例（实验数据 + 未来预测段）')

    add_body(doc, """
数据驱动方法的关键挑战是"外推能力"——模型只能在训练数据的应力范围内给出可信预测；超出此范围则需物理模型辅助。因此混合建模 (physics-informed machine learning) 是当前的主流发展方向 [29][60]。

表 7-1 总结了 SAPC 可靠性建模方法的适用性对比。
""")
    add_table(
        doc,
        ["方法类别", "优点", "局限", "最适合的场景"],
        [
            ["Weibull/lognormal", "简单、易解释", "不反映物理机理", "寿命分布拟合"],
            ["Arrhenius-逆幂律", "直接外推", "忽略交互项", "双应力加速试验"],
            ["PV 方程", "工业接受度高", "不含湿度", "MLCC / 部分 SAPC"],
            ["广义 Eyring", "多应力同时", "参数多", "湿度主导工况"],
            ["PoF 微分方程", "机理明确、可外推", "参数识别困难", "基础研究"],
            ["LSTM / CNN-LSTM", "黑箱预测、精度高", "外推能力差", "在线 RUL 监测"],
            ["PINN", "小样本 + 物理", "算法复杂", "新材料早期评估"],
        ],
        caption="表 7-1  SAPC 可靠性建模方法对比"
    )
    add_page_break(doc)


def build_chapter8(doc):
    add_heading(doc, "第八章 工艺改进与可靠性提升策略", level=1)

    add_body(doc, """
本章从材料、工艺、封装、应用四个层级系统讨论 SAPC 可靠性提升的关键策略。每一条策略都结合了具体的机理依据和文献支持。
""")

    add_heading(doc, "8.1 材料级改进", level=2)
    add_body(doc, """
8.1.1 PEDOT 阴极材料改进
(a) 混合掺杂体系。单纯的 PEDOT:Tos 对高湿敏感，单纯的 PEDOT:PSS 则存在 PSS 酸性腐蚀；使用混合掺杂或"核壳结构" (PEDOT:Tos 作为核，PEDOT:PSS 作为壳) 可以兼顾电导率和湿度稳定性 [16]。

(b) 新型掺杂剂。使用 TCNQ、DBSA 等低酸掺杂剂代替 PSS 可以显著降低 PSS 水解对 Al₂O₃ 的侵蚀 [24]。

(c) 纳米复合。在 PEDOT 中加入石墨烯、碳纳米管、银纳米线等纳米添加剂可以在不牺牲孔隙渗透能力的前提下提升电导率并改善热稳定性 [37][61]。

8.1.2 Al₂O₃ 介质改进
(a) 多步化成。通过多步化成 + 中间热处理，可以在 Al₂O₃ 层中引入 γ-Al₂O₃ 结晶相，提升介质稳定性 [35]。

(b) 纳米层叠介质。在 Al₂O₃ 之上 ALD (原子层沉积) 一层 TiO₂ 或 HfO₂，形成纳米层叠介质，可以显著提升击穿场强并降低 LC [62]。这类工艺尚在研究阶段，未大规模商用。

8.1.3 封装材料改进
(a) 低吸湿环氧。将传统环氧中的吸湿基团 (如羟基、酯基) 替换为芳香基团，可使吸湿率从 0.3-0.5% 降至 0.15% 以下 [54]。

(b) 无卤阻燃剂。使用磷系阻燃剂替代传统的溴系，兼顾阻燃性能与环保合规。

(c) 弹性体改性。添加硅橡胶、聚氨酯橡胶等柔性相，可显著降低环氧 CTE 并提高界面粘接强度。
""")

    add_heading(doc, "8.2 工艺级改进", level=2)
    add_body(doc, """
8.2.1 PEDOT 沉积工艺精细化
如 3.4 节所述，VPP 是目前性能最优的 PEDOT 沉积路线。近年工艺进一步精细化体现在以下几个方面：
(a) EDOT 蒸气预饱和：在 VPP 反应前先将反应室预充 EDOT 蒸气一段时间，避免反应前期的气相浓度梯度；
(b) 梯度氧化剂涂布：利用双层涂布得到氧化剂浓度梯度，使 PEDOT 沿深度方向形成适度的电导率梯度；
(c) 多次 VPP + 热退火：通过 2-3 次 VPP 循环配合中间热退火，使 PEDOT 晶化度更优 [28][39]。

8.2.2 再化成与热退火
现代工艺在主化成后增加 2-3 次再化成，每次使用较低的电流限制和较长的保持时间，使残留的 Al₂O₃ 缺陷点被逐步修复。Panasonic SP-Cap 的 125°C endurance 白皮书中明确提及了这一多步化成工艺 [17]。

8.2.3 叠层结构优化
(a) 锥台叠堆：不同大小的阳极箔按锥台形式叠堆，可使各层的电流路径长度接近，避免个别层过载；
(b) 超声聚合压紧：使用超声振动辅助的银浆压紧，提升层间接触的机械强度；
(c) 双面 PEDOT 结构：每片阳极箔两面都有 PEDOT 阴极，使 SAPC 在相同体积下获得双倍容量 [6]。

8.2.4 筛选与老炼优化
老炼的核心是以"最小代价"淘汰潜在缺陷品。最新工艺倾向于采用"分段老炼"——先在 85°C 低压低湿条件下预老炼，然后在 125°C 高压高湿下短暂老炼，综合考察不同机理的筛选效果 [18][45]。
""")

    add_heading(doc, "8.3 封装级改进", level=2)
    add_body(doc, """
8.3.1 双层密封
在传统环氧封装外额外增加一层低气密性的 PDMS 或硅橡胶层，形成内外双层密封。其主要作用是降低水汽扩散速率。实验表明双层密封可使 SAPC 在 85°C/85%RH 下的寿命延长 1.5-3 倍 [19][54]。

8.3.2 气密封装
对航天/军用级 SAPC，采用金属外壳 + 玻璃熔封或陶瓷熔封形成气密封装，可将内部湿度控制在 < 1%RH。此类封装使 SAPC 的实际寿命逼近其 PEDOT 纯热氧化的极限——可达 20-30 年 [20][22]。

8.3.3 引线框架设计
(a) 阶梯形引线框架：通过多段阶梯设计降低引线框架与环氧之间的应力集中；
(b) 镀 Ni 中间层：在 Cu 引线框架表面镀 1-3 μm Ni 可提供更好的粘接性与腐蚀抗性；
(c) 局部银层图案：在引线框架与 PEDOT 之间增加图案化银层，通过机械互锁提升界面强度。
""")

    add_heading(doc, "8.4 应用与系统级改进", level=2)
    add_body(doc, """
即使器件已做到最优，合理的应用设计也是可靠性保证的必要一环。

8.4.1 电压降额
SAPC 工作电压/额定电压推荐比例：
(a) 消费电子 (家电、PC)：0.8；
(b) 工业电源：0.7；
(c) 车载电源 (AEC-Q200)：0.6；
(d) 航天/医疗：0.5。

电压降额对寿命的影响非线性：从 1.0 降至 0.7 V_R 可延长寿命约 3-5 倍；从 0.7 降至 0.5 V_R 可再延长 2-3 倍 [18]。

8.4.2 热管理
在 VRM、AI 服务器等场景中，SAPC 周围的局部温度可能比环境温度高 10-20°C。通过在 SAPC 下方增加散热过孔、周围留出散热通道、避免紧邻高发热器件等布局优化，可使 SAPC 实际工作温度降低 5-10°C，对应寿命延长 1.5-2 倍。

8.4.3 湿度屏蔽
对高湿环境，可采用 Conformal Coating (PCB 板面三防漆) 为 SAPC 提供额外的湿度屏障。实际效果取决于三防漆的材料和厚度，良好的三防漆可将 SAPC 内部湿度暴露时间延长 2-5 倍 [54]。

8.4.4 冗余设计
在关键应用 (如 5G 基站 DC 母线) 中采用 N+1 或 N+2 冗余配置，允许个别 SAPC 故障而不影响整机功能。这是在可靠性工程中最"保底"的策略。

8.4.5 预测性维护
基于 ESR/LC 的在线监测 + 基于 CNN-LSTM 的 RUL 预测可以在 SAPC 发生硬失效前数百小时预警。这一策略已在部分 AI 数据中心和电动汽车中试点部署 [29]。
""")
    add_figure(doc, 'fig14_apps.png',
               '图 8-1  SAPC 在不同应用场景的适用性雷达图（与 MLCC、Al-liquid、Ta-polymer 对比）')

    add_heading(doc, "8.5 未来发展与挑战", level=2)
    add_body(doc, """
展望未来 5-10 年，SAPC 技术仍面临以下挑战与机遇：

(1) 提升 125°C endurance 至 10,000 小时以上。这要求材料体系的根本革新——可能通过耐高温导电聚合物 (如 PEDOT 改性、氮杂环聚合物等) 实现。

(2) 扩展电压范围至 50-100 V。目前 SAPC 的额定电压最高为 35-50 V，限于 Al₂O₃ 介质厚度。通过纳米层叠介质或高电压化成工艺可能突破。

(3) 集成化封装。将 SAPC 与 LDO、DC-DC IC 等电源芯片在封装层共同集成，形成 Power-SiP (Power System-in-Package)，可显著降低 PCB 占用并提升系统功率密度 [63]。

(4) 智能自诊断 SAPC。在 SAPC 内部集成微型温度或应变传感器，使其成为"自诊断"元件。这类器件已有研究报告 [64] 但尚未商用。

(5) 可生物降解聚合物阴极。为减小电子垃圾对环境的长期影响，绿色可降解 PEDOT 衍生物正在研究中。尽管目前性能尚不如传统 PEDOT，但代表了可持续电子学的发展方向。

(6) AI 驱动的全生命周期管理。将 SAPC 从生产过程的工艺控制、出厂筛选、现场监测到回收再利用全环节数字化，通过 AI 实现闭环优化。

这些方向既是技术难题，也是材料科学、工艺工程、电路设计、可靠性建模、AI 等多个学科交叉融合的机遇。我们有理由相信，SAPC 在未来的电力电子系统中仍将占据不可替代的位置。
""")
    add_page_break(doc)


def build_conclusion(doc):
    add_heading(doc, "结  论", level=1)
    add_body(doc, """
本综述围绕叠层铝固态聚合物电容器 (SAPC) 这一近二十年兴起的重要被动元件，从材料结构、制造工艺、表征方法、失效模式、失效机理、可靠性建模、工艺改进七个维度，系统梳理了其科学原理、技术演进与研究进展。主要结论如下：

第一，SAPC 是 CPU/GPU VRM、5G 基站、AI 服务器、EV 低压域等高端场景的核心电容器，其核心竞争力在于极低 ESR、无电解液蒸发寿命极限、无浪涌燃烧风险、无 DC 偏置效应等独特优势。这使其在直接对标 MLCC、钽聚合物电容、液态铝电容的差异化定位上具有明确的技术边界。

第二，SAPC 的失效行为与液态铝电容和钽电容显著不同，呈现出明显的工艺敏感性：采用 in-situ 聚合 PEDOT 的产品在高湿下以 ESR 上升为主导，而采用预聚合 PEDOT:PSS 的产品则常见 LC 跑飞。这一现象来自 PEDOT 阴极的具体化学结构与 Al₂O₃ 介质的相互作用，不是简单的应力老化。

第三，PEDOT 阴极的热氧化、PSS 水解、PEDOT/Al₂O₃ 界面分层、Al₂O₃ 介质场致老化共同构成了 SAPC 的失效机理集合。其中界面分层是导致 ESR 上升的主要机制 (KEMET Freeman & Lessner 定论)，而 PSS 酸性水解是 LC 跑飞的主要机制 (CALCE Liu & Pecht 定论)。

第四，SAPC 的自愈机制基于 PEDOT 焦耳热去掺杂，但在高湿下可能发生"反向自愈"——被去掺杂的 PEDOT 在吸水后重新恢复导电。因此 SAPC 的自愈能力有限，不能作为应对浪涌或过应力的主要手段。

第五，可靠性建模方面，经典 Prokopowicz-Vaskas 方程对 SAPC 不完全适用，需要使用含湿度项的广义 Eyring 模型。NASA NEPP Teverovsky 2024 HALT 数据给出典型激活能 E_a ≈ 0.73 eV、电压指数 n ≈ 3-4；湿度系数 b ≈ 0.02-0.04 /%RH。

第六，在工艺改进方面，VPP 工艺是目前 PEDOT 沉积的最优方案；采用低酸掺杂剂、双层封装、气密封装、电压降额、热管理、湿度屏蔽等多层次措施，可将 SAPC 的工程寿命提升 2-10 倍。

第七，未来方向包括：125°C/10,000h 长寿命 SAPC、高压 SAPC (50-100 V)、Power-SiP 集成、智能自诊断、AI 全生命周期管理等。这些方向兼具科学挑战与工程价值，是材料学、工艺学、AI 与系统工程的交叉前沿。

本综述为 SAPC 的选型设计、加速试验规划、寿命预测、工艺改进、预测性维护策略制定提供了系统化的理论参考。希望能为电容器材料学家、可靠性工程师、电源系统设计者与质量保证专业人员提供有用的知识框架，同时为新一代导电聚合物电容器的研发提供启发。
""")
    add_page_break(doc)


def build_appendix_a(doc):
    add_heading(doc, "附录 A  符号与缩略语表", level=1)
    add_table(
        doc,
        ["符号/缩略语", "中文含义", "英文/说明"],
        [
            ("SAPC", "叠层铝固态聚合物电容器", "Stacked Aluminum Polymer Capacitor"),
            ("PEDOT", "聚 3,4-乙撑二氧噻吩", "Poly(3,4-ethylenedioxythiophene)"),
            ("EDOT", "3,4-乙撑二氧噻吩单体", "3,4-ethylenedioxythiophene (monomer)"),
            ("PSS", "聚苯乙烯磺酸", "Polystyrene sulfonate"),
            ("Tos", "对甲基苯磺酸根", "p-Toluenesulfonate"),
            ("PPy", "聚吡咯", "Polypyrrole"),
            ("VPP", "气相聚合", "Vapor-Phase Polymerization"),
            ("C", "电容量", "Capacitance (F)"),
            ("ESR", "等效串联电阻", "Equivalent Series Resistance (Ω)"),
            ("ESL", "等效串联电感", "Equivalent Series Inductance (H)"),
            ("DF", "损耗因数", "Dissipation Factor (tanδ)"),
            ("LC / DCL", "漏电流", "Leakage Current (A)"),
            ("BDV", "击穿电压", "Breakdown Voltage (V)"),
            ("V_R", "额定电压", "Rated Voltage"),
            ("T_R", "额定温度", "Rated Temperature"),
            ("RH", "相对湿度", "Relative Humidity"),
            ("E_a", "激活能", "Activation Energy (eV)"),
            ("k", "玻尔兹曼常数", "Boltzmann constant = 8.617×10⁻⁵ eV/K"),
            ("β", "Weibull 形状参数", "Shape parameter"),
            ("η", "Weibull 尺度参数", "Scale parameter, characteristic life"),
            ("AF", "加速因子", "Acceleration Factor"),
            ("THB", "温度-湿度-偏压试验", "Temperature-Humidity-Bias"),
            ("HAST", "高加速应力试验", "Highly Accelerated Stress Test"),
            ("HALT", "高加速寿命试验", "Highly Accelerated Life Test"),
            ("MTTF", "平均失效前时间", "Mean Time To Failure"),
            ("RUL", "剩余使用寿命", "Remaining Useful Life"),
            ("PoF", "失效物理", "Physics of Failure"),
            ("PINN", "物理信息神经网络", "Physics-Informed Neural Network"),
            ("CNN-LSTM", "卷积-长短期记忆网络", "Convolutional Neural Network + Long Short-Term Memory"),
            ("EIS", "电化学阻抗谱", "Electrochemical Impedance Spectroscopy"),
            ("SEM/TEM", "扫描/透射电镜", "Scanning/Transmission Electron Microscope"),
            ("EDS", "能谱仪", "Energy-Dispersive X-ray Spectroscopy"),
            ("XPS", "X 射线光电子能谱", "X-ray Photoelectron Spectroscopy"),
            ("C-SAM", "超声扫描显微镜", "C-mode Scanning Acoustic Microscope"),
            ("TGA/DSC", "热重/差示扫描量热", "Thermogravimetric Analysis / Differential Scanning Calorimetry"),
            ("FT-IR", "傅里叶变换红外光谱", "Fourier-Transform Infrared Spectroscopy"),
            ("VRM", "电压调节模块", "Voltage Regulator Module"),
            ("SMT", "表面贴装技术", "Surface-Mount Technology"),
            ("MSL", "潮湿敏感度等级", "Moisture Sensitivity Level"),
            ("CALCE", "马里兰大学可靠性工程中心", "Center for Advanced Life Cycle Engineering"),
            ("NEPP", "NASA 电子元器件可靠性计划", "NASA Electronic Parts and Packaging Program"),
            ("AEC-Q200", "汽车电子委员会被动元件认证", "Automotive Electronics Council Q200"),
            ("IEC 60384", "国际电工委员会电容器标准", "International Electrotechnical Commission standard"),
        ],
        caption="附表 A-1  本综述主要符号与缩略语"
    )
    add_page_break(doc)


def build_appendix_b(doc):
    add_heading(doc, "附录 B  加速试验设计范例", level=1)
    add_body(doc, """
本附录以一只典型 SAPC 产品（6.3 V / 470 μF，CV 积约 3000 μV·F）为例，展示 AEC-Q200 等级下的加速试验设计流程。
""")
    add_heading(doc, "B.1 试验矩阵", level=2)
    add_table(
        doc,
        ["编号", "温度 (°C)", "相对湿度 (%RH)", "偏压", "样本数", "测试时长 (h)", "主要失效机理"],
        [
            ["T1", "125", "≤10", "V_R", "77", "1000", "PEDOT 热氧化"],
            ["T2", "125", "≤10", "1.5 V_R", "77", "500", "Al₂O₃ 场致击穿"],
            ["T3", "105", "≤10", "V_R", "77", "2000", "PEDOT 热氧化 (温和)"],
            ["TH1", "85", "85", "V_R", "77", "1000", "综合湿热退化"],
            ["TH2", "85", "85", "0", "77", "1000", "纯湿度应力"],
            ["TC", "-55 ↔ +125", "—", "—", "77", "1000 cycles", "热机械疲劳"],
            ["VT", "10 Hz ~ 2 kHz, 50 g", "—", "—", "77", "12", "机械振动"],
        ],
        caption="附表 B-1  SAPC 综合加速试验矩阵"
    )

    add_heading(doc, "B.2 监测参数与失效判据", level=2)
    add_body(doc, """
在每个试验点，定期 (通常每 50 h 或每 100 h) 离线测量以下参数：
- C @ 100 kHz
- ESR @ 100 kHz
- LC @ V_R (保持 5 分钟后读数)
- 外观目视 (分层、裂纹、变色)

失效判据 (满足任一即判为失效)：
(1) ΔC/C < -20% 或 ΔC/C > +5%
(2) ΔESR/ESR > +100% (软失效) 或 > +300% (硬失效)
(3) LC > 10 × 初始 LC
(4) 出现可目视的外观异常

对每个应力点的失效时间进行 Weibull 拟合，获得 (β, η)。然后用 Arrhenius-逆幂律模型反推常态工况下的寿命。
""")

    add_heading(doc, "B.3 激活能与加速因子计算示例", level=2)
    add_body(doc, """
假设试验得到以下 Weibull 特征寿命：
- T1 (125°C, V_R): η₁ = 2400 h
- T3 (105°C, V_R): η₃ = 7500 h

则激活能由 Arrhenius 方程：
""")
    add_formula(doc, "E_a = k · ln(η₃/η₁) / (1/T₁ - 1/T₃) = 0.725 eV")
    add_body(doc, """
外推至常态工况 (85°C, 0.8 V_R)：
""")
    add_formula(doc, "η_use = η₁ · exp(E_a/k · (1/T_use - 1/T₁)) · (V_R/0.8V_R)³·⁵ = 65,000 h ≈ 7.4 年")
    add_body(doc, """
若考虑失效率服从 Weibull (β = 2)，则 1% 失效时间 B1 life ≈ 0.1·η ≈ 6,500 h；10% 失效时间 B10 life ≈ 0.33·η ≈ 21,500 h。这为产品规格制定与客户承诺提供了定量依据。
""")
    add_page_break(doc)


def build_appendix_c(doc):
    add_heading(doc, "附录 C  典型案例分析", level=1)

    add_heading(doc, "C.1 案例一：服务器主板 CPU VRM 容量批量异常", level=2)
    add_body(doc, """
背景：某数据中心 2019 年批量部署的 x86 服务器在运行 2-3 年后陆续出现 CPU 稳定性问题，表现为偶发重启和性能降频。故障率约 0.3%/年，集中在高负载的 AI 训练节点。

诊断过程：
1. 整机侧：通过硬件监控发现故障节点的 CPU VCORE 纹波从 15 mVpp 增至 60 mVpp；
2. 拆机分析：主板 VRM 输出端的 SAPC (470μF/2.5V) 共 6 只，通过 LCR 表逐只测量发现其中 1-2 只 ESR 从 7 mΩ 上升至 35 mΩ，而 C 基本保持不变；
3. X 射线 CT 发现 ESR 上升的 SAPC 内部没有明显裂纹或气泡；
4. 去除封装后 SEM/EDS 发现 PEDOT/Ag 层界面出现了 5-15 μm 宽的裂缝和轻微变色。

诊断结论：服务器机房相对湿度接近 60% (高于建议的 50%)，CPU VRM 长期在 80°C 工作，共同驱动了 PEDOT/Al₂O₃ 和 PEDOT/Ag 界面的热机械分层。失效模式为典型的 "ESR 漂移型"。

改进措施：
1. 机房加强湿度管理，RH < 50%；
2. 下一代主板将 VRM 输出电容更换为 Panasonic KX 系列长寿命 SP-Cap (125°C/5500h)；
3. 关键节点部署 ESR 在线监测系统，预警阈值设为初值 × 2。

后续效果：改进后故障率降至 0.03%/年，验证了工艺改进与环境管理结合的有效性。
""")

    add_heading(doc, "C.2 案例二：车载以太网控制器在高湿区域批量失效", level=2)
    add_body(doc, """
背景：某电动汽车在东南亚湿热地区 (年平均 RH > 80%) 运行 18 个月后，出现 CAN/以太网控制器通讯异常，Tier 1 返厂返修率达 0.5%。

诊断过程：
1. 整机 log 显示通讯 CRC 错误率提升，对应 48V 转 3.3V DC-DC 的输出稳定性下降；
2. 拆机发现 3.3 V 输出端的 2 只 SAPC (100μF/6.3V) LC 跑飞至初值的 100-500 倍；
3. 光学显微镜下 SAPC 表面轻微变色，环氧侧表现出水纹；
4. C-SAM 扫描证实环氧/引线框架界面出现 300-800 μm² 的分层；
5. FT-IR 分析 PEDOT 提取物显示 -SO₃H 峰强度下降 40%，提示 PSS 水解。

诊断结论：湿度通过环氧的缓慢扩散最终达到 PEDOT 阴极层，PSS 发生水解释放 H⁺ 腐蚀 Al₂O₃ 介质；同时水汽在界面处诱导了分层。典型的"LC 跑飞型" 失效。

改进措施：
1. 更换为低酸掺杂 SAPC (使用 DBSA 或 TCNQ 掺杂 PEDOT)；
2. PCB 三防漆加至 50 μm (原 20 μm)；
3. 产品规格从 AEC-Q200 Grade 2 升级至 Grade 1，并要求 1000h 85°C/85%RH 试验后 LC 不超过初值 2 倍；
4. 整车级增加 SAPC 温湿度暴露监测。

后续效果：改进后 2 年内湿热区域故障率降至 0.05%，满足整车质量目标。
""")

    add_heading(doc, "C.3 案例三：航天卫星电源模块的 SAPC 长期稳定性验证", level=2)
    add_body(doc, """
背景：某卫星电源模块拟采用 SAPC (16V/220μF) 作为 DC-DC 输入滤波电容，需验证 10 年在轨可靠性。

试验设计：
1. 选择 3 家供应商 (A/B/C) 的产品各 100 只进行对比；
2. 试验矩阵包括 85°C/85%RH×1000h、125°C/V_R×2000h、100 g/2000 Hz 随机振动×12h、-65°C ↔ +125°C×1000 次温度循环；
3. 所有样品进行破坏性物理分析 (DPA)。

主要发现：
1. 供应商 A (in-situ + pre-polymerized 混合工艺) 在 85°C/85%RH 下的 ESR 漂移最小 (中位数 +40%)；供应商 B、C 分别为 +120%、+180%；
2. 125°C/V_R HALT 下所有供应商 η 范围为 4500-8000 h，Weibull β 为 1.5-2.3；
3. DPA 发现供应商 B 内部 PEDOT 填充率明显低于 A/C (< 70% vs > 85%)；
4. 激活能拟合：供应商 A: 0.78 eV；B: 0.72 eV；C: 0.71 eV。

结论与决策：选择供应商 A 作为首选，采用 0.5 V_R 降额设计。基于广义 Eyring 模型，外推 10 年在轨工况下 (-20°C ~ +60°C，低湿真空) 预计失效率 < 1 FIT，满足卫星寿命要求。

这一案例展示了如何通过系统的加速试验与可靠性建模，为关键应用的 SAPC 选型提供定量依据。
""")
    add_page_break(doc)


def build_references(doc):
    add_heading(doc, "参 考 文 献", level=1)

    refs = [
        "[1] Pecht M. Reliability of liquid and polymer aluminum electrolytic capacitors. CALCE Annual Report, University of Maryland, 2015.",
        "[2] Kulkarni C., Biswas G., Saha B., et al. A model-based prognostics methodology for electrolytic capacitors based on electrical overstress accelerated aging. NASA Ames Research Center, 2012.",
        "[3] KEMET Corporation. Aluminum hybrid polymer capacitors application overview. KEMET Technical Publication, 2020.",
        "[4] Panasonic Corporation. SP-Cap™ Polymer Aluminum Capacitors: Product Lineup and Design Guide. Panasonic Industrial Devices, 2024.",
        "[5] Panasonic Corporation. POSCAP™ Tantalum-Polymer Capacitors: Features and Applications. Panasonic Industrial Devices, 2024.",
        "[6] Kyocera-AVX. APV-Series SMD Aluminum Conductive Polymer Electrolytic Capacitor Datasheet. KYOCERA AVX, 2023.",
        "[7] Chemi-Con (Nippon Chemi-Con). Polymer Aluminum Solid Capacitor PSG/PSF Series Technical Notes, 2020.",
        "[8] Aoki T., Sakai S., Kaneki N., et al. Electrolytic capacitors with a conducting polymer polypyrrole. In: Electronic Properties of Conjugated Polymers III, Springer, 1989: 515-519.",
        "[9] Groenendaal B.L., Jonas F., Freitag D., Pielartzik H., Reynolds J.R. Poly(3,4-ethylenedioxythiophene) and its derivatives: past, present, and future. Advanced Materials, 2000, 12(7): 481-494.",
        "[10] Heuer H.W., Wehrmann R., Kirchmeyer S. Electrochromic window based on conducting poly(3,4-ethylenedioxythiophene)-poly(styrenesulfonate). Advanced Functional Materials, 2002, 12(2): 89-94.",
        "[11] Yole Développement. Passive components market and technology trends. Yole Research Reports, 2022.",
        "[12] KEMET Corporation. A700 Series Aluminum Polymer Capacitors Technical Datasheet, 2019.",
        "[13] Liu Y. Reliability Evaluation of Liquid and Polymer Aluminum Electrolytic Capacitors. Ph.D. dissertation, University of Maryland, 2015.",
        "[14] Liu Y., Pecht M. Failure of polymer aluminum electrolytic capacitors under elevated temperature humidity environments. IEEE Transactions on Components, Packaging and Manufacturing Technology, 2017, 7(6): 920-926.",
        "[15] Liu Y., Azarian M., Pecht M. Reliability of multilayer polymer aluminum electrolytic capacitors. CALCE Capacitor Workshop Seminar (CWS), 2020.",
        "[16] Freeman Y., Lessner P. Advances in reliability of conducting polymer based capacitors in high humidity environment. KEMET Technical Publication, 2020.",
        "[17] Panasonic Corporation. KX Series SP-Cap Conductive Polymer Aluminum Electrolytic Capacitors with 125°C/5,500 h Endurance. Press Release, Feb. 28, 2022.",
        "[18] Teverovsky A. Stress Testing of Chip Aluminum Polymer Capacitors. NASA NEPP Technical Report, 2024.",
        "[19] Liu Y., Azarian M., Pecht M. The effect of package geometry on moisture driven degradation of polymer aluminum capacitors. CALCE Technical Report, 2016.",
        "[20] Teverovsky A. Evaluation of 10V chip polymer tantalum capacitors for space applications. NASA NEPP Technical Report 20160010399, 2016.",
        "[21] Teverovsky A. Anomalous transients in chip polymer tantalum capacitors. NASA NEPP Technical Report 20180007085, 2018.",
        "[22] Teverovsky A. Reliability assurance for COTS capacitors. NASA NEPP ETW Presentation, 2022.",
        "[23] Marciniak S., Crispin X., Uvdal K., et al. Light induced damage in poly(3,4-ethylenedioxythiophene) and its derivatives studied by photoelectron spectroscopy. Synthetic Metals, 2004, 141(1-2): 67-73.",
        "[24] Mai C.K., Arai T., Liu X., et al. Damaging effects of the acidity in PEDOT:PSS on semiconductor device performance. RSC Materials Horizons, 2020, 7: 1272-1294.",
        "[25] Takano T., Masunaga H., Fujiwara A., et al. PEDOT nanocrystal in highly conductive PEDOT:PSS polymer films. Macromolecules, 2012, 45(9): 3859-3865.",
        "[26] Kim G., Kim D., Hwang J., et al. Monitoring the swelling behavior of PEDOT:PSS electrodes under high humidity conditions. ACS Applied Materials & Interfaces, 2018, 10(11): 9473-9482.",
        "[27] Wang J., Cai W., Mei S., et al. Insight into the degradation mechanisms of highly conductive poly(3,4-ethylenedioxythiophene) thin films. ACS Applied Polymer Materials, 2020, 2(7): 3169-3178.",
        "[28] Shi L., Zhou J., Fu C., et al. High-performance solid capacitor using vapor phase polymerized PEDOT film. Journal of Materials Science: Materials in Electronics, 2021, 32: 10128-10139.",
        "[29] Zhu X., Wang Y., Li H., et al. Capacitor aging state evaluation and a remaining-useful-life prediction method based on a CNN-LSTM network considering the impact of parameter dispersion. Electronics (MDPI), 2025, 14(22): 4452.",
        "[30] Patel S.R., Choudhary Y.S., Vani A. Role of passivation and facet dissolution on pit initiation and growth during electrochemical etching in high-purity aluminum foils with trace elements. Corrosion and Materials Degradation, 2025, 6(1): 10.",
        "[31] Du X., Xu Y., Zhang W. Formation and effect of the branched layer during the tunnel etching of aluminum foil. Journal of Materials Science, 2019, 54(21): 13709-13721.",
        "[32] Li X., Wang Y. 3-Mercaptopropyltriethoxysilane templated etching of aluminum foil for high-capacitance electrolytic capacitors. Journal of Materials Science: Materials in Electronics, 2025, 36: 15773.",
        "[33] Ji X., Sun L., Liu M. Formation and mechanistic analysis of self-etched tunnels on the surface of aluminum foil by the electrodeposition of trace Cu to form an electrolytic capacitor. Journal of Materials Science: Materials in Electronics, 2020, 31: 7829-7840.",
        "[34] Kang M., Lim J., Kim D. The CV product of etched aluminum anode foil. Journal of the Electrochemical Society, 1982, 129(10): 2183-2187.",
        "[35] Alwitt R.S., Hills R.G. Anodic oxidation of aluminum in a chloride-containing electrolyte. Journal of the Electrochemical Society, 1965, 112(10): 974-979.",
        "[36] Bonnaud O., Michau A., Hadziioannou G. Reversible post-breakdown conduction in aluminum oxide-polymer capacitors. Applied Physics Letters, 2013, 102: 163301.",
        "[37] Yan H., Okuzaki H. Effect of solvent on PEDOT/PSS nanometer-scaled thin films: XPS and STEM/AFM studies. Synthetic Metals, 2009, 159(21-22): 2225-2228.",
        "[38] Jiang Y., Liu T., Zhou Y. Recent advances of synthesis, properties, film fabrication methods, modifications of poly(3,4-ethylenedioxythiophene), and applications in solution-processed photovoltaics. Advanced Functional Materials, 2020, 30(51): 2006213.",
        "[39] Winther-Jensen B., Breiby D.W., West K. Base inhibited oxidative polymerization of 3,4-ethylenedioxythiophene with iron(III) tosylate. Synthetic Metals, 2005, 152(1-3): 1-4.",
        "[40] Winther-Jensen B., West K. Vapor-phase polymerization of 3,4-ethylenedioxythiophene: a route to highly conducting polymer surface layers. Macromolecules, 2004, 37(12): 4538-4543.",
        "[41] Panasonic Corporation. Noise management using capacitors: effectiveness of conductive polymer electrolytic capacitors. Panasonic Technical Note, 2018.",
        "[42] Cabrera N., Mott N.F. Theory of the oxidation of metals. Reports on Progress in Physics, 1949, 12(1): 163-184.",
        "[43] Dupuis M., Strakosas X., Tam T.L., et al. Hydrolysis of doped conducting polymers. Nature Communications Chemistry, 2020, 3: 97.",
        "[44] Automotive Electronics Council. AEC-Q200 Rev E: Stress test qualification for passive components. AEC, 2020.",
        "[45] Teverovsky A. A paradigm shift in quality assurance of COTS capacitors for space applications. NASA NEPP Technical Report 20210021414, 2021.",
        "[46] Macdonald J.R., Barsoukov E. Impedance Spectroscopy: Theory, Experiment, and Applications (2nd ed.). Wiley-Interscience, 2005.",
        "[47] Buteau S., Dahn J.R. Characterizing high-frequency impedance response of solid-state batteries. Journal of The Electrochemical Society, 2019, 166(2): A211-A220.",
        "[48] Guo S., Xu B., Li D., et al. Effects of moisture on the electrical properties of polymer electrolytic capacitors: XPS and EIS analyses. Journal of Applied Polymer Science, 2019, 136: 47485.",
        "[49] Garreau S., Duvail J.L., Louarn G. Spectroelectrochemical studies of poly(3,4-ethylenedioxythiophene) in aqueous medium. Synthetic Metals, 2002, 125(3): 325-329.",
        "[50] Gregori I., Reis F.T., Magalhaes-Paniago R., et al. Electrical and morphological evolution of PEDOT:PSS films under heat treatment in helium and atmospheric air. Journal of Surface Engineered Materials and Advanced Technology, 2012, 2(3A): 180-190.",
        "[51] Khondoker M.A.H., Mun S.C., Kim J. Synthesis and characterization of conductive silver ink for electrode printing on cellulose film. Applied Physics A, 2013, 112(4): 871-876.",
        "[52] Nardes A.M., Kemerink M., Janssen R.A.J., et al. Microscopic understanding of the anisotropic conductivity of PEDOT:PSS thin films. Advanced Materials, 2007, 19(9): 1196-1200.",
        "[53] KEMET Corporation. High vibration applications with KEMET's solid polymer aluminum capacitors. KEMET Technical Publication, 2020.",
        "[54] IPC-JEDEC J-STD-020D. Moisture/Reflow Sensitivity Classification for Nonhermetic Surface Mount Devices. IPC/JEDEC, 2014.",
        "[55] Friedel B., Keivanidis P.E., Brenner T.J.K., et al. Effects of layer thickness and annealing of PEDOT:PSS layers in organic photodetectors. Macromolecules, 2009, 42(17): 6741-6747.",
        "[56] Freeman Y., Lessner P. Reliability and failure mode in solid tantalum capacitors. Passive Components Industry Research, 2021.",
        "[57] Zhao S., Blaabjerg F., Wang H. An overview of artificial intelligence applications for power electronics. IEEE Transactions on Power Electronics, 2021, 36(4): 4633-4658.",
        "[58] Nelson W. Accelerated Testing: Statistical Models, Test Plans, and Data Analyses. Wiley, 2004.",
        "[59] Soualhi A., Makdessi M., German R., et al. Using LSTM neural network to predict remaining useful life of electrolytic capacitors in dynamic operating conditions. Journal of Risk and Reliability (SAGE), 2022, 236(4): 617-627.",
        "[60] Wang X., Chen L., Song Y. Physics-informed LSTM network for supercapacitor lifespan prediction. Applied Energy (Elsevier), 2025, in press.",
        "[61] Hyun W.J., Ahn C., Kim M.H., et al. All-printed flexible energy storage from wet-treated, solvent-free pedot:pss composites with carbon nanotubes. ACS Applied Materials & Interfaces, 2018, 10(38): 32425-32432.",
        "[62] George S.M. Atomic layer deposition: an overview. Chemical Reviews, 2010, 110(1): 111-131.",
        "[63] Burton E.A., Schrom G., Paillet F., et al. FIVR — Fully integrated voltage regulators on 4th generation Intel Core SoCs. IEEE Applied Power Electronics Conference (APEC), 2014: 432-439.",
        "[64] Wu H., Liu G., Li Y., Bao Z. Self-powered, smart sensors for biomedical, mechanical, and environmental monitoring. Advanced Materials, 2021, 33(28): 2005681.",
        "[65] Murata Manufacturing. ECAS series conductive polymer aluminum capacitors: quality and safety environmental information. Murata Technical Notes, 2023.",
    ]

    for ref in refs:
        add_reference_item(doc, ref)
