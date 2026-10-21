"""
BriefForge JSON Exporter
Exports machine-readable Esko-compatible traceability JSON documents.
"""

import json
from core.generation.brief_schema import BriefDocument


class JSONExporter:
    """Exports structured brief data mirroring Esko_Brief_Traceability.json schema."""

    def export(self, brief: BriefDocument) -> str:
        data = {
            "project_title": brief.title,
            "executive_summary": brief.executive_summary,
            "project_and_brand_overview": [],
            "structural_and_pack_specs": [],
            "mandatory_copy_and_regulatory": [],
            "visual_and_creative_direction": [],
            "typography_and_print_corrections": [c.description for c in brief.corrections],
            "open_questions_for_agency": [q.question for q in brief.open_questions],
            "compliance_audit": [a.to_dict() for a in brief.compliance_audit],
            "conflict_resolution_log": [c.to_dict() for c in brief.conflict_log]
        }

        # Map sections into legacy format keys
        for s in brief.sections:
            target_key = s.section_id
            if target_key in data:
                for f in s.fields:
                    data[target_key].append({
                        "label": f.label,
                        "value": f.value,
                        "source_citation": f.source
                    })

        return json.dumps(data, indent=2)

    def save(self, brief: BriefDocument, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.export(brief))
