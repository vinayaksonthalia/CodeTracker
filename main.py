from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional
import enum

# ==========================================
# Database Configuration
# ==========================================
# We use SQLite for simplicity. It stores data in a local file 'codetracker.db'.
SQLALCHEMY_DATABASE_URL = "sqlite:///./codetracker.db"

# Create the SQLAlchemy engine that will communicate with the SQLite database.
# connect_args={"check_same_thread": False} is needed only for SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class will be a database session factory. Each instance is a DB session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy models to inherit from.
Base = declarative_base()

# ==========================================
# SQLAlchemy Models (Database Structure)
# ==========================================
class DifficultyEnum(str, enum.Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

class Problem(Base):
    """
    SQLAlchemy model representing the 'problems' table in the database.
    """
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    difficulty = Column(SQLEnum(DifficultyEnum), nullable=False)
    pattern = Column(String, nullable=True)  # e.g., Sliding Window, Two Pointers
    language = Column(String, default="C++")
    notes = Column(Text, nullable=True)
    link = Column(String, nullable=True)

# Create all tables in the database (if they don't exist yet).
Base.metadata.create_all(bind=engine)

# ==========================================
# Pydantic Schemas (Data Validation)
# ==========================================
class ProblemBase(BaseModel):
    """
    Base schema containing common attributes for a problem.
    Used to validate data coming into and going out of the API.
    """
    title: str = Field(..., description="Title of the problem")
    difficulty: DifficultyEnum = Field(..., description="Difficulty: Easy, Medium, or Hard")
    pattern: Optional[str] = Field(None, description="Algorithm pattern (e.g., Sliding Window)")
    language: str = Field(default="C++", description="Language used to solve")
    notes: Optional[str] = Field(None, description="Personal notes or explanations")
    link: Optional[str] = Field(None, description="URL to the problem")

class ProblemCreate(ProblemBase):
    """
    Schema for creating a new problem. Inherits from ProblemBase.
    (Kept separate in case creation needs different fields later).
    """
    pass

class ProblemResponse(ProblemBase):
    """
    Schema for sending problem data back to the client.
    Includes the auto-generated database ID.
    """
    id: int

    class Config:
        # Pydantic V2 config to read data even if it is an ORM model
        from_attributes = True

# ==========================================
# FastAPI Application & Middleware
# ==========================================
app = FastAPI(
    title="CodeTracker API",
    description="A simple API to track coding problems solved.",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests from frontends (e.g., React, Vue).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. In production, specify exact frontend URLs.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ==========================================
# Dependencies
# ==========================================
def get_db():
    """
    Dependency function to yield a database session for each request.
    Ensures the session is safely closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# API Routes
# ==========================================
@app.post("/problems", response_model=ProblemResponse, status_code=201)
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    """
    Create a new problem log.
    - Validates incoming data using ProblemCreate schema.
    - Converts it to a SQLAlchemy model and saves to the database.
    """
    # Use model_dump() for Pydantic V2 (or dict() for V1) to convert schema to dictionary
    db_problem = Problem(**problem.model_dump())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@app.get("/problems", response_model=List[ProblemResponse])
def read_problems(db: Session = Depends(get_db)):
    """
    Retrieve all logged problems.
    """
    problems = db.query(Problem).all()
    return problems

@app.get("/problems/{problem_id}", response_model=ProblemResponse)
def read_problem(problem_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific problem by its ID.
    Returns a 404 error if the problem is not found.
    """
    db_problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if db_problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem

@app.delete("/problems/{problem_id}", status_code=204)
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    """
    Delete a problem by its ID.
    Returns a 404 error if the problem is not found.
    """
    db_problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if db_problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db.delete(db_problem)
    db.commit()
    return None
