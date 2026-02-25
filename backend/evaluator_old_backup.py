from typing import Dict, List
import re

class AdmissionsEvaluator:
    def __init__(self):
        self.schools_data = self._load_schools_data()

    def _load_schools_data(self) -> Dict:
        """Load college data with acceptance rates and score ranges"""
        return {
            "Harvard University": {
                "acceptance_rate": 0.033,
                "avg_gpa": 3.95,
                "sat_range": (1460, 1580),
                "selectivity": "most_competitive"
            },
            "Stanford University": {
                "acceptance_rate": 0.035,
                "avg_gpa": 3.96,
                "sat_range": (1470, 1570),
                "selectivity": "most_competitive"
            },
            "MIT": {
                "acceptance_rate": 0.04,
                "avg_gpa": 3.96,
                "sat_range": (1520, 1580),
                "selectivity": "most_competitive"
            },
            "UC Berkeley": {
                "acceptance_rate": 0.11,
                "avg_gpa": 3.89,
                "sat_range": (1330, 1530),
                "selectivity": "highly_competitive"
            },
            "UCLA": {
                "acceptance_rate": 0.09,
                "avg_gpa": 3.90,
                "sat_range": (1290, 1510),
                "selectivity": "highly_competitive"
            },
            "University of Michigan": {
                "acceptance_rate": 0.18,
                "avg_gpa": 3.88,
                "sat_range": (1340, 1530),
                "selectivity": "highly_competitive"
            },
            "NYU": {
                "acceptance_rate": 0.12,
                "avg_gpa": 3.69,
                "sat_range": (1350, 1530),
                "selectivity": "very_competitive"
            },
            "Boston University": {
                "acceptance_rate": 0.14,
                "avg_gpa": 3.71,
                "sat_range": (1310, 1500),
                "selectivity": "very_competitive"
            }
        }

    def get_available_schools(self) -> List[str]:
        return list(self.schools_data.keys())

    def evaluate(self, applicant) -> Dict:
        school_data = self.schools_data.get(applicant.target_school)

        if not school_data:
            return {
                "decision": "Unknown",
                "admission_probability": 0.0,
                "reasoning": [f"School '{applicant.target_school}' not found in database"],
                "strengths": [],
                "weaknesses": [],
                "score_breakdown": {}
            }

        # Calculate component scores
        academic_score = self._calculate_academic_score(applicant, school_data)
        extracurricular_score = self._calculate_extracurricular_score(applicant)
        application_score = self._calculate_application_score(applicant)
        demographic_score = self._calculate_demographic_score(applicant)

        # Weighted total score
        total_score = (
            academic_score * 0.45 +
            extracurricular_score * 0.30 +
            application_score * 0.20 +
            demographic_score * 0.05
        )

        # Calculate admission probability
        base_acceptance = school_data["acceptance_rate"]
        admission_probability = self._calculate_probability(
            total_score, base_acceptance, school_data["selectivity"]
        )

        # Generate reasoning
        strengths, weaknesses = self._analyze_profile(
            applicant, school_data, academic_score, extracurricular_score, application_score
        )
        reasoning = self._generate_reasoning(
            applicant, school_data, admission_probability, strengths, weaknesses
        )

        decision = "Likely Admit" if admission_probability >= 0.7 else \
                   "Possible" if admission_probability >= 0.4 else \
                   "Reach" if admission_probability >= 0.15 else "Unlikely"

        return {
            "decision": decision,
            "admission_probability": round(admission_probability, 3),
            "reasoning": reasoning,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "score_breakdown": {
                "academic": round(academic_score, 2),
                "extracurricular": round(extracurricular_score, 2),
                "application": round(application_score, 2),
                "demographic": round(demographic_score, 2),
                "total": round(total_score, 2)
            }
        }

    def _calculate_academic_score(self, applicant, school_data) -> float:
        score = 0.0

        # GPA score (40% of academic)
        gpa_percentile = min(applicant.gpa / school_data["avg_gpa"], 1.2)
        score += gpa_percentile * 40

        # GPA trend bonus/penalty
        if applicant.gpa_trend == "upward":
            score += 5
        elif applicant.gpa_trend == "downward":
            score -= 8

        # SAT score (35% of academic)
        if applicant.sat_score:
            sat_min, sat_max = school_data["sat_range"]
            sat_mid = (sat_min + sat_max) / 2
            if applicant.sat_score >= sat_max:
                score += 35
            elif applicant.sat_score >= sat_mid:
                score += 25 + ((applicant.sat_score - sat_mid) / (sat_max - sat_mid)) * 10
            else:
                score += max(0, 15 + ((applicant.sat_score - sat_min) / (sat_mid - sat_min)) * 10)

        # AP courses (15% of academic)
        ap_score = min(applicant.ap_courses / 10, 1.0) * 10
        if applicant.ap_scores:
            avg_ap_score = sum(applicant.ap_scores) / len(applicant.ap_scores)
            ap_score += (avg_ap_score / 5) * 5
        score += ap_score

        # Curriculum difficulty (10% of academic)
        difficulty_map = {"low": 3, "medium": 6, "high": 9, "very_high": 10}
        score += difficulty_map.get(applicant.curriculum_difficulty, 5)

        # TOEFL/IELTS for international students
        if applicant.region == "International":
            if applicant.toefl_score and applicant.toefl_score >= 100:
                score += 3
            elif applicant.ielts_score and applicant.ielts_score >= 7.0:
                score += 3
            elif (applicant.toefl_score and applicant.toefl_score < 90) or \
                 (applicant.ielts_score and applicant.ielts_score < 6.5):
                score -= 5

        return min(score, 100)

    def _calculate_extracurricular_score(self, applicant) -> float:
        score = 0.0

        # Research experience (35% of EC)
        if applicant.research_experience and len(applicant.research_experience) > 50:
            research_keywords = ["published", "paper", "journal", "conference", "lab", "professor", "independent"]
            keyword_count = sum(1 for kw in research_keywords if kw.lower() in applicant.research_experience.lower())
            score += min(keyword_count * 5, 35)

        # Extracurriculars (40% of EC)
        num_activities = len(applicant.extracurriculars)
        if num_activities >= 8:
            score += 40
        elif num_activities >= 5:
            score += 30
        elif num_activities >= 3:
            score += 20
        else:
            score += num_activities * 5

        # Leadership keywords bonus
        leadership_keywords = ["president", "founder", "captain", "lead", "director", "chair"]
        for activity in applicant.extracurriculars:
            if any(kw in activity.lower() for kw in leadership_keywords):
                score += 5
                break

        # Competitions and awards (25% of EC)
        num_competitions = len(applicant.competitions)
        if num_competitions >= 5:
            score += 25
        elif num_competitions >= 3:
            score += 18
        elif num_competitions >= 1:
            score += 10

        # Prestigious competition bonus
        prestigious = ["international", "national", "olympiad", "intel", "regeneron", "siemens"]
        for comp in applicant.competitions:
            if any(p in comp.lower() for p in prestigious):
                score += 10
                break

        return min(score, 100)

    def _calculate_application_score(self, applicant) -> float:
        score = 0.0

        # Letter of recommendation (50%)
        score += (applicant.lor_quality / 5) * 50

        # Essay quality (50%)
        score += (applicant.essay_quality / 5) * 50

        return min(score, 100)

    def _calculate_demographic_score(self, applicant) -> float:
        score = 50.0  # Neutral baseline

        # Geographic diversity
        if applicant.region == "International":
            score += 15
        elif applicant.region in ["Midwest", "Southwest"]:
            score += 5

        # Gender balance (slight adjustment for STEM majors)
        stem_keywords = ["engineering", "computer", "physics", "mathematics", "chemistry"]
        is_stem = any(kw in applicant.target_major.lower() for kw in stem_keywords)

        if is_stem and applicant.sex == "Female":
            score += 10

        return min(score, 100)

    def _calculate_probability(self, total_score: float, base_acceptance: float, selectivity: str) -> float:
        # Normalize score to 0-1 range
        normalized_score = total_score / 100

        # Adjust based on selectivity
        if selectivity == "most_competitive":
            # Very steep curve - even high scores have moderate chances
            probability = base_acceptance + (normalized_score ** 2) * (0.8 - base_acceptance)
        elif selectivity == "highly_competitive":
            probability = base_acceptance + (normalized_score ** 1.5) * (0.85 - base_acceptance)
        else:
            probability = base_acceptance + normalized_score * (0.9 - base_acceptance)

        return min(max(probability, 0.01), 0.95)

    def _analyze_profile(self, applicant, school_data, academic_score, ec_score, app_score):
        strengths = []
        weaknesses = []

        # Academic analysis
        if applicant.gpa >= school_data["avg_gpa"]:
            strengths.append(f"Strong GPA ({applicant.gpa}) meets or exceeds school average")
        else:
            weaknesses.append(f"GPA ({applicant.gpa}) below school average ({school_data['avg_gpa']})")

        if applicant.gpa_trend == "upward":
            strengths.append("Upward GPA trend shows academic growth")
        elif applicant.gpa_trend == "downward":
            weaknesses.append("Downward GPA trend is concerning")

        if applicant.sat_score:
            sat_min, sat_max = school_data["sat_range"]
            if applicant.sat_score >= sat_max:
                strengths.append(f"Excellent SAT score ({applicant.sat_score}) in top range")
            elif applicant.sat_score < sat_min:
                weaknesses.append(f"SAT score ({applicant.sat_score}) below typical range")

        if applicant.ap_courses >= 8:
            strengths.append(f"Rigorous course load with {applicant.ap_courses} AP courses")
        elif applicant.ap_courses < 4:
            weaknesses.append("Limited AP course rigor")

        # Extracurricular analysis
        if len(applicant.research_experience) > 100:
            strengths.append("Substantial research experience")

        if len(applicant.extracurriculars) >= 5:
            strengths.append("Well-rounded extracurricular profile")
        elif len(applicant.extracurriculars) < 3:
            weaknesses.append("Limited extracurricular involvement")

        if len(applicant.competitions) >= 3:
            strengths.append("Strong competition record")

        # Application materials
        if applicant.lor_quality >= 4:
            strengths.append("Strong letters of recommendation")
        elif applicant.lor_quality <= 2:
            weaknesses.append("Weak letters of recommendation")

        if applicant.essay_quality >= 4:
            strengths.append("Compelling personal essays")
        elif applicant.essay_quality <= 2:
            weaknesses.append("Essays need improvement")

        return strengths, weaknesses

    def _generate_reasoning(self, applicant, school_data, probability, strengths, weaknesses):
        reasoning = []

        reasoning.append(
            f"{applicant.target_school} has an acceptance rate of {school_data['acceptance_rate']*100:.1f}%, "
            f"making it a {school_data['selectivity'].replace('_', ' ')} school."
        )

        if probability >= 0.7:
            reasoning.append("Your profile is highly competitive for this institution.")
        elif probability >= 0.4:
            reasoning.append("Your profile is competitive, but admission is not guaranteed.")
        elif probability >= 0.15:
            reasoning.append("This school is a reach, but you have a chance with a strong application.")
        else:
            reasoning.append("This school is a significant reach given your current profile.")

        if strengths:
            reasoning.append(f"Key strengths: {', '.join(strengths[:3])}")

        if weaknesses:
            reasoning.append(f"Areas for improvement: {', '.join(weaknesses[:3])}")

        return reasoning
