# -*- coding: utf-8 -*-
"""参考文献"""
from rs_common import add_heading_cn, set_cn_font
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt


REFS = [
    "Wang H, Blaabjerg F. Reliability of capacitors for DC-link applications in power electronic converters—An overview. IEEE Transactions on Industry Applications, 2014, 50(5): 3569-3578.",
    "Wang H, Liserre M, Blaabjerg F. Toward reliable power electronics: Challenges, design tools, and opportunities. IEEE Industrial Electronics Magazine, 2013, 7(2): 17-26.",
    "Yang S, Bryant A, Mawby P, et al. An industry-based survey of reliability in power electronic converters. IEEE Transactions on Industry Applications, 2011, 47(3): 1441-1451.",
    "Prokopowicz T I, Vaskas A R. Research and development, intrinsic reliability, subminiature ceramic capacitors. Final Report ECOM-90705-F, NTIS AD-864068, 1969.",
    "Waser R, Baiatu T, Hardtl K H. dc electrical degradation of perovskite-type titanates. Journal of the American Ceramic Society, 1990, 73(6): 1645-1673.",
    "Baiatu T, Waser R, Hardtl K H. dc electrical degradation of perovskite-type titanates III: A model of the mechanism. Journal of the American Ceramic Society, 1990, 73(6): 1663-1673.",
    "Liu D, Sampson M J. Physics-of-failure assessment of base-metal-electrode ceramic capacitors. NASA NEPP Report, 2014.",
    "Liu D. Failure modes and mechanisms in BME multilayer ceramic capacitors with cracks. NASA Electronic Parts and Packaging (NEPP) Program, 2017.",
    "Teverovsky A. Reliability of solid tantalum capacitors: Field crystallization and breakdown. NASA NEPP Report, 2008.",
    "Teverovsky A. Breakdown voltages and leakage currents in solid tantalum capacitors. NASA NEPP Report, 2021.",
    "Pozdeev-Freeman Y, Gill J. Crystallization of anodic Ta2O5 in solid tantalum capacitors. CARTS Proceedings, 2004.",
    "Parler S G. Deriving life multipliers for electrolytic capacitors. IEEE Power Electronics Society Newsletter, 2004, 16(1): 11-12.",
    "Gasperi M L. Life prediction modeling of bus capacitors in AC variable-frequency drives. IEEE Transactions on Industry Applications, 2005, 41(6): 1430-1435.",
    "Sankaran V A, Rees F L, Avant C S. Electrolytic capacitor life testing and prediction. IEEE IAS Annual Meeting, 1997: 1058-1065.",
    "Venet P, Perisse F, El-Husseini M H, et al. Realization of a smart electrolytic capacitor circuit. IEEE Industry Applications Magazine, 2002, 8(1): 16-20.",
    "Abdennadher K, Venet P, Rojat G, et al. A real-time predictive-maintenance system of aluminum electrolytic capacitors. IEEE Transactions on Industry Applications, 2010, 46(4): 1644-1652.",
    "El-Husseini M H, Venet P, Rojat G, et al. Thermal simulation for geometric optimization of metallized polypropylene film capacitors. IEEE Transactions on Industry Applications, 2002, 38(5): 995-1001.",
    "Makdessi M, Sari A, Venet P. Metallized polymer film capacitors aging law. Microelectronics Reliability, 2014, 54(9-10): 1788-1796.",
    "Kim M, et al. Activation energy and lifetime estimation of high-capacitance MLCCs. Scientific Reports, 2024.",
    "Kim M, et al. Physics-constrained machine learning for failure-time prediction of MLCCs. APL Machine Learning, 2023.",
    "Lu X, et al. Reliability assessment of capacitors and transistors via BP neural network and thermal simulation. Scientific Reports, 2025.",
    "Sun Y, et al. Coupled electro-thermal stress aging of DC-link film capacitors in smart grids. Scientific Reports, 2025.",
    "Soualhi A, et al. Long short-term memory based RUL prediction of capacitors under dynamic conditions. 2022.",
    "Yan J, et al. Remaining useful life prediction of supercapacitors based on SG-VMD-LSTM. 2020.",
    "Kurzweil P, Frenzel B, Hildebrand A. Voltage-dependent capacitance and aging of supercapacitors. Journal of Power Sources, 2015.",
    "KEMET. Failure analysis of capacitors and inductors (technical white paper). 2019.",
    "TDK. Avoiding mechanical cracks (flex cracks) in MLCCs (application note). 2018.",
    "Murata. Chip multilayer ceramic capacitors for general purpose: cautions and failure mechanisms. 2020.",
    "IEC 60384-1. Fixed capacitors for use in electronic equipment - Part 1: Generic specification. International Electrotechnical Commission.",
    "MIL-HDBK-217F. Reliability prediction of electronic equipment. US Department of Defense.",
    "JEDEC JESD22 series. Reliability test methods for solid-state devices. JEDEC Solid State Technology Association.",
    "AEC-Q200. Stress test qualification for passive components. Automotive Electronics Council.",
    "Greason W D. Self-healing breakdown studies in metallized film capacitors. 1995.",

    # ===== 国内（中国）研究现状相关文献（第八章专论重点引用；DOI/卷期/作者信息建议在提交前逐条核验）=====
    "Removal of protonic doping from PEDOT:PSS by weak base for improving aluminum solid electrolytic capacitor performance. RSC Advances, 2025, DOI: 10.1039/D5RA00124B.（铝固态电解电容器/PEDOT:PSS去质子化；作者与卷期建议核验）",
    "High-performance solid capacitor using vapor phase polymerized PEDOT film. Journal of Materials Science, 2021, 56, DOI: 10.1007/s10853-021-05976-1.（气相聚合PEDOT固态电容；作者建议核验）",
    "Liquid electrolyte-free cylindrical Al polymer capacitor: Materials and characteristics (review). 2015.（无液态电解质柱状铝聚合物电容综述；卷期/作者建议核验）",
    "Lu W G, Zhou L W, Du X, 等. Grey-box online monitoring method for DC-link capacitors（重庆大学，直流母线电容灰箱在线监测）. IEEE Transactions on Power Electronics / 电工技术学报, 卷期与年份建议核验.",
    "Reliability Mechanisms of the Ultrathin-Layered BaTiO3-Based BME MLCC. 物理化学学报 (Acta Physico-Chimica Sinica), 2024, 40(1): 2304015.（超薄层BME MLCC可靠性机理）",
    "Huang X, 等. Excellent permittivity-temperature stability and reliability of ultra-thin Ba0.97Ca0.03TiO3-based MLCCs（中科院深圳先进电子材料研究院）. Journal of Asian Ceramic Societies, 2023, 11(1), DOI: 10.1080/21870764.2023.2166655.",
    "晶粒尺寸对多层陶瓷电容器可靠性的影响及其机理. 华南师范大学学报(自然科学版), 2024, DOI: 10.6054/j.jscnun.2024031.",
    "Jian Y, Chen Z, Peng S, 等. Capacitor Aging State Evaluation and a Remaining-Useful-Life Prediction Method Based on a CNN-LSTM Network Considering the Impact of Parameter Dispersion. Electronics (MDPI), 2025, 14(22): 4452.",
    "Huang Z, 等. An Online Remaining Useful Life Prediction Method for Tantalum Capacitors Based on Temperature Measurements. Electronics (MDPI), 2025, 14(22): 4393.",
    "Composite denoising-based LSTM prediction method of supercapacitor performance degradation law and remaining useful life. Circuit World (Emerald), 2024, DOI: 10.1108/CW-12-2023-0459.（作者建议核验）",
    "A physics-informed neural network-based method for predicting degradation trajectories and remaining useful life of supercapacitors. Green Energy and Intelligent Transportation, 2025, DOI: 10.1016/j.geits.2025.100291.",
    "Lifetime prediction and reliability analysis for aluminum electrolytic capacitors in EV charging module based on mission profiles. Frontiers in Electronics, 2023, 4: 1226006, DOI: 10.3389/felec.2023.1226006.",
    "Unveiling first self-healing in metallised film capacitor: A macro–micro analysis. High Voltage (CSEE/IET), 2025.（金属化膜电容自愈宏-微观分析；DOI/卷期建议核验）",
    "Study of the in situ test setup and analysis methods for self-healing properties of metallized film capacitors. Review of Scientific Instruments, 2024, 95(4): 045105, DOI: 10.1063/5.0194057.",
    "Capacitance Evaluation of Metallized Polypropylene Film Capacitors Considering Cumulative Self-Healing Damage. Electronics (MDPI), 2024, 13(14): 2886.",
    "Ma Y, 等. Detection of Self-Healing Discharge in Metallized Film Capacitors Using an Ultrasonic Method. Electronics (MDPI), 2020, 9(11): 1893.",
    "Song W, Yang X, Deng W, 等. Remaining Useful Life Prediction for Power Storage Electronic Components Based on Fractional Weibull Process and Shock Poisson Model. Fractal and Fractional (MDPI), 2024, 8(8): 485.",
    "Challenges and New Trends in Power Electronic Devices Reliability (含中国学者). Electronics (MDPI), 2021, 10(8): 925.",
    "一种高可靠性电解电容器的制造方法. 中国振华集团新云电子元器件有限责任公司, 中国发明专利 CN105489376B, 2016.",
    "金属化膜电容器初始自愈类型分类方法与系统. 中国发明专利 CN ZL2023 1 0098802.X（对应 US20240272240A1）, 2023/2024.",
    "艾华集团（湖南，上交所 603989）. 固态聚合物/多层聚合物铝电解电容器产品与可靠性技术资料（低ESR、不起火良性失效）. 企业技术资料.",
    "南通江海电容器股份有限公司（深交所 002484）. 铝电解、薄膜（DC-link）、聚合物混合及超级电容器产品与可靠性技术资料. 企业技术资料.",
    "GB/T 2693《电子设备用固定电容器 第1部分：总规范》(等同采用 IEC 60384-1). 中国国家标准（年代/版本建议核验）.",
    "GJB 360《电子及电气元件试验方法》及 GJB 系列高可靠电容器详细规范. 中国国家军用标准（具体编号/年代建议核验）.",

    "本报告国内研究现状部分（第八章专论）在上述可溯源公开文献基础上撰写，并综合参考了国内高校与研究院所在风电/光伏变流器母线电容在线监测、车规级MLCC裂纹扩展与可靠性、国产固态铝/聚合物电容材料与工艺、金属化膜电容自愈、超级电容循环寿命建模、数据驱动与物理信息RUL预测等方向的公开成果；凡未能确证的DOI、卷期或作者信息均已标注“建议核验”，提交前请在 CNKI / Web of Science / IEEE Xplore 及出版商页面逐条复核并按GB/T 7714统一著录。",
]


def build_references(doc):
    add_heading_cn(doc, "参考文献", level=1)
    for i, ref in enumerate(REFS, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(0.9)
        p.paragraph_format.first_line_indent = Cm(-0.9)
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run("[%d] %s" % (i, ref))
        set_cn_font(run, font_name="宋体", size_pt=10.5)
