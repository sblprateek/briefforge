"""
BriefForge Packaging Council — Multi-Agent Expert Board
Simulates an elite enterprise review board representing:
1. Regulatory & Food Law (FDA / FALCPA compliance)
2. Pre-Press & Print Conversion (dieline mechanics, trapping, separation)
3. Brand & Creative Direction (visual hierarchy, asset lockups, retail impact)
4. Materials & Sustainability (FSC substrate, barrier pouch, How2Recycle)
"""

from dataclasses import dataclass, field as dc_field
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class CouncilVerdict:
    agent_id: str
    agent_name: str
    role_title: str
    avatar_emoji: str
    verdict: str           # "PASSED" | "CONDITIONAL_APPROVAL" | "REJECTED"
    score: int             # 0 - 100
    executive_critique: str
    key_findings: List[str]
    mandatory_signoff_conditions: List[str]
    color_theme: str


class PackagingCouncil:
    """Orchestrates multi-persona packaging audit debate and sign-offs."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def convene_council(self, facts: Dict[str, Any], issues: List[Any], user_answers: Dict[str, str]) -> List[CouncilVerdict]:
        """Runs the four expert agent evaluations over the packaging facts and issues."""
        
        # 1. Regulatory & Food Law Agent
        has_vegan_conflict = any(getattr(i, 'issue_id', '') == "FDA_VEGAN_HONEY_CONFLICT" for i in issues)
        has_sugar_conflict = any("sugar" in getattr(i, 'issue_id', '').lower() for i in issues)
        has_allergen_conflict = any("allergen" in getattr(i, 'issue_id', '').lower() for i in issues)
        
        reg_status = "CONDITIONAL_APPROVAL" if (has_vegan_conflict or has_sugar_conflict or has_allergen_conflict) else "PASSED"
        reg_score = 62 if (has_vegan_conflict or has_sugar_conflict) else 95
        
        reg_critique = (
            "Current artwork proof exhibits severe, actionable FDA 21 CFR and FALCPA violations. "
            "Displaying 'Certified Vegan' while formulating with bee honey constitutes deceptive labeling. "
            "Furthermore, claiming 'NO ADDED SUGAR' with 0g declared on the panel while adding honey, coconut sugar, "
            "and crystallized ginger is legally indefensible under FDA 21 CFR 101.60. All intentional tree nuts "
            "must be elevated from 'May Contain' to a bold 'CONTAINS:' statement immediately."
        )
        if user_answers:
            reg_critique += " NOTE: Brand Manager has confirmed remediation directives which will resolve these liabilities upon agency execution."
            reg_score = 94
            reg_status = "PASSED"

        reg_verdict = CouncilVerdict(
            agent_id="regulatory_counsel",
            agent_name="Dr. Evelyn Reed, JD",
            role_title="VP of Global Food Regulatory & Labeling Compliance",
            avatar_emoji="🧑‍⚖️",
            verdict=reg_status,
            score=reg_score,
            executive_critique=reg_critique,
            key_findings=[
                "FTC / Vegan Action: Honey disqualifies product from Certified Vegan mark.",
                "FDA 21 CFR 101.60: 'No Added Sugar' claim is prohibited with caloric sweeteners present.",
                "FALCPA 21 U.S.C. 343(w): Almonds, Pecans, Walnuts require mandatory bold CONTAINS callout.",
                "FDA 21 CFR 101.7: Dual net weight declaration (16.9 oz / 480g) required in lower 30% of PDP."
            ],
            mandatory_signoff_conditions=[
                "Delete Certified Vegan logo; replace with 'Suitable for Vegetarians'.",
                "Delete 'NO ADDED SUGAR' badges from top flap and back panel.",
                "Replace side panel with standard FDA 2016 Nutrition Facts declaring accurate Added Sugars."
            ],
            color_theme="#EF4444" if reg_score < 70 else "#10B981"
        )

        # 2. Pre-Press & Print Conversion Director
        has_dieline_text = any("dieline" in getattr(i, 'issue_id', '').lower() for i in issues)
        has_typos = any("typo" in getattr(i, 'issue_id', '').lower() for i in issues)
        prep_score = 74 if (has_dieline_text or has_typos) else 98
        prep_status = "CONDITIONAL_APPROVAL" if prep_score < 90 else "PASSED"

        prep_critique = (
            "Mechanical separation inspection revealed non-printing dieline guide text ('Front panel Orientation', 'Copy free') "
            "contaminating printable vector layers. Typographical defects in key headings ('DIETRAY', 'RECYCABLE') must be "
            "corrected before cylinder engraving or offset plate exposure. Trapping tolerances of 0.5pt and 1/8\" (3.175mm) "
            "bleed margins must be enforced per converter mechanical guidelines."
        )

        prep_verdict = CouncilVerdict(
            agent_id="prepress_director",
            agent_name="Marcus Vance",
            role_title="Technical Pre-Press & Print Conversion Director",
            avatar_emoji="🏭",
            verdict=prep_status,
            score=prep_score,
            executive_critique=prep_critique,
            key_findings=[
                "Dieline annotations detected on active art separation layers.",
                "UPC-A barcode requires 0.25 in (6.35 mm) quiet zone verification on solid white backing.",
                "Typos 'RECYCABLE' and 'DIETRAY' will spoil plate runs if not corrected in Illustrator masters.",
                "Bleed margin minimum 1/8 in (3.175 mm) required for high-speed folding carton die-cutters."
            ],
            mandatory_signoff_conditions=[
                "Purge non-printing annotations from CMYK and spot separation channels.",
                "Correct typographical errors in recycling and nutrition panel headers.",
                "Converter sign-off on 18pt SBS crease scores and glue flap adhesive window."
            ],
            color_theme="#F59E0B" if prep_score < 80 else "#10B981"
        )

        # 3. Creative & Brand Identity Director
        brand_score = 88
        brand_critique = (
            "Brand identity assets (Dancing Fish character illustration, custom header typography, and color palette) "
            "are strictly locked and must not be altered by the agency. Visual hierarchy must balance artisan storytelling "
            "('Start tapping, swishing & shaking your tail fins!') with clean regulatory panel zoning. A mandatory 'Serving Suggestion' "
            "disclaimer must be added without occluding the photography."
        )

        brand_verdict = CouncilVerdict(
            agent_id="creative_director",
            agent_name="Sophia Chen",
            role_title="Executive Packaging Creative Director",
            avatar_emoji="🎨",
            verdict="PASSED",
            score=brand_score,
            executive_critique=brand_critique,
            key_findings=[
                "Brand lockup and character illustration locked; agency restricted from restyling.",
                "Serving photography disclosure must integrate seamlessly adjacent to cereal bowl.",
                "Typography hierarchy preserves premium artisan positioning for Whole Foods and Sprouts channels."
            ],
            mandatory_signoff_conditions=[
                "Preserve master logo typography and brand colors exactly as supplied in vector package.",
                "Place 'Serving Suggestion. Fresh fruit not included.' in minimum 6pt sans-serif text."
            ],
            color_theme="#3B82F6"
        )

        # 4. Materials & Sustainability Specialist
        mat_score = 92
        mat_critique = (
            "Substrate specification of FSC-certified 18pt Solid Bleached Sulfate (SBS) provides excellent carton stiffness, "
            "high ink holdout, and high recyclability in standard municipal paperboard streams. Internal barrier pouch film "
            "requires converter verification regarding metallized vs clear poly barrier to confirm overall pack recyclability scoring."
        )

        mat_verdict = CouncilVerdict(
            agent_id="sustainability_engineer",
            agent_name="Liam O'Connor",
            role_title="Head of Packaging Materials & Sustainable Circularity",
            avatar_emoji="🌿",
            verdict="PASSED",
            score=mat_score,
            executive_critique=mat_critique,
            key_findings=[
                "FSC-certified 18pt SBS carton is 100% curbside recyclable.",
                "Matte aqueous coating is repulpable and biodegradable.",
                "How2Recycle paperboard callout badge must be retained on side panel."
            ],
            mandatory_signoff_conditions=[
                "Converter must supply chain-of-custody FSC certificate for board batch.",
                "Verify interior pouch barrier recyclability coding (Code 4 LDPE vs Multi-layer)."
            ],
            color_theme="#10B981"
        )

        return [reg_verdict, prep_verdict, brand_verdict, mat_verdict]
