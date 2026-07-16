from typing import TypedDict, List, Literal

class EvalCase(TypedDict):
    """one row of the evaluation schema"""
    id:str
    contract_clause:str      #the input text being reviewed
    question:str             #what the intake agent should generate
    relevant_policy_chunks:List[str]  #the relevant policy chunks that should be used to answer the question
    expected_risk_level:Literal["HIGH", "MEDIUM", "LOW", "UNKNOWN"] 
    expected_resoning_contains : List[str]  #the expected reasoning that should be used to answer the question

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