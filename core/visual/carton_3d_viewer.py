"""
BriefForge 3D Folded Carton WebGL Simulator (Esko Studio Grade)
Renders an interactive, dynamic 3D folding carton in Three.js with 360-degree orbital rotation,
interactive Before/After remediation toggle, dynamic product metadata injection,
and preset camera inspection views.
"""

import json
from typing import Optional, Dict, Any


def render_3d_carton_html(facts: Optional[Dict[str, Any]] = None, brief: Optional[Any] = None, initial_mode: str = "remediated") -> str:
    """
    Renders a self-contained WebGL 3D folding carton simulator with Three.js.
    Supports dynamic data injection from extracted facts and interactive Defective vs. Remediated modes.
    """
    if facts is None:
        facts = {}
        
    brand_name = facts.get("brand", "DANCING FISH").upper()
    product_name = facts.get("product_name", "GRANOLA BERRY CRUNCH").upper()
    net_weight = facts.get("declared_net_quantity", "NET WT 16.9 OZ (480g)")
    barcode_val = facts.get("upc_barcode", "1 20000 00003 6")
    story_copy = facts.get("brand_copywriting", "Start tapping, swishing & shaking your tail fins!")

    data_payload = {
        "brand": brand_name,
        "productName": product_name,
        "netWeight": net_weight,
        "barcode": barcode_val,
        "storyCopy": story_copy,
        "initialMode": initial_mode
    }
    data_json = json.dumps(data_payload)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; padding: 0; background: #0B1120; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; overflow: hidden; }}
            #container {{ width: 100%; height: 530px; position: relative; }}
            
            /* Top Header Bar */
            #overlay-header {{
                position: absolute;
                top: 14px;
                left: 18px;
                right: 18px;
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                pointer-events: none;
                z-index: 10;
            }}
            .badge-esko {{
                display: inline-block;
                background: linear-gradient(135deg, #2563EB, #1D4ED8);
                color: white;
                font-size: 10px;
                font-weight: 800;
                padding: 4px 10px;
                border-radius: 4px;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            }}
            .title-3d {{
                margin: 4px 0 0 0;
                font-size: 16px;
                font-weight: 800;
                color: #F8FAFC;
                letter-spacing: -0.01em;
            }}
            .sub-3d {{
                font-size: 11.5px;
                color: #94A3B8;
            }}

            /* Mode Switcher Banner (Interactive) */
            #mode-switcher {{
                pointer-events: auto;
                background: rgba(15, 23, 42, 0.85);
                backdrop-filter: blur(8px);
                border: 1px solid #334155;
                padding: 4px;
                border-radius: 8px;
                display: flex;
                gap: 4px;
            }}
            .mode-btn {{
                background: transparent;
                border: none;
                color: #94A3B8;
                font-size: 11px;
                font-weight: 700;
                padding: 6px 14px;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            .mode-btn.active-remediated {{
                background: #059669;
                color: #FFFFFF;
                box-shadow: 0 2px 8px rgba(5, 150, 105, 0.4);
            }}
            .mode-btn.active-defective {{
                background: #DC2626;
                color: #FFFFFF;
                box-shadow: 0 2px 8px rgba(220, 38, 38, 0.4);
            }}

            /* Bottom Quick Preset Controls */
            #controls {{
                position: absolute;
                bottom: 14px;
                left: 18px;
                right: 18px;
                z-index: 10;
                display: flex;
                justify-content: space-between;
                align-items: center;
                pointer-events: none;
            }}
            .btn-group {{
                display: flex;
                gap: 6px;
                pointer-events: auto;
                background: rgba(15, 23, 42, 0.85);
                backdrop-filter: blur(8px);
                padding: 5px 8px;
                border-radius: 8px;
                border: 1px solid #334155;
            }}
            .btn-3d {{
                background: #1E293B;
                color: #F1F5F9;
                border: 1px solid #475569;
                padding: 6px 11px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 700;
                cursor: pointer;
                transition: background 0.15s ease;
            }}
            .btn-3d:hover {{ background: #334155; color: #38BDF8; }}
            .btn-3d.active {{ background: #2563EB; border-color: #38BDF8; color: white; }}

            /* Panel Info HUD */
            #panel-hud {{
                pointer-events: auto;
                background: rgba(15, 23, 42, 0.9);
                backdrop-filter: blur(8px);
                border: 1px solid #334155;
                padding: 6px 14px;
                border-radius: 8px;
                font-size: 11px;
                color: #E2E8F0;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="container">
            <!-- Top Overlay -->
            <div id="overlay-header">
                <div>
                    <span class="badge-esko">Esko Studio 3D WebGL</span>
                    <div class="title-3d">3D Folding Carton Simulator</div>
                    <div class="sub-3d">Drag to rotate 360° • Scroll to zoom • Toggle Before/After remediation</div>
                </div>
                <div id="mode-switcher">
                    <button class="mode-btn" id="btn-mode-defective">🔴 Original Defective Artwork</button>
                    <button class="mode-btn active-remediated" id="btn-mode-remediated">🟢 Remediated Production Pack</button>
                </div>
            </div>

            <!-- Bottom Controls -->
            <div id="controls">
                <div class="btn-group">
                    <button class="btn-3d" id="btn-spin">⏸️ Pause Spin</button>
                    <button class="btn-3d active" id="btn-pdp">Front (PDP)</button>
                    <button class="btn-3d" id="btn-back">Back Panel</button>
                    <button class="btn-3d" id="btn-nutrition">Nutrition (Left)</button>
                    <button class="btn-3d" id="btn-specs">Specs & Barcode (Right)</button>
                    <button class="btn-3d" id="btn-top">Top Flap</button>
                    <button class="btn-3d" id="btn-base">Base</button>
                </div>

                <div id="panel-hud">
                    <span id="hud-dot" style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10B981;"></span>
                    <span id="hud-text"><strong>Front PDP:</strong> Remediated US 21 CFR 101.7 Net Quantity & Disclaimer</span>
                </div>
            </div>
        </div>

        <script>
            const CARTON_DATA = {data_json};
            let currentMode = CARTON_DATA.initialMode || 'remediated'; // 'remediated' or 'defective'
            let autoSpin = true;

            const container = document.getElementById('container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0B1120);

            const camera = new THREE.PerspectiveCamera(42, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(2.9, 1.4, 4.2);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.minDistance = 2.0;
            controls.maxDistance = 8.0;

            // Studio Lighting Setup
            const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.75);
            scene.add(ambientLight);

            const keyLight = new THREE.DirectionalLight(0xFFFFFF, 0.9);
            keyLight.position.set(6, 12, 8);
            keyLight.castShadow = true;
            keyLight.shadow.mapSize.width = 1024;
            keyLight.shadow.mapSize.height = 1024;
            scene.add(keyLight);

            const fillLight = new THREE.DirectionalLight(0x93C5FD, 0.4);
            fillLight.position.set(-6, 3, -6);
            scene.add(fillLight);

            const rimLight = new THREE.DirectionalLight(0xFDE68A, 0.35);
            rimLight.position.set(0, -5, -4);
            scene.add(rimLight);

            // ==========================================
            // TEXTURE GENERATORS (Dynamic Canvas)
            // ==========================================

            function drawCerealBowlGraphic(ctx, cx, cy, radius) {{
                // Ceramic bowl rim
                ctx.save();
                ctx.beginPath();
                ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                ctx.fillStyle = '#1E293B';
                ctx.fill();
                ctx.lineWidth = 6;
                ctx.strokeStyle = '#F8FAFC';
                ctx.stroke();

                // Granola oat cluster layers
                const clusterColors = ['#D97706', '#B45309', '#F59E0B', '#92400E'];
                for (let i = 0; i < 24; i++) {{
                    const angle = (i / 24) * Math.PI * 2;
                    const dist = radius * (0.3 + (i % 3) * 0.22);
                    const ox = cx + Math.cos(angle) * dist;
                    const oy = cy + Math.sin(angle) * dist;
                    ctx.beginPath();
                    ctx.ellipse(ox, oy, 14, 9, angle, 0, Math.PI * 2);
                    ctx.fillStyle = clusterColors[i % clusterColors.length];
                    ctx.fill();
                }}

                // Berries (Cranberries & Blueberries)
                const berries = [
                    {{ x: cx - 35, y: cy - 20, r: 12, col: '#DC2626' }}, // Cranberry
                    {{ x: cx + 30, y: cy - 35, r: 10, col: '#2563EB' }}, // Blueberry
                    {{ x: cx + 15, y: cy + 30, r: 11, col: '#1E40AF' }}, // Blueberry
                    {{ x: cx - 25, y: cy + 35, r: 13, col: '#B91C1C' }}, // Cranberry
                    {{ x: cx + 45, y: cy + 10, r: 12, col: '#EF4444' }}  // Cranberry
                ];
                berries.forEach(b => {{
                    ctx.beginPath();
                    ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                    ctx.fillStyle = b.col;
                    ctx.fill();
                    // Specular highlight
                    ctx.beginPath();
                    ctx.arc(b.x - 3, b.y - 3, b.r * 0.3, 0, Math.PI * 2);
                    ctx.fillStyle = 'rgba(255,255,255,0.7)';
                    ctx.fill();
                }});

                // Almond slices
                ctx.fillStyle = '#FDE68A';
                ctx.strokeStyle = '#78350F';
                ctx.lineWidth = 1.5;
                for (let j = 0; j < 4; j++) {{
                    ctx.beginPath();
                    ctx.ellipse(cx + (j - 1.5) * 28, cy - 5 + (j % 2) * 12, 16, 7, 0.4 * j, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.stroke();
                }}
                ctx.restore();
            }}

            // 1. FRONT PDP TEXTURE
            function createFrontTexture(mode) {{
                const c = document.createElement('canvas');
                c.width = 512; c.height = 768;
                const ctx = c.getContext('2d');

                // Rich Deep Navy Blue Background
                const bgGrad = ctx.createLinearGradient(0, 0, 0, 768);
                bgGrad.addColorStop(0, '#1E3A8A');
                bgGrad.addColorStop(1, '#0F172A');
                ctx.fillStyle = bgGrad;
                ctx.fillRect(0, 0, 512, 768);

                // Gold foil border
                ctx.strokeStyle = '#F59E0B';
                ctx.lineWidth = 10;
                ctx.strokeRect(18, 18, 476, 732);

                // Brand Header
                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 44px sans-serif';
                ctx.textAlign = 'center';
                ctx.letterSpacing = '2px';
                ctx.fillText(CARTON_DATA.brand, 256, 115);

                ctx.fillStyle = '#FCD34D';
                ctx.font = 'bold 24px sans-serif';
                ctx.fillText(CARTON_DATA.productName, 256, 160);

                // Cereal Bowl Artwork
                drawCerealBowlGraphic(ctx, 256, 335, 125);

                if (mode === 'defective') {{
                    // DEFECT 1: MISSING SERVING DISCLAIMER
                    ctx.strokeStyle = '#EF4444';
                    ctx.lineWidth = 3;
                    ctx.setLineDash([6, 4]);
                    ctx.strokeRect(40, 470, 432, 38);
                    ctx.setLineDash([]);
                    ctx.fillStyle = '#EF4444';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('❌ MISSING DISCLAIMER: Depicts fresh berries with no notice', 256, 494);

                    // DEFECT 2: ILLEGAL CERTIFIED VEGAN BADGE ON HONEY PRODUCT
                    ctx.fillStyle = '#EF4444';
                    ctx.fillRect(40, 520, 210, 46);
                    ctx.strokeStyle = '#FFFFFF';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(40, 520, 210, 46);
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillText('❌ CERTIFIED VEGAN', 145, 545);
                    ctx.font = '10px sans-serif';
                    ctx.fillText('VIOLATION: HONEY INCLUDED', 145, 560);

                    // GMO Free Badge
                    ctx.fillStyle = '#475569';
                    ctx.fillRect(265, 520, 205, 46);
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillText('NON-GMO VERIFIED', 367, 548);

                    // DEFECT 3: MISPLACED / NON-COMPLIANT NET WEIGHT
                    ctx.fillStyle = '#7F1D1D';
                    ctx.fillRect(100, 640, 312, 50);
                    ctx.fillStyle = '#FCA5A5';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('❌ NET WT: Misplaced / Missing lower 30% rule', 256, 670);

                }} else {{
                    // REMEDIATED PRODUCTION PDP
                    // Mandatory Serving Suggestion Disclaimer (FTC & FDA truth in advertising)
                    ctx.fillStyle = '#FDE68A';
                    ctx.font = 'italic 15px sans-serif';
                    ctx.fillText('Serving Suggestion. Fresh fruit not included.', 256, 485);

                    // Badges: USDA Organic & Non-GMO Verified
                    ctx.fillStyle = '#059669';
                    ctx.beginPath();
                    ctx.roundRect(50, 515, 195, 42, 6);
                    ctx.fill();
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = 'bold 15px sans-serif';
                    ctx.fillText('🌿 USDA ORGANIC', 147, 542);

                    ctx.fillStyle = '#2563EB';
                    ctx.beginPath();
                    ctx.roundRect(265, 515, 195, 42, 6);
                    ctx.fill();
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = 'bold 15px sans-serif';
                    ctx.fillText('✔ NON-GMO VERIFIED', 362, 542);

                    // Statutory Net Weight in Lower 30% Zone (FDA 21 CFR 101.7)
                    ctx.fillStyle = '#0F172A';
                    ctx.beginPath();
                    ctx.roundRect(40, 620, 432, 70, 8);
                    ctx.fill();
                    ctx.strokeStyle = '#10B981';
                    ctx.lineWidth = 3;
                    ctx.stroke();

                    ctx.fillStyle = '#10B981';
                    ctx.font = 'bold 26px sans-serif';
                    ctx.fillText(CARTON_DATA.netWeight, 256, 664);
                }}

                return new THREE.CanvasTexture(c);
            }}

            // 2. BACK PANEL TEXTURE (Story, Formula, Allergens, Lozenges)
            function createBackTexture(mode) {{
                const c = document.createElement('canvas');
                c.width = 512; c.height = 768;
                const ctx = c.getContext('2d');

                ctx.fillStyle = '#111827';
                ctx.fillRect(0, 0, 512, 768);

                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 28px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('PACKED WITH GOODNESS', 256, 75);

                ctx.font = 'italic 16px sans-serif';
                ctx.fillStyle = '#93C5FD';
                ctx.fillText('"' + CARTON_DATA.storyCopy + '"', 256, 110);

                ctx.textAlign = 'left';
                ctx.fillStyle = '#F59E0B';
                ctx.font = 'bold 17px sans-serif';
                ctx.fillText('INGREDIENTS:', 40, 165);

                if (mode === 'defective') {{
                    // DEFECT: FORMULA CONFLICT & WEAK ALLERGENS & UK TRAFFIC LIGHTS
                    ctx.fillStyle = '#F87171';
                    ctx.font = '14px sans-serif';
                    ctx.fillText('Organic Oat Flakes (79%), Honey (1% vs 9% Conflict!),', 40, 195);
                    ctx.fillText('Vegetable Oils, Blueberries, Cranberries, Seeds.', 40, 220);

                    // Weak Allergen Declaration
                    ctx.fillStyle = '#450A0A';
                    ctx.fillRect(35, 270, 442, 85);
                    ctx.strokeStyle = '#EF4444';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(35, 270, 442, 85);

                    ctx.fillStyle = '#EF4444';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillText('❌ DEFECT: ADVISORY ALLERGEN PHRASING', 50, 298);
                    ctx.fillStyle = '#FCA5A5';
                    ctx.font = '13px sans-serif';
                    ctx.fillText('May Contain Almonds, May Contain Pecans (FALCPA Violation)', 50, 324);

                    // UK Traffic Light Lozenges
                    ctx.fillStyle = '#1F2937';
                    ctx.fillRect(35, 385, 442, 95);
                    ctx.strokeStyle = '#EF4444';
                    ctx.strokeRect(35, 385, 442, 95);
                    ctx.fillStyle = '#EF4444';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('❌ NON-COMPLIANT UK TRAFFIC LIGHT LOZENGES:', 50, 412);

                    const colors = ['#10B981', '#F59E0B', '#EF4444', '#10B981'];
                    const labels = ['FAT 4.2g', 'SAT 0.8g', 'SUG 18g', 'SALT 0.2g'];
                    for (let i = 0; i < 4; i++) {{
                        ctx.fillStyle = colors[i];
                        ctx.fillRect(55 + i * 102, 428, 92, 38);
                        ctx.fillStyle = '#FFFFFF';
                        ctx.font = 'bold 12px sans-serif';
                        ctx.fillText(labels[i], 65 + i * 102, 452);
                    }}

                    // Contradictory Vegan text
                    ctx.fillStyle = '#EF4444';
                    ctx.font = 'bold 15px sans-serif';
                    ctx.fillText('❌ "Suitable for Vegetarians (Vegan)" - Deceptive', 50, 525);

                }} else {{
                    // REMEDIATED PRODUCTION BACK PANEL
                    ctx.fillStyle = '#E2E8F0';
                    ctx.font = '14.5px sans-serif';
                    const lines = [
                        'Organic Wholegrain Oat Flakes (79%), Almonds,',
                        'Pecans, Walnuts, Flax Seeds, Vegetable Oil,',
                        'Dried Strawberries, Blueberries, Cranberries,',
                        'Pumpkin Seeds, Honey (1%), Coconut Sugar,',
                        'Crystallized Ginger, Himalayan Pink Salt.'
                    ];
                    lines.forEach((l, i) => ctx.fillText(l, 40, 195 + i * 25));

                    // Mandatory Bold FALCPA Allergen Box
                    ctx.fillStyle = '#0F172A';
                    ctx.beginPath();
                    ctx.roundRect(35, 340, 442, 110, 8);
                    ctx.fill();
                    ctx.strokeStyle = '#10B981';
                    ctx.lineWidth = 2.5;
                    ctx.stroke();

                    ctx.fillStyle = '#10B981';
                    ctx.font = 'bold 15px sans-serif';
                    ctx.fillText('MANDATORY ALLERGEN DECLARATION (FALCPA / FASTER):', 50, 372);
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillText('CONTAINS: ALMONDS, PECANS, WALNUTS.', 50, 402);
                    ctx.font = '13px sans-serif';
                    ctx.fillStyle = '#CBD5E1';
                    ctx.fillText('MAY CONTAIN: BRAZIL NUTS, OTHER TREE NUTS, WHEAT.', 50, 428);

                    // Compliant Vegetarian Claim
                    ctx.fillStyle = '#10B981';
                    ctx.font = 'bold 17px sans-serif';
                    ctx.fillText('✔ Suitable for Vegetarians', 50, 490);

                    // Storage Copy
                    ctx.fillStyle = '#94A3B8';
                    ctx.font = '13.5px sans-serif';
                    ctx.fillText('Store in a cool, dry place. Keep closed once opened.', 50, 540);
                    ctx.fillText('For best before date, see base of pack.', 50, 565);
                }}

                return new THREE.CanvasTexture(c);
            }}

            // 3. NUTRITION PANEL (LEFT SIDE FACE)
            function createNutritionTexture(mode) {{
                const c = document.createElement('canvas');
                c.width = 256; c.height = 768;
                const ctx = c.getContext('2d');

                ctx.fillStyle = '#FFFFFF';
                ctx.fillRect(0, 0, 256, 768);

                ctx.fillStyle = '#000000';
                ctx.font = '900 28px sans-serif';
                ctx.fillText('Nutrition Facts', 16, 52);

                if (mode === 'defective') {{
                    ctx.fillStyle = '#DC2626';
                    ctx.font = 'bold 12px sans-serif';
                    ctx.fillText('❌ 8 servings (unverified grams)', 16, 78);
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillText('Serving size   ??', 16, 102);

                    ctx.fillStyle = '#000000';
                    ctx.fillRect(16, 114, 224, 8);
                    ctx.font = 'bold 24px sans-serif';
                    ctx.fillText('Calories   166', 16, 165);
                    ctx.fillRect(16, 178, 224, 4);

                    // Typo DIETRAY FIBER
                    ctx.fillStyle = '#DC2626';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillText('❌ DIETRAY FIBER  3g', 16, 230);

                    // False Added Sugars 0g
                    ctx.fillStyle = '#DC2626';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('❌ Incl. 0g Added Sugars', 16, 275);
                    ctx.font = '10px sans-serif';
                    ctx.fillText('(FALSE: Contains Honey & Sugar)', 16, 292);

                    ctx.fillStyle = '#7F1D1D';
                    ctx.fillRect(12, 330, 232, 60);
                    ctx.fillStyle = '#FCA5A5';
                    ctx.font = 'bold 11px sans-serif';
                    ctx.fillText('NON-COMPLIANT FDA PANEL', 20, 355);
                    ctx.font = '10px sans-serif';
                    ctx.fillText('Outdated vertical format', 20, 372);

                }} else {{
                    ctx.font = '14px sans-serif';
                    ctx.fillText('8 servings per container', 16, 78);
                    ctx.font = 'bold 15px sans-serif';
                    ctx.fillText('Serving size       60g', 16, 102);

                    ctx.fillRect(16, 114, 224, 9);

                    ctx.font = 'bold 12px sans-serif';
                    ctx.fillText('Amount per serving', 16, 138);
                    ctx.font = '900 28px sans-serif';
                    ctx.fillText('Calories    166', 16, 172);
                    ctx.fillRect(16, 182, 224, 4);

                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('Total Fat 15g                    19%', 16, 212);
                    ctx.fillText('Total Carbohydrate 15g    5%', 16, 242);

                    // Statutory DIETARY FIBER
                    ctx.font = '13px sans-serif';
                    ctx.fillText('  Dietary Fiber 3g            11%', 16, 270);
                    ctx.fillText('  Total Sugars 18g', 16, 298);

                    // Remediated Added Sugars
                    ctx.fillStyle = '#059669';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('  Incl. 7g Added Sugars     14%', 16, 326);

                    ctx.fillStyle = '#000000';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('Protein 34g', 16, 356);

                    ctx.fillRect(16, 370, 224, 1);
                    ctx.font = '10px sans-serif';
                    ctx.fillStyle = '#64748B';
                    ctx.fillText('* The % Daily Value tells you how', 16, 395);
                    ctx.fillText('much a nutrient in a serving contributes.', 16, 410);
                }}

                return new THREE.CanvasTexture(c);
            }}

            // 4. SPECS & BARCODE (RIGHT SIDE FACE)
            function createSpecTexture(mode) {{
                const c = document.createElement('canvas');
                c.width = 256; c.height = 768;
                const ctx = c.getContext('2d');

                ctx.fillStyle = '#0F172A';
                ctx.fillRect(0, 0, 256, 768);

                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('SPECIFICATIONS', 20, 60);

                ctx.font = '13px sans-serif';
                ctx.fillStyle = '#94A3B8';
                ctx.fillText('Substrate: FSC 18pt SBS', 20, 95);
                ctx.fillText('Coating: Matte Aqueous', 20, 122);
                ctx.fillText('Logo: Spot Gloss UV', 20, 149);

                if (mode === 'defective') {{
                    // Typo RECYCABLE
                    ctx.fillStyle = '#450A0A';
                    ctx.fillRect(16, 200, 224, 60);
                    ctx.strokeStyle = '#EF4444';
                    ctx.strokeRect(16, 200, 224, 60);
                    ctx.fillStyle = '#EF4444';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('❌ TYPO ON PACK:', 25, 226);
                    ctx.font = 'bold 15px sans-serif';
                    ctx.fillText('"RECYCABLE"', 25, 248);

                }} else {{
                    // Corrected RECYCLABLE
                    ctx.fillStyle = '#064E3B';
                    ctx.beginPath();
                    ctx.roundRect(16, 200, 224, 55, 6);
                    ctx.fill();
                    ctx.fillStyle = '#34D399';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText('✔ 100% RECYCLABLE', 25, 233);
                }}

                // Barcode Block with standard quiet zones
                ctx.fillStyle = '#FFFFFF';
                ctx.fillRect(18, 300, 220, 120);
                ctx.fillStyle = '#000000';
                for (let i = 35; i < 215; i += 6) {{
                    const w = (i % 4 === 0) ? 3.5 : (i % 3 === 0 ? 2 : 1.5);
                    ctx.fillRect(i, 320, w, 68);
                }}
                ctx.font = '14px monospace';
                ctx.textAlign = 'center';
                ctx.fillText(CARTON_DATA.barcode, 128, 410);

                return new THREE.CanvasTexture(c);
            }}

            // 5. TOP FLAP TEXTURE
            function createTopTexture(mode) {{
                const c = document.createElement('canvas');
                c.width = 512; c.height = 256;
                const ctx = c.getContext('2d');

                ctx.fillStyle = '#1E3A8A';
                ctx.fillRect(0, 0, 512, 256);

                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 28px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(CARTON_DATA.brand, 256, 85);

                if (mode === 'defective') {{
                    // ILLEGAL NO ADDED SUGAR CALLOUT
                    ctx.fillStyle = '#DC2626';
                    ctx.fillRect(40, 120, 432, 65);
                    ctx.strokeStyle = '#FFFFFF';
                    ctx.lineWidth = 3;
                    ctx.strokeRect(40, 120, 432, 65);

                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = 'bold 20px sans-serif';
                    ctx.fillText('❌ NO ADDED SUGAR', 256, 155);
                    ctx.font = '12px sans-serif';
                    ctx.fillStyle = '#FEE2E2';
                    ctx.fillText('CRITICAL VIOLATION: FDA 21 CFR 101.60(c)(2)', 256, 175);

                }} else {{
                    // CLEAN REMEDIATED TOP FLAP
                    ctx.fillStyle = '#FCD34D';
                    ctx.font = '17px sans-serif';
                    ctx.fillText('Artisan Packaging Closure', 256, 130);
                    ctx.fillStyle = '#93C5FD';
                    ctx.font = '13px sans-serif';
                    ctx.fillText('Esko ArtiosCAD Mechanical Tuck Lock Flap', 256, 165);
                }}

                return new THREE.CanvasTexture(c);
            }}

            // 6. BOTTOM BASE TEXTURE
            function createBottomTexture() {{
                const c = document.createElement('canvas');
                c.width = 512; c.height = 256;
                const ctx = c.getContext('2d');

                ctx.fillStyle = '#0B1120';
                ctx.fillRect(0, 0, 512, 256);

                ctx.fillStyle = '#94A3B8';
                ctx.font = '16px monospace';
                ctx.textAlign = 'center';
                ctx.fillText('LOT: DF-2026-B448', 256, 110);
                ctx.fillText('BEST BEFORE: OCT 2027', 256, 145);
                ctx.font = '12px sans-serif';
                ctx.fillStyle = '#64748B';
                ctx.fillText('Base Panel Inkjet Date Code Window', 256, 180);

                return new THREE.CanvasTexture(c);
            }}

            // Assemble Mesh
            const geometry = new THREE.BoxGeometry(1.8, 2.6, 0.9);
            let materials = [];

            function updateMaterials(mode) {{
                materials = [
                    new THREE.MeshStandardMaterial({{ map: createSpecTexture(mode), roughness: 0.45 }}),      // +X (Right)
                    new THREE.MeshStandardMaterial({{ map: createNutritionTexture(mode), roughness: 0.3 }}), // -X (Left)
                    new THREE.MeshStandardMaterial({{ map: createTopTexture(mode), roughness: 0.45 }}),        // +Y (Top)
                    new THREE.MeshStandardMaterial({{ map: createBottomTexture(), roughness: 0.55 }}),         // -Y (Bottom)
                    new THREE.MeshStandardMaterial({{ map: createFrontTexture(mode), roughness: 0.25 }}),     // +Z (Front)
                    new THREE.MeshStandardMaterial({{ map: createBackTexture(mode), roughness: 0.35 }})        // -Z (Back)
                ];
                if (carton) {{
                    carton.material = materials;
                }}
            }}

            updateMaterials(currentMode);
            const carton = new THREE.Mesh(geometry, materials);
            carton.castShadow = true;
            carton.receiveShadow = true;
            scene.add(carton);

            // Shadow Ground Plane
            const planeGeo = new THREE.PlaneGeometry(10, 10);
            const planeMat = new THREE.ShadowMaterial({{ opacity: 0.3 }});
            const plane = new THREE.Mesh(planeGeo, planeMat);
            plane.rotation.x = -Math.PI / 2;
            plane.position.y = -1.35;
            plane.receiveShadow = true;
            scene.add(plane);

            // ==========================================
            // UI INTERACTIONS & CAMERA PRESETS
            // ==========================================

            const hudDot = document.getElementById('hud-dot');
            const hudText = document.getElementById('hud-text');

            function setHUD(text, isRemediated) {{
                hudDot.style.background = isRemediated ? '#10B981' : '#EF4444';
                hudText.innerHTML = text;
            }}

            // Mode Switching
            const btnDefective = document.getElementById('btn-mode-defective');
            const btnRemediated = document.getElementById('btn-mode-remediated');

            btnDefective.onclick = () => {{
                currentMode = 'defective';
                btnDefective.className = 'mode-btn active-defective';
                btnRemediated.className = 'mode-btn';
                updateMaterials('defective');
                setHUD('<strong>Defective Artwork Mode:</strong> Red highlights reveal 12 hidden FDA violations & typos', false);
            }};

            btnRemediated.onclick = () => {{
                currentMode = 'remediated';
                btnRemediated.className = 'mode-btn active-remediated';
                btnDefective.className = 'mode-btn';
                updateMaterials('remediated');
                setHUD('<strong>Remediated Mode:</strong> Verified production specs meeting US 21 CFR standards', true);
            }};

            // Camera Controls
            let targetCamPos = null;

            function animateCameraTo(x, y, z) {{
                autoSpin = false;
                document.getElementById('btn-spin').textContent = '▶️ Resume Spin';
                targetCamPos = new THREE.Vector3(x, y, z);
            }}

            document.getElementById('btn-spin').onclick = function() {{
                autoSpin = !autoSpin;
                this.textContent = autoSpin ? '⏸️ Pause Spin' : '▶️ Resume Spin';
                targetCamPos = null;
            }};

            document.getElementById('btn-pdp').onclick = () => {{
                animateCameraTo(0, 0, 3.8);
                setHUD(currentMode === 'defective' ? '<strong>Front PDP:</strong> Illegal vegan badge & missing disclaimer' : '<strong>Front PDP:</strong> Remediated 21 CFR 101.7 Net Quantity & Disclaimer', currentMode === 'remediated');
            }};

            document.getElementById('btn-back').onclick = () => {{
                animateCameraTo(0, 0, -3.8);
                setHUD(currentMode === 'defective' ? '<strong>Back Panel:</strong> Recipe conflict, weak allergen phrasing, UK lozenges' : '<strong>Back Panel:</strong> Authorized formulation, bold FALCPA box, Vegetarian claim', currentMode === 'remediated');
            }};

            document.getElementById('btn-nutrition').onclick = () => {{
                animateCameraTo(-3.6, 0, 0);
                setHUD(currentMode === 'defective' ? '<strong>Left Panel:</strong> Misspelled "DIETRAY FIBER" & 0g Added Sugars falsification' : '<strong>Left Panel:</strong> US FDA 2016 vertical Nutrition Facts with true Added Sugars', currentMode === 'remediated');
            }};

            document.getElementById('btn-specs').onclick = () => {{
                animateCameraTo(3.6, 0, 0);
                setHUD(currentMode === 'defective' ? '<strong>Right Panel:</strong> Typo "RECYCABLE PAPERBOARD"' : '<strong>Right Panel:</strong> Corrected "RECYCLABLE", FSC 18pt SBS & UPC quiet zone verified', currentMode === 'remediated');
            }};

            document.getElementById('btn-top').onclick = () => {{
                animateCameraTo(0, 3.8, 0.05);
                setHUD(currentMode === 'defective' ? '<strong>Top Flap:</strong> Critical violation: "NO ADDED SUGAR" badge' : '<strong>Top Flap:</strong> Clean closure flap with illegal claim purged', currentMode === 'remediated');
            }};

            document.getElementById('btn-base').onclick = () => {{
                animateCameraTo(0, -3.8, 0.05);
                setHUD('<strong>Base Panel:</strong> Inkjet date code & lot number inspection window', true);
            }};

            // Render Loop
            function animate() {{
                requestAnimationFrame(animate);

                if (autoSpin) {{
                    carton.rotation.y += 0.007;
                }}

                if (targetCamPos) {{
                    camera.position.lerp(targetCamPos, 0.08);
                    controls.target.set(0, 0, 0);
                    if (camera.position.distanceTo(targetCamPos) < 0.02) {{
                        camera.position.copy(targetCamPos);
                        targetCamPos = null;
                    }}
                }}

                controls.update();
                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </body>
    </html>
    """
    return html
