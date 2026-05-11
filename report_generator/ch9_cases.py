# -*- coding: utf-8 -*-
"""附录 A：典型工程案例分析"""
from build_report import add_heading_cn, add_body, add_page_break, add_table_simple, add_formula


def build_appendix_cases(doc):
    add_heading_cn(doc, "附录A  典型工程案例分析", level=1)

    add_body(doc, """
本附录选取了电力电子、航空航天、电动汽车、轨道交通、通信基站等典型领域中五个具有代表性的电容器失效案例，按照"背景→现象→失效分析→机理判定→改进措施"五段式结构开展案例分析，以便读者将报告中阐述的原理与工程实践相互印证。
""")

    add_heading_cn(doc, "A.1 案例一：变频器直流母线铝电解电容器大批量失效", level=2)
    add_heading_cn(doc, "A.1.1 背景与现象", level=3)
    add_body(doc, """
某工业用通用变频器在沿海高温高湿地区运行3年后出现批量性故障，故障率显著高于同型产品在华北内陆地区的故障率。整机失效的主要表现为：输出电压纹波超标、IGBT模块过电流跳闸，最终直流母线过压报警。现场拆机发现，故障产品的直流母线Al-cap普遍出现壳体顶部鼓包，部分电容防爆阀已开启并有电解液结晶渗出。
""")
    add_heading_cn(doc, "A.1.2 失效分析", level=3)
    add_body(doc, """
对故障电容进行拆解与成分分析，发现：
（1）电解液质量较初始值减少了约35%~42%，电解液中有色的氧化物沉淀显著增多；
（2）阳极箔表面化成膜出现点状缺陷，SEM图可观察到直径5~20 μm的点蚀坑；
（3）阴极箔几乎已"干涸"，与电解纸黏连；
（4）密封橡胶塞表面出现氧化硬化龟裂。
""")
    add_heading_cn(doc, "A.1.3 机理判定", level=3)
    add_body(doc, """
结合现场工况（环境温度长期35~40℃、空气中盐雾与潮气富集、变频器机箱设计散热不佳使内部温度进一步升至55~65℃）与拆解数据，判定主导失效机理为：
（1）电解液溶剂蒸发加速——现场温度比设计工况高约15℃，依据Arrhenius激活能0.94 eV估算，蒸发速率上升约4.0倍[23][28]；
（2）密封胶塞在高温高湿下加速老化，进一步加剧溶剂散逸；
（3）海盐气溶胶中的Cl⁻离子渗入电容器内部催化Al2O3氧化膜点蚀，直接诱发介质局部击穿；
（4）击穿-再化成循环释放的H2、O2气体累积使内压上升，最终触发防爆阀开启。
""")
    add_heading_cn(doc, "A.1.4 改进措施", level=3)
    add_body(doc, """
（1）变频器内部布局优化，将Al-cap从IGBT模块正上方迁移至下方，降低热辐射影响；机箱加装强制风道使Al-cap壳体温度下降约10℃；
（2）将通用级Al-cap（105℃/2000 h）替换为高寿命型（105℃/10000 h）与长寿型车规级产品；
（3）对沿海与热带地区出厂产品采用增强密封规格（双道橡胶塞+环氧灌封）；
（4）部署简易监测系统，周期性测量Al-cap的ESR，当ESR升至初值2倍时发出预警。
上述措施在随后的跟踪中，沿海地区的故障率下降约一个数量级。
""")

    add_heading_cn(doc, "A.2 案例二：汽车ECU板上MLCC的PCB弯曲裂纹失效", level=2)
    add_heading_cn(doc, "A.2.1 背景与现象", level=3)
    add_body(doc, """
某车型的发动机ECU在量产初期出现偶发性整机不工作故障，返厂统计显示故障率为每千台约0.5~0.8只。对失效板卡进行X射线与C-SAM检测，发现故障板上至少一只1210/1812尺寸的MLCC出现贯穿性裂纹短路，裂纹起始于端电极-陶瓷体交界处，沿45°方向向对角延伸至内电极区。
""")
    add_heading_cn(doc, "A.2.2 失效分析", level=3)
    add_body(doc, """
对故障板的装配工艺做系统追溯，发现故障集中发生在某批次使用了较硬的PCB固定螺钉扭矩（由1.2 N·m增加至1.8 N·m）的装配工艺。通过应变片在线测量装配过程中的PCB应变，发现MLCC所在区域的瞬时弯曲应变峰值可达1200~1500 μstrain，已进入1210尺寸X7R MLCC的flex crack敏感区（典型阈值约1000 μstrain）[25][26]。
""")
    add_heading_cn(doc, "A.2.3 机理判定", level=3)
    add_body(doc, """
判定失效机理为：
（1）装配过程中的PCB弯曲应变超过MLCC flex crack阈值，陶瓷本体在端电极-陶瓷交界处（应力集中区）起裂；
（2）热循环与振动应力使裂纹稳步扩展至内电极区；
（3）裂纹通道内渗入湿气，电化学迁移使阴阳电极短路[30][31]。
""")
    add_heading_cn(doc, "A.2.4 改进措施", level=3)
    add_body(doc, """
（1）将1210与1812尺寸MLCC替换为采用软端电极工艺的同规格产品，flex crack阈值提升至2500 μstrain以上；
（2）修改PCB布局，将大尺寸MLCC迁移出螺钉安装孔附近与分板V-cut区域，至少保持5 mm安全距离；
（3）优化螺钉装配扭矩规程，采用扭矩可控的电动螺丝刀配合二阶段拧紧；
（4）在PCB设计审查流程中引入"flex-crack risk checklist"，强制要求1210及以上MLCC进行板级应变仿真。
改进后故障率下降至可忽略水平（<1 ppm）。
""")

    add_heading_cn(doc, "A.3 案例三：电动汽车逆变器DC-link薄膜电容的过热退化", level=2)
    add_heading_cn(doc, "A.3.1 背景与现象", level=3)
    add_body(doc, """
某款电动汽车主驱逆变器在累计里程10万km后，部分车辆反映动力输出异常与间歇性电机抖动。售后部门的OBD日志显示逆变器DC-link电容的实时监测值ESR已上升至初始值的180%~220%，容量下降了5%~8%。
""")
    add_heading_cn(doc, "A.3.2 失效分析", level=3)
    add_body(doc, """
对返修件做切片分析，发现BOPP薄膜局部出现发黄、喷金层与膜界面出现微裂纹。测试其离线阻抗谱，可见中频段ESR明显上升，低频段容量在DC偏置下偏离较多。热成像分析发现车辆在高负荷工况下，电容本体表面温度可达95~102℃，而产品规格最高工作温度为105℃。
""")
    add_heading_cn(doc, "A.3.3 机理判定", level=3)
    add_body(doc, """
主导机理为热应力与电应力耦合下的BOPP薄膜氧化老化与喷金层腐蚀[36][37]：
（1）高温下BOPP主链断裂与侧基氧化，介质损耗上升，反过来使自发热加剧；
（2）喷金层（Zn/Sn）在高温潮气下发生电偶腐蚀，接触电阻上升；
（3）自愈事件逐步累积，容量进一步下降；
（4）单体间的温度不均引起容量/ESR离散度增大，最终逆变器控制系统判断参数超出允许区间。
""")
    add_heading_cn(doc, "A.3.4 改进措施", level=3)
    add_body(doc, """
（1）将DC-link电容模块改为液冷集成式，使电容壳体温度峰值控制在85℃以下；
（2）升级薄膜材料至110℃额定的纳米复合BOPP；
（3）端面喷金由常规Zn升级为Zn/Sn合金多层喷涂，提升湿度耐受；
（4）在VCU软件层增加电容温度监测与降功率保护逻辑，防止极端工况下过温；
（5）厂内量产件100%老炼+纹波电流测试。
跟踪结果表明，售后故障率明显改善，10万km故障率降低约一个量级。
""")

    add_heading_cn(doc, "A.4 案例四：航天电源模块钽电容的浪涌着火", level=2)
    add_heading_cn(doc, "A.4.1 背景与现象", level=3)
    add_body(doc, """
某卫星电源模块在入轨后第108小时出现功率母线瞬时断电，地面遥测数据显示电流在毫秒内剧增后迅速下降至零。冗余切换机构启动后恢复供电。后续对备份地面工程样机的系统级复现测试中，发现同批次的10V/100μF固体钽电容器在承受数百毫秒的瞬态过压时发生着火。
""")
    add_heading_cn(doc, "A.4.2 失效分析", level=3)
    add_body(doc, """
对故障件做切片与SEM/EDS分析，发现Ta阳极表面Ta2O5介质在靠近阴极的数十个区域存在明显的结晶区域（β-Ta2O5晶粒直径约1~3 μm）；故障后壳体内部MnO2已全部碳化，钽阳极已形成熔化迹象，证实了钽的燃烧[2][9][10][39]。
""")
    add_heading_cn(doc, "A.4.3 机理判定", level=3)
    add_body(doc, """
判定机理为典型的"场致结晶+浪涌热失控"：
（1）入轨前地面测试阶段Ta2O5介质已积累一定结晶区；
（2）入轨后主电源瞬态尖峰（约1.6倍额定电压）叠加温度波动，使漏电流呈非线性上升；
（3）局部焦耳热升至MnO2还原温度(450℃)以上，但浪涌能量过大，MnO2自愈已来不及发挥作用；
（4）Ta与O发生放热反应，形成着火。
""")
    add_heading_cn(doc, "A.4.4 改进措施", level=3)
    add_body(doc, """
（1）在卫星电源母线前端增加浪涌抑制电路（TVS+串联电阻+后级电感）；
（2）钽电容工作电压降额从60%降至50%以下；
（3）选用F-Tech工艺的钽电容（早期失效率低一个量级）[10]；
（4）关键母线改用MnO2阴极+聚合物阴极的"混合型"钽电容，同时满足ESR与安全性需求；
（5）出厂前100%做三次浪涌测试（3SCT）筛选。
该改进方案已在后续的三颗卫星中得到验证，未再出现类似事件。
""")

    add_heading_cn(doc, "A.5 案例五：储能系统超级电容模组的容量早衰", level=2)
    add_heading_cn(doc, "A.5.1 背景与现象", level=3)
    add_body(doc, """
某风电变桨备用电源采用48V/165F超级电容模组作为应急储能。投入使用约2年后，冬季低温启动时可用能量明显不足，经检测模组总容量已从165F下降至120F（下降27%），ESR从16 mΩ上升至30 mΩ（上升87%）。
""")
    add_heading_cn(doc, "A.5.2 失效分析", level=3)
    add_body(doc, """
对单体做离线测试，发现模组内单体容量离散度较投运前明显扩大：最高单体容量约2980 F、最低仅约2440 F。离线阻抗谱显示所有单体在低频段的等效电荷转移电阻Rct均增加2~3倍；X射线无鼓包现象，拆解未见明显漏液。活性炭极片表征发现其BET比表面积由2050 m²/g下降至约1720 m²/g。
""")
    add_heading_cn(doc, "A.5.3 机理判定", level=3)
    add_body(doc, """
判定为多机理协同作用[11][22][42][43]：
（1）模组内因温度分布不均，局部单体长期工作温度偏高5~8℃，加速有机电解液分解；
（2）活性炭的微孔在电压电化学应力下部分塌陷，有效比表面积下降；
（3）集流体Al箔在电解液中含微量水分下发生腐蚀，界面电阻上升；
（4）由于无主动均衡电路，高压单体长期处于过压边缘，进一步加速局部老化。
""")
    add_heading_cn(doc, "A.5.4 改进措施", level=3)
    add_body(doc, """
（1）模组内增加主动均衡管理单元（BMS），实时监测每个单体电压并主动均衡；
（2）升级活性炭材料至经过表面处理的高比表面积活性炭（2200 m²/g），并使用镀碳铝箔集流体；
（3）优化模组散热结构，改善内部温度均匀性；
（4）部署基于CNN-LSTM的健康监测算法[15][45]，对每个单体的ΔC/ΔESR做趋势预测，按需更换高龄单体。
改进后同类型系统10年循环寿命的预测置信度大幅提升，年均运维成本下降约30%。
""")
    add_page_break(doc)


