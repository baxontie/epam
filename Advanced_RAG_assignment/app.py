import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import requests

COLLECTION_NAME = "legal"
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3.1"

client = QdrantClient(url=QDRANT_URL)
model = SentenceTransformer("all-MiniLM-L6-v2")


def call_llm(prompt: str) -> str:
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "temperature": 0.1,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[Empty response]")
    except Exception as e:
        return f"Error calling Ollama: {e}"


st.title("RAG Legal Assistant — Qdrant + Local LLM (Ollama)")

query = st.text_input("Enter your legal question:")
top_k = st.slider("Number of retrieved documents:", 1, 10, 3)


if query:

    st.subheader("Performing vector search in the knowledge base...")
    query_vector = model.encode(query).tolist()

    try:
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k
        )
    except Exception as e:
        st.error(f"Qdrant search error: {e}")
        st.stop()

    docs = []
    for hit in search_result:
        payload = hit.payload
        text = payload.get("text", "")
        docs.append(text)

    st.subheader("Retrieved documents:")
    if not docs:
        st.info("No matching documents were found.")
    else:
        for i, d in enumerate(docs, 1):
            st.markdown(f"**{i}.** {d}")

    context_block = "\n\n".join(docs)

    st.subheader("AI-generated answer (RAG):")

    prompt = f"""
You are a legal assistant. Use ONLY the context provided below.

Context:
{context_block}

Question:
{query}

Provide a concise, accurate, legally neutral answer strictly based on the context above.
If the context does not contain enough information to answer the question, say:
'The dataset does not contain enough information to answer this question.'
"""

    with st.spinner("Generating answer..."):
        answer = call_llm(prompt)

    st.write(answer)
