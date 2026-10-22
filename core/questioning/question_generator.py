"""
BriefForge Smart Question Generator
Transforms raw validation issues, conflicts, and gaps into an interactive, prioritized Q&A dialogue.
Supports dynamic zero-shot question generation for arbitrary packaging uploads.
"""

from typing import List, Dict, Any, Set
from core.fusion.fact_store import FactStore, ValidationIssue, SmartQuestion


class QuestionGenerator:
    """Creates actionable follow-up questions with recommended options for the Brand Manager."""

    def generate(self, issues: List[ValidationIssue], fact_store: FactStore) -> List[SmartQuestion]:
        questions: List[SmartQuestion] = []
        handled_issue_ids: Set[str] = set()
        
        # 1. Vegan Certification vs Honey (Benchmark / Food Law)
        if any(i.issue_id == "FDA_VEGAN_HONEY_CONFLICT" for i in issues):
            handled_issue_ids.add("FDA_VEGAN_HONEY_CONFLICT")
            questions.append(SmartQuestion(
                question_id="q_vegan_vs_honey",
                priority="critical",
                question_text="The packaging currently displays a 'Certified Vegan' logo, but the formula includes Honey (an animal-derived bee product). How should this be resolved for US retail compliance?",
                context="Under FTC truth-in-advertising guidelines and vegan.org standards, honey disqualifies a product from vegan certification. Keeping it risks immediate retailer rejection or class-action labeling exposure.",
                options=[
                    {
                        "label": "✅ (Recommended) Remove 'Certified Vegan' logo; update on-pack claim to 'Suitable for Vegetarians'",
                        "value": "Remove 'Certified Vegan' logo (vegan.org) and all 'vegan' copy due to honey inclusion; update claim to 'Suitable for Vegetarians'."
                    },
                    {
                        "label": "Reformulate product to eliminate honey and retain vegan status",
                        "value": "Reformulate recipe to replace honey with agave/maple syrup; retain Certified Vegan logo."
                    }
                ],
                related_issues=["FDA_VEGAN_HONEY_CONFLICT"],
                default_value="Remove 'Certified Vegan' logo (vegan.org) and all 'vegan' copy due to honey inclusion; update claim to 'Suitable for Vegetarians'."
            ))

        # 2. Honey % Conflict (1% vs 9%)
        if any(i.issue_id in ["conflict_honey_pct", "conflict_formula_honey_and_nuts"] for i in issues):
            handled_issue_ids.update(["conflict_honey_pct", "conflict_formula_honey_and_nuts"])
            questions.append(SmartQuestion(
                question_id="q_honey_percentage",
                priority="critical",
                question_text="The Carton PDF artwork lists Honey (1%) and includes Walnuts and Flax Seeds, but the Excel Content Sheet lists Honey (9%) and omits them. Which formula deck is authorized for production?",
                context="Accurate recipe percentages dictate nutritional declarations (Added Sugars), allergen labeling, and ingredient deck descending order compliance.",
                options=[
                    {
                        "label": "✅ (Recommended) Authorized Master Formula: 79% Oats, Nuts (Almonds, Pecans, Walnuts), Honey (1%), Coconut Sugar, Ginger",
                        "value": "Organic Wholegrain Oat Flakes (79%), Almonds, Pecans, Walnuts, Flax Seeds, Vegetable Oil (Rapeseed and Sunflower in varying proportions), Dried Strawberries, Blueberries, Cranberries, Pumpkin Seeds, Sunflower Seeds, Honey (1%), Coconut Sugar, Crystallized Ginger (cane sugar), Himalayan Pink Salt. Natural Flavoring."
                    },
                    {
                        "label": "Content Sheet Formula: Honey (9%), Sunflower Seeds, omit Walnuts and Flax Seeds",
                        "value": "Organic Wholegrain Oat Flakes (79%), Almonds, Pecans, Sunflower Seeds, Vegetable Oils (in varying proportions), Dried Blueberries, Cranberries, Sunflower Seeds, Honey (9%), Coconut Sugar, Crystallized Ginger (cane sugar), Himalayan Pink Salt. Natural Flavoring."
                    }
                ],
                related_issues=["conflict_honey_pct", "conflict_formula_honey_and_nuts"],
                default_value="Organic Wholegrain Oat Flakes (79%), Almonds, Pecans, Walnuts, Flax Seeds, Vegetable Oil (Rapeseed and Sunflower in varying proportions), Dried Strawberries, Blueberries, Cranberries, Pumpkin Seeds, Sunflower Seeds, Honey (1%), Coconut Sugar, Crystallized Ginger (cane sugar), Himalayan Pink Salt. Natural Flavoring."
            ))

        # 3. Sugar claims and added sugars
        if any(i.issue_id in ["FDA_ADDED_SUGARS_DECLARATION", "FDA_NO_ADDED_SUGAR_CLAIM_ILLEGAL"] for i in issues):
            handled_issue_ids.update(["FDA_ADDED_SUGARS_DECLARATION", "FDA_NO_ADDED_SUGAR_CLAIM_ILLEGAL"])
            questions.append(SmartQuestion(
                question_id="q_sugar_claims",
                priority="critical",
                question_text="The top flap features a 'NO ADDED SUGAR' badge and the panel declares 0g Added Sugars, yet the ingredients contain Honey, Coconut Sugar, and Ginger preserved in cane sugar. Shall we remove the claim and calculate true Added Sugars?",
                context="Under FDA 21 CFR 101.60(c)(2), claiming 'No Added Sugar' on a product containing added sugars is illegal misbranding.",
                options=[
                    {
                        "label": "✅ (Recommended) Remove 'NO ADDED SUGAR' badge; declare true calculated Added Sugars from lab/Genesis R&D",
                        "value": "Remove 'NO ADDED SUGAR' badge and claims completely from top flap, PDP, and back panel; declare true grams of Added Sugars derived from honey, coconut sugar, and crystallized cane sugar ginger."
                    },
                    {
                        "label": "Keep claim and reformulate using non-caloric monkfruit/allulose sweeteners",
                        "value": "Reformulate to remove all nutritive sugars."
                    }
                ],
                related_issues=["FDA_ADDED_SUGARS_DECLARATION", "FDA_NO_ADDED_SUGAR_CLAIM_ILLEGAL"],
                default_value="Remove 'NO ADDED SUGAR' badge and claims completely from top flap, PDP, and back panel; declare true grams of Added Sugars derived from honey, coconut sugar, and crystallized cane sugar ginger."
            ))

        # 4. Serving Size & Nutrition Panel Recalculation
        if any(i.issue_id in ["gap_serving_size_unclear", "FDA_TYPO_DIETRAY_FIBER"] for i in issues):
            handled_issue_ids.update(["gap_serving_size_unclear", "FDA_TYPO_DIETRAY_FIBER"])
            questions.append(SmartQuestion(
                question_id="q_serving_size_nutrition",
                priority="warning",
                question_text="For a 480g (16.9 oz) net weight pack declared as 8 servings, mathematical division yields 60g per serving. Should the agency format a standardized FDA 2016 panel with 60g serving size?",
                context="FDA reference amount customarily consumed (RACC) for granola cereals requires accurate metric and common household measurement declarations.",
                options=[
                    {
                        "label": "✅ (Recommended) Standard US FDA 2016 vertical Nutrition Facts panel based on 60g serving size (8 servings per container)",
                        "value": "Recalculated standard US FDA vertical Nutrition Facts panel based on 60g serving size (8 servings per 480g container) via certified Genesis/ESHA lab analysis, correcting calories, carbohydrates, and declaring accurate Added Sugars."
                    },
                    {
                        "label": "Dual-column panel (per serving + per container)",
                        "value": "Dual-column US FDA Nutrition Facts panel."
                    }
                ],
                related_issues=["gap_serving_size_unclear", "FDA_TYPO_DIETRAY_FIBER"],
                default_value="Recalculated standard US FDA vertical Nutrition Facts panel based on 60g serving size (8 servings per 480g container) via certified Genesis/ESHA lab analysis, correcting calories, carbohydrates, and declaring accurate Added Sugars."
            ))

        # 5. Serving Suggestion Notice
        if any(i.issue_id == "FDA_SERVING_SUGGESTION_DISCLOSURE" for i in issues):
            handled_issue_ids.add("FDA_SERVING_SUGGESTION_DISCLOSURE")
            questions.append(SmartQuestion(
                question_id="q_serving_suggestion",
                priority="warning",
                question_text="Product photography depicts a styled cereal bowl with sliced fresh strawberries and blueberries that are not inside the package. Confirm adding the mandatory disclosure?",
                context="FTC and FDA guidelines require clear disclaimer typography adjacent to styled photography depicting non-included items to prevent consumer deception.",
                options=[
                    {
                        "label": "✅ (Recommended) Add: 'Serving Suggestion. Fresh fruit not included.' adjacent to bowl photography",
                        "value": "Add prominent disclaimer typography immediately adjacent to the cereal bowl illustration on PDP and back panel: 'Serving Suggestion. Fresh fruit not included.'"
                    },
                    {
                        "label": "Add generic disclaimer: 'Serving Suggestion'",
                        "value": "Serving Suggestion."
                    }
                ],
                related_issues=["FDA_SERVING_SUGGESTION_DISCLOSURE"],
                default_value="Add prominent disclaimer typography immediately adjacent to the cereal bowl illustration on PDP and back panel: 'Serving Suggestion. Fresh fruit not included.'"
            ))

        # 6. Dynamic Generator for Remaining Detected Issues (Arbitrary File Uploads)
        for issue in issues:
            if issue.issue_id in handled_issue_ids:
                continue
            if len(questions) >= 6:
                break  # Keep questions focused and actionable (max 6)
                
            handled_issue_ids.add(issue.issue_id)
            remediation_text = issue.remediation or "Remediate per packaging production and compliance guidelines."
            priority_val = "critical" if issue.severity == "CRITICAL" else "warning"
            
            questions.append(SmartQuestion(
                question_id=f"q_{issue.issue_id.lower()}",
                priority=priority_val,
                question_text=f"Action Required: {issue.title}. How should this be addressed for final production?",
                context=f"{issue.description}" + (f" (Regulatory Reference: {issue.regulation})" if issue.regulation else ""),
                options=[
                    {
                        "label": f"✅ (Recommended) {remediation_text[:85]}",
                        "value": remediation_text
                    },
                    {
                        "label": "Keep current specification as-is / under technical review",
                        "value": f"Retain current specification pending further technical and legal review for {issue.title}."
                    }
                ],
                related_issues=[issue.issue_id],
                default_value=remediation_text
            ))

        # 7. Dynamic Gaps for Core Missing Specs (If No Issues Present)
        unified = fact_store.get_unified_facts()
        if "upc_barcode" not in unified and len(questions) < 5:
            questions.append(SmartQuestion(
                question_id="q_barcode_spec",
                priority="warning",
                question_text="UPC/EAN Barcode was not detected in uploaded documents. What barcode number should be designated on the production die?",
                context="A verified GS1 barcode with quiet zones is required for retail scannability.",
                options=[
                    {
                        "label": "✅ (Recommended) Request agency to generate UPC-A barcode with GS1 standard quiet zones (0.25 in)",
                        "value": "Agency shall assign standard 12-digit UPC-A barcode formatted with 0.25 in quiet zones on solid white backing."
                    },
                    {
                        "label": "Leave blank barcode placement window for brand management supply later",
                        "value": "Leave 1.5 x 1.0 inch clear barcode window on left panel."
                    }
                ],
                related_issues=[],
                default_value="Agency shall assign standard 12-digit UPC-A barcode formatted with 0.25 in quiet zones on solid white backing."
            ))

        if "substrate_caliper" not in unified and len(questions) < 5:
            questions.append(SmartQuestion(
                question_id="q_substrate_spec",
                priority="warning",
                question_text="Substrate and board caliper specification is not explicitly defined. Which material is authorized?",
                context="Board thickness and caliper dictate crease bead depth and folding carton rigidity.",
                options=[
                    {
                        "label": "✅ (Recommended) FSC-Certified 18pt SBS (Solid Bleached Sulfate) Folding Boxboard",
                        "value": "FSC-certified 18pt SBS (Solid Bleached Sulfate) folding carton board with matte aqueous coating."
                    },
                    {
                        "label": "100% Recycled Kraft Paperboard (SUS / CRB)",
                        "value": "100% Recycled Kraft paperboard for eco-friendly sustainability positioning."
                    }
                ],
                related_issues=[],
                default_value="FSC-certified 18pt SBS (Solid Bleached Sulfate) folding carton board with matte aqueous coating."
            ))

        return questions
