from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
import uvicorn

from evaluator import AdmissionsEvaluator

app = FastAPI(title="College Admissions Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"
    TRANSGENDER_MALE = "Transgender Male"
    TRANSGENDER_FEMALE = "Transgender Female"
    GENDERQUEER = "Genderqueer"
    PREFER_NOT_TO_SAY = "Prefer not to say"
    OTHER = "Other"

class APCourse(BaseModel):
    subject: str = Field(description="AP course name (e.g., 'AP Calculus BC')")
    score: int = Field(ge=1, le=5, description="AP exam score (1-5)")
    year_taken: str = Field(description="Year taken (e.g., '10th', '11th', '12th')")

class ExtracurricularActivity(BaseModel):
    activity_name: str
    role: str = Field(description="Your role/position")
    years_participated: float = Field(ge=0, le=4, description="Number of years")
    hours_per_week: int = Field(ge=0, description="Average hours per week")
    description: str = Field(description="Brief description of involvement and impact")

class Competition(BaseModel):
    name: str
    level: str = Field(description="school, regional, state, national, or international")
    award: str = Field(description="Specific award/placement")
    year: str

class ApplicationRound(str, Enum):
    ED = "Early Decision (ED)"
    ED1 = "Early Decision I (ED1)"
    ED2 = "Early Decision II (ED2)"
    EA = "Early Action (EA)"
    REA = "Restrictive Early Action (REA)"
    SCEA = "Single-Choice Early Action (SCEA)"
    RD = "Regular Decision (RD)"
    ROLLING = "Rolling Admission"

class ApplicantData(BaseModel):
    # Basic Information
    country: str
    state_province: str = Field(description="State (US) or Province/Region")
    city: str
    gender: Gender
    ethnicity: List[str] = Field(description="e.g., ['Asian', 'White', 'Hispanic/Latino', 'Black/African American', 'Native American', 'Pacific Islander', 'Other']")
    first_generation: bool = Field(description="First generation college student")
    legacy_status: bool = Field(description="Parent(s) attended target school")
    recruited_athlete: bool = Field(description="Recruited athlete status")

    target_school: str
    target_major: str = Field(description="Specific major (e.g., 'Computer Science - Artificial Intelligence', 'Biology - Pre-Med')")
    target_degree: str = Field(description="Bachelor of Arts or Bachelor of Science")
    application_round: ApplicationRound = Field(description="Application round/deadline type")

    # Socioeconomic
    family_income_bracket: str = Field(description="<$30k, $30k-$75k, $75k-$150k, $150k-$250k, >$250k")
    fee_waiver: bool = Field(description="Received application fee waiver")

    # High School Information
    high_school_name: str
    high_school_type: str = Field(description="public, private, charter, international, homeschool")
    high_school_ranking: Optional[str] = Field(None, description="If known: top 1%, top 5%, top 10%, etc.")
    class_size: Optional[int] = Field(None, description="Total students in graduating class")
    class_rank: Optional[int] = Field(None, description="Your rank in class")

    # Academic Metrics
    gpa_unweighted: float = Field(ge=0.0, le=4.0)
    gpa_weighted: Optional[float] = Field(None, ge=0.0, le=5.0)
    gpa_trend: str = Field(description="upward, stable, or downward")
    gpa_by_year: Dict[str, float] = Field(description="GPA for each year, e.g., {'9th': 3.7, '10th': 3.85, '11th': 3.95, '12th': 4.0}")

    ap_courses: List[APCourse] = Field(description="List of AP courses with details")
    honors_courses: int = Field(ge=0, description="Number of honors courses taken")
    ib_diploma: bool = Field(description="Pursuing IB Diploma")
    ib_score: Optional[int] = Field(None, ge=0, le=45, description="IB predicted/final score")

    sat_score: Optional[int] = Field(None, ge=400, le=1600)
    sat_math: Optional[int] = Field(None, ge=200, le=800)
    sat_ebrw: Optional[int] = Field(None, ge=200, le=800)
    act_score: Optional[int] = Field(None, ge=1, le=36)

    sat_subject_tests: List[Dict[str, int]] = Field(default=[], description="e.g., [{'Math II': 800}, {'Physics': 780}]")

    toefl_score: Optional[int] = Field(None, ge=0, le=120)
    ielts_score: Optional[float] = Field(None, ge=0.0, le=9.0)
    duolingo_score: Optional[int] = Field(None, ge=10, le=160)

    curriculum_difficulty: str = Field(description="low, medium, high, very_high")

    # Research & Academic Interests
    research_experience: str = Field(description="Detailed description of research")
    research_publications: List[str] = Field(default=[], description="List of publications with details")
    research_presentations: List[str] = Field(default=[], description="Conference presentations")
    independent_projects: List[str] = Field(default=[], description="Independent academic projects")

    # Extracurriculars
    extracurriculars: List[ExtracurricularActivity]

    # Competitions and Awards
    competitions: List[Competition]
    academic_honors: List[str] = Field(default=[], description="Academic honors (National Merit, AP Scholar, etc.)")

    # Work Experience
    work_experience: List[str] = Field(default=[], description="Jobs, internships")

    # Community Service
    community_service_hours: int = Field(ge=0)
    community_service_description: str

    # Summer Activities
    summer_activities: List[str] = Field(description="Summer programs, camps, courses, jobs")

    # Application Materials
    lor_quality: int = Field(ge=1, le=5, description="Letter of recommendation quality (1-5)")
    lor_sources: List[str] = Field(description="e.g., ['Math Teacher', 'Research Mentor', 'Counselor']")
    essay_quality: int = Field(ge=1, le=5, description="Essay quality (1-5)")
    essay_topics: List[str] = Field(description="Brief description of essay topics")
    supplemental_materials: List[str] = Field(default=[], description="Portfolio, art samples, etc.")

    # Demonstrated Interest
    campus_visit: bool
    interview_completed: bool
    contacted_admissions: bool
    attended_info_sessions: int = Field(ge=0)

class AdmissionResult(BaseModel):
    decision: str
    admission_probability: float
    reasoning: List[str]
    detailed_analysis: Dict[str, str]
    strengths: List[str]
    weaknesses: List[str]
    score_breakdown: dict
    advice: List[str]
    fit_analysis: Dict[str, str]

evaluator = AdmissionsEvaluator()

@app.post("/evaluate", response_model=AdmissionResult)
async def evaluate_applicant(applicant: ApplicantData):
    result = evaluator.evaluate(applicant)
    return result

@app.get("/schools")
async def get_schools():
    return evaluator.get_available_schools()

@app.get("/")
async def root():
    return {"message": "College Admissions Simulator API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
