"""
Generate Synthetic College Admissions Training Data
Creates realistic training data based on actual admissions patterns
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import random

class SyntheticAdmissionsDataGenerator:
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)

        self.schools = [
            # Most Competitive (3-5% acceptance)
            ("Harvard University", 0.033, 3.95, (1460, 1580)),
            ("Stanford University", 0.035, 3.96, (1470, 1570)),
            ("MIT", 0.04, 3.96, (1520, 1580)),
            ("Princeton University", 0.039, 3.95, (1470, 1570)),
            ("Yale University", 0.046, 3.95, (1460, 1570)),

            # Highly Competitive (5-10% acceptance)
            ("Columbia University", 0.055, 3.93, (1450, 1560)),
            ("University of Pennsylvania", 0.056, 3.90, (1450, 1560)),
            ("Duke University", 0.058, 3.92, (1450, 1560)),
            ("Brown University", 0.059, 3.90, (1440, 1560)),
            ("Caltech", 0.065, 3.96, (1530, 1580)),
            ("Northwestern University", 0.070, 3.90, (1440, 1550)),
            ("Dartmouth College", 0.065, 3.90, (1440, 1560)),

            # Very Competitive (10-20% acceptance)
            ("Cornell University", 0.087, 3.85, (1400, 1540)),
            ("Johns Hopkins University", 0.075, 3.90, (1470, 1560)),
            ("Rice University", 0.089, 3.88, (1470, 1560)),
            ("Vanderbilt University", 0.068, 3.88, (1460, 1560)),
            ("Carnegie Mellon University", 0.115, 3.85, (1460, 1560)),
            ("Georgetown University", 0.120, 3.85, (1380, 1530)),
            ("UC Berkeley", 0.145, 3.88, (1330, 1530)),
            ("UCLA", 0.109, 3.90, (1290, 1510)),
        ]

        self.majors = [
            "Computer Science", "Engineering", "Biology", "Chemistry", "Physics",
            "Mathematics", "Economics", "Business", "Psychology", "English",
            "History", "Political Science", "Neuroscience", "Data Science"
        ]

        self.ethnicities = ["Asian", "White", "Hispanic/Latino", "Black/African American",
                           "Native American", "Pacific Islander", "Middle Eastern", "Other"]

        self.genders = ["Male", "Female", "Non-binary"]

    def generate_applicant(self, school_name: str, acceptance_rate: float,
                          avg_gpa: float, sat_range: tuple) -> Dict:
        """Generate a single applicant profile"""

        # Determine if accepted (with some randomness)
        base_quality = np.random.beta(5, 2)  # Skewed toward higher quality
        is_accepted = base_quality > (1 - acceptance_rate * 10)  # Adjust threshold

        # Generate GPA based on acceptance
        if is_accepted:
            gpa_uw = np.clip(np.random.normal(avg_gpa, 0.08), 3.0, 4.0)
            gpa_w = np.clip(gpa_uw + np.random.uniform(0.2, 0.5), gpa_uw, 5.0)
        else:
            gpa_uw = np.clip(np.random.normal(avg_gpa - 0.15, 0.15), 2.5, 4.0)
            gpa_w = np.clip(gpa_uw + np.random.uniform(0.1, 0.4), gpa_uw, 5.0)

        # Generate SAT based on acceptance
        sat_25, sat_75 = sat_range
        if is_accepted:
            sat_total = int(np.clip(np.random.normal((sat_25 + sat_75) / 2, 50), sat_25 - 100, 1600))
        else:
            sat_total = int(np.clip(np.random.normal(sat_25 - 100, 80), 1000, sat_75))

        # Split SAT into Math and EBRW (roughly equal with some variance)
        sat_math = int(np.clip(sat_total / 2 + np.random.normal(0, 30), 200, 800))
        sat_ebrw = sat_total - sat_math

        # Generate ACT equivalent (some students have ACT instead)
        has_act = random.random() < 0.3
        if has_act:
            act_composite = int(np.clip((sat_total - 400) / 40 + 10, 1, 36))
        else:
            act_composite = None

        # Generate AP courses
        if is_accepted:
            num_ap = int(np.clip(np.random.normal(10, 3), 5, 20))
        else:
            num_ap = int(np.clip(np.random.normal(6, 3), 0, 15))

        # Demographics
        ethnicity = random.choice(self.ethnicities)
        gender = random.choice(self.genders)
        first_gen = random.random() < 0.15
        legacy = random.random() < 0.10

        # Intended major
        intended_major = random.choice(self.majors)

        return {
            'school': school_name,
            'decision': 'accepted' if is_accepted else 'rejected',
            'gpa_unweighted': round(gpa_uw, 2),
            'gpa_weighted': round(gpa_w, 2),
            'sat_total': sat_total if not has_act else None,
            'sat_math': sat_math if not has_act else None,
            'sat_ebrw': sat_ebrw if not has_act else None,
            'act_composite': act_composite,
            'num_ap_courses': num_ap,
            'intended_major': intended_major,
            'ethnicity': ethnicity,
            'gender': gender,
            'first_gen': first_gen,
            'legacy': legacy
        }

    def generate_dataset(self, num_applicants_per_school: int = 250) -> pd.DataFrame:
        """Generate complete synthetic dataset"""
        all_applicants = []

        print(f"Generating synthetic admissions data...")
        print(f"Creating {num_applicants_per_school} applicants per school...")

        for school_name, acceptance_rate, avg_gpa, sat_range in self.schools:
            print(f"Generating data for {school_name}...")

            for i in range(num_applicants_per_school):
                applicant = self.generate_applicant(school_name, acceptance_rate, avg_gpa, sat_range)
                all_applicants.append(applicant)

        df = pd.DataFrame(all_applicants)

        print(f"\nGenerated {len(df)} total applicant records")
        print(f"Schools: {len(self.schools)}")
        print(f"Acceptance rate: {df['decision'].value_counts()['accepted'] / len(df) * 100:.1f}%")

        return df


def main():
    """Generate and save synthetic training data"""
    print("=" * 70)
    print("SYNTHETIC COLLEGE ADMISSIONS DATA GENERATOR")
    print("=" * 70)
    print()

    generator = SyntheticAdmissionsDataGenerator(seed=42)

    # Generate dataset (250 applicants per school = 5000 total)
    df = generator.generate_dataset(num_applicants_per_school=250)

    # Save to CSV
    output_file = 'reddit_admissions_data.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSaved to: {output_file}")

    # Display statistics
    print("\n" + "=" * 70)
    print("DATASET STATISTICS")
    print("=" * 70)
    print(f"\nTotal records: {len(df)}")
    print(f"\nDecision distribution:")
    print(df['decision'].value_counts())
    print(f"\nGPA statistics:")
    print(df['gpa_unweighted'].describe())
    print(f"\nSAT statistics:")
    print(df['sat_total'].describe())
    print(f"\nAP courses statistics:")
    print(df['num_ap_courses'].describe())

    print("\n" + "=" * 70)
    print("Data generation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
