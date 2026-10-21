"""
BriefForge Regulatory Compliance Engine
Executes deterministic FDA 21 CFR and FALCPA audits over the fact repository.
"""

from typing import List
from core.fusion.fact_store import FactStore, ValidationIssue
from config.regulatory_rules import evaluate_rules


class ComplianceEngine:
    """Evaluates packaging facts against codified food labeling regulations."""

    def validate(self, fact_store: FactStore) -> List[ValidationIssue]:
        unified = fact_store.get_unified_facts()
        raw_violations = evaluate_rules(unified)
        
        issues = []
        for v in raw_violations:
            issues.append(ValidationIssue(
                issue_id=v["rule_id"],
                title=v["title"],
                severity=v["severity"],
                issue_type="regulatory_violation",
                description=v["description"],
                affected_fields=v.get("affected_fields", []),
                regulation=v.get("regulation", ""),
                remediation=v.get("remediation", "")
            ))
            
        return issues
