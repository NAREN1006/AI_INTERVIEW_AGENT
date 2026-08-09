# AI Interview Agent — Requirements Document

## 1. Project Title

**AI Interview Agent**

## 2. Project Description

AI Interview Agent is an AI-powered web application that simulates technical interviews. The platform creates interview sessions, asks technical questions, evaluates candidate responses, tracks progress, and provides a final performance report.

## 3. Objectives

* Conduct automated technical interviews.
* Provide structured interview questions.
* Evaluate candidate answers.
* Track interview progress.
* Identify candidate strengths and improvement areas.
* Provide topic-wise performance analysis.
* Store interview session information.
* Provide a web-based candidate dashboard.

## 4. Functional Requirements

### 4.1 Candidate

The candidate should be able to:

* Start an interview.
* Receive interview questions.
* Submit answers.
* Continue through multiple interview questions.
* View interview progress.
* Complete an interview.
* View the final evaluation.
* View strengths and areas for improvement.
* View topic-wise performance.

### 4.2 Interview Management

The system should:

* Create a unique interview session.
* Maintain the current interview state.
* Store questions and answers.
* Track the number of completed questions.
* Detect interview completion.
* Store the final interview status.

### 4.3 Answer Evaluation

The system should:

* Accept candidate answers.
* Evaluate answers based on the interview topic.
* Generate a score.
* Store evaluation feedback.
* Identify areas where the candidate needs improvement.

### 4.4 Dashboard

The candidate dashboard should display:

* Interview status.
* Overall score.
* Topic-wise scores.
* Strengths.
* Areas for improvement.
* Recommended next steps.

### 4.5 RAG / Knowledge Retrieval

The system includes a retrieval architecture for:

* Creating embeddings from knowledge documents.
* Storing document vectors.
* Retrieving relevant context.
* Providing relevant knowledge to the interview system.

The deployment version can operate without active RAG retrieval when resource constraints require it.

## 5. Non-Functional Requirements

### Performance

* API responses should be reasonably fast.
* The application should support multiple interview requests.
* The frontend should load efficiently.

### Reliability

* Interview failures should not crash the entire application.
* API errors should be handled gracefully.
* Interview sessions should be persisted.

### Usability

* The interface should be simple and easy to navigate.
* Candidates should clearly see interview progress.
* Feedback should be understandable.

### Scalability

The architecture should allow future integration of:

* PostgreSQL
* Cloud-hosted vector databases
* LLM APIs
* Docker
* Kubernetes

## 6. Technology Requirements

### Frontend

* React.js
* Vite
* React Router
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy

### AI / ML

* Natural Language Processing
* Embeddings
* Retrieval-Augmented Generation
* ChromaDB
* Scikit-learn
* Hugging Face ecosystem

### Database

* SQLite
* SQLAlchemy ORM

### Deployment

* GitHub
* Render

## 7. Hardware Requirements

### Development Machine

Recommended:

* Processor: Intel Core i5 / AMD Ryzen 5 or higher
* RAM: 8 GB minimum, 16 GB recommended
* Storage: At least 10 GB free space
* Internet connection
* Windows, Linux, or macOS

### Production

The deployed application runs on cloud infrastructure provided by Render.

## 8. Software Requirements

* Python 3.x
* Node.js
* npm
* Git
* GitHub account
* Modern web browser
* VS Code or another code editor

## 9. System Architecture

```text
Candidate
   |
   v
React Frontend
   |
   | REST API
   v
FastAPI Backend
   |
   +------------------+
   |                  |
   v                  v
Interview Service   Evaluation
   |                  |
   v                  v
Session Manager    Answer Analysis
   |
   v
SQLAlchemy / SQLite
   |
   v
Candidate Dashboard
```

## 10. API Requirements

### Health Check

```http
GET /
```

### Interview API

```http
POST /api/interview
```

### Candidate Dashboard

```http
GET /api/candidate/dashboard/{session_id}
```

### API Documentation

```text
/docs
```

FastAPI provides interactive Swagger API documentation.

## 11. Data Requirements

The system stores information such as:

* Session ID
* Candidate name
* Interview status
* Questions
* Answers
* Scores
* Evaluation feedback
* Interview completion status
* Creation timestamp

## 12. Deployment Requirements

### Backend

The backend must:

* Listen on the port provided by the hosting platform.
* Allow frontend CORS requests.
* Provide REST API endpoints.
* Initialize required database tables during application startup.

### Frontend

The frontend must:

* Build successfully using Vite.
* Use the deployed backend API URL.
* Be configured with the correct backend endpoint.
* Serve the generated production files.

## 13. Future Requirements

Future versions may include:

* Resume-based personalized interviews.
* Voice interview functionality.
* Real-time speech recognition.
* LLM-based answer evaluation.
* Multilingual interviews.
* Authentication.
* PostgreSQL database.
* Cloud vector database.
* Docker containerization.
* Kubernetes deployment.
* Advanced candidate analytics.

## 14. Success Criteria

The project will be considered successful when:

1. A candidate can open the web application.
2. The candidate can start an interview.
3. The backend creates an interview session.
4. Questions are presented to the candidate.
5. Answers can be submitted.
6. Answers are evaluated.
7. Interview progress is tracked.
8. The interview can be completed.
9. Results are stored.
10. The candidate dashboard displays the interview results.

## 15. Live Deployment

**Frontend:**
https://ai-interview-agent-c4xq.onrender.com

**Backend:**
https://ai-interview-agent-s4da.onrender.com

**API Documentation:**
https://ai-interview-agent-s4da.onrender.com/docs

## 16. Repository

GitHub Repository:

https://github.com/NAREN1006/AI_INTERVIEW_AGENT
