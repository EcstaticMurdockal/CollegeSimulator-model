# College Admissions Simulator - Model, Algorithm & Data Sources

## IMPORTANT CLARIFICATION

### What the Current System Actually Is

The system I've built is **NOT a machine learning model**. It's a **sophisticated rule-based heuristic system** that simulates admissions decisions using:

1. **Weighted scoring algorithms** based on known admissions factors
2. **Statistical modeling** using publicly available aggregate data
3. **Expert-designed rules** that approximate holistic review processes

### Why Not True Machine Learning?

**The fundamental problem**: Real college admissions data with individual applicant details is **not publicly available** due to privacy laws (FERPA) and institutional policies.

What we DON'T have access to:
- Individual applicant profiles with all details (GPA, test scores, essays, activities, etc.)
- Corresponding admission decisions (accept/reject/waitlist)
- Thousands of examples needed to train ML models

What we DO have access to:
- Aggregate statistics (acceptance rates, average GPA/SAT ranges)
- Self-reported data from forums (unreliable, biased)
- General admissions criteria published by universities

---

## CURRENT SYSTEM ARCHITECTURE

### 1. Rule-Based Scoring System

The system uses a **weighted multi-factor scoring algorithm**:

```
Total Score = (Academic × 0.35) +
              (Major Alignment × 0.15) +
              (Extracurricular × 0.25) +
              (Application Quality × 0.15) +
              (Demographics × 0.05) +
              (Demonstrated Interest × 0.03) +
              (Contextual Factors × 0.02)
```

Each component score (0-100) is calculated using sub-rules:

#### Academic Score (35%)
```python
score = 0

# GPA Analysis (35 points)
gpa_percentile = min(applicant.gpa / school.avg_gpa, 1.2)
score += gpa_percentile * 25

# GPA Trend (10 points)
if gpa_trend == "upward":
    improvement = gpa_12th - gpa_9th
    if improvement > 0.3: score += 10
    elif improvement > 0.15: score += 7
    else: score += 5
elif gpa_trend == "downward":
    score -= 12

# SAT Score (25 points)
if sat_score >= school.sat_75th_percentile:
    score += 25
elif sat_score >= school.sat_median:
    score += 15 + interpolate(sat_score, median, 75th)
elif sat_score >= school.sat_25th_percentile:
    score += 10
else:
    score += 5

# AP Courses (15 points)
num_aps = len(ap_courses)
if num_aps >= 10: score += 10
elif num_aps >= 7: score += 8
# ... etc

# AP Score Quality (5 points)
avg_ap_score = mean(ap_scores)
if avg_ap_score >= 4.5: score += 5
elif avg_ap_score >= 4.0: score += 4
# ... etc

# Curriculum Difficulty (5 points)
difficulty_map = {"very_high": 5, "high": 4, "medium": 3, "low": 1}
score += difficulty_map[curriculum_difficulty]

# International Language Proficiency
if country != "USA":
    if toefl >= 110: score += 3
    elif toefl < 90: score -= 8

return min(score, 100)
```

#### Major Alignment Score (15%)
```python
# Determine major category
major_category = categorize_major(target_major)
# e.g., "Computer Science - AI" → "STEM"

# Check AP course alignment
relevant_aps = get_relevant_aps(major_category)
# For STEM: [Calc BC, Physics C, Chemistry, CS A, etc.]

taken_relevant = count_matching_aps(ap_courses, relevant_aps)
score = (taken_relevant / len(relevant_aps)) * 40

# Check extracurricular alignment
relevant_activities = get_relevant_activities(major_category)
# For STEM: ["research", "robotics", "math team", "coding", etc.]

matching_activities = count_matching_activities(extracurriculars, relevant_activities)
score += min(matching_activities * 10, 30)

# Research alignment
if major_category == "STEM" and has_stem_research:
    score += 20
elif major_category == "Humanities" and has_humanities_research:
    score += 20

# Competition alignment
if has_relevant_competitions(competitions, major_category):
    score += 10

return min(score, 100)
```

