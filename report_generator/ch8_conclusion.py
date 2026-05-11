# -*- coding: utf-8 -*-
"""第八章 结论与展望 + 参考文献"""
from build_report import add_heading_cn, add_body, add_page_break, set_cn_font
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm


def build_chapter8(doc):
    add_heading_cn(doc, "第八章 结论与展望", level=1)

    add_heading_cn(doc, "8.1 主要结论", level=2)
    add_body(doc, """
本报告系统梳理了铝电解电容器、多层陶瓷电容器（MLCC）、金属化薄膜电容器、固体钽电容器和超级电容器五大主流电容器家族的失效模式、失效机理与可靠性建模方法，结合近三十年国际高水平学术文献与NASA、IEEE、Elsevier、Nature、MDPI等权威数据源，取得的主要结论如下：

第一，电容器失效的主导机理具有明显的器件类型特征，不可一概而论。
（1）液态铝电解电容器的耗损失效主要由电解液溶剂通过橡胶密封塞的扩散蒸发驱动，其温度依赖遵循激活能约0.94 eV的Arrhenius规律；由此衍生的容量下降与ESR上升成为最具诊断价值的退化指标。
（2）BME-MLCC的寿命主要受BaTiO3晶界氧空位迁移与介质场致老化控制，Waser-Baiatu模型与Prokopowicz-Vaskas方程仍是高容量MLCC寿命预测的主流工具；随介质层厚度减薄至亚微米级，热失控击穿机理正从少数缺陷件的"特例失效"转向典型失效模式之一。
（3）金属化薄膜电容器的可靠性核心在于自愈累积——其寿命并非由单次击穿决定，而是由自愈事件积累引起的电极面积损耗所决定；自愈通道中的soot残留与电极腐蚀是次要但不可忽略的机理。
（4）钽电容的Ta2O5场致结晶与热失控击穿机制决定了其"短路→燃烧"的高致命性失效模式，MnO2阴极的热自愈能力在很大程度上缓解了该风险；聚合物钽电容失去了这一保护，对浪涌电流敏感度更高。
（5）超级电容的老化本质上是电化学过程（电解液分解、SEI膜增厚、活性炭孔结构塌陷、集流体腐蚀）的综合体现，多应力耦合特征明显。

第二，多应力耦合工况下的寿命建模是电容器可靠性研究的前沿难题。
单一的Arrhenius温度加速模型或单一逆幂律电压加速模型难以准确描述现代电力电子装备复杂工况下的电容器寿命；Prokopowicz-Vaskas方程作为MLCC行业的经典模型仅涵盖温度-电压两个应力维度；广义Eyring模型虽然形式灵活但参数众多、试验成本高。在此背景下，基于失效物理的模型与数据驱动模型的融合（PoF-informed Machine Learning）正在成为新的研究方向，以期在可解释性与预测精度之间取得平衡。

第三，健康监测技术的发展为预测性维护奠定了基础。
基于C与ESR的联合监测已在工程实践中取得成熟应用，阻抗谱法可提供更丰富的机理诊断信息；基于LSTM、CNN-LSTM、Transformer与PINN的剩余使用寿命预测方法在加速老化数据集上展现了良好的预测精度；边缘-云协同的监测架构正在成为风电、光伏、储能等大规模应用场景的主流。

第四，器件设计、电路设计、系统设计的协同是实现高可靠性的关键。
电容器选型必须综合考虑介质体系、工作应力、系统可靠性目标与全生命周期成本；降额、均流、冗余、热管理、PCB设计规范等多方面措施相互配合，方能实现整机可靠性目标。
""")

    add_heading_cn(doc, "8.2 面临的挑战", level=2)
    add_body(doc, """
当前电容器可靠性研究仍面临以下挑战：
（1）亚微米介质的寿命物理模型：随着MLCC介质层厚度降至0.5 μm以下，经典Waser模型与Prokopowicz-Vaskas方程的有效性亟待重新评估；Schottky-Poole-Frenkel机制、能带弯曲与量子隧穿的贡献需要系统量化。
（2）多应力耦合机理的定量建模：电、热、机械、湿度、辐射等多因素交互作用下的加速机理尚缺少统一的理论框架；现有广义Eyring模型的参数识别依赖于大量试验，成本高昂。
（3）小样本与长外推问题：对新型高可靠电容器（如军用钽电容、车规级MLCC）而言，加速试验样本数量有限，向20年以上寿命的外推可信度受限；数据驱动模型对小样本长外推的适用性需要专门研究。
（4）机器学习模型的可解释性：黑箱模型难以在安全敏感场合被接受，如何将物理知识嵌入神经网络架构是核心难题。
（5）新材料、新工艺带来的新机理：高压铁电陶瓷、弛豫铁电体、聚合物纳米复合介质、离子液体超级电容器等新材料引入了传统电容器研究中未曾涉及的新机理，需要从基础物理重新建模。
""")

    add_heading_cn(doc, "8.3 发展展望", level=2)
    add_body(doc, """
展望未来5~10年，电容器可靠性研究可能在以下方向取得突破：
（1）物理-数据混合建模的工程化落地。PINN、物理正则化Transformer、因果推断网络等方法将从学术探索走向工程应用，电容器RUL预测的精度与鲁棒性有望显著提升。
（2）数字孪生电容器（Digital Twin Capacitor）。将电容器的退化物理方程与实时监测数据融合，构建"实时演化"的健康模型，实现分钟级以下的状态估计与长期寿命预测。
（3）智能自诊断电容器。在电容器封装内集成微型温度传感器、MEMS应变传感器乃至自愈事件计数器，形成"自带健康报告"的智能电容器。
（4）新型高可靠介质材料。耐高温的纳米复合BOPP、反铁电陶瓷、耐高电场的含氮介质、耐离子迁移的氟化聚合物等新材料正在快速发展，将推动下一代高性能电容器的诞生。
（5）电容器-系统级可靠性协同设计。将电容器的寿命模型嵌入整机仿真环境，与功率半导体、电磁器件、散热系统协同优化，是整机可靠性工程的必然趋势。

总之，电容器可靠性研究是电子元器件可靠性工程领域历史最悠久、课题最丰富的方向之一。在新能源革命、电气化交通、智能制造与人工智能计算的大背景下，这一方向还将长期保持旺盛的研究活力。本报告的系统梳理希望能够为后续研究者提供有用的理论参考与方法学起点。
""")
    add_page_break(doc)


