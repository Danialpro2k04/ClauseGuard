# ClauseGuard Project Progress Log

This document tracks the engineering progress, architectural decisions, and technical roadblocks resolved during the development of ClauseGuard—a pragmatic, LLM-powered contract compliance review system.

---

## 1. System Architecture & State Schema
We defined a 4-node execution pipeline to handle contract analysis with clear boundaries and state transitions.

[Intake Node] ──> [Retrieval Node] ──> [Risk-Scoring Node] ──> [Human Approval Node]

- **Shared State Schema (`ContractReviewState`)**: Houses the uploaded contract, chunked legal text, retrieved reference clauses, risk scores, and final validation status.
- **Pragmatic Design**: The architecture prioritizes deterministic data retrieval and reliable scoring over unpredictable, fully autonomous agentic behavior.

---

## 2. Infrastructure & Tech Stack
- **Vector Database**: Qdrant Cloud (for scalable, remote vector storage and quick semantic searches).
- **Embeddings**: Free, local Hugging Face model (`sentence-transformers/all-MiniLM-L6-v2`) to eliminate API cost during chunk indexing.
- **Frameworks**: LangChain (specifically `langchain-text-splitters` for semantic-preserving recursive chunking).
- **Version Control**: Initialized local Git repository and successfully linked to GitHub for future CI/CD deployment.

---

## 3. Roadblocks & Resolutions (Intel Mac Dependency Issues)
We encountered a severe dependency blocker when trying to install machine learning libraries on Python 3.14/3.13 on an Intel-based Mac. 

### The Problem:
- PyTorch officially ended macOS Intel (`x86_64`) binary support after version `2.2.2`.
- Modern Hugging Face `transformers` libraries require `torch >= 2.4`.
- Modern `numpy 2.x` is incompatible with `torch 2.2.2`.
- This mismatch broke imports, resulting in a `NameError: name 'torch' is not defined` crash.

### The Solution:
We downgraded and aligned the environment to versions compatible with the Intel platform:
1. Created a virtual environment using **Python 3.12** instead of 3.14.
2. Uninstalled conflicting modern ML packages.
3. Installed a matching legacy stack:
   - Downgraded NumPy: `numpy<2`
   - Downgraded Transformers: `transformers<4.46`
   - Allowed PyTorch to sit safely at version `2.2.2`.

This resolved all import and memory compatibility conflicts.

---

## 4. Current Milestone Accomplished
- **Corpus Setup**: Established standard legal documents (GDPR, MSAs, NDAs) in `/corpus`.
- **Ingestion Script**: Developed and tested `load_documents.py`.
- **Successful Run**: The script successfully initializes the local embedding model, splits raw text files, connects to the Qdrant Cloud cluster over HTTPS, and uploads the vectors cleanly.

---

## Next Steps
1. **Pipeline Orchestration**: Implement the four core state nodes using LangGraph/LangChain.
2. **Evaluation Framework**: Set up 30-48 labeled mock compliance test cases to evaluate chunk-retrieval accuracy and model scoring consistency.