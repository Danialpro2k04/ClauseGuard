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