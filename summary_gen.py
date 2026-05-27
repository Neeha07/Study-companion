
import os
from dotenv import load_dotenv
from groq import Groq
from flashcard_gen import get_document_text

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_quick_notes(text: str) -> str:
    sample = text[:3000]
    print("[SUMMARY] Generating quick notes...")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a study assistant. Be clear, simple and concise."},
            {"role": "user", "content": f"""Read this document and give a quick simple summary in this format:

**What is this about?**
(1-2 sentences, very simple)

**Top 5 Key Points:**
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

Document:
{sample}"""}
        ]
    )
    return response.choices[0].message.content


def generate_summary() -> str:
    text = get_document_text()
    if not text:
        return "No document uploaded yet."

    sample = text[:4000]
    print("[SUMMARY] Generating study guide...")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert study guide creator. Use clear simple language a student can understand."},
            {"role": "user", "content": f"""Create a structured study guide from this document.

## Overview
(2-3 simple sentences about what this is)

## Key Concepts
(bullet points of important ideas, explained simply)

## Detailed Notes
(organized by topic, plain simple language)

## Quick Review
(5 key takeaways, one line each)

Document:
{sample}"""}
        ]
    )
    return response.choices[0].message.content