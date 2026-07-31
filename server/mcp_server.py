import os
import json
import atexit
from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "qdrant_db")
REVIEWS_FILE = os.path.join(BASE_DIR, "pending_reviews.json")

COLLECTION_NAME = "company_policies"

#Initialize FastMCP server instance
mcp = FastMCP("ClauseGuard-MCP-Server")

#Initialize persistent Qdrant client and embedding model
qdrant_client = QdrantClient(path=DB_PATH)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def _cleanup_qdrant():
    try:
        qdrant_client.close()
    except Exception:
        pass

#This guarantees close() runs BEFORE Python unloads system modules like 'sys'
atexit.register(_cleanup_qdrant)


@mcp.tool()
def search_policy_docs(query_text: str, limit: int = 3) -> str:
    """Searches internal company compliance policies for text relevant to a query.

    Args:
        query_text: Compliance topic or question (e.g., 'data retention rules GDPR').
        limit: Number of top relevant policy passages to return (default: 3).

    Returns:
        Formatted string containing matched policy passages and their document sources.
    """

    query_vector = embedder.encode(query_text).tolist()


    try:
        results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit).points

    except Exception as e:
        return f"Error querying Qdrant database: {str(e)}"

    if not results:
        return "No relevant policy documents found matching the query."

    #Format search hits for LLM consumption
    formatted_passages = []
    for idx, hit in enumerate(results, start=1):
        source = hit.payload.get("source", "Unknown File")
        text = hit.payload.get("text", "")
        formatted_passages.append(
            f"--- [Policy Result {idx}] (Source: {source} | Similarity Score: {hit.score:.2f}) ---\n{text}"
        )

    return "\n\n".join(formatted_passages)


@mcp.tool()
def log_for_human_review(
    contract_name: str,
    clause_text: str,
    risk_level: str,
    justification: str
) -> str:
    """Logs a evaluated contract clause to the pending review queue for human sign-off.

    Args:
        contract_name: Name or ID of the contract document.
        clause_text: Original text of the contract clause evaluated.
        risk_level: Risk classification ('HIGH', 'MEDIUM', 'LOW').
        justification: Reasoning behind the assigned risk level.

    Returns:
        Status message confirming the review record was created.
    """
    review_record = {
        "contract_name": contract_name,
        "clause_text": clause_text,
        "risk_level": risk_level.upper(),
        "justification": justification,
        "status": "PENDING"
    }

    reviews = []
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
                reviews = json.load(f)
        except json.JSONDecodeError:
            reviews = []

    reviews.append(review_record)

    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2)

    return f"Logged clause under '{risk_level.upper()}' risk level for human review."


if __name__ == "__main__":
    mcp.run()