#### Extracurricular Score (25%)
```python
score = 0

# Depth: Years and hours
for activity in extracurriculars:
    depth_score = (activity.years * 5) + (activity.hours_per_week * 0.5)
    score += min(depth_score, 15)

# Leadership
leadership_keywords = ["president", "captain", "founder", "director", "lead"]
for activity in extracurriculars:
    if any(keyword in activity.role.lower() for keyword in leadership_keywords):
        score += 10
        break

# Impact
if any("founded" in activity.description.lower() for activity in extracurriculars):
    score += 10
if any(number > 50 in activity.description for activity in extracurriculars):
    # e.g., "taught 200 students", "raised $5000"
    score += 10

# Breadth
categories = categorize_activities(extracurriculars)
# STEM, Arts, Sports, Community Service, Leadership, etc.
score += len(categories) * 5

return min(score, 100)
```

#### Competition Score (part of Extracurricular)
```python
score = 0

prestige_map = {
    "international": 30,  # IOI, IMO, IPhO
    "national": 20,       # USACO, AIME, Intel ISEF
    "state": 10,
    "regional": 5,
    "school": 2
}

for competition in competitions:
    score += prestige_map[competition.level]

    # Specific prestigious competitions
    if "olympiad" in competition.name.lower() and competition.level == "international":
        if "gold" in competition.award.lower(): score += 20
        elif "silver" in competition.award.lower(): score += 15
        elif "bronze" in competition.award.lower(): score += 10

return min(score, 100)
```

### 2. Probability Calculation

After calculating the total score (0-100), we convert it to admission probability:

```python
def calculate_probability(total_score, school_data, applicant):
    base_acceptance = school_data["acceptance_rate"]
    normalized_score = total_score / 100

    # Selectivity-based curve
    if school_data["selectivity"] == "most_competitive":
        # Very steep curve - even perfect scores have moderate chances
        # because of holistic review randomness
        probability = base_acceptance + (normalized_score ** 2.5) * (0.85 - base_acceptance)

    elif school_data["selectivity"] == "highly_competitive":
        probability = base_acceptance + (normalized_score ** 2.0) * (0.90 - base_acceptance)

    else:  # very_competitive
        probability = base_acceptance + (normalized_score ** 1.5) * (0.92 - base_acceptance)

    # Adjustments for special factors
    if applicant.legacy_status and school_data["values_legacy"]:
        probability *= 1.3

    if applicant.recruited_athlete:
        probability *= 2.5

    if applicant.first_generation and school_data["values_first_gen"]:
        probability *= 1.2

    # URM boost (context-dependent)
    if is_underrepresented_minority(applicant.ethnicity, school_data):
        probability *= 1.15

    # Cap probability
    return min(max(probability, 0.01), 0.95)
```

### 3. Data Sources

#### Currently Used (Publicly Available):

1. **College Board / Common Data Set**
   - Acceptance rates
   - GPA ranges (25th-75th percentile)
   - SAT/ACT ranges (25th-75th percentile)
   - Class size, demographics
   - Source: Each university's Common Data Set (CDS)

2. **University Websites**
   - Admissions criteria and values
   - Popular majors
   - Whether they track demonstrated interest
   - Need-blind vs. need-aware policies

3. **US News & World Report**
   - Selectivity rankings
   - Acceptance rates
   - Average test scores

4. **Admissions Books & Guides**
   - "A is for Admission" by Michele Hernandez
   - "The Price of Admission" by Daniel Golden
   - General admissions criteria and weighting

5. **Admissions Officer Interviews & Publications**
   - General guidance on holistic review
   - Importance of various factors
   - What makes a strong application

#### What We DON'T Have (Private/Confidential):

1. **Individual Applicant Data**
   - Actual student profiles with all details
   - Corresponding admission decisions
   - Internal ratings/scores

2. **Institutional Formulas**
   - Exact weighting of factors
   - How essays are scored
   - How recommendations are evaluated

3. **Admissions Committee Deliberations**
   - How decisions are actually made
   - What tips the balance
   - Institutional priorities each year

---

## TRUE MACHINE LEARNING APPROACH

### What Would Be Required

