# 🧠 NeuralNotes — Smart Study Assistant

An AI-powered study assistant that transforms any PDF into an
interactive learning experience. Upload lecture notes or textbooks
and get instant AI-generated notes, answers to your questions,
flashcards, and a full study guide.

---

## ✨ Features

- 📄 **PDF Upload** — Drag and drop any PDF document
- ⚡ **Quick Notes** — Instant summary generated right after upload
- 💬 **Q&A Chat** — Ask anything about your document
- 🃏 **Flashcards** — Auto-generated question/answer cards
- 📚 **Study Guide** — Structured notes with key concepts and review

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python + FastAPI |
| AI | Groq API (LLaMA 3.1) |
| PDF Processing | PyMuPDF |

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/smart-study-assistant.git
cd smart-study-assistant
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API Key
```bash
cp .env.example .env
```
Open `.env` and add your Groq API key: