import os
import google.generativeai as genai
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

# This lifespan function will run on application startup.
# This is the correct place to create the database tables.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created.")
    yield
    print("Application shutdown...")

# --- Configuration ---
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    model = None

# --- Data Models ---
class Problem(BaseModel):
    text: str

class AnalysisReport(BaseModel):
    diagnostic_question: str
    root_cause_analysis: str
    foresight_prediction: str

# --- FastAPI App ---
# We pass the lifespan function to the FastAPI app here.
app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"Hello": "Stealth Seekers Foresight Engine is Online"}

@app.post("/analyze", response_model=AnalysisReport)
async def analyze_problem(problem: Problem, db: Session = Depends(get_db)):
    if not model:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured on the server.")

    try:
        # --- PROMPT CHAIN ---
        prompt1 = f"You are a world-class business consultant... Client's problem: '{problem.text}'"
        diagnostic_response = model.generate_content(prompt1)
        diagnostic_question = diagnostic_response.text.strip()

        prompt2 = f"A client's problem is '{problem.text}'... Based on this, what are the top 2-3 likely underlying root causes...?"
        root_cause_response = model.generate_content(prompt2)
        root_cause_analysis = root_cause_response.text.strip()

        prompt3 = f"A client's problem is '{problem.text}'... predict one significant, negative business outcome..."
        foresight_response = model.generate_content(prompt3)
        foresight_prediction = foresight_response.text.strip()
        
        # --- SAVE TO DATABASE ---
        db_report = models.Report(
            client_problem=problem.text,
            diagnostic_question=diagnostic_question,
            root_cause_analysis=root_cause_analysis,
            foresight_prediction=foresight_prediction,
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)

        return AnalysisReport(
            diagnostic_question=diagnostic_question,
            root_cause_analysis=root_cause_analysis,
            foresight_prediction=foresight_prediction,
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during AI analysis: {str(e)}")
# Test commit for Cloud Build trigger
