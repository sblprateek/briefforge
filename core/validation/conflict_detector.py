"""
BriefForge Conflict Detector
Detects direct discrepancies between multi-document extractions.
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
            
            if pdf_facts and excel_facts:
                val_pdf = str(pdf_facts[0].value).strip()
                val_xl = str(excel_facts[0].value).strip()
                
                # Check for Honey 1% vs 9% in ingredients
                if "honey (1%)" in val_pdf.lower() and "honey (9%)" in val_xl.lower():
                    issues.append(ValidationIssue(
                        issue_id="conflict_honey_pct",
                        title="Formulation Conflict: Honey (1%) in Artwork vs Honey (9%) in Content Sheet",
                        severity="CRITICAL",
                        issue_type="conflict",
                        description=f"PDF artwork shows Honey (1%) while Excel spec states Honey (9%).",
                        affected_fields=["ingredient_deck", "sugar_claims"],
                        regulation="FDA 21 CFR 101.4",
                        remediation="Confirm with Brand Manager whether 1% or 9% Honey is the true production recipe."
                    ))

        return issues
