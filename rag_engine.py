import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

_store = {"chunks": []}


def reset_store():
    _store["chunks"] = []


def store_chunks(chunks: list[str]):
    reset_store()
    _store["chunks"] = chunks
    print(f"[RAG] Stored {len(chunks)} chunks")


def retrieve_relevant_chunks(query: str, n_results: int = 6) -> list[str]:
    if not _store["chunks"]:
        return []
    query_words = set(re.sub(r'[^\w\s]', '', query.lower()).split())
    if not query_words:
        return _store["chunks"][:n_results]
    scored = []
    for chunk in _store["chunks"]:
        chunk_words = set(re.sub(r'[^\w\s]', '', chunk.lower()).split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [c for s, c in scored[:n_results] if s > 0]
    return top if top else _store["chunks"][:n_results]


def answer_question(question: str) -> str:
    if not _store["chunks"]:
        return "No document uploaded yet. Please upload a PDF first."
    chunks = retrieve_relevant_chunks(question)
    context = "\n\n".join(chunks)
    print(f"[RAG] Answering: {question[:50]}")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant. Answer questions based ONLY on the provided context. If the answer is not in the context, say 'I could not find that in your document.'"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content