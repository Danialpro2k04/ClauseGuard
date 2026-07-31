import os
import sys
import json
from groq import Groq
from dotenv import load_dotenv

#Ensure parent directory is in python path to import server tools & agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.mcp_server import log_for_human_review
from agents.intake import run_intake_agent
from agents.retrieval import run_retrieval_agent

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"


def score_clause_risk(contract_name: str, clause_info: dict) -> dict:
    """Evaluates a single contract clause against retrieved company policy context

    and assigns a risk score.

    Args:
        contract_name: Name or ID of the contract document.
        clause_info: Dictionary containing clause text, statement, and retrieved context.

    Returns:
        dict: Evaluated clause with risk level, justification, and recommendation.
    """
    clause_title = clause_info.get("clause_title", "Untitled Clause")
    clause_text = clause_info.get("clause_text", "")
    policy_context = clause_info.get("retrieved_policy_context", "")

    system_prompt = (
        "You are an expert Corporate Compliance Risk Assessor. Your task is to compare a "
        "proposed contract clause against retrieved internal company compliance policies.\n\n"
        "Assign one of the following risk levels:\n"
        "- HIGH: Direct violation or contradiction of company policy, severe legal/security risk.\n"
        "- MEDIUM: Ambiguous language, partial mismatch, or missing required protective terms.\n"
        "- LOW: Fully compliant with company policy, zero or minimal risk.\n\n"
        "Return ONLY valid JSON with this structure:\n"
        "{\n"
        '  "risk_level": "HIGH | MEDIUM | LOW",\n'
        '  "justification": "Clear, objective breakdown of why this risk score was assigned relative to company policy.",\n'
        '  "recommendation": "Suggested modification or action for the legal team."\n'
        "}"
    )

    user_prompt = f"""
CONTRACT CLAUSE TITLE: {clause_title}
CONTRACT CLAUSE TEXT:
"{clause_text}"

RETRIEVED COMPANY POLICY CONTEXT:
{policy_context}
"""

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )

    score_data = json.loads(response.choices[0].message.content)
    risk_level = score_data.get("risk_level", "MEDIUM").upper()
    justification = score_data.get("justification", "")
    recommendation = score_data.get("recommendation", "")

    #MCP Integration: Log HIGH and MEDIUM risk clauses to Human-in-the-Loop queue
    if risk_level in ["HIGH", "MEDIUM"]:
        log_msg = log_for_human_review(
            contract_name=contract_name,
            clause_text=clause_text,
            risk_level=risk_level,
            justification=justification
        )
        print(f"MCP HITL Tool: {log_msg}")

    return {
        "clause_title": clause_title,
        "clause_text": clause_text,
        "risk_level": risk_level,
        "justification": justification,
        "recommendation": recommendation
    }


def run_risk_scoring_agent(retrieval_payload: dict, contract_name: str = "Sample_Contract.txt") -> dict:
    """Runs the risk scoring agent across all retrieved clauses in a payload."""
    scored_clauses = []
    clauses = retrieval_payload.get("clauses", [])

    print(f" Risk Scorer evaluating {len(clauses)} clause(s)...")
    for clause in clauses:
        evaluated = score_clause_risk(contract_name, clause)
        scored_clauses.append(evaluated)

    return {
        "contract_name": contract_name,
        "document_type": retrieval_payload.get("document_type", "Unknown"),
        "evaluations": scored_clauses
    }


# if __name__ == "__main__":
#     #Full end-to-end dry run: Intake -> Retrieve -> Score -> Log
#     sample_contract = """
#     CONFIDENTIALITY AND DATA STORAGE AGREEMENT
#     The Recipient agrees to store all Customer Data on third-party cloud servers without requiring explicit encryption at rest, provided access controls are in place. Furthermore, Recipient shall retain all proprietary logs for a minimum of 10 years following termination.
#     """

#     print("--- STEP 1: Intake ---")
#     intake_out = run_intake_agent(sample_contract)

#     print("\n--- STEP 2: Retrieval ---")
#     retrieval_out = run_retrieval_agent(intake_out, top_k=2)

#     print("\n--- STEP 3: Risk Scoring ---")
#     final_report = run_risk_scoring_agent(retrieval_out, contract_name="NDA_Vendor_Draft.txt")

#     print("\n✅ Final Compliance Report:")
#     print(json.dumps(final_report, indent=2))