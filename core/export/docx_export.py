"""
BriefForge Word (.docx) Exporter
Generates genuine Microsoft Word (.docx) briefs with styled tables, callout blocks,
and source traceability badges matching Esko_Packaging_Design_Brief.docx.
"""

from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from core.generation.brief_schema import BriefDocument


class DocxExporter:
    """Exports BriefDocument into a publication-grade Word document."""

    def export_to_file(self, brief: BriefDocument, output_path: str):
        doc = docx.Document()

        # Page margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.75)
            section.bottom_margin = Inches(0.75)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)

        # Brand Tag Header
        p_tag = doc.add_paragraph()
        p_tag.paragraph_format.space_after = Pt(2)
        run_tag = p_tag.add_run("PACKAGING POWERED BY ESKO • AI BRIEF STUDIO")
        run_tag.font.size = Pt(9)
        run_tag.font.bold = True
        run_tag.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

        # Title
        p_title = doc.add_paragraph()
        p_title.paragraph_format.space_after = Pt(4)
        run_title = p_title.add_run(brief.title)
        run_title.font.size = Pt(18)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        # Date & Meta
        p_meta = doc.add_paragraph()
        p_meta.paragraph_format.space_after = Pt(14)
        run_meta = p_meta.add_run(f"Prepared via BriefForge AI Packaging Studio  |  Date: {brief.generated_date}  |  Status: Approved for Agency Handover")
        run_meta.font.size = Pt(9.5)
        run_meta.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        # Executive Summary Box
        p_exec_head = doc.add_paragraph()
        p_exec_head.paragraph_format.space_after = Pt(2)
        run_eh = p_exec_head.add_run("Executive Summary")
        run_eh.font.size = Pt(12)
        run_eh.font.bold = True
        run_eh.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

        p_exec = doc.add_paragraph()
        p_exec.paragraph_format.space_after = Pt(16)
        run_exec = p_exec.add_run(brief.executive_summary)
        run_exec.font.size = Pt(10)
        run_exec.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        # Sections & Tables
        for s_idx, section in enumerate(brief.sections):
            p_sec = doc.add_paragraph()
            p_sec.paragraph_format.space_before = Pt(14)
            p_sec.paragraph_format.space_after = Pt(6)
            run_sec = p_sec.add_run(section.title)
            run_sec.font.size = Pt(13)
            run_sec.font.bold = True
            run_sec.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

            # Create Table: Attribute | Verified Agency Specification | Source Traceability
            table = doc.add_table(rows=1, cols=3)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False

            # Column widths
            widths = [Inches(1.8), Inches(3.4), Inches(1.8)]
            hdr_cells = table.rows[0].cells
            hdr_titles = ["Packaging Attribute", "Verified Agency Specification", "Source Traceability"]
            for idx, text in enumerate(hdr_titles):
                hdr_cells[idx].text = text
                hdr_cells[idx].width = widths[idx]
                p = hdr_cells[idx].paragraphs[0]
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(9)
                p.runs[0].font.color.rgb = RGBColor(0x47, 0x55, 0x69)
                # Background shading
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
                hdr_cells[idx]._tc.get_or_add_tcPr().append(shading)

            for field in section.fields:
                row_cells = table.add_row().cells
                row_cells[0].width = widths[0]
                row_cells[1].width = widths[1]
                row_cells[2].width = widths[2]

                # Attribute
                row_cells[0].text = field.label
                p0 = row_cells[0].paragraphs[0]
                p0.runs[0].font.bold = True
                p0.runs[0].font.size = Pt(9.5)
                p0.runs[0].font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

                # Specification
                row_cells[1].text = field.value
                p1 = row_cells[1].paragraphs[0]
                p1.runs[0].font.size = Pt(9)
                p1.runs[0].font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

                # Traceability
                row_cells[2].text = f"📌 {field.source}"
                p2 = row_cells[2].paragraphs[0]
                p2.runs[0].font.size = Pt(8.5)
                p2.runs[0].font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

        # 5. Mandatory Pre-Press & Artwork Corrections
        p_c_head = doc.add_paragraph()
        p_c_head.paragraph_format.space_before = Pt(16)
        p_c_head.paragraph_format.space_after = Pt(6)
        run_ch = p_c_head.add_run("5. Mandatory Pre-Press & Artwork Corrections Checklist")
        run_ch.font.size = Pt(13)
        run_ch.font.bold = True
        run_ch.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

        for item in brief.corrections:
            p_item = doc.add_paragraph(style='List Bullet')
            p_item.paragraph_format.space_after = Pt(3)
            run_item = p_item.add_run(f"☐  {item.description}")
            run_item.font.size = Pt(9.5)
            run_item.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        # 6. Open Questions for Agency
        p_q_head = doc.add_paragraph()
        p_q_head.paragraph_format.space_before = Pt(16)
        p_q_head.paragraph_format.space_after = Pt(6)
        run_qh = p_q_head.add_run("6. Open Questions for the Design Agency & Converter")
        run_qh.font.size = Pt(13)
        run_qh.font.bold = True
        run_qh.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

        for q in brief.open_questions:
            p_q = doc.add_paragraph(style='List Bullet')
            p_q.paragraph_format.space_after = Pt(4)
            run_q = p_q.add_run(f"❓  {q.question}")
            run_q.font.size = Pt(9.5)
            run_q.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        # Save document
        doc.save(output_path)
