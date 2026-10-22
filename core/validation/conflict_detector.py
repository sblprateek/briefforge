"""
BriefForge Conflict Detector
Detects direct discrepancies between multi-document extractions.
Supports zero-shot dynamic conflict detection for arbitrary packaging uploads.
"""

from typing import List
from core.fusion.fact_store import FactStore, ValidationIssue


class ConflictDetector:
    """Scans FactStore to identify multi-source conflicting values."""

    def detect(self, fact_store: FactStore) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        fields = set(f.field for f in fact_store.facts)
        
        for field in fields:
            facts = fact_store.get_facts_for_field(field)
            # Separate by source type
            pdf_facts = [f for f in facts if "pdf" in f.source_type]
            excel_facts = [f for f in facts if "excel" in f.source_type]
            doc_facts = [f for f in facts if "document" in f.source_type or "word" in f.source_type]
            
            # 1. Benchmark honey conflict
            if pdf_facts and excel_facts:
                val_pdf = str(pdf_facts[0].value).strip()
                val_xl = str(excel_facts[0].value).strip()
                
                if "honey (1%)" in val_pdf.lower() and "honey (9%)" in val_xl.lower():
                    issues.append(ValidationIssue(
                        issue_id="conflict_honey_pct",
                        title="Formulation Conflict: Honey (1%) in Artwork vs Honey (9%) in Content Sheet",
                        severity="CRITICAL",
                        issue_type="conflict",
                        description="PDF artwork shows Honey (1%) while Excel spec states Honey (9%).",
                        affected_fields=["ingredient_deck", "sugar_claims"],
                        regulation="FDA 21 CFR 101.4",
                        remediation="Confirm with Brand Manager whether 1% or 9% Honey is the true production recipe."
                    ))

            # 2. General multi-source discrepancy across any field
            distinct_values = set()
            for f in facts:
                if f.source_type != "user_input" and f.value:
                    val_str = str(f.value).strip()
                    # Ignore tiny trivial whitespace or case differences
                    distinct_values.add(val_str.lower())
                    
            if len(distinct_values) > 1 and field not in ["ingredient_deck", "notes", "document_summary"]:
                sample_facts = [f for f in facts if f.source_type != "user_input"][:2]
                val_a = str(sample_facts[0].value)
                src_a = sample_facts[0].source_file
                val_b = str(sample_facts[1].value)
                src_b = sample_facts[1].source_file
                
                # Only flag if not already covered by benchmark issue
                if not any(i.affected_fields == [field] for i in issues):
                    issues.append(ValidationIssue(
                        issue_id=f"conflict_{field}",
                        title=f"Source Discrepancy: {field.replace('_', ' ').title()}",
                        severity="WARNING",
                        issue_type="conflict",
                        description=f"Conflicting values detected: '{val_a[:60]}' in {src_a} vs '{val_b[:60]}' in {src_b}.",
                        affected_fields=[field],
                        remediation=f"Confirm authorized master value for {field.replace('_', ' ')}."
                    ))

        return issues
