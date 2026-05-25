# -*- coding: utf-8 -*-
"""
专题报告生成器入口
《SAPC（叠层铝固态电容器）湿、热及热电耦合应力下
失效模式、机理与可靠性的国内外研究现状》
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.oxml.ns import qn
from build_report import configure_page, add_page_number_footer
from ch_research_status import (
    build_cover, build_abstract, build_toc,
    build_chapter1, build_chapter2, build_chapter3, build_chapter4,
    build_references,
)


def main():
    doc = Document()
    configure_page(doc)
    add_page_number_footer(doc)

    # Default font
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Document body
    build_cover(doc)
    build_abstract(doc)
    build_toc(doc)
    build_chapter1(doc)
    build_chapter2(doc)
    build_chapter3(doc)
    build_chapter4(doc)
    build_references(doc)

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "SAPC_叠层铝固态电容器_国内外研究现状.docx",
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