def build_appendix_symbols(doc):
    add_heading_cn(doc, "附录B  符号与缩略语表", level=1)
    rows = [
        ("C", "电容量", "单位 F（法拉）"),
        ("ESR", "等效串联电阻", "Equivalent Series Resistance"),
        ("ESL", "等效串联电感", "Equivalent Series Inductance"),
        ("IR", "绝缘电阻", "Insulation Resistance"),
        ("LC/DCL", "漏电流", "Leakage Current / DC Leakage"),
        ("tanδ", "损耗因数", "Dissipation Factor"),
        ("fSR", "自谐振频率", "Self-Resonant Frequency"),
        ("Ea", "激活能", "Activation Energy, eV"),
        ("k", "玻尔兹曼常数", "8.617×10⁻⁵ eV/K"),
        ("β", "Weibull形状参数", "Shape Parameter"),
        ("η", "Weibull尺度参数", "Scale Parameter"),
        ("AF", "加速因子", "Acceleration Factor"),
        ("MTTF", "平均失效时间", "Mean Time To Failure"),
        ("MTBF", "平均故障间隔时间", "Mean Time Between Failures"),
        ("FIT", "单位时间失效数", "Failures in Time, per 10⁹ h"),
        ("ALT", "加速寿命试验", "Accelerated Life Test"),
        ("HALT", "高加速寿命试验", "Highly Accelerated Life Test"),
        ("HAST", "高加速应力试验", "Highly Accelerated Stress Test"),
        ("THB", "高温高湿偏压", "Temperature Humidity Bias"),
        ("HTOL", "高温工作寿命", "High Temperature Operating Life"),
        ("DPA", "破坏性物理分析", "Destructive Physical Analysis"),
        ("RUL", "剩余使用寿命", "Remaining Useful Life"),
        ("PHM", "预测与健康管理", "Prognostics and Health Management"),
        ("PoF", "失效物理", "Physics of Failure"),
        ("PINN", "物理信息神经网络", "Physics-Informed Neural Network"),
        ("BME", "贱金属电极", "Base Metal Electrode"),
        ("PME", "贵金属电极", "Precious Metal Electrode"),
        ("MLCC", "多层陶瓷电容器", "Multi-Layer Ceramic Capacitor"),
        ("MPFC", "金属化聚合物薄膜电容", "Metallized Polymer Film Capacitor"),
        ("EDLC", "双电层电容器", "Electric Double-Layer Capacitor"),
        ("BOPP", "双向拉伸聚丙烯", "Biaxially Oriented Polypropylene"),
        ("CSAM", "声学扫描显微镜", "C-Mode Scanning Acoustic Microscope"),
        ("DC-link", "直流母线", "Direct-Current Link"),
        ("Mission Profile", "任务剖面", "实际工况下的电-热-机械-时间曲线"),
    ]
    add_table_simple(
        doc,
        ["符号/缩略语", "中文含义", "英文/说明"],
        rows,
        caption="表B-1  报告中主要符号与缩略语对照"
    )
    add_page_break(doc)
