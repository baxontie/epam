import json
import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "legal"
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434/api/generate"
TOP_K = 2

client = QdrantClient(url=QDRANT_URL)
model = SentenceTransformer("all-MiniLM-L6-v2")


def rewrite_query(question: str) -> list[str]:
    prompt = f"""
Rewrite the following legal question into 3 different semantically equivalent formulations.

Question:
{question}

Return each version on a new line.
"""
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "temperature": 0.3,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    text = response.json().get("response", "")
    rewrites = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]

    return rewrites[:3]


with open("evaluation_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

total = len(questions)
relevant = 0

for q in questions:
    all_queries = [q["question"]] + rewrite_query(q["question"])
    retrieved_text = ""

    for query in all_queries:
        vector = model.encode(query).tolist()
        result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=TOP_K
        )
        for hit in result:
            retrieved_text += " " + hit.payload.get("text", "").lower()

    if any(keyword.lower() in retrieved_text for keyword in q["expected_keywords"]):
        relevant += 1

cr_at_k = relevant / total

print("==== Enhanced Retrieval Evaluation ====")
print(f"Total questions: {total}")
print(f"Relevant contexts found: {relevant}")
print(f"CR@{TOP_K}: {cr_at_k:.2f}")
