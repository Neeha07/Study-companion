from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import traceback

from pdf_processor import extract_text_from_pdf, chunk_text
from rag_engine import store_chunks, answer_question
from flashcard_gen import generate_flashcards, set_document_text
from summary_gen import generate_summary

app = FastAPI(title="NeuralNotes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "NeuralNotes API running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    try:
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF appears empty or scanned.")
        chunks = chunk_text(text)
        store_chunks(chunks)
        set_document_text(text)
        return {
            "message": "PDF uploaded and processed successfully",
            "filename": file.filename,
            "chunks_created": len(chunks)
        }
    except HTTPException:
        raise
    except Exception as e:
        print("UPLOAD ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        answer = answer_question(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        print("CHAT ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/flashcards")
async def get_flashcards():
    try:
        cards = generate_flashcards()
        return {"flashcards": cards, "count": len(cards)}
    except Exception as e:
        print("FLASHCARD ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/summary")
async def get_summary():
    try:
        summary = generate_summary()
        return {"summary": summary}
    except Exception as e:
        print("SUMMARY ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)