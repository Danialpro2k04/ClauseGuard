import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def run_intake_agent(contract_text: str) -> dict:
    """Parses contract text and identifies risk-bearing clauses, generating

    declarative compliance statements to match against company policies.

    Args:
        contract_text: The text of the incoming contract.

    Returns:
        dict: Containing 'document_type' and list of 'clauses' with 'compliance_statement'.
    """
    system_prompt = (
        "You are an expert Legal Intake Compliance Agent. Your job is to analyze contract text "
        "and identify key risk-bearing clauses (e.g., data security, liability, data retention, IP).\n\n"
        "CRITICAL INSTRUCTION: Do NOT generate questions. Instead, formulate clear, direct, "
        "declarative STATEMENTS summarizing what the contract stipulates or permits. "
        "These statements will be semantically matched against company policy documents.\n\n"
        "Return ONLY valid JSON with this exact structure:\n"
        "{\n"
        '  "document_type": "NDA | MSA | Vendor Agreement | Unknown",\n'
        '  "clauses": [\n'
        '    {\n'
        '      "clause_title": "Title or summary of clause",\n'
        '      "clause_text": "Exact or verbatim snippet from the contract",\n'
        '      "compliance_statement": "Declarative statement of what the clause permits/requires (e.g., \'Data storage at rest is not required to be encrypted.\')"\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this contract text:\n\n{contract_text}"}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )

    result_json = response.choices[0].message.content
    return json.loads(result_json)


# if __name__ == "__main__":
#     # Test script with sample contract text
#     sample_contract = """
#     CONFIDENTIALITY AND DATA STORAGE AGREEMENT
#     The Recipient agrees to store all Customer Data on third-party cloud servers without requiring explicit encryption at rest, provided access controls are in place. Furthermore, Recipient shall retain all proprietary logs for a minimum of 10 years following termination.
#     """

#     print("🚀 Running Intake Agent test...\n")
#     analysis = run_intake_agent(sample_contract)
#     print(json.dumps(analysis, indent=2))