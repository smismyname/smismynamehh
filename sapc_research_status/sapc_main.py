# -*- coding: utf-8 -*-
"""
主入口：生成图表 -> 组装全部章节 -> 输出 Word 文档
叠层铝固态电容器（SAPC）国内外研究现状专题综述
组织主线：材料与结构—制备工艺—电气性能—失效模式—失效机理—可靠性建模—状态监测—应用需求
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sapc_figures
from sapc_common import (new_document, build_cover, add_toc_field, add_page_break)
from sapc_front import build_abstract, build_glossary
from sapc_ch1 import build_chapter1
from sapc_ch2 import build_chapter2
from sapc_ch3 import build_chapter3
from sapc_ch4 import build_chapter4
from sapc_ch5 import build_chapter5
from sapc_ch6 import build_chapter6
from sapc_ch7 import build_chapter7
from sapc_ch8 import build_chapter8
from sapc_ch9 import build_chapter9
from sapc_ch10 import build_chapter10
from sapc_ch11 import build_chapter11
from sapc_refs import build_references


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    figs_dir = os.path.join(here, "figs")

    print("[1/3] 生成图表 ...")
    FIGS = sapc_figures.generate_all(figs_dir)
    print("      已生成 %d 张图" % len(FIGS))

    print("[2/3] 组装文档 ...")
    doc = new_document()

    build_cover(
        doc,
        title_lines=["叠层铝固态电容器（SAPC）", "国内外研究现状"],
        subtitle_en="A Review of Research Status on Stacked Aluminium Solid Polymer Capacitors:\n"
                    "Materials & Structure - Process - Performance - Failure Mode - Mechanism - "
                    "Reliability Model - Condition Monitoring - Applications",
        meta=[
            ("报 告 类 型", "博士论文·国内外研究现状专题综述"),
            ("研 究 对 象", "叠层铝固态（导电高分子）电容器 SAPC / SP-Cap"),
            ("组 织 主 线", "材料结构—工艺—性能—失效模式—机理—建模—监测—应用"),
            ("研 究 领 域", "电子元器件可靠性工程"),
            ("完 成 时 间", "2026 年 5 月"),
        ],
    )

    build_abstract(doc)
    add_toc_field(doc)
    build_glossary(doc)

    build_chapter1(doc, FIGS)
    build_chapter2(doc, FIGS)
    build_chapter3(doc, FIGS)
    build_chapter4(doc, FIGS)
    build_chapter5(doc, FIGS)
    build_chapter6(doc, FIGS)
    build_chapter7(doc, FIGS)
    build_chapter8(doc, FIGS)
    build_chapter9(doc, FIGS)
    build_chapter10(doc, FIGS)
    build_chapter11(doc, FIGS)
    build_references(doc)

    out_path = os.path.abspath(os.path.join(
        here, "..", "叠层铝固态电容器SAPC_国内外研究现状.docx"))
    doc.save(out_path)
    print("[3/3] 已保存: %s" % out_path)
    try:
        kb = os.path.getsize(out_path) / 1024
        print("      文件大小: %.1f KB" % kb)
    except Exception:
        pass
    return out_path


if __name__ == "__main__":
    main()
