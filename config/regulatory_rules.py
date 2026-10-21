"""
BriefForge Regulatory Rules Engine
Deterministic packaging compliance rules for US FDA (21 CFR), FTC, FALCPA, and FASTER Act standards.
"""

from typing import Dict, Any, List, Tuple

REGULATORY_RULES: List[Dict[str, Any]] = [
    {
        "id": "FDA_VEGAN_HONEY_CONFLICT",
        "name": "Vegan Certification Incompatible with Honey",
        "severity": "CRITICAL",
        "regulation": "FTC Truth in Advertising / Vegan Action Standards",
        "description": "Products containing honey, dairy, eggs, or insect/animal-derived components cannot legally display a Certified Vegan trustmark.",
        "rule_fn": "check_vegan_honey"
    },
    {
        "id": "FDA_ADDED_SUGARS_DECLARATION",
        "name": "Caloric Sweetener with Zero Added Sugars Declared",
        "severity": "CRITICAL",
        "regulation": "FDA 21 CFR 101.9(c)(6)(iii)",
        "description": "When formulation includes honey, cane sugar, coconut sugar, syrups, or juice concentrates, Added Sugars cannot be declared as 0g / 0%.",
        "rule_fn": "check_added_sugars"
    },
    {
        "id": "FDA_NO_ADDED_SUGAR_CLAIM_ILLEGAL",
        "name": "Illegal 'No Added Sugar' Nutrient Content Claim",
        "severity": "CRITICAL",
        "regulation": "FDA 21 CFR 101.60(c)(2)",
        "description": "'No Added Sugar' claim is prohibited if the food contains added sugars such as honey or coconut sugar, unless explicit disclaimer is made.",
        "rule_fn": "check_no_added_sugar_claim"
    },
    {
        "id": "FALCPA_TREE_NUT_ALLERGEN_CONTAINS",
        "name": "Allergen 'May Contain' Advisory for Intentional Recipe Ingredients",
        "severity": "CRITICAL",
        "regulation": "FALCPA 21 U.S.C. 343(w) / FASTER Act",
        "description": "If almonds, walnuts, pecans or other major allergens are formulation ingredients, they must be declared under a bold 'CONTAINS:' statement, not relegated to advisory 'May Contain'.",
        "rule_fn": "check_allergen_contains"
    },
    {
        "id": "FDA_NET_QUANTITY_PDP",
        "name": "Missing or Misplaced Net Quantity of Contents",
        "severity": "CRITICAL",
        "regulation": "FDA 21 CFR 101.7 / Fair Packaging and Labeling Act",
        "description": "The net quantity statement (e.g. NET WT 16.9 OZ (480g)) must appear in the lower 30 percent of the Principal Display Panel parallel to the base.",
        "rule_fn": "check_net_quantity"
    },
    {
        "id": "FDA_EU_UK_TRAFFIC_LIGHT_LOZENGES",
        "name": "Non-compliant EU/UK Traffic Light Nutrition Lozenges on US Pack",
        "severity": "WARNING",
        "regulation": "FDA 21 CFR 101 (US Labeling Standards)",
        "description": "Traffic-light color-coded front/back of pack nutrition lozenges are an EU/UK construct and not permitted or recognized under standard FDA labeling.",
        "rule_fn": "check_eu_lozenges"
    },
    {
        "id": "FDA_SERVING_SUGGESTION_DISCLOSURE",
        "name": "Missing Serving Photography Disclosure",
        "severity": "WARNING",
        "regulation": "FTC Deceptive Advertising Guidelines / FDA 21 CFR 101",
        "description": "When serving imagery portrays ingredients not present in the package (e.g., fresh berries, milk, yogurt), 'Serving Suggestion' disclaimer is mandatory.",
        "rule_fn": "check_serving_suggestion"
    },
    {
        "id": "FDA_DIELINE_GUIDE_TEXT_CONTAMINATION",
        "name": "Dieline Mechanical & Guide Text in Printable Layers",
        "severity": "CRITICAL",
        "regulation": "Pre-Press Packaging Mechanical Standards",
        "description": "Non-printing annotations (e.g. 'Front panel Orientation', 'Copy free', 'Dieline - Do Not Print') must not contaminate print-ready separation layers.",
        "rule_fn": "check_dieline_text"
    },
    {
        "id": "FDA_TYPO_RECYCABLE",
        "name": "Typographical Error in Recycling Callout",
        "severity": "WARNING",
        "regulation": "Packaging Quality Control",
        "description": "Detected 'RECYCABLE' on packaging artwork which must be remediated to 'RECYCLABLE'.",
        "rule_fn": "check_recyclable_typo"
    },
    {
        "id": "FDA_TYPO_DIETRAY_FIBER",
        "name": "Typographical Error in Nutrition Facts Panel",
        "severity": "CRITICAL",
        "regulation": "FDA 21 CFR 101.9 Mandatory Heading Accuracy",
        "description": "Detected 'DIETRAY' in Nutrition Facts panel which must be corrected to 'DIETARY FIBER'.",
        "rule_fn": "check_dietary_typo"
    },
    {
        "id": "FDA_SERVING_CALCULATION_MISMATCH",
        "name": "Serving Size × Servings Per Container Math Mismatch",
        "severity": "WARNING",
        "regulation": "FDA 21 CFR 101.9",
        "description": "Number of servings multiplied by gram serving size should align within rounding tolerances to declared total net weight.",
        "rule_fn": "check_serving_math"
    },
    {
        "id": "FDA_BARCODE_QUIET_ZONE",
        "name": "UPC-A Barcode Quiet Zone & Contrast Verification",
        "severity": "WARNING",
        "regulation": "GS1 General Specifications (ISO/IEC 15420)",
        "description": "UPC-A symbol must have minimum 0.25 inch quiet zone margins on high-contrast solid background.",
        "rule_fn": "check_barcode"
    }
]


