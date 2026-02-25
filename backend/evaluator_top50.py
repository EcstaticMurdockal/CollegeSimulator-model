"""
Top 50 US Universities Admissions Evaluator
Complete implementation with application rounds, major alignment, and detailed analysis
"""

from typing import Dict, List, Tuple
import re

class Top50AdmissionsEvaluator:
    def __init__(self):
        self.schools_data = self._load_schools_data()
        self.application_round_multipliers = {
            "Early Decision (ED)": 3.0,
            "Early Decision I (ED1)": 3.0,
            "Early Decision II (ED2)": 2.0,
            "Restrictive Early Action (REA)": 2.5,
            "Single-Choice Early Action (SCEA)": 2.5,
            "Early Action (EA)": 1.5,
            "Regular Decision (RD)": 1.0,
            "Rolling Admission": 1.2
        }

    def _load_schools_data(self) -> Dict:
        """Load all Top 50 US universities with complete data"""
        return {
            # Top 10
            "Princeton University": {
                "rank": 1,
                "acceptance_rate": 0.039,
                "avg_gpa_unweighted": 3.95,
                "avg_gpa_weighted": 4.18,
                "sat_range": (1470, 1570),
                "sat_25th": 1470, "sat_75th": 1570,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["SCEA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": True
            },
            "MIT": {
                "rank": 2,
                "acceptance_rate": 0.04,
                "avg_gpa_unweighted": 3.96,
                "avg_gpa_weighted": 4.17,
                "sat_range": (1520, 1580),
                "sat_25th": 1520, "sat_75th": 1580,
                "act_range": (34, 36),
                "selectivity": "most_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": True
            },
            "Harvard University": {
                "rank": 3,
                "acceptance_rate": 0.033,
                "avg_gpa_unweighted": 3.95,
                "avg_gpa_weighted": 4.18,
                "sat_range": (1460, 1580),
                "sat_25th": 1460, "sat_75th": 1580,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["SCEA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": True
            },
            "Stanford University": {
                "rank": 3,
                "acceptance_rate": 0.035,
                "avg_gpa_unweighted": 3.96,
                "avg_gpa_weighted": 4.19,
                "sat_range": (1470, 1570),
                "sat_25th": 1470, "sat_75th": 1570,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["REA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": True
            },
            "Yale University": {
                "rank": 5,
                "acceptance_rate": 0.046,
                "avg_gpa_unweighted": 3.95,
                "avg_gpa_weighted": 4.19,
                "sat_range": (1460, 1570),
                "sat_25th": 1460, "sat_75th": 1570,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["SCEA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": True
            },
            "University of Pennsylvania": {
                "rank": 6,
                "acceptance_rate": 0.056,
                "avg_gpa_unweighted": 3.90,
                "avg_gpa_weighted": 4.16,
                "sat_range": (1450, 1560),
                "sat_25th": 1450, "sat_75th": 1560,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Caltech": {
                "rank": 7,
                "acceptance_rate": 0.029,
                "avg_gpa_unweighted": 3.97,
                "avg_gpa_weighted": 4.19,
                "sat_range": (1530, 1580),
                "sat_25th": 1530, "sat_75th": 1580,
                "act_range": (35, 36),
                "selectivity": "most_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": True
            },
            "Duke University": {
                "rank": 7,
                "acceptance_rate": 0.058,
                "avg_gpa_unweighted": 3.94,
                "avg_gpa_weighted": 4.17,
                "sat_range": (1480, 1570),
                "sat_25th": 1480, "sat_75th": 1570,
                "act_range": (34, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Johns Hopkins University": {
                "rank": 9,
                "acceptance_rate": 0.073,
                "avg_gpa_unweighted": 3.92,
                "avg_gpa_weighted": 4.15,
                "sat_range": (1480, 1570),
                "sat_25th": 1480, "sat_75th": 1570,
                "act_range": (34, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Northwestern University": {
                "rank": 9,
                "acceptance_rate": 0.070,
                "avg_gpa_unweighted": 3.92,
                "avg_gpa_weighted": 4.15,
                "sat_range": (1450, 1550),
                "sat_25th": 1450, "sat_75th": 1550,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            # 11-20
            "Brown University": {
                "rank": 11,
                "acceptance_rate": 0.052,
                "avg_gpa_unweighted": 3.94,
                "avg_gpa_weighted": 4.16,
                "sat_range": (1450, 1560),
                "sat_25th": 1450, "sat_75th": 1560,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Cornell University": {
                "rank": 11,
                "acceptance_rate": 0.087,
                "avg_gpa_unweighted": 3.90,
                "avg_gpa_weighted": 4.14,
                "sat_range": (1400, 1540),
                "sat_25th": 1400, "sat_75th": 1540,
                "act_range": (32, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Dartmouth College": {
                "rank": 11,
                "acceptance_rate": 0.062,
                "avg_gpa_unweighted": 3.93,
                "avg_gpa_weighted": 4.15,
                "sat_range": (1440, 1560),
                "sat_25th": 1440, "sat_75th": 1560,
                "act_range": (32, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Columbia University": {
                "rank": 14,
                "acceptance_rate": 0.039,
                "avg_gpa_unweighted": 3.95,
                "avg_gpa_weighted": 4.17,
                "sat_range": (1470, 1570),
                "sat_25th": 1470, "sat_75th": 1570,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Vanderbilt University": {
                "rank": 14,
                "acceptance_rate": 0.066,
                "avg_gpa_unweighted": 3.91,
                "avg_gpa_weighted": 4.15,
                "sat_range": (1460, 1570),
                "sat_25th": 1460, "sat_75th": 1570,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Washington University in St. Louis": {
                "rank": 14,
                "acceptance_rate": 0.116,
                "avg_gpa_unweighted": 3.92,
                "avg_gpa_weighted": 4.15,
                "sat_range": (1470, 1570),
                "sat_25th": 1470, "sat_75th": 1570,
                "act_range": (33, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Rice University": {
                "rank": 17,
                "acceptance_rate": 0.087,
                "avg_gpa_unweighted": 3.92,
                "avg_gpa_weighted": 4.15,
                "sat_range": (1470, 1570),
                "sat_25th": 1470, "sat_75th": 1570,
                "act_range": (34, 35),
                "selectivity": "most_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "University of Notre Dame": {
                "rank": 18,
                "acceptance_rate": 0.128,
                "avg_gpa_unweighted": 3.90,
                "avg_gpa_weighted": 4.13,
                "sat_range": (1400, 1550),
                "sat_25th": 1400, "sat_75th": 1550,
                "act_range": (32, 35),
                "selectivity": "highly_competitive",
                "available_rounds": ["REA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "UCLA": {
                "rank": 18,
                "acceptance_rate": 0.090,
                "avg_gpa_unweighted": 3.90,
                "avg_gpa_weighted": 4.31,
                "sat_range": (1290, 1510),
                "sat_25th": 1290, "sat_75th": 1510,
                "act_range": (27, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "UC Berkeley": {
                "rank": 20,
                "acceptance_rate": 0.113,
                "avg_gpa_unweighted": 3.89,
                "avg_gpa_weighted": 4.29,
                "sat_range": (1330, 1530),
                "sat_25th": 1330, "sat_75th": 1530,
                "act_range": (28, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            # 21-30
            "Emory University": {
                "rank": 21,
                "acceptance_rate": 0.113,
                "avg_gpa_unweighted": 3.88,
                "avg_gpa_weighted": 4.12,
                "sat_range": (1370, 1520),
                "sat_25th": 1370, "sat_75th": 1520,
                "act_range": (31, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Georgetown University": {
                "rank": 21,
                "acceptance_rate": 0.120,
                "avg_gpa_unweighted": 3.89,
                "avg_gpa_weighted": 4.13,
                "sat_range": (1380, 1530),
                "sat_25th": 1380, "sat_75th": 1530,
                "act_range": (31, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["REA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "University of Michigan": {
                "rank": 23,
                "acceptance_rate": 0.180,
                "avg_gpa_unweighted": 3.88,
                "avg_gpa_weighted": 4.11,
                "sat_range": (1340, 1530),
                "sat_25th": 1340, "sat_75th": 1530,
                "act_range": (31, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Carnegie Mellon University": {
                "rank": 24,
                "acceptance_rate": 0.114,
                "avg_gpa_unweighted": 3.91,
                "avg_gpa_weighted": 4.14,
                "sat_range": (1460, 1560),
                "sat_25th": 1460, "sat_75th": 1560,
                "act_range": (33, 35),
                "selectivity": "highly_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "University of Southern California": {
                "rank": 24,
                "acceptance_rate": 0.095,
                "avg_gpa_unweighted": 3.86,
                "avg_gpa_weighted": 4.10,
                "sat_range": (1380, 1530),
                "sat_25th": 1380, "sat_75th": 1530,
                "act_range": (31, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "University of Virginia": {
                "rank": 24,
                "acceptance_rate": 0.191,
                "avg_gpa_unweighted": 3.87,
                "avg_gpa_weighted": 4.11,
                "sat_range": (1370, 1520),
                "sat_25th": 1370, "sat_75th": 1520,
                "act_range": (31, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Wake Forest University": {
                "rank": 27,
                "acceptance_rate": 0.217,
                "avg_gpa_unweighted": 3.84,
                "avg_gpa_weighted": 4.08,
                "sat_range": (1330, 1480),
                "sat_25th": 1330, "sat_75th": 1480,
                "act_range": (30, 33),
                "selectivity": "highly_competitive",
                "available_rounds": ["ED", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "New York University": {
                "rank": 28,
                "acceptance_rate": 0.120,
                "avg_gpa_unweighted": 3.69,
                "avg_gpa_weighted": 3.95,
                "sat_range": (1350, 1530),
                "sat_25th": 1350, "sat_75th": 1530,
                "act_range": (31, 34),
                "selectivity": "very_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Tufts University": {
                "rank": 28,
                "acceptance_rate": 0.095,
                "avg_gpa_unweighted": 3.91,
                "avg_gpa_weighted": 4.13,
                "sat_range": (1420, 1540),
                "sat_25th": 1420, "sat_75th": 1540,
                "act_range": (32, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "University of North Carolina at Chapel Hill": {
                "rank": 28,
                "acceptance_rate": 0.167,
                "avg_gpa_unweighted": 3.87,
                "avg_gpa_weighted": 4.39,
                "sat_range": (1300, 1480),
                "sat_25th": 1300, "sat_75th": 1480,
                "act_range": (29, 33),
                "selectivity": "highly_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            # 31-40
            "UC Santa Barbara": {
                "rank": 31,
                "acceptance_rate": 0.257,
                "avg_gpa_unweighted": 3.85,
                "avg_gpa_weighted": 4.22,
                "sat_range": (1230, 1480),
                "sat_25th": 1230, "sat_75th": 1480,
                "act_range": (27, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "University of Florida": {
                "rank": 32,
                "acceptance_rate": 0.230,
                "avg_gpa_unweighted": 3.85,
                "avg_gpa_weighted": 4.42,
                "sat_range": (1280, 1450),
                "sat_25th": 1280, "sat_75th": 1450,
                "act_range": (28, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "UC Irvine": {
                "rank": 32,
                "acceptance_rate": 0.211,
                "avg_gpa_unweighted": 3.83,
                "avg_gpa_weighted": 4.18,
                "sat_range": (1230, 1450),
                "sat_25th": 1230, "sat_75th": 1450,
                "act_range": (26, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Boston College": {
                "rank": 34,
                "acceptance_rate": 0.167,
                "avg_gpa_unweighted": 3.86,
                "avg_gpa_weighted": 4.09,
                "sat_range": (1370, 1500),
                "sat_25th": 1370, "sat_75th": 1500,
                "act_range": (31, 34),
                "selectivity": "highly_competitive",
                "available_rounds": ["ED", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "UC San Diego": {
                "rank": 34,
                "acceptance_rate": 0.238,
                "avg_gpa_unweighted": 3.87,
                "avg_gpa_weighted": 4.23,
                "sat_range": (1250, 1490),
                "sat_25th": 1250, "sat_75th": 1490,
                "act_range": (27, 34),
                "selectivity": "very_competitive",
                "available_rounds": ["RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "University of Rochester": {
                "rank": 36,
                "acceptance_rate": 0.387,
                "avg_gpa_unweighted": 3.80,
                "avg_gpa_weighted": 4.05,
                "sat_range": (1330, 1510),
                "sat_25th": 1330, "sat_75th": 1510,
                "act_range": (30, 34),
                "selectivity": "very_competitive",
                "available_rounds": ["ED", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Boston University": {
                "rank": 37,
                "acceptance_rate": 0.140,
                "avg_gpa_unweighted": 3.71,
                "avg_gpa_weighted": 3.96,
                "sat_range": (1310, 1500),
                "sat_25th": 1310, "sat_75th": 1500,
                "act_range": (30, 34),
                "selectivity": "very_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "UC Davis": {
                "rank": 37,
                "acceptance_rate": 0.372,
                "avg_gpa_unweighted": 3.82,
                "avg_gpa_weighted": 4.16,
                "sat_range": (1160, 1430),
                "sat_25th": 1160, "sat_75th": 1430,
                "act_range": (25, 32),
                "selectivity": "very_competitive",
                "available_rounds": ["RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Brandeis University": {
                "rank": 39,
                "acceptance_rate": 0.310,
                "avg_gpa_unweighted": 3.79,
                "avg_gpa_weighted": 4.03,
                "sat_range": (1330, 1500),
                "sat_25th": 1330, "sat_75th": 1500,
                "act_range": (30, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Case Western Reserve University": {
                "rank": 39,
                "acceptance_rate": 0.267,
                "avg_gpa_unweighted": 3.78,
                "avg_gpa_weighted": 4.02,
                "sat_range": (1330, 1500),
                "sat_25th": 1330, "sat_75th": 1500,
                "act_range": (31, 34),
                "selectivity": "very_competitive",
                "available_rounds": ["ED1", "ED2", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "College of William & Mary": {
                "rank": 39,
                "acceptance_rate": 0.333,
                "avg_gpa_unweighted": 3.84,
                "avg_gpa_weighted": 4.28,
                "sat_range": (1330, 1490),
                "sat_25th": 1330, "sat_75th": 1490,
                "act_range": (30, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["ED", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            # 41-50
            "Georgia Institute of Technology": {
                "rank": 42,
                "acceptance_rate": 0.161,
                "avg_gpa_unweighted": 3.87,
                "avg_gpa_weighted": 4.18,
                "sat_range": (1370, 1530),
                "sat_25th": 1370, "sat_75th": 1530,
                "act_range": (31, 35),
                "selectivity": "highly_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Tulane University": {
                "rank": 42,
                "acceptance_rate": 0.089,
                "avg_gpa_unweighted": 3.76,
                "avg_gpa_weighted": 4.00,
                "sat_range": (1340, 1490),
                "sat_25th": 1340, "sat_75th": 1490,
                "act_range": (30, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["ED1", "ED2", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "University of Wisconsin-Madison": {
                "rank": 42,
                "acceptance_rate": 0.494,
                "avg_gpa_unweighted": 3.82,
                "avg_gpa_weighted": 4.05,
                "sat_range": (1300, 1480),
                "sat_25th": 1300, "sat_75th": 1480,
                "act_range": (28, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "University of Illinois Urbana-Champaign": {
                "rank": 45,
                "acceptance_rate": 0.447,
                "avg_gpa_unweighted": 3.80,
                "avg_gpa_weighted": 4.04,
                "sat_range": (1280, 1490),
                "sat_25th": 1280, "sat_75th": 1490,
                "act_range": (28, 34),
                "selectivity": "very_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Lehigh University": {
                "rank": 45,
                "acceptance_rate": 0.323,
                "avg_gpa_unweighted": 3.75,
                "avg_gpa_weighted": 3.99,
                "sat_range": (1320, 1480),
                "sat_25th": 1320, "sat_75th": 1480,
                "act_range": (30, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["ED1", "ED2", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Northeastern University": {
                "rank": 45,
                "acceptance_rate": 0.066,
                "avg_gpa_unweighted": 3.82,
                "avg_gpa_weighted": 4.06,
                "sat_range": (1390, 1530),
                "sat_25th": 1390, "sat_75th": 1530,
                "act_range": (32, 35),
                "selectivity": "highly_competitive",
                "available_rounds": ["ED1", "ED2", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Pepperdine University": {
                "rank": 45,
                "acceptance_rate": 0.317,
                "avg_gpa_unweighted": 3.73,
                "avg_gpa_weighted": 3.97,
                "sat_range": (1230, 1420),
                "sat_25th": 1230, "sat_75th": 1420,
                "act_range": (27, 32),
                "selectivity": "very_competitive",
                "available_rounds": ["ED", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            },
            "Ohio State University": {
                "rank": 49,
                "acceptance_rate": 0.527,
                "avg_gpa_unweighted": 3.76,
                "avg_gpa_weighted": 4.00,
                "sat_range": (1240, 1450),
                "sat_25th": 1240, "sat_75th": 1450,
                "act_range": (27, 32),
                "selectivity": "competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Purdue University": {
                "rank": 49,
                "acceptance_rate": 0.528,
                "avg_gpa_unweighted": 3.74,
                "avg_gpa_weighted": 3.98,
                "sat_range": (1190, 1440),
                "sat_25th": 1190, "sat_75th": 1440,
                "act_range": (26, 33),
                "selectivity": "competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "University of Georgia": {
                "rank": 49,
                "acceptance_rate": 0.426,
                "avg_gpa_unweighted": 3.79,
                "avg_gpa_weighted": 4.02,
                "sat_range": (1240, 1420),
                "sat_25th": 1240, "sat_75th": 1420,
                "act_range": (27, 32),
                "selectivity": "competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "University of Texas at Austin": {
                "rank": 49,
                "acceptance_rate": 0.298,
                "avg_gpa_unweighted": 3.77,
                "avg_gpa_weighted": 4.01,
                "sat_range": (1230, 1480),
                "sat_25th": 1230, "sat_75th": 1480,
                "act_range": (27, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["EA", "RD"],
                "values_demonstrated_interest": False,
                "need_blind": False
            },
            "Villanova University": {
                "rank": 49,
                "acceptance_rate": 0.230,
                "avg_gpa_unweighted": 3.78,
                "avg_gpa_weighted": 4.01,
                "sat_range": (1330, 1480),
                "sat_25th": 1330, "sat_75th": 1480,
                "act_range": (30, 33),
                "selectivity": "very_competitive",
                "available_rounds": ["ED1", "ED2", "EA", "RD"],
                "values_demonstrated_interest": True,
                "need_blind": False
            }
        }

    def get_available_schools(self) -> List[str]:
        """Return list of all available schools"""
        return sorted(list(self.schools_data.keys()))

    def _get_application_round_multiplier(self, round_name: str, school_data: Dict) -> float:
        """Get multiplier for application round, checking if school offers it"""
        # Extract just the round type (ED, EA, REA, etc.) from the full name
        round_type = round_name.split("(")[1].rstrip(")") if "(" in round_name else round_name

        # Check if school offers this round
        available_rounds = school_data.get("available_rounds", ["RD"])

        # Match the round type
        for available in available_rounds:
            if round_type in available or available in round_type:
                return self.application_round_multipliers.get(round_name, 1.0)

        # If school doesn't offer this round, return RD multiplier
        return 1.0

    def evaluate(self, applicant) -> Dict:
        """Main evaluation method"""
        school_data = self.schools_data.get(applicant.target_school)

        if not school_data:
            return {
                "decision": "Unknown",
                "admission_probability": 0.0,
                "reasoning": [f"School '{applicant.target_school}' not found in database"],
                "detailed_analysis": {},
                "strengths": [],
                "weaknesses": [],
                "score_breakdown": {},
                "advice": [],
                "fit_analysis": {},
                "application_round_impact": {}
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

        # Calculate base admission probability
        base_acceptance = school_data["acceptance_rate"]
        base_probability = self._calculate_probability(
            total_score, base_acceptance, school_data["selectivity"]
        )

        # Apply application round multiplier
        round_multiplier = self._get_application_round_multiplier(
            applicant.application_round, school_data
        )
        admission_probability = min(base_probability * round_multiplier, 0.95)

        # Generate analysis
        strengths, weaknesses = self._analyze_profile(
            applicant, school_data, academic_score, extracurricular_score, application_score
        )
        reasoning = self._generate_reasoning(
            applicant, school_data, admission_probability, strengths, weaknesses
        )
        detailed_analysis = self._generate_detailed_analysis(
            applicant, school_data, academic_score, extracurricular_score
        )
        advice = self._generate_advice(applicant, weaknesses, school_data)
        fit_analysis = self._generate_fit_analysis(applicant, school_data)

        decision = "Likely Admit" if admission_probability >= 0.7 else \
                   "Possible" if admission_probability >= 0.4 else \
                   "Reach" if admission_probability >= 0.15 else "Unlikely"

        return {
            "decision": decision,
            "admission_probability": round(admission_probability, 3),
            "reasoning": reasoning,
            "detailed_analysis": detailed_analysis,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "score_breakdown": {
                "academic": round(academic_score, 2),
                "extracurricular": round(extracurricular_score, 2),
                "application": round(application_score, 2),
                "demographic": round(demographic_score, 2),
                "total": round(total_score, 2)
            },
            "advice": advice,
            "fit_analysis": fit_analysis,
            "application_round_impact": {
                "round": applicant.application_round,
                "multiplier": round_multiplier,
                "base_probability": round(base_probability, 3),
                "final_probability": round(admission_probability, 3)
            }
        }

    def _calculate_academic_score(self, applicant, school_data) -> float:
        score = 0.0

        # GPA score (40% of academic)
        gpa_percentile = min(applicant.gpa_unweighted / school_data["avg_gpa_unweighted"], 1.2)
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
        num_aps = len(applicant.ap_courses)
        ap_score = min(num_aps / 10, 1.0) * 10
        if applicant.ap_courses:
            avg_ap_score = sum(ap.score for ap in applicant.ap_courses) / len(applicant.ap_courses)
            ap_score += (avg_ap_score / 5) * 5
        score += ap_score

        # Curriculum difficulty (10% of academic)
        difficulty_map = {"low": 3, "medium": 6, "high": 9, "very_high": 10}
        score += difficulty_map.get(applicant.curriculum_difficulty, 5)

        # TOEFL/IELTS for international students
        if applicant.country != "United States":
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
            if any(kw in activity.role.lower() for kw in leadership_keywords):
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
            if any(p in comp.level.lower() for p in prestigious):
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
        if applicant.country != "United States":
            score += 15
        elif applicant.state_province in ["Wyoming", "Montana", "North Dakota", "South Dakota", "Alaska"]:
            score += 5

        # First generation bonus
        if applicant.first_generation:
            score += 10

        # Legacy penalty (holistic review considers this negatively in some contexts)
        if applicant.legacy_status:
            score += 5

        # Recruited athlete major boost
        if applicant.recruited_athlete:
            score += 20

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
        elif selectivity == "very_competitive":
            probability = base_acceptance + (normalized_score ** 1.3) * (0.90 - base_acceptance)
        else:  # competitive
            probability = base_acceptance + normalized_score * (0.92 - base_acceptance)

        return min(max(probability, 0.01), 0.95)

    def _analyze_profile(self, applicant, school_data, academic_score, ec_score, app_score):
        strengths = []
        weaknesses = []

        # Academic analysis
        if applicant.gpa_unweighted >= school_data["avg_gpa_unweighted"]:
            strengths.append(f"Strong GPA ({applicant.gpa_unweighted}) meets or exceeds school average")
        else:
            weaknesses.append(f"GPA ({applicant.gpa_unweighted}) below school average ({school_data['avg_gpa_unweighted']})")

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

        num_aps = len(applicant.ap_courses)
        if num_aps >= 8:
            strengths.append(f"Rigorous course load with {num_aps} AP courses")
        elif num_aps < 4:
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

    def _generate_detailed_analysis(self, applicant, school_data, academic_score, ec_score):
        return {
            "academic": f"Academic score: {academic_score:.1f}/100. Your GPA and test scores are {'competitive' if academic_score >= 70 else 'below average'} for this school.",
            "extracurricular": f"Extracurricular score: {ec_score:.1f}/100. Your activities demonstrate {'strong' if ec_score >= 70 else 'moderate'} involvement.",
            "fit": f"This school values {'demonstrated interest' if school_data.get('values_demonstrated_interest') else 'academic excellence primarily'}."
        }

    def _generate_advice(self, applicant, weaknesses, school_data):
        advice = []

        if any("GPA" in w for w in weaknesses):
            advice.append("Focus on maintaining or improving your GPA in remaining semesters")

        if any("SAT" in w for w in weaknesses):
            advice.append("Consider retaking standardized tests to improve your scores")

        if any("AP" in w for w in weaknesses):
            advice.append("Take more rigorous courses if available")

        if any("extracurricular" in w for w in weaknesses):
            advice.append("Deepen involvement in 2-3 key activities rather than spreading thin")

        if school_data.get("values_demonstrated_interest"):
            advice.append("Visit campus, attend info sessions, and contact admissions to show interest")

        return advice if advice else ["Continue your strong performance across all areas"]

    def _generate_fit_analysis(self, applicant, school_data):
        return {
            "selectivity": f"This is a {school_data['selectivity'].replace('_', ' ')} school",
            "acceptance_rate": f"{school_data['acceptance_rate']*100:.1f}% acceptance rate",
            "your_standing": "Competitive applicant" if applicant.gpa_unweighted >= school_data["avg_gpa_unweighted"] else "Below average applicant"
        }
