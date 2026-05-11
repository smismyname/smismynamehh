# -*- coding: utf-8 -*-
"""第五章 电容器可靠性建模方法"""
from build_report import add_heading_cn, add_body, add_page_break, add_table_simple, add_formula


def build_chapter5(doc):
    add_heading_cn(doc, "第五章 电容器可靠性建模方法", level=1)

    add_body(doc, """
可靠性建模的目的是建立器件电参数、应力水平、工作时间与失效概率之间的定量关系，从而支持寿命预测、加速试验规划、降额设计与维护决策。本章按照"统计模型→加速寿命模型→物理失效模型→数据驱动混合模型"的逻辑递进，系统梳理电容器领域常用的可靠性建模方法，并讨论各自适用范围与局限。
""")

    add_heading_cn(doc, "5.1 统计可靠性模型", level=2)
    add_heading_cn(doc, "5.1.1 基本可靠性函数", level=3)
    add_body(doc, """
可靠性函数R(t)表示元件在工作至时间t时仍未失效的概率：
""")
    add_formula(doc, "R(t) = P(T > t) = 1 - F(t)")
    add_body(doc, """
其中F(t)为失效时间T的累积分布函数。对应的失效密度函数为f(t) = dF(t)/dt。瞬时失效率（hazard rate）定义为：
""")
    add_formula(doc, "λ(t) = f(t) / R(t) = -d[ln R(t)]/dt")
    add_body(doc, """
平均失效时间MTTF = ∫R(t)dt（从0到+∞）。对于修复型部件（虽然电容器通常不修复），则以MTBF（Mean Time Between Failure）表征。失效率的工程单位常采用FIT（Failures in Time，1 FIT = 1 failure per 10^9 device-hours）。
""")

    add_heading_cn(doc, "5.1.2 Weibull分布", level=3)
    add_body(doc, """
两参数Weibull分布是电容器寿命数据分析中最广泛使用的分布模型，其累积分布函数与概率密度函数分别为：
""")
    add_formula(doc, "F(t) = 1 - exp[-(t/η)^β]")
    add_formula(doc, "f(t) = (β/η)·(t/η)^(β-1)·exp[-(t/η)^β]")
    add_body(doc, """
其中β为形状参数（shape parameter），η为尺度参数（scale parameter，等于失效概率63.2%时的时间）。β的工程含义十分丰富：β<1对应早期失效（hazard rate递减），β≈1对应随机失效（恒定hazard rate，指数分布），β>1对应耗损失效（hazard rate递增）。NASA Liu与Sampson（2014）的BME MLCC可靠性模型中β典型值在1.5~4.0之间[4]，Makdessi等（2014）的MPFC研究中β在1.2~2.5之间，Teverovsky（2008）的钽电容研究中场致结晶失效的β约为0.8~1.2（具有早期失效特征）。

Weibull参数的估计方法主要有：
（1）最大似然估计（MLE），适合完全数据与右删失数据；
（2）中位秩回归（Median Rank Regression），简单直观，工程常用；
（3）贝叶斯估计，适合结合先验信息的情形。
对于多个失效模式混合的数据，通常采用混合Weibull或分段Weibull模型。
""")

    add_heading_cn(doc, "5.1.3 对数正态分布与正态分布", level=3)
    add_body(doc, """
对于由"乘积型"过程（如多步扩散、迁移）主导的失效，对数正态分布（lognormal distribution）常常具有更好的拟合效果：
""")
    add_formula(doc, "f(t) = 1/(tσ√(2π)) · exp[-(ln t - μ)² / (2σ²)]")
    add_body(doc, """
其中μ、σ为对数化时间的均值与标准差。在Al-cap、超级电容的电解液蒸发过程中，由于蒸发过程可近似为扩散与泄漏的乘积过程，lognormal模型往往比Weibull更为贴合。

正态分布主要用于参数漂移（如ΔC/C、ESR倍增）的生产批次分布分析，一般不直接用于寿命建模。
""")

    add_heading_cn(doc, "5.1.4 混合Weibull与竞争失效", level=3)
    add_body(doc, """
在实际加速试验中，电容器经常呈现多失效模式共存，例如MLCC同时存在早期缺陷型短路与后期氧空位致退化型失效。此时单一Weibull无法准确拟合，需要采用混合Weibull（mixed Weibull）或竞争失效模型（competing risks model）。Liu-Sampson模型将BME MLCC的可靠性函数表达为两个独立失效模式之乘积：
""")
    add_formula(doc, "R_total(t) = R_catastrophic(t) · R_slow_degradation(t)")
    add_body(doc, """
其中灾难性失效对应低β值（早期失效），而慢退化失效对应高β值（耗损失效）[4][29]。这一分解模型已成为现代MLCC可靠性评估的标准范式。
""")

    add_heading_cn(doc, "5.2 加速寿命试验与Arrhenius类模型", level=2)
    add_heading_cn(doc, "5.2.1 加速寿命试验的理论基础", level=3)
    add_body(doc, """
加速寿命试验（Accelerated Life Test, ALT）的理论基础是"应力-寿命（stress-life）等效关系"——在不同应力水平下，失效过程的物理机理保持一致，寿命仅通过一个加速因子AF与常态寿命相关联。Nelson在其经典著作《Accelerated Testing》（1990）中给出了这一等效的三个必要条件：
（1）失效机理不变（no shift in failure mechanism）；
（2）分布形状参数不变（shape parameter invariance）；
（3）累积损伤可线性叠加（Miner-Palmgren准则适用）。
违反上述任一条件，ALT结果都不能线性外推到实际工况。
""")

    add_heading_cn(doc, "5.2.2 Arrhenius温度加速模型", level=3)
    add_body(doc, """
Arrhenius模型描述温度对失效速率的加速作用：
""")
    add_formula(doc, "AF_T = exp[(Ea/k)·(1/T_use - 1/T_stress)]")
    add_body(doc, """
其中Ea为激活能（eV），k为玻尔兹曼常数（8.617×10⁻⁵ eV/K），T以绝对温标计。典型激活能取值：
（1）Al-cap电解液蒸发：0.94 eV[28]；
（2）BME MLCC氧空位迁移：1.0~1.5 eV[12][17]；
（3）Ta2O5场致结晶：1.0~1.5 eV[9][38]；
（4）BOPP氧化老化：0.8~1.2 eV。

所谓"10℃法则"（温度每升高10℃寿命减半）对应于在70~125℃范围内Ea约0.55~0.65 eV的特定情况，不是普适规律。选择Ea时必须基于具体失效机理的物理建模，而非盲目套用经验常数。
""")

    add_heading_cn(doc, "5.2.3 逆幂律电压加速模型", level=3)
    add_body(doc, """
对电压应力而言，加速因子通常服从逆幂律（Inverse Power Law）：
""")
    add_formula(doc, "AF_V = (V_stress / V_use)^n")
    add_body(doc, """
其中幂指数n反映电压对寿命的敏感度。典型值：
（1）MLCC：n=3~7（Prokopowicz-Vaskas）[4][12]；
（2）BOPP薄膜：n=7~13（Kawamura, 1988）；
（3）Ta2O5：n=15~40（结晶模型）[9]。

n值越大，说明寿命对电压越敏感。电压加速模型中的n并非纯经验参数，而是与介质内部的退化机理紧密相关。对MLCC而言，n与氧空位迁移中电场对势垒的降低作用有关；对BOPP而言，n反映了电子雪崩注入过程的非线性响应。
""")

    add_heading_cn(doc, "5.3 Prokopowicz-Vaskas方程", level=2)
    add_body(doc, """
Prokopowicz-Vaskas方程是MLCC行业最经典也最广泛使用的加速寿命模型：
""")
    add_formula(doc, "t1/t2 = (V2/V1)^n · exp[(Ea/k)·(1/T1 - 1/T2)]")
    add_body(doc, """
其中（t1, V1, T1）与（t2, V2, T2）为两个试验点的寿命、电压、温度。该方程同时包含Arrhenius温度项与逆幂律电压项，是典型的"乘积分离"型加速模型。Kim等（2024）基于125~250℃、1.1~5倍额定电压的BME MLCC加速试验数据，给出了现代高容X7R MLCC的Ea=0.88~1.49 eV、n=3.1~4.8的拟合参数，并证实Prokopowicz-Vaskas方程在五倍额定电压以下保持良好的线性外推能力[12]。

然而Prokopowicz-Vaskas方程存在若干假设前提：
（1）失效机理在ALT应力范围内保持不变，即严格的机理同一性；
（2）电场-温度两因素可线性分离，忽略交互项；
（3）介质厚度与工作场强关系已固定。

对于亚微米级介质厚度的最新MLCC，当电场强度超过20 V/μm时，Schottky-Poole-Frenkel发射机制将逐步取代氧空位迁移成为主导机制，此时经典Prokopowicz-Vaskas方程不再适用，需要引入修正项。Teverovsky（NASA/NEPP）对此问题有详细论述。
""")

    add_heading_cn(doc, "5.4 多应力广义Eyring模型", level=2)
    add_body(doc, """
对于多应力耦合工况，广义Eyring模型（Generalized Eyring Model）提供了比Arrhenius+逆幂律更普适的框架：
""")
    add_formula(doc, "t_f = A · T^m · exp(Ea/kT) · exp(B·S1 + C·S2·… + D/kT·S1·S2 + …)")
    add_body(doc, """
其中S1, S2为电场、湿度等非温度应力，D/kT·S1·S2形式的项显式引入了非线性交互效应。Eyring模型的优点是能够描述交互作用；缺点是参数众多、试验成本高。IEC 62380、Military Handbook 217F的部件应力法在一定意义上就是广义Eyring模型的简化工程实现。

对于DC-link金属化薄膜电容，Sun等（2025）提出了考虑热应力和电应力耦合的修正Eyring模型，形式如下：
""")
    add_formula(doc, "L(V, T) = L0 · (V0/V)^n · exp[Ea/k·(1/T - 1/T0)] · g(ΔT_ripple)")
    add_body(doc, """
其中g(ΔT_ripple)是描述纹波电流引起自发热循环损伤的修正因子，本质上是Manson-Coffin低周疲劳损伤的一阶近似[44]。这种多因素复合模型在工程实践中已被广泛应用于逆变器DC-link电容的寿命预测。
""")

    add_heading_cn(doc, "5.5 基于失效物理的寿命模型（PoF）", level=2)
    add_body(doc, """
PoF模型不依赖于大量经验试验，而是从微观退化物理量的演化出发，通过对底层变量的建模给出寿命估计。典型的PoF建模步骤如下：
（1）识别主导退化变量（如ESR、C、IR、漏电流）；
（2）建立退化方程，形式可以是d(Param)/dt = f(T, E, H, ...)的微分方程；
（3）设定失效阈值（failure threshold），当退化变量达到阈值时即判为失效；
（4）通过解析解或蒙特卡洛仿真得到寿命分布。

5.5.1 Al-cap的ESR退化PoF模型
Sankaran等（2010）给出了Al-cap的ESR退化模型：
""")
    add_formula(doc, "ESR(t) = ESR0 / (1 - α·t·exp(-Ea/kT))")
    add_body(doc, """
其中α为电解液蒸发速率常数。该式预测当t接近1/(α·exp(-Ea/kT))时ESR发散，对应电解液完全耗尽的失效时刻[27]。

5.5.2 MLCC的氧空位迁移PoF模型
Waser模型给出绝缘电阻演化：
""")
    add_formula(doc, "IR(t) = IR0 · exp(-k·t^n · E^m)")
    add_body(doc, """
阈值IR_critical与绝缘电阻下降两个数量级相对应。激活能Ea与Prokopowicz-Vaskas方程中的Ea一致[17]。

5.5.3 MPFC的自愈累积PoF模型
Makdessi模型给出容量演化：
""")
    add_formula(doc, "C(t) = C0·[1 - γ·N_sh(t)]")
    add_body(doc, """
其中N_sh(t)为累积自愈次数，γ为每次自愈的单位面积损失系数。寿命终点时N_sh达到临界值N_critical[34]。

5.5.4 钽电容的场致结晶PoF模型
DCL增长可建模为：
""")
    add_formula(doc, "DCL(t) = DCL0 + β·E²·t·exp(-Ea/kT)")
    add_body(doc, """
当DCL达到热失控临界值时发生灾难性失效[9][38]。

PoF模型的优势在于物理可解释性强、可跨工作点外推、可用于新型器件的早期寿命预测；局限在于需要较深入的机理理解与关键参数的独立测量，且对多机理共存情形的描述仍较为复杂。
""")

    add_heading_cn(doc, "5.6 数据驱动与物理-数据混合模型", level=2)
    add_body(doc, """
近年来，机器学习在电容器寿命预测中的应用取得了显著进展，代表性方法包括：
（1）BP神经网络：Lu等（2025）将Arrhenius加速试验与Icepak热仿真得到的生命数据作为输入，训练BP网络预测电容器与功率晶体管的寿命[13]；
（2）LSTM与CNN-LSTM：Soualhi等（2022）建立了考虑动态工况变化的Al-cap LSTM模型[45]；MDPI Electronics（2025）提出了考虑参数离散的CNN-LSTM模型，在SECU数据集上RUL预测的RMSE低至5%以内[15]；
（3）遗传算法-LSTM（GA-LSTM）：Su等（2024）基于IET数字图书馆，对超级电容的循环寿命进行了早期预测，在前20%循环数据即可完成有效预测[46]；
（4）Transformer与Attention模型：具有比LSTM更强的长时依赖建模能力，但训练数据要求更大；
（5）物理信息神经网络（PINN）：Nature子刊EurekAlert（2025）报道的超级电容PINN模型将SEI膜增厚的物理微分方程作为损失函数约束项，在小样本条件下预测精度显著优于纯数据方法[6]；
（6）AIP APL Machine Learning（2023）提出的物理约束机器学习方法，用于MLCC失效时间预测，将Prokopowicz-Vaskas方程嵌入神经网络的先验[14]。

数据驱动模型的优点包括：（i）无需显式机理假设；（ii）可容纳任意数量与类型的监测输入；（iii）具有端到端训练能力。其主要局限包括：（i）对训练数据量敏感；（ii）外推能力有限（易过拟合）；（iii）缺乏物理可解释性。

物理-数据混合模型是当前的最新发展方向，其核心思想是把物理模型（如PoF微分方程）作为神经网络的先验知识或损失函数的约束项，以期在小样本、多应力、长外推条件下仍保持可靠预测能力。PINN、残差网络混合模型（hybrid residual model）、物理正则化Transformer等都属于这一方向。
""")

    add_heading_cn(doc, "5.7 主要建模方法的比较", level=2)
    add_table_simple(
        doc,
        ["模型类别", "代表形式", "优势", "局限", "适用场景"],
        [
            ["统计Weibull", "两/三参数Weibull", "简单通用", "无物理机理", "初步寿命估计"],
            ["Arrhenius", "exp(Ea/kT)", "成熟可靠", "单一温度应力", "温度主导失效"],
            ["Prokopowicz-Vaskas", "Arrhenius+逆幂律", "MLCC行业标准", "多应力交互不足", "MLCC寿命外推"],
            ["广义Eyring", "多应力耦合", "可描述交互", "参数多、试验贵", "复杂工况"],
            ["PoF物理模型", "退化微分方程", "可解释、可外推", "需机理认识", "机理清楚场合"],
            ["BP/LSTM/CNN", "神经网络", "灵活强大", "外推性差", "大样本监测数据"],
            ["PINN/混合模型", "物理+数据", "小样本、可外推", "设计复杂", "高可靠场景"],
        ],
        caption="表5-1  主要电容器可靠性建模方法比较"
    )
    add_page_break(doc)
