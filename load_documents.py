import os
import glob
import uuid
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Make sure QDRANT_URL and QDRANT_API_KEY are set in your .env file.")

# 2. Setup the FREE embedding model (runs locally on your machine)
print("Loading free embedding model (this might take a few seconds the first time)...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
VECTOR_SIZE = 384 # This is the mathematical size this specific free model uses

def get_embedding(text):
    # This translates the text chunk into a list of numbers (a vector)
    return embedding_model.encode(text).tolist()

def main():
    # 3. Connect to your free Qdrant Cloud database
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    COLLECTION_NAME = "policy_documents"

    # 4. Create the "folder" (collection) in Qdrant if it doesn't exist yet
    if not client.collection_exists(COLLECTION_NAME):
        print(f"Creating collection: {COLLECTION_NAME}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )

    # 5. Setup the Chunking tool
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    documents = []
    
    # 6. Read every text file inside your "corpus" folder
    for filepath in glob.glob("corpus/*.txt"):
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Cut the document into smaller pieces (chunks)
        chunks = text_splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            documents.append({
                "text": chunk,
                "metadata": {
                    "source": filename,
                    "chunk_id": i
                }
            })

    print(f"Split raw files into {len(documents)} text chunks.")

    # 7. Convert the chunks to math and prepare them for uploading
    points = []
    for doc in documents:
        text_content = doc["text"]
        vector = get_embedding(text_content)
        point_id = str(uuid.uuid4())
        
        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": text_content,
                    "source": doc["metadata"]["source"],
                    "chunk_id": doc["metadata"]["chunk_id"]
                }
            )
        )

    # 8. Upload to Qdrant
    print("Uploading vectors to Qdrant Cloud...")
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print("Successfully uploaded everything to Qdrant!")

if __name__ == "__main__":
    main()