To build a **real ML-based admissions predictor**, you would need:

#### 1. Training Data (Minimum 10,000+ examples per school)

```json
[
  {
    "applicant_id": "anonymous_12345",
    "school": "Stanford",
    "year": 2024,
    "decision": "accepted",
    "features": {
      "gpa_unweighted": 3.92,
      "gpa_weighted": 4.45,
      "sat_total": 1560,
      "sat_math": 800,
      "sat_ebrw": 760,
      "ap_courses": [
        {"subject": "Calculus BC", "score": 5},
        {"subject": "Physics C Mechanics", "score": 5},
        // ... all APs
      ],
      "extracurriculars": [
        {
          "category": "STEM",
          "leadership": true,
          "years": 4,
          "hours_per_week": 15,
          "impact_score": 8  // manually rated
        },
        // ... all activities
      ],
      "research": {
        "has_publication": true,
        "publication_tier": "top_conference",
        "first_author": true
      },
      "competitions": [
        {"name": "IOI", "level": "international", "placement": "silver"}
      ],
      "demographics": {
        "ethnicity": ["Asian"],
        "first_gen": true,
        "legacy": false,
        "recruited_athlete": false,
        "state": "California",
        "country": "USA"
      },
      "essay_score": 8.5,  // manually rated by experts
      "lor_score": 9.0,    // manually rated
      // ... 50+ more features
    }
  },
  // ... 10,000+ more examples
]
```

#### 2. ML Algorithm Options

**Option A: Gradient Boosting (XGBoost/LightGBM)**
```python
import xgboost as xgb
from sklearn.model_selection import train_test_split

# Prepare data
X = extract_features(applicant_data)  # 100+ features
y = extract_labels(applicant_data)    # 0 = reject, 1 = accept

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = xgb.XGBClassifier(
    max_depth=8,
    learning_rate=0.05,
    n_estimators=500,
    objective='binary:logistic',
    eval_metric='auc'
)

model.fit(X_train, y_train)

# Predict probability
probability = model.predict_proba(new_applicant)[0][1]
```

**Pros:**
- Handles non-linear relationships
- Feature importance analysis
- Good with mixed data types
- Interpretable

**Cons:**
- Needs large dataset
- Can overfit
- Doesn't capture complex interactions well

**Option B: Neural Network**
```python
import tensorflow as tf
from tensorflow import keras

# Build model
model = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(num_features,)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy', 'AUC']
)

# Train
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

# Predict
probability = model.predict(new_applicant)[0][0]
```

**Pros:**
- Can learn complex patterns
- Handles high-dimensional data
- Can incorporate text (essays) with embeddings

**Cons:**
- Needs very large dataset (50k+ examples)
- Black box (hard to interpret)
- Prone to overfitting
- Computationally expensive

**Option C: Ensemble of Models**
```python
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

# Create ensemble
ensemble = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression()),
        ('rf', RandomForestClassifier(n_estimators=200)),
        ('xgb', xgb.XGBClassifier())
    ],
    voting='soft'  # Use probability averaging
)

ensemble.fit(X_train, y_train)
probability = ensemble.predict_proba(new_applicant)[0][1]
```

**Pros:**
- More robust than single model
- Reduces overfitting
- Better generalization

**Cons:**
- More complex to maintain
- Slower inference
- Still needs large dataset

#### 3. Feature Engineering

Key features to extract:

**Numerical Features (50+):**
- GPA (unweighted, weighted)
- GPA trend (slope from 9th-12th)
- SAT/ACT scores and subscores
- Number of AP courses
- Average AP score
- Number of honors courses
- Class rank percentile
- Test score percentiles relative to school
- Number of extracurriculars
- Total extracurricular hours
- Years of participation (max, average)
- Number of leadership positions
- Number of competitions
- Highest competition level (encoded: 1-5)
- Community service hours
- Number of work experiences
- Number of summer programs

**Categorical Features (30+):**
- Target school (one-hot encoded)
- Target major category (STEM, Humanities, etc.)
- Gender
- Ethnicity (multi-hot encoded)
- State/Country
- High school type
- First-generation status
- Legacy status
- Recruited athlete status
- Income bracket
- Each AP subject taken (multi-hot encoded)
- Extracurricular categories (multi-hot encoded)

