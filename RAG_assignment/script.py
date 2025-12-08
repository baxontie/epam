# script.py
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import json
import os

dataset_path = "dataset.json"
collection_name = "legal"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = QdrantClient(url="http://localhost:6333")

existing_collections = [c.name for c in client.get_collections().collections]
if collection_name in existing_collections:
    client.delete_collection(collection_name)
    print("Old collection deleted.")

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE)
)
print("Collection created.")

if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"{dataset_path} not found! Put it near script.py")

with open(dataset_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)

points = []
for item in dataset:
    vector = model.encode(item["text"]).tolist()
    points.append(
        PointStruct(
            id=item["id"],
            vector=vector,
            payload={
                "title": item["title"],
                "text": item["text"],
                "source_type": item["source_type"],
                "tags": item["tags"]
            }
        )
    )

client.upsert(collection_name=collection_name, points=points)
print("Data successfully uploaded to Qdrant!")
