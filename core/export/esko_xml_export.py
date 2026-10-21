"""
BriefForge Esko Automation Engine & DeskPack XML Exporter
Generates industry-standard JDF/XML packaging job ticket metadata for Esko WebCenter and Automation Engine.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from core.generation.brief_schema import BriefDocument


class EskoXMLExporter:
    """Exports machine-readable Esko Packaging Job Ticket XML."""

    def export(self, brief: BriefDocument) -> str:
        root = ET.Element("EskoPackagingJobTicket", {
            "version": "2.4",
            "generator": "BriefForge AI Studio",
            "schema": "Esko-WebCenter-Brief-v2"
        })

        # Header
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "JobTitle").text = brief.title
        ET.SubElement(header, "CreationDate").text = brief.generated_date
        ET.SubElement(header, "Brand").text = brief.metadata.get("brand", "Dancing Fish")
        ET.SubElement(header, "SKU").text = brief.metadata.get("sku", "DF-GRAN-BERRY-US-001")
        ET.SubElement(header, "ComplianceStatus").text = brief.metadata.get("compliance_status", "FULLY COMPLIANT")

        # Executive Summary
        ET.SubElement(root, "ExecutiveSummary").text = brief.executive_summary

        # Specifications
        specs = ET.SubElement(root, "Specifications")
        for s in brief.sections:
            sec_el = ET.SubElement(specs, "Section", {"id": s.section_id, "title": s.title})
            for f in s.fields:
                field_el = ET.SubElement(sec_el, "Field", {"label": f.label, "confidence": str(f.confidence)})
                ET.SubElement(field_el, "Value").text = f.value
                ET.SubElement(field_el, "SourceCitation").text = f.source

        # Pre-Press Corrections
        corrections = ET.SubElement(root, "PrePressRemediations")
        for c in brief.corrections:
            ET.SubElement(corrections, "Correction", {"severity": c.severity, "completed": str(c.completed)}).text = c.description

        # Open Agency Inquiries
        questions = ET.SubElement(root, "AgencyOpenQuestions")
        for q in brief.open_questions:
            ET.SubElement(questions, "Question").text = q.question

        # Format pretty XML
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def save(self, brief: BriefDocument, output_path: str):
        content = self.export(brief)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
