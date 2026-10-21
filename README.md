# 📦 BriefForge — AI Packaging Design Brief Studio

> **From Product Idea to Agency Design Brief**: Autonomous packaging knowledge fusion, regulatory audit & traceable brief synthesis.

Built for the **Esko Challenge: "From Product Idea to Design Brief"**.

---

## 🌟 What BriefForge Does

Brand managers launching products typically start from a messy baseline:
- An old packaging artwork PDF or dieline proof
- A product specification spreadsheet with conflicting notes
- Word/PDF regulatory documents or meeting memos
- Image photos or character assets

**BriefForge turns this messy starting point into a production-ready, agency-grade packaging design brief.**

---

## 🎯 How BriefForge Solves Every Requirement

| Challenge Requirement | How BriefForge Solves It | Technical Engine |
| :--- | :--- | :--- |
| **1. Read messy files & understand product packaging** | Ingests PDF packaging artwork proofs, multi-tab Excel content sheets, Word docs, and photos. | Multimodal Gemini 2.5 Vision + pure Python PDF & openpyxl parsers. |
| **2. Ask smart follow-up questions when information is missing** | Identifies unconfirmed recipes, illegible serving sizes, and risks; presents prioritized, multiple-choice questions with recommended compliant choices. | `core/questioning/question_generator.py` |
| **3. Identify inconsistencies or unclear information** | Cross-references documents to find recipe mismatches (e.g. Honey 1% on artwork vs Honey 9% in Excel; Walnuts omitted in spreadsheet). | `core/fusion/cross_reference.py` & `core/validation/conflict_detector.py` |
| **4. Create a clear final brief for design agencies** | Synthesizes an agency-ready brief with executive summary, 4 structured specification sections, an 11-point pre-press correction checklist, and open technical converter questions. | `core/generation/brief_composer.py` |
| **5. Show where important information came from** | Every single attribute is tagged with an audit badge citing the exact file, panel, or spreadsheet cell coordinates (e.g., `Carton PDF (Front Panel PDP) & Content Sheet Excel (Row 0)`). | `core/fusion/fact_store.py` |
| **6. Allow the user to review and edit the brief** | Interactive live editor lets the brand manager modify any text field, check off mechanical corrections, and re-export in real time. | Streamlit Interactive UI (`app.py`) |
| **7. "Think beyond a chatbot"** | A 6-stage autonomous AI/ML pipeline with deterministic FDA 21 CFR / FALCPA validation rules, not a single-turn conversational prompt. | `core/pipeline.py` |

---

## 🏗️ Architecture

```
                      [ Carton Artwork PDF ]    [ Content Sheet XLSX ]    [ Technical Docs ]
                                │                         │                      │
                                └────────────┬────────────┴──────────────────────┘
                                             ▼
                                  STAGE 1: DOCUMENT INGESTION
                                (Multimodal Vision + Cell Parsing)
                                             │
                                             ▼
                                   STAGE 2: KNOWLEDGE FUSION
                              (Atomic Fact Store & Provenance Matrix)
                                             │
                                             ▼
                                STAGE 3: VALIDATION & COMPLIANCE
                          (Deterministic FDA 21 CFR / FALCPA Rules Engine)
                                             │
                                             ▼
                                  STAGE 4: SMART QUESTIONING
                            (Contextual Multi-Choice Q&A for Brand Manager)
                                             │
                                             ▼
                                   STAGE 5: BRIEF SYNTHESIS
                           (Agency Handover Document Composition)
                                             │
                                             ▼
                                 STAGE 6: REVIEW & MULTI-EXPORT
                        [ Markdown (.md) ]  [ Print HTML (.html) ]  [ JSON Traceability ]
```

---

## ⚖️ Built-in Regulatory & Mechanical Audits

BriefForge automatically checks for:
- 🔴 **FDA 21 CFR 101.60**: "No Added Sugar" claims on formulations containing Honey, Coconut Sugar, or Cane Sugar.
- 🔴 **FTC & Vegan Action**: "Certified Vegan" badges displayed on products with bee honey.
- 🔴 **FALCPA 21 U.S.C. 343(w)**: Intentional formulation tree nuts listed under advisory "May Contain" instead of bold "CONTAINS:".
- 🔴 **FDA 21 CFR 101.7**: Missing dual Net Quantity statements in the lower 30% of the PDP.
- 🔴 **Pre-Press Quality**: Dieline annotations left in printable separation layers (`Front panel Orientation`, `Copy free`).
- 🟡 **FTC Guidelines**: Food photography depicting fresh fruit without mandatory `Serving Suggestion. Fresh fruit not included.`
- 🟡 **US Market Standards**: European/UK color-coded traffic light nutrition lozenges on US cartons.
- 🟡 **Pre-Press Typos**: Catching typos such as `RECYCABLE` ➔ `RECYCLABLE` and `DIETRAY` ➔ `DIETARY`.

---

## 🚀 How to Run BriefForge

### Option A: 1-Click Launch (Windows)
Double-click:
```
C:\Users\sblpr\Downloads\Esko\run_briefforge.bat
```

### Option B: Terminal Command
```powershell
cd C:\Users\sblpr\Downloads\Esko\briefforge
& "C:\Users\sblpr\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run app.py
```

The web studio opens in your browser at `http://localhost:8501`.

Click **"📥 Load Esko Benchmark Files"** in the sidebar to run the full Dancing Fish Granola benchmark demonstration!
