# -*- coding: utf-8 -*-
"""
电容器失效模式、失效机理与可靠性建模学术报告生成器
Generator for: Capacitor Failure Modes, Mechanisms and Reliability Modeling
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_cn_font(run, font_name="宋体", size_pt=12, bold=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rpr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:ascii'), "Times New Roman")
    rFonts.set(qn('w:hAnsi'), "Times New Roman")


def add_page_break(doc):
    from docx.enum.text import WD_BREAK
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(WD_BREAK.PAGE)


def add_heading_cn(doc, text, level=1):
    """添加中文样式标题"""
    sizes = {0: 22, 1: 18, 2: 15, 3: 13, 4: 12}
    p = doc.add_paragraph()
    if level == 0:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_cn_font(run, font_name="黑体", size_pt=sizes.get(level, 12), bold=True)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    # 设置大纲级别，便于生成目录
    pPr = p._p.get_or_add_pPr()
    outlineLvl = OxmlElement('w:outlineLvl')
    outlineLvl.set(qn('w:val'), str(level))
    pPr.append(outlineLvl)
    return p


def add_body(doc, text, first_indent=True, size=11):
    """添加正文段落"""
    for para_text in text.strip().split('\n'):
        para_text = para_text.strip()
        if not para_text:
            continue
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if first_indent:
            p.paragraph_format.first_line_indent = Cm(0.74)  # 2 chars
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(para_text)
        set_cn_font(run, font_name="宋体", size_pt=size)


def add_formula(doc, text):
    """添加公式（居中、斜体说明）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_cn_font(run, font_name="Times New Roman", size_pt=11)


def add_table_simple(doc, headers, rows, caption=None):
    """添加三线表"""
    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(caption)
        set_cn_font(run, font_name="黑体", size_pt=10.5, bold=True)
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        set_cn_font(run, font_name="黑体", size_pt=10, bold=True)
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(val))
            set_cn_font(run, font_name="宋体", size_pt=10)
    # 添加上下边线
    tbl = table._tbl
    for border in ['top', 'bottom']:
        pass
    return table


def configure_page(doc):
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.75)


def add_page_number_footer(doc):
    section = doc.sections[0]
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = "PAGE"
    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar_begin)
    run._r.append(instrText)
    run._r.append(fldChar_end)
    set_cn_font(run, font_name="Times New Roman", size_pt=10)


def build_cover(doc):
    """封面"""
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("学  术  研  究  报  告")
    set_cn_font(run, font_name="黑体", size_pt=28, bold=True)
    doc.add_paragraph()
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("电容器失效模式、失效机理")
    set_cn_font(run, font_name="黑体", size_pt=22, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("与可靠性建模")
    set_cn_font(run, font_name="黑体", size_pt=22, bold=True)
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Failure Modes, Mechanisms and Reliability Modeling of Capacitors")
    set_cn_font(run, font_name="Times New Roman", size_pt=14, bold=False)
    run.italic = True
    for _ in range(6):
        doc.add_paragraph()
    labels = [
        ("报 告 类 型", "专题研究报告"),
        ("研 究 领 域", "电子元器件可靠性工程"),
        ("关 键 词", "电容器;失效模式;失效机理;可靠性建模;寿命预测"),
        ("完 成 时 间", "2026 年 5 月"),
    ]
    for k, v in labels:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"{k}：{v}")
        set_cn_font(run, font_name="宋体", size_pt=14)
    add_page_break(doc)


if __name__ == "__main__":
    print("framework OK")
