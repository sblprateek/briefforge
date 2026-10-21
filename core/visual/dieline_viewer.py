"""
BriefForge Interactive Visual Dieline Inspector
Renders an interactive SVG folding carton net with defect pins, mechanical panel boundaries,
and side-by-side remediation annotations.
"""

from typing import List, Dict, Any


def render_interactive_dieline(issues: List[Any], active_panel: str = "all") -> str:
    """
    Generates a responsive SVG folding carton net with panel zones,
    mechanical crease lines, and interactive defect hotspot markers.
    """
    
    html = """
    <div style="background:#0F172A; border-radius:12px; padding:20px; color:white; font-family:-apple-system, sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <div>
                <span style="font-size:11px; font-weight:800; color:#38BDF8; letter-spacing:0.1em; text-transform:uppercase;">Esko ArtiosCAD-Grade Mechanical Net</span>
                <h3 style="margin:2px 0 0 0; color:white; font-size:16px;">Interactive Folding Carton Dieline Inspector</h3>
            </div>
            <div style="display:flex; gap:12px; font-size:11px;">
                <span style="display:flex; align-items:center; gap:4px;"><span style="display:inline-block; width:10px; height:10px; background:#EF4444; border-radius:50%;"></span> Critical Defect</span>
                <span style="display:flex; align-items:center; gap:4px;"><span style="display:inline-block; width:10px; height:10px; background:#F59E0B; border-radius:50%;"></span> Pre-Press Warning</span>
                <span style="display:flex; align-items:center; gap:4px;"><span style="display:inline-block; width:10px; height:10px; background:#10B981; border-radius:50%;"></span> Verified Spec</span>
            </div>
        </div>

        <svg viewBox="0 0 940 540" style="width:100%; height:auto; background:#1E293B; border-radius:8px; border:1px solid #334155;">
            <!-- Definitions for markers and patterns -->
            <defs>
                <pattern id="crease" width="8" height="8" patternUnits="userSpaceOnUse">
                    <line x1="0" y1="0" x2="0" y2="8" stroke="#475569" stroke-width="1" stroke-dasharray="2,2"/>
                </pattern>
                <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>

            <!-- GLUE TAB (Far Left) -->
            <g id="panel-glue-tab">
                <polygon points="40,160 80,140 80,400 40,380" fill="#1E293B" stroke="#64748B" stroke-dasharray="4,4" stroke-width="1.5"/>
                <text x="60" y="275" fill="#94A3B8" font-size="10" font-weight="700" transform="rotate(-90 60 275)" text-anchor="middle">GLUE TAB (Adhesive Window)</text>
            </g>

            <!-- LEFT SIDE PANEL (Nutrition & Allergens) -->
            <g id="panel-left-side" style="cursor:pointer;">
                <rect x="80" y="140" width="180" height="260" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="170" y="165" fill="#38BDF8" font-size="11" font-weight="700" text-anchor="middle">LEFT PANEL (Nutrition & Allergens)</text>
                
                <!-- Mockup Nutrition Box -->
                <rect x="95" y="180" width="150" height="150" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="105" y="200" fill="white" font-size="10" font-weight="800">Nutrition Facts</text>
                <text x="105" y="215" fill="#EF4444" font-size="9" font-weight="700">8 servings per container (60g)</text>
                <text x="105" y="235" fill="#CBD5E1" font-size="8">Calories 166</text>
                <text x="105" y="250" fill="#EF4444" font-size="8" font-weight="700">❌ Typo: 'DIETRAY FIBER'</text>
                <text x="105" y="265" fill="#EF4444" font-size="8" font-weight="700">❌ Added Sugars: Declared 0g (False)</text>
                <text x="105" y="285" fill="#38BDF8" font-size="8">Footnote 2,000 cal advice</text>

                <!-- Allergen Box -->
                <rect x="95" y="340" width="150" height="48" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="102" y="355" fill="#F59E0B" font-size="8" font-weight="700">⚠️ Allergen Formatting:</text>
                <text x="102" y="370" fill="#CBD5E1" font-size="7">Must mandate bold 'CONTAINS:' statement</text>

                <!-- Defect Pin -->
                <circle cx="230" cy="195" r="10" fill="#EF4444" filter="url(#glow)"/>
                <text x="230" y="199" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>
            </g>

            <!-- FRONT PANEL (Principal Display Panel / PDP) -->
            <g id="panel-front-pdp" style="cursor:pointer;">
                <rect x="260" y="140" width="220" height="260" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
                <text x="370" y="165" fill="#38BDF8" font-size="12" font-weight="800" text-anchor="middle">FRONT PANEL (Principal Display Panel)</text>

                <!-- Brand & Artwork Mockup -->
                <rect x="300" y="180" width="140" height="30" rx="4" fill="#2563EB"/>
                <text x="370" y="200" fill="white" font-size="13" font-weight="900" text-anchor="middle">DANCING FISH</text>
                <text x="370" y="222" fill="#F8FAFC" font-size="10" font-weight="700" text-anchor="middle">Granola Berry Crunch</text>

                <!-- Illustration / Photography area -->
                <circle cx="370" cy="270" r="36" fill="#334155" stroke="#64748B"/>
                <text x="370" y="274" fill="#94A3B8" font-size="8" text-anchor="middle">Cereal Bowl Photo</text>

                <!-- Defect Pin: Missing Serving Suggestion -->
                <circle cx="415" cy="265" r="10" fill="#F59E0B" filter="url(#glow)"/>
                <text x="415" y="269" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>
                <text x="370" y="318" fill="#F59E0B" font-size="7.5" font-weight="700" text-anchor="middle">+ Add: 'Serving Suggestion. Fresh fruit not included.'</text>

                <!-- Lower 30% Net Weight Target Zone -->
                <rect x="270" y="340" width="200" height="50" fill="#0F172A" stroke="#EF4444" stroke-dasharray="3,3" rx="4"/>
                <text x="370" y="360" fill="#EF4444" font-size="8.5" font-weight="800" text-anchor="middle">MANDATORY NET QUANTITY ZONE (21 CFR 101.7)</text>
                <text x="370" y="378" fill="#10B981" font-size="10" font-weight="900" text-anchor="middle">NET WT 16.9 OZ (480g)</text>
            </g>

            <!-- RIGHT SIDE PANEL (Barcodes & Certifications) -->
            <g id="panel-right-side" style="cursor:pointer;">
                <rect x="480" y="140" width="180" height="260" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="570" y="165" fill="#38BDF8" font-size="11" font-weight="700" text-anchor="middle">RIGHT PANEL (Specs & Barcode)</text>

                <!-- UPC Barcode -->
                <rect x="500" y="190" width="140" height="65" fill="white" rx="4"/>
                <line x1="515" y1="200" x2="515" y2="235" stroke="black" stroke-width="2"/>
                <line x1="520" y1="200" x2="520" y2="235" stroke="black" stroke-width="3"/>
                <line x1="528" y1="200" x2="528" y2="235" stroke="black" stroke-width="1"/>
                <line x1="535" y1="200" x2="535" y2="235" stroke="black" stroke-width="4"/>
                <line x1="545" y1="200" x2="545" y2="235" stroke="black" stroke-width="2"/>
                <line x1="555" y1="200" x2="555" y2="235" stroke="black" stroke-width="3"/>
                <line x1="565" y1="200" x2="565" y2="235" stroke="black" stroke-width="1.5"/>
                <line x1="575" y1="200" x2="575" y2="235" stroke="black" stroke-width="3"/>
                <text x="570" y="248" fill="black" font-size="8" font-family="monospace" text-anchor="middle">1 20000 00003 6</text>

                <!-- Recycling Typo callout -->
                <rect x="500" y="275" width="140" height="40" fill="#1E293B" stroke="#F59E0B" rx="4"/>
                <text x="570" y="292" fill="#F59E0B" font-size="8" font-weight="700" text-anchor="middle">❌ Typo: 'RECYCABLE'</text>
                <text x="570" y="306" fill="#10B981" font-size="7.5" font-weight="700" text-anchor="middle">➜ Correct to 'RECYCLABLE'</text>

                <!-- Substrate callout -->
                <rect x="500" y="330" width="140" height="55" fill="#1E293B" stroke="#475569" rx="4"/>
                <text x="570" y="348" fill="#94A3B8" font-size="7.5" font-weight="700" text-anchor="middle">FSC 18pt SBS Caliper</text>
                <text x="570" y="362" fill="#94A3B8" font-size="7" text-anchor="middle">Matte Aqueous + Spot UV</text>
            </g>

            <!-- BACK PANEL (Formulation, Story, Claims) -->
            <g id="panel-back" style="cursor:pointer;">
                <rect x="660" y="140" width="220" height="260" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
                <text x="770" y="165" fill="#38BDF8" font-size="12" font-weight="800" text-anchor="middle">BACK PANEL (Formulation & Story)</text>

                <!-- Brand Story -->
                <rect x="675" y="180" width="190" height="35" fill="#0F172A" rx="4"/>
                <text x="770" y="196" fill="#F8FAFC" font-size="8" font-weight="700" text-anchor="middle">"Start tapping, swishing & shaking your tail fins!"</text>
                <text x="770" y="208" fill="#38BDF8" font-size="7" text-anchor="middle">PACKED WITH GOODNESS (Artisan Grain)</text>

                <!-- Ingredients Deck Mockup -->
                <rect x="675" y="222" width="190" height="60" fill="#0F172A" rx="4"/>
                <text x="682" y="235" fill="#94A3B8" font-size="7.5" font-weight="700">AUTHORIZED FORMULA (Honey 1% vs 9%):</text>
                <text x="682" y="248" fill="#CBD5E1" font-size="6.5">Organic Oat Flakes (79%), Almonds, Pecans, Walnuts,</text>
                <text x="682" y="258" fill="#CBD5E1" font-size="6.5">Flax, Berries, Honey (1%), Coconut Sugar, Ginger...</text>
                <text x="682" y="272" fill="#10B981" font-size="7" font-weight="700">✅ Recipe Verified by Brand Manager</text>

                <!-- Contradiction Badges -->
                <rect x="675" y="290" width="90" height="45" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="720" y="306" fill="#EF4444" font-size="7" font-weight="800" text-anchor="middle">❌ DELETE CLAIM</text>
                <text x="720" y="320" fill="#CBD5E1" font-size="6" text-anchor="middle">Certified Vegan (Honey)</text>

                <rect x="775" y="290" width="90" height="45" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="820" y="306" fill="#EF4444" font-size="7" font-weight="800" text-anchor="middle">❌ STRIP LOZENGES</text>
                <text x="820" y="320" fill="#CBD5E1" font-size="6" text-anchor="middle">UK Traffic Lights on US pack</text>

                <!-- Storage Copy -->
                <rect x="675" y="345" width="190" height="42" fill="#0F172A" rx="4"/>
                <text x="770" y="362" fill="#94A3B8" font-size="7" text-anchor="middle">Store in a cool dry place. Keep closed once opened.</text>
                <text x="770" y="376" fill="#38BDF8" font-size="7" font-weight="700" text-anchor="middle">For Best Before See Base of Pack</text>

                <!-- Defect Pin -->
                <circle cx="855" cy="195" r="10" fill="#EF4444" filter="url(#glow)"/>
                <text x="855" y="199" fill="white" font-size="11" font-weight="900" text-anchor="middle">!</text>
            </g>

            <!-- TOP FLAP (Tuck Flap & Dust Flaps) -->
            <g id="panel-top-flap">
                <polygon points="260,140 280,40 440,40 460,140" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="360" y="85" fill="#38BDF8" font-size="10" font-weight="800" text-anchor="middle">TOP TUCK FLAP</text>
                <rect x="300" y="95" width="120" height="25" fill="#1E293B" stroke="#EF4444" rx="4"/>
                <text x="360" y="112" fill="#EF4444" font-size="8" font-weight="900" text-anchor="middle">❌ DELETE: 'NO ADDED SUGAR'</text>
                <circle cx="420" cy="107" r="8" fill="#EF4444" filter="url(#glow)"/>
                <text x="420" y="110" fill="white" font-size="9" font-weight="900" text-anchor="middle">!</text>

                <!-- Dust Flaps -->
                <polygon points="80,140 100,70 240,70 260,140" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <text x="170" y="110" fill="#64748B" font-size="8" text-anchor="middle">Dust Flap L</text>

                <polygon points="480,140 500,70 640,70 660,140" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <text x="570" y="110" fill="#64748B" font-size="8" text-anchor="middle">Dust Flap R</text>
            </g>

            <!-- BOTTOM FLAPS -->
            <g id="panel-bottom-flap">
                <polygon points="260,400 280,490 440,490 460,400" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                <text x="360" y="445" fill="#94A3B8" font-size="9" font-weight="700" text-anchor="middle">BOTTOM FLAP (Base of Pack)</text>
                <text x="360" y="465" fill="#64748B" font-size="8" text-anchor="middle">Inkjet Date Code &amp; Lot Number Window</text>

                <polygon points="80,400 100,470 240,470 260,400" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
                <polygon points="480,400 500,470 640,470 660,400" fill="#1E293B" stroke="#64748B" stroke-dasharray="3,3"/>
            </g>

            <!-- MECHANICAL DIELINE GUIDELINES (CREASE LINES) -->
            <line x1="80" y1="140" x2="880" y2="140" stroke="#EF4444" stroke-width="1" stroke-dasharray="5,3"/>
            <line x1="80" y1="400" x2="880" y2="400" stroke="#EF4444" stroke-width="1" stroke-dasharray="5,3"/>
            <line x1="260" y1="140" x2="260" y2="400" stroke="#EF4444" stroke-width="1" stroke-dasharray="5,3"/>
            <line x1="480" y1="140" x2="480" y2="400" stroke="#EF4444" stroke-width="1" stroke-dasharray="5,3"/>
            <line x1="660" y1="140" x2="660" y2="400" stroke="#EF4444" stroke-width="1" stroke-dasharray="5,3"/>
        </svg>

        <div style="margin-top:12px; display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; font-size:12px;">
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:8px 10px; border-radius:4px;">
                <strong style="color:#EF4444;">Top Flap:</strong> Purge 'NO ADDED SUGAR' badge.
            </div>
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:8px 10px; border-radius:4px;">
                <strong style="color:#EF4444;">Left Panel:</strong> Recalculate added sugars &amp; fix 'DIETRAY'.
            </div>
            <div style="background:#1E293B; border-left:3px solid #10B981; padding:8px 10px; border-radius:4px;">
                <strong style="color:#10B981;">PDP (Front):</strong> Position NET WT 16.9 OZ (480g) in lower 30%.
            </div>
            <div style="background:#1E293B; border-left:3px solid #EF4444; padding:8px 10px; border-radius:4px;">
                <strong style="color:#EF4444;">Back Panel:</strong> Remove Certified Vegan logo &amp; UK lozenges.
            </div>
        </div>
    </div>
    """
    return html
