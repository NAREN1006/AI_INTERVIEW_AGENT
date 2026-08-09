# 🤖 AI Interview Agent

An AI-powered interview platform that conducts personalized technical interviews, evaluates candidate answers, tracks interview progress, and provides performance insights.

## 🚀 Live Demo

**Frontend:**
https://ai-interview-agent-c4xq.onrender.com

**Backend API:**
https://ai-interview-agent-s4da.onrender.com

**API Documentation:**
https://ai-interview-agent-s4da.onrender.com/docs

---

## 📌 Project Overview

AI Interview Agent is a web-based platform designed to simulate technical interviews using AI.

The system creates an interview session for a candidate, presents technical questions, accepts answers, evaluates responses, and generates a final performance report.

The platform is designed to provide a structured and interactive interview experience.

---

## ✨ Features

* 🎯 AI-powered technical interview
* 👤 Candidate profile and interview session management
* 📝 Dynamic interview questions
* 💬 Candidate answer submission
* 📊 Automatic answer evaluation
* 📈 Interview progress tracking
* 🏆 Final interview score
* 📋 Strengths and improvement areas
* 📚 Topic-based performance analysis
* 🗄️ Interview data persistence
* 🌐 React frontend
* ⚡ FastAPI backend
* 🔌 REST API architecture
* ☁️ Render deployment

---

## 🏗️ System Architecture

```text
                ┌──────────────────────┐
                │      Candidate       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    React Frontend    │
                │      (Vite)          │
                └──────────┬───────────┘
                           │ REST API
                           ▼
                ┌──────────────────────┐
                │    FastAPI Backend   │
                └──────────┬───────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   ┌────────────┐   ┌─────────────┐  ┌──────────────┐
   │ Interview  │   │ Evaluation  │  │   Database   │
   │ Management │   │   System    │  │   SQLite     │
   └────────────┘   └─────────────┘  └──────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ RAG / AI    │
                    │ Components  │
                    └─────────────┘
```

---

## 🛠️ Technologies Used

### Frontend

* React.js
* Vite
* React Router
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy

### AI / ML

* NLP
* Embeddings
* Retrieval-Augmented Generation (RAG)
* ChromaDB
* Scikit-learn
* Hugging Face ecosystem

### Database

* SQLite
* SQLAlchemy ORM

### Deployment

* Render
* GitHub

---

## 📂 Project Structure

```text
AI_INTERVIEW_AGENT/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── session_manager.py
│   ├── candidate_service.py
│   ├── curriculum_service.py
│   ├── interview_planner.py
│   ├── answer_evaluator.py
│   │
│   └── rag/
│       ├── rag_service.py
│       ├── embeddings.py
│       ├── retriever.py
│       └── vector_store.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Interview.jsx
│   │   │   └── Dashboard.jsx
│   │   │
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

## 🔄 Interview Workflow

```text
Candidate
    ↓
Start Interview
    ↓
Create Interview Session
    ↓
Generate Interview Question
    ↓
Candidate Submits Answer
    ↓
Evaluate Answer
    ↓
Store Evaluation
    ↓
Next Question
    ↓
Interview Completion
    ↓
Generate Performance Report
    ↓
Candidate Dashboard
```

---

## 📊 Candidate Dashboard

The dashboard provides:

* Interview completion status
* Overall evaluation score
* Topic-wise performance
* Strengths
* Areas for improvement
* Recommended next steps

---

## 🔌 API Endpoints

### Health Check

```http
GET /
```

Returns the API status.

### Interview

```http
POST /api/interview
```

Creates or continues an interview session.

### Candidate Dashboard

```http
GET /api/candidate/dashboard/{session_id}
```

Retrieves the candidate's interview performance.

### API Documentation

FastAPI automatically provides interactive API documentation:

```text
/docs
```

---

## 💻 Local Development

### Clone the repository

```bash
git clone https://github.com/NAREN1006/AI_INTERVIEW_AGENT.git
cd AI_INTERVIEW_AGENT
```

### Backend

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend will run on:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally run on:

```text
http://localhost:5173
```

---

## ☁️ Deployment

The project is deployed using Render.

### Frontend

```text
https://ai-interview-agent-c4xq.onrender.com
```

### Backend

```text
https://ai-interview-agent-s4da.onrender.com
```

The React frontend communicates with the deployed FastAPI backend through REST APIs.

---

## 🔐 Security & Configuration

Sensitive configuration values should be stored using environment variables rather than committing them directly to GitHub.

Do not commit:

```text
.env
*.db
venv/
node_modules/
__pycache__/
```

---

## 🎯 Future Improvements

* Voice-based interviews
* Speech-to-text answer evaluation
* LLM-powered personalized feedback
* Resume-based question generation
* Multi-language interviews
* Advanced RAG knowledge retrieval
* Authentication and user accounts
* PostgreSQL production database
* Advanced analytics dashboard
* Docker and Kubernetes deployment

---

## 👨‍💻 Author

**Narendran**

MCA – Generative AI

GitHub:
https://github.com/NAREN1006

---

## 📄 License

This project is developed for educational and hackathon purposes.
