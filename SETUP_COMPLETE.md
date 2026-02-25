# College Admissions Simulator - Enhanced Version

## ✅ Implementation Complete

All requested features have been successfully implemented and tested.

## Features Implemented

### 1. Top 50+ Universities (53 total)
- Complete data for all schools including:
  - Acceptance rates
  - GPA ranges (unweighted & weighted)
  - SAT/ACT ranges (25th-75th percentile)
  - Available application rounds
  - Demonstrated interest policies
  - Need-blind status

**Sample Schools:**
- Princeton University, MIT, Harvard, Stanford, Yale
- University of Pennsylvania, Caltech, Duke, Johns Hopkins
- Northwestern, Brown, Cornell, Dartmouth, Columbia
- And 40 more top universities...

### 2. Comprehensive Gender Options (11 options)
- Male
- Female
- Non-binary
- Transgender Male
- Transgender Female
- Genderqueer/Gender Fluid
- Agender
- Two-Spirit
- Questioning
- Prefer not to say
- Prefer to self-describe

### 3. All 38 AP Subjects
Complete enumeration across all categories:
- **Math & CS (5):** Calculus AB/BC, Statistics, CS A, CS Principles
- **Sciences (8):** Biology, Chemistry, Physics 1/2/C, Environmental Science
- **English (2):** Language & Composition, Literature & Composition
- **History & Social Sciences (9):** US/World/European History, Government, Economics, Psychology, Human Geography
- **World Languages (8):** Spanish, French, German, Italian, Chinese, Japanese, Latin
- **Arts (5):** Art History, Music Theory, Studio Art (2-D, 3-D, Drawing)
- **Capstone (2):** Seminar, Research

### 4. Specific Geographic Locations
- **26 Countries:** United States, China, India, Canada, UK, South Korea, Japan, and more
- **52 US States/Territories:** All 50 states + DC + Puerto Rico
- **City field:** For precise location

### 5. Application Rounds with Impact
- **ED (Early Decision):** Binding, 3.0x boost
- **ED1/ED2:** Two ED rounds, 3.0x and 2.0x boost
- **REA (Restrictive Early Action):** Non-binding, 2.5x boost
- **SCEA (Single-Choice Early Action):** Non-binding, 2.5x boost
- **EA (Early Action):** Non-binding, 1.5x boost
- **RD (Regular Decision):** Baseline, 1.0x
- **Rolling:** Slight boost if early, 1.2x

School-specific round availability (e.g., Harvard/Stanford/Yale only offer REA, not ED)

## How to Run

### Option 1: Using the run script (Recommended)
```bash
cd backend
python run_server.py
```

### Option 2: Direct execution
```bash
cd backend
python main.py
```

The server will automatically try port 8000, and if occupied, will use port 8001.

## API Endpoints

Once running, the API is available at `http://localhost:8000` (or 8001):

- `GET /` - API information and features
- `GET /schools` - List all 53 universities
- `GET /ap-subjects` - List all 38 AP subjects
- `GET /countries` - List all 26 countries
- `GET /us-states` - List all 52 US states/territories
- `POST /evaluate` - Evaluate applicant profile
- `GET /docs` - Interactive API documentation (Swagger UI)

## Testing

All endpoints have been tested and verified:
- ✅ 53 universities loaded
- ✅ 38 AP subjects available
- ✅ 11 gender options
- ✅ 8 application rounds
- ✅ 26 countries
- ✅ 52 states/territories
- ✅ Evaluation logic working with application round multipliers

## Files Modified

1. **backend/main.py** - Enhanced with all new features
2. **backend/evaluator.py** - Complete Top 50 evaluator with all calculation methods
3. **backend/run_server.py** - New startup script (created)

## Backup Files

Original files backed up as:
- `backend/main_old_backup.py`
- `backend/evaluator_old_backup.py`

## Current Status

✅ **FULLY FUNCTIONAL** - Server is running on port 8001 with all enhancements active.

To verify, visit:
- http://localhost:8001/ (API info)
- http://localhost:8001/docs (Interactive documentation)
- http://localhost:8001/schools (See all 53 universities)
