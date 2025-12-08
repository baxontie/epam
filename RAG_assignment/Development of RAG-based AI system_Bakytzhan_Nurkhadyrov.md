Development of RAG-based AI system_Baha_[LastName].md
Project Title

RAG Legal Assistant — Qdrant + SentenceTransformers + Local LLM (Ollama)

Overview

This project implements a Retrieval-Augmented Generation (RAG) system designed to answer legal questions based on a curated dataset of English-language civil and contract law documents. The system enriches LLM responses by retrieving the most relevant legal context from a vector database and injecting it into the model prompt.

The result is a fully local, reproducible, privacy-preserving RAG pipeline built with open-source tools.

Main Idea and Concepts

The solution enhances an LLM's reasoning with domain-specific knowledge by combining:

• Vector embeddings of legal texts
• Semantic search in Qdrant
• LLM generation via Ollama (local, free, no API keys)
• Interactive UI via Streamlit

RAG allows the LLM to produce grounded, context-aware answers while avoiding hallucinations.

Dataset Description

The dataset consists of 15 English-language entries including:

• Civil Code articles
• Explanations
• Examples
• FAQs
• Templates
• Commentary
• Court procedure basics

Each record includes:

id, source_type, title, text, tags


The dataset provides a small but representative legal corpus suitable for demonstrating retrieval and context augmentation.

Stored in: dataset.json

Technical Architecture
Components

Embedding Model: SentenceTransformers all-MiniLM-L6-v2

Vector Database: Qdrant (Docker container, port 6333)

LLM: Local Ollama model (llama3.1, mistral, etc.)

Frontend: Streamlit web interface

Backend Scripts:
• script.py — loads dataset, generates embeddings, uploads to Qdrant
• app.py — handles RAG workflow, UI, and LLM invocation

System Workflow

User enters a question in Streamlit

System generates an embedding vector with SentenceTransformers

Qdrant performs vector search and returns top-k relevant documents

The documents are bundled into a context block

The prompt + context is passed to the Ollama LLM

LLM returns a grounded answer

Answer is displayed to the user

Tools & Technologies

Python 3.11

SentenceTransformers

Qdrant client 1.7.0

Qdrant (Docker image)

Streamlit

Ollama (local LLM engine)

Requests

Requirements

Python 3.10–3.12

Docker installed and running

Models downloaded in Ollama (ollama pull llama3.1, etc.)

Port availability:
• 6333 (Qdrant)
• 11434 (Ollama)
• 8501 (Streamlit)

Limitations

RAG answers are restricted to the dataset context

Dataset is small and serves as a demonstration

Not intended for real legal advice

Local LLM quality depends on model size (8B performs reasonably well)

How to Run the System
1. Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

2. Prepare dataset

Place dataset.json in the working directory.

3. Load data into Qdrant
python script.py


Expected result:

Collection created.
Data successfully uploaded.

4. Start Ollama
ollama run llama3.1


(or simply ensure Ollama is running in the background)

5. Launch the UI
streamlit run app.py


Open in browser:

http://localhost:8501

Video Demonstration Link

https://drive.google.com/file/d/1-e5wdwwYOWcDK_qqv_KuWG-8y8-xxaJ5/view?usp=drive_link

Conclusion

The project successfully implements a fully local RAG system meeting all assignment requirements, demonstrating retrieval-based augmentation of LLM knowledge through Qdrant vector search and a structured dataset.