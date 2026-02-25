# Data Collection and ML Training System

## Available Data Sources

Based on research, here are the publicly available data sources we can use:

### 1. Graduate Admissions Dataset (Kaggle)
- **Source**: [Kaggle Graduate Admissions](https://github.com/mayur29/Kaggle_Graduate_Admissions)
- **Size**: 500 records
- **Features**: GRE Score, TOEFL Score, University Rating, SOP, LOR, CGPA, Research, Chance of Admit
- **Type**: Graduate school admissions (can be adapted)

### 2. Reddit r/collegeresults
- **Source**: [Reddit College Results](https://reddit.wellgoll.com/r/collegeresults)
- **Size**: 10,000+ self-reported posts
- **Features**: GPA, SAT/ACT, AP courses, extracurriculars, essays, decisions
- **Type**: Undergraduate admissions (perfect for our use case)
- **Tool**: [GradGPT Admits Like Me](https://www.gradgpt.com/tools/admits-like-me) uses this data

### 3. CollegeBase.org
- **Source**: [CollegeBase Applications](https://www.collegebase.org/applications)
- **Size**: 1,100+ complete applications
- **Features**: Full profiles with essays, activities, test scores, decisions
- **Type**: Real undergraduate applications
- **Access**: May require subscription

### 4. Berkeley 1973 Dataset
- **Source**: [Berkeley Graduate Admissions](https://discovery.cs.illinois.edu/dataset/berkeley/)
- **Size**: 12,763 applicants
- **Features**: Department, Gender, Admission decision
- **Type**: Historical graduate admissions

### 5. College Scorecard API
- **Source**: [US Department of Education](https://collegescorecard.ed.gov/data/)
- **Features**: Aggregate statistics, acceptance rates, demographics
- **Type**: Institutional data (not individual applicants)

## Data Collection Strategy

### Phase 1: Use Existing Datasets (Immediate)
Download and prepare publicly available datasets

### Phase 2: Web Scraping (1-2 weeks)
Scrape Reddit r/collegeresults for self-reported data

### Phase 3: Synthetic Data Augmentation (Ongoing)
Generate synthetic data to supplement real data

### Phase 4: User Contributions (Long-term)
Collect data from users of our simulator

## Implementation

I'll create:
1. Data download scripts
2. Data preprocessing pipeline
3. ML model training code
4. Model evaluation and validation
5. Integration with the backend API
