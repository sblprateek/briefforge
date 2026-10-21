"""
BriefForge Visual Packaging Diff & Remediation Matrix
Generates comprehensive panel-by-panel before-and-after audit diffs between original artwork and remediated brief.
"""

from typing import List, Dict, Any


def get_packaging_diff_matrix() -> List[Dict[str, str]]:
    """Returns side-by-side comparison of original artwork defects vs remediated specifications for all 12 defects."""
    return [
        {
            "panel": "Top Tuck Flap",
            "before_artwork": "Prominent 'NO ADDED SUGAR' callout badge printed across flap fold line.",
            "after_remediated": "Badge completely purged from printable separation layers.",
            "regulatory_driver": "FDA 21 CFR 101.60(c)(2) — Prohibits claim when recipe contains added honey and coconut sugar.",
            "severity": "CRITICAL"
        },
        {
            "panel": "Front PDP",
            "before_artwork": "Net Quantity missing or misplaced in uncertified upper margin area.",
            "after_remediated": "Mandatory 'NET WT 16.9 OZ (480g)' positioned in lower 30% of PDP in bold, compliant type.",
            "regulatory_driver": "FDA 21 CFR 101.7 / Fair Packaging and Labeling Act (FPLA).",
            "severity": "CRITICAL"
        },
        {
            "panel": "Front PDP & Back",
            "before_artwork": "Cereal bowl photography depicts fresh strawberries and blueberries with no disclaimer.",
            "after_remediated": "Prominent disclaimer added: 'Serving Suggestion. Fresh fruit not included.'",
            "regulatory_driver": "FTC Deceptive Advertising Guidelines / FDA Truth in Food Labeling.",
            "severity": "WARNING"
        },
        {
            "panel": "Front PDP & Back",
            "before_artwork": "'Certified Vegan' (vegan.org) logo displayed on PDP and story panel.",
            "after_remediated": "Vegan mark deleted; updated to compliant claim: 'Suitable for Vegetarians'.",
            "regulatory_driver": "Vegan Action Certification Standards / Bee honey is an animal-derived product.",
            "severity": "CRITICAL"
        },
        {
            "panel": "Left Panel (Nutrition)",
            "before_artwork": "Outdated panel format declaring 0g Added Sugars despite caloric sweeteners in recipe.",
            "after_remediated": "FDA 2016 vertical standard based on 60g serving size (8 servings), declaring true Added Sugars.",
            "regulatory_driver": "FDA 21 CFR 101.9 Mandatory Nutrition Labeling Revision.",
            "severity": "CRITICAL"
        },
        {
            "panel": "Left Panel (Nutrition)",
            "before_artwork": "Typographical error in key nutrient line: 'DIETRAY FIBER'.",
            "after_remediated": "Corrected typography to statutory standard: 'DIETARY FIBER'.",
            "regulatory_driver": "FDA 21 CFR 101.9(c)(6)(i) Mandatory Nutrient Nomenclature.",
            "severity": "CRITICAL"
        },
        {
            "panel": "Left Panel (Nutrition)",
            "before_artwork": "Unverified serving size and mathematical ambiguity on 480g total pack net weight.",
            "after_remediated": "Standardized 60g serving size (exactly 8 servings per 480g container) via Genesis R&D calculation.",
            "regulatory_driver": "FDA Reference Amount Customarily Consumed (RACC) for Granola / Ready-to-Eat Cereals.",
            "severity": "WARNING"
        },
        {
            "panel": "Back Panel (Recipe)",
            "before_artwork": "Discrepancy: PDF shows Honey (1%) with Walnuts and Flax; Excel shows Honey (9%) with no Walnuts.",
            "after_remediated": "Authorized Master Formulation Deck locked: 79% Oats, Walnuts, Pecans, Almonds, 1% Honey, Coconut Sugar.",
            "regulatory_driver": "FDA 21 CFR 101.4 Ingredients in Descending Order of Predominance.",
            "severity": "CRITICAL"
        },
        {
            "panel": "Back Panel (Allergens)",
            "before_artwork": "Allergens grouped under weak advisory phrasing: 'May Contain Almonds, May Contain Pecans'.",
            "after_remediated": "Elevated to bold standard: 'CONTAINS: ALMONDS, PECANS, WALNUTS. MAY CONTAIN: BRAZIL NUTS, OTHER TREE NUTS, WHEAT.'",
            "regulatory_driver": "FALCPA 21 U.S.C. 343(w) / FASTER Act Tree Nut Standards.",
            "severity": "CRITICAL"
        },
        {
            "panel": "Back Panel (Lozenges)",
            "before_artwork": "European/UK front-of-pack color-coded Reference Intake traffic light lozenges printed on back.",
            "after_remediated": "All EU/UK traffic-light lozenges purged to maintain strict US FDA single-format standard.",
            "regulatory_driver": "FDA 21 CFR 101 / US retail single-format standard.",
            "severity": "WARNING"
        },
        {
            "panel": "Right Panel (Specs)",
            "before_artwork": "Typographical error in recycling callout badge: 'RECYCABLE PAPERBOARD'.",
            "after_remediated": "Corrected typography to 'RECYCLABLE PAPERBOARD' matching How2Recycle guidelines.",
            "regulatory_driver": "Packaging Pre-Press Quality Standard & How2Recycle Label Guidelines.",
            "severity": "WARNING"
        },
        {
            "panel": "Artwork Mechanicals",
            "before_artwork": "Non-printing dieline guide text ('Front panel Orientation', 'Copy free', 'Dieline - Do Not Print') present in art layers.",
            "after_remediated": "Purged from all CMYK and spot separation channels; moved to dedicated non-printing dieline layer.",
            "regulatory_driver": "Pre-Press Plate Separation Hygiene (prevents expensive plate ruins and cylinder re-engraving).",
            "severity": "CRITICAL"
        }
    ]
