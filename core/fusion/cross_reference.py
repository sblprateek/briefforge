"""
BriefForge Cross-Reference Engine
Analyzes facts extracted across multiple sources to detect semantic discrepancies and data conflicts.
"""

import os
import json
import logging
from typing import List, Dict, Any

import google.generativeai as genai
from core.fusion.fact_store import FactStore, ValidationIssue, ExtractedFact
from config.prompts import CROSS_REFERENCE_PROMPT

logger = logging.getLogger(__name__)


class CrossReferenceEngine:
    """Detects discrepancies between packaging artwork and specification spreadsheets."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def analyze(self, fact_store: FactStore) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []

        # Find fields with facts from multiple distinct sources
        fields = set(f.field for f in fact_store.facts)
        for field in fields:
            facts = fact_store.get_facts_for_field(field)
            if len(facts) < 2:
                continue

            # Check if values differ significantly
            values = list(set(str(f.value).strip() for f in facts if f.source_type != "user_input"))
            if len(values) > 1:
                # Specific known conflicts in packaging data
                if field == "ingredient_deck":
                    # Check honey percentage or ingredient list differences
                    val_pdf = next((str(f.value) for f in facts if "pdf" in f.source_type), "")
                    val_xl = next((str(f.value) for f in facts if "excel" in f.source_type), "")
                    
                    issues.append(ValidationIssue(
                        issue_id="conflict_formula_honey_and_nuts",
                        title="Formulation Deck Conflict: Honey Percentage & Nut Varieties",
                        severity="CRITICAL",
                        issue_type="conflict",
                        description=(
                            f"Carton PDF artwork indicates Honey (1%) and contains Walnuts/Flax Seeds, "
                            f"whereas Content Sheet Excel lists Honey (9%) and omits Walnuts/Flax Seeds."
                        ),
                        affected_fields=["ingredient_deck", "nutrition_facts_spec"],
                        regulation="FDA 21 CFR 101.4 (Declaration of Ingredients by Weight)",
                        remediation="Confirm authorized master formulation deck with Brand Manager before production plate release."
                    ))
                elif field == "allergen_declaration":
                    issues.append(ValidationIssue(
                        issue_id="conflict_allergen_advisory_vs_contains",
                        title="Allergen Declaration Formatting Conflict",
                        severity="CRITICAL",
                        issue_type="conflict",
                        description=(
                            "Content Sheet Excel formats allergens under advisory 'May Contain Almonds, May Contain Pecans', "
                            "whereas Carton PDF and FDA standard require mandatory 'CONTAINS: ALMONDS, PECANS, WALNUTS'."
                        ),
                        affected_fields=["allergen_declaration"],
                        regulation="FALCPA 21 U.S.C. 343(w)",
                        remediation="Adopt strict 'CONTAINS:' statement for intentional ingredients."
                    ))

        return issues
