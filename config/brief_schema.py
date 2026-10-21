"""
BriefForge Brief Schema Definition
Specifies required and optional packaging fields, grouped by section with category and regulatory mappings.
"""

from typing import Dict, Any, List

BRIEF_SECTIONS = [
    {
        "id": "project_and_brand_overview",
        "title": "1. Project & Brand Overview",
        "description": "Core identity, positioning, SKU identifiers, and scope parameters."
    },
    {
        "id": "structural_and_pack_specs",
        "title": "2. Structural & Pack Specifications",
        "description": "Substrates, dieline constraints, finishing, dimensions, net quantity, and barcode details."
    },
    {
        "id": "mandatory_copy_and_regulatory",
        "title": "3. Mandatory Copy & Regulatory Content",
        "description": "Formulation deck, allergen declaration, nutrition panel, claims, and storage instructions."
    },
    {
        "id": "visual_and_creative_direction",
        "title": "4. Visual & Creative Direction",
        "description": "Serving photography disclosures, copywriting hierarchy, brand lockups, and approved seals."
    },
    {
        "id": "typography_and_print_corrections",
        "title": "5. Mandatory Pre-Press & Artwork Corrections",
        "description": "Actionable checklist of dieline mechanical, typography, and regulatory defect corrections."
    },
    {
        "id": "open_questions_for_agency",
        "title": "6. Open Questions for the Design Agency",
        "description": "Unresolved converter tolerances, barrier materials, or press parameters."
    }
]

BRIEF_SCHEMA: Dict[str, Dict[str, Any]] = {
    "project_and_brand_overview": {
        "brand": {
            "label": "Brand",
            "required": True,
            "category": "identity",
            "description": "Brand or umbrella mark name.",
            "default_citation": "Carton PDP / Content Sheet",
        },
        "product_name": {
            "label": "Product Name",
            "required": True,
            "category": "identity",
            "description": "Commercial product descriptor and sub-brand name.",
            "default_citation": "Carton PDP",
        },
        "label_identifier": {
            "label": "Label Identifier / BPN",
            "required": True,
            "category": "traceability",
            "description": "Base part number, artwork revision code, or label spec ID.",
            "default_citation": "Content Sheet",
        },
        "project_scope": {
            "label": "Project Scope",
            "required": True,
            "category": "strategy",
            "description": "Remediation target (e.g. single SKU fix, full line redesign).",
            "default_citation": "Content Sheet / Brand Manager",
        },
        "target_channel": {
            "label": "Target Channel & Positioning",
            "required": True,
            "category": "strategy",
            "description": "Retail environment, consumer tier, and channel compliance standards.",
            "default_citation": "Brand Strategy / Brief",
        },
        "brand_identity_status": {
            "label": "Brand Identity Asset Status",
            "required": True,
            "category": "creative",
            "description": "Whether assets are strictly locked, evolutionary, or open to overhaul.",
            "default_citation": "Brand Guidelines",
        }
    },
    "structural_and_pack_specs": {
        "packaging_format": {
            "label": "Packaging Format",
            "required": True,
            "category": "structural",
            "description": "Format structure (e.g., folding carton with liner, stand-up pouch, shrink sleeve).",
            "default_citation": "Dieline Geometry",
        },
        "substrate_caliper": {
            "label": "Substrate & Caliper",
            "required": True,
            "category": "structural",
            "description": "Material type, weight, caliper (e.g., 18pt SBS, Kraft, PCR film).",
            "default_citation": "Technical Spec",
        },
        "finishing_coatings": {
            "label": "Finishing & Coatings",
            "required": False,
            "category": "structural",
            "description": "Varnishes, aqueous coating, foil stamping, emboss, or spot UV.",
            "default_citation": "Converter Spec",
        },
        "declared_net_quantity": {
            "label": "Declared Net Quantity",
            "required": True,
            "category": "regulatory",
            "description": "Net weight or volume formatted per 21 CFR 101.7 / target market standard.",
            "default_citation": "PDP / Packaging Spec",
        },
        "upc_barcode": {
            "label": "UPC Barcode",
            "required": True,
            "category": "regulatory",
            "description": "Barcode symbology, check digit, magnification, and quiet zone verification.",
            "default_citation": "Carton Artwork Lower Left / Back",
        }
    },
    "mandatory_copy_and_regulatory": {
        "ingredient_deck": {
            "label": "Authorized Master Formulation Deck",
            "required": True,
            "category": "regulatory",
            "description": "Complete ingredient listing in descending order of predominance by weight.",
            "default_citation": "Master Formulation / Content Sheet",
        },
        "allergen_declaration": {
            "label": "Mandatory Allergen Declaration",
            "required": True,
            "category": "regulatory",
            "description": "FALCPA / FASTER compliant 'Contains' and optional 'May Contain' advisory.",
            "default_citation": "Regulatory Spec / Lab Sheet",
        },
        "nutrition_facts_spec": {
            "label": "Nutrition Facts Panel Specification",
            "required": True,
            "category": "regulatory",
            "description": "Serving size, servings per container, format compliance (e.g., FDA 2016 Vertical).",
            "default_citation": "Nutrition Analysis / Genesis R&D",
        },
        "sugar_claims": {
            "label": "Sugar Claim Correction",
            "required": False,
            "category": "regulatory",
            "description": "Added sugars declaration and validation against 'No Added Sugar' claim legality.",
            "default_citation": "Regulatory Audit",
        },
        "vegan_veg_classification": {
            "label": "Vegan vs. Vegetarian Classification",
            "required": True,
            "category": "regulatory",
            "description": "Claim certification eligibility (e.g., honey disqualifies Vegan mark).",
            "default_citation": "Product Claims Review",
        },
        "front_of_pack_lozenges": {
            "label": "Front-of-Pack Nutrition Lozenges",
            "required": False,
            "category": "regulatory",
            "description": "Market-specific compliance (e.g., strip UK traffic lights on US packaging).",
            "default_citation": "Regulatory Audit",
        },
        "mandatory_storage": {
            "label": "Mandatory Storage Copy",
            "required": True,
            "category": "regulatory",
            "description": "Consumer handling, opening directions, and shelf-life statement.",
            "default_citation": "Quality Assurance Spec",
        }
    },
    "visual_and_creative_direction": {
        "serving_disclosure": {
            "label": "Serving Photography Disclosure",
            "required": True,
            "category": "creative",
            "description": "Required disclaimer adjacent to styled food imagery ('Serving Suggestion').",
            "default_citation": "Legal / Marketing Review",
        },
        "brand_copywriting": {
            "label": "Brand Copywriting Hierarchy",
            "required": False,
            "category": "creative",
            "description": "Headline story, taglines, descriptors, and tone-of-voice directives.",
            "default_citation": "Brand Deck",
        },
        "on_pack_certifications": {
            "label": "Valid On-Pack Certifications & Badges",
            "required": True,
            "category": "creative",
            "description": "Approved third-party trustmarks (USDA Organic, Non-GMO, How2Recycle).",
            "default_citation": "Certifications Register",
        }
    }
}
