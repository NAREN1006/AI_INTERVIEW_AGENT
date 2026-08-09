from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from database import Base


# =====================================================
# INTERVIEW
# =====================================================

class Interview(Base):

    __tablename__ = "interviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    candidate_name = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        default="in_progress"
    )

    final_score = Column(
        Integer,
        nullable=True
    )

    completed = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =====================================================
# INTERVIEW QUESTIONS
# =====================================================

class InterviewQuestion(Base):

    __tablename__ = "interview_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        String,
        ForeignKey("interviews.session_id"),
        nullable=False
    )

    question_number = Column(
        Integer,
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    day = Column(
        Integer,
        nullable=True
    )

    answer = Column(
        Text,
        nullable=True
    )

    score = Column(
        Integer,
        nullable=True
    )

    evaluation = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )