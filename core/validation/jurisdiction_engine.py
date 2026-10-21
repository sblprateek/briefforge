"""
BriefForge Global Regulatory Jurisdiction Engine
Compares packaging requirements across US (FDA), European Union / UK (EU 1169/2011), and Canada (CFIA).
"""

from typing import Dict, Any, List


JURISDICTION_STANDARDS = {
    "US": {
        "title": "United States (FDA 21 CFR / FALCPA / FASTER)",
        "net_weight_format": "Dual Declaration Mandatory: NET WT 16.9 OZ (480g) in bottom 30% of PDP.",
        "allergen_rules": "Mandatory 'CONTAINS: [ALLERGENS]' callout or bolded in-ingredient naming.",
        "front_of_pack_lozenges": "Prohibited / Unrecognized. Strip all UK/EU traffic-light circles.",
        "sugar_claims": "Under 21 CFR 101.60, 'No Added Sugar' illegal if formulation contains caloric sweeteners (honey, coconut sugar).",
        "nutrition_panel": "FDA 2016 Vertical format with mandatory Added Sugars line and 2,000 calorie footnote."
    },
    "EU_UK": {
        "title": "European Union & United Kingdom (EU No 1169/2011 / Natasha's Law)",
        "net_weight_format": "Metric only: 480 g ℮ with EEC estimated sign.",
        "allergen_rules": "Allergens MUST be highlighted (e.g. bolded) strictly inside the ingredient deck. Separate 'Contains' box is prohibited under EU guidance.",
        "front_of_pack_lozenges": "Permitted. Reference Intake (RI) color-coded nutrition lozenges encouraged.",
        "sugar_claims": "Regulated under EU Regulation 1924/2006 on nutrition and health claims.",
        "nutrition_panel": "Per 100g mandatory table; per serving optional."
    },
    "CANADA": {
        "title": "Canada (Health Canada / Canadian Food Inspection Agency - CFIA)",
        "net_weight_format": "Metric primary: 480 g (net weight in both official languages).",
        "allergen_rules": "Bilingual mandatory: 'Contains: Almonds, Pecans / Contient : Amandes, Pacanes'.",
        "front_of_pack_lozenges": "New Canadian FOP Nutrition symbol mandatory for products high in saturated fat, sugars, or sodium.",
        "sugar_claims": "Health Canada Food and Drug Regulations.",
        "nutrition_panel": "Strictly bilingual English/French Nutrition Facts table (Valeur nutritive)."
    }
}


def compare_jurisdictions(market: str = "US") -> Dict[str, Any]:
    """Returns comparative packaging legal directives for the target market."""
    return JURISDICTION_STANDARDS.get(market.upper(), JURISDICTION_STANDARDS["US"])