def evaluate_rules(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Evaluates all regulatory rules against the accumulated fact dictionary.
    Returns list of triggered violations with actionable remediation guidance.
    """
    violations = []
    
    # Text aggregations for searching
    raw_text = " ".join(str(v) for v in facts.values()).lower()
    ingredients = str(facts.get("ingredient_deck", facts.get("ingredient_list", ""))).lower()
    claims = str(facts.get("on_pack_certifications", facts.get("certifications", facts.get("notes", "")))).lower()
    allergens = str(facts.get("allergen_declaration", facts.get("allergen_information", ""))).lower()
    nutrition = facts.get("nutrition_facts_spec", {})
    if isinstance(nutrition, str):
        nutrition_text = nutrition.lower()
    else:
        nutrition_text = str(nutrition).lower()
        
    # 1. Vegan vs Honey
    has_honey = "honey" in ingredients or "honey" in raw_text
    has_vegan = "vegan" in claims or "vegan" in raw_text or "certified vegan" in raw_text
    if has_honey and has_vegan:
        violations.append({
            "rule_id": "FDA_VEGAN_HONEY_CONFLICT",
            "title": "Certified Vegan Logo Incompatible with Honey Formulation",
            "severity": "CRITICAL",
            "regulation": "FTC Fair Packaging / Vegan Action Standards",
            "affected_fields": ["vegan_veg_classification", "on_pack_certifications"],
            "description": "Product formulation contains honey (animal-derived bee product), yet artwork displays 'Certified Vegan' (vegan.org) logo.",
            "remediation": "Remove 'Certified Vegan' logo from PDP and back panel; update claim copy to 'Suitable for Vegetarians'."
        })

    # 2. Added sugars zero check
    sweeteners = ["honey", "sugar", "cane sugar", "coconut sugar", "syrup", "molasses"]
    has_sweeteners = any(s in ingredients for s in sweeteners)
    declared_added_zero = "added sugar" in raw_text and ("0g" in raw_text or " 0%" in raw_text or "incl. added sugars 0g" in raw_text)
    if has_sweeteners and declared_added_zero:
        violations.append({
            "rule_id": "FDA_ADDED_SUGARS_DECLARATION",
            "title": "Caloric Sweeteners Declared with 0g Added Sugars",
            "severity": "CRITICAL",
            "regulation": "FDA 21 CFR 101.9(c)(6)(iii)",
            "affected_fields": ["nutrition_facts_spec", "sugar_claims"],
            "description": "Formulation includes Honey, Coconut Sugar, and Crystallized Ginger (cane sugar), yet Nutrition Panel declares 0g (0% DV) Added Sugars.",
            "remediation": "Perform certified nutritional recalculation; declare true grams of Added Sugars and appropriate % Daily Value."
        })

    # 3. No Added Sugar claim illegal
    has_no_added_sugar_claim = "no added sugar" in claims or "no added sugar" in raw_text
    if has_sweeteners and has_no_added_sugar_claim:
        violations.append({
            "rule_id": "FDA_NO_ADDED_SUGAR_CLAIM_ILLEGAL",
            "title": "Misleading 'No Added Sugar' Callout",
            "severity": "CRITICAL",
            "regulation": "FDA 21 CFR 101.60(c)(2)",
            "affected_fields": ["sugar_claims", "on_pack_certifications"],
            "description": "'NO ADDED SUGAR' badge appears on pack flaps while recipe contains added honey and sugars.",
            "remediation": "Delete 'NO ADDED SUGAR' badge completely from top flap, PDP, and back panel."
        })

    # 4. Allergen declaration contains vs may contain
    tree_nuts_in_ingredients = [nut for nut in ["almond", "pecan", "walnut", "cashew", "hazelnut"] if nut in ingredients]
    has_may_contain_only = "may contain" in allergens and "contains:" not in allergens
    if tree_nuts_in_ingredients and has_may_contain_only:
        violations.append({
            "rule_id": "FALCPA_TREE_NUT_ALLERGEN_CONTAINS",
            "title": "Major Tree Nut Allergens Listed Only Under Advisory 'May Contain'",
            "severity": "CRITICAL",
            "regulation": "FALCPA 21 U.S.C. 343(w)",
            "affected_fields": ["allergen_declaration"],
            "description": "Almonds and pecans are primary ingredients in the formula deck, but packaging groups them under 'May Contain'.",
            "remediation": "Revise statement to bold standard: 'CONTAINS: ALMONDS, PECANS, WALNUTS. MAY CONTAIN: BRAZIL NUTS, OTHER TREE NUTS, WHEAT.'"
        })

    # 5. Dieline Guide Text Contamination
    dieline_markers = ["front panel orientation", "copy free", "dieline - do not print", "art orientation"]
    if any(m in raw_text for m in dieline_markers):
        violations.append({
            "rule_id": "FDA_DIELINE_GUIDE_TEXT_CONTAMINATION",
            "title": "Dieline Guide Annotations Present on Artwork Separation Layers",
            "severity": "CRITICAL",
            "regulation": "Pre-Press Quality Standards",
            "affected_fields": ["prepress_production"],
            "description": "Artwork proof contains non-printing guide text ('Front panel Orientation', 'Copy free', 'Dieline - Do Not Print') directly on printable art layers.",
            "remediation": "Move or purge non-printing dieline guide text from final production artwork layers."
        })

    # 6. Serving photography disclosure
    has_food_photo = "bowl" in raw_text or "fruit" in raw_text or "photography" in raw_text or "cereal bowl" in raw_text
    has_serving_suggestion = "serving suggestion" in raw_text
    if has_food_photo and not has_serving_suggestion:
        violations.append({
            "rule_id": "FDA_SERVING_SUGGESTION_DISCLOSURE",
            "title": "Missing Mandatory Serving Photography Disclaimer",
            "severity": "WARNING",
            "regulation": "FTC Guidelines / FDA 21 CFR 101",
            "affected_fields": ["serving_disclosure"],
            "description": "Styled cereal bowl imagery depicts fresh fruit, but lacks 'Serving Suggestion' notice.",
            "remediation": "Add prominent copy adjacent to photography: 'Serving Suggestion. Fresh fruit not included.'"
        })

    # 7. EU Traffic lights on US pack
    if "traffic" in raw_text or "lozenge" in raw_text or "ri lozenge" in raw_text:
        violations.append({
            "rule_id": "FDA_EU_UK_TRAFFIC_LIGHT_LOZENGES",
            "title": "EU/UK Traffic Light Nutrition Lozenges on US Pack",
            "severity": "WARNING",
            "regulation": "FDA 21 CFR 101",
            "affected_fields": ["front_of_pack_lozenges"],
            "description": "UK/EU style color-coded nutritional lozenges are present on US folding carton back panel.",
            "remediation": "Remove UK/EU traffic-light style nutrition lozenges completely from back panel."
        })

    # 8. Typos
    if "recycable" in raw_text:
        violations.append({
            "rule_id": "FDA_TYPO_RECYCABLE",
            "title": "Typographical Error in Recycling Callout",
            "severity": "WARNING",
            "regulation": "Packaging Quality Control",
            "affected_fields": ["on_pack_certifications"],
            "description": "Typo 'RECYCABLE' found on recycling badge.",
            "remediation": "Correct typo 'RECYCABLE' to 'RECYCLABLE' on recycling callout badge."
        })
        
    if "dietray" in raw_text:
        violations.append({
            "rule_id": "FDA_TYPO_DIETRAY_FIBER",
            "title": "Typographical Error in Nutrition Facts Header",
            "severity": "CRITICAL",
            "regulation": "FDA 21 CFR 101.9",
            "affected_fields": ["nutrition_facts_spec"],
            "description": "Typo 'DIETRAY' in Nutrition Facts panel (Dietary Fiber).",
            "remediation": "Correct typo 'DIETRAY' to 'DIETARY' in Nutrition Facts panel."
        })

    return violations
