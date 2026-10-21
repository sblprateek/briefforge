"""
BriefForge Interactive Visual Dieline Inspector (ArtiosCAD Grade)
Renders an interactive SVG folding carton net with dynamic defect pins, mechanical panel boundaries,
and side-by-side remediation annotations.
"""

from typing import List, Dict, Any, Optional


def render_interactive_dieline(issues: Optional[List[Any]] = None, facts: Optional[Dict[str, Any]] = None) -> str:
    """
    Generates a responsive SVG folding carton net with panel zones,
    mechanical crease lines, and interactive defect hotspot markers across all 12 detected defects.
    """
    if issues is None:
        issues = []
    if facts is None:
        facts = {}

    brand = facts.get("brand", "DANCING FISH")
    product = facts.get("product_name", "Granola Berry Crunch")
    net_wt = facts.get("declared_net_quantity", "NET WT 16.9 OZ (480g)")
    barcode = facts.get("upc_barcode", "1 20000 00003 6")

    html = f"""
    <div style="background:#0F172A; border-radius:12px; padding:18px; color:white; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; box-sizing:border-box;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
            <div>
                <span style="font-size:10.5px; font-weight:800; color:#38BDF8; letter-spacing:0.1em; text-transform:uppercase;">Esko ArtiosCAD-Grade Mechanical Net</span>
                <h3 style="margin:2px 0 0 0; color:white; font-size:15px;">Interactive 2D Folding Carton Dieline Inspector</h3>
                <div style="font-size:11px; color:#94A3B8;">Hover over panel hotspot pins (!) to inspect statutory violations &amp; mechanical guidelines</div>
            </div>
            <div style="display:flex; gap:12px; font-size:11px; background:#1E293B; padding:5px 12px; border-radius:6px; border:1px solid #334155;">
                <span style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:9px; height:9px; background:#EF4444; border-radius:50%;"></span> Critical Defect (8)</span>
                <span style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:9px; height:9px; background:#F59E0B; border-radius:50%;"></span> Pre-Press Warning (4)</span>
                <span style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:9px; height:9px; background:#10B981; border-radius:50%;"></span> Verified Production Spec</span>
            </div>
        </div>

        <svg viewBox="0 0 940 460" style="width:100%; height:auto; max-height:460px; background:#1E293B; border-radius:8px; border:1px solid #334155; display:block;">
            <!-- Definitions for markers and patterns -->
            <defs>
                <pattern id="crease" width="8" height="8" patternUnits="userSpaceOnUse">
                    <line x1="0" y1="0" x2="0" y2="8" stroke="#475569" stroke-width="1" stroke-dasharray="2,2"/>
                </pattern>
                <filter id="glow-red" x="-30%" y="-30%" width="160%" height="160%">
                    <feGaussianBlur stdDeviation="4" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
                <filter id="glow-amber" x="-30%" y="-30%" width="160%" height="160%">
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>

            <!-- GLUE TAB (Far Left) -->
            <g id="panel-glue-tab">
                <polygon points="40,120 80,100 80,350 40,330" fill="#1E293B" stroke="#64748B" stroke-dasharray="4,4" stroke-width="1.5"/>
                <text x="60" y="235" fill="#94A3B8" font-size="9.5" font-weight="700" transform="rotate(-90 60 235)" text-anchor="middle">GLUE TAB (Adhesive Window 15mm)</text>
            </g>

            <!-- LEFT SIDE PANEL (Nutrition & Allergens) -->
            <g id="panel-left-side" style="cursor:pointer;">
                <rect x="80" y="100" width="180" height="250" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="170" y="122" fill="#38BDF8" font-size="10.5" font-weight="700" text-anchor="middle">LEFT PANEL (Nutrition &amp; Allergens)</text>
                
                <!-- Nutrition Box Mockup -->
                <rect x="95" y="135" width="150" height="135" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="105" y="152" fill="white" font-size="9.5" font-weight="800">Nutrition Facts</text>
                <text x="105" y="165" fill="#38BDF8" font-size="8">8 servings per container (60g)</text>
                <text x="105" y="180" fill="#CBD5E1" font-size="8">Calories 166</text>
                <text x="105" y="197" fill="#EF4444" font-size="7.5" font-weight="800">❌ Typo: 'DIETRAY FIBER'</text>
                <text x="105" y="212" fill="#EF4444" font-size="7.5" font-weight="800">❌ Declared 0g Added Sugars</text>
                <text x="105" y="227" fill="#10B981" font-size="7.5" font-weight="700">➜ Correct to 7g Added Sugars</text>

                <!-- Hotspot Pin: Nutrition Typo & Sugars -->
                <circle cx="230" cy="148" r="9" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="230" y="152" fill="white" font-size="10" font-weight="900" text-anchor="middle">!</text>

                <!-- Hotspot Pin: Serving size -->
                <circle cx="230" cy="175" r="7.5" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="230" y="178" fill="white" font-size="8" font-weight="900" text-anchor="middle">!</text>

                <!-- Allergen Box -->
                <rect x="95" y="278" width="150" height="62" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="102" y="293" fill="#F59E0B" font-size="7.5" font-weight="700">⚠️ Allergen Formatting:</text>
                <text x="102" y="307" fill="#CBD5E1" font-size="7">Mandate bold 'CONTAINS:' statement</text>
                <text x="102" y="322" fill="#10B981" font-size="7" font-weight="700">Tree nuts: Almonds, Pecans, Walnuts</text>
            </g>

            <!-- FRONT PANEL (Principal Display Panel / PDP) -->
            <g id="panel-front-pdp" style="cursor:pointer;">
                <rect x="260" y="100" width="220" height="250" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
                <text x="370" y="122" fill="#38BDF8" font-size="11.5" font-weight="800" text-anchor="middle">FRONT PANEL (Principal Display Panel)</text>

                <!-- Brand & Artwork Mockup -->
                <rect x="295" y="135" width="150" height="28" rx="4" fill="#2563EB"/>
                <text x="370" y="153" fill="white" font-size="12" font-weight="900" text-anchor="middle">{brand}</text>
                <text x="370" y="175" fill="#F8FAFC" font-size="9.5" font-weight="700" text-anchor="middle">{product}</text>

                <!-- Illustration / Photography area -->
                <circle cx="370" cy="220" r="32" fill="#334155" stroke="#64748B"/>
                <text x="370" y="218" fill="#94A3B8" font-size="7" text-anchor="middle">Cereal Bowl Photo</text>
                <text x="370" y="229" fill="#94A3B8" font-size="6" text-anchor="middle">(Fresh Berries Shown)</text>

                <!-- Hotspot Pin: Missing Serving Suggestion -->
                <circle cx="410" cy="215" r="9" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="410" y="219" fill="white" font-size="10" font-weight="900" text-anchor="middle">!</text>
                <text x="370" y="264" fill="#F59E0B" font-size="7" font-weight="700" text-anchor="middle">+ Add: 'Serving Suggestion. Fresh fruit not included.'</text>

                <!-- Hotspot Pin: Certified Vegan Badge Conflict -->
                <circle cx="310" cy="188" r="9" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="310" y="192" fill="white" font-size="10" font-weight="900" text-anchor="middle">!</text>
                <text x="310" y="204" fill="#EF4444" font-size="6" font-weight="800">❌ VEGAN BADGE</text>

                <!-- Lower 30% Net Weight Target Zone -->
                <rect x="270" y="280" width="200" height="60" fill="#0F172A" stroke="#EF4444" stroke-dasharray="3,3" rx="4"/>
                <text x="370" y="298" fill="#EF4444" font-size="7.5" font-weight="800" text-anchor="middle">MANDATORY NET QUANTITY ZONE (21 CFR 101.7)</text>
                <text x="370" y="320" fill="#10B981" font-size="10" font-weight="900" text-anchor="middle">{net_wt}</text>

                <!-- Hotspot Pin: Net weight location -->
                <circle cx="455" cy="300" r="8.5" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="455" y="303" fill="white" font-size="9.5" font-weight="900" text-anchor="middle">!</text>
            </g>

            <!-- RIGHT SIDE PANEL (Barcodes & Certifications) -->
            <g id="panel-right-side" style="cursor:pointer;">
                <rect x="480" y="100" width="180" height="250" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="570" y="122" fill="#38BDF8" font-size="10.5" font-weight="700" text-anchor="middle">RIGHT PANEL (Specs &amp; Barcode)</text>

                <!-- UPC Barcode -->
                <rect x="500" y="140" width="140" height="65" fill="white" rx="4"/>
                <line x1="515" y1="148" x2="515" y2="185" stroke="black" stroke-width="2"/>
                <line x1="520" y1="148" x2="520" y2="185" stroke="black" stroke-width="3"/>
                <line x1="528" y1="148" x2="528" y2="185" stroke="black" stroke-width="1"/>
                <line x1="535" y1="148" x2="535" y2="185" stroke="black" stroke-width="4"/>
                <line x1="545" y1="148" x2="545" y2="185" stroke="black" stroke-width="2"/>
                <line x1="555" y1="148" x2="555" y2="185" stroke="black" stroke-width="3"/>
                <line x1="565" y1="148" x2="565" y2="185" stroke="black" stroke-width="1.5"/>
                <line x1="575" y1="148" x2="575" y2="185" stroke="black" stroke-width="3"/>
                <text x="570" y="196" fill="black" font-size="8" font-family="monospace" text-anchor="middle">{barcode}</text>

                <!-- Hotspot Pin: Quiet Zone -->
                <circle cx="630" cy="150" r="7.5" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="630" y="153" fill="white" font-size="8" font-weight="900" text-anchor="middle">!</text>

                <!-- Recycling Typo callout -->
                <rect x="500" y="215" width="140" height="40" fill="#1E293B" stroke="#F59E0B" rx="4"/>
                <text x="570" y="230" fill="#F59E0B" font-size="7.5" font-weight="700" text-anchor="middle">❌ Typo: 'RECYCABLE'</text>
                <text x="570" y="244" fill="#10B981" font-size="7" font-weight="700" text-anchor="middle">➜ Correct to 'RECYCLABLE'</text>

                <!-- Hotspot Pin: Typo -->
                <circle cx="630" cy="228" r="7.5" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="630" y="231" fill="white" font-size="8" font-weight="900" text-anchor="middle">!</text>

                <!-- Substrate callout -->
                <rect x="500" y="265" width="140" height="75" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="570" y="282" fill="#38BDF8" font-size="7.5" font-weight="700" text-anchor="middle">Substrate Specification</text>
                <text x="570" y="298" fill="#94A3B8" font-size="7" text-anchor="middle">FSC-Certified 18pt SBS Caliper</text>
                <text x="570" y="314" fill="#94A3B8" font-size="6.5" text-anchor="middle">Matte Aqueous + Spot UV Logo</text>
            </g>

            <!-- BACK PANEL (Formulation, Story, Claims) -->
            <g id="panel-back" style="cursor:pointer;">
                <rect x="660" y="100" width="220" height="250" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
                <text x="770" y="122" fill="#38BDF8" font-size="11.5" font-weight="800" text-anchor="middle">BACK PANEL (Formulation &amp; Story)</text>

                <!-- Brand Story -->
                <rect x="675" y="135" width="190" height="28" fill="#0F172A" rx="4"/>
                <text x="770" y="152" fill="#F8FAFC" font-size="7" font-weight="700" text-anchor="middle">"{facts.get('brand_copywriting', 'Start tapping, swishing & shaking your tail fins!')[:38]}..."</text>

                <!-- Ingredients Deck Mockup -->
                <rect x="675" y="170" width="190" height="58" fill="#0F172A" rx="4"/>
                <text x="682" y="184" fill="#F59E0B" font-size="7" font-weight="700">AUTHORIZED FORMULA (Honey 1% vs 9%):</text>
                <text x="682" y="197" fill="#CBD5E1" font-size="6.5">Organic Oat Flakes (79%), Almonds, Pecans, Walnuts,</text>
                <text x="682" y="208" fill="#CBD5E1" font-size="6.5">Flax, Berries, Honey (1%), Coconut Sugar, Ginger...</text>
                <text x="682" y="220" fill="#10B981" font-size="6.5" font-weight="700">✅ Authorized Master Deck Verified</text>

                <!-- Hotspot Pin: Formula Conflict -->
                <circle cx="855" cy="180" r="9" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="855" y="184" fill="white" font-size="10" font-weight="900" text-anchor="middle">!</text>

                <!-- Contradiction Badges -->
                <rect x="675" y="234" width="90" height="44" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="720" y="248" fill="#EF4444" font-size="7" font-weight="800" text-anchor="middle">❌ PURGE CLAIM</text>
                <text x="720" y="262" fill="#CBD5E1" font-size="6" text-anchor="middle">Certified Vegan</text>
                <text x="720" y="271" fill="#FCA5A5" font-size="5.5" text-anchor="middle">(Honey included)</text>

                <rect x="775" y="234" width="90" height="44" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="820" y="248" fill="#EF4444" font-size="7" font-weight="800" text-anchor="middle">❌ STRIP LOZENGES</text>
                <text x="820" y="262" fill="#CBD5E1" font-size="6" text-anchor="middle">UK Traffic Lights</text>
                <text x="820" y="271" fill="#FCA5A5" font-size="5.5" text-anchor="middle">on US packaging</text>

                <!-- Hotspot Pin: UK Lozenges -->
                <circle cx="855" cy="242" r="7.5" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="855" y="245" fill="white" font-size="8" font-weight="900" text-anchor="middle">!</text>

                <!-- Storage Copy -->
                <rect x="675" y="286" width="190" height="54" fill="#0F172A" rx="4"/>
                <text x="770" y="302" fill="#94A3B8" font-size="6.5" text-anchor="middle">Store in a cool dry place. Keep closed once opened.</text>
                <text x="770" y="316" fill="#38BDF8" font-size="6.5" font-weight="700" text-anchor="middle">For Best Before See Base of Pack</text>
            </g>

            <!-- TOP FLAP (Tuck Flap & Dust Flaps) -->
            <g id="panel-top-flap">
                <polygon points="260,100 280,20 440,20 460,100" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="360" y="55" fill="#38BDF8" font-size="9.5" font-weight="800" text-anchor="middle">TOP TUCK FLAP</text>
                <rect x="295" y="65" width="130" height="28" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="360" y="78" fill="#EF4444" font-size="7.5" font-weight="900" text-anchor="middle">❌ DELETE: 'NO ADDED SUGAR'</text>
                <text x="360" y="88" fill="#FCA5A5" font-size="6" text-anchor="middle">Violates FDA 21 CFR 101.60(c)(2)</text>
                
                <!-- Hotspot Pin: Top Flap -->
                <circle cx="420" cy="78" r="9" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="420" y="82" fill="white" font-size="10" font-weight="900" text-anchor="middle">!</text>

                <!-- Dust Flaps -->
                <polygon points="80,100 100,45 240,45 260,100" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <text x="170" y="75" fill="#64748B" font-size="7.5" text-anchor="middle">Dust Flap L</text>

                <polygon points="480,100 500,45 640,45 660,100" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <text x="570" y="75" fill="#64748B" font-size="7.5" text-anchor="middle">Dust Flap R</text>
            </g>

            <!-- BOTTOM FLAPS -->
            <g id="panel-bottom-flap">
                <polygon points="260,350 280,430 440,430 460,350" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="360" y="388" fill="#94A3B8" font-size="8.5" font-weight="700" text-anchor="middle">BOTTOM FLAP (Base of Pack)</text>
                <text x="360" y="405" fill="#64748B" font-size="7.5" text-anchor="middle">Inkjet Date Code &amp; Lot Number Window (15 x 30 mm)</text>

                <polygon points="80,350 100,415 240,415 260,350" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <polygon points="480,350 500,415 640,415 660,350" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
            </g>

            <!-- MECHANICAL DIELINE GUIDELINES (CREASE LINES) -->
            <line x1="80" y1="100" x2="880" y2="100" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="80" y1="350" x2="880" y2="350" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="260" y1="100" x2="260" y2="350" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="480" y1="100" x2="480" y2="350" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="660" y1="100" x2="660" y2="350" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
        </svg>

        <div style="margin-top:12px; display:grid; grid-template-columns: repeat(4, 1fr); gap:8px; font-size:11px;">
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:8px 10px; border-radius:5px;">
                <strong style="color:#EF4444;">1. Top Flap:</strong> Purge illegal 'NO ADDED SUGAR' claim badge per 21 CFR 101.60.
            </div>
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:8px 10px; border-radius:5px;">
                <strong style="color:#EF4444;">2. Left Panel:</strong> Fix 'DIETRAY' typo, standardize 60g serving &amp; declare true added sugars.
            </div>
            <div style="background:#1E293B; border-left:3px solid #10B981; padding:8px 10px; border-radius:5px;">
                <strong style="color:#10B981;">3. PDP (Front):</strong> Position dual Net Quantity {net_wt} in lower 30% per 21 CFR 101.7.
            </div>
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:8px 10px; border-radius:5px;">
                <strong style="color:#EF4444;">4. Back Panel:</strong> Elevate tree nuts to bold 'CONTAINS:', purge UK traffic lights &amp; vegan mark.
            </div>
        </div>
    </div>
    """
    return html
