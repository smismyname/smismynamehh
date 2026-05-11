# -*- coding: utf-8 -*-
"""失效模式 + 失效机理 章节"""
from docx_utils import (add_heading, add_body, add_page_break, add_figure,
                         add_formula, add_table, add_quote, set_cn_font)


def build_chapter5(doc):
    add_heading(doc, "第五章 SAPC 典型失效模式", level=1)

    add_heading(doc, "5.1 失效模式分类框架", level=2)
    add_body(doc, """
依据 IEC 61709、MIL-HDBK-217 与 IPC 联合发布的 A-610 等主流标准，电容器失效可按照外在表现分为开路、短路、参数漂移、外观与密封失效四大类。对于 SAPC，由于其固态聚合物阴极与引线框架封装结构，失效模式呈现以下鲜明特征：
(1) 参数漂移型失效 (尤其是 ESR 上升和 LC 跑飞) 占主导地位，约 75-85% 的耗损失效均可归入此类；
(2) 开路型失效相对罕见，通常由端电极焊点老化或叠层分离引起；
(3) 短路型失效主要由 Al₂O₃ 介质缺陷点的热失控引起，表现为个别点的局部击穿；
(4) 外观与密封失效以环氧分层为主，不像液态铝电容那样出现漏液或鼓包。

SAPC 的失效后果一般相对温和——不会发生液态铝电容的爆炸事件，也不会发生钽电容的着火事件。然而 SAPC 失效仍可能造成整机功能异常：ESR 上升会直接恶化 VRM 的纹波和瞬态响应；LC 跑飞会加重整机待机功耗；在严重短路情况下，局部焦耳热可能将周围 PCB 焊盘烧黄。

按 Teverovsky (NASA NEPP, 2024) 的归类 [18]，SAPC 的失效模式可以按"参数漂移幅度"分为三个梯度：
- "软失效" (soft failure)：ΔESR 或 ΔC 超出规格值但未到严重影响整机功能的程度 (通常 ΔESR < 200%)；
- "硬失效" (hard failure)：ΔESR > 300% 或 ΔC > 20% 导致整机明显异常；
- "灾难性失效" (catastrophic failure)：内部短路/开路，整机无法工作。

在 85°C/85%RH/V_R 偏压条件下的 CALCE 加速老化中，大部分 SAPC 在进入硬失效阶段前均已表现出可识别的软失效征兆，这为在线监测提供了可能性 [14]。
""")

    add_heading(doc, "5.2 参数漂移模式 (ESR / C / DF)", level=2)
    add_body(doc, """
SAPC 参数漂移模式中，ESR 上升是最主要的表现形式。根据 CALCE 实验室 Liu 等 (2017) [14] 对 Nichicon 与 Nippon Chemi-Con (现 Chemi-Con) 两家制造商 SAPC 的系统对比：

(1) Nichicon 样品在 85°C/85%RH 下 2000 小时内 ESR 从初始的约 12 mΩ 上升到 30~50 mΩ，容量保持稳定，LC 仅有小幅增加——这被称为"ESR 上升模式" (ESR-rise mode)；
(2) Chemi-Con 样品在相同条件下 ESR 上升相对缓慢 (1.5-2 倍)，但 LC 从初始 5 μA 跑飞至数百 μA——这被称为"LC 跑飞模式" (LC-runaway mode)。

这两种截然不同的失效模式并非偶然，而是与各厂商的 PEDOT 沉积工艺密切相关：
- in-situ 聚合的 PEDOT:Tos 在湿热环境下易发生电导率下降，表现为 ESR 上升；
- 预聚合 PEDOT:PSS 对 Al₂O₃ 介质的酸性侵蚀更显著，表现为 LC 增加。

这一发现对失效诊断具有重要指导意义：基于 ESR 的监测与基于 LC 的监测在不同制造商 SAPC 之间不具有通用性，必须针对具体产品选择合适的健康指标 [14][16]。
""")
    add_figure(doc, 'fig06_degradation.png',
               '图 5-1  SAPC 在 85°C/85%RH 加速老化下两种主导失效模式的 ESR 和 LC 演化曲线 (数据曲线基于 Liu & Pecht, IEEE T-CPMT, 2017 [14] 与 Teverovsky, NASA/NEPP, 2024 [18] 的报道重绘)')

    add_body(doc, """
参数漂移失效的"硬阈值"通常由以下两个条件之一触发：
(1) ESR 达到初始值的 2 倍；
(2) C 下降超过 20% 或 C < 额定容量的 80%。

一些特殊行业 (如航天、医疗植入) 还会设置更严格的 LC 上限，典型为初始 LC 的 5-10 倍。Teverovsky (2024) [18] 对 chip APC 的 HALT 数据显示，不同制造商在 125°C/1.5 V_R 下的 t₆₃ (Weibull 特征寿命) 差异可达 3-10 倍，反映了工艺控制对可靠性的一阶影响。

从时间尺度上看，SAPC 的参数漂移呈现典型的"肘型" (elbow) 趋势——前期 (0-50%) 参数变化缓慢，后期 (50-100%) 参数加速恶化。这一特征与 PEDOT 界面的"穿刺"(percolation) 行为一致：当 PEDOT 导电网络中电连通性被破坏至某一阈值后，电导率下降呈指数加速 [23][52]。
""")

    add_heading(doc, "5.3 漏电流跑飞与短路模式", level=2)
    add_body(doc, """
LC 跑飞 (leakage current runaway) 是 SAPC 中特有的失效机理之一。其典型特征是：在老化过程中 LC 先稳定在初值附近，在某一阈值 (通常对应临界水汽浓度或临界界面分层) 后 LC 陡然上升 2-4 个数量级，最终导致器件短路 [14]。

Liu 与 Pecht (2017) [14] 通过 FT-IR/XPS 表征发现，LC 跑飞前 SAPC 的 PEDOT 层中 Fe 元素含量明显升高——这提示 Fe³⁺ 从 Tos 盐中释放并穿过 Al₂O₃ 介质层形成新的漏电通道。进一步的 SEM 分析发现 Al₂O₃ 层在 LC 跑飞点出现了数十纳米尺度的局部溶解坑，确认了"Fe³⁺ 催化 + H₂O 协同 + Al₂O₃ 缺陷通道"的综合机理。

SAPC 的短路失效相对少见且通常是非致命的——即使发生内部击穿，由于 PEDOT 具有一定的"软熔丝"特性 (局部过热时会因焦耳热升高而去掺杂转变为高阻态)，短路电流会被快速限制在毫安量级 [16][53]。这也是为什么相较于钽电容的 MnO2 阴极体系，SAPC 的"安全性"显著更好——即使失效也不会发生着火。

然而在极端情况下 (如 VRM 输出端严重过压、ESD 瞬态、反向电压) SAPC 仍可能出现持续性短路：此时 Al₂O₃ 介质的大面积击穿使 PEDOT 与 Al 箔直接接触形成金属化焊接，难以再恢复高阻态。这类失效通常伴随有烧焦痕迹，属于灾难性失效 [18]。
""")

    add_heading(doc, "5.4 开路模式 (端电极与内部连接失效)", level=2)
    add_body(doc, """
SAPC 的开路失效主要源于三类原因：
(1) 端电极焊点老化：在温度循环或振动应力下，Sn 基焊点可能发生疲劳裂纹扩展。AEC-Q200 的 TC-1000 试验 (1000 次 -55°C ↔ +125°C 循环) 是标准评估手段 [44]；
(2) 内部银浆层老化：Ag 迁移或银浆基质树脂热老化可能导致内部接触电阻大幅升高直至开路；
(3) 引线框架断裂：在极端机械应力下 (如重力跌落、冲击) 引线框架可能出现局部断裂。

KEMET 的一项高振动环境测试 [53] 报告指出，在 20 g 随机振动下，SAPC 的失效率 (10,000 小时内) 较同参数液态铝电容低约 80%。这证实了 SAPC 优异的机械可靠性，使其成为车载、航空场景的合适选择。

开路失效的外观识别通常较为直接——X 射线透视可以清楚看到引线框架断裂或端电极处的气泡；SEM 可识别焊点裂纹。开路失效的一个重要特点是"缓变-突变"双阶段：早期 ESR 缓慢上升 (可能是几个月到几年)，突然增大至开路 (秒到小时级)。这与参数漂移模式的持续渐变有显著区别 [14][18]。
""")

    add_heading(doc, "5.5 外观与密封失效", level=2)
    add_body(doc, """
SAPC 的外观与密封失效主要表现为环氧封装的分层 (delamination)、裂纹 (crack)、表面变色和翘曲 (warpage)。与液态铝电容的鼓包/漏液相比，SAPC 的密封失效相对温和，但仍是可靠性评估的重要环节。

5.5.1 环氧分层
分层主要发生在环氧/引线框架界面与环氧/PEDOT 界面。常见诱因包括：
(1) CTE 失配：环氧 ≈ 15 ppm/°C，Cu 引线框架 ≈ 17 ppm/°C，PEDOT ≈ 30-50 ppm/°C；
(2) 回流焊温度冲击：260°C 瞬时冲击使各层之间出现剪切应力；
(3) 水汽诱导的"pop-corn"效应：吸湿后的器件在高温焊接时内部水蒸气膨胀引起突发性分层。

为此，IPC/JEDEC J-STD-020 对 SMT 元件规定了"潮湿敏感度等级 (MSL)"，SAPC 大部分产品为 MSL 3-4，要求短暂潮湿暴露后必须进行烘烤再回流焊。

5.5.2 表面变色
SAPC 表面在高温老化后可能出现黄褐色的变色，这通常是环氧封装中溴化阻燃剂的氧化产物或银浆层银的轻微氧化所致。变色本身对功能无影响，但往往作为"提示即将失效"的警示信号 [6]。

5.5.3 翘曲
SAPC 整体尺寸较大 (7.3×4.3 mm 或 12.0×10.0 mm) 时，在 260°C 回流焊下可能出现数十微米的翘曲。严重翘曲会引起焊点应力集中，影响长期焊接可靠性。封装材料的 Tg 和橡胶相态调控是关键 [54]。
""")

    add_heading(doc, "5.6 失效模式与应用工况的映射", level=2)
    add_body(doc, """
表 5-1 给出了 SAPC 失效模式在不同应用工况下的主导性比较。可以看到：
(1) 在 CPU/GPU VRM 这种高纹波低温工况下，ESR 漂移是主要失效；
(2) 在 5G 基站高温工况下，LC 跑飞风险显著；
(3) 在车载高湿高振动工况下，外观与密封失效权重增加；
(4) 在航天真空环境下，由于无湿度应力，整体寿命显著延长，此时 PEDOT 的纯热氧化成为寿命限制因素。

这一映射对产品选型和应用设计具有重要指导意义：针对不同工况应有针对性地选择不同制造商的不同型号。
""")
    add_table(
        doc,
        ["应用工况", "主导失效模式", "次要失效模式", "推荐 PEDOT 工艺"],
        [
            ["CPU/GPU VRM (室温高纹波)", "ESR 漂移", "外观变色", "in-situ / VPP 混合"],
            ["5G 基站 (85-105°C 室外)", "LC 跑飞, ESR 漂移", "分层", "VPP + 低酸封装"],
            ["EV 低压域 (车载)", "端电极焊点", "分层", "VPP + AEC-Q200 工艺"],
            ["AI 服务器 (高温稳态)", "ESR 漂移", "PEDOT 热氧化", "VPP"],
            ["航天 (真空低温)", "PEDOT 热氧化", "端电极", "VPP + 真空封装"],
            ["医疗 (低 LC 稳态)", "LC 漂移", "外观", "pre-polymerized"],
        ],
        caption="表 5-1  SAPC 失效模式在不同应用工况下的主导性比较"
    )
    add_page_break(doc)