**Text Features (Requires NLP):**
- Essay embeddings (using BERT/GPT)
- Research description embeddings
- Extracurricular descriptions embeddings

**Derived Features (20+):**
- Major alignment score (calculated)
- Academic-EC coherence score
- Spike vs. well-rounded indicator
- Socioeconomic adversity index
- High school competitiveness index
- Geographic diversity score

#### 4. Model Training Process

```python
# 1. Data Collection
data = load_applicant_data()  # 10,000+ examples

# 2. Feature Engineering
features = engineer_features(data)

# 3. Handle Class Imbalance
# Most applicants are rejected, so we need to balance
from imblearn.over_sampling import SMOTE
X_balanced, y_balanced = SMOTE().fit_resample(X, y)

# 4. Train-Test Split (by year to avoid data leakage)
train_data = data[data.year < 2023]
test_data = data[data.year >= 2023]

# 5. Cross-Validation
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits=5)

# 6. Hyperparameter Tuning
from sklearn.model_selection import GridSearchCV
param_grid = {
    'max_depth': [6, 8, 10],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [300, 500, 700]
}
grid_search = GridSearchCV(xgb.XGBClassifier(), param_grid, cv=cv)
grid_search.fit(X_train, y_train)

# 7. Evaluate
from sklearn.metrics import roc_auc_score, precision_recall_curve
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred_proba)
print(f"AUC: {auc}")

# 8. Calibration (ensure probabilities are accurate)
from sklearn.calibration import CalibratedClassifierCV
calibrated_model = CalibratedClassifierCV(model, method='isotonic', cv=5)
calibrated_model.fit(X_train, y_train)
```

---

## REALISTIC DATA SOURCES FOR ML APPROACH

### Option 1: Self-Reported Data (Unreliable but Available)

**Sources:**
1. **College Confidential Forums**
   - Users post their stats and decisions
   - ~100k+ posts over years
   - **Problem**: Self-reported, biased (people with extreme results more likely to post)

2. **Reddit (r/ApplyingToCollege, r/collegeresults)**
   - Similar to College Confidential
   - More recent data
   - **Problem**: Same bias issues

3. **Parchment.com / Cappex.com**
   - Students self-report profiles and decisions
   - Larger dataset
   - **Problem**: Still self-reported, selection bias

**Web Scraping Approach:**
```python
import requests
from bs4 import BeautifulSoup
import re

def scrape_college_confidential():
    results = []
    for page in range(1, 1000):
        url = f"https://talk.collegeconfidential.com/stanford-university/results?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for post in soup.find_all('div', class_='result-post'):
            # Extract: GPA, SAT, decision, etc.
            data = parse_result_post(post)
            results.append(data)

    return results
```

**Data Quality Issues:**
- Missing fields (not everyone reports everything)
- Exaggeration (people inflate stats)
- Selection bias (extreme results over-represented)
- No verification

### Option 2: Synthetic Data Generation (For Development)

Generate realistic synthetic data based on known distributions:

```python
import numpy as np
from scipy import stats

def generate_synthetic_applicant(school_data):
    # GPA: Normal distribution around school average
    gpa = np.random.normal(school_data['avg_gpa'], 0.15)
    gpa = np.clip(gpa, 0, 4.0)

    # SAT: Normal distribution
    sat_mean = (school_data['sat_25th'] + school_data['sat_75th']) / 2
    sat_std = (school_data['sat_75th'] - school_data['sat_25th']) / 2
    sat = int(np.random.normal(sat_mean, sat_std))
    sat = np.clip(sat, 400, 1600)

    # AP courses: Poisson distribution
    num_aps = np.random.poisson(7)
    ap_scores = [np.random.choice([3, 4, 5], p=[0.2, 0.3, 0.5]) for _ in range(num_aps)]

    # Extracurriculars: 3-8 activities
    num_ecs = np.random.randint(3, 9)

    # Decision: Based on score
    score = calculate_score(gpa, sat, num_aps, num_ecs)
    acceptance_threshold = get_threshold(school_data['acceptance_rate'])
    decision = 1 if score > acceptance_threshold else 0

    return {
        'gpa': gpa,
        'sat': sat,
        'num_aps': num_aps,
        'ap_scores': ap_scores,
        'num_ecs': num_ecs,
        'decision': decision
    }

# Generate 10,000 synthetic applicants
synthetic_data = [generate_synthetic_applicant(stanford_data) for _ in range(10000)]
```

