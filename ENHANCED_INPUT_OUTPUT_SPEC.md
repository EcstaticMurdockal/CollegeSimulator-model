# Enhanced College Admissions Simulator - Complete Input/Output Specification

## INPUTS (What User Submits)

### 1. Basic Information
```json
{
  "country": "United States" | "China" | "India" | etc.,
  "state_province": "California" | "New York" | "Beijing" | etc.,
  "city": "San Francisco",
  "gender": "Male" | "Female" | "Non-binary" | "Transgender Male" | "Transgender Female" | "Genderqueer" | "Prefer not to say" | "Other",
  "ethnicity": ["Asian", "White", "Hispanic/Latino", "Black/African American", "Native American", "Pacific Islander", "Other"],
  "first_generation": true | false,
  "legacy_status": true | false,
  "recruited_athlete": true | false
}
```

### 2. Target School & Major
```json
{
  "target_school": "Stanford University",
  "target_major": "Computer Science - Artificial Intelligence",
  "target_degree": "Bachelor of Science" | "Bachelor of Arts"
}
```

### 3. Socioeconomic Background
```json
{
  "family_income_bracket": "<$30k" | "$30k-$75k" | "$75k-$150k" | "$150k-$250k" | ">$250k",
  "fee_waiver": true | false
}
```

### 4. High School Information
```json
{
  "high_school_name": "Example High School",
  "high_school_type": "public" | "private" | "charter" | "international" | "homeschool",
  "high_school_ranking": "top 1%" | "top 5%" | "top 10%" | "top 25%" | "top 50%" | null,
  "class_size": 450,
  "class_rank": 5
}
```

### 5. Academic Metrics - GPA
```json
{
  "gpa_unweighted": 3.92,
  "gpa_weighted": 4.45,
  "gpa_trend": "upward" | "stable" | "downward",
  "gpa_by_year": {
    "9th": 3.75,
    "10th": 3.88,
    "11th": 3.98,
    "12th": 4.0
  }
}
```

### 6. Academic Metrics - AP Courses (DETAILED)
```json
{
  "ap_courses": [
    {
      "subject": "AP Calculus BC",
      "score": 5,
      "year_taken": "11th"
    },
    {
      "subject": "AP Computer Science A",
      "score": 5,
      "year_taken": "10th"
    },
    {
      "subject": "AP Physics C: Mechanics",
      "score": 5,
      "year_taken": "11th"
    },
    {
      "subject": "AP Physics C: E&M",
      "score": 4,
      "year_taken": "12th"
    },
    {
      "subject": "AP Chemistry",
      "score": 5,
      "year_taken": "11th"
    },
    {
      "subject": "AP English Language",
      "score": 4,
      "year_taken": "11th"
    },
    {
      "subject": "AP US History",
      "score": 5,
      "year_taken": "10th"
    },
    {
      "subject": "AP Statistics",
      "score": 5,
      "year_taken": "12th"
    }
  ],
  "honors_courses": 6,
  "ib_diploma": false,
  "ib_score": null
}
```

### 7. Academic Metrics - Standardized Tests
```json
{
  "sat_score": 1560,
  "sat_math": 800,
  "sat_ebrw": 760,
  "act_score": null,
  "sat_subject_tests": [
    {"Math II": 800},
    {"Physics": 790}
  ],
  "toefl_score": 115,
  "ielts_score": null,
  "duolingo_score": null,
  "curriculum_difficulty": "very_high"
}
```

### 8. Research & Academic Projects
```json
{
  "research_experience": "Conducted independent research on neural network optimization under Professor Jane Smith at Stanford AI Lab for 18 months. Developed novel pruning algorithm that improved inference speed by 40%.",
  "research_publications": [
    "First author: 'Efficient Neural Network Pruning via Gradient-Based Importance Scoring' - Published at ICML 2024",
    "Co-author: 'Applications of Reinforcement Learning in Robotics' - NeurIPS 2024 Workshop"
  ],
  "research_presentations": [
    "Presented research at California Science Fair - 1st Place",
    "Poster presentation at Stanford AI Symposium 2024"
  ],
  "independent_projects": [
    "Built open-source machine learning library with 2000+ GitHub stars",
    "Created mobile app for accessibility - 50k+ downloads"
  ]
}
```

### 9. Extracurricular Activities (DETAILED)
```json
{
  "extracurriculars": [
    {
      "activity_name": "Robotics Team",
      "role": "Team Captain & Lead Programmer",
      "years_participated": 4,
      "hours_per_week": 15,
      "description": "Led team of 25 students to regional championships. Designed autonomous navigation system. Mentored 10 underclassmen."
    },
    {
      "activity_name": "Math Club",
      "role": "President",
      "years_participated": 3,
      "hours_per_week": 5,
      "description": "Grew club from 15 to 60 members. Organized weekly problem-solving sessions and competition prep."
    },
    {
      "activity_name": "Volunteer Coding Instructor",
      "role": "Instructor",
      "years_participated": 2,
      "hours_per_week": 4,
      "description": "Taught Python programming to 50+ underprivileged middle school students at local community center."
    }
  ]
}
```

