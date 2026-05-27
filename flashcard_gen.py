import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

_document_text = ""


def set_document_text(text: str):
    global _document_text
    _document_text = text
    print(f"[FLASHCARD] Document set: {len(text)} chars")


def get_document_text() -> str:
    return _document_text


def generate_flashcards() -> list[dict]:
    if not _document_text:
        return []

    sample = _document_text[:3000]
    print("[FLASHCARD] Generating...")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a study assistant. Return ONLY valid JSON array, no markdown, no backticks, no explanation."},
            {"role": "user", "content": f"""Generate 10 flashcards from this document.
Return ONLY this JSON format, nothing else:
[{{"question": "...", "answer": "..."}}, {{"question": "...", "answer": "..."}}]

Document:
{sample}"""}
        ]
    )

    raw = response.choices[0].message.content.strip()
    print(f"[FLASHCARD] Raw: {raw[:150]}")

    if "```" in raw:
        raw = re.sub(r'```(?:json)?', '', raw).strip()
    start = raw.find('[')
    end = raw.rfind(']') + 1
    if start != -1 and end > start:
        raw = raw[start:end]

    try:
        cards = json.loads(raw)
        return cards if isinstance(cards, list) else []
    except Exception as e:
        print(f"[FLASHCARD] Parse error: {e}, raw: {raw[:200]}")
        return [{"question": "Error generating flashcards", "answer": "Please try again"}]