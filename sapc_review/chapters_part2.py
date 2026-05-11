# -*- coding: utf-8 -*-
"""制造工艺 + 表征方法 章节"""
from docx_utils import (add_heading, add_body, add_page_break, add_figure,
                         add_formula, add_table, add_quote, set_cn_font)


def build_chapter3(doc):
    add_heading(doc, "第三章 制造工艺与工艺-可靠性耦合", level=1)

    add_heading(doc, "3.1 工艺流程总览", level=2)
    add_body(doc, """
SAPC 的制造工艺可分为前段 (阳极箔处理)、中段 (PEDOT 阴极沉积与叠层) 和后段 (引线焊接、封装、测试筛选) 三个大阶段，共涉及 30~50 道子工序。其中每一道工序都可能对最终器件的可靠性产生一阶影响。表 3-1 给出了主要工序与其对可靠性的影响机制：
""")
    add_table(
        doc,
        ["工序", "主要工艺参数", "对可靠性影响的关键机制"],
        [
            ["1. 铝箔纯化", "纯度 ≥99.99%", "杂质 (Fe, Si, Cu) 会作为蚀刻坑起始点，影响隧道均匀度"],
            ["2. 蚀刻 (etching)", "HCl + H₂SO₄, 1-3 mol/L, 75-85°C, 电流密度", "隧道密度/深度决定比容量；过度蚀刻降低机械强度"],
            ["3. 化成 (formation)", "硼酸铵/己二酸铵水溶液, V_form = 1.3 V_R, 85-95°C", "介质厚度/缺陷密度直接决定耐压、LC 与寿命"],
            ["4. 再化成 (reformation)", "低电流密度 0.1-0.3 V_form", "修复微观缺陷，降低 LC"],
            ["5. PEDOT 沉积", "in-situ / VPP / dispersion", "决定 ESR 初值与湿热退化速率"],
            ["6. 碳浆涂布", "导电碳浆，烘烤 150-200°C", "影响 PEDOT/Ag 欧姆接触"],
            ["7. 银浆涂布", "导电银浆，固化 180-220°C", "影响阴极电流汇流与 Ag 迁移"],
            ["8. 叠层压紧", "多片铝箔堆叠 3-12 层", "每层对齐度影响内部应力与寿命"],
            ["9. 引线框架焊接", "激光焊或超声焊", "焊接缺陷导致高 ESR 或开路"],
            ["10. 环氧模塑", "低吸湿低应力环氧, 175°C", "决定水汽屏障与 CTE 失配应力"],
            ["11. 老炼 (burn-in)", "85-105°C, 1.2 V_R, 数十小时", "去除早期失效品"],
            ["12. 终测", "C/ESR/LC @ 室温 + 高/低温", "筛选不合格品"],
        ],
        caption="表 3-1  SAPC 主要制造工序及其对可靠性的影响机制"
    )

    add_heading(doc, "3.2 阳极箔蚀刻工艺", level=2)
    add_body(doc, """
蚀刻工艺的核心目标是在 Al 箔表面形成均匀分布、足够深度的隧道状微孔以最大化有效表面积。典型直流蚀刻工艺中，蚀刻电流在 Al 表面引发局部阳极溶解，Cl⁻ 与 Al 表面的天然氧化膜形成可溶性 AlCl₄⁻ 络合物，在缺陷点处优先发生溶解而形成隧道。

蚀刻工艺的三个关键参数：
(1) 电流密度。电流密度越高，隧道起始密度越大，但单个隧道直径越小；电流密度过大会导致表面过蚀刻（表面粗糙度增加而有效表面积不增）。
(2) 电解液组成。HCl 作为主蚀刻剂提供 Cl⁻；H₂SO₄ 调节 pH 并抑制隧道侧向扩张，增加纵向生长速度；此外添加 HNO₃ 可增强氧化效应，形成更稳定的隧道 [31]。
(3) 温度。提高温度加快反应速率但降低反应选择性；工业生产中温度控制在 ±1°C 以内是批次一致性的关键。

2024 年 MDPI Metals 发表的一项工作 [33] 通过痕量 Cu (10-100 ppm) 的掺杂在 Al 箔表面电化学沉积出微电池，为隧道起始提供额外驱动力，使蚀刻后的比表面积提升约 30%。这是近年来阳极箔蚀刻工艺领域少见的重要创新。Al-Cu 微电池机制也解释了工业界长期观察到的"Al 箔痕量杂质对蚀刻行为存在强烈影响"的经验规律。

从可靠性角度看，蚀刻隧道过深或过于密集会导致以下问题：(1) 阳极箔机械强度下降，在叠层压紧过程中易折断；(2) 隧道密集处化成难以形成完整 Al₂O₃ 介质层；(3) PEDOT 填充隧道过程易留下空洞，形成空穴 (void)，在高温下成为热点。因此，现代工业界普遍采用 CV (capacitance × voltage) 积为目标的工艺优化，而非单纯追求高比容量 [34]。
""")

    add_heading(doc, "3.3 阳极氧化 (化成) 工艺", level=2)
    add_body(doc, """
化成工艺对 SAPC 的寿命具有决定性影响。典型工艺为：将蚀刻好的 Al 箔浸入 3% 硼酸铵水溶液，温度 85-92°C，施加电压 V_form = 1.3-1.5 V_R，维持恒压 3-20 分钟。这一过程中在 Al 箔表面生长出约 (1.4 nm/V) × V_form 厚度的 Al₂O₃ 非晶氧化膜。

化成过程涉及复杂的双向离子迁移：Al³⁺ 通过氧化膜向外迁移，O²⁻ 通过氧化膜向内迁移，两者在氧化膜中间相遇并结晶为 Al₂O₃ 网络。现场电压与电流行为遵循 Cabrera-Mott 理论，电流在电压突变时呈现尖峰，在恒压下按 ∝ t⁻¹ 衰减 [35][42]。

Al₂O₃ 氧化膜的质量由以下三个指标表征：
(1) 耐电压强度 BDV：典型为 V_form 的 1.2~1.4 倍；
(2) 漏电流 LC：典型 < 0.01 CV (μA) = 0.01·C(μF)·V(V)；
(3) 氧化膜结晶度：非晶态氧化膜的电学性能远优于含晶相者。

再化成是工业界普遍采用的工艺改进手段。其核心是在主化成之后施加一定电流限制下的恒电压，使得在主化成中未充分反应的缺陷点继续发生再氧化。这一过程可使 LC 下降一到两个量级 [36]。

SAPC 的一个工艺特点是：由于固态 PEDOT 阴极不能像液态电解液一样在现场修复介质层，化成质量必须在出厂前就达到极高标准。这就是为什么主流 SAPC 厂商都采用多阶段化成 + 再化成 + 热处理的复合工艺，而非单次化成。Panasonic SP-Cap 白皮书显示其采用 4 阶段化成工艺 [4]。
""")

    add_heading(doc, "3.4 PEDOT 阴极沉积工艺", level=2)
    add_body(doc, """
PEDOT 阴极沉积是 SAPC 最关键也最具工艺差异化的环节。如 2.4 节所述，工业界存在三种主要工艺路线。本节进一步详细讨论各工艺路线的具体操作、优缺点以及对长期可靠性的影响。

3.4.1 在位化学聚合 (in-situ chemical polymerization)
首先将化成好的 Al 箔浸入 EDOT 单体的醇溶液 (浓度 5~30 wt%) 约 30 秒~5 分钟，使 EDOT 充分渗入蚀刻隧道；随后浸入氧化剂 Fe(OTs)₃ 的醇溶液 (浓度 30~50 wt%)，在 30~80°C 下反应 0.5~2 小时完成聚合。反应完成后用醇和水冲洗去除残留的单体、氧化剂和副产物。

这一工艺的关键是控制反应速率，使其既快到足以在 PEDOT 胶体凝聚前完成孔内聚合，又慢到不会在浅层形成致密壳而阻塞深层渗透。Freeman 等 (KEMET) 研究表明，对于聚合过程控制不佳的样品，在 85°C/85%RH 环境下 1000 小时内 PEDOT 电导率可下降 50% 以上，主要原因是 Fe³⁺ 残留与 PEDOT:Tos 的局部水解 [16]。

3.4.2 预聚合分散液 (pre-polymerized dispersion)
将商品化的 PEDOT:PSS 分散液 (如 Heraeus CLEVIOS P 系列) 稀释至目标固含量后，浸渍并烘干；可能需要多次重复以达到目标厚度。PSS 的酸性 (pH ≈ 1-2) 对 Al₂O₃ 介质的长期稳定性构成挑战——RSC Materials Horizons 的一项工作指出，PSS 中的 SO₃H 基团会在水分存在下缓慢水解 Al₂O₃ [43]。为此，Heraeus 开发了经过"去酸化"处理的 CLEVIOS PH 系列产品，pH 可提高到 3-4，但会牺牲部分电导率。

3.4.3 气相聚合 (vapor-phase polymerization, VPP)
将化成好的 Al 箔涂以 Fe(OTs)₃ 氧化剂薄层，然后放入恒温恒湿 (60-80°C / 5-20% RH) 的反应腔中，通入 EDOT 蒸汽，反应 30 min~3 h 完成 PEDOT 沉积。VPP 的优点突出：(1) 得到的 PEDOT 薄膜电导率高 (10³ S/cm 量级)；(2) 孔隙填充率最高；(3) 无液相携带的污染 [28][39][40]。其缺点是反应速率受扩散限制，工艺窗口窄，对温湿度精确控制要求高。

Shi 等 2021 年在 J Mater Sci: Mater Electron [28] 上的工作通过 XRD 与 TEM 表征指出，VPP 过程可划分为三个阶段：覆盖期 (0-10 min，初始 PEDOT 单层覆盖氧化剂)、褶皱期 (10 min - 2 h，生成大量褶皱结构增加电导率) 与非晶期 (> 2 h，过度聚合导致结晶度下降电导率降低)。该工作给出 1 小时反应时间下得到最优性能的 PEDOT 膜，ESR 可达 3.71 mΩ。这一结果对 VPP 工艺的精确控制提供了微观机理指导。

表 3-2 系统对比了三种 PEDOT 沉积工艺路线：
""")
    add_table(
        doc,
        ["工艺", "电导率 (S/cm)", "孔隙填充", "工艺复杂度", "湿度稳定性", "代表厂商"],
        [
            ["in-situ", "200-500", "高", "中", "中-低", "NEC Tokin (早期), Nichicon"],
            ["pre-polymerized", "0.1-100", "中-低", "低", "高", "KEMET (部分), Murata"],
            ["VPP", ">1000", "很高", "高", "高", "Panasonic KX, AVX 部分系列"],
        ],
        caption="表 3-2  PEDOT 阴极三种沉积工艺对比"
    )

    add_heading(doc, "3.5 多层叠堆与压紧烧结", level=2)
    add_body(doc, """
完成 PEDOT 阴极与碳/银浆层的单片阳极箔按照目标容量进行叠堆，通过银导电胶或银烧结粘结成多层结构。叠堆工艺的关键挑战包括：
(1) 层间对齐——错位会导致部分有效电极面积丢失和局部电场集中；
(2) 粘结胶填充均匀性——气泡会在高温下形成热点；
(3) 叠堆应力均匀性——不均匀的压紧会在银浆/碳浆层引入剪切应力。

现代厂商多采用分层热压烧结工艺：在 180-220°C 下施加 5-20 MPa 的压力，持续 10-60 分钟完成银浆烧结。这一过程会固化银浆并释放溶剂，需要严格控制升温速率以避免气泡 [6][17]。
""")

    add_heading(doc, "3.6 端电极与封装密封", level=2)
    add_body(doc, """
端电极的主要功能是将阳极和阴极引线框架牵引到器件外表面，实现 SMT 贴装。典型的端电极结构为三层：(1) 内层 Cu (与引线框架连接)；(2) 阻挡层 Ni (典型 1-3 μm，防止 Sn 向 Cu 渗入形成脆性 IMC)；(3) 外层 Sn 或 Sn/Ag (可焊层, 2-10 μm)。端电极的 AEC-Q200 要求包括：耐温度循环、耐湿度、耐焊料浸渍等 [44]。

环氧封装的要求：低吸湿率 (< 0.3%)、低 CTE (10-20 ppm/°C)、高 Tg (> 150°C)、高粘接强度。实际工业中常用的封装材料包括 Sumitomo EME 系列、Shin-Etsu KMC 系列、Hitachi Chemical CEL 系列等。随着 PbCl₂、聚溴二苯醚 (PBDE) 等卤素阻燃剂被法规禁用，近年来无卤低吸湿环氧配方成为研发热点。

封装的薄弱环节是环氧/引线框架界面与环氧/PEDOT 界面。两者 CTE 差异可达 15-50 ppm/°C，在 -55~+125°C 循环下会产生显著剪应力，长期可能导致分层 (delamination)。CALCE 的 Liu 等 (2016) [19] 系统研究了封装几何 (引线框架露出面积、分层数、长宽比) 对湿度驱动失效的影响，发现封装几何优化可使 85°C/85%RH 下的寿命延长 1.5-3 倍。
""")

    add_heading(doc, "3.7 筛选与老炼工艺", level=2)
    add_body(doc, """
出厂前筛选是淘汰"早期失效品"(infant mortality) 的关键步骤。典型 SAPC 筛选流程包括：
(1) 初始电参数测试 (初测)：C @ 100 Hz/120 Hz/100 kHz, ESR @ 100 kHz, LC @ 额定电压；
(2) 高温老炼 (burn-in / ageing)：85-105°C 下施加 1.2~1.5 V_R，持续 20-100 小时；
(3) 再测与筛选：比较老炼前后的参数变化，淘汰 ΔC/C > 5% 或 ΔESR > 50% 的样品；
(4) 选择性应力筛选：如对航天级产品进行 HALT 或 HAST。

筛选强度的选择是一门工艺权衡艺术：过低的筛选强度无法淘汰潜在缺陷，过高的筛选强度会消耗合格品的寿命。工业界通常基于"破坏性物理分析 (DPA) + Weibull 分析"的联合结果确定筛选条件 [45]。
""")
    add_page_break(doc)


