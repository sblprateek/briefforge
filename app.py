"""
BriefForge — World-Class AI Packaging Design Brief Studio
Autonomous packaging knowledge fusion, multi-agent council review,
interactive 3D & 2D dieline inspection, visual remediation diffs, and enterprise handover synthesis.
"""

import os
import sys
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load local environment
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
sys.path.insert(0, str(BASE_DIR))

import streamlit as st
from core.pipeline import BriefForgePipeline
from core.fusion.fact_store import ExtractedFact, ValidationIssue, SmartQuestion
from core.generation.brief_schema import BriefDocument, BriefSection, BriefField

# Page configuration
st.set_page_config(
    page_title="BriefForge • Enterprise Packaging Intelligence Studio",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        margin: 2px 0;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
    }
    .badge-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-critical { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .badge-warning { background-color: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
    .badge-pass { background-color: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; }
    .citation-tag {
        font-size: 11px;
        background-color: #EEF2FF;
        color: #3730A3;
        padding: 3px 8px;
        border-radius: 6px;
        border: 1px solid #C7D2FE;
        font-weight: 600;
    }
    .council-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.03);
    }
    .diff-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        margin-top: 10px;
    }
    .diff-table th {
        background: #0F172A;
        color: white;
        text-align: left;
        padding: 10px 14px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .diff-table td {
        padding: 12px 14px;
        border-bottom: 1px solid #E2E8F0;
        vertical-align: top;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "pipeline" not in st.session_state:
    st.session_state.pipeline = BriefForgePipeline()
if "brief" not in st.session_state:
    st.session_state.brief = None

pipeline: BriefForgePipeline = st.session_state.pipeline

# Auto-load benchmark on first boot for instant experience
if not pipeline.ingested_files:
    esko_dir = Path(r"c:\Users\sblpr\Downloads\Esko")
    pdf_file = esko_dir / "DancingFish_Granola_Berry_US_Carton (2)4def4e1.pdf"
    xl_file = esko_dir / "DancingFish_Granola_BerryCrunch_US_Content_Sheet (3)2057df9.xlsx"
    if pdf_file.exists() and xl_file.exists():
        pipeline.ingest_file(str(pdf_file))
        pipeline.ingest_file(str(xl_file))
        pipeline.analyze()
        pipeline.get_questions()
        st.session_state.brief = pipeline.generate_brief()

# Sidebar Controls
with st.sidebar:
    st.title("📦 BriefForge Studio")
    st.caption("Enterprise Packaging Intelligence Engine")
    st.markdown("---")
    
    st.subheader("🔑 Intelligence Core")
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if api_key:
        st.success(f"Gemini 2.5 Active ({api_key[:8]}...)")
    else:
        new_key = st.text_input("Gemini API Key", type="password")
        if new_key:
            os.environ["GEMINI_API_KEY"] = new_key
            st.rerun()

    st.markdown("---")
    st.subheader("⚡ Quick Scenarios")
    if st.button("🔄 Reset to Benchmark Files", use_container_width=True):
        pipeline.reset()
        esko_dir = Path(r"c:\Users\sblpr\Downloads\Esko")
        pipeline.ingest_file(str(esko_dir / "DancingFish_Granola_Berry_US_Carton (2)4def4e1.pdf"))
        pipeline.ingest_file(str(esko_dir / "DancingFish_Granola_BerryCrunch_US_Content_Sheet (3)2057df9.xlsx"))
        pipeline.analyze()
        pipeline.get_questions()
        st.session_state.brief = pipeline.generate_brief()
        st.rerun()

    st.markdown("---")
    scorecard = pipeline.get_readiness_scorecard()
    st.metric("Agency Readiness Score", f"{scorecard['readiness_score']}%")
    st.metric("Est. Pre-Press Cost Saved", f"${scorecard['estimated_cost_saved_usd']:,}")
    st.metric("Time-to-Market Saved", f"{scorecard['estimated_days_saved']} Days")

# Top Executive KPI Ribbon
scorecard = pipeline.get_readiness_scorecard()
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card" style="border-left: 4px solid {scorecard['badge_color']};">
        <div class="kpi-label">Agency Readiness Score</div>
        <div class="kpi-value" style="color:{scorecard['badge_color']};">{scorecard['readiness_score']}%</div>
        <div style="font-size:11px; font-weight:700; color:#475569;">{scorecard['status']}</div>
    </div>
    <div class="kpi-card" style="border-left: 4px solid #3B82F6;">
        <div class="kpi-label">Rework Cycles Prevented</div>
        <div class="kpi-value" style="color:#3B82F6;">{scorecard['rework_loops_prevented']} Loops</div>
        <div style="font-size:11px; color:#64748B;">Saves ~{scorecard['estimated_days_saved']} days pre-press turnaround</div>
    </div>
    <div class="kpi-card" style="border-left: 4px solid #10B981;">
        <div class="kpi-label">Pre-Press Cost Savings</div>
        <div class="kpi-value" style="color:#10B981;">${scorecard['estimated_cost_saved_usd']:,}</div>
        <div style="font-size:11px; color:#64748B;">Plate remakes &amp; recall avoidance</div>
    </div>
    <div class="kpi-card" style="border-left: 4px solid #F59E0B;">
        <div class="kpi-label">Audit Defects Detected</div>
        <div class="kpi-value" style="color:#F59E0B;">{len(pipeline.fact_store.issues)} Defects</div>
        <div style="font-size:11px; color:#64748B;">{scorecard['unresolved_critical']} Critical FDA / Pre-Press Blockers</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tabs = st.tabs([
    "📦 1. 3D Folded Carton WebGL",
    "🎨 2. 2D Dieline Net Inspector",
    "🔄 3. Before vs. After Visual Diff",
    "🧑‍⚖️ 4. Packaging Council Review",
    "💬 5. Smart Q&A Resolution Center",
    "📋 6. Master Brief Live Editor",
    "🌍 7. Global Market Jurisdictions",
    "📥 8. Agency Handover Suite",
    "📁 9. File Ingestion Hub"
])

# ==========================================
# TAB 1: 3D FOLDED CARTON WEBGL SIMULATOR
# ==========================================
with tabs[0]:
    st.subheader("📦 Interactive 3D Folded Carton Simulator (Esko Studio Grade)")
    st.write(
        "WebGL real-time 3D rendering of the folded packaging carton. "
        "Drag with your mouse to rotate 360°, zoom in to inspect panels, or click quick view buttons."
    )
    carton_3d_html = pipeline.get_3d_carton_html()
    st.components.v1.html(carton_3d_html, height=540, scrolling=False)

    col1, col2, col3 = st.columns(3)
    col1.info("💡 **Front Panel (PDP)**: Highlights mandatory lower 30% Net Quantity zone and cereal bowl photography.")
    col2.info("💡 **Left Panel**: Recalculated FDA 2016 vertical Nutrition Facts panel with true Added Sugars.")
    col3.info("💡 **Top Flap**: Verifies complete purging of the non-compliant 'NO ADDED SUGAR' badge.")

# ==========================================
# TAB 2: 2D DIELINE NET INSPECTOR
# ==========================================
with tabs[1]:
    st.subheader("🎨 Mechanical 2D Dieline Net Inspector")
    st.write(
        "Flat dieline net layout showing panel geometry, fold creases, and exact mechanical defect hotspot pins."
    )
    dieline_svg = pipeline.get_dieline_html()
    st.components.v1.html(dieline_svg, height=620, scrolling=False)

# ==========================================
# TAB 3: BEFORE VS AFTER VISUAL DIFF
# ==========================================
with tabs[2]:
    st.subheader("🔄 Side-by-Side Packaging Remediation Diff Matrix")
    st.write(
        "Direct audit comparison between the defective initial artwork / messy specifications and the remediated agency handover requirements."
    )
    diff_data = pipeline.get_diff_matrix()
    
    st.markdown("""
    <table class="diff-table">
        <thead>
            <tr>
                <th style="width: 14%;">Panel Location</th>
                <th style="width: 28%; background:#991B1B;">Original Artwork / Messy Input (Defect)</th>
                <th style="width: 32%; background:#065F46;">Remediated Production Specification</th>
                <th style="width: 26%;">Regulatory &amp; Technical Mandate</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)

    for row in diff_data:
        st.markdown(f"""
        <tr>
            <td style="font-weight:700; color:#0F172A;">{row['panel']}</td>
            <td style="color:#991B1B; background:#FFF1F2;">❌ {row['before_artwork']}</td>
            <td style="color:#065F46; background:#ECFDF5; font-weight:600;">✅ {row['after_remediated']}</td>
            <td style="font-size:12px; color:#475569;">{row['regulatory_driver']}</td>
        </tr>
        """, unsafe_allow_html=True)

    st.markdown("</tbody></table>", unsafe_allow_html=True)

# ==========================================
# TAB 4: PACKAGING COUNCIL REVIEW
# ==========================================
with tabs[3]:
    st.subheader("🧑‍⚖️ Multi-Agent Packaging Council Audit")
    st.write(
        "Four specialized AI personas simulate an enterprise review board, auditing regulatory law, pre-press engineering, brand identity, and circular sustainability."
    )

    verdicts = pipeline.council_verdicts
    if not verdicts:
        st.info("Convene council by running analysis.")
    else:
        for v in verdicts:
            st.markdown(f"""
            <div class="council-card" style="border-left: 5px solid {v.color_theme};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span style="font-size:24px;">{v.avatar_emoji}</span>
                        <div>
                            <div style="font-weight:800; font-size:15px; color:#0F172A;">{v.agent_name}</div>
                            <div style="font-size:12px; color:#64748B;">{v.role_title}</div>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <span class="badge-pill" style="background:{v.color_theme}22; color:{v.color_theme}; border:1px solid {v.color_theme};">{v.verdict}</span>
                        <div style="font-size:12px; font-weight:700; color:{v.color_theme}; margin-top:3px;">Score: {v.score}/100</div>
                    </div>
                </div>
                <div style="font-size:13.5px; color:#334155; margin:12px 0; line-height:1.6; background:#F8FAFC; padding:10px 14px; border-radius:6px;">
                    <strong>Executive Critique:</strong> {v.executive_critique}
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; font-size:12px;">
                    <div>
                        <strong style="color:#0F172A;">Key Findings:</strong>
                        <ul style="margin:4px 0 0 0; padding-left:18px; color:#475569;">
                            {"".join(f"<li>{k}</li>" for k in v.key_findings)}
                        </ul>
                    </div>
                    <div>
                        <strong style="color:#0F172A;">Mandatory Sign-Off Conditions:</strong>
                        <ul style="margin:4px 0 0 0; padding-left:18px; color:#065F46;">
                            {"".join(f"<li>{c}</li>" for c in v.mandatory_signoff_conditions)}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 5: SMART Q&A RESOLUTION CENTER
# ==========================================
with tabs[4]:
    st.subheader("💬 Smart Q&A Resolution Center")
    st.write(
        "BriefForge automatically transformed complex document discrepancies into high-impact, prioritized choices for the Brand Manager."
    )

    questions = pipeline.fact_store.questions
    if not questions:
        st.info("No questions pending.")
    else:
        for idx, q in enumerate(questions):
            with st.container():
                st.markdown(f"#### ❓ Question {idx+1}: {q.question_text}")
                st.caption(f"**Regulatory / Commercial Impact:** {q.context}")
                
                opts = [opt["label"] for opt in q.options]
                selected_label = st.radio(
                    f"Choose approved directive for Q{idx+1}:",
                    options=opts,
                    key=f"radio_{q.question_id}",
                    index=0
                )
                
                chosen_val = next((opt["value"] for opt in q.options if opt["label"] == selected_label), selected_label)
                if st.button(f"Confirm Approval for Q{idx+1}", key=f"btn_confirm_{q.question_id}"):
                    pipeline.answer_question(q.question_id, chosen_val)
                    st.session_state.brief = pipeline.generate_brief()
                    st.success("Decision logged in audit trail and brief updated!")
                    st.rerun()
                st.markdown("---")

# ==========================================
# TAB 6: MASTER BRIEF LIVE EDITOR
# ==========================================
with tabs[5]:
    st.subheader("📋 Production Packaging Design Brief (Live Draft)")
    brief: BriefDocument = st.session_state.brief
    
    if brief:
        brief.title = st.text_input("Project Title", value=brief.title)
        brief.executive_summary = st.text_area("Executive Summary", value=brief.executive_summary, height=110)

        for s_idx, section in enumerate(brief.sections):
            with st.expander(section.title, expanded=True):
                for f_idx, field in enumerate(section.fields):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        field.value = st.text_area(field.label, value=field.value, height=65, key=f"edit_sec_{s_idx}_{f_idx}")
                    with c2:
                        st.markdown(f"<div style='margin-top:28px;'><span class='citation-tag'>📌 {field.source}</span></div>", unsafe_allow_html=True)

        with st.expander("5. Mandatory Pre-Press & Artwork Corrections Checklist", expanded=True):
            for c_idx, item in enumerate(brief.corrections):
                item.completed = st.checkbox(item.description, value=item.completed, key=f"chk_brief_{c_idx}")

        with st.expander("6. Open Questions for the Design Agency", expanded=True):
            for q in brief.open_questions:
                st.markdown(f"- ❓ **{q.question}**")

# ==========================================
# TAB 7: GLOBAL MARKET JURISDICTIONS
# ==========================================
with tabs[6]:
    st.subheader("🌍 Multi-Market Regulatory Localization Engine")
    st.write(
        "Packaging regulations diverge significantly between global territories. Compare how this folding carton specification adapts across the US, EU/UK, and Canada."
    )

    market_choice = st.selectbox("Select Target Retail Market:", ["United States (FDA)", "European Union & UK", "Canada (Health Canada / CFIA)"])
    
    code = "US" if "United States" in market_choice else ("EU_UK" if "European" in market_choice else "CANADA")
    rules = pipeline.get_jurisdiction_guide(code)
    
    st.markdown(f"### 📜 Directive Profile: {rules['title']}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Net Weight Format:** {rules['net_weight_format']}")
        st.markdown(f"**Allergen Declaration Protocol:** {rules['allergen_rules']}")
        st.markdown(f"**Front-of-Pack Nutrition Lozenges:** {rules['front_of_pack_lozenges']}")
    with col2:
        st.markdown(f"**Sugar & Sweetener Claims:** {rules['sugar_claims']}")
        st.markdown(f"**Nutrition Facts Panel Format:** {rules['nutrition_panel']}")

# ==========================================
# TAB 8: AGENCY HANDOVER SUITE (5 FORMATS)
# ==========================================
with tabs[7]:
    st.subheader("📦 Final Agency Handover Suite (5 Formats)")
    st.write(
        "Export production-ready briefs matching and surpassing Esko AI Brief Studio specifications. All downloads include complete source citations."
    )

    brief = st.session_state.brief
    if brief:
        md_content = pipeline.export(brief, fmt="markdown")
        html_content = pipeline.export(brief, fmt="html")
        json_content = pipeline.export(brief, fmt="json")
        docx_bytes = pipeline.export(brief, fmt="docx")
        xml_content = pipeline.export(brief, fmt="xml")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.download_button(
            "📥 Markdown (.md)",
            data=md_content,
            file_name="Esko_Packaging_Design_Brief.md",
            mime="text/markdown",
            use_container_width=True
        )
        c2.download_button(
            "🖨️ Print HTML (.html)",
            data=html_content,
            file_name="Esko_Packaging_Design_Brief_Print.html",
            mime="text/html",
            use_container_width=True
        )
        c3.download_button(
            "💾 Esko JSON (.json)",
            data=json_content,
            file_name="Esko_Brief_Traceability.json",
            mime="application/json",
            use_container_width=True
        )
        c4.download_button(
            "📄 Word (.docx)",
            data=docx_bytes,
            file_name="Esko_Packaging_Design_Brief.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        c5.download_button(
            "⚙️ Esko XML (.xml)",
            data=xml_content,
            file_name="Esko_Job_Ticket.xml",
            mime="application/xml",
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🖥️ Certified Print Layout Preview")
        st.components.v1.html(html_content, height=850, scrolling=True)

# ==========================================
# TAB 9: FILE INGESTION HUB
# ==========================================
with tabs[8]:
    st.subheader("📁 Ingest Additional Packaging Documents")
    st.write("Upload additional supplier spec sheets, lab assays, regulatory certificates, or artwork revisions.")
    
    new_files = st.file_uploader(
        "Upload files for knowledge fusion",
        type=["pdf", "xlsx", "xls", "docx", "txt", "md", "png", "jpg"],
        accept_multiple_files=True,
        key="tab9_uploader"
    )
    if new_files and st.button("Ingest Uploaded Files", type="primary"):
        with st.status("Extracting and fusing data...", expanded=True) as status:
            for uf in new_files:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uf.name}")
                temp_file.write(uf.getbuffer())
                temp_file.close()
                pipeline.ingest_file(temp_file.name)
            pipeline.analyze()
            pipeline.get_questions()
            st.session_state.brief = pipeline.generate_brief()
            status.update(label="Files ingested and fused!", state="complete")
        st.rerun()

    st.markdown("#### Currently Ingested Files:")
    for f in pipeline.ingested_files:
        st.markdown(f"- 📄 `{f}`")
