from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import json
import logging

from rag.rag_service import retrieve_context
from answer_evaluator import evaluate_answer
from data_loader import load_curriculum, load_candidates
from candidate_service import build_candidate_profile
from curriculum_service import get_relevant_curriculum_days
from interview_planner import build_interview_plan

from session_manager import (
    create_session,
    get_session,
    add_question,
    add_answer,
    add_evaluation,
    is_interview_complete,
    mark_interview_complete,
)

from database import SessionLocal, init_database
from models import Interview, InterviewQuestion

from breeth_memory import save_memory, search_memory


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("ai_interview_agent")

app = FastAPI(
    title="AI Interview Agent",
    version="1.0.0",
)
init_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INTERVIEW_QUESTION_COUNT = 8


class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class TopicFeedback(BaseModel):
    topic: str
    score: float
    strengths: List[str]
    gaps: List[str]


class Feedback(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[str]
    next: List[str]
    topic_feedback: List[TopicFeedback]


class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[Feedback] = None


@app.get("/")
def root():
    return {"message": "AI Interview Agent API is running"}


def create_fallback_plan(profile):
    candidate = profile.get("candidate", {})
    if not isinstance(candidate, dict):
        candidate = {}

    skills = candidate.get("skills", [])
    if not isinstance(skills, list):
        skills = []

    topic_data = {
        "Python": {
            "day": 1,
            "type": "SKILL",
            "tools": ["Python", "Pandas", "NumPy", "Scikit-learn", "FastAPI"],
            "objectives": [
                "Explain Python programming",
                "Apply Python in real-world projects",
                "Use Python libraries for data processing",
                "Build backend applications using Python",
            ],
        },
        "Machine Learning": {
            "day": 2,
            "type": "AI_CORE",
            "tools": ["Python", "Scikit-learn"],
            "objectives": [
                "Explain machine learning concepts",
                "Describe the machine learning project workflow",
                "Explain data preprocessing and feature engineering",
                "Explain model training and evaluation",
                "Apply machine learning to real-world problems",
            ],
        },
        "NLP": {
            "day": 3,
            "type": "AI_CORE",
            "tools": ["Python", "NLTK", "spaCy", "Scikit-learn"],
            "objectives": [
                "Explain natural language processing",
                "Describe NLP preprocessing techniques",
                "Explain text representation using TF-IDF or embeddings",
                "Describe NLP model training and evaluation",
                "Apply NLP to real-world projects",
            ],
        },
        "Embeddings": {
            "day": 7,
            "type": "AI_CORE",
            "tools": ["Sentence Transformers", "OpenAI Embeddings", "Scikit-learn"],
            "objectives": [
                "Explain text embeddings",
                "Explain how text is converted into vectors",
                "Generate embeddings for documents",
                "Explain similarity between embeddings",
            ],
        },
        "Vector Databases": {
            "day": 8,
            "type": "BUILD",
            "tools": ["ChromaDB", "Pinecone"],
            "objectives": [
                "Explain vector databases",
                "Explain semantic search",
                "Store embeddings in a vector database",
                "Retrieve relevant documents",
            ],
        },
        "Prompt Engineering Fundamentals": {
            "day": 4,
            "type": "GENERATIVE_AI",
            "tools": ["LLM", "Prompt Engineering", "System Prompts"],
            "objectives": [
                "Explain prompt engineering",
                "Explain zero-shot and few-shot prompting",
                "Design effective system prompts",
                "Compare prompts based on accuracy and output quality",
            ],
        },
        "Docker & Kubernetes Deployment": {
            "day": 9,
            "type": "DEPLOYMENT",
            "tools": ["Docker", "Kubernetes"],
            "objectives": [
                "Explain Docker containers",
                "Create a Dockerfile",
                "Explain containerized application deployment",
                "Explain Kubernetes pods and deployments",
            ],
        },
        "Monitoring, Logging & Observability": {
            "day": 10,
            "type": "OPERATIONS",
            "tools": ["Logging", "Monitoring", "Observability"],
            "objectives": [
                "Explain application logging",
                "Explain monitoring concepts",
                "Explain observability",
                "Identify application failures using logs and metrics",
            ],
        },
    }

    plan = []

    for skill in skills:
        if not isinstance(skill, str):
            continue

        matched_topic = next(
            (
                topic_name
                for topic_name in topic_data
                if skill.lower() == topic_name.lower()
            ),
            None,
        )

        if matched_topic:
            data = topic_data[matched_topic]
            plan.append({
                "title": matched_topic,
                "day": data["day"],
                "type": data["type"],
                "tools": data["tools"],
                "objectives": data["objectives"],
            })

    additional_topics = [
        "Prompt Engineering Fundamentals",
        "Embeddings",
        "Vector Databases",
        "Docker & Kubernetes Deployment",
        "Monitoring, Logging & Observability",
    ]

    for topic_name in additional_topics:
        if len(plan) >= 4:
            break

        if any(topic["title"] == topic_name for topic in plan):
            continue

        data = topic_data[topic_name]
        plan.append({
            "title": topic_name,
            "day": data["day"],
            "type": data["type"],
            "tools": data["tools"],
            "objectives": data["objectives"],
        })

    if not plan:
        for topic_name in [
            "Python",
            "Machine Learning",
            "NLP",
            "Prompt Engineering Fundamentals",
        ]:
            data = topic_data[topic_name]
            plan.append({
                "title": topic_name,
                "day": data["day"],
                "type": data["type"],
                "tools": data["tools"],
                "objectives": data["objectives"],
            })

    return plan


def build_question_plan(interview_plan):
    if not interview_plan:
        return []

    question_plan = []

    for topic in interview_plan:
        question_plan.append({
            **topic,
            "question_type": "conceptual",
        })

        if len(question_plan) >= INTERVIEW_QUESTION_COUNT:
            break

        question_plan.append({
            **topic,
            "question_type": "practical",
        })

        if len(question_plan) >= INTERVIEW_QUESTION_COUNT:
            break

    if len(question_plan) < INTERVIEW_QUESTION_COUNT:
        fallback = create_fallback_plan({})

        for topic in fallback:
            if len(question_plan) >= INTERVIEW_QUESTION_COUNT:
                break

            if any(
                item["title"] == topic["title"]
                for item in question_plan
            ):
                continue

            question_plan.append({
                **topic,
                "question_type": "conceptual",
            })

            if len(question_plan) < INTERVIEW_QUESTION_COUNT:
                question_plan.append({
                    **topic,
                    "question_type": "practical",
                })

    if not question_plan:
        return []

    index = 0
    while len(question_plan) < INTERVIEW_QUESTION_COUNT:
        original = question_plan[index % len(question_plan)]
        question_plan.append({
            **original,
            "question_type": "practical",
        })
        index += 1

    return question_plan[:INTERVIEW_QUESTION_COUNT]


def generate_question(topic):
    title = topic.get("title", "this topic")
    question_type = topic.get("question_type", "conceptual")

    if question_type == "conceptual":
        return (
            f"Let's explore {title}. "
            f"Can you explain the key concepts of {title} "
            f"and why they are important?"
        )

    return (
        f"Let's explore {title}. "
        f"How would you apply {title} "
        f"in a practical real-world project?"
    )


def build_final_feedback(session):
    evaluations = session.get("evaluations", [])
    all_strengths = []
    all_gaps = []
    topic_results = {}

    for item in evaluations:
        if not isinstance(item, dict):
            continue

        topic = item.get("topic", "Unknown Topic")
        evaluation = item.get("evaluation", item)

        if not isinstance(evaluation, dict):
            continue

        if topic not in topic_results:
            topic_results[topic] = {
                "scores": [],
                "strengths": [],
                "gaps": [],
            }

        score = evaluation.get("score", 0)
        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0

        topic_results[topic]["scores"].append(score)

        strengths = evaluation.get("strengths", [])
        if not isinstance(strengths, list):
            strengths = []

        for strength in strengths:
            if strength not in topic_results[topic]["strengths"]:
                topic_results[topic]["strengths"].append(strength)
            if strength not in all_strengths:
                all_strengths.append(strength)

        gaps = evaluation.get("gaps", [])
        if not isinstance(gaps, list):
            gaps = []

        for gap in gaps:
            if gap not in topic_results[topic]["gaps"]:
                topic_results[topic]["gaps"].append(gap)
            if gap not in all_gaps:
                all_gaps.append(gap)

    topic_feedback = []

    for topic, data in topic_results.items():
        scores = data["scores"]
        topic_score = (
            round(sum(scores) / len(scores), 2)
            if scores
            else 0
        )

        topic_feedback.append(
            TopicFeedback(
                topic=topic,
                score=topic_score,
                strengths=data["strengths"][:5],
                gaps=data["gaps"][:5],
            )
        )

    all_scores = []

    for item in evaluations:
        if not isinstance(item, dict):
            continue

        evaluation = item.get("evaluation", item)
        if not isinstance(evaluation, dict):
            continue

        try:
            all_scores.append(float(evaluation.get("score", 0)))
        except (TypeError, ValueError):
            continue

    average_score = (
        round(sum(all_scores) / len(all_scores), 2)
        if all_scores
        else 0
    )

    summary = (
        "Interview completed with an average "
        f"evaluation score of {average_score}/100 "
        f"across {len(topic_feedback)} topics."
    )

    next_steps = [
        "Practice the topics identified in the gaps.",
        "Work on practical project-based explanations.",
        "Continue improving technical depth.",
    ]

    return Feedback(
        summary=summary,
        strengths=all_strengths[:5],
        gaps=all_gaps[:5],
        next=next_steps,
        topic_feedback=topic_feedback,
    )


def calculate_final_score(session):
    evaluations = session.get("evaluations", [])
    scores = []

    for item in evaluations:
        if not isinstance(item, dict):
            continue

        evaluation = item.get("evaluation", item)
        if not isinstance(evaluation, dict):
            continue

        try:
            scores.append(float(evaluation.get("score")))
        except (TypeError, ValueError):
            continue

    if not scores:
        return 0

    return round(sum(scores) / len(scores))


@app.post("/api/interview", response_model=InterviewResponse)
def interview(request: InterviewRequest):
    session_id = request.sessionId

    logger.info(
        "Interview request received | session=%s",
        session_id,
    )

    session = get_session(session_id)

    if session is None:
        logger.info(
            "Creating new interview session | session=%s",
            session_id,
        )

        candidates = load_candidates()
        curriculum = load_curriculum()

        candidate = request.candidate
        if candidate is None:
            candidate = candidates["candidates"][0]

        profile = build_candidate_profile(candidate)

        relevant_days = get_relevant_curriculum_days(
            profile,
            curriculum,
        )

        interview_plan = build_interview_plan(
            profile,
            relevant_days,
        )

        if not interview_plan:
            logger.warning(
                "Personalized plan empty. Using fallback plan."
            )
            interview_plan = create_fallback_plan(profile)

        question_plan = build_question_plan(interview_plan)

        if not question_plan:
            logger.error("Unable to create interview questions.")
            return InterviewResponse(
                reply="Unable to create interview questions.",
                done=True,
                feedback=None,
            )

        create_session(
            session_id,
            profile,
            question_plan,
        )

        try:
            candidate_data = profile.get("candidate", {})
            candidate_name = candidate_data.get("name", "Candidate")
            candidate_skills = candidate_data.get("skills", [])

            if not isinstance(candidate_skills, list):
                candidate_skills = []

            skills_text = ", ".join(
                str(skill) for skill in candidate_skills
            )

            save_memory(
                f"Candidate {candidate_name} is participating "
                f"in an AI technical interview. "
                f"Candidate skills: {skills_text}. "
                f"Interview session: {session_id}.",
                group_id=session_id,
            )
        except Exception:
            logger.exception("Breeth candidate memory error")

        first_topic = question_plan[0]
        question = generate_question(first_topic)

        add_question(
            session_id,
            question,
            first_topic["day"],
        )

        return InterviewResponse(
            reply=question,
            done=False,
            feedback=None,
        )

    if session.get("done"):
        feedback = build_final_feedback(session)
        return InterviewResponse(
            reply="The interview has already been completed.",
            done=True,
            feedback=feedback,
        )

    if request.message:
        answer = request.message.strip()

        if answer:
            answered_question_index = (
                len(session.get("questions_asked", [])) - 1
            )

            interview_plan = session.get(
                "interview_plan",
                [],
            )

            add_answer(
                session_id,
                answer,
            )

            session = get_session(session_id)

            if (
                0 <= answered_question_index
                < len(interview_plan)
            ):
                topic = interview_plan[answered_question_index]

                try:
                    rag_context = retrieve_context(
                        topic.get("title", ""),
                        top_k=2,
                    )
                except Exception:
                    logger.exception("RAG retrieval failed")
                    rag_context = []

                try:
                    memory_query = (
                        f"What does the candidate know about "
                        f"{topic.get('title', '')}?"
                    )

                    breeth_context = search_memory(
                        memory_query,
                        limit=3,
                    )

                    logger.info(
                        "Breeth memory retrieved | items=%d",
                        len(breeth_context),
                    )
                except Exception:
                    logger.exception(
                        "Breeth memory retrieval failed"
                    )

                try:
                    evaluation = evaluate_answer(
                        answer,
                        topic,
                        context=rag_context,
                    )
                except Exception:
                    logger.exception(
                        "Answer evaluation failed"
                    )

                    evaluation = {
                        "score": 0,
                        "strengths": [],
                        "gaps": topic.get("objectives", []),
                        "matched_objectives": [],
                        "missed_objectives": topic.get(
                            "objectives",
                            [],
                        ),
                        "matched_tools": [],
                    }

                evaluation_record = {
                    "topic": topic.get(
                        "title",
                        "Unknown Topic",
                    ),
                    "evaluation": evaluation,
                }

                add_evaluation(
                    session_id,
                    evaluation_record,
                )

                try:
                    candidate_data = session.get(
                        "candidate",
                        {},
                    )

                    if not isinstance(candidate_data, dict):
                        candidate_data = {}

                    candidate_name = candidate_data.get(
                        "name",
                        "Unknown Candidate",
                    )

                    memory_content = (
                        f"Candidate {candidate_name} "
                        f"answered an interview question about "
                        f"{topic.get('title', 'Unknown Topic')}. "
                        f"Candidate answer: {answer}. "
                        f"Evaluation score: "
                        f"{evaluation.get('score', 0)}/100. "
                        f"Strengths: "
                        f"{evaluation.get('strengths', [])}. "
                        f"Gaps: "
                        f"{evaluation.get('gaps', [])}."
                    )

                    save_memory(
                        memory_content,
                        group_id=session_id,
                    )
                except Exception:
                    logger.exception(
                        "Breeth answer memory save failed"
                    )

    if is_interview_complete(session_id):
        session = get_session(session_id)
        final_score = calculate_final_score(session)

        mark_interview_complete(
            session_id,
            final_score,
        )

        session = get_session(session_id)
        feedback = build_final_feedback(session)

        return InterviewResponse(
            reply="Thank you. The interview is now complete.",
            done=True,
            feedback=feedback,
        )

    session = get_session(session_id)

    interview_plan = session.get(
        "interview_plan",
        [],
    )

    questions_asked = session.get(
        "questions_asked",
        [],
    )

    question_index = len(questions_asked)

    if question_index >= INTERVIEW_QUESTION_COUNT:
        final_score = calculate_final_score(session)

        mark_interview_complete(
            session_id,
            final_score,
        )

        session = get_session(session_id)
        feedback = build_final_feedback(session)

        return InterviewResponse(
            reply="Thank you. The interview is now complete.",
            done=True,
            feedback=feedback,
        )

    if question_index >= len(interview_plan):
        final_score = calculate_final_score(session)

        mark_interview_complete(
            session_id,
            final_score,
        )

        session = get_session(session_id)
        feedback = build_final_feedback(session)

        return InterviewResponse(
            reply="Thank you. The interview is now complete.",
            done=True,
            feedback=feedback,
        )

    topic = interview_plan[question_index]

    question = generate_question(topic)

    add_question(
        session_id,
        question,
        topic["day"],
    )

    return InterviewResponse(
        reply=question,
        done=False,
        feedback=None,
    )


@app.get("/api/data-check")
def data_check():
    curriculum = load_curriculum()
    candidates = load_candidates()

    return {
        "curriculum_days": len(curriculum["days"]),
        "candidates": len(candidates["candidates"]),
    }


@app.get("/api/candidate-check")
def candidate_check():
    candidates = load_candidates()
    candidate = candidates["candidates"][0]

    profile = build_candidate_profile(candidate)

    return profile


@app.get("/api/curriculum-check")
def curriculum_check():
    candidates = load_candidates()
    curriculum = load_curriculum()

    candidate = candidates["candidates"][0]
    profile = build_candidate_profile(candidate)

    relevant_days = get_relevant_curriculum_days(
        profile,
        curriculum,
    )

    return {
        "candidate": profile["candidate"],
        "relevant_days": relevant_days,
    }


@app.get("/api/interview-plan-check")
def interview_plan_check():
    candidates = load_candidates()
    curriculum = load_curriculum()

    candidate = candidates["candidates"][0]
    profile = build_candidate_profile(candidate)

    relevant_days = get_relevant_curriculum_days(
        profile,
        curriculum,
    )

    plan = build_interview_plan(
        profile,
        relevant_days,
    )

    if not plan:
        plan = create_fallback_plan(profile)

    question_plan = build_question_plan(plan)

    return {
        "candidate": profile["candidate"],
        "interview_plan": question_plan,
        "question_count": len(question_plan),
        "covered_days": sorted(
            list({
                topic["day"]
                for topic in question_plan
            })
        ),
    }


@app.get("/api/rag-check")
def rag_check(
    query: str = "What is machine learning?",
):
    documents = retrieve_context(
        query,
        top_k=2,
    )

    return {
        "query": query,
        "retrieved_documents": documents,
    }


@app.get("/api/breeth-check")
def breeth_check(
    query: str = (
        "What does the candidate know about Python?"
    ),
):
    try:
        result = search_memory(
            query,
            limit=5,
        )

        return {
            "success": True,
            "query": query,
            "memory": result,
        }

    except Exception as error:
        logger.exception("Breeth check failed")

        return {
            "success": False,
            "query": query,
            "message": str(error),
        }


@app.get("/api/candidate/dashboard/{session_id}")
def candidate_dashboard(session_id: str):
    db = SessionLocal()

    try:
        interview = (
            db.query(Interview)
            .filter(
                Interview.session_id == session_id
            )
            .first()
        )

        if not interview:
            return {
                "success": False,
                "message": "Interview session not found",
            }

        questions = (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.session_id == session_id
            )
            .order_by(
                InterviewQuestion.question_number
            )
            .all()
        )

        question_history = []

        for item in questions:
            evaluation_data = None

            if item.evaluation:
                try:
                    evaluation_data = json.loads(
                        item.evaluation
                    )
                except Exception:
                    evaluation_data = item.evaluation

            question_history.append({
                "question_number": item.question_number,
                "question": item.question,
                "day": item.day,
                "answer": item.answer,
                "score": item.score,
                "evaluation": evaluation_data,
            })

        scores = [
            item.score
            for item in questions
            if item.score is not None
        ]

        average_score = (
            round(sum(scores) / len(scores), 2)
            if scores
            else 0
        )

        return {
            "success": True,
            "session_id": interview.session_id,
            "candidate_name": interview.candidate_name,
            "status": interview.status,
            "completed": interview.completed,
            "final_score": interview.final_score,
            "average_score": average_score,
            "total_questions": len(questions),
            "questions": question_history,
        }

    finally:
        db.close()