### 10. Competitions & Awards (DETAILED)
```json
{
  "competitions": [
    {
      "name": "International Olympiad in Informatics (IOI)",
      "level": "international",
      "award": "Silver Medal",
      "year": "2024"
    },
    {
      "name": "USA Computing Olympiad (USACO)",
      "level": "national",
      "award": "Platinum Division",
      "year": "2023-2024"
    },
    {
      "name": "Google Code Jam",
      "level": "international",
      "award": "Top 500 Worldwide",
      "year": "2024"
    },
    {
      "name": "American Mathematics Competition (AMC)",
      "level": "national",
      "award": "AIME Qualifier - Score 12",
      "year": "2024"
    }
  ],
  "academic_honors": [
    "National Merit Finalist",
    "AP Scholar with Distinction",
    "Presidential Scholar Candidate",
    "National Honor Society President"
  ]
}
```

### 11. Work Experience
```json
{
  "work_experience": [
    "Software Engineering Intern at Google - Summer 2024 - Worked on TensorFlow optimization",
    "Research Assistant at Stanford AI Lab - 18 months - Neural network research",
    "Freelance Web Developer - 2 years - Built websites for 15+ small businesses"
  ]
}
```

### 12. Community Service
```json
{
  "community_service_hours": 350,
  "community_service_description": "Founded non-profit 'Code for Good' teaching programming to 200+ underprivileged students. Organized 5 hackathons raising $25k for local schools. Weekly volunteer at homeless shelter."
}
```

### 13. Summer Activities
```json
{
  "summer_activities": [
    "Stanford AI Summer Program - 8 weeks",
    "Google Computer Science Summer Institute (CSSI)",
    "MIT Launch Entrepreneurship Program",
    "Self-studied advanced machine learning - completed 5 online courses"
  ]
}
```

### 14. Application Materials
```json
{
  "lor_quality": 5,
  "lor_sources": [
    "AP Computer Science Teacher (4 years)",
    "Research Mentor - Stanford Professor",
    "School Counselor",
    "Robotics Team Coach"
  ],
  "essay_quality": 5,
  "essay_topics": [
    "Personal Statement: Overcoming learning disability through coding",
    "Why Major: How AI can solve healthcare disparities",
    "Community Essay: Building tech education in underserved areas"
  ],
  "supplemental_materials": [
    "GitHub portfolio with 15+ projects",
    "Research paper preprints",
    "Video demonstration of robotics project"
  ]
}
```

### 15. Demonstrated Interest
```json
{
  "campus_visit": true,
  "interview_completed": true,
  "contacted_admissions": true,
  "attended_info_sessions": 3
}
```

---

## OUTPUTS (What System Returns)

### 1. Decision Category
```json
{
  "decision": "Strong Admit" | "Likely Admit" | "Competitive" | "Reach" | "High Reach" | "Unlikely"
}
```

### 2. Admission Probability
```json
{
  "admission_probability": 0.742
}
```
*Interpretation: 74.2% estimated chance of admission*

### 3. Reasoning (High-Level Summary)
```json
{
  "reasoning": [
    "Stanford University has an acceptance rate of 3.5%, making it one of the most selective institutions in the world.",
    "Your profile is exceptionally strong and highly competitive for Stanford's Computer Science program.",
    "Your research experience, publications, and technical achievements demonstrate exceptional preparation for CS at the highest level.",
    "The combination of perfect technical coursework alignment, international-level competition success, and meaningful community impact creates a compelling narrative.",
    "Your upward GPA trend (3.75 → 4.0) and perfect scores in all STEM APs show strong academic trajectory.",
    "First-generation status and demonstrated commitment to educational equity add unique perspective to your application."
  ]
}
```

