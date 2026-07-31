import os
import sys
import json

#Ensure parent directory is in python path to resolve server import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.mcp_server import search_policy_docs
from agents.intake import run_intake_agent


def run_retrieval_agent(intake_data: dict, top_k: int = 2) -> dict:
    """Queries the Qdrant policy database via the search_policy_docs MCP tool

    for each declarative compliance statement extracted by the Intake Agent.

    Args:
        intake_data: Structured dictionary output from run_intake_agent().
        top_k: Number of relevant policy passages to retrieve per clause.

    Returns:
        dict: Combined payload containing contract metadata, clauses, and retrieved policy context.
    """
    evaluated_clauses = []

    clauses = intake_data.get("clauses", [])
    print(f"🔍 Retrieval Agent processing {len(clauses)} clause(s)...")

    for idx, clause in enumerate(clauses, start=1):
        statement = clause.get("compliance_statement", "")
        print(f"  └─ [{idx}/{len(clauses)}] Querying policy database for: '{statement[:60]}...'")

        #Query Qdrant via the MCP search tool
        retrieved_context = search_policy_docs(query_text=statement, limit=top_k)

        evaluated_clauses.append({
            "clause_title": clause.get("clause_title", "Untitled Clause"),
            "clause_text": clause.get("clause_text", ""),
            "compliance_statement": statement,
            "retrieved_policy_context": retrieved_context
        })

    return {
        "document_type": intake_data.get("document_type", "Unknown"),
        "clauses": evaluated_clauses
    }


# if __name__ == "__main__":
#     # Test end-to-end integration of Intake -> Retrieval
#     sample_contract = """
#     CONFIDENTIALITY AND DATA STORAGE AGREEMENT
#     The Recipient agrees to store all Customer Data on third-party cloud servers without requiring explicit encryption at rest, provided access controls are in place. Furthermore, Recipient shall retain all proprietary logs for a minimum of 10 years following termination.
#     """

#     print("--- STEP 1: Intake Agent ---")
#     intake_output = run_intake_agent(sample_contract)

#     print("\n--- STEP 2: Retrieval Agent ---")
#     retrieved_output = run_retrieval_agent(intake_output, top_k=2)

#     print("\n✅ Final Combined Output:")
#     print(json.dumps(retrieved_output, indent=2))