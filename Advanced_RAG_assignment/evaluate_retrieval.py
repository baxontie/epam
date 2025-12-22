import json
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "legal"
QDRANT_URL = "http://localhost:6333"
TOP_K = 1

client = QdrantClient(url=QDRANT_URL)
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("evaluation_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

total = len(questions)
relevant = 0

for q in questions:
    query_vector = model.encode(q["question"]).tolist()

    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=TOP_K
    )

    retrieved_text = " ".join(
        hit.payload.get("text", "").lower() for hit in search_result
    )

    if any(keyword.lower() in retrieved_text for keyword in q["expected_keywords"]):
        relevant += 1

cr_at_k = relevant / total

print("==== Retrieval Evaluation ====")
print(f"Total questions: {total}")
print(f"Relevant contexts found: {relevant}")
print(f"CR@{TOP_K}: {cr_at_k:.2f}")