### 4. Detailed Analysis (Category-by-Category)
```json
{
  "detailed_analysis": {
    "academic_strength": "Exceptional. GPA of 3.92 UW / 4.45 W places you in the top tier of applicants. Your SAT score of 1560 (800M/760EBRW) is at the 75th percentile for Stanford. Perfect 800 on Math II and 790 on Physics SAT Subject Tests demonstrate mastery. The progression from 3.75 (9th) to 4.0 (12th) shows remarkable growth and resilience.",

    "curriculum_rigor": "Outstanding. 8 AP courses with average score of 4.75, including the most rigorous STEM sequence (Calc BC, Physics C Mechanics & E&M, Chemistry, CS A). Taking AP CS in 10th grade shows early specialization. Very high curriculum difficulty rating is appropriate given course load.",

    "major_alignment": "Perfect fit. Your AP coursework (Calc BC, Physics C, CS A, Chemistry, Statistics) directly aligns with CS-AI major requirements. Research in neural network optimization is highly relevant. Publications at top-tier ML conferences (ICML, NeurIPS) demonstrate graduate-level work. Independent ML projects show genuine passion beyond academics.",

    "research_quality": "Exceptional and rare for undergraduate applicant. First-author publication at ICML (acceptance rate ~20%) is remarkable. 18-month commitment to Stanford AI Lab shows sustained engagement. Novel algorithm with measurable impact (40% improvement) demonstrates real contribution to field. This level of research is typically seen in top 1% of applicants.",

    "extracurricular_depth": "Strong leadership and impact. 4-year commitment to robotics with captain role shows dedication. Growing Math Club from 15 to 60 members demonstrates leadership. Teaching coding to 50+ underprivileged students aligns with stated values. However, activities are somewhat concentrated in STEM - could benefit from more diversity.",

    "competition_achievements": "World-class. IOI Silver Medal places you among top ~100 high school programmers globally. USACO Platinum is top 200 in US. Google Code Jam Top 500 is highly selective. AIME qualification with score of 12 is strong. These achievements validate your technical abilities at the highest level.",

    "personal_narrative": "Compelling story of using technology for social good. First-generation status adds unique perspective. Founded non-profit teaching 200+ students shows initiative and impact. Essays about overcoming learning disability and addressing healthcare disparities through AI create authentic, memorable narrative. This differentiates you from other high-stats CS applicants.",

    "letters_of_recommendation": "Likely exceptional given 4-year relationship with CS teacher and research mentor who is Stanford professor. Having a Stanford faculty member vouch for your research abilities is significant advantage.",

    "demonstrated_interest": "Strong. Campus visit, interview, and multiple info sessions show genuine interest. While Stanford claims not to track demonstrated interest, engagement with community is noted.",

    "contextual_factors": "First-generation college student status is significant advantage at Stanford, which actively seeks to increase socioeconomic diversity. Coming from public high school (if applicable) provides additional context for achievements."
  }
}
```

### 5. Strengths (Specific Bullet Points)
```json
{
  "strengths": [
    "World-class competition achievements: IOI Silver Medal, USACO Platinum, Google Code Jam Top 500",
    "Exceptional research credentials: First-author ICML publication, 18-month Stanford AI Lab experience",
    "Perfect major alignment: All relevant STEM APs (Calc BC-5, Physics C-5, CS A-5, Chem-5) directly support CS-AI major",
    "Outstanding standardized testing: SAT 1560 (800M), Math II 800, Physics 790 - all at/above 75th percentile",
    "Strong upward GPA trend: 3.75 (9th) → 4.0 (12th) demonstrates growth and resilience",
    "Meaningful community impact: Founded non-profit teaching 200+ students, 350+ service hours",
    "Demonstrated leadership: Robotics Captain (4 years), Math Club President, grew club 4x",
    "First-generation college student: Adds unique perspective and aligns with Stanford's diversity goals",
    "Exceptional letters of recommendation: Stanford professor research mentor provides insider validation",
    "Authentic personal narrative: Overcoming learning disability, using AI for healthcare equity",
    "Summer enrichment: Stanford AI Program, Google CSSI, MIT Launch show initiative",
    "Technical portfolio: GitHub with 2000+ stars, mobile app with 50k+ downloads demonstrates real-world impact",
    "Early specialization: Taking AP CS in 10th grade shows early commitment to field"
  ]
}
```

### 6. Weaknesses (Areas for Improvement)
```json
{
  "weaknesses": [
    "Extracurricular activities heavily concentrated in STEM - could benefit from demonstrating broader interests (arts, humanities, sports)",
    "SAT EBRW score (760) slightly below Math (800) - while still excellent, shows relative weakness in verbal",
    "No mention of arts, music, or athletic involvement - Stanford values well-rounded students",
    "Limited international experience or language skills mentioned - could strengthen global perspective",
    "Essay quality rated 5/5 but topics are somewhat conventional for CS applicants (overcoming challenges, using tech for good) - could be more unique",
    "While research is exceptional, it's concentrated in one area (neural networks) - broader CS exposure could help",
    "Community service, while substantial, is entirely tech-focused - showing diverse interests could strengthen application"
  ]
}
```

### 7. Score Breakdown (0-100 scale for each category)
```json
{
  "score_breakdown": {
    "academic": 96.5,
    "major_alignment": 98.0,
    "extracurricular": 89.0,
    "application": 94.0,
    "demographic": 72.0,
    "demonstrated_interest": 85.0,
    "contextual": 78.0,
    "total": 91.8
  }
}
```

