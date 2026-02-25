import numpy as np
from typing import Dict, List
import re

class AdmissionsEvaluator:
    def __init__(self):
        self.schools_data = self._load_schools_data()
        self.major_categories = self._load_major_categories()
        self.ap_subjects = self._load_ap_subjects()

    def _load_schools_data(self) -> Dict:
        """Load comprehensive college data"""
        return {
            "Harvard University": {
                "acceptance_rate": 0.033,
                "avg_gpa_unweighted": 3.95,
                "avg_gpa_weighted": 4.18,
                "sat_range": (1460, 1580),
                "sat_25th": 1460,
                "sat_75th": 1580,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "values_demonstrated_interest": False,
                "holistic_review": True,
                "need_blind": True,
                "popular_majors": ["Economics", "Government", "Computer Science", "Biology", "Psychology"]
            },
            "Stanford University": {
                "acceptance_rate": 0.035,
                "avg_gpa_unweighted": 3.96,
                "avg_gpa_weighted": 4.20,
                "sat_range": (1470, 1570),
                "sat_25th": 1470,
                "sat_75th": 1570,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "values_demonstrated_interest": False,
                "holistic_review": True,
                "need_blind": True,
                "popular_majors": ["Computer Science", "Engineering", "Biology", "Economics", "Human Biology"]
            },
            "MIT": {
                "acceptance_rate": 0.04,
                "avg_gpa_unweighted": 3.96,
                "avg_gpa_weighted": 4.17,
                "sat_range": (1520, 1580),
                "sat_25th": 1520,
                "sat_75th": 1580,
                "act_range": (34, 36),
                "selectivity": "most_competitive",
                "values_demonstrated_interest": True,
                "holistic_review": True,
                "need_blind": True,
                "popular_majors": ["Computer Science", "Mechanical Engineering", "Mathematics", "Physics", "Electrical Engineering"]
            },
            "UC Berkeley": {
                "acceptance_rate": 0.11,
                "avg_gpa_unweighted": 3.89,
                "avg_gpa_weighted": 4.43,
                "sat_range": (1330, 1530),
                "sat_25th": 1330,
                "sat_75th": 1530,
                "act_range": (30, 35),
                "selectivity": "highly_competitive",
                "values_demonstrated_interest": False,
                "holistic_review": True,
                "need_blind": False,
                "popular_majors": ["Computer Science", "Economics", "Electrical Engineering", "Political Science", "Business"]
            },
            "UCLA": {
                "acceptance_rate": 0.09,
                "avg_gpa_unweighted": 3.90,
                "avg_gpa_weighted": 4.42,
                "sat_range": (1290, 1510),
                "sat_25th": 1290,
                "sat_75th": 1510,
                "act_range": (29, 34),
                "selectivity": "highly_competitive",
                "values_demonstrated_interest": False,
                "holistic_review": True,
                "need_blind": False,
                "popular_majors": ["Biology", "Psychology", "Economics", "Political Science", "Computer Science"]
            },
            "University of Michigan": {
                "acceptance_rate": 0.18,
                "avg_gpa_unweighted": 3.88,
                "avg_gpa_weighted": 4.25,
                "sat_range": (1340, 1530),
                "sat_25th": 1340,
                "sat_75th": 1530,
                "act_range": (31, 34),
                "selectivity": "highly_competitive",
                "values_demonstrated_interest": True,
                "holistic_review": True,
                "need_blind": False,
                "popular_majors": ["Business", "Engineering", "Computer Science", "Economics", "Psychology"]
            },
            "NYU": {
                "acceptance_rate": 0.12,
                "avg_gpa_unweighted": 3.69,
                "avg_gpa_weighted": 3.86,
                "sat_range": (1350, 1530),
                "sat_25th": 1350,
                "sat_75th": 1530,
                "act_range": (31, 34),
                "selectivity": "very_competitive",
                "values_demonstrated_interest": True,
                "holistic_review": True,
                "need_blind": False,
                "popular_majors": ["Business", "Liberal Arts", "Film", "Economics", "Psychology"]
            },
            "Boston University": {
                "acceptance_rate": 0.14,
                "avg_gpa_unweighted": 3.71,
                "avg_gpa_weighted": 3.91,
                "sat_range": (1310, 1500),
                "sat_25th": 1310,
                "sat_75th": 1500,
                "act_range": (30, 34),
                "selectivity": "very_competitive",
                "values_demonstrated_interest": True,
                "holistic_review": True,
                "need_blind": False,
                "popular_majors": ["Business", "Communications", "Engineering", "Biology", "Economics"]
            }
        }

    def _load_major_categories(self) -> Dict:
        """Categorize majors for alignment analysis"""
        return {
            "STEM": {
                "keywords": ["computer", "engineering", "mathematics", "physics", "chemistry", "biology", "data science", "statistics"],
                "relevant_aps": ["AP Calculus BC", "AP Calculus AB", "AP Physics C", "AP Physics 1", "AP Physics 2",
                                "AP Chemistry", "AP Biology", "AP Computer Science A", "AP Computer Science Principles",
                                "AP Statistics"],
                "relevant_activities": ["research", "science olympiad", "math team", "robotics", "coding", "hackathon"]
            },
            "Humanities": {
                "keywords": ["english", "literature", "history", "philosophy", "classics", "languages"],
                "relevant_aps": ["AP English Literature", "AP English Language", "AP US History", "AP World History",
                                "AP European History", "AP Art History", "AP Spanish", "AP French", "AP Latin"],
                "relevant_activities": ["debate", "writing", "journalism", "literary magazine", "model un"]
            },
            "Social Sciences": {
                "keywords": ["psychology", "sociology", "economics", "political science", "anthropology", "government"],
                "relevant_aps": ["AP Psychology", "AP US Government", "AP Comparative Government", "AP Macroeconomics",
                                "AP Microeconomics", "AP Human Geography"],
                "relevant_activities": ["debate", "model un", "student government", "political campaigns", "research"]
            },
            "Business": {
                "keywords": ["business", "finance", "accounting", "marketing", "management", "entrepreneurship"],
                "relevant_aps": ["AP Macroeconomics", "AP Microeconomics", "AP Statistics", "AP Calculus"],
                "relevant_activities": ["DECA", "FBLA", "entrepreneurship", "business club", "investment club"]
            },
            "Arts": {
                "keywords": ["art", "music", "theater", "dance", "film", "design"],
                "relevant_aps": ["AP Art History", "AP Studio Art", "AP Music Theory"],
                "relevant_activities": ["art portfolio", "music performance", "theater", "film production", "art exhibitions"]
            }
        }

    def _load_ap_subjects(self) -> List[str]:
        """List of all AP subjects"""
        return [
            "AP Calculus AB", "AP Calculus BC", "AP Statistics",
            "AP Physics 1", "AP Physics 2", "AP Physics C: Mechanics", "AP Physics C: E&M",
            "AP Chemistry", "AP Biology", "AP Environmental Science",
            "AP Computer Science A", "AP Computer Science Principles",
            "AP English Language", "AP English Literature",
            "AP US History", "AP World History", "AP European History", "AP Art History",
            "AP US Government", "AP Comparative Government",
            "AP Macroeconomics", "AP Microeconomics",
            "AP Psychology", "AP Human Geography",
            "AP Spanish Language", "AP Spanish Literature", "AP French Language", "AP German Language",
            "AP Chinese Language", "AP Japanese Language", "AP Latin", "AP Italian Language",
            "AP Music Theory", "AP Studio Art", "AP Art and Design"
        ]

    def get_available_schools(self) -> List[str]:
        return list(self.schools_data.keys())

    def evaluate(self, applicant) -> Dict:
        school_data = self.schools_data.get(applicant.target_school)

        if not school_data:
            return self._unknown_school_response(applicant.target_school)

        # Calculate all component scores
        academic_score = self._calculate_academic_score(applicant, school_data)
        major_alignment_score = self._calculate_major_alignment(applicant, school_data)
        extracurricular_score = self._calculate_extracurricular_score(applicant)
        application_score = self._calculate_application_score(applicant)
        demographic_score = self._calculate_demographic_score(applicant, school_data)
        demonstrated_interest_score = self._calculate_demonstrated_interest(applicant, school_data)
        context_score = self._calculate_contextual_factors(applicant)

        # Weighted total score with more nuanced weighting
        total_score = (
            academic_score * 0.35 +
            major_alignment_score * 0.15 +
            extracurricular_score * 0.25 +
            application_score * 0.15 +
            demographic_score * 0.05 +
            demonstrated_interest_score * 0.03 +
            context_score * 0.02
        )

        # Calculate admission probability
        admission_probability = self._calculate_probability(
            total_score, school_data, applicant
        )

        # Generate comprehensive analysis
        strengths, weaknesses = self._analyze_profile(applicant, school_data, academic_score,
                                                       major_alignment_score, extracurricular_score)
        reasoning = self._generate_reasoning(applicant, school_data, admission_probability,
                                             strengths, weaknesses)
        detailed_analysis = self._generate_detailed_analysis(applicant, school_data)
        advice = self._generate_advice(applicant, school_data, weaknesses, admission_probability)
        fit_analysis = self._analyze_fit(applicant, school_data)

        decision = self._determine_decision_category(admission_probability)

        return {
            "decision": decision,
            "admission_probability": round(admission_probability, 3),
            "reasoning": reasoning,
            "detailed_analysis": detailed_analysis,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "score_breakdown": {
                "academic": round(academic_score, 2),
                "major_alignment": round(major_alignment_score, 2),
                "extracurricular": round(extracurricular_score, 2),
                "application": round(application_score, 2),
                "demographic": round(demographic_score, 2),
                "demonstrated_interest": round(demonstrated_interest_score, 2),
                "contextual": round(context_score, 2),
                "total": round(total_score, 2)
            },
            "advice": advice,
            "fit_analysis": fit_analysis
        }

    def _unknown_school_response(self, school_name: str) -> Dict:
        return {
            "decision": "Unknown",
            "admission_probability": 0.0,
            "reasoning": [f"School '{school_name}' not found in database"],
            "detailed_analysis": {},
            "strengths": [],
            "weaknesses": [],
            "score_breakdown": {},
            "advice": ["Please select a school from the available list"],
            "fit_analysis": {}
        }

    def _calculate_academic_score(self, applicant, school_data) -> float:
        score = 0.0

        # GPA Analysis (35 points)
        gpa_percentile = min(applicant.gpa_unweighted / school_data["avg_gpa_unweighted"], 1.2)
        score += gpa_percentile * 25

        # Weighted GPA bonus
        if applicant.gpa_weighted:
            weighted_percentile = min(applicant.gpa_weighted / school_data["avg_gpa_weighted"], 1.2)
            score += weighted_percentile * 10

        # GPA Trend Analysis (10 points)
        if applicant.gpa_trend == "upward":
            # Calculate actual trend from gpa_by_year
            years = sorted(applicant.gpa_by_year.keys())
            if len(years) >= 2:
                improvement = applicant.gpa_by_year[years[-1]] - applicant.gpa_by_year[years[0]]
                if improvement > 0.3:
                    score += 10
                elif improvement > 0.15:
                    score += 7
                else:
                    score += 5
        elif applicant.gpa_trend == "downward":
            score -= 12

        # Class Rank (5 points)
        if applicant.class_rank and applicant.class_size:
            rank_percentile = (applicant.class_size - applicant.class_rank) / applicant.class_size
            if rank_percentile >= 0.95:
                score += 5
            elif rank_percentile >= 0.90:
                score += 4
            elif rank_percentile >= 0.80:
                score += 3

        # Standardized Test Scores (25 points)
        if applicant.sat_score:
            sat_min, sat_max = school_data["sat_range"]
            if applicant.sat_score >= school_data["sat_75th"]:
                score += 25
            elif applicant.sat_score >= (sat_min + sat_max) / 2:
                score += 15 + ((applicant.sat_score - (sat_min + sat_max) / 2) / (sat_max - (sat_min + sat_max) / 2)) * 10
            elif applicant.sat_score >= school_data["sat_25th"]:
                score += 10
            else:
                score += max(0, 5)

        elif applicant.act_score:
            act_min, act_max = school_data["act_range"]
            if applicant.act_score >= act_max:
                score += 25
            elif applicant.act_score >= (act_min + act_max) / 2:
                score += 15 + ((applicant.act_score - (act_min + act_max) / 2) / (act_max - (act_min + act_max) / 2)) * 10
            elif applicant.act_score >= act_min:
                score += 10
            else:
                score += 5

        # AP Courses (15 points)
        num_aps = len(applicant.ap_courses)
        if num_aps >= 10:
            score += 10
        elif num_aps >= 7:
            score += 8
        elif num_aps >= 5:
            score += 6
        elif num_aps >= 3:
            score += 4
        else:
            score += num_aps

        # AP Scores Quality
        if applicant.ap_courses:
            avg_ap_score = sum(ap.score for ap in applicant.ap_courses) / len(applicant.ap_courses)
            if avg_ap_score >= 4.5:
                score += 5
            elif avg_ap_score >= 4.0:
                score += 4
            elif avg_ap_score >= 3.5:
                score += 2

        # IB Diploma
        if applicant.ib_diploma and applicant.ib_score:
            if applicant.ib_score >= 40:
                score += 8
            elif applicant.ib_score >= 35:
                score += 5
            elif applicant.ib_score >= 30:
                score += 3

        # Curriculum Difficulty (5 points)
        difficulty_map = {"low": 1, "medium": 3, "high": 4, "very_high": 5}
        score += difficulty_map.get(applicant.curriculum_difficulty, 3)

        # SAT Subject Tests bonus
        if applicant.sat_subject_tests:
            high_scores = sum(1 for test in applicant.sat_subject_tests for score in test.values() if score >= 750)
            score += min(high_scores * 2, 5)

        # International student language proficiency
        if applicant.country != "United States":
            if applicant.toefl_score and applicant.toefl_score >= 110:
                score += 3
            elif applicant.ielts_score and applicant.ielts_score >= 7.5:
                score += 3
            elif applicant.duolingo_score and applicant.duolingo_score >= 130:
                score += 3
            elif (applicant.toefl_score and applicant.toefl_score < 90) or \
                 (applicant.ielts_score and applicant.ielts_score < 6.5):
                score -= 8

        return min(score, 100)
