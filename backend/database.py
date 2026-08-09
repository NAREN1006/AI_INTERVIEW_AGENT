from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# =====================================================
# DATABASE CONFIGURATION
# =====================================================

DATABASE_URL = "sqlite:///./interview.db"


# =====================================================
# DATABASE ENGINE
# =====================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# =====================================================
# BASE MODEL
# =====================================================

Base = declarative_base()


# =====================================================
# DATABASE SESSION
# =====================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =====================================================
# INITIALIZE DATABASE
# =====================================================

def init_database():

    Base.metadata.create_all(
        bind=engine
    )