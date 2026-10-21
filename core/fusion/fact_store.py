"""
BriefForge Fact Store & Provenance Registry
Manages atomic facts extracted from diverse packaging sources, tracking exact source file,
panel location, extraction confidence, and audit trail.
"""

from dataclasses import dataclass, field as dc_field
from typing import Dict, Any, List, Optional, Tuple
import json


@dataclass
class ExtractedFact:
    """A single atomic unit of product or packaging specification."""
    field: str                  # Canonical schema key (e.g., 'brand', 'ingredient_deck')
    value: Any                  # Extracted value (string, dict, or list)
    source_file: str            # Origin filename
    source_type: str            # 'pdf_artwork' | 'excel_content_sheet' | 'word_doc' | 'image' | 'user_input'
    source_location: str        # e.g., 'Front Panel PDP', 'Row 26 Cell B26'
    confidence: float = 0.95    # 0.0 - 1.0 confidence score
    category: str = "general"   # 'identity', 'structural', 'regulatory', 'creative'
    notes: str = ""             # Dieline overlap warnings, OCR notes, etc.

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "value": self.value,
            "source_file": self.source_file,
            "source_type": self.source_type,
            "source_location": self.source_location,
            "confidence": self.confidence,
            "category": self.category,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ExtractedFact":
        return cls(**d)


@dataclass
class ValidationIssue:
    """A compliance defect, conflict, gap, or typography issue."""
    issue_id: str
    title: str
    severity: str               # 'CRITICAL' | 'WARNING' | 'INFO'
    issue_type: str             # 'regulatory_violation' | 'conflict' | 'missing' | 'typo'
    description: str
    affected_fields: List[str]
    regulation: str = ""
    remediation: str = ""
    resolved: bool = False
    resolution: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "severity": self.severity,
            "issue_type": self.issue_type,
            "description": self.description,
            "affected_fields": self.affected_fields,
            "regulation": self.regulation,
            "remediation": self.remediation,
            "resolved": self.resolved,
            "resolution": self.resolution
        }


@dataclass
class SmartQuestion:
    """A targeted follow-up question presented to brand or packaging manager."""
    question_id: str
    priority: str               # 'critical' | 'warning' | 'info'
    question_text: str
    context: str
    options: List[Dict[str, str]] = dc_field(default_factory=list)  # [{"label": "...", "value": "..."}]
    related_issues: List[str] = dc_field(default_factory=list)
    default_value: str = ""
    answer: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "priority": self.priority,
            "question_text": self.question_text,
            "context": self.context,
            "options": self.options,
            "related_issues": self.related_issues,
            "default_value": self.default_value,
            "answer": self.answer
        }


class FactStore:
    """Central repository storing all multi-source facts, issues, and resolutions."""

    def __init__(self):
        self.facts: List[ExtractedFact] = []
        self.issues: List[ValidationIssue] = []
        self.questions: List[SmartQuestion] = []
        self.user_answers: Dict[str, str] = {}

    def add_facts(self, facts: List[ExtractedFact]):
        for f in facts:
            self.facts.append(f)

    def add_issue(self, issue: ValidationIssue):
        # Prevent exact duplicate issue IDs
        if not any(i.issue_id == issue.issue_id for i in self.issues):
            self.issues.append(issue)

    def add_question(self, question: SmartQuestion):
        if not any(q.question_id == question.question_id for q in self.questions):
            self.questions.append(question)

    def resolve_issue(self, issue_id: str, resolution: str):
        for i in self.issues:
            if i.issue_id == issue_id:
                i.resolved = True
                i.resolution = resolution

    def answer_question(self, question_id: str, answer: str):
        for q in self.questions:
            if q.question_id == question_id:
                q.answer = answer
                break

    def apply_user_answer(self, field: str, value: str, notes: str = ""):
        self.user_answers[field] = value
        # Insert high-confidence user override fact
        override_fact = ExtractedFact(
            field=field,
            value=value,
            source_file="Brand Manager Input",
            source_type="user_input",
            source_location="Direct Q&A Session",
            confidence=1.0,
            notes=notes or "Confirmed by user in interactive session"
        )
        self.facts.append(override_fact)

    def get_facts_for_field(self, field: str) -> List[ExtractedFact]:
        return [f for f in self.facts if f.field == field]

    def get_best_fact(self, field: str) -> Optional[ExtractedFact]:
        field_facts = self.get_facts_for_field(field)
        if not field_facts:
            return None
        # User input always has highest priority
        user_facts = [f for f in field_facts if f.source_type == "user_input"]
        if user_facts:
            return user_facts[-1]
        # Otherwise sort by confidence
        return max(field_facts, key=lambda f: f.confidence)

    def get_unified_facts(self) -> Dict[str, Any]:
        """Returns consolidated key-value mapping with provenance summaries."""
        fields = set(f.field for f in self.facts)
        unified = {}
        for fld in fields:
            best = self.get_best_fact(fld)
            if best:
                unified[fld] = best.value
        return unified

    def get_citation_for_field(self, field: str) -> str:
        """Constructs Esko-grade source citation badge string."""
        facts = self.get_facts_for_field(field)
        if not facts:
            return "Unverified"
        
        has_user = any(f.source_type == "user_input" for f in facts)
        has_pdf = any("pdf" in f.source_type for f in facts)
        has_excel = any("excel" in f.source_type for f in facts)
        
        parts = []
        if has_pdf:
            pdf_locs = [f.source_location for f in facts if "pdf" in f.source_type]
            loc_str = pdf_locs[0] if pdf_locs else "Artwork Dieline"
            parts.append(f"Carton PDF ({loc_str})")
        if has_excel:
            xl_locs = [f.source_location for f in facts if "excel" in f.source_type]
            loc_str = xl_locs[0] if xl_locs else "Content Sheet"
            parts.append(f"Content Sheet Excel ({loc_str})")
        if has_user:
            parts.append("Confirmed by Brand Manager")
            
        return " + ".join(parts) if parts else "Carton PDF & Content Sheet"

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_facts": len(self.facts),
            "distinct_fields": len(set(f.field for f in self.facts)),
            "total_issues": len(self.issues),
            "unresolved_issues": sum(1 for i in self.issues if not i.resolved),
            "critical_issues": sum(1 for i in self.issues if i.severity == "CRITICAL"),
            "warning_issues": sum(1 for i in self.issues if i.severity == "WARNING"),
            "total_questions": len(self.questions),
            "answered_questions": sum(1 for q in self.questions if q.answer)
        }