def build_chapter6(doc):
    add_heading(doc, "第六章 SAPC 失效机理", level=1)

    add_body(doc, """
理解 SAPC 的失效机理需要从 PEDOT 阴极、Al₂O₃ 介质、封装界面三大系统出发，并结合温度、电压、湿度、机械应力等外部应力的作用机制。图 6-1 给出了 SAPC 失效机理的整体映射：以四大应力源 (温度/湿度/电场/机械) 为起点，经由四条主要机理通路 (PEDOT 热氧化、PSS 水解、介质击穿、界面分层) 最终汇聚于可观测的失效表现 (ESR↑/LC↑/C↓)。
""")
    add_figure(doc, 'fig11_mechanism_map.png',
               '图 6-1  SAPC 应力-机理-失效综合映射图 (基于 Liu & Pecht 2017 [14]、Freeman & Lessner KEMET 2020 [16]、Teverovsky 2024 [18] 文献综合构建)')

    add_heading(doc, "6.1 PEDOT 阴极的热氧化降解", level=2)
    add_body(doc, """
PEDOT 的热氧化降解是 SAPC 高温老化过程中最主要的机理之一。Marciniak 等 (2004) 发表于 Synthetic Metals 的工作 [23] 通过 TGA/FT-IR/XPS 联合表征，首次系统阐明了 PEDOT:PSS 热氧化的分子机理。其核心反应路径如下：

(1) PEDOT 的侧链 C-O-C 键在氧气存在下首先被氧化断裂：
""")
    add_formula(doc, "-CH₂-O-CH₂- + O₂ → 2-CHO + H₂O")
    add_body(doc, """
(2) 生成的醛基 (-CHO) 进一步被氧化为羧基 (-COOH)；
(3) 羧基的积累破坏了 PEDOT 主链上的 π 共轭，导致电导率显著下降；
(4) 极端情况下 PEDOT 主链完全断裂，转变为无定形碳。

这一降解过程遵循 Arrhenius 温度依赖，激活能 E_a 约为 0.75-0.95 eV [23][50][55]。这意味着温度从 85°C 升至 125°C，降解速率提升约 7-10 倍。
""")
    add_quote(doc,
              '"The conductivity decrease as a function of time is consistent with a granular metal type structure, '
              'in which aging is due to the shrinking of PEDOT conductive grains." —— Marciniak 等，'
              'Synthetic Metals (2004), [23]')

    add_body(doc, """
Scirp (2012) 的一项独立研究 [50] 在氦气与空气环境下对比热处理 PEDOT:PSS 薄膜，发现：氦气中 400°C 处理后电导率可保持 50% 以上，而空气中 200°C 处理后电导率即下降 >80%——证明氧气是主要的降解驱动因素。这一结论对 SAPC 的工艺改进具有直接指导意义：加强封装的氧气屏蔽能显著延长 SAPC 寿命。

此外 PEDOT 的热氧化有两个重要的非线性特征：
(i) 自催化性——反应生成的酸性副产物会进一步加速降解；
(ii) 位置选择性——PEDOT 薄膜的表面和边缘降解速率远高于内部。

后者解释了为什么 SAPC 的 ESR 上升常在器件边缘处最为显著——这也是 X 射线 CT 和 EDS 线扫描常用的"边缘优先老化"诊断线索 [16][19]。
""")

    add_heading(doc, "6.2 PSS 水解与酸性腐蚀", level=2)
    add_body(doc, """
对采用 PEDOT:PSS 的 SAPC (如部分 KEMET 产品)，PSS 的水解是另一条重要失效通路。PSS (polystyrene sulfonate) 中的磺酸基 (-SO₃H) 具有较强的酸性 (pH ≈ 1-2)，在潮气存在下会释放出磺酸根离子并引发如下连锁反应：

(1) PSS 水解：
""")
    add_formula(doc, "-C₆H₄-SO₃H + H₂O ⇌ -C₆H₄-SO₃⁻ + H₃O⁺")
    add_body(doc, """
(2) H₃O⁺ 攻击 Al₂O₃ 介质层：
""")
    add_formula(doc, "Al₂O₃ + 6H⁺ → 2Al³⁺ + 3H₂O")
    add_body(doc, """
(3) Al₂O₃ 的局部溶解形成新的漏电通道，导致 LC 快速上升。

Dupuis 等 (2020) 在 Nature Communications 发表的研究 [43] 通过原位 XPS 观察了掺杂导电聚合物 (包括 PEDOT:PSS) 在不同盐溶液中的水解行为，证实 PEDOT:PSS 在中性水溶液中就可发生缓慢水解，而在酸性环境中水解速率显著加速。这一机理解释了为何 SAPC 在高湿下 LC 跑飞比 ESR 漂移更为剧烈。

进一步的实验证据来自 Mai 等 (2019) 发表在 RSC Materials Horizons 上的文章 [24]，他们发现 PEDOT:PSS 中的 PSS 酸性是导致邻近 Al、Mg、Cu 等金属在高湿条件下腐蚀的主要原因。为此作者提出用低酸的 PSS 替代品 (如 TCNQ⁻ 或 DBSA⁻) 作为掺杂剂，以提升器件稳定性。

相应的工艺解决方案包括：(1) Heraeus 开发的 CLEVIOS PH 中性化产品；(2) 在 PEDOT:PSS 中添加 Zn²⁺ 或 Ca²⁺ 作为酸中和剂；(3) 减小 PEDOT:PSS 厚度、增大 in-situ 沉积比例 [9][16]。
""")

    add_heading(doc, "6.3 界面分层与热机械失效", level=2)
    add_body(doc, """
SAPC 的界面分层是引起 ESR 上升的另一核心机理。KEMET 的 Freeman 与 Lessner 在其白皮书 [16] 中明确指出：

"Our studies suggest that delamination caused by the thermomechanical and voltage induced stress generated in these capacitors is primarily responsible for conductivity degradation in polymer capacitors."

也就是说，界面分层——特别是 PEDOT/Al₂O₃ 界面与 PEDOT/Ag 界面——才是 PEDOT 电导率退化的首要原因，而不是 PEDOT 本身的化学降解。分层一旦形成，原本的欧姆接触点显著减少，电流被迫通过剩余的少量接触点，导致 ESR 迅速上升。

分层的驱动力主要来自两方面：
(1) 热机械应力：不同材料的 CTE 失配 (Al: 23 ppm/°C, Al₂O₃: 8 ppm/°C, PEDOT: ~50 ppm/°C, 环氧: ~15 ppm/°C)；
(2) 电化学应力：在电压偏置下，界面处的电荷累积引发的局部力。

CALCE 的 Liu 等 (2016) [19] 通过封装几何比较实验发现，将引线框架的宽高比从 1:1 调整到 1:3 后，分层起始时间可延长 30-50%。这说明通过封装几何优化，可以显著延长 SAPC 的寿命而无需改变材料体系。

自 2020 年以来，KEMET、Panasonic 等厂商已在工艺中引入"热机械应力缓冲层" (stress buffer layer)——在 PEDOT 与环氧之间沉积一层低 CTE 的柔性材料 (如硅树脂) 以缓解界面应力集中。Panasonic KX 系列的 125°C/5500h 长寿命指标就与此类工艺改进直接相关 [17]。
""")

    add_heading(doc, "6.4 Al₂O₃ 介质场致击穿与老化", level=2)
    add_body(doc, """
Al₂O₃ 阳极氧化膜是 SAPC 的电气绝缘核心。其在电场作用下的老化遵循 Schottky-Poole-Frenkel 发射机制，即载流子通过陷阱能级跳跃实现传导，漏电流满足：
""")
    add_formula(doc, "J_PF = C·E·exp(-q(φ - √(qE/πε))/kT)")
    add_body(doc, """
其中 φ 为陷阱深度，ε 为介电常数，E 为电场强度。Al₂O₃ 介质在 125°C 工作电场下的典型漏电流密度为 10⁻⁹ A/cm²；在 150°C 下可上升到 10⁻⁷ A/cm²。

在长期运行中 Al₂O₃ 的老化还受水汽驱动。Rivera-Torres 等 (2013) 在 AIP APL [36] 发表的工作发现，Al/Al₂O₃/polymer/metal 结构在低功率恒流应力下会发生"可逆击穿"——即击穿后在无电应力下静置一段时间可自愈恢复绝缘性。这一现象提示 SAPC 的 Al₂O₃ 层存在某种"自愈裕度"，但这种自愈在持续偏压下并不有效。

此外，当电场强度接近 Al₂O₃ 击穿场强 (7-10 MV/cm) 时，会触发 Frenkel-Poole 到 Fowler-Nordheim 隧穿机制的转变，漏电流对电压的敏感度急剧升高 (幂指数 n 从 2-3 跃变为 10 以上)。这也是为何 SAPC 在接近额定电压 (特别是 Vr > 16V 的高压型号) 工作时，寿命对电压非常敏感的物理原因 [18][36]。
""")
    add_figure(doc, 'fig10_bdv.png',
               '图 6-2  SAPC 击穿电压的双峰分布：缺陷峰在 1.4 V_R 处、主体峰在 2.5 V_R 处 (数据风格参考 Teverovsky, NASA/NEPP, 2024 [18] 与 Pozdeev-Freeman 2005 [38])')

    add_heading(doc, "6.5 自愈机理与其有限性", level=2)
    add_body(doc, """
SAPC 的 PEDOT 阴极具有一定的"自愈"能力，但其机理与液态铝电容和金属化薄膜电容的自愈都有本质不同。

6.5.1 自愈三步机理
当 Al₂O₃ 介质在局部薄弱点发生击穿时，从 Al 阳极流入的电流会集中在这一点上，瞬时电流密度极高；PEDOT 阴极在局部焦耳热作用下升温至 200-300°C，此时 PEDOT 发生"去掺杂"反应 (即 Tos⁻ 或 PSS⁻ 从聚合物链中脱出)，PEDOT 从导电态转变为绝缘态；绝缘态 PEDOT 形成的高阻区覆盖了击穿点，阻断了漏电路径。

这一过程可概括为"局部击穿 → 焦耳热 → PEDOT 去掺杂 → 自愈"。

6.5.2 自愈与反向自愈
然而这种自愈并非无代价的，也并非总是成功的：
(1) 每次自愈会消耗一定的有效 PEDOT 面积，长期积累会导致阴极电阻上升，即 ESR 逐步增大；
(2) 在高湿环境下，去掺杂的 PEDOT 可能因吸水而重新恢复导电性——这被称为"反向自愈" (reverse self-healing)，此时先前隔离的击穿点重新漏电，LC 再次上升 [43][56]；
(3) 如果击穿功率过大 (例如反向电压或浪涌)，焦耳热可能瞬时使 PEDOT 完全碳化为石墨态碳——碳化后形成永久性短路通道，失去自愈能力。

这些局限性意味着 SAPC 的自愈机制在设计上是"辅助性"而非"主导性"的。因此在器件设计中不应依赖自愈来应对过应力，必须通过电压降额、温度控制、湿度屏蔽等手段从根源降低击穿发生的概率 [16][18]。
""")
    add_figure(doc, 'fig12_selfhealing.png',
               '图 6-3  SAPC 中 PEDOT 阴极自愈三步过程示意图 (机理依据 Freeman & Lessner, KEMET, 2020 [16]; Rivera-Torres et al., Appl. Phys. Lett., 2013 [36]; Dupuis et al., Nat. Commun. Chem., 2020 [43])')

    add_heading(doc, "6.6 多应力耦合下的机理交互", level=2)
    add_body(doc, """
在实际应用中，SAPC 同时承受温度、电压、湿度、纹波电流、机械振动等多种应力，各机理之间存在显著的耦合与交互。理解这些耦合对寿命预测和可靠性建模至关重要。

典型的耦合效应包括：
(1) 温度 × 湿度 (T × H)：PEDOT 的水解速率在高温下显著加快 (反应速率 k ∝ exp(-E_a/kT))，因此同等湿度下 85°C/85%RH 比 60°C/85%RH 更具破坏力；但极高温度 (> 100°C) 下水汽沉降减少，反而减缓水解——存在一个最恶劣温度窗口 (约 85-95°C)；
(2) 温度 × 电压 (T × V)：Al₂O₃ 的漏电流对温度和电压都存在指数依赖，双应力作用下的激活能会有所降低；
(3) 湿度 × 电压 (H × V)：界面处 H₂O 在电场下发生极化，部分分解为 H⁺ 和 OH⁻，加剧对介质层的侵蚀；
(4) 机械振动 × 电化学：振动诱发的微位移会破坏已经愈合的 PEDOT 隔离区，导致反向自愈发生。

对这些耦合效应的定量建模是 SAPC 可靠性研究的前沿课题。传统的 Eyring 模型 t = A·exp(E_a/kT)·V^(-n)·H^(-m) 虽然可以在一定范围内拟合试验数据，但对耦合项的描述仍嫌粗糙。最新研究趋向于使用广义多元回归或物理信息神经网络 (PINN) 进行多应力寿命预测 [29][57]。
""")
    add_page_break(doc)
