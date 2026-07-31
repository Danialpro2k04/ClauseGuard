import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Resolve paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_DIR = os.path.join(BASE_DIR, "corpus")
DB_PATH = os.path.join(BASE_DIR, "qdrant_db")

COLLECTION_NAME = "company_policies"


def ingest_corpus():
    print(f" Looking for corpus files in: {CORPUS_DIR}")
    if not os.path.exists(CORPUS_DIR):
        print(f" Error: Corpus directory does not exist at {CORPUS_DIR}")
        return

    #Initialize Qdrant Client (Persistent local DB)
    client = QdrantClient(path=DB_PATH)

    #Initialize Embedding Model (384-dimensional vectors)
    print(" Loading embedding model (all-MiniLM-L6-v2)...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    #Re-create collection if it already exists to ensure a clean state
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in collections:
        print(f" Resetting existing collection '{COLLECTION_NAME}'...")
        client.delete_collection(COLLECTION_NAME)

    print(f" Creating collection '{COLLECTION_NAME}'...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    #Configure text splitter (500 chars with 50 overlap for context retention)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    points = []
    point_id = 1

    # Iterate over files in the corpus folder
    for file_name in os.listdir(CORPUS_DIR):
        file_path = os.path.join(CORPUS_DIR, file_name)
        
        # Ignore subdirectories or hidden files like .gitkeep
        if os.path.isfile(file_path) and not file_name.startswith('.'):
            print(f" Processing: {file_name}")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f" Could not read {file_name}: {e}")
                continue

            chunks = text_splitter.split_text(content)
            for chunk_idx, chunk in enumerate(chunks):
                vector = embedder.encode(chunk).tolist()
                
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "text": chunk,
                            "source": file_name,
                            "chunk_id": chunk_idx
                        }
                    )
                )
                point_id += 1

    if points:
        print(f"Upserting {len(points)} vector chunks to Qdrant...")
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print("Ingestion completed successfully!")
    else:
        print("No valid files found in corpus directory to ingest.")


if __name__ == "__main__":
    ingest_corpus()