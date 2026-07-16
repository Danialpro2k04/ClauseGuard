
Gemini
New chat
Search chats
Images
New
Library
LinkedIn Reach Strategy for Students
write a description for this project to add to github, Forget agents and graphs for a second. Imagine you work at a company, and every time someone signs a contract, a person has to read it and answer: "Does anything in this contract violate our company's policies?" That's it. That's the whole product. You're automating that one question, but doing it carefully enough that a human still signs off before anything final happens. The 4 "agents" are just 4 steps in that process, done by an LLM instead of a human: Intake agent — reads the contract, figures out what kind of document it is, and figures out what question to even ask (e.g. "does this NDA's data retention clause conflict with our GDPR policy?") Retrieval agent — goes and finds the actual company policy text relevant to that question (this is the RAG part — it searches your policy documents in Qdrant) Risk-scoring agent — reads the policy text it found + the contract clause, and decides: is this HIGH / MEDIUM / LOW risk, and why Human approval step — a person looks at the AI's HIGH/MEDIUM verdict and clicks approve or reject before anything is final That's the entire system. No magic — a smart search + a careful reasoning step + a safety net.
Enhance Interview Prep Prompt for Claude
Upwork Catalog Image Prompts: RAG Chatbot
Understanding AWS Lambda Serverless Computing
AI Temperature: Creativity vs. Predictability
Understanding Loom Notes
AI Project Challenges and Solutions
Startup Idea Generation Refined
Understanding SaaS: Software as a Service
Explaining React Code Simply
CPU Scheduling Algorithms: FCFS vs. Round Robin
Probability and Statistics Request Failed
Pi vs. Phi on Calculator
Probability and Statistics Exam Prep
Chatbot Project: Implementation and Domain
Hottest Stars and Their Planets
Interpreting Mathematical Expressions: Ambiguity
Uploading Your CV to LinkedIn
Turing Machine for Binary Subtraction
Multivariable Calculus: Gradient Vectors Explained
Machine Learning Model Concepts Explained
Bhang Identification and Thandai Risks
Computer Architecture: RISC, CISC, SIMD, MIMD
Upload Project to GitHub Via CLI
Candle ML Framework Hardware Support
Delta Lake Features and Best Practices
Edit Screen Recordings on Mac
Update Web Page Code
MacBook YouTube Lag Troubleshooting Guide
CSS Fixes and Layout Adjustments
Fix Hero Bio Alignment CSS
Python Environment Debugging
LangChain Tool Decorator Best Practices
Gelato: Italian Ice Cream Explained
API Image Analysis and Payload Generation
IMAP Settings Unavailable Tool
Turing Test Reminder Reply Options
Conversation with Gemini
write a description for this project to add to github,



Forget agents and graphs for a second. Imagine you work at a company, and every time someone signs a contract, a person has to read it and answer: "Does anything in this contract violate our company's policies?"

That's it. That's the whole product. You're automating that one question, but doing it carefully enough that a human still signs off before anything final happens.

The 4 "agents" are just 4 steps in that process, done by an LLM instead of a human:



Intake agent — reads the contract, figures out what kind of document it is, and figures out what question to even ask (e.g. "does this NDA's data retention clause conflict with our GDPR policy?")

Retrieval agent — goes and finds the actual company policy text relevant to that question (this is the RAG part — it searches your policy documents in Qdrant)

Risk-scoring agent — reads the policy text it found + the contract clause, and decides: is this HIGH / MEDIUM / LOW risk, and why

Human approval step — a person looks at the AI's HIGH/MEDIUM verdict and clicks approve or reject before anything is final

That's the entire system. No magic — a smart search + a careful reasoning step + a safety net.

Here is a clean, professional, and pragmatic description you can drop right into your GitHub README.md. It keeps the grounded "no magic" philosophy of your original text while formatting it perfectly for developers and visitors.

[Project Name]
A pragmatic, LLM-powered workflow that answers one crucial question: Does this contract violate our company's policies?

This project automates the tedious first pass of contract review. Instead of a human manually reading every new contract and cross-referencing it against a dense policy handbook, this system does the heavy lifting—while keeping a human in the loop for the final call.

No runaway agents, no overly complex graphs. Just smart search, careful reasoning, and a reliable safety net.

⚙️ How It Works
The system is broken down into a simple, sequential 4-step pipeline:

Intake Agent: Reads the incoming contract, identifies the document type, and formulates the specific compliance questions that need to be asked (e.g., "Does this NDA's data retention clause conflict with our GDPR policy?").

Retrieval Agent (RAG): Takes the formulated question and searches a Qdrant vector database to find the exact, relevant text from your company's internal policy documents.

Risk-Scoring Agent: Compares the contract clause against the retrieved policy text. It decides if the risk is HIGH, MEDIUM, or LOW and writes out a clear justification for its verdict.

Human Approval: The ultimate safety net. A human reviewer looks at the AI's verdict and reasoning, then clicks Approve or Reject before any final action is taken.

🛠️ Key Technologies
LLM Integration: For reasoning, question formulation, and risk scoring.

Qdrant: Vector database used by the Retrieval Agent to store and semantically search company policies.

Human-in-the-Loop (HITL): UI/Workflow step ensuring zero automated actions without human sign-off.

💡 Design Philosophy
This project is built on the idea that AI is best used as a tireless assistant, not a fully autonomous decision-maker. By breaking the problem down into strict, observable steps (Intake → Retrieve → Score → Approve), the system remains highly accurate, easy to debug, and inherently safe for enterprise use.

case_001: EvalCase = {

    "id": "001_clear_violation",

    "contract_clause": "Vendor shall retain all customer data indefinitely for analytics purposes, unless otherwise requested in writing by the customer.",

    "question": "Does this vendor's data retention clause comply with our 90-day deletion policy?",

    "relevant_policy_chunks": ["Company Data Retention Policy, Clause 4.2: All customer personal data must be deleted or anonymized within 90 days of contract termination, per GDPR Article 17."],

    "expected_risk_level": "HIGH",

    "expected_reasoning_contains": ["90 days", "indefinite", "conflict"],

}



