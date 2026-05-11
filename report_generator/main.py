# -*- coding: utf-8 -*-
"""
主入口：组装全部章节，生成 Word 报告
"""
import os
import sys
from docx import Document

# 确保能够 import 本目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_report import (
    configure_page,
    build_cover,
    add_page_number_footer,
)
from ch0_front import build_abstract, build_toc
from ch1_intro import build_chapter1
from ch2_classification import build_chapter2
from ch3_modes import build_chapter3
from ch4_mechanisms import build_chapter4
from ch5_modeling import build_chapter5
from ch6_monitoring import build_chapter6
from ch7_improvement import build_chapter7
from ch8_conclusion import build_chapter8, build_references
from ch9_cases import build_appendix_cases, build_appendix_symbols
from ch_supp import build_supplement


def main():
    doc = Document()
    configure_page(doc)
    add_page_number_footer(doc)

    # 设置默认 Normal 样式字体
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    from docx.oxml.ns import qn
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # ------- 封面 -------
    build_cover(doc)

    # ------- 摘要 -------
    build_abstract(doc)

    # ------- 目录 -------
    build_toc(doc)

    # ------- 正文 -------
    build_chapter1(doc)
    build_chapter2(doc)
    build_chapter3(doc)
    build_chapter4(doc)
    build_chapter5(doc)
    build_chapter6(doc)
    build_chapter7(doc)
    build_chapter8(doc)

    # ------- 附录 -------
    build_appendix_cases(doc)
    build_supplement(doc)
    build_appendix_symbols(doc)

    # ------- 参考文献 -------
    build_references(doc)

    # 保存
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "电容器失效模式_失效机理_与可靠性建模_学术报告.docx",
    )
    out_path = os.path.abspath(out_path)
    doc.save(out_path)
    print(f"Saved: {out_path}")
    try:
        size_kb = os.path.getsize(out_path) / 1024
        print(f"Size: {size_kb:.1f} KB")
    except Exception:
        pass


if __name__ == "__main__":
    main()
