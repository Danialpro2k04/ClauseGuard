# ClauseGuard Project Progress Log
 
- **built the data ingestion for our corpus files. The script /server/ingest_corpus.py takes all the policy files from the corpus folder and then embeds the chunks of size 500 with 50 chunk overlap for context.**
- **resolved the version mis match issue for the libraries by using another file contraints.txt along with requirements.txt to get the correct versions of libraries that align with eachother and works fine:**1. Diagnosed the real chain of failures. Your original error (NameError: name 'torch' is not defined) looked like a single crash, but it was actually three independent version conflicts stacked on top of each other, each masking the next:

transformers 5.14.1 hard-requires torch>=2.4 at runtime (confirmed by reading transformers' actual source, not just its metadata)
torch>=2.4 has no wheel at all for Intel Mac (macOS x86_64) — PyTorch dropped those builds after 2.2.2
Even with the right torch, numpy 2.4.6 broke torch 2.2.2's C-API bridge (torch predates NumPy 2.0 support), causing .numpy() calls to fail

2. Verified instead of guessing at every step. Rather than picking version numbers from memory or blog posts, I pulled real package metadata from PyPI, inspected transformers' actual source code to find the true runtime floor, and dry-run installed candidate version sets in a sandbox venv to confirm they resolved without conflicts before recommending anything.

3. Respected your constraint of not touching requirements.txt. Instead of editing your file, I added a separate constraints.txt that only caps ceilings (transformers<5.0.0, torch==2.2.2, numpy<2) on packages your file already pulls in transitively. This narrows versions without adding new top-level dependencies or changing anything else in your dependency graph — verified by dry-run against your exact file.

4. Fixed it in two passes as each layer surfaced: first transformers/torch, then numpy, once the first fix revealed the next problem underneath.

- **ingest_corpus.py worked perfectly fine**

- **built mcp_server.py file which has two functions as tools to be used by our agents. One tool searches the policy docs to find relevent chunks to the contract clause and second tools logs for human review.**

- **4 step pipeline Agents:**
[ Incoming Contract ] 
         │
         ▼
┌─────────────────┐
│ 1. Intake Agent │ ──► Extracts clauses & formulates compliance questions
└─────────────────┘
         │
         ▼
┌────────────────────┐
│ 2. Retrieval Agent │ ──► Calls MCP search_policy_docs tool
└────────────────────┘
         │
         ▼
┌──────────────────┐
│ 3. Risk Scorer   │ ──► Evaluates risk (HIGH/MED/LOW) & logs for HITL
└──────────────────┘

-**Built the intake agent: So the intake agent takes a contract string or document(currently i have a sample text to be processed) and gives it to an llm provided by groq to go through that and i dentify risk bearing clauses and create declarative statements for that then return json formatted response containing the document type with clauses(clause title, clause text and compliance statement)**

-**Built the retrieval agent: so in retrieval.py the retrieval agent takes the response from intake.py and takes the compliance statement from intake.py and returns matching chunks(number currently set to 2) from out pilicy documents stored in qdrant locally on a folder then returns the document type with clauses including the retrieved chunks to give to llm**

-**Built risk_scorer.py: So this script takes the string, runs the two agents, takes the response from the retrieval agent then evaluates the statement with policy clause and then gives it to llm and returns the risk level, justifications and recommendations. if the risk level is low nothing happens but when it is medium or high, it is flagged for human review and stored in pending_reviews.json file**

-**Created pipeline.py which orchestrates the whole process ie it takes the document which should be specified in the pipeline.py file and then parses it weather if it is pdf or .docx or txt gets the content and then runs the three agents and gives the final output.**

-**Created app.py a python streamlit web interface for Human In The Loop(HITL) to review the pending_reviews.json reviews for the flagged responses.**

