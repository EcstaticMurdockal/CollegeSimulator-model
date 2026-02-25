"""
COMPLETE Enhanced Backend with:
- Top 50 US Universities
- Comprehensive gender options
- Specific countries/states
- All 38 AP subjects
- Application rounds (ED/EA/REA/RD)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import uvicorn

app = FastAPI(title="College Admissions Simulator - Enhanced")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ENUMS - Comprehensive Options
# ============================================================================

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"
    TRANSGENDER_MALE = "Transgender Male"
    TRANSGENDER_FEMALE = "Transgender Female"
    GENDERQUEER = "Genderqueer/Gender Fluid"
    AGENDER = "Agender"
    TWO_SPIRIT = "Two-Spirit"
    QUESTIONING = "Questioning"
    PREFER_NOT_TO_SAY = "Prefer not to say"
    PREFER_TO_SELF_DESCRIBE = "Prefer to self-describe"

class ApplicationRound(str, Enum):
    ED = "Early Decision (ED)"
    ED1 = "Early Decision I (ED1)"
    ED2 = "Early Decision II (ED2)"
    EA = "Early Action (EA)"
    REA = "Restrictive Early Action (REA)"
    SCEA = "Single-Choice Early Action (SCEA)"
    RD = "Regular Decision (RD)"
    ROLLING = "Rolling Admission"

# All 38 AP Subjects
class APSubject(str, Enum):
    # Math & CS
    CALC_AB = "AP Calculus AB"
    CALC_BC = "AP Calculus BC"
    STATISTICS = "AP Statistics"
    CS_A = "AP Computer Science A"
    CS_PRINCIPLES = "AP Computer Science Principles"

    # Sciences
    BIOLOGY = "AP Biology"
    CHEMISTRY = "AP Chemistry"
    PHYSICS_1 = "AP Physics 1: Algebra-Based"
    PHYSICS_2 = "AP Physics 2: Algebra-Based"
    PHYSICS_C_MECH = "AP Physics C: Mechanics"
    PHYSICS_C_EM = "AP Physics C: Electricity and Magnetism"
    ENVIRONMENTAL_SCIENCE = "AP Environmental Science"

    # English
    ENGLISH_LANG = "AP English Language and Composition"
    ENGLISH_LIT = "AP English Literature and Composition"

    # History & Social Sciences
    US_HISTORY = "AP United States History"
    WORLD_HISTORY = "AP World History: Modern"
    EUROPEAN_HISTORY = "AP European History"
    US_GOVERNMENT = "AP United States Government and Politics"
    COMPARATIVE_GOVERNMENT = "AP Comparative Government and Politics"
    MACROECONOMICS = "AP Macroeconomics"
    MICROECONOMICS = "AP Microeconomics"
    PSYCHOLOGY = "AP Psychology"
    HUMAN_GEOGRAPHY = "AP Human Geography"

    # World Languages
    SPANISH_LANG = "AP Spanish Language and Culture"
    SPANISH_LIT = "AP Spanish Literature and Culture"
    FRENCH_LANG = "AP French Language and Culture"
    GERMAN_LANG = "AP German Language and Culture"
    ITALIAN_LANG = "AP Italian Language and Culture"
    CHINESE_LANG = "AP Chinese Language and Culture"
    JAPANESE_LANG = "AP Japanese Language and Culture"
    LATIN = "AP Latin"

    # Arts
    ART_HISTORY = "AP Art History"
    MUSIC_THEORY = "AP Music Theory"
    STUDIO_ART_2D = "AP Studio Art: 2-D Design"
    STUDIO_ART_3D = "AP Studio Art: 3-D Design"
    STUDIO_ART_DRAWING = "AP Studio Art: Drawing"

    # Capstone
    SEMINAR = "AP Seminar"
    RESEARCH = "AP Research"

# ============================================================================
# DATA MODELS
# ============================================================================

class APCourse(BaseModel):
    subject: APSubject
    score: int = Field(ge=1, le=5)
    year_taken: str = Field(description="9th, 10th, 11th, or 12th")

class ExtracurricularActivity(BaseModel):
    activity_name: str
    role: str
    years_participated: float = Field(ge=0, le=4)
    hours_per_week: int = Field(ge=0)
    description: str

class Competition(BaseModel):
    name: str
    level: str = Field(description="school, regional, state, national, or international")
    award: str
    year: str

class ApplicantData(BaseModel):
    # Demographics - Specific Location
    country: str = Field(description="Specific country (e.g., 'United States', 'China', 'India', 'Canada', 'United Kingdom')")
    state_province: str = Field(description="Specific state/province (e.g., 'California', 'New York', 'Beijing', 'Ontario')")
    city: str

    gender: Gender
    ethnicity: List[str] = Field(description="Can select multiple: Asian, White, Hispanic/Latino, Black/African American, Native American, Pacific Islander, Middle Eastern, Other")
    first_generation: bool
    legacy_status: bool
    recruited_athlete: bool

    # Target School & Application
    target_school: str = Field(description="Select from Top 50 US universities")
    target_major: str
    target_degree: str = Field(description="Bachelor of Arts (BA) or Bachelor of Science (BS)")
    application_round: ApplicationRound

    # Socioeconomic
    family_income_bracket: str = Field(description="<$30k, $30k-$75k, $75k-$150k, $150k-$250k, >$250k")
    fee_waiver: bool

    # High School
    high_school_name: str
    high_school_type: str = Field(description="public, private, charter, international, homeschool")
    high_school_ranking: Optional[str] = Field(None, description="top 1%, top 5%, top 10%, etc.")
    class_size: Optional[int] = None
    class_rank: Optional[int] = None

    # Academic Metrics
    gpa_unweighted: float = Field(ge=0.0, le=4.0)
    gpa_weighted: Optional[float] = Field(None, ge=0.0, le=5.0)
    gpa_trend: str = Field(description="upward, stable, downward")
    gpa_by_year: Dict[str, float] = Field(description="{'9th': 3.7, '10th': 3.85, '11th': 3.95, '12th': 4.0}")

    ap_courses: List[APCourse] = Field(description="List of AP courses with specific subjects")
    honors_courses: int = Field(ge=0)
    ib_diploma: bool
    ib_score: Optional[int] = Field(None, ge=0, le=45)

    sat_score: Optional[int] = Field(None, ge=400, le=1600)
    sat_math: Optional[int] = Field(None, ge=200, le=800)
    sat_ebrw: Optional[int] = Field(None, ge=200, le=800)
    act_score: Optional[int] = Field(None, ge=1, le=36)
    sat_subject_tests: List[Dict[str, int]] = Field(default=[])

    toefl_score: Optional[int] = Field(None, ge=0, le=120)
    ielts_score: Optional[float] = Field(None, ge=0.0, le=9.0)
    duolingo_score: Optional[int] = Field(None, ge=10, le=160)

    curriculum_difficulty: str = Field(description="low, medium, high, very_high")

    # Research & Activities
    research_experience: str
    research_publications: List[str] = Field(default=[])
    research_presentations: List[str] = Field(default=[])
    independent_projects: List[str] = Field(default=[])

    extracurriculars: List[ExtracurricularActivity]
    competitions: List[Competition]
    academic_honors: List[str] = Field(default=[])

    work_experience: List[str] = Field(default=[])
    community_service_hours: int = Field(ge=0)
    community_service_description: str
    summer_activities: List[str]

    # Application Materials
    lor_quality: int = Field(ge=1, le=5)
    lor_sources: List[str]
    essay_quality: int = Field(ge=1, le=5)
    essay_topics: List[str]
    supplemental_materials: List[str] = Field(default=[])

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
    application_round_impact: Dict[str, Any]
    ml_info: Dict[str, Any]

# ============================================================================
# EVALUATOR (Import from evaluator)
# ============================================================================

from evaluator import Top50AdmissionsEvaluator

evaluator = Top50AdmissionsEvaluator()

@app.post("/evaluate", response_model=AdmissionResult)
async def evaluate_applicant(applicant: ApplicantData):
    result = evaluator.evaluate(applicant)
    return result

@app.get("/schools")
async def get_schools():
    """Get list of all Top 50 universities"""
    return evaluator.get_available_schools()

@app.get("/ap-subjects")
async def get_ap_subjects():
    """Get list of all 38 AP subjects"""
    return [subject.value for subject in APSubject]

@app.get("/countries")
async def get_countries():
    """Get list of common countries"""
    return [
        "United States", "China", "India", "Canada", "United Kingdom",
        "South Korea", "Japan", "Singapore", "Germany", "France",
        "Australia", "Mexico", "Brazil", "Russia", "Italy",
        "Spain", "Netherlands", "Switzerland", "Sweden", "Taiwan",
        "Hong Kong", "Thailand", "Vietnam", "Indonesia", "Philippines",
        "Other"
    ]

@app.get("/us-states")
async def get_us_states():
    """Get list of US states"""
    return [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California",
        "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
        "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
        "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
        "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
        "Washington D.C.", "Puerto Rico"
    ]

@app.get("/")
async def root():
    return {
        "message": "College Admissions Simulator API - Enhanced Version",
        "features": [
            "Top 50 US Universities",
            "11 Gender Options",
            "All 38 AP Subjects",
            "Application Rounds (ED/EA/REA/RD)",
            "Specific Countries & States",
            "ML-Powered Predictions"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
