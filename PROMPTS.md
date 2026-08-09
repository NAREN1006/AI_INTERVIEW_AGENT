# AI Usage Log — AI Interview Agent

## Overview

This project was developed with AI-assisted coding and debugging. AI tools were used for architecture planning, implementation guidance, debugging, deployment troubleshooting, documentation, and frontend/backend integration.

The primary AI assistant used during development was ChatGPT.

---

## 1. Project Architecture

### Prompt

> Help me design an AI Interview Agent project with a React frontend and FastAPI backend. I want interview sessions, question generation, answer evaluation, and a candidate dashboard.

### AI Assistance

Used AI assistance to plan:

* React frontend structure
* FastAPI backend structure
* Interview session workflow
* Candidate dashboard
* REST API communication
* Database structure

---

## 2. Backend Development

### Prompt

> Help me create a FastAPI backend for an AI interview application with interview session management and candidate evaluation.

### AI Assistance

Used AI assistance to develop and troubleshoot:

* FastAPI application structure
* API endpoints
* Request/response handling
* CORS configuration
* Uvicorn deployment
* Error handling

---

## 3. Database

### Prompt

> Help me create SQLAlchemy models for interview sessions, interview questions, candidate answers, scores, and evaluations.

### AI Assistance

AI assistance was used to design:

* `Interview` model
* `InterviewQuestion` model
* Session IDs
* Answer storage
* Evaluation scores
* Interview completion status
* Database initialization

The project uses SQLAlchemy with SQLite for the current deployment.

---

## 4. Frontend Development

### Prompt

> Help me build a React frontend for an AI interview platform with Home, Interview, and Candidate Dashboard pages.

### AI Assistance

Used AI assistance for:

* React component structure
* React Router configuration
* Navbar implementation
* Interview page
* Dashboard page
* API integration
* Frontend debugging
* Responsive UI improvements

---

## 5. Frontend and Backend Integration

### Prompt

> My React frontend is running separately from my FastAPI backend. Help me connect the frontend to the deployed FastAPI backend.

### AI Assistance

Used AI assistance to:

* Replace local API URLs
* Configure the deployed backend URL
* Debug API requests
* Configure FastAPI CORS
* Test frontend-to-backend communication

Example deployed backend URL:

```text
https://ai-interview-agent-s4da.onrender.com
```

---

## 6. CORS Debugging

### Problem

The deployed frontend was unable to communicate correctly with the FastAPI backend.

### Prompt

> My Render frontend is calling my deployed FastAPI backend, but the browser is showing CORS errors. Help me configure FastAPI CORS for the deployed frontend.

### AI Assistance

The FastAPI CORS configuration was updated to allow the deployed frontend origin.

This was tested using browser requests and Render application logs.

---

## 7. Database Deployment Debugging

### Problem

The deployed backend returned:

```text
sqlite3.OperationalError: no such table: interviews
```

### Prompt

> My deployed FastAPI application says no such table: interviews even though the SQLAlchemy model exists. Help me initialize the database when the application starts.

### AI Assistance

Used AI assistance to identify that the database tables needed to be initialized during application startup.

The application was updated to call the database initialization function when FastAPI starts.

---

## 8. Deployment

### Prompt

> Help me deploy my FastAPI backend and React frontend to Render.

### AI Assistance

Used AI assistance for:

* Render backend configuration
* Uvicorn startup command
* Render `$PORT` configuration
* React production build
* Static site deployment
* Frontend/backend URL configuration
* Deployment troubleshooting

Backend:

```text
https://ai-interview-agent-s4da.onrender.com
```

Frontend:

```text
https://ai-interview-agent-c4xq.onrender.com
```

---

## 9. Interview API Debugging

### Problem

The interview endpoint initially returned HTTP 500 errors.

### Prompt

> My FastAPI interview endpoint returns HTTP 500 on Render. Help me interpret the application logs and identify the cause.

### AI Assistance

Used AI assistance to analyze:

* FastAPI logs
* SQLAlchemy errors
* API responses
* CORS preflight requests
* Render deployment logs

The API was subsequently tested successfully with:

```text
POST /api/interview → 200 OK
```

---

## 10. Candidate Dashboard

### Prompt

> Help me create a candidate dashboard that displays interview completion, scores, strengths, areas for improvement, and topic performance.

### AI Assistance

Used AI assistance to implement and debug:

* Candidate dashboard
* Session-based dashboard retrieval
* Topic performance
* Strengths
* Improvement areas
* Final interview score

---

## 11. Documentation

### Prompt

> Help me create professional README and requirements documentation for my AI Interview Agent hackathon project.

### AI Assistance

Used AI assistance to prepare:

* Project overview
* Features
* Architecture
* Technology stack
* API documentation
* Installation instructions
* Deployment information
* Requirements documentation
* Future improvements

---

## 12. AI-Assisted Debugging Summary

AI assistance was used throughout development for:

* Architecture planning
* Code generation
* Code modification
* Debugging
* Error analysis
* API integration
* Database troubleshooting
* CORS troubleshooting
* Deployment troubleshooting
* Documentation

The final implementation was tested and adjusted manually during development.

---

## 13. AI Tools Used

**Primary tool:**

* ChatGPT

**Usage areas:**

* Code assistance
* Technical explanations
* Debugging
* Architecture planning
* Documentation
* Deployment troubleshooting

---

## 14. Transparency Statement

AI assistance was used as a development aid throughout the project. Generated suggestions were reviewed, adapted, tested, and integrated into the project based on the application's requirements.

The developer remained responsible for integrating the components, configuring the deployment, testing the application, and resolving project-specific issues.
