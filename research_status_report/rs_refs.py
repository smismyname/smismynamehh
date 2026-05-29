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
    "本报告国内研究现状部分综合参考了国内高校与研究院所在风电/光伏变流器母线电容在线监测、车规级MLCC裂纹扩展有限元分析、国产钽电容场致结晶跟踪、超级电容循环寿命建模、数据驱动RUL预测等方向的公开成果（详见正文相应章节论述）。",
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
