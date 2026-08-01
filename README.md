# ClauseGuard: MCP-Powered Legal Compliance & Risk Scoring Pipeline

An MCP-native agentic system that automates contract compliance reviews. ClauseGuard parses multi-format legal documents (`.pdf`, `.docx`, `.txt`), extracts risk-bearing clauses, evaluates them against internal corporate policies stored in a local vector database (Qdrant), scores potential risk levels, and flags violations for Human-in-the-Loop (HITL) review.

---

## Why the live demo doesn't run through MCP

This repo includes a full MCP (Model Context Protocol) server in
`server/mcp_server.py`, but the hosted live demo doesn't call it. That's
intentional, not a shortcut.

MCP servers communicate over local transport (stdio) with a client running
on the same machine — like Claude Desktop or Cursor — not with anonymous
visitors over the public web. There's no equivalent of a "public MCP
endpoint" the way there is with a REST API.

So this project has two front doors to the same core agents:

- **Live demo** (`clauseguardlive.streamlit.app`) — a Streamlit app that
  calls the Intake, Retrieval, and Risk-Scoring agents directly, so anyone
  can try the full pipeline instantly with zero setup.
- **MCP server** (`server/mcp_server.py`) — exposes `search_policy_docs`
  and `log_for_human_review` as MCP tools, so the same capability can be
  plugged directly into an MCP client like Claude Desktop for local use.

Same agents, same logic — two different doors, built for two different
audiences.

##  System Architecture

The pipeline operates via a 4-stage agentic workflow integrated with Model Context Protocol (MCP) tools and a local vector database.

```
                               ┌───────────────────────────┐
                               │   Incoming Contract       │
                               │  (.pdf, .docx, or .txt)   │
                               └─────────────┬─────────────┘
                                             │
                                             ▼
                               ┌───────────────────────────┐
                               │   Multi-Format Parser     │
                               └─────────────┬─────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. INTAKE AGENT (Groq LLM)                                                                │
│    • Identifies contract type & risk-bearing clauses.                                     │
│    • Formulates declarative compliance statements & outputs structured JSON.              │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. RETRIEVAL AGENT (MCP Vector Search Tool)                                               │
│    • Calls MCP `search_policy_docs` tool.                                                 │
│    • Queries local Qdrant Vector DB for top-K matching corporate policy chunks.           │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. RISK-SCORING AGENT                                                                     │
│    • Compares contract statements against retrieved corporate policies.                   │
│    • Outputs Risk Level (HIGH / MEDIUM / LOW), Justification, & Recommendations.          │
│    • LOW Risk  ──► Automatically Approved.                                                │
│    • MED / HIGH Risk ──► Flagged & logged via MCP to `pending_reviews.json`.              │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. HUMAN-IN-THE-LOOP (HITL) DASHBOARD (Streamlit Web Interface)                           │
│    • Interactive UI for legal teams to review, edit, and clear flagged risks.             │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- **Multi-Format Ingestion**: Native text extraction support for `.pdf`, `.docx`, and `.txt` contracts.
- **Deterministic Structured JSON Output**: Enforced schema constraints on LLM responses to ensure zero pipeline crashes.
- **Local Vector Storage**: Zero third-party data-leakage risk by hosting policy embeddings locally using Qdrant.
- **MCP Tooling Architecture**: Decoupled Model Context Protocol tools for vector policy retrieval and HITL event logging.
- **Fail-Safe Risk Defaults**: Automatically defaults to MEDIUM risk on edge-case parsing failures to force human verification.
- **Streamlit HITL Review Dashboard**: Dedicated interface for legal teams to audit flagged clauses and policy conflicts.

---

## 📂 Project Structure

```
.
├── agents/                  # Multi-agent system modules (Intake, Retrieval, Risk Scorer)
├── contracts/               # Target contract files (.pdf, .docx, .txt) for testing & review
├── corpus/                  # Source internal corporate policy & regulatory documents
├── qdrant_db/                # Local persistent storage for Qdrant vector database embeddings
├── server/                  # Server logic (ingest_corpus.py & mcp_server.py tools)
├── PROGRESS.md               # Detailed project dev log & architectural decision notes
├── app.py                    # Streamlit web interface for Human-In-The-Loop (HITL) review
├── constraints.txt           # Transitive dependency caps (resolves PyTorch/NumPy bugs)
├── pipeline.py                # Main execution script running end-to-end processing
└── requirements.txt           # Primary project dependencies
```

---

##  Critical Dependency Setup (`requirements.txt` + `constraints.txt`)

### Understanding the Version Resolution

Building high-performance ML/RAG pipelines on specific OS targets (e.g., Intel-based Macs x86_64) can lead to cascading library conflicts:

- `transformers>=5.0` hard-requires `torch>=2.4` at runtime.
- `torch>=2.4` dropped binary wheel releases for Intel Mac (macOS x86_64), requiring a fallback to `torch==2.2.2`.
- `numpy 2.x` breaks the C-API bridge inside `torch==2.2.2`, causing crashes on `.numpy()` vector conversions.

To maintain a clean `requirements.txt` without editing top-level packages, we use a separate `constraints.txt` file to enforce version ceilings across transitive dependencies.

### Content Breakdown

`requirements.txt` defines high-level dependencies:

```
groq
qdrant-client
sentence-transformers
transformers
pypdf
python-docx
streamlit
```

`constraints.txt` pins specific lower-level bounds to guarantee runtime compatibility:

```
transformers<5.0.0
torch==2.2.2
numpy<2.0.0
```

---

##  Quick Start & Installation

### 1. Prerequisites

- Python 3.10 or 3.11
- Groq API Key (set in your environment variables as `GROQ_API_KEY`)

### 2. Environment Setup

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/your-username/clauseguard-agent.git
cd clauseguard-agent

python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies Using Constraints

To install all dependencies while forcing pip to respect version ceilings:

```bash
pip install -r requirements.txt -c constraints.txt
```

**Why `-c constraints.txt`?**
The `-c` flag tells pip to restrict transitive sub-dependencies without changing your primary requirement specifications. This ensures `torch`, `transformers`, and `numpy` resolve to mutually compatible versions.

---

## ⚙️ Running the Pipeline

### Step 1: Ingest Corporate Policy Corpus

Place all corporate policies into the `corpus/` directory, then run the ingestion script:

```bash
python server/ingest_corpus.py
```

This process chunks policy documents into 500-character segments (50-character overlap) and generates local vector embeddings stored in `./qdrant_db`.

### Step 2: Run Automated Contract Review

Pass any contract file (`.pdf`, `.docx`, or `.txt`) into the pipeline:

```bash
python pipeline.py
```

**Console Output Example:**

```
  Starting Compliance Review for: sample_vendor_contract.pdf

🔹 [Step 0/3] Reading and extracting contract text...
🔹 [Step 1/3] Running Intake Agent (Parsing clauses & formulating statements)...
   └── Identified Document Type: MSA
   └── Extracted 6 risk-bearing clause(s).

🔹 [Step 2/3] Running Retrieval Agent (Searching vector database)...
   └─ Querying policy database for clauses...

🔹 [Step 3/3] Running Risk-Scoring Agent (Evaluating policy compliance)...

 Compliance Review Completed Successfully!
 Report generated & flagged items sent to pending_reviews.json
```

### Step 3: Launch Human-in-the-Loop (HITL) Dashboard

To review and resolve flagged HIGH or MEDIUM risk items:

```bash
streamlit run app.py
```

Open your browser to [http://localhost:8501](http://localhost:8501) to view non-compliant clauses, inspect matched company policy passages, adjust risk tags, and sign off on legal reviews.
