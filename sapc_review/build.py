# -*- coding: utf-8 -*-
"""主入口：组装全部章节，生成 Word 综述 (SAPC)"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx import Document
from docx_utils import configure_page
from chapters_part1 import build_cover, build_abstract, build_toc, build_chapter1, build_chapter2
from chapters_part2 import build_chapter3, build_chapter4
from chapters_part3 import build_chapter5, build_chapter6
from chapters_part4 import build_chapter7, build_chapter8, build_conclusion, build_references


def main():
    doc = Document()
    configure_page(doc)

    # 默认样式
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    from docx.oxml.ns import qn
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    build_cover(doc)
    build_abstract(doc)
    build_toc(doc)
    build_chapter1(doc)
    build_chapter2(doc)
    build_chapter3(doc)
    build_chapter4(doc)
    build_chapter5(doc)
    build_chapter6(doc)
    build_chapter7(doc)
    build_chapter8(doc)
    build_conclusion(doc)
    build_references(doc)

    out = os.path.join(HERE, "..", "叠层铝固态聚合物电容器学术综述.docx")
    out = os.path.abspath(out)
    doc.save(out)
    print("Saved:", out)
    size = os.path.getsize(out) / 1024
    print(f"Size: {size:.1f} KB")


if __name__ == "__main__":
    main()
