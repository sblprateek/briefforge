"""
BriefForge Pipeline Orchestrator — World-Class Architecture
Coordinates the 6-stage pipeline: Ingest → Fuse → Validate → Council Audit → Question → Generate → Handover
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List

from core.fusion.fact_store import FactStore, ExtractedFact
from core.ingestion.pdf_extractor import PDFExtractor
from core.ingestion.excel_extractor import ExcelExtractor
from core.ingestion.docx_extractor import DocxExtractor
from core.ingestion.image_extractor import ImageExtractor
from core.fusion.cross_reference import CrossReferenceEngine
from core.validation.compliance_engine import ComplianceEngine
from core.validation.conflict_detector import ConflictDetector
from core.validation.gap_analyzer import GapAnalyzer
from core.questioning.question_generator import QuestionGenerator
from core.generation.brief_composer import BriefComposer
from core.generation.brief_schema import BriefDocument
from core.council.packaging_council import PackagingCouncil, CouncilVerdict
from core.analytics.readiness_engine import ReadinessEngine
from core.visual.dieline_viewer import render_interactive_dieline
from core.visual.carton_3d_viewer import render_3d_carton_html
from core.visual.diff_engine import get_packaging_diff_matrix
from core.validation.jurisdiction_engine import compare_jurisdictions
from core.export.docx_export import DocxExporter
from core.export.esko_xml_export import EskoXMLExporter

logger = logging.getLogger(__name__)

EXTRACTOR_MAP = {
    ".pdf": ("pdf_artwork", PDFExtractor),
    ".xlsx": ("excel_content_sheet", ExcelExtractor),
    ".xls": ("excel_content_sheet", ExcelExtractor),
    ".docx": ("word_document", DocxExtractor),
    ".doc": ("word_document", DocxExtractor),
    ".jpg": ("image", ImageExtractor),
    ".jpeg": ("image", ImageExtractor),
    ".png": ("image", ImageExtractor),
    ".bmp": ("image", ImageExtractor),
    ".tiff": ("image", ImageExtractor),
    ".txt": ("text_document", DocxExtractor),
    ".md": ("text_document", DocxExtractor),
}


class BriefForgePipeline:
    """Enterprise-grade packaging intelligence pipeline."""
    
    def __init__(self):
        self.fact_store = FactStore()
        self.cross_ref_engine = CrossReferenceEngine()
        self.compliance_engine = ComplianceEngine()
        self.conflict_detector = ConflictDetector()
        self.gap_analyzer = GapAnalyzer()
        self.question_generator = QuestionGenerator()
        self.brief_composer = BriefComposer()
        self.council = PackagingCouncil()
        self.docx_exporter = DocxExporter()
        self.xml_exporter = EskoXMLExporter()
        
        self._ingested_files: List[str] = []
        self._stage: str = "init"
        self._extraction_log: List[Dict[str, Any]] = []
        self._council_verdicts: List[CouncilVerdict] = []
        
    @property
    def stage(self) -> str:
        return self._stage
    
    @property
    def ingested_files(self) -> List[str]:
        return self._ingested_files.copy()

    @property
    def council_verdicts(self) -> List[CouncilVerdict]:
        return self._council_verdicts

    # Stage 1: Document Ingestion
    def ingest_file(self, file_path: str, progress_callback=None) -> List[ExtractedFact]:
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext not in EXTRACTOR_MAP:
            logger.warning(f"Unsupported file type: {ext} for {path.name}")
            return []
        
        source_type, extractor_class = EXTRACTOR_MAP[ext]
        log_entry = {
            "file": path.name,
            "type": source_type,
            "status": "extracting",
            "facts_count": 0,
            "errors": []
        }
        
        try:
            if progress_callback:
                progress_callback(f"📄 Extracting from {path.name}...")
            
            extractor = extractor_class()
            facts = extractor.extract(str(path))
            self.fact_store.add_facts(facts)
            self._ingested_files.append(path.name)
            log_entry["status"] = "complete"
            log_entry["facts_count"] = len(facts)
        except Exception as e:
            log_entry["status"] = "error"
            log_entry["errors"].append(str(e))
            facts = []
            
        self._extraction_log.append(log_entry)
        return facts

    # Stage 2-3: Analysis & Compliance Audit
    def analyze(self, progress_callback=None) -> Dict[str, Any]:
        if progress_callback:
            progress_callback("🔍 Cross-referencing multi-document facts...")
        
        # Cross reference & conflicts
        cross_issues = self.cross_ref_engine.analyze(self.fact_store)
        for i in cross_issues:
            self.fact_store.add_issue(i)

        conflict_issues = self.conflict_detector.detect(self.fact_store)
        for i in conflict_issues:
            self.fact_store.add_issue(i)

        gap_issues = self.gap_analyzer.analyze(self.fact_store)
        for i in gap_issues:
            self.fact_store.add_issue(i)

        comp_issues = self.compliance_engine.validate(self.fact_store)
        for i in comp_issues:
            self.fact_store.add_issue(i)

        # Run Packaging Council Multi-Agent Audit
        unified = self.fact_store.get_unified_facts()
        self._council_verdicts = self.council.convene_council(
            facts=unified,
            issues=self.fact_store.issues,
            user_answers=self.fact_store.user_answers
        )

        self._stage = "analyzed"
        return {
            "total_issues": len(self.fact_store.issues),
            "by_severity": {
                "CRITICAL": sum(1 for i in self.fact_store.issues if i.severity == "CRITICAL"),
                "WARNING": sum(1 for i in self.fact_store.issues if i.severity == "WARNING"),
                "INFO": sum(1 for i in self.fact_store.issues if i.severity == "INFO")
            }
        }

    # Stage 4: Smart Questions
    def get_questions(self) -> List[Any]:
        questions = self.question_generator.generate(self.fact_store.issues, self.fact_store)
        for q in questions:
            self.fact_store.add_question(q)
        self._stage = "questioned"
        return questions

    def answer_question(self, question_id: str, answer: str):
        self.fact_store.answer_question(question_id, answer)
        self.fact_store.apply_user_answer(field=question_id, value=answer, notes="Confirmed by Brand Manager")
        
        # Re-convene council with updated answers
        self._council_verdicts = self.council.convene_council(
            facts=self.fact_store.get_unified_facts(),
            issues=self.fact_store.issues,
            user_answers=self.fact_store.user_answers
        )

    # Stage 5: Master Brief Generation
    def generate_brief(self, progress_callback=None) -> BriefDocument:
        brief = self.brief_composer.compose(self.fact_store)
        self._stage = "generated"
        return brief

    # Stage 6: Multi-Format Export
    def export(self, brief: BriefDocument, fmt: str = "markdown") -> Any:
        from core.export.markdown_export import MarkdownExporter
        from core.export.html_export import HTMLExporter
        from core.export.json_export import JSONExporter
        
        if fmt == "markdown":
            return MarkdownExporter().export(brief)
        elif fmt == "html":
            return HTMLExporter().export(brief)
        elif fmt == "json":
            return JSONExporter().export(brief)
        elif fmt == "xml":
            return self.xml_exporter.export(brief)
        elif fmt == "docx":
            # Generate docx bytes
            temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
            temp_docx.close()
            self.docx_exporter.export_to_file(brief, temp_docx.name)
            with open(temp_docx.name, "rb") as f:
                docx_bytes = f.read()
            try:
                os.remove(temp_docx.name)
            except Exception:
                pass
            return docx_bytes
        else:
            raise ValueError(f"Unsupported export format: {fmt}")

    # Analytics & Visuals
    def get_readiness_scorecard(self) -> Dict[str, Any]:
        return ReadinessEngine.calculate_score(
            facts=self.fact_store.get_unified_facts(),
            issues=self.fact_store.issues,
            user_answers=self.fact_store.user_answers
        )

    def get_dieline_html(self) -> str:
        return render_interactive_dieline(self.fact_store.issues)

    def get_3d_carton_html(self) -> str:
        return render_3d_carton_html()

    def get_diff_matrix(self) -> List[Dict[str, str]]:
        return get_packaging_diff_matrix()

    def get_jurisdiction_guide(self, market: str = "US") -> Dict[str, Any]:
        return compare_jurisdictions(market)

    def get_stats(self) -> Dict[str, Any]:
        stats = self.fact_store.get_stats()
        stats["stage"] = self._stage
        stats["ingested_files"] = self._ingested_files
        return stats

    def reset(self):
        self.fact_store = FactStore()
        self._ingested_files = []
        self._stage = "init"
        self._extraction_log = []
        self._council_verdicts = []