def build_chapter4(doc):
    from ch4_expanded import (CH4_INTRO, CH4_SEC41, CH4_SEC42, CH4_SEC43,
                               CH4_SEC44, CH4_SEC45, CH4_SEC46, CH4_CLOSE)

    add_heading(doc, "第四章 表征与检测方法", level=1)
    add_body(doc, CH4_INTRO)

    # ----- 4.1 电学参数 -----
    add_heading(doc, "4.1 电学参数表征", level=2)
    add_body(doc, CH4_SEC41)

    # ----- 4.2 EIS -----
    add_heading(doc, "4.2 电化学阻抗谱 (EIS)", level=2)
    add_body(doc, CH4_SEC42)
    add_figure(doc, 'fig09_eis.png',
               '图 4-1  SAPC 在 85°C/85%RH 加速老化过程中的 Nyquist 阻抗谱演化 (数据范式参照 Liu & Pecht, IEEE T-CPMT, 2017 [14]; Macdonald & Barsoukov, Wiley, 2005 [46])')
    add_figure(doc, 'fig17_bode.png',
               '图 4-2  SAPC 老化过程中 |Z|-f 与相位-频率 Bode 图 (Maguire, 2023 [67]; Liu & Pecht, 2017 [14])')

    # ----- 4.3 Micro-CT & C-SAM -----
    add_heading(doc, "4.3 X 射线显微 CT 与 C-SAM", level=2)
    add_body(doc, CH4_SEC43)
    add_figure(doc, 'fig18_microct.png',
               '图 4-3  Micro-CT 成像原理与典型 SAPC 内部缺陷重建特征 (成像原理参照 Piao et al., SPIE 9302, 2015 [69]; 器件结果示意参照 Teverovsky, NASA/NEPP, 2024 [18]; Liu, CALCE Tech Report, 2016 [19])')

    # ----- 4.4 SEM/TEM/EDS -----
    add_heading(doc, "4.4 SEM / TEM / EDS 微结构分析", level=2)
    add_body(doc, CH4_SEC44)

    # ----- 4.5 TGA / DSC -----
    add_heading(doc, "4.5 TGA / DSC 热分析", level=2)
    add_body(doc, CH4_SEC45)
    add_figure(doc, 'fig19_tga.png',
               '图 4-4  PEDOT:PSS 在空气与 N₂ 气氛下的 TGA 曲线及四阶段降解解释 (Marciniak et al., Synth. Met., 2004 [23]; Gregori et al., J. Surf. Eng. Mater. Adv. Technol., 2012 [71])')

    # ----- 4.6 FT-IR / Raman / XPS -----
    add_heading(doc, "4.6 FT-IR / Raman / XPS 化学分析", level=2)
    add_body(doc, CH4_SEC46)
    add_figure(doc, 'fig20_ftir.png',
               '图 4-5  PEDOT:PSS 在 85°C/85%RH 老化前后的 FT-IR 光谱对比 (Gregori et al., 2012 [71]; Marciniak et al., Synth. Met., 2004 [23])')
    add_figure(doc, 'fig16_raman.png',
               '图 4-6  新制 PEDOT 与 85°C/85%RH 老化 1500 h 后 PEDOT 的 Raman 谱对比 (掺杂度分析参照 Chatterjee et al., PCCP, 2022 [72]; Kvarnström et al., Macromolecules, 2004 [49])')
    add_figure(doc, 'fig15_xps_s2p.png',
               '图 4-7  PEDOT 阴极的 XPS S 2p 峰分峰拟合示例 (分峰参数参照 Akdemir et al., Mater. Res. Express, 2025 [73]; Zotti et al., 2004 [50])')

    # ----- 4.7 组合应用策略 -----
    add_heading(doc, "4.7 表征方法的组合应用策略", level=2)
    add_body(doc, CH4_CLOSE)
    add_table(
        doc,
        ["失效现象", "一级方法", "二级方法", "目标证据链"],
        [
            ["ESR 上升、C 与 LC 微变", "EIS (识别 R_s 或 R_p 主导)", "FIB+SEM+Raman+XPS", "PEDOT 去掺杂 或 界面分层"],
            ["LC 跑飞、ESR 微变", "C-SAM 定位分层", "Micro-CT+FT-IR+XPS (O1s)", "PSS 水解 + Al₂O₃ 羟基化"],
            ["C 显著下降", "Micro-CT 定量 PEDOT 填充率", "TEM (Al₂O₃ 截面)", "有效电极面积损失"],
            ["灾难性短路 (HALT)", "C-SAM+Micro-CT 定位", "FIB+TEM+Raman (D/G 带)", "PEDOT 局部碳化"],
            ["外观变色/鼓胀", "光学显微 + C-SAM", "DSC/TGA+FT-IR", "环氧老化 或 PEDOT 降解副产物"],
            ["端电极开路", "X 射线 2D 透视", "SEM 横截面 (IMC)", "Sn/Cu IMC 疲劳裂纹"],
        ],
        caption="表 4-1  SAPC 典型失效现象与表征方法组合决策矩阵"
    )
    add_page_break(doc)
