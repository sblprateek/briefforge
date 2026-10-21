"""
BriefForge 3D Folded Carton WebGL Simulator
Renders an interactive 3D folding carton in Three.js with 360-degree orbital rotation,
panel textures, and inspection callouts matching Esko Studio 3D capabilities.
"""


def render_3d_carton_html() -> str:
    """Renders a self-contained WebGL 3D folding carton with Three.js."""
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { margin: 0; padding: 0; background: #0F172A; font-family: -apple-system, sans-serif; overflow: hidden; }
            #container { width: 100%; height: 500px; position: relative; }
            #overlay {
                position: absolute;
                top: 14px;
                left: 18px;
                color: white;
                pointer-events: none;
                z-index: 10;
            }
            .badge-3d {
                display: inline-block;
                background: #2563EB;
                color: white;
                font-size: 10px;
                font-weight: 800;
                padding: 3px 8px;
                border-radius: 4px;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }
            #controls {
                position: absolute;
                bottom: 14px;
                left: 18px;
                z-index: 10;
                display: flex;
                gap: 8px;
            }
            .btn-3d {
                background: #1E293B;
                color: #F8FAFC;
                border: 1px solid #475569;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 700;
                cursor: pointer;
            }
            .btn-3d:hover { background: #334155; }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="container">
            <div id="overlay">
                <span class="badge-3d">Esko Studio 3D Simulation</span>
                <h3 style="margin:4px 0 0 0; font-size:15px; color:#F8FAFC;">3D Folded Carton Inspector</h3>
                <div style="font-size:11px; color:#94A3B8;">Drag mouse to rotate 360° • Scroll to zoom • Inspect all 6 panels</div>
            </div>
            <div id="controls">
                <button class="btn-3d" id="btn-toggle-spin">⏸️ Pause Spin</button>
                <button class="btn-3d" id="btn-front">PDP (Front)</button>
                <button class="btn-3d" id="btn-back">Back Panel</button>
                <button class="btn-3d" id="btn-nutrition">Nutrition Side</button>
            </div>
        </div>

        <script>
            const container = document.getElementById('container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0F172A);

            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(2.8, 1.5, 4.2);

            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;

            // Lights
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
            dirLight.position.set(5, 10, 7);
            scene.add(dirLight);

            const rimLight = new THREE.DirectionalLight(0x38BDF8, 0.4);
            rimLight.position.set(-5, -2, -5);
            scene.add(rimLight);

            // Canvas Textures
            function createFrontTexture() {
                const c = document.createElement('canvas');
                c.width = 512; c.height = 768;
                const ctx = c.getContext('2d');
                ctx.fillStyle = '#1E3A8A';
                ctx.fillRect(0, 0, 512, 768);

                // Gold border accent
                ctx.strokeStyle = '#F59E0B';
                ctx.lineWidth = 12;
                ctx.strokeRect(20, 20, 472, 728);

                // Brand
                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 44px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('DANCING FISH', 256, 120);

                ctx.fillStyle = '#FCD34D';
                ctx.font = 'bold 28px sans-serif';
                ctx.fillText('GRANOLA BERRY CRUNCH', 256, 170);

                // Illustration circle
                ctx.beginPath();
                ctx.arc(256, 360, 140, 0, Math.PI * 2);
                ctx.fillStyle = '#1E293B';
                ctx.fill();
                ctx.strokeStyle = '#FFFFFF';
                ctx.lineWidth = 6;
                ctx.stroke();

                ctx.fillStyle = '#FFFFFF';
                ctx.font = '22px sans-serif';
                ctx.fillText('🥣 Cereal Bowl', 256, 350);
                ctx.font = '16px sans-serif';
                ctx.fillStyle = '#94A3B8';
                ctx.fillText('Artisan Oven Baked', 256, 385);

                // Serving suggestion
                ctx.fillStyle = '#FDE68A';
                ctx.font = '15px sans-serif';
                ctx.fillText('Serving Suggestion. Fresh fruit not included.', 256, 530);

                // Badges
                ctx.fillStyle = '#10B981';
                ctx.fillRect(50, 560, 180, 40);
                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 16px sans-serif';
                ctx.fillText('USDA ORGANIC', 140, 586);

                ctx.fillStyle = '#6366F1';
                ctx.fillRect(280, 560, 180, 40);
                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 16px sans-serif';
                ctx.fillText('NON-GMO VERIFIED', 370, 586);

                // Net weight target lower 30%
                ctx.fillStyle = '#0F172A';
                ctx.fillRect(40, 640, 432, 70);
                ctx.fillStyle = '#10B981';
                ctx.font = 'bold 26px sans-serif';
                ctx.fillText('NET WT 16.9 OZ (480g)', 256, 685);

                return new THREE.CanvasTexture(c);
            }

            function createBackTexture() {
                const c = document.createElement('canvas');
                c.width = 512; c.height = 768;
                const ctx = c.getContext('2d');
                ctx.fillStyle = '#1E293B';
                ctx.fillRect(0, 0, 512, 768);

                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 30px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('PACKED WITH GOODNESS', 256, 80);

                ctx.font = 'italic 18px sans-serif';
                ctx.fillStyle = '#93C5FD';
                ctx.fillText('"Start tapping, swishing & shaking your tail fins!"', 256, 120);

                // Ingredients
                ctx.textAlign = 'left';
                ctx.fillStyle = '#F59E0B';
                ctx.font = 'bold 18px sans-serif';
                ctx.fillText('AUTHORIZED MASTER INGREDIENTS:', 40, 180);

                ctx.fillStyle = '#E2E8F0';
                ctx.font = '15px sans-serif';
                const lines = [
                    'Organic Wholegrain Oat Flakes (79%), Almonds,',
                    'Pecans, Walnuts, Flax Seeds, Vegetable Oil,',
                    'Dried Strawberries, Blueberries, Cranberries,',
                    'Pumpkin Seeds, Honey (1%), Coconut Sugar,',
                    'Crystallized Ginger, Pink Salt. Natural Flavoring.'
                ];
                lines.forEach((l, i) => ctx.fillText(l, 40, 215 + (i * 26)));

                // Allergen Box
                ctx.fillStyle = '#0F172A';
                ctx.fillRect(35, 360, 442, 90);
                ctx.strokeStyle = '#EF4444';
                ctx.strokeRect(35, 360, 442, 90);

                ctx.fillStyle = '#EF4444';
                ctx.font = 'bold 16px sans-serif';
                ctx.fillText('MANDATORY ALLERGEN DECLARATION:', 50, 390);
                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 15px sans-serif';
                ctx.fillText('CONTAINS: ALMONDS, PECANS, WALNUTS.', 50, 418);
                ctx.font = '14px sans-serif';
                ctx.fillText('MAY CONTAIN: BRAZIL NUTS, OTHER TREE NUTS, WHEAT.', 50, 438);

                // Claims
                ctx.fillStyle = '#10B981';
                ctx.font = 'bold 18px sans-serif';
                ctx.fillText('✔ Suitable for Vegetarians', 50, 500);

                // Storage
                ctx.fillStyle = '#94A3B8';
                ctx.font = '14px sans-serif';
                ctx.fillText('Store in cool dry place. Keep closed once opened.', 50, 560);
                ctx.fillText('For best before, see base of pack.', 50, 585);

                return new THREE.CanvasTexture(c);
            }

            function createNutritionTexture() {
                const c = document.createElement('canvas');
                c.width = 256; c.height = 768;
                const ctx = c.getContext('2d');
                ctx.fillStyle = '#FFFFFF';
                ctx.fillRect(0, 0, 256, 768);

                ctx.fillStyle = '#000000';
                ctx.font = 'bold 28px sans-serif';
                ctx.fillText('Nutrition Facts', 16, 50);

                ctx.font = '14px sans-serif';
                ctx.fillText('8 servings per container', 16, 78);
                ctx.font = 'bold 16px sans-serif';
                ctx.fillText('Serving size   60g', 16, 102);

                ctx.fillRect(16, 112, 224, 8);

                ctx.font = 'bold 13px sans-serif';
                ctx.fillText('Amount Per Serving', 16, 138);
                ctx.font = 'bold 26px sans-serif';
                ctx.fillText('Calories   166', 16, 170);

                ctx.fillRect(16, 180, 224, 4);

                ctx.font = 'bold 14px sans-serif';
                ctx.fillText('Total Fat 15g', 16, 210);
                ctx.fillText('Total Carb. 15g', 16, 240);
                ctx.fillText('Dietary Fiber 3g', 30, 268);
                ctx.fillText('Total Sugars 18g', 16, 298);

                ctx.fillStyle = '#10B981';
                ctx.fillText('Incl. Added Sugars', 30, 326);

                ctx.fillStyle = '#000000';
                ctx.fillText('Protein 34g', 16, 356);

                return new THREE.CanvasTexture(c);
            }

            function createSpecTexture() {
                const c = document.createElement('canvas');
                c.width = 256; c.height = 768;
                const ctx = c.getContext('2d');
                ctx.fillStyle = '#0F172A';
                ctx.fillRect(0, 0, 256, 768);

                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 20px sans-serif';
                ctx.fillText('SPECIFICATIONS', 20, 60);

                ctx.font = '12px sans-serif';
                ctx.fillStyle = '#94A3B8';
                ctx.fillText('Substrate: FSC 18pt SBS', 20, 95);
                ctx.fillText('Coating: Matte Aqueous', 20, 120);
                ctx.fillText('Brand Mark: Spot Gloss UV', 20, 145);

                // Barcode white box
                ctx.fillStyle = '#FFFFFF';
                ctx.fillRect(20, 220, 216, 110);
                ctx.fillStyle = '#000000';
                for(let i=35; i<210; i+=6) {
                    ctx.fillRect(i, 235, (i%3===0)?3:1.5, 60);
                }
                ctx.font = '13px monospace';
                ctx.fillText('1 20000 00003 6', 60, 316);

                return new THREE.CanvasTexture(c);
            }

            function createTopTexture() {
                const c = document.createElement('canvas');
                c.width = 512; c.height = 256;
                const ctx = c.getContext('2d');
                ctx.fillStyle = '#1E3A8A';
                ctx.fillRect(0, 0, 512, 256);

                ctx.fillStyle = '#FFFFFF';
                ctx.font = 'bold 28px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('DANCING FISH', 256, 90);
                ctx.fillStyle = '#10B981';
                ctx.font = 'bold 18px sans-serif';
                ctx.fillText('✔ NO ADDED SUGAR BADGE PURGED', 256, 140);
                ctx.fillStyle = '#93C5FD';
                ctx.font = '14px sans-serif';
                ctx.fillText('Top Flap Mechanical Closure', 256, 175);

                return new THREE.CanvasTexture(c);
            }

            function createBottomTexture() {
                const c = document.createElement('canvas');
                c.width = 512; c.height = 256;
                const ctx = c.getContext('2d');
                ctx.fillStyle = '#0F172A';
                ctx.fillRect(0, 0, 512, 256);
                ctx.fillStyle = '#94A3B8';
                ctx.font = '16px monospace';
                ctx.textAlign = 'center';
                ctx.fillText('LOT: DF-2026-B448', 256, 110);
                ctx.fillText('BEST BEFORE: OCT 2027', 256, 150);
                return new THREE.CanvasTexture(c);
            }

            // Box Geometry (Width 1.8, Height 2.6, Depth 0.9)
            const geometry = new THREE.BoxGeometry(1.8, 2.6, 0.9);
            const materials = [
                new THREE.MeshStandardMaterial({ map: createSpecTexture(), roughness: 0.4 }),      // Right
                new THREE.MeshStandardMaterial({ map: createNutritionTexture(), roughness: 0.3 }), // Left
                new THREE.MeshStandardMaterial({ map: createTopTexture(), roughness: 0.4 }),        // Top
                new THREE.MeshStandardMaterial({ map: createBottomTexture(), roughness: 0.5 }),     // Bottom
                new THREE.MeshStandardMaterial({ map: createFrontTexture(), roughness: 0.25 }),     // Front
                new THREE.MeshStandardMaterial({ map: createBackTexture(), roughness: 0.3 })        // Back
            ];

            const carton = new THREE.Mesh(geometry, materials);
            scene.add(carton);

            // Shadow plane
            const planeGeo = new THREE.PlaneGeometry(10, 10);
            const planeMat = new THREE.ShadowMaterial({ opacity: 0.2 });
            const plane = new THREE.Mesh(planeGeo, planeMat);
            plane.rotation.x = -Math.PI / 2;
            plane.position.y = -1.35;
            scene.add(plane);

            let autoSpin = true;
            document.getElementById('btn-toggle-spin').onclick = function() {
                autoSpin = !autoSpin;
                this.textContent = autoSpin ? '⏸️ Pause Spin' : '▶️ Resume Spin';
            };

            document.getElementById('btn-front').onclick = () => {
                autoSpin = false;
                camera.position.set(0, 0, 3.8);
                controls.target.set(0, 0, 0);
            };

            document.getElementById('btn-back').onclick = () => {
                autoSpin = false;
                camera.position.set(0, 0, -3.8);
                controls.target.set(0, 0, 0);
            };

            document.getElementById('btn-nutrition').onclick = () => {
                autoSpin = false;
                camera.position.set(-3.5, 0, 0);
                controls.target.set(0, 0, 0);
            };

            function animate() {
                requestAnimationFrame(animate);
                if (autoSpin) {
                    carton.rotation.y += 0.008;
                }
                controls.update();
                renderer.render(scene, camera);
            }
            animate();

            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
        </script>
    </body>
    </html>
    """
    return html
