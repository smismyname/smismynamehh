# -*- coding: utf-8 -*-
"""
主入口：生成图表 -> 组装全部章节 -> 输出 Word 文档
电容器可靠性国内外研究现状专题综述（按 器件—失效模式—失效机理—可靠性建模—状态监测 主线）
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rs_figures
from rs_common import (new_document, build_cover, add_toc_field, add_page_break)
from rs_front import build_abstract, build_glossary
from rs_ch1 import build_chapter1
from rs_ch2 import build_chapter2
from rs_ch3 import build_chapter3
from rs_ch4 import build_chapter4
from rs_ch5 import build_chapter5
from rs_ch6 import build_chapter6
from rs_ch_app import build_chapter_app
from rs_ch7 import build_chapter7
from rs_ch8 import build_chapter8
from rs_refs import build_references


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    figs_dir = os.path.join(here, "figs")

    print("[1/3] 生成图表 ...")
    FIGS = rs_figures.generate_all(figs_dir)
    print("      已生成 %d 张图" % len(FIGS))

    print("[2/3] 组装文档 ...")
    doc = new_document()

    build_cover(
        doc,
        title_lines=["电容器失效与可靠性", "国内外研究现状"],
        subtitle_en="A Review of Research Status on Capacitor Failure and Reliability:\n"
                    "Device - Failure Mode - Mechanism - Reliability Model - Condition Monitoring",
        meta=[
            ("报 告 类 型", "博士论文·国内外研究现状专题综述"),
            ("组 织 主 线", "器件—失效模式—失效机理—可靠性建模—状态监测"),
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
    build_chapter_app(doc, FIGS)
    build_chapter7(doc, FIGS)
    build_chapter8(doc, FIGS)
    build_references(doc)

    out_path = os.path.abspath(os.path.join(
        here, "..", "电容器可靠性_国内外研究现状_专题综述.docx"))
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