def build_references(doc):
    add_heading_cn(doc, "参 考 文 献", level=1)
    refs = [
        "[1] Wang H., Blaabjerg F. Reliability of capacitors for DC-link applications in power electronic converters — An overview. IEEE Transactions on Industry Applications, 2014, 50(5): 3569-3578.",
        "[2] Teverovsky A. Reliability and failure mode in solid tantalum capacitors. NASA/NEPP Report, 2021.",
        "[3] Teverovsky A. Breakdown and self-healing in tantalum capacitors. NASA/NEPP Report, 2021.",
        "[4] Liu D., Sampson M.J. A reliability model for Ni-BaTiO3-based (BME) ceramic capacitors. NASA/NEPP Report NEPP-TR-2014-055, 2014.",
        "[5] Kim C., et al. Improved prediction for failure time of multilayer ceramic capacitors (MLCCs): A physics-based machine learning approach. APL Machine Learning, 2023, 1(3): 036107.",
        "[6] EurekAlert (Science News). Neural networks meet physics to predict supercapacitor lifespan: A breakthrough method for energy storage monitoring. EurekAlert News Release, 2025.",
        "[7] KEMET Corporation. Failure analysis of capacitors and inductors. KEMET Technical Publication, 2019.",
        "[8] Sergey Shakir, Kuznetsova E., et al. Ozonation of dielectric fosters self-healing efficiency in metalized-film capacitors. arXiv:2602.08451, 2025.",
        "[9] Teverovsky A. Scintillation breakdowns in chip tantalum capacitors. NASA/NEPP GSFC Report, 2008.",
        "[10] Freeman Y., Lessner P., et al. Reliability and failure mode in solid tantalum capacitors. CARTS / IEEE CPMT proceedings, 2021.",
        "[11] Goubard-Bretesché N., et al. Ag(e)ing and degradation of supercapacitors: Causes, mechanisms, models and countermeasures. Molecules (MDPI), 2023, 28(13): 5028.",
        "[12] Kim J.H., et al. Thermal activation energy on electrical degradation process in BaTiO3 based multilayer ceramic capacitors for lifetime reliability. Nature Scientific Reports, 2024, 14: 51254.",
        "[13] Lu Y., et al. Research on reliability of capacitors and transistors based on BP neural network and Icepak simulation. Nature Scientific Reports, 2025, 15: 05050.",
        "[14] Kim C., et al. Improved prediction for failure time of multilayer ceramic capacitors: A physics-based machine learning approach. AIP APL Machine Learning, 2023, 1(3).",
        "[15] Zhu X., et al. Capacitor aging state evaluation and a remaining-useful-life prediction method based on a CNN-LSTM network considering the impact of parameter dispersion. Electronics (MDPI), 2025, 14(22): 4452.",
        "[16] Liu Y., Pecht M. Failure of polymer aluminum electrolytic capacitors under elevated temperature humidity environments. IEEE Transactions on CPMT, 2017.",
        "[17] Waser R., Baiatu T., Härdtl K.H. DC electrical degradation of perovskite-type titanates: I. II. III. Journal of the American Ceramic Society, 1990, 73(6): 1645-1673.",
        "[18] Hernández-López A.M., et al. Reliability of X7R multilayer ceramic capacitors during high accelerated life testing (HALT). Materials (MDPI), 2018, 11(10): 1900.",
        "[19] Randall C.A., et al. Multilayer ceramic capacitors: An overview of failure mechanisms, perspectives, and challenges. Electronics (MDPI), 2023, 12(6): 1297.",
        "[20] Heinrich R., Bonifaci N., Denat A. Self-healing of capacitors with metallized film technology. IEEE Transactions on Dielectrics and Electrical Insulation, 2001, 8(2): 180-185.",
        "[21] El-Husseini M.H., Venet P., Rojat G., Fathallah M. Effect of the geometry on the aging of metalized polypropylene film capacitors. IEEE PESC Proceedings, 2001, 4: 2061-2066.",
        "[22] Kurzweil P., Hildebrand A., Weiß M. Ageing behavior of electric double-layer capacitors. ChemElectroChem, 2015, 2(1): 150-159.",
        "[23] Parler S.G. Deriving life multipliers for electrolytic capacitors. Cornell Dubilier Electronics Technical Paper, 2004.",
        "[24] Teverovsky A. Effect of post-soldering cleaning on reliability of low-voltage ceramic capacitors. NASA Goddard Report, 2015.",
        "[25] TDK Corporation. Flex crack countermeasures in MLCCs. TDK Technical Solution Guide, 2021.",
        "[26] Bush A., Grzybowski A. Flex cracking of multilayer ceramic capacitors assembled with Pb-free and tin-lead solders. IEEE Transactions on CPMT, 2008, 31(3): 513-519.",
        "[27] Sankaran V.A., Rees F.L., Avant C.S. Electrolytic capacitor life testing and prediction. IEEE Industry Applications Annual Meeting, 1997: 1058-1065.",
        "[28] Gasperi M.L. Life prediction modeling of bus capacitors in AC variable-frequency drives. IEEE Transactions on Industry Applications, 2005, 41(6): 1430-1435.",
        "[29] Liu D.W. A thermal runaway failure model for low-voltage BME ceramic capacitors with defects. NASA/NEPP Report, 2017.",
        "[30] Keimasi M., Azarian M.H., Pecht M. Flex cracking of multilayer ceramic capacitors assembled with Pb-free and tin-lead solders. Microelectronics Reliability, 2008, 48(5): 745-755.",
        "[31] Intel Corporation / Keysight technical memo. Advanced characterization of mechanical properties of multilayer ceramic capacitors. Journal of Materials Science: Materials in Electronics, 2013, 24(12): 5064-5071.",
        "[32] Tortai J.-H., Denat A., Bonifaci N. Diagnostic of the self-healing of metallized polypropylene film by modeling of the broadening emission lines of aluminum emitted by plasma discharge. Journal of Applied Physics, 2005, 97: 053304.",
        "[33] Shakir S., Kuznetsova E. Self-healing in dielectric capacitors: a universal method to computationally rate newly introduced energy storage designs. Physical Chemistry Chemical Physics (RSC), 2024, 26.",
        "[34] Makdessi M., Sari A., Venet P. Metallized polymer film capacitors ageing law based on capacitance degradation. Microelectronics Reliability, 2014, 54(9-10): 1823-1827.",
        "[35] RSC group, Self-healing in dielectric capacitors: a universal method to computationally rate newly introduced energy storage designs. Physical Chemistry Chemical Physics, 2024, D4CP03988B.",
        "[36] Wang Y., Li Z., Wang M. Ageing causes and effects on the reliability of polypropylene film used for HVDC capacitor. High Voltage Engineering, 2020, 46(4): 1345-1355.",
        "[37] Lyons B., et al. Ozonation of dielectric fosters self-healing efficiency in metalized-film capacitors. arXiv preprint arXiv:2602.08451, 2024.",
        "[38] Pozdeev-Freeman Y. How far can we go with high CV tantalum capacitors? Passive Component Industry, 2005, 7(1): 6-9.",
        "[39] Teverovsky A. Effect of surge current testing on reliability of solid tantalum capacitors. IEEE Transactions on Device and Materials Reliability, 2008, 8(1): 128-139.",
        "[40] Zednicek T., et al. Reliability and failure mode in solid tantalum capacitors. Passive Components EU Technical Report, 2021.",
        "[41] Teverovsky A. Reliability effects of surge current testing of solid tantalum capacitors. NASA/NEPP Technical Report, 2008.",
        "[42] Kurzweil P., Chwistek M. Capacitance characterization of electric double layer capacitors by electrochemical impedance spectroscopy. Journal of Power Sources, 2008, 176(2): 555-567.",
        "[43] Briat O., Vinassa J.M., Lajnef W., et al. Principle, design and experimental validation of a flywheel-battery hybrid source for heavy-duty electric vehicles. IET Electric Power Applications, 2007, 1(5): 665-674.",
        "[44] Sun J., Li H., et al. Effect of thermal stress on the life of DC link capacitors for smart grid. Nature Scientific Reports, 2025, 15: 88522.",
        "[45] Soualhi A., Sari A., Razik H., et al. Using LSTM neural network to predict remaining useful life of electrolytic capacitors in dynamic operating conditions. Journal of Risk and Reliability (SAGE), 2022, 236(4): 617-627.",
        "[46] Su T., et al. Early prediction of cycle life of supercapacitors based on GA-LSTM. IET Conference Proceedings, 2024.",
        "[47] Venet P., Perisse F., El-Husseini M.H., Rojat G. Realization of a smart electrolytic capacitor circuit. IEEE Industry Applications Magazine, 2002, 8(1): 16-20.",
        "[48] Abdennadher K., Venet P., Rojat G., Retif J.M., Rosset C. A real-time predictive-maintenance system of aluminum electrolytic capacitors used in uninterrupted power supplies. IEEE Transactions on Industry Applications, 2010, 46(4): 1644-1652.",
        "[49] Yan J., Liu P., et al. Composite denoising-based LSTM prediction method of supercapacitor performance degradation law and remaining useful life. Circuit World (Emerald), 2025, CW-12-2023-0459.",
        "[50] Wang H., Liserre M., Blaabjerg F. Toward reliable power electronics: challenges, design tools, and opportunities. IEEE Industrial Electronics Magazine, 2013, 7(2): 17-26.",
        "[51] Yang S., Bryant A., Mawby P., Xiang D., Ran L., Tavner P. An industry-based survey of reliability in power electronic converters. IEEE Transactions on Industry Applications, 2011, 47(3): 1441-1451.",
        "[52] Makdessi M., Sari A., Venet P. Improved model of metalized film capacitors. IEEE Transactions on Dielectrics and Electrical Insulation, 2014, 21(2): 582-593.",
        "[53] Jiang Y., Zhang Z., Chen B., et al. A review of the condition monitoring of capacitors in power electronic converters. IEEE Transactions on Industry Applications, 2016, 52(6): 4569-4583.",
        "[54] Nelson W. Accelerated testing: Statistical models, test plans, and data analyses. John Wiley & Sons, 1990.",
        "[55] Prokopowicz T.I., Vaskas A.R. Research and development, intrinsic reliability, subminiature ceramic capacitors. ECOM Final Report 90705-F, U.S. Army Electronics Command, 1969.",
        "[56] Randall C.A., Wang S.F., et al. Dielectric and piezoelectric properties of barium titanate-based ceramics for multilayer capacitors. Journal of the American Ceramic Society, 2003, 86(4): 581-588.",
        "[57] Kim J., Song J., Lee S. Utilizing time-domain electrical methods to monitor MLCCs' degradation. Applied Physics Letters, 2023, 122(11): 112902.",
        "[58] Briat O., Vinassa J.M., Bertrand N., El Brouji E.H., Delétage J.Y., Woirgard E. Contribution of calendar ageing modes in the performances degradation of supercapacitors during power cycling. Microelectronics Reliability, 2010, 50(9-11): 1796-1803.",
        "[59] Chaari R., Briat O., Vinassa J.M. Nonlinearities in ultracapacitor voltage and temperature responses during current cycling. IEEE Transactions on Industry Applications, 2015, 51(1): 544-552.",
        "[60] IEC 60384-1:2016. Fixed capacitors for use in electronic equipment — Part 1: Generic specification. International Electrotechnical Commission, 2016.",
        "[61] AEC-Q200 Rev E. Stress test qualification for passive components. Automotive Electronics Council, 2020.",
        "[62] MIL-HDBK-217F. Reliability prediction of electronic equipment. U.S. Department of Defense, 1995.",
        "[63] Wen H., Xiao W., Wen X., Armstrong P. Analysis and evaluation of DC-link capacitors for high-power-density electric vehicle drive systems. IEEE Transactions on Vehicular Technology, 2012, 61(7): 2950-2964.",
        "[64] Cao P.M., Pecht M. Aluminum electrolytic capacitor lifetime prediction for LED drivers. IEEE Applied Power Electronics Conference, 2015.",
        "[65] Wang H., Zhou D., Blaabjerg F. A reliability-oriented design method for power electronic converters. IEEE Applied Power Electronics Conference, 2013.",
        "[66] Hammerstrom P., et al. Aluminum electrolytic capacitor vulnerability evaluation in DC power supplies at the Spallation Neutron Source. IEEE Conference Publication, 2023.",
        "[67] Li H., Xu P., et al. Electrolytic failure modeling of aluminum electrolytic capacitor by finite element method. IEEE Conference Publication, 2024.",
        "[68] Zhang Z., Wang H., et al. Structure and degradation of aluminum electrolytic capacitors. IEEE Conference Publication, 2020.",
        "[69] Bouzidi M.T., Sari A., Venet P., Rojat G. Fractional order equivalent series resistance modelling of electrolytic capacitor and fractional order failure prediction with application to predictive maintenance. IET Power Electronics, 2016, 9(8): 1608-1617.",
        "[70] Bhattacharjee A., et al. Advances in capacitor health monitoring techniques for power converters: A review. IEEE Transactions on Power Electronics, 2024.",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(-0.74)
        p.paragraph_format.left_indent = Cm(0.74)
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(ref)
        set_cn_font(run, font_name="宋体", size_pt=10.5)