case_004: EvalCase = {

    "id": "004_irrelevant_trap",

    "contract_clause": "Vendor shall provide 24/7 customer support via phone and email.",

    "question": "Does this support clause relate to our data retention policy?",

    "relevant_policy_chunks": [],  # nothing SHOULD be relevant here

    "expected_risk_level": "LOW",

    "expected_reasoning_contains": ["not related", "no conflict"],

}



# Your job for the rest of today: write 28-48 more of these by hand,

# covering: 10 clear violations, 10 clear compliant cases, 10 ambiguous

# cases, and 10-15 trap cases (irrelevant clauses, missing info, etc.)



Give me more examples like this in python and the samples should include no violation, ambigious and ones which ai shouldn't know anything about(irrelevent) to see if ai halucinates or not

Python
from typing import TypedDict, List, Literal

class EvalCase(TypedDict):
    id: str
    contract_clause: str
    question: str
    relevant_policy_chunks: List[str]
    expected_risk_level: Literal["HIGH", "MEDIUM", "LOW"]
    expected_reasoning_contains: List[str]

# =====================================================================
# SECTION 1: CLEAR VIOLATIONS (HIGH RISK)
# =====================================================================

case_005_violation_geo: EvalCase = {
    "id": "005_violation_geo",
    "contract_clause": "Vendor reserves the right to host, store, and process all customer data within data centers located in the United States and Singapore.",
    "question": "Does this hosting arrangement comply with our data sovereignty policy requiring EU-only storage?",
    "relevant_policy_chunks": [
        "Data Sovereignty Policy, Section 1.1: To comply with regulatory mandates, all primary and backup customer data must be hosted and processed exclusively within the European Union (EU)."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["United States", "Singapore", "EU-only", "conflict"],
}

case_006_violation_breach_notice: EvalCase = {
    "id": "006_violation_breach_notice",
    "contract_clause": "In the event of a security incident, Vendor shall notify Customer within seventy-two (72) hours of confirming a breach.",
    "question": "Does this notification window satisfy our security breach response requirements?",
    "relevant_policy_chunks": [
        "Information Security Policy, Article 9: Vendors handling sensitive systems must notify our Security Operations Center of any suspected or confirmed breach within 24 hours."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["72 hours", "24 hours", "exceeds", "violation"],
}

case_007_violation_liability: EvalCase = {
    "id": "007_violation_liability",
    "contract_clause": "Vendor's total aggregate liability for any data breaches, privacy violations, or confidentiality leaks shall be capped at $10,000.",
    "question": "Does this liability cap comply with our vendor risk management requirements for data breaches?",
    "relevant_policy_chunks": [
        "Vendor Management Policy, Section 5.4: Any contract involving access to personally identifiable information (PII) must have uncapped liability for data breaches and confidentiality failures."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["capped at $10,000", "uncapped liability", "conflict"],
}

case_008_violation_audit: EvalCase = {
    "id": "008_violation_audit",
    "contract_clause": "Customer may audit Vendor's security practices no more than once every five (5) years, with at least 90 days prior written notice.",
    "question": "Does this audit frequency comply with our annual compliance review policy?",
    "relevant_policy_chunks": [
        "Compliance Framework, Section 3.2: We require the right to conduct an independent security audit of third-party vendors at least once annually."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["once every 5 years", "annually", "restricts audit", "conflict"],
}

case_009_violation_subcontractor: EvalCase = {
    "id": "009_violation_subcontractor",
    "contract_clause": "Vendor may freely subcontract any portion of the services to third parties at its sole discretion, without prior notice to Customer.",
    "question": "Does this subcontracting clause comply with our vendor vetting requirements?",
    "relevant_policy_chunks": [
        "Procurement Policy, Section 8.1: No vendor may delegate or subcontract operations handling customer data without prior written consent and vetting by our risk team."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["freely subcontract", "without prior notice", "prior written consent", "violation"],
}

case_010_violation_insurance: EvalCase = {
    "id": "010_violation_insurance",
    "contract_clause": "Vendor shall maintain a general commercial liability insurance policy with a limit of not less than $1,000,000 per occurrence.",
    "question": "Does this insurance coverage meet our requirements for tech vendors?",
    "relevant_policy_chunks": [
        "Risk & Insurance Policy, Clause 12.3: Technology vendors handling customer systems must maintain active Cyber Liability Insurance of at least $5,000,000."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["$1,000,000", "$5,000,000", "Cyber Liability", "insufficient"],
}

case_011_violation_ip: EvalCase = {
    "id": "011_violation_ip",
    "contract_clause": "Vendor shall retain all right, title, and interest in and to any software, deliverables, or custom scripts developed during the course of this engagement.",
    "question": "Does this intellectual property clause comply with our standard work-for-hire requirements?",
    "relevant_policy_chunks": [
        "Intellectual Property Policy, Section 2.1: All custom code, software, and deliverables developed specifically for our company by third-party contractors must be assigned exclusively to us as work-for-hire."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["Vendor shall retain", "work-for-hire", "assigned exclusively", "IP violation"],
}

case_012_violation_termination: EvalCase = {
    "id": "012_violation_termination",
    "contract_clause": "Either party may terminate this agreement for convenience only upon one hundred and twenty (120) days prior written notice.",
    "question": "Does this termination notice period comply with our corporate agility guidelines?",
    "relevant_policy_chunks": [
        "Legal Playbook, Clause 7.4: We do not accept termination for convenience notice periods exceeding sixty (60) days."
    ],
    "expected_risk_level": "HIGH",
    "expected_reasoning_contains": ["120 days", "exceeds", "sixty (60) days", "conflict"],
}


# =====================================================================
# SECTION 2: CLEAR COMPLIANT CASES (LOW RISK)
# =====================================================================

case_013_compliant_geo: EvalCase = {
    "id": "013_compliant_geo",
    "contract_clause": "Vendor covenants and agrees that all Customer personal data shall be hosted, processed, and stored strictly within AWS data centers located in Frankfurt, Germany.",
    "question": "Does this hosting arrangement comply with our data sovereignty policy requiring EU-only storage?",
    "relevant_policy_chunks": [
        "Data Sovereignty Policy, Section 1.1: To comply with regulatory mandates, all primary and backup customer data must be hosted and processed exclusively within the European Union (EU)."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["Germany", "EU", "compliant", "no conflict"],
}

case_014_compliant_breach_notice: EvalCase = {
    "id": "014_compliant_breach_notice",
    "contract_clause": "In the event of a security breach, Vendor will notify Customer's security contact via email within twelve (12) hours of discovery.",
    "question": "Does this notification window satisfy our security breach response requirements?",
    "relevant_policy_chunks": [
        "Information Security Policy, Article 9: Vendors handling sensitive systems must notify our Security Operations Center of any suspected or confirmed breach within 24 hours."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["12 hours", "within 24 hours", "compliant", "fully satisfies"],
}

case_015_compliant_liability: EvalCase = {
    "id": "015_compliant_liability",
    "contract_clause": "Notwithstanding anything to the contrary, Vendor's liability for breaches of confidentiality, data protection, or security obligations shall not be subject to any liability caps.",
    "question": "Does this liability cap comply with our vendor risk management requirements for data breaches?",
    "relevant_policy_chunks": [
        "Vendor Management Policy, Section 5.4: Any contract involving access to personally identifiable information (PII) must have uncapped liability for data breaches and confidentiality failures."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not subject to any liability caps", "uncapped", "compliant"],
}

case_016_compliant_audit: EvalCase = {
    "id": "016_compliant_audit",
    "contract_clause": "Customer, or its designated independent auditor, shall have the right to inspect and audit Vendor's facilities and security controls once per calendar year.",
    "question": "Does this audit frequency comply with our annual compliance review policy?",
    "relevant_policy_chunks": [
        "Compliance Framework, Section 3.2: We require the right to conduct an independent security audit of third-party vendors at least once annually."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["once per calendar year", "at least once annually", "compliant"],
}

case_017_compliant_subcontractor: EvalCase = {
    "id": "017_compliant_subcontractor",
    "contract_clause": "Vendor shall not subcontract, delegate, or assign any of its obligations under this Agreement to any third party without obtaining prior written consent from Customer.",
    "question": "Does this subcontracting clause comply with our vendor vetting requirements?",
    "relevant_policy_chunks": [
        "Procurement Policy, Section 8.1: No vendor may delegate or subcontract operations handling customer data without prior written consent and vetting by our risk team."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["prior written consent", "compliant"],
}

case_018_compliant_insurance: EvalCase = {
    "id": "018_compliant_insurance",
    "contract_clause": "Vendor shall maintain Cyber and Technology Errors & Omissions liability insurance with a limit of $5,000,000 per claim and in the aggregate.",
    "question": "Does this insurance coverage meet our requirements for tech vendors?",
    "relevant_policy_chunks": [
        "Risk & Insurance Policy, Clause 12.3: Technology vendors handling customer systems must maintain active Cyber Liability Insurance of at least $5,000,000."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["$5,000,000", "Cyber and Technology Errors & Omissions", "compliant"],
}

case_019_compliant_ip: EvalCase = {
    "id": "019_compliant_ip",
    "contract_clause": "All deliverables and custom intellectual property created under this SOW are work-for-hire and will automatically become the sole and exclusive property of Customer upon creation.",
    "question": "Does this intellectual property clause comply with our standard work-for-hire requirements?",
    "relevant_policy_chunks": [
        "Intellectual Property Policy, Section 2.1: All custom code, software, and deliverables developed specifically for our company by third-party contractors must be assigned exclusively to us as work-for-hire."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["work-for-hire", "exclusive property", "compliant"],
}

case_020_compliant_termination: EvalCase = {
    "id": "020_compliant_termination",
    "contract_clause": "Customer may terminate this Agreement for convenience at any time upon giving forty-five (45) days written notice to Vendor.",
    "question": "Does this termination notice period comply with our corporate agility guidelines?",
    "relevant_policy_chunks": [
        "Legal Playbook, Clause 7.4: We do not accept termination for convenience notice periods exceeding sixty (60) days."
    ],
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["45 days", "under sixty (60) days", "compliant"],
}


# =====================================================================
# SECTION 3: AMBIGUOUS CASES (MEDIUM RISK)
# =====================================================================

case_021_ambiguous_geo: EvalCase = {
    "id": "021_ambiguous_geo",
    "contract_clause": "Vendor reserves the right to migrate data assets dynamically to any major Western region, utilizing regional AWS instances.",
    "question": "Does this hosting arrangement comply with our data sovereignty policy requiring EU-only storage?",
    "relevant_policy_chunks": [
        "Data Sovereignty Policy, Section 1.1: To comply with regulatory mandates, all primary and backup customer data must be hosted and processed exclusively within the European Union (EU)."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["Western region", "does not guarantee", "EU", "ambiguous"],
}

case_022_ambiguous_breach_notice: EvalCase = {
    "id": "022_ambiguous_breach_notice",
    "contract_clause": "Vendor will make reasonable efforts to notify Customer of security incidents as soon as practically possible during regular corporate business hours.",
    "question": "Does this notification window satisfy our security breach response requirements?",
    "relevant_policy_chunks": [
        "Information Security Policy, Article 9: Vendors handling sensitive systems must notify our Security Operations Center of any suspected or confirmed breach within 24 hours."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["reasonable efforts", "business hours", "no firm timeframe", "ambiguous"],
}

case_023_ambiguous_liability: EvalCase = {
    "id": "023_ambiguous_liability",
    "contract_clause": "Vendor's liability for security breaches is limited to direct damages up to $1,000,000, unless the breach is determined to have been caused by gross negligence or willful misconduct.",
    "question": "Does this liability cap comply with our vendor risk management requirements for data breaches?",
    "relevant_policy_chunks": [
        "Vendor Management Policy, Section 5.4: Any contract involving access to personally identifiable information (PII) must have uncapped liability for data breaches and confidentiality failures."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["limited to direct damages", "gross negligence", "partially capped", "ambiguous"],
}

case_024_ambiguous_audit: EvalCase = {
    "id": "024_ambiguous_audit",
    "contract_clause": "Customer has the right to perform compliance audits, provided that Customer reimburses Vendor for all reasonable engineering hours and administrative support required to facilitate the audit.",
    "question": "Does this audit frequency comply with our annual compliance review policy?",
    "relevant_policy_chunks": [
        "Compliance Framework, Section 3.2: We require the right to conduct an independent security audit of third-party vendors at least once annually."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["reimburses Vendor", "financial barrier", "right to audit exists", "ambiguous"],
}

case_025_ambiguous_subcontractor: EvalCase = {
    "id": "025_ambiguous_subcontractor",
    "contract_clause": "Vendor may utilize pre-approved corporate affiliates and partners listed in Appendix B to deliver services without requiring separate written permission.",
    "question": "Does this subcontracting clause comply with our vendor vetting requirements?",
    "relevant_policy_chunks": [
        "Procurement Policy, Section 8.1: No vendor may delegate or subcontract operations handling customer data without prior written consent and vetting by our risk team."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["pre-approved corporate affiliates", "Appendix B", "unvetted third parties", "ambiguous"],
}

case_026_ambiguous_insurance: EvalCase = {
    "id": "026_ambiguous_insurance",
    "contract_clause": "Vendor shall carry insurance protection that meets or exceeds standard risk profiles for mid-sized software-as-a-service providers.",
    "question": "Does this insurance coverage meet our requirements for tech vendors?",
    "relevant_policy_chunks": [
        "Risk & Insurance Policy, Clause 12.3: Technology vendors handling customer systems must maintain active Cyber Liability Insurance of at least $5,000,000."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["no specific dollar amount", "industry standards", "unspecified", "ambiguous"],
}

case_027_ambiguous_ip: EvalCase = {
    "id": "027_ambiguous_ip",
    "contract_clause": "Customer is granted an exclusive, fully paid-up, perpetual, worldwide license to exploit all custom deliverables produced during the project.",
    "question": "Does this intellectual property clause comply with our standard work-for-hire requirements?",
    "relevant_policy_chunks": [
        "Intellectual Property Policy, Section 2.1: All custom code, software, and deliverables developed specifically for our company by third-party contractors must be assigned exclusively to us as work-for-hire."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["exclusive perpetual license", "not ownership transfer", "not work-for-hire", "ambiguous"],
}

case_028_ambiguous_termination: EvalCase = {
    "id": "028_ambiguous_termination",
    "contract_clause": "Customer can terminate this agreement with 30 days notice, but must pay a dynamic project wind-down fee as outlined in current milestone forecasts.",
    "question": "Does this termination notice period comply with our corporate agility guidelines?",
    "relevant_policy_chunks": [
        "Legal Playbook, Clause 7.4: We do not accept termination for convenience notice periods exceeding sixty (60) days."
    ],
    "expected_risk_level": "MEDIUM",
    "expected_reasoning_contains": ["30 days", "wind-down fee", "penalty", "ambiguous"],
}


# =====================================================================
# SECTION 4: IRRELEVANT / TRAP CASES (LOW RISK - EXPECT NO HALLUCINATIONS)
# =====================================================================

case_029_trap_marketing: EvalCase = {
    "id": "029_trap_marketing",
    "contract_clause": "Customer grants Vendor a non-exclusive license to use Customer's trademark logo in promotional presentations and client case studies.",
    "question": "Does this logo-use clause comply with our 90-day data deletion policy?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "trademark", "data deletion"],
}

case_030_trap_support_hours: EvalCase = {
    "id": "030_trap_support_hours",
    "contract_clause": "Customer support shall be available via email Monday through Friday, 9:00 AM to 5:00 PM EST, excluding US Federal holidays.",
    "question": "Does this customer support availability clause violate our data encryption policy?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "support hours", "data encryption"],
}

case_031_trap_pricing: EvalCase = {
    "id": "031_trap_pricing",
    "contract_clause": "All subscription rates are subject to a maximum automatic annual escalation of 3% per year, starting on the first anniversary of the effective date.",
    "question": "Does this annual escalation pricing structure violate our background check policies?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "pricing", "background check"],
}

case_032_trap_governing_law: EvalCase = {
    "id": "032_trap_governing_law",
    "contract_clause": "This Agreement and any dispute arising out of it shall be governed exclusively by the internal laws of the State of Delaware, without regard to conflict of laws principles.",
    "question": "Does this Delaware choice of law provision conflict with our clean desk physical security policy?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "governing law", "clean desk"],
}

case_033_trap_training: EvalCase = {
    "id": "033_trap_training",
    "contract_clause": "Vendor will provide up to 5 hours of remote onboarding instruction and user documentation to assist with the system roll-out.",
    "question": "Does this user training onboarding clause violate our disaster recovery failover policy?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "training", "disaster recovery"],
}

case_034_trap_force_majeure: EvalCase = {
    "id": "034_trap_force_majeure",
    "contract_clause": "Neither party shall be liable for failures to perform due to acts of God, strikes, pandemics, or government lockdown mandates.",
    "question": "Does this force majeure definition violate our subcontractor background screening policy?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "force majeure", "background screening"],
}

case_035_trap_branding: EvalCase = {
    "id": "035_trap_branding",
    "contract_clause": "Vendor shall construct all co-branded marketing assets utilizing standard hex color codes provided in the official corporate style guide.",
    "question": "Does this color palette configuration conflict with our database encryption guidelines?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "branding", "database encryption"],
}

case_036_trap_travel: EvalCase = {
    "id": "036_trap_travel",
    "contract_clause": "Customer will reimburse Vendor's pre-authorized economy class travel and reasonable lodging expenses within 30 days of invoice presentation.",
    "question": "Does this expense reimbursement clause violate our strict multi-factor authentication policy?",
    "relevant_policy_chunks": [],  # Nothing relevant
    "expected_risk_level": "LOW",
    "expected_reasoning_contains": ["not related", "no conflict", "travel expenses", "multi-factor authentication"],
}
write this readme.md in markdown format,



# "ClauseGuard": MCP-Native Compliance Review Agent Team

A pragmatic, LLM-powered workflow that answers one crucial question: Does this contract violate our company's policies?



This project automates the tedious first pass of contract review. Instead of a human manually reading every new contract and cross-referencing it against a dense policy handbook, this system does the heavy lifting—while keeping a human in the loop for the final call.



No runaway agents, no overly complex graphs. Just smart search, careful reasoning, and a reliable safety net.



⚙️ How It Works

The system is broken down into a simple, sequential 4-step pipeline:



Intake Agent: Reads the incoming contract, identifies the document type, and formulates the specific compliance questions that need to be asked (e.g., "Does this NDA's data retention clause conflict with our GDPR policy?").



Retrieval Agent (RAG): Takes the formulated question and searches a Qdrant vector database to find the exact, relevant text from your company's internal policy documents.



Risk-Scoring Agent: Compares the contract clause against the retrieved policy text. It decides if the risk is HIGH, MEDIUM, or LOW and writes out a clear justification for its verdict.



Human Approval: The ultimate safety net. A human reviewer looks at the AI's verdict and reasoning, then clicks Approve or Reject before any final action is taken.



🛠️ Key Technologies

LLM Integration: For reasoning, question formulation, and risk scoring.



Qdrant: Vector database used by the Retrieval Agent to store and semantically search company policies.



Human-in-the-Loop (HITL): UI/Workflow step ensuring zero automated actions without human sign-off.



💡 Design Philosophy

This project is built on the idea that AI is best used as a tireless assistant, not a fully autonomous decision-maker. By breaking the problem down into strict, observable steps (Intake → Retrieve → Score → Approve), the system remains highly accurate, easy to debug, and inherently safe for enterprise use.

Markdown
# ClauseGuard: MCP-Native Compliance Review Agent Team

A pragmatic, LLM-powered workflow that answers one crucial question: **Does this contract violate our company's policies?**

This project automates the tedious first pass of contract review. Instead of a human manually reading every new contract and cross-referencing it against a dense policy handbook, this system does the heavy lifting—while keeping a human in the loop for the final call.

No runaway agents, no overly complex graphs. Just smart search, careful reasoning, and a reliable safety net.

## ⚙️ How It Works

The system is broken down into a simple, sequential 4-step pipeline:

1. **Intake Agent:** Reads the incoming contract, identifies the document type, and formulates the specific compliance questions that need to be asked (e.g., *"Does this NDA's data retention clause conflict with our GDPR policy?"*).
2. **Retrieval Agent (RAG):** Takes the formulated question and searches a Qdrant vector database to find the exact, relevant text from your company's internal policy documents.
3. **Risk-Scoring Agent:** Compares the contract clause against the retrieved policy text. It decides if the risk is **HIGH**, **MEDIUM**, or **LOW** and writes out a clear justification for its verdict.
4. **Human Approval:** The ultimate safety net. A human reviewer looks at the AI's verdict and reasoning, then clicks *Approve* or *Reject* before any final action is taken.

## 🛠️ Key Technologies

* **LLM Integration:** For reasoning, question formulation, and risk scoring.
* **Qdrant:** Vector database used by the Retrieval Agent to store and semantically search company policies.
* **Human-in-the-Loop (HITL):** UI/Workflow step ensuring zero automated actions without human sign-off.

## 💡 Design Philosophy

This project is built on the idea that AI is best used as a tireless assistant, not a fully autonomous decision-maker. By breaking the problem down into strict, observable steps (Intake → Retrieve → Score → Approve), the system remains highly accurate, easy to debug, and inherently safe for enterprise use.
this is the project architecture so write it in a way that i should post it as architecture file to github,



4 agents: Intake (reads doc, picks question) → Retrieval (searches policy corpus) → Risk Scoring (HIGH/MED/LOW + why) → Human Approval (pauses for a person to click yes/no). State passes between them as one shared object.



The 4 agents and what each does:



Intake/Classifier agent — reads document, decides document type and routing

Retrieval agent — RAG query against your Qdrant policy corpus, returns top-k chunks

Risk-Scoring agent — reasons over retrieved chunks, produces structured output: {risk_level: HIGH/MEDIUM/LOW, justification: "...", cited_clauses: [...]}

Human-in-the-loop approval node — graph pauses, sends a notification (even just a print statement for now, Slack/email later), resumes when you call graph.invoke(Command(resume=True), config).







State schema (Python TypedDict with all fields the graph passes between nodes)

MCP server: which 2–3 tools you'll expose (retrieve_policy_context, score_risk, get_pending_approvals)

Eval plan: 30 labeled test cases, which Ragas metrics, target thresholds

Deployment: Docker → GitHub Actions → Azure Container Apps (same pipeline as your existing project)

ClauseGuard: Architecture & Technical Design
This document details the system architecture, state management, tool definitions, evaluation framework, and deployment pipeline for ClauseGuard.

1. System Topology & Agent Pipeline
ClauseGuard is designed as a deterministic, stateful pipeline (orchestrated via a state graph) rather than an unconstrained autonomous agent loop. This ensures predictable execution, auditability, and clear boundaries for human-in-the-loop intervention.

                  [ Raw Contract Input ]
                            │
                            ▼
                  ┌───────────────────┐
                  │ 1. Intake Agent   │ ── Classifier & Router
                  └───────────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ 2. Retrieval Agent│ ── Qdrant Vector Search (RAG)
                  └───────────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ 3. Risk-Scoring   │ ── LLM Analyzer & Structurer
                  └───────────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ 4. Human Approval │ ── Interrupt State (Awaiting Resume)
                  └───────────────────┘
                            │
                            ▼
                [ Final Approved Verdict ]
The 4 Pipeline Nodes
Intake / Classifier Agent: Parses the raw contract text, determines the document category (e.g., NDA, SLA, SaaS MSA), and formulates targeted compliance questions.

Retrieval Agent: Conducts semantic vector searches using Qdrant against your internal policy corpus to retrieve the top-k relevant policy chunks for each formulated question.

Risk-Scoring Agent: Compares the contract clauses directly with the retrieved policy chunks. It evaluates the alignment and produces a structured risk profile: HIGH, MEDIUM, or LOW, accompanied by clean citations and reasoning.

Human-in-the-loop (HITL) Approval Node: Pauses graph execution using a state-saving interrupt. It generates a notification event (console print, Slack webhook, or email) and yields control back to the orchestrator. Execution only resumes once an external approval action updates the state.

2. State Schema
A single, shared state object passes between all nodes. This state tracks the progression of the review, ensures reproducibility, and simplifies debugging.

Python
from typing import TypedDict, List, Literal, Optional

class ContractReviewState(TypedDict):
    # Inputs
    raw_contract_text: str
    
    # Intake / Classification Outputs
    document_type: str                         # e.g., "NDA", "SaaS_MSA", "SLA"
    compliance_questions: List[str]            # Targeted questions formulated by Intake
    
    # Retrieval Outputs
    retrieved_policy_chunks: List[str]         # Context passages fetched from Qdrant
    
    # Risk-Scoring Outputs
    risk_level: Optional[Literal["HIGH", "MEDIUM", "LOW"]]
    justification: Optional[str]               # Detailed explanation of the risk assessment
    cited_clauses: List[str]                   # Specific lines from contract causing the risk
    
    # Human-in-the-loop Tracking
    approval_status: Optional[Literal["APPROVED", "REJECTED"]]
    reviewer_notes: Optional[str]              # Comments provided by the human operator
3. MCP Server & Tool Definitions
The codebase exposes its core capabilities through a Model Context Protocol (MCP) server, allowing external LLM clients (like Claude Desktop) to invoke the compliance pipeline directly.

Exposed Tools
1. retrieve_policy_context
Description: Searches the Qdrant policy corpus for internal policy rules matching a query.

Arguments:

query (string): The search query formulated from the contract clause.

limit (integer, optional): Max chunks to return (default: 3).

Returns: List of text fragments matching the semantic search.

2. score_risk
Description: Performs a structured risk comparison between a contract clause and relevant policy guidelines.

Arguments:

contract_clause (string): The specific text from the contract.

policy_context (array of strings): Relevant internal policy requirements.

Returns: JSON object matching the schema: { "risk_level": "HIGH" | "MEDIUM" | "LOW", "justification": string, "cited_clauses": string[] }.

3. get_pending_approvals
Description: Fetches contracts currently paused at the human approval node.

Arguments: None.

Returns: List of active runs requiring human input, including their current state values.

4. Human-in-the-Loop Implementation
To prevent unauthorized actions, the graph pauses immediately after the Risk-Scoring agent writes its verdict. We manage this using state machine interrupt patterns.

Pausing and Resuming the Graph
When execution reaches the human approval step, the graph execution is suspended. Resuming the flow requires sending a resume command along with any reviewer notes and status updates.

Python
# 1. Start pipeline execution
# The graph runs until it reaches the Human Approval node and pauses.
thread_config = {"configurable": {"thread_id": "contract_abc_123"}}
graph.invoke({"raw_contract_text": contract_payload}, thread_config)

# 2. Extract state to display to the human reviewer
current_state = graph.get_state(thread_config)
print(f"Risk Rating: {current_state.values['risk_level']}")
print(f"Justification: {current_state.values['justification']}")

# 3. Resume the graph once a human clicks 'Approve' or 'Reject'
graph.invoke(
    Command(
        resume={
            "approval_status": "APPROVED",
            "reviewer_notes": "Exception approved for this vendor due to strict backup protocols."
        }
    ),
    config=thread_config
)
5. Evaluation Plan
To ensure the safety, reliability, and accuracy of the pipeline, ClauseGuard runs against a rigorous test suite of 30-48 handcrafted evaluation cases.

Test Suite Distribution
10 Clear Violations (HIGH Risk): Blatant conflicts (e.g., indefinite data retention, insufficient insurance caps).

10 Compliant Cases (LOW Risk): Clauses that cleanly satisfy or exceed requirements.

10 Ambiguous Cases (MEDIUM Risk): Soft conflicts, undefined windows, or partial matches requiring careful legal review.

10-18 Trap Cases (LOW Risk): Irrelevant clauses (marketing, pricing, color schemes) matched with unrelated policies to test for hallucinations.

Evaluation Metrics (via Ragas)
We run evaluations against the pipeline using Ragas to measure Retrieval and Generation accuracy:

Metric	Target Threshold	Description
Faithfulness	≥0.90	Ensures the risk justification only references facts present in the policy or contract (no hallucinations).
Context Precision	≥0.85	Verifies that the Retrieval agent places relevant policy chunks at the top of the search results.
Aspect Critic (Strictness)	≥0.95	Measures whether the LLM correctly categorizes HIGH-risk violations without false negatives.
6. Deployment Pipeline
ClauseGuard uses a lightweight, continuous delivery pipeline matching standard enterprise cloud architectures.

 [ Local Dev ] ──> [ GitHub Repo ] ──> [ GitHub Actions ] ──> [ Azure Container Registry ] ──> [ Azure Container Apps ]
Packaging: Dockerized container built using a secure multi-stage build.

Orchestration / CI: GitHub Actions trigger on merges to the main branch, run the test suite, and run the Ragas evaluation step.

Registry: Upon successful tests, the runner pushes the container image to Azure Container Registry (ACR).

Hosting: Deployments run on Azure Container Apps (ACA) as a secure, serverless container hosting environment, natively exposing the MCP server endpoint for consumer apps.

you added stuff don't do that it needs to be accurate and create an architecture file which i should donwload

Save the code block below as ARCHITECTURE.md to add it directly to your GitHub repository.

Markdown
# ClauseGuard: Architecture and Technical Design

This document describes the system architecture, state tracking, tool definitions, evaluation strategy, and deployment pipeline for ClauseGuard.

---

## 1. System Architecture

ClauseGuard uses a sequential 4-step pipeline where state passes between nodes as a single, shared object.

[ Raw Contract ]
│
▼
┌──────────────────────────┐
│ 1. Intake/Classifier     │ ── Reads document, decides type and routing
└──────────────────────────┘
│
▼
┌──────────────────────────┐
│ 2. Retrieval             │ ── RAG query against Qdrant policy corpus
└──────────────────────────┘
│
▼
┌──────────────────────────┐
│ 3. Risk-Scoring          │ ── Evaluates context, outputs risk level & reasons
└──────────────────────────┘
│
▼
┌──────────────────────────┐
│ 4. Human Approval        │ ── Pauses execution for human manual review
└──────────────────────────┘
│
▼
[ Final Approved Contract ]


### The 4 Agents

1. **Intake/Classifier Agent:** Reads the incoming contract document, decides the document type (e.g., NDA, MSA), and determines routing.
2. **Retrieval Agent:** Runs a Retrieval-Augmented Generation (RAG) query against your Qdrant policy corpus to fetch the top-k relevant policy chunks.
3. **Risk-Scoring Agent:** Reasons over the retrieved policy chunks and the contract clause to produce a structured JSON output:
   ```json
   {
     "risk_level": "HIGH/MEDIUM/LOW",
     "justification": "Detailed explanation...",
     "cited_clauses": ["Specific text from the contract..."]
   }
Human-in-the-loop Approval Node: The graph pauses execution and sends a notification (a print statement for now; Slack or email integration later). It resumes only when you call:

Python
graph.invoke(Command(resume=True), config)
2. State Schema
The entire pipeline updates and reads from a single shared Python TypedDict object:

Python
from typing import TypedDict, List, Literal, Optional

class ContractState(TypedDict):
    contract_text: str
    document_type: str
    compliance_questions: List[str]
    retrieved_policy_chunks: List[str]
    risk_level: Optional[Literal["HIGH", "MEDIUM", "LOW"]]
    justification: Optional[str]
    cited_clauses: List[str]
    approved: Optional[bool]
3. MCP Server Tools
The system exposes its core capabilities as Model Context Protocol (MCP) tools for external LLM clients:

retrieve_policy_context: Searches the Qdrant policy vector store using the generated compliance question and returns the top relevant text chunks.

score_risk: Takes a contract clause and relevant policy text, analyzes the conflict, and returns the structured risk level and justification.

get_pending_approvals: Lists the current pipeline runs that are paused at the human-in-the-loop step awaiting user confirmation.

4. Evaluation Plan
To maintain high accuracy and protect against hallucinations, we evaluate the pipeline using a structured test suite.

30 Labeled Test Cases:

10 clear violations (High risk cases)

10 clear compliant cases (Low risk cases)

10 ambiguous cases (Medium risk cases requiring human nuance)

10-15 trap cases (Irrelevant clauses or missing information to test hallucination resistance)

Ragas Metrics & Target Thresholds:

Faithfulness (Target: > 0.85) - Ensures the risk justification only uses facts from the policy document.

Context Recall (Target: > 0.90) - Confirms the retrieval step fetches the exact policy chunk needed to answer the compliance question.

Answer Relevance (Target: > 0.85) - Ensures the generated risk justifications directly address the compliance question asked.

5. Deployment
The system is deployed using a continuous integration and deployment pipeline:

Docker: Packages the application, the MCP server, and its dependencies into a single lightweight container image.

GitHub Actions: Automatically runs the test suite and Ragas evaluations on every pull request or merge to main.

Azure Container Apps (ACA): Hosts the containerized application and exposes the MCP server endpoint securely.

generate a file

[ Raw Contract ]
│
▼
┌──────────────────────────┐
│ 1. Intake/Classifier     │ ── Reads document, decides type and routing
└──────────────────────────┘
│
▼
┌──────────────────────────┐
│ 2. Retrieval             │ ── RAG query against Qdrant policy corpus
└──────────────────────────┘
│
▼
┌──────────────────────────┐
│ 3. Risk-Scoring          │ ── Evaluates context, outputs risk level & reasons
└──────────────────────────┘
│
▼
┌──────────────────────────┐
│ 4. Human Approval        │ ── Pauses execution for human manual review
└──────────────────────────┘
│
▼
[ Final Approved Contract ]


### The 4 Agents

1. **Intake/Classifier Agent:** Reads the incoming contract document, decides the document type (e.g., NDA, MSA), and determines routing.
2. **Retrieval Agent:** Runs a Retrieval-Augmented Generation (RAG) query against your Qdrant policy corpus to fetch the top-k relevant policy chunks.
3. **Risk-Scoring Agent:** Reasons over the retrieved policy chunks and the contract clause to produce a structured JSON output:
   ```json
   {
     "risk_level": "HIGH/MEDIUM/LOW",
     "justification": "Detailed explanation...",
     "cited_clauses": ["Specific text from the contract..."]
   }
Human-in-the-loop Approval Node: The graph pauses execution and sends a notification (a print statement for now; Slack or email integration later). It resumes only when you call:

Python
graph.invoke(Command(resume=True), config)
2. State Schema
The entire pipeline updates and reads from a single shared Python TypedDict object:

Python
from typing import TypedDict, List, Literal, Optional

class ContractState(TypedDict):
    contract_text: str
    document_type: str
    compliance_questions: List[str]
    retrieved_policy_chunks: List[str]
    risk_level: Optional[Literal["HIGH", "MEDIUM", "LOW"]]
    justification: Optional[str]
    cited_clauses: List[str]
    approved: Optional[bool]
3. MCP Server Tools
The system exposes its core capabilities as Model Context Protocol (MCP) tools for external LLM clients:

retrieve_policy_context: Searches the Qdrant policy vector store using the generated compliance question and returns the top relevant text chunks.

score_risk: Takes a contract clause and relevant policy text, analyzes the conflict, and returns the structured risk level and justification.

get_pending_approvals: Lists the current pipeline runs that are paused at the human-in-the-loop step awaiting user confirmation.

4. Evaluation Plan
To maintain high accuracy and protect against hallucinations, we evaluate the pipeline using a structured test suite.

30 Labeled Test Cases:

10 clear violations (High risk cases)

10 clear compliant cases (Low risk cases)

10 ambiguous cases (Medium risk cases requiring human nuance)

10-15 trap cases (Irrelevant clauses or missing information to test hallucination resistance)

Ragas Metrics & Target Thresholds:

Faithfulness (Target: > 0.85) - Ensures the risk justification only uses facts from the policy document.

Context Recall (Target: > 0.90) - Confirms the retrieval step fetches the exact policy chunk needed to answer the compliance question.

Answer Relevance (Target: > 0.85) - Ensures the generated risk justifications directly address the compliance question asked.

5. Deployment
The system is deployed using a continuous integration and deployment pipeline:

Docker: Packages the application, the MCP server, and its dependencies into a single lightweight container image.

GitHub Actions: Automatically runs the test suite and Ragas evaluations on every pull request or merge to main.

Azure Container Apps (ACA): Hosts the containerized application and exposes the MCP server endpoint securely.
"""

with open("ARCHITECTURE.md", "w", encoding="utf-8") as f:
f.write(markdown_content)

print("File ARCHITECTURE.md successfully created.")


```text?code_stdout&code_event_index=1
File ARCHITECTURE.md successfully created.

Your Markdown file is ready
MD icon
ARCHITECTURE
 MD 
Open

I have generated the ARCHITECTURE.md file exactly matching the specifications and routing architecture you approved. You can now download it and add it directly to your GitHub repository.




Your National University of Modern Languages chats aren’t used to improve our models. Gemini is AI and can make mistakes. Your privacy & GeminiOpens in a new window

# ClauseGuard: Architecture and Technical Design

This document describes the system architecture, state tracking, tool definitions, evaluation strategy, and deployment pipeline for ClauseGuard.

---

## 1. System Architecture

ClauseGuard uses a sequential 4-step pipeline where state passes between nodes as a single, shared object.

```
[ Raw Contract ] 
       │
       ▼
┌──────────────────────────┐
│ 1. Intake/Classifier     │ ── Reads document, decides type and routing
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 2. Retrieval             │ ── RAG query against Qdrant policy corpus
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 3. Risk-Scoring          │ ── Evaluates context, outputs risk level & reasons
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 4. Human Approval        │ ── Pauses execution for human manual review
└──────────────────────────┘
       │
       ▼
[ Final Approved Contract ]
```

### The 4 Agents

1. **Intake/Classifier Agent:** Reads the incoming contract document, decides the document type (e.g., NDA, MSA), and determines routing.
2. **Retrieval Agent:** Runs a Retrieval-Augmented Generation (RAG) query against your Qdrant policy corpus to fetch the top-k relevant policy chunks.
3. **Risk-Scoring Agent:** Reasons over the retrieved policy chunks and the contract clause to produce a structured JSON output:
   ```json
   {
     "risk_level": "HIGH/MEDIUM/LOW",
     "justification": "Detailed explanation...",
     "cited_clauses": ["Specific text from the contract..."]
   }
   ```
4. **Human-in-the-loop Approval Node:** The graph pauses execution and sends a notification (a print statement for now; Slack or email integration later). It resumes only when you call:
   ```python
   graph.invoke(Command(resume=True), config)
   ```

---

## 2. State Schema

The entire pipeline updates and reads from a single shared Python `TypedDict` object:

```python
from typing import TypedDict, List, Literal, Optional

class ContractState(TypedDict):
    contract_text: str
    document_type: str
    compliance_questions: List[str]
    retrieved_policy_chunks: List[str]
    risk_level: Optional[Literal["HIGH", "MEDIUM", "LOW"]]
    justification: Optional[str]
    cited_clauses: List[str]
    approved: Optional[bool]
```

---

## 3. MCP Server Tools

The system exposes its core capabilities as Model Context Protocol (MCP) tools for external LLM clients:

* **`retrieve_policy_context`**: Searches the Qdrant policy vector store using the generated compliance question and returns the top relevant text chunks.
* **`score_risk`**: Takes a contract clause and relevant policy text, analyzes the conflict, and returns the structured risk level and justification.
* **`get_pending_approvals`**: Lists the current pipeline runs that are paused at the human-in-the-loop step awaiting user confirmation.

---

## 4. Evaluation Plan

To maintain high accuracy and protect against hallucinations, we evaluate the pipeline using a structured test suite.

* **30 Labeled Test Cases:**
  * 10 clear violations (High risk cases)
  * 10 clear compliant cases (Low risk cases)
  * 10 ambiguous cases (Medium risk cases requiring human nuance)
  * 10-15 trap cases (Irrelevant clauses or missing information to test hallucination resistance)
* **Ragas Metrics & Target Thresholds:**
  * **Faithfulness** (Target: > 0.85) - Ensures the risk justification only uses facts from the policy document.
  * **Context Recall** (Target: > 0.90) - Confirms the retrieval step fetches the exact policy chunk needed to answer the compliance question.
  * **Answer Relevance** (Target: > 0.85) - Ensures the generated risk justifications directly address the compliance question asked.

---

## 5. Deployment

The system is deployed using a continuous integration and deployment pipeline:

1. **Docker:** Packages the application, the MCP server, and its dependencies into a single lightweight container image.
2. **GitHub Actions:** Automatically runs the test suite and Ragas evaluations on every pull request or merge to main.
3. **Azure Container Apps (ACA):** Hosts the containerized application and exposes the MCP server endpoint securely.
ARCHITECTURE.md
Displaying ARCHITECTURE.md.