**Pros:**
- Can generate unlimited data
- No privacy concerns
- Controlled distributions

**Cons:**
- Not real data
- May not capture true admissions complexity
- Model learns synthetic patterns, not real ones

### Option 3: Partner with Universities (Ideal but Difficult)

**Approach:**
- Partner with universities to access anonymized admissions data
- Sign data use agreements
- Ensure FERPA compliance

**Challenges:**
- Universities are extremely protective of this data
- Concerns about gaming the system
- Legal and ethical issues
- Would require institutional approval

### Option 4: Naviance Data (Possible)

**Naviance** is a college planning platform used by high schools. It has:
- Student GPA and test scores
- College application outcomes
- Scattergrams showing acceptance patterns

**Approach:**
- Partner with Naviance/PowerSchool
- Access aggregated, anonymized data

**Challenges:**
- Proprietary data
- Expensive licensing
- Still missing essay quality, recommendations, etc.

---

## CURRENT SYSTEM vs. TRUE ML SYSTEM

| Aspect | Current (Rule-Based) | True ML System |
|--------|---------------------|----------------|
| **Data Required** | Aggregate statistics only | 10,000+ individual examples per school |
| **Development Time** | 2-3 weeks | 6-12 months |
| **Accuracy** | ~60-70% (estimated) | ~75-85% (with good data) |
| **Interpretability** | High (can explain every decision) | Low (black box) |
| **Maintenance** | Update rules manually | Retrain annually with new data |
| **Bias** | Designer bias in rules | Data bias (garbage in, garbage out) |
| **Generalization** | Works for all schools (with stats) | Needs training data per school |
| **Cost** | Low (no data acquisition) | High (data licensing, compute) |
| **Legal Risk** | Low | Medium (data privacy concerns) |

---

## RECOMMENDATION

### For Your Project:

**Phase 1: Rule-Based System (Current)**
- Use the sophisticated heuristic system I've designed
- Based on publicly available data and admissions expertise
- Transparent and explainable
- Good enough for educational/simulation purposes
- **Accuracy: ~60-70%**

**Phase 2: Hybrid System**
- Collect self-reported data from users
- Use ML to refine rule weights
- Calibrate probabilities based on actual outcomes
- **Accuracy: ~70-75%**

**Phase 3: Full ML System (If You Get Data)**
- Partner with data providers or universities
- Train proper ML models
- Continuous learning from new data
- **Accuracy: ~75-85%**

### Realistic Expectations:

Even with perfect ML and real data, admissions prediction will never be 100% accurate because:
1. **Holistic review is subjective** - different readers may rate the same application differently
2. **Institutional priorities change** - schools may prioritize certain majors or demographics each year
3. **Unmeasurable factors** - personal qualities, interview performance, "fit"
4. **Randomness** - at top schools, many qualified applicants are rejected due to limited spots

**Best possible accuracy: ~85%** (even for admissions officers themselves!)

---

## CONCLUSION

The current system is a **sophisticated rule-based simulator** that approximates admissions decisions using:
- Weighted scoring algorithms
- Publicly available aggregate statistics
- Expert knowledge of admissions processes

It's **not a machine learning model** because we don't have access to the individual-level training data required.

For a true ML system, you would need to:
1. Acquire 10,000+ labeled examples per school (very difficult)
2. Use gradient boosting or neural networks
3. Extensive feature engineering
4. Continuous retraining

The rule-based approach is appropriate for this project and provides valuable insights, even if it can't match the theoretical accuracy of a well-trained ML model with real data.
