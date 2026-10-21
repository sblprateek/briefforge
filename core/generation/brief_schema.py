"""
BriefForge Brief Document Data Models
Represents the structured, production-ready packaging brief with complete provenance and compliance metadata.
"""

from dataclasses import dataclass, field as dc_field
from typing import List, Dict, Any, Optional


@dataclass
class BriefField:
    """A verified attribute inside a brief section."""
    label: str                  # Display attribute name (e.g., 'Brand', 'Substrate & Caliper')
    value: str                  # Verified specification text
    source: str                 # Traceability badge citation
    confidence: float = 0.98    # Confidence score (0.0 - 1.0)
    compliance: str = "pass"    # 'pass' | 'fail' | 'warning' | 'pending'
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "value": self.value,
            "source": self.source,
            "confidence": self.confidence,
            "compliance": self.compliance,
            "notes": self.notes
        }


@dataclass
class BriefSection:
    """A major grouped section of the brief."""
    title: str
    section_id: str
    fields: List[BriefField] = dc_field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "section_id": self.section_id,
            "fields": [f.to_dict() for f in self.fields]
        }


@dataclass
class CorrectionItem:
    """Actionable pre-press and artwork remediation checklist item."""
    description: str
    severity: str = "CRITICAL"
    completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "severity": self.severity,
            "completed": self.completed
        }


@dataclass
class ComplianceAuditItem:
    """An audited regulatory rule result."""
    rule_id: str
    rule_name: str
    status: str                 # 'pass' | 'fail' | 'warning'
    description: str
    regulation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "status": self.status,
            "description": self.description,
            "regulation": self.regulation
        }


@dataclass
class ConflictResolutionItem:
    """Documenting resolved discrepancies between input sources."""
    field: str
    source_a: str
    value_a: str
    source_b: str
    value_b: str
    resolution: str
    resolved_by: str = "Brand Manager"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "source_a": self.source_a,
            "value_a": self.value_a,
            "source_b": self.source_b,
            "value_b": self.value_b,
            "resolution": self.resolution,
            "resolved_by": self.resolved_by
        }


@dataclass
class OpenQuestion:
    """Technical open questions for converter or packaging design agency."""
    question: str
    context: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "context": self.context
        }


@dataclass
class BriefDocument:
    """The master BriefForge packaging design brief."""
    title: str
    generated_date: str
    executive_summary: str
    sections: List[BriefSection] = dc_field(default_factory=list)
    corrections: List[CorrectionItem] = dc_field(default_factory=list)
    compliance_audit: List[ComplianceAuditItem] = dc_field(default_factory=list)
    conflict_log: List[ConflictResolutionItem] = dc_field(default_factory=list)
    open_questions: List[OpenQuestion] = dc_field(default_factory=list)
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_title": self.title,
            "generated_date": self.generated_date,
            "executive_summary": self.executive_summary,
            "sections": [s.to_dict() for s in self.sections],
            "typography_and_print_corrections": [c.description for c in self.corrections],
            "compliance_audit": [a.to_dict() for a in self.compliance_audit],
            "conflict_log": [c.to_dict() for c in self.conflict_log],
            "open_questions_for_agency": [q.question for q in self.open_questions],
            "metadata": self.metadata
        }
