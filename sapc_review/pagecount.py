# -*- coding: utf-8 -*-
"""
Approximate page-count estimator for the generated .docx (no LibreOffice available).

It walks the document body in order, estimating the vertical space consumed by
paragraphs (incl. inline images), tables and explicit page breaks, then divides by
the usable page height. This is an APPROXIMATION (typically within ~10-15% of Word's
rendering); Word usually renders slightly longer due to widow/orphan control and
table padding, so we treat the estimate as a lower-ish bound.
"""
import math
import sys
from docx import Document
from docx.oxml.ns import qn

PT_PER_CM = 28.3465
USABLE_H_CM = 29.7 - 2 * 2.54           # ~24.62 cm
USABLE_W_CM = 21.0 - 2 * 2.54           # ~15.92 cm
EMU_PER_CM = 360000


def _para_lines(text, size_pt, indent_chars=0):
    if not text:
        return 1
    # crude CJK vs ascii width: CJK char ~ size_pt, ascii ~ 0.5*size_pt (in pt)
    cjk = sum(1 for ch in text if ord(ch) > 0x2E80)
    ascii_like = len(text) - cjk
    width_pt = cjk * size_pt + ascii_like * size_pt * 0.55
    usable_w_pt = USABLE_W_CM * PT_PER_CM - indent_chars * size_pt
    return max(1, math.ceil(width_pt / max(usable_w_pt, 1)))


def _run_size(p):
    for r in p.runs:
        if r.font.size is not None:
            return r.font.size.pt
    return 12.0


def estimate(path):
    doc = Document(path)
    total_cm = 0.0
    pages_from_breaks = 0
    body = doc.element.body
    # map tables for quick lookup
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    def para_height(p_el):
        nonlocal pages_from_breaks
        p = Paragraph(p_el, doc)
        h = 0.0
        # explicit page break?
        brs = p_el.findall('.//' + qn('w:br'))
        for br in brs:
            if br.get(qn('w:type')) == 'page':
                pages_from_breaks += 1
        # inline image height
        cy_total = 0
        for ext in p_el.findall('.//' + qn('wp:extent')):
            cy = ext.get('cy')
            if cy:
                cy_total += int(cy)
        if cy_total:
            h += cy_total / EMU_PER_CM + 0.2
        # text
        size = _run_size(p)
        pf = p.paragraph_format
        ls = pf.line_spacing if pf.line_spacing else 1.5
        if isinstance(ls, float):
            line_h_cm = size * ls / PT_PER_CM
        else:
            line_h_cm = size * 1.2 / PT_PER_CM
        indent_chars = 0
        if pf.first_line_indent is not None:
            try:
                indent_chars = max(0, pf.first_line_indent.pt / size)
            except Exception:
                indent_chars = 0
        text = p.text
        nlines = _para_lines(text, size, indent_chars) if text else (0 if cy_total else 1)
        h += nlines * line_h_cm
        sa = pf.space_after.pt if pf.space_after is not None else 6
        sb = pf.space_before.pt if pf.space_before is not None else 0
        h += (sa + sb) / PT_PER_CM
        # heading styles add a bit
        if p.style and p.style.name and p.style.name.lower().startswith('heading'):
            h += 0.15
        return h

    def table_height(tbl_el):
        tbl = Table(tbl_el, doc)
        ncols = len(tbl.columns) if tbl.columns else 1
        col_w_cm = USABLE_W_CM / max(ncols, 1)
        h = 0.0
        for row in tbl.rows:
            max_lines = 1
            for cell in row.cells:
                txt = cell.text
                # chars per line in this cell at ~9pt
                size = 9.0
                cjk = sum(1 for ch in txt if ord(ch) > 0x2E80)
                ascii_like = len(txt) - cjk
                width_pt = cjk * size + ascii_like * size * 0.55
                usable = col_w_cm * PT_PER_CM
                lines = max(1, math.ceil(width_pt / max(usable, 1)))
                max_lines = max(max_lines, lines)
            row_h = max_lines * (9.0 * 1.25 / PT_PER_CM) + 0.18  # padding
            h += row_h
        return h

    for child in body.iterchildren():
        tag = child.tag
        if tag == qn('w:p'):
            total_cm += para_height(child)
        elif tag == qn('w:tbl'):
            total_cm += table_height(child)

    pages_text = total_cm / USABLE_H_CM
    # each explicit page break also tends to leave whitespace -> count as page boundary
    est = pages_text + pages_from_breaks * 0.5
    return {
        "content_cm": round(total_cm, 1),
        "pages_from_text_flow": round(pages_text, 1),
        "explicit_page_breaks": pages_from_breaks,
        "estimated_pages": round(est, 1),
    }


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "../SAPC可靠性研究现状_20260529.docx"
    import os
    p = os.path.join(os.path.dirname(__file__), p) if not os.path.isabs(p) else p
    info = estimate(p)
    for k, v in info.items():
        print(f"{k}: {v}")
