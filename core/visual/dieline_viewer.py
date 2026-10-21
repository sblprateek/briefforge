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
    <div style="background:#0F172A; border-radius:12px; padding:20px; color:white; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
            <div>
                <span style="font-size:11px; font-weight:800; color:#38BDF8; letter-spacing:0.1em; text-transform:uppercase;">Esko ArtiosCAD-Grade Mechanical Net</span>
                <h3 style="margin:2px 0 0 0; color:white; font-size:16px;">Interactive 2D Folding Carton Dieline Inspector</h3>
                <div style="font-size:11px; color:#94A3B8;">Hover over panel hotspot pins (!) to inspect statutory violations &amp; mechanical guidelines</div>
            </div>
            <div style="display:flex; gap:14px; font-size:11.5px; background:#1E293B; padding:6px 12px; border-radius:6px; border:1px solid #334155;">
                <span style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:10px; height:10px; background:#EF4444; border-radius:50%;"></span> Critical Defect (8)</span>
                <span style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:10px; height:10px; background:#F59E0B; border-radius:50%;"></span> Pre-Press Warning (4)</span>
                <span style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:10px; height:10px; background:#10B981; border-radius:50%;"></span> Verified Production Spec</span>
            </div>
        </div>

        <svg viewBox="0 0 940 540" style="width:100%; height:auto; background:#1E293B; border-radius:8px; border:1px solid #334155;">
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
                <polygon points="40,160 80,140 80,400 40,380" fill="#1E293B" stroke="#64748B" stroke-dasharray="4,4" stroke-width="1.5"/>
                <text x="60" y="275" fill="#94A3B8" font-size="10" font-weight="700" transform="rotate(-90 60 275)" text-anchor="middle">GLUE TAB (Adhesive Window 15mm)</text>
            </g>

            <!-- LEFT SIDE PANEL (Nutrition & Allergens) -->
            <g id="panel-left-side" style="cursor:pointer;">
                <rect x="80" y="140" width="180" height="260" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="170" y="165" fill="#38BDF8" font-size="11" font-weight="700" text-anchor="middle">LEFT PANEL (Nutrition &amp; Allergens)</text>
                
                <!-- Nutrition Box Mockup -->
                <rect x="95" y="180" width="150" height="145" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="105" y="198" fill="white" font-size="10" font-weight="800">Nutrition Facts</text>
                <text x="105" y="212" fill="#38BDF8" font-size="8.5">8 servings per container (60g)</text>
                <text x="105" y="228" fill="#CBD5E1" font-size="8.5">Calories 166</text>
                <text x="105" y="246" fill="#EF4444" font-size="8" font-weight="800">❌ Typo: 'DIETRAY FIBER'</text>
                <text x="105" y="262" fill="#EF4444" font-size="8" font-weight="800">❌ Declared 0g Added Sugars</text>
                <text x="105" y="278" fill="#10B981" font-size="8" font-weight="700">➜ Correct to 7g Added Sugars</text>

                <!-- Hotspot Pin: Nutrition Typo & Sugars -->
                <circle cx="230" cy="195" r="10" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="230" y="199" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>

                <!-- Hotspot Pin: Serving size -->
                <circle cx="230" cy="225" r="8" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="230" y="228" fill="white" font-size="9" font-weight="900" text-anchor="middle">!</text>

                <!-- Allergen Box -->
                <rect x="95" y="335" width="150" height="55" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="102" y="350" fill="#F59E0B" font-size="8" font-weight="700">⚠️ Allergen Formatting:</text>
                <text x="102" y="365" fill="#CBD5E1" font-size="7">Mandate bold 'CONTAINS:' statement</text>
                <text x="102" y="378" fill="#10B981" font-size="7" font-weight="700">Tree nuts: Almonds, Pecans, Walnuts</text>
            </g>

            <!-- FRONT PANEL (Principal Display Panel / PDP) -->
            <g id="panel-front-pdp" style="cursor:pointer;">
                <rect x="260" y="140" width="220" height="260" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
                <text x="370" y="165" fill="#38BDF8" font-size="12" font-weight="800" text-anchor="middle">FRONT PANEL (Principal Display Panel)</text>

                <!-- Brand & Artwork Mockup -->
                <rect x="295" y="180" width="150" height="30" rx="4" fill="#2563EB"/>
                <text x="370" y="200" fill="white" font-size="13" font-weight="900" text-anchor="middle">{brand}</text>
                <text x="370" y="222" fill="#F8FAFC" font-size="10" font-weight="700" text-anchor="middle">{product}</text>

                <!-- Illustration / Photography area -->
                <circle cx="370" cy="270" r="36" fill="#334155" stroke="#64748B"/>
                <text x="370" y="268" fill="#94A3B8" font-size="7.5" text-anchor="middle">Cereal Bowl Photo</text>
                <text x="370" y="280" fill="#94A3B8" font-size="6.5" text-anchor="middle">(Fresh Berries Shown)</text>

                <!-- Hotspot Pin: Missing Serving Suggestion -->
                <circle cx="415" cy="265" r="10" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="415" y="269" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>
                <text x="370" y="316" fill="#F59E0B" font-size="7.5" font-weight="700" text-anchor="middle">+ Add: 'Serving Suggestion. Fresh fruit not included.'</text>

                <!-- Hotspot Pin: Certified Vegan Badge Conflict -->
                <circle cx="310" cy="235" r="10" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="310" y="239" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>
                <text x="310" y="252" fill="#EF4444" font-size="6.5" font-weight="800">❌ VEGAN BADGE</text>

                <!-- Lower 30% Net Weight Target Zone -->
                <rect x="270" y="335" width="200" height="55" fill="#0F172A" stroke="#EF4444" stroke-dasharray="3,3" rx="4"/>
                <text x="370" y="352" fill="#EF4444" font-size="8" font-weight="800" text-anchor="middle">MANDATORY NET QUANTITY ZONE (21 CFR 101.7)</text>
                <text x="370" y="372" fill="#10B981" font-size="10" font-weight="900" text-anchor="middle">{net_wt}</text>

                <!-- Hotspot Pin: Net weight location -->
                <circle cx="455" cy="355" r="9" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="455" y="358" fill="white" font-size="10" font-weight="900" text-anchor="middle">!</text>
            </g>

            <!-- RIGHT SIDE PANEL (Barcodes & Certifications) -->
            <g id="panel-right-side" style="cursor:pointer;">
                <rect x="480" y="140" width="180" height="260" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="570" y="165" fill="#38BDF8" font-size="11" font-weight="700" text-anchor="middle">RIGHT PANEL (Specs &amp; Barcode)</text>

                <!-- UPC Barcode -->
                <rect x="500" y="185" width="140" height="70" fill="white" rx="4"/>
                <line x1="515" y1="195" x2="515" y2="235" stroke="black" stroke-width="2"/>
                <line x1="520" y1="195" x2="520" y2="235" stroke="black" stroke-width="3"/>
                <line x1="528" y1="195" x2="528" y2="235" stroke="black" stroke-width="1"/>
                <line x1="535" y1="195" x2="535" y2="235" stroke="black" stroke-width="4"/>
                <line x1="545" y1="195" x2="545" y2="235" stroke="black" stroke-width="2"/>
                <line x1="555" y1="195" x2="555" y2="235" stroke="black" stroke-width="3"/>
                <line x1="565" y1="195" x2="565" y2="235" stroke="black" stroke-width="1.5"/>
                <line x1="575" y1="195" x2="575" y2="235" stroke="black" stroke-width="3"/>
                <text x="570" y="248" fill="black" font-size="8.5" font-family="monospace" text-anchor="middle">{barcode}</text>

                <!-- Hotspot Pin: Quiet Zone -->
                <circle cx="630" cy="195" r="8" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="630" y="198" fill="white" font-size="9" font-weight="900" text-anchor="middle">!</text>

                <!-- Recycling Typo callout -->
                <rect x="500" y="270" width="140" height="42" fill="#1E293B" stroke="#F59E0B" rx="4"/>
                <text x="570" y="286" fill="#F59E0B" font-size="8" font-weight="700" text-anchor="middle">❌ Typo: 'RECYCABLE'</text>
                <text x="570" y="302" fill="#10B981" font-size="7.5" font-weight="700" text-anchor="middle">➜ Correct to 'RECYCLABLE'</text>

                <!-- Hotspot Pin: Typo -->
                <circle cx="630" cy="285" r="8" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="630" y="288" fill="white" font-size="9" font-weight="900" text-anchor="middle">!</text>

                <!-- Substrate callout -->
                <rect x="500" y="325" width="140" height="65" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="570" y="342" fill="#38BDF8" font-size="8" font-weight="700" text-anchor="middle">Substrate Specification</text>
                <text x="570" y="358" fill="#94A3B8" font-size="7.5" text-anchor="middle">FSC-Certified 18pt SBS Caliper</text>
                <text x="570" y="374" fill="#94A3B8" font-size="7" text-anchor="middle">Matte Aqueous + Spot UV Logo</text>
            </g>

            <!-- BACK PANEL (Formulation, Story, Claims) -->
            <g id="panel-back" style="cursor:pointer;">
                <rect x="660" y="140" width="220" height="260" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
                <text x="770" y="165" fill="#38BDF8" font-size="12" font-weight="800" text-anchor="middle">BACK PANEL (Formulation &amp; Story)</text>

                <!-- Brand Story -->
                <rect x="675" y="180" width="190" height="30" fill="#0F172A" rx="4"/>
                <text x="770" y="198" fill="#F8FAFC" font-size="7.5" font-weight="700" text-anchor="middle">"{facts.get('brand_copywriting', 'Start tapping, swishing & shaking your tail fins!')[:42]}..."</text>

                <!-- Ingredients Deck Mockup -->
                <rect x="675" y="218" width="190" height="60" fill="#0F172A" rx="4"/>
                <text x="682" y="232" fill="#F59E0B" font-size="7.5" font-weight="700">AUTHORIZED FORMULA (Honey 1% vs 9%):</text>
                <text x="682" y="246" fill="#CBD5E1" font-size="6.5">Organic Oat Flakes (79%), Almonds, Pecans, Walnuts,</text>
                <text x="682" y="258" fill="#CBD5E1" font-size="6.5">Flax, Berries, Honey (1%), Coconut Sugar, Ginger...</text>
                <text x="682" y="271" fill="#10B981" font-size="7" font-weight="700">✅ Authorized Master Deck Verified</text>

                <!-- Hotspot Pin: Formula Conflict -->
                <circle cx="855" cy="225" r="10" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="855" y="229" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>

                <!-- Contradiction Badges -->
                <rect x="675" y="286" width="90" height="48" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="720" y="302" fill="#EF4444" font-size="7.5" font-weight="800" text-anchor="middle">❌ PURGE CLAIM</text>
                <text x="720" y="318" fill="#CBD5E1" font-size="6.5" text-anchor="middle">Certified Vegan</text>
                <text x="720" y="328" fill="#FCA5A5" font-size="6" text-anchor="middle">(Honey included)</text>

                <rect x="775" y="286" width="90" height="48" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="820" y="302" fill="#EF4444" font-size="7.5" font-weight="800" text-anchor="middle">❌ STRIP LOZENGES</text>
                <text x="820" y="318" fill="#CBD5E1" font-size="6.5" text-anchor="middle">UK Traffic Lights</text>
                <text x="820" y="328" fill="#FCA5A5" font-size="6" text-anchor="middle">on US packaging</text>

                <!-- Hotspot Pin: UK Lozenges -->
                <circle cx="855" cy="295" r="8" fill="#F59E0B" filter="url(#glow-amber)"/>
                <text x="855" y="298" fill="white" font-size="9" font-weight="900" text-anchor="middle">!</text>

                <!-- Storage Copy -->
                <rect x="675" y="342" width="190" height="48" fill="#0F172A" rx="4"/>
                <text x="770" y="358" fill="#94A3B8" font-size="7" text-anchor="middle">Store in a cool dry place. Keep closed once opened.</text>
                <text x="770" y="374" fill="#38BDF8" font-size="7" font-weight="700" text-anchor="middle">For Best Before See Base of Pack</text>
            </g>

            <!-- TOP FLAP (Tuck Flap & Dust Flaps) -->
            <g id="panel-top-flap">
                <polygon points="260,140 280,40 440,40 460,140" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="360" y="80" fill="#38BDF8" font-size="10" font-weight="800" text-anchor="middle">TOP TUCK FLAP</text>
                <rect x="295" y="92" width="130" height="30" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="360" y="108" fill="#EF4444" font-size="8" font-weight="900" text-anchor="middle">❌ DELETE: 'NO ADDED SUGAR'</text>
                <text x="360" y="118" fill="#FCA5A5" font-size="6.5" text-anchor="middle">Violates FDA 21 CFR 101.60(c)(2)</text>
                
                <!-- Hotspot Pin: Top Flap -->
                <circle cx="420" cy="107" r="10" fill="#EF4444" filter="url(#glow-red)"/>
                <text x="420" y="111" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>

                <!-- Dust Flaps -->
                <polygon points="80,140 100,70 240,70 260,140" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <text x="170" y="110" fill="#64748B" font-size="8" text-anchor="middle">Dust Flap L</text>

                <polygon points="480,140 500,70 640,70 660,140" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <text x="570" y="110" fill="#64748B" font-size="8" text-anchor="middle">Dust Flap R</text>
            </g>

            <!-- BOTTOM FLAPS -->
            <g id="panel-bottom-flap">
                <polygon points="260,400 280,490 440,490 460,400" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="360" y="440" fill="#94A3B8" font-size="9" font-weight="700" text-anchor="middle">BOTTOM FLAP (Base of Pack)</text>
                <text x="360" y="460" fill="#64748B" font-size="8" text-anchor="middle">Inkjet Date Code &amp; Lot Number Window (15 x 30 mm)</text>

                <polygon points="80,400 100,470 240,470 260,400" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <polygon points="480,400 500,470 640,470 660,400" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
            </g>

            <!-- MECHANICAL DIELINE GUIDELINES (CREASE LINES) -->
            <line x1="80" y1="140" x2="880" y2="140" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="80" y1="400" x2="880" y2="400" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="260" y1="140" x2="260" y2="400" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="480" y1="140" x2="480" y2="400" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
            <line x1="660" y1="140" x2="660" y2="400" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="5,3"/>
        </svg>

        <div style="margin-top:14px; display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; font-size:12px;">
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:9px 12px; border-radius:6px;">
                <strong style="color:#EF4444;">1. Top Flap:</strong> Purge illegal 'NO ADDED SUGAR' claim badge per 21 CFR 101.60.
            </div>
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:9px 12px; border-radius:6px;">
                <strong style="color:#EF4444;">2. Left Panel:</strong> Fix 'DIETRAY' typo, standardized 60g serving &amp; declare true added sugars.
            </div>
            <div style="background:#1E293B; border-left:3px solid #10B981; padding:9px 12px; border-radius:6px;">
                <strong style="color:#10B981;">3. PDP (Front):</strong> Position dual Net Quantity {net_wt} in lower 30% per 21 CFR 101.7.
            </div>
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:9px 12px; border-radius:6px;">
                <strong style="color:#EF4444;">4. Back Panel:</strong> Elevate tree nuts to bold 'CONTAINS:', purge UK traffic lights &amp; vegan mark.
            </div>
        </div>
    </div>
    """
    return html
