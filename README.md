# US College Admissions Simulator

A comprehensive web application that simulates the US college admissions process using a holistic review model. The system evaluates applicants based on academic metrics, extracurricular activities, application materials, and demographic factors to provide admission probability estimates.

## Features

- **Holistic Evaluation**: Considers GPA, SAT/ACT, AP courses, research, extracurriculars, competitions, essays, and letters of recommendation
- **Detailed Analysis**: Provides strengths, weaknesses, and specific reasoning for admission decisions
- **Multiple Universities**: Pre-loaded with data for top US universities (Harvard, Stanford, MIT, UC Berkeley, UCLA, etc.)
- **Trend Analysis**: Accounts for GPA trends and curriculum difficulty
- **International Support**: Includes TOEFL/IELTS scoring for international applicants
- **Score Breakdown**: Shows detailed scoring across academic, extracurricular, application, and demographic categories

## Technology Stack

**Backend:**
- Python 3.8+
- FastAPI
- Pydantic for data validation
- NumPy for calculations

**Frontend:**
- React 18
- Axios for API calls
- Modern CSS with responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. Navigate to the project root directory:
```bash
cd CollegeSimulator
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

## Usage

1. **Fill out the application form** with your academic information:
   - Basic info (region, sex, target school and major)
   - Academic metrics (GPA, SAT, AP courses, etc.)
   - Research experience and extracurriculars
   - Competition awards
   - Application material quality ratings

2. **Submit for evaluation** - The system will analyze your profile

3. **Review results** including:
   - Admission decision category (Likely Admit, Possible, Reach, Unlikely)
   - Numerical admission probability
   - Detailed reasoning
   - Your strengths and weaknesses
   - Score breakdown by category

## API Endpoints

### `POST /evaluate`
Evaluates an applicant's profile and returns admission prediction.

**Request Body:**
```json
{
  "region": "Northeast",
  "sex": "Female",
  "target_school": "MIT",
  "target_major": "Computer Science",
  "gpa": 3.95,
  "gpa_trend": "upward",
  "ap_courses": 12,
  "ap_scores": [5, 5, 4, 5, 5],
  "sat_score": 1560,
  "toefl_score": null,
  "ielts_score": null,
  "curriculum_difficulty": "very_high",
  "research_experience": "Published paper in machine learning conference...",
  "extracurriculars": ["President of Robotics Club", "Varsity Tennis Captain"],
  "competitions": ["USACO Gold Division", "Intel ISEF Finalist"],
  "lor_quality": 5,
  "essay_quality": 4
}
```

**Response:**
```json
{
  "decision": "Likely Admit",
  "admission_probability": 0.723,
  "reasoning": ["MIT has an acceptance rate of 4.0%...", "Your profile is highly competitive..."],
  "strengths": ["Strong GPA (3.95) meets or exceeds school average", "Excellent SAT score..."],
  "weaknesses": [],
  "score_breakdown": {
    "academic": 92.5,
    "extracurricular": 85.0,
    "application": 90.0,
    "demographic": 60.0,
    "total": 86.4
  }
}
```

### `GET /schools`
Returns list of available schools in the database.

## Evaluation Model

The simulator uses a weighted scoring system:

- **Academic (45%)**: GPA, SAT/ACT, AP courses, curriculum difficulty, grade trends
- **Extracurricular (30%)**: Research, activities, leadership, competitions
- **Application Materials (20%)**: Essay quality, letter of recommendation strength
- **Demographics (5%)**: Geographic diversity, gender balance in STEM

The model adjusts probabilities based on school selectivity and considers fine-grained details like:
- Upward vs downward GPA trends
- Curriculum difficulty level
- Leadership positions in activities
- Prestigious competition recognition
- International student language proficiency

## Customization

### Adding More Schools

Edit `backend/evaluator.py` and add entries to the `_load_schools_data()` method:

```python
"Your University": {
    "acceptance_rate": 0.15,
    "avg_gpa": 3.85,
    "sat_range": (1300, 1500),
    "selectivity": "highly_competitive"
}
```

### Adjusting Weights

Modify the weights in `backend/evaluator.py` in the `evaluate()` method:

```python
total_score = (
    academic_score * 0.45 +      # Adjust these weights
    extracurricular_score * 0.30 +
    application_score * 0.20 +
    demographic_score * 0.05
)
```

## Limitations

- This is a **simulation tool** for educational purposes
- Results are estimates based on statistical models, not actual admissions decisions
- Real college admissions involve many subjective factors not captured by algorithms
- The model uses publicly available aggregate data, not actual admissions data
- Individual circumstances and holistic review factors vary significantly

## Future Enhancements

- Machine learning model trained on real data (if available)
- More universities and colleges
- Financial aid estimation
- Application timeline planning
- Comparison across multiple schools
- Historical trends analysis
- Essay feedback system

## License

This project is for educational purposes only.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