### 8. Advice (Actionable Recommendations)
```json
{
  "advice": [
    "IMMEDIATE ACTIONS (Before Application Deadline):",
    "• Ensure your essays tell a unique story beyond 'I love CS and want to help people' - dig deeper into specific moments, failures, and insights",
    "• Ask your Stanford research mentor to emphasize specific examples of your intellectual curiosity and problem-solving in their letter",
    "• In supplemental essays, highlight any non-STEM interests or experiences to show you're not one-dimensional",
    "• Consider submitting your ICML paper and GitHub portfolio as supplemental materials if not already included",

    "IF WAITLISTED/DEFERRED:",
    "• Send update letter highlighting any new achievements (additional publications, competition results, project launches)",
    "• Have your research mentor send an additional letter if appropriate",
    "• Demonstrate continued interest through thoughtful communication with admissions",

    "TO STRENGTHEN PROFILE (If Reapplying or for Other Schools):",
    "• Develop at least one significant non-STEM extracurricular to show breadth",
    "• Consider taking SAT again to bring EBRW closer to 800 (though 760 is already strong)",
    "• Expand research to adjacent areas (robotics, HCI, computational biology) to show versatility",
    "• Seek international research collaboration or summer program to add global dimension",

    "APPLICATION STRATEGY:",
    "• Apply to Stanford REA (Restrictive Early Action) if it's your top choice - your profile is strong enough",
    "• Also apply to: MIT, Caltech, CMU (CS), UC Berkeley (CS), Harvey Mudd as target/reach schools",
    "• Include match schools: UIUC (CS), Georgia Tech, UT Austin (CS), UW Madison",
    "• Safety schools: UC San Diego, UC Irvine, Purdue, RPI",

    "INTERVIEW PREPARATION:",
    "• Be ready to discuss your research in accessible terms - admissions officers aren't ML experts",
    "• Prepare stories about failure and learning, not just successes",
    "• Show genuine curiosity about Stanford's specific programs (CS+Social Good, AI4ALL, etc.)",
    "• Ask thoughtful questions about undergraduate research opportunities",

    "LONG-TERM (If Admitted):",
    "• Consider declaring CS+X joint major to leverage your interdisciplinary interests",
    "• Reach out to professors in AI/ML groups before arriving",
    "• Look into Stanford's CURIS (summer research) and CS+Social Good programs",
    "• Balance technical coursework with humanities to develop well-rounded perspective"
  ]
}
```

### 9. Fit Analysis (School-Specific Compatibility)
```json
{
  "fit_analysis": {
    "academic_fit": "Excellent match. Stanford's CS program emphasizes both theoretical foundations and real-world impact, which aligns perfectly with your research background and community service focus. Your interest in AI for healthcare directly matches Stanford's CS+Social Good initiative and interdisciplinary approach.",

    "cultural_fit": "Strong alignment. Stanford values 'intellectual vitality' and using education to benefit society - your non-profit teaching 200+ students and focus on educational equity embodies this. First-generation status aligns with Stanford's commitment to socioeconomic diversity. Your entrepreneurial projects (mobile app, open-source library) match Stanford's startup culture.",

    "major_fit": "Perfect. CS-AI is one of Stanford's flagship programs. Your ICML publication and neural network research demonstrate you're already working at the level of Stanford PhD students. Having Stanford faculty as research mentor provides insider validation. Your technical achievements (IOI, USACO Platinum) show you can handle rigorous curriculum.",

    "community_fit": "Good, with room for growth. Your teaching and mentorship experience would contribute to Stanford's collaborative culture. However, your heavily STEM-focused profile may not fully leverage Stanford's strengths in humanities and arts. Consider how you'd engage with Stanford's broader intellectual community.",

    "opportunity_fit": "Exceptional. Stanford offers unparalleled opportunities in AI/ML research, access to Silicon Valley internships, and resources for social entrepreneurship. Your profile suggests you'd take full advantage of these. The combination of world-class CS faculty, industry connections, and social impact programs is ideal for your goals."
  }
}
```

---

## Summary

**Input**: Comprehensive applicant profile with 15 major categories and 50+ specific data points including exact AP courses, detailed extracurriculars with time commitments, specific competition placements, research publications, and demographic factors.

**Output**: Detailed evaluation with:
- Admission probability (0-100%)
- Decision category (6 levels)
- 6+ reasoning points
- 10+ category-specific detailed analyses
- 10-15 specific strengths
- 5-10 specific weaknesses
- 8-category score breakdown
- 15-20 actionable advice items
- 5-category fit analysis

**Key Enhancement**: The system now considers:
- Exact AP course alignment with intended major
- Progression and timing of coursework
- Quality and relevance of research/publications
- Depth vs. breadth of extracurriculars
- Socioeconomic context and first-gen status
- Geographic diversity
- Demonstrated interest (school-specific)
- Narrative coherence across application
- Specific competition prestige levels
- Work experience relevance
