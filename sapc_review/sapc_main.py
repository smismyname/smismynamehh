# -*- coding: utf-8 -*-
"""
主入口：生成图表 -> 组装全部章节 -> 输出 Word 文档
叠层铝固态电容器（SAPC，导电聚合物 PEDOT 阴极）失效模式与失效机理国内外研究现状综述
组织主线：器件结构与材料体系 -> 失效模式 -> 失效机理（仅此三模块）
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sapc_figures
from sapc_common import new_document, build_cover, add_toc_field
from sapc_front import build_abstract, build_glossary
from sapc_ch1 import build_chapter1
from sapc_ch2 import build_chapter2
from sapc_ch3 import build_chapter3
from sapc_ch4 import build_chapter4
from sapc_ch5 import build_chapter5
from sapc_ch6 import build_chapter6
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
        title_lines=["叠层铝固态电容器（SAPC）", "失效模式与失效机理"],
        subtitle_en="Failure Modes and Failure Mechanisms of Stacked Aluminum Polymer\n"
                    "Capacitors (SAPC, Conductive-Polymer / PEDOT Cathode):\n"
                    "A Review of Domestic and International Research Status",
        meta=[
            ("报 告 类 型", "博士论文·国内外研究现状专题综述"),
            ("主    线", "叠层铝固态电容器 SAPC（PEDOT 阴极）"),
            ("对 照 对 象", "液态铝电解 / MLCC(BME) / 金属化薄膜 / 固体钽"),
            ("组 织 主 线", "器件 — 失效模式 — 失效机理"),
            ("研 究 领 域", "电子元器件可靠性·失效物理"),
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
    build_references(doc)

    out_path = os.path.abspath(os.path.join(
        here, "..", "叠层铝固态电容器SAPC_失效模式与失效机理_国内外研究现状综述.docx"))
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
