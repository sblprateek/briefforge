"""
BriefForge LLM Prompt Library
Prompt definitions for multimodal PDF vision extraction, Excel semantic parsing,
cross-reference reconciliation, question generation, and brief generation.
"""

PDF_EXTRACTION_PROMPT = """
You are an expert packaging engineer, pre-press production manager, and FDA regulatory labeling compliance specialist.
Analyze this high-resolution packaging artwork/dieline file in detail.

Examine all packaging panels (Front / PDP, Back Panel, Left Side, Right Side, Top Flap, Bottom Flap, Glue Tab).

Extract the following verified data into JSON:
1. Brand Name & Product Statement of Identity
2. Full ingredients list (verbatim, including percentages and parentheticals)
3. Allergen warnings (exact wording, distinguishing 'CONTAINS:' vs 'MAY CONTAIN:')
4. Nutrition Facts panel (format, serving size, servings per container, calories, nutrient values, %DV, Added Sugars)
5. Packaging specifications (dieline dimensions, substrate callouts, finishings, net weight declaration on PDP)
6. Barcode symbology (UPC-A, number string, quiet zone condition)
7. On-pack certifications, trustmarks, and claims (e.g. USDA Organic, Certified Vegan, Non-GMO, No Added Sugar)
8. Mandatory warnings, storage instructions, recycling badges (How2Recycle), marketing copy
9. Mechanical / pre-press defects: dieline guide annotations, typographical errors, formatting issues

Output strictly valid JSON with this structure:
{
  "brand": "...",
  "product_name": "...",
  "net_quantity": "...",
  "ingredient_deck": "...",
  "allergen_declaration": "...",
  "nutrition_panel": {
    "servings_per_container": "...",
    "serving_size": "...",
    "calories": "...",
    "added_sugars": "...",
    "nutrients": {}
  },
  "certifications": ["..."],
  "claims": ["..."],
  "marketing_copy": "...",
  "storage_instructions": "...",
  "barcode": "...",
  "packaging_format": "...",
  "substrate_and_coatings": "...",
  "dieline_observations": ["..."],
  "typos_detected": ["..."]
}
"""

EXCEL_SEMANTIC_PROMPT = """
You are an expert packaging content manager and specification engineer.
You are given parsed row-and-column data from an internal product specification content sheet.

Review all labeled sections, field names, language variations, revision notes, and comments.

Extract and map all product attributes into structured JSON matching the packaging brief schema:
- Brand & Product Identity (Brand name, SKU, BPN, market territory, target consumer)
- Ingredient Deck & Allergen Information (verbatim text, plus any author notes or warnings)
- Nutrition Table Values (servings, serving size, grams, %DV, added sugars)
- Packaging and Format attributes (carton type, portions, net weight, substrate, barcodes)
- Claims, marketing copy, and storage directives
- Spreadsheet Author Notes (e.g., warnings about dieline overlap, unconfirmed BPNs, allergen advisory vs intentional recipe nuts)

Output strictly valid JSON:
{
  "brand": "...",
  "product_name": "...",
  "label_identifier": "...",
  "net_weight": "...",
  "servings": "...",
  "serving_size": "...",
  "ingredient_deck": "...",
  "allergen_declaration": "...",
  "claims": ["..."],
  "marketing_copy": "...",
  "storage_instructions": "...",
  "barcode": "...",
  "author_notes": ["..."]
}
"""

CROSS_REFERENCE_PROMPT = """
You are a Lead Packaging Compliance Auditor comparing facts extracted from multiple sources (e.g., packaging artwork PDF vs formulation Excel sheet vs brand guidelines).

Analyze the inputs and detect:
1. DIRECT CONFLICTS: Where source A asserts one value and source B asserts a contradictory value (e.g. Honey 1% vs Honey 9%, or allergen lists differing).
2. REGULATORY VIOLATIONS: Inconsistencies between ingredients and claims (e.g., Honey present but 'Certified Vegan' badge displayed; added caloric sugars present but 'No Added Sugar' claimed).
3. GAPS: Essential FDA or pre-press information missing across all documents.
4. TYPOGRAPHICAL / MECHANICAL DEFECTS: Spelling errors or dieline marks in printable art.

Output strictly valid JSON:
{
  "conflicts": [
    {
      "field": "...",
      "source_a_value": "...",
      "source_b_value": "...",
      "severity": "CRITICAL|WARNING|INFO",
      "impact": "..."
    }
  ],
  "regulatory_violations": [
    {
      "title": "...",
      "severity": "CRITICAL|WARNING",
      "regulation": "...",
      "recommendation": "..."
    }
  ],
  "gaps": ["..."]
}
"""

QUESTION_GENERATION_PROMPT = """
You are an AI Packaging Project Director preparing follow-up questions for a Brand Manager.
Given the detected conflicts, regulatory violations, and missing fields, generate smart, prioritized questions.

Rules:
1. Group related issues together.
2. Formulate concise, professional questions that explain the business or regulatory impact.
3. Provide selectable concrete options and recommend the compliant choice first.
4. Mark priority as 'critical' (legal/FDA/safety blocker), 'warning' (spec mismatch), or 'info' (creative preference).

Output strictly valid JSON list:
[
  {
    "question_id": "q_...",
    "priority": "critical|warning|info",
    "question_text": "...",
    "context": "...",
    "recommended_option": "...",
    "options": [
      {"label": "...", "value": "..."},
      {"label": "...", "value": "..."}
    ],
    "default_value": "..."
  }
]
"""

EXECUTIVE_SUMMARY_PROMPT = """
You are an Executive Packaging Director writing an authoritative Executive Summary for an agency packaging design remediation brief.

Summarize:
- The product name, brand, target market channel, and packaging format.
- The core purpose of the remediation brief (correcting FDA 21 CFR violations, allergen alignment under FALCPA/FASTER, dieline mechanical cleanup, claim removal).
- The scope and operational requirements for the pre-press and design agency.

Keep it concise (1 punchy paragraph), highly professional, and agency-ready.
"""
