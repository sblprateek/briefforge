"""
BriefForge Gap Analyzer
Compares extracted facts against BRIEF_SCHEMA to detect missing mandatory specifications.
"""

from typing import List
from core.fusion.fact_store import FactStore, ValidationIssue
from config.brief_schema import BRIEF_SCHEMA


class GapAnalyzer:
    """Verifies all mandatory brief attributes are accounted for before agency handover."""

    def analyze(self, fact_store: FactStore) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []
        unified = fact_store.get_unified_facts()
        
        for section_id, fields in BRIEF_SCHEMA.items():
            for field_name, spec in fields.items():
                if spec.get("required") and field_name not in unified:
                    issues.append(ValidationIssue(
                        issue_id=f"gap_missing_{field_name}",
                        title=f"Missing Mandatory Specification: {spec['label']}",
                        severity="CRITICAL" if spec.get("category") == "regulatory" else "WARNING",
                        issue_type="missing",
                        description=f"Field '{spec['label']}' is required for agency execution but was not found in any uploaded document.",
                        affected_fields=[field_name],
                        remediation=f"Request confirmation from Brand Manager for {spec['label']}."
                    ))

        # Check for Serving Size legibility
        nutr_facts = fact_store.get_facts_for_field("nutrition_facts_spec")
        if any("pending verification" in str(f.value).lower() or "illegible" in str(f.notes).lower() for f in nutr_facts):
            issues.append(ValidationIssue(
                issue_id="gap_serving_size_unclear",
                title="Serving Size Weight Not Clearly Legible in Dieline",
                severity="WARNING",
                issue_type="missing",
                description="Nutrition Facts panel states 8 servings per container, but gram serving size was obscured on dieline proof.",
                affected_fields=["nutrition_facts_spec"],
                regulation="FDA 21 CFR 101.9(b)",
                remediation="Confirm serving size is 60g (480g net / 8 servings = 60g per serving)."
            ))

        return issues
