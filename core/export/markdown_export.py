"""
BriefForge Markdown Exporter
Renders standard agency-ready Markdown briefs with traceability badges, compliance audits, and correction checklists.
"""

from core.generation.brief_schema import BriefDocument


class MarkdownExporter:
    """Exports BriefDocument to clean, structured GitHub Flavored Markdown."""

    def export(self, brief: BriefDocument) -> str:
        lines = []
        lines.append(f"# 📦 Packaging Design Brief: {brief.title}\n")
        lines.append(f"**Generated:** {brief.generated_date} | **Powered by:** BriefForge AI • Esko Brief Studio Ready\n")
        lines.append(f"**Executive Summary:** {brief.executive_summary}\n")

        # Sections
        for section in brief.sections:
            lines.append(f"## {section.title}")
            lines.append("| Attribute | Verified Specification | Source Traceability |")
            lines.append("| :--- | :--- | :--- |")
            for field in section.fields:
                clean_val = field.value.replace("\n", " ")
                lines.append(f"| **{field.label}** | {clean_val} | `{field.source}` |")
            lines.append("")

        # Section 5: Mandatory Artwork & Pre-Press Corrections
        lines.append("## 5. Mandatory Artwork & Pre-Press Corrections")
        for item in brief.corrections:
            check_box = "[x]" if item.completed else "[ ]"
            lines.append(f"- {check_box} {item.description}")
        lines.append("")

        # Section 6: Open Questions for the Design Agency
        lines.append("## 6. Open Questions for the Design Agency")
        for q in brief.open_questions:
            lines.append(f"- ❓ {q.question}")
        lines.append("")

        # Section 7: Regulatory Compliance Audit
        if brief.compliance_audit:
            lines.append("## 7. Regulatory Compliance & Quality Audit")
            lines.append("| Rule / Regulation | Status | Finding & Remediation |")
            lines.append("| :--- | :--- | :--- |")
            for a in brief.compliance_audit:
                status_icon = "✅ Passed" if a.status == "pass" else "⚠️ Warning"
                lines.append(f"| **{a.rule_name}**<br>`{a.regulation}` | {status_icon} | {a.description} |")
            lines.append("")

        # Section 8: Conflict Resolution Log
        if brief.conflict_log:
            lines.append("## 8. Multi-Source Conflict Resolution Log")
            lines.append("| Attribute | Document A | Document B | Resolved Specification | Authority |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for c in brief.conflict_log:
                lines.append(f"| **{c.field}** | {c.source_a}: *{c.value_a}* | {c.source_b}: *{c.value_b}* | {c.resolution} | {c.resolved_by} |")
            lines.append("")

        return "\n".join(lines)
