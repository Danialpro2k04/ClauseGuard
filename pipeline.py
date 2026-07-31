import os
import sys
import json
import pypdf
from docx import Document

from agents.intake import run_intake_agent
from agents.retrieval import run_retrieval_agent
from agents.risk_scorer import run_risk_scoring_agent


def extract_text_from_file(file_path: str) -> str:
    """Extracts raw text content from TXT, PDF, or DOCX contract files.

    Args:
        file_path: Path to the target contract file.

    Returns:
        str: Extracted plain text string from the file.
    """
    ext = os.path.splitext(file_path)[1].lower()

    # 1. Plain Text Files
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # 2. PDF Documents
    elif ext == ".pdf":
        reader = pypdf.PdfReader(file_path)
        extracted_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)
        return "\n".join(extracted_text)

    # 3. Word Documents (.docx)
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    else:
        raise ValueError(
            f"Unsupported file format: '{ext}'. Supported formats are .txt, .pdf, and .docx"
        )


def review_contract(file_path: str, top_k_policies: int = 2) -> dict:
    """Executes the full ClauseGuard compliance pipeline on a target contract file.

    Pipeline sequence:
      1. File Parser (TXT/PDF/DOCX)
      2. Intake Agent (Extracts clauses into structured JSON)
      3. Retrieval Agent (Queries Qdrant vector database for policies)
      4. Risk-Scoring Agent (Evaluates risk & triggers MCP HITL queue)

    Args:
        file_path: Path to the raw contract file (.txt, .pdf, or .docx).
        top_k_policies: Number of relevant policy context passages to fetch per clause.

    Returns:
        dict: Complete structured risk evaluation report.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Contract file not found at path: {file_path}")

    contract_name = os.path.basename(file_path)

    print(f"  Starting Compliance Review for: {contract_name}")

    # Step 0: Extract text from file (Supports .txt, .pdf, .docx)
    print(" [Step 0/3] Reading and extracting contract text...")
    contract_text = extract_text_from_file(file_path)

    # Step 1: Intake Agent
    print(" [Step 1/3] Running Intake Agent (Parsing clauses & formulating statements)...")
    intake_data = run_intake_agent(contract_text)
    print(f"   └── Identified Document Type: {intake_data.get('document_type')}")
    print(f"   └── Extracted {len(intake_data.get('clauses', []))} risk-bearing clause(s).")

    # Step 2: Retrieval Agent (MCP Qdrant Tool)
    print("\n [Step 2/3] Running Retrieval Agent (Searching vector database)...")
    retrieval_data = run_retrieval_agent(intake_data, top_k=top_k_policies)

    # Step 3: Risk-Scoring Agent (MCP HITL Logging)
    print("\n [Step 3/3] Running Risk-Scoring Agent (Evaluating policy compliance)...")
    final_report = run_risk_scoring_agent(retrieval_data, contract_name=contract_name)

    print("\n Compliance Review Completed Successfully!")
    return final_report


if __name__ == "__main__":
    #Ensure contracts directory exists and contains a test file
    sample_dir = os.path.join(os.path.dirname(__file__), "contracts")
    sample_file = os.path.join(sample_dir, "sample_vendor_contract.pdf")

    if not os.path.exists(sample_file):
        print(f"Error: Sample contract file not found at {sample_file}. Please add a .txt, .pdf, or .docx file for testing.")
        exit(1)

    report = review_contract(sample_file)
    print("\n Final Assessment Summary:")
    print(json.dumps(report, indent=2))