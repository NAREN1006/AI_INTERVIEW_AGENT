
import json

from database import SessionLocal
from models import Interview, InterviewQuestion


# =====================================================
# CONFIGURATION
# =====================================================

INTERVIEW_QUESTION_COUNT = 8

# In-memory cache
sessions = {}


# =====================================================
# HELPER
# =====================================================

def get_candidate_name(candidate_profile):

    if not isinstance(candidate_profile, dict):
        return None

    candidate = candidate_profile.get("candidate")

    if isinstance(candidate, dict):
        return (
            candidate.get("name")
            or candidate.get("full_name")
            or candidate.get("fullName")
        )

    if isinstance(candidate, str):
        return candidate

    return (
        candidate_profile.get("name")
        or candidate_profile.get("full_name")
        or candidate_profile.get("fullName")
    )


# =====================================================
# CREATE SESSION
# =====================================================

def create_session(
    session_id,
    candidate_profile,
    interview_plan,
):

    if session_id in sessions:
        return sessions[session_id]

    session = {
        "candidate": candidate_profile,
        "profile": candidate_profile,
        "interview_plan": interview_plan,
        "current_question": 0,
        "questions_asked": [],
        "answers": [],
        "evaluations": [],
        "covered_days": [],
        "done": False,
    }

    sessions[session_id] = session

    db = SessionLocal()

    try:

        interview = (
            db.query(Interview)
            .filter(
                Interview.session_id == session_id
            )
            .first()
        )

        if interview is None:

            candidate_name = get_candidate_name(
                candidate_profile
            )

            interview = Interview(
                session_id=session_id,
                candidate_name=candidate_name,
                status="in_progress",
                final_score=None,
                completed=False,
            )

            db.add(interview)
            db.commit()

        else:

            interview.status = "in_progress"
            interview.completed = False
            interview.final_score = None

            db.commit()

    except Exception:

        db.rollback()
        sessions.pop(session_id, None)
        raise

    finally:

        db.close()

    return session


# =====================================================
# RESTORE SESSION FROM DATABASE
# =====================================================

def restore_session(
    session_id,
    interview_plan=None,
    candidate_profile=None,
):

    db = SessionLocal()

    try:

        interview = (
            db.query(Interview)
            .filter(
                Interview.session_id == session_id
            )
            .first()
        )

        if interview is None:
            return None

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

        questions_asked = []
        answers = []
        evaluations = []
        covered_days = []

        for item in questions:

            questions_asked.append({
                "question": item.question,
                "day": item.day,
            })

            if item.answer is not None:

                answers.append(
                    item.answer
                )

            if item.evaluation is not None:

                try:

                    evaluations.append(
                        json.loads(
                            item.evaluation
                        )
                    )

                except Exception:

                    evaluations.append(
                        item.evaluation
                    )

            if (
                item.day is not None
                and item.day not in covered_days
            ):

                covered_days.append(
                    item.day
                )

        if candidate_profile is None:

            candidate_profile = {
                "candidate": {
                    "name": interview.candidate_name
                }
            }

        session = {
            "candidate": candidate_profile,
            "profile": candidate_profile,
            "interview_plan": interview_plan or [],
            "current_question": len(
                questions_asked
            ),
            "questions_asked": questions_asked,
            "answers": answers,
            "evaluations": evaluations,
            "covered_days": covered_days,
            "done": bool(interview.completed),
        }

        sessions[session_id] = session

        return session

    finally:

        db.close()


# =====================================================
# GET SESSION
# =====================================================

def get_session(session_id):

    # First check memory
    session = sessions.get(session_id)

    if session is not None:
        return session

    # If not found, restore from database
    return restore_session(session_id)


# =====================================================
# ADD QUESTION
# =====================================================

def add_question(
    session_id,
    question,
    day,
):

    session = get_session(session_id)

    if session is None:

        raise ValueError(
            f"Interview session not found: {session_id}"
        )

    if len(
        session["questions_asked"]
    ) >= INTERVIEW_QUESTION_COUNT:

        return

    session["questions_asked"].append({
        "question": question,
        "day": day,
    })

    session["current_question"] = len(
        session["questions_asked"]
    )

    if day not in session["covered_days"]:

        session["covered_days"].append(
            day
        )

    db = SessionLocal()

    try:

        question_number = len(
            session["questions_asked"]
        )

        existing = (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.session_id
                == session_id,
                InterviewQuestion.question_number
                == question_number,
            )
            .first()
        )

        if existing is None:

            db_question = InterviewQuestion(
                session_id=session_id,
                question_number=question_number,
                question=question,
                day=day,
            )

            db.add(db_question)
            db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# =====================================================
# ADD ANSWER
# =====================================================

def add_answer(
    session_id,
    answer,
):

    session = get_session(session_id)

    if session is None:

        raise ValueError(
            f"Interview session not found: {session_id}"
        )

    question_number = len(
        session["answers"]
    ) + 1

    session["answers"].append(
        answer
    )

    db = SessionLocal()

    try:

        db_question = (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.session_id
                == session_id,
                InterviewQuestion.question_number
                == question_number,
            )
            .first()
        )

        if db_question:

            db_question.answer = answer

            db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# =====================================================
# ADD EVALUATION
# =====================================================

def add_evaluation(
    session_id,
    evaluation,
):

    session = get_session(session_id)

    if session is None:

        raise ValueError(
            f"Interview session not found: {session_id}"
        )

    session["evaluations"].append(
        evaluation
    )

    question_number = len(
        session["evaluations"]
    )

    db = SessionLocal()

    try:

        db_question = (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.session_id
                == session_id,
                InterviewQuestion.question_number
                == question_number,
            )
            .first()
        )

        if db_question:

            score = None

            if isinstance(
                evaluation,
                dict,
            ):

                nested = evaluation.get(
                    "evaluation"
                )

                if isinstance(
                    nested,
                    dict,
                ):

                    score = nested.get(
                        "score"
                    )

                else:

                    score = evaluation.get(
                        "score"
                    )

            if score is not None:

                try:

                    db_question.score = int(
                        float(score)
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    db_question.score = None

            db_question.evaluation = json.dumps(
                evaluation,
                default=str,
            )

            db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# =====================================================
# CALCULATE FINAL SCORE
# =====================================================

def calculate_final_score(
    session_id,
):

    db = SessionLocal()

    try:

        questions = (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.session_id
                == session_id
            )
            .all()
        )

        scores = [
            question.score
            for question in questions
            if question.score is not None
        ]

        if not scores:
            return None

        return round(
            sum(scores) / len(scores)
        )

    finally:

        db.close()


# =====================================================
# MARK INTERVIEW COMPLETE
# =====================================================

def mark_interview_complete(
    session_id,
    final_score=None,
):

    session = get_session(
        session_id
    )

    if session:

        session["done"] = True

    if final_score is None:

        final_score = calculate_final_score(
            session_id
        )

    db = SessionLocal()

    try:

        interview = (
            db.query(Interview)
            .filter(
                Interview.session_id
                == session_id
            )
            .first()
        )

        if interview:

            interview.completed = True
            interview.status = "completed"
            interview.final_score = final_score

            db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# =====================================================
# CHECK COMPLETION
# =====================================================

def is_interview_complete(
    session_id,
):

    session = get_session(
        session_id
    )

    if session is None:
        return False

    return (
        len(
            session.get(
                "questions_asked",
                [],
            )
        )
        >= INTERVIEW_QUESTION_COUNT
    )

