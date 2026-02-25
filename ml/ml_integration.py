"""
ML Model Integration with FastAPI Backend
Combines rule-based system with trained ML model
"""

import joblib
import numpy as np
from typing import Dict
from pathlib import Path

class HybridAdmissionsPredictor:
    """
    Hybrid system that combines:
    1. Rule-based heuristic scoring (from evaluator.py)
    2. ML model predictions (from trained model)
    """

    def __init__(self, model_path: str = None):
        self.ml_model = None
        self.ml_available = False

        if model_path and Path(model_path).exists():
            try:
                model_data = joblib.load(model_path)
                self.ml_model = model_data['model']
                self.scaler = model_data['scaler']
                self.label_encoders = model_data['label_encoders']
                self.feature_names = model_data['feature_names']
                self.ml_available = True
                print(f"ML model loaded successfully from {model_path}")
            except Exception as e:
                print(f"Failed to load ML model: {e}")
                print("Falling back to rule-based system only")

    def prepare_ml_features(self, applicant) -> Dict:
        """Convert applicant data to ML model features"""

        features = {}

        # Academic features
        features['gpa_unweighted'] = applicant.gpa_unweighted
        features['gpa_weighted'] = applicant.gpa_weighted if applicant.gpa_weighted else applicant.gpa_unweighted * 1.1

        # Test scores
        features['sat_total'] = applicant.sat_score if applicant.sat_score else 0
        features['sat_math'] = applicant.sat_math if applicant.sat_math else 0
        features['sat_ebrw'] = applicant.sat_ebrw if applicant.sat_ebrw else 0
        features['act_composite'] = applicant.act_score if applicant.act_score else 0

        # AP courses
        features['num_ap_courses'] = len(applicant.ap_courses)

        # Engineered features
        features['gpa_difference'] = features['gpa_weighted'] - features['gpa_unweighted']

        if features['sat_math'] and features['sat_ebrw']:
            features['sat_balance'] = abs(features['sat_math'] - features['sat_ebrw'])
        else:
            features['sat_balance'] = 0

        # Convert ACT to SAT equivalent
        if features['act_composite'] > 0:
            act_to_sat = {
                36: 1600, 35: 1560, 34: 1520, 33: 1480, 32: 1440,
                31: 1400, 30: 1360, 29: 1330, 28: 1290, 27: 1260,
                26: 1220, 25: 1190, 24: 1160, 23: 1130, 22: 1100
            }
            features['sat_equivalent'] = act_to_sat.get(features['act_composite'], 1000)
        else:
            features['sat_equivalent'] = 0

        features['standardized_test'] = features['sat_total'] if features['sat_total'] > 0 else features['sat_equivalent']

        # Academic index
        features['academic_index'] = (
            (features['gpa_unweighted'] / 4.0) * 40 +
            (features['standardized_test'] / 1600) * 40 +
            min(features['num_ap_courses'] / 10, 1.0) * 20
        )

        # Categorical features
        features['ethnicity'] = applicant.ethnicity[0] if applicant.ethnicity else 'Unknown'
        features['gender'] = applicant.gender.value
        features['intended_major'] = applicant.target_major

        # Boolean features
        features['first_gen'] = int(applicant.first_generation)
        features['legacy'] = int(applicant.legacy_status)

        return features

    def get_ml_prediction(self, applicant) -> float:
        """Get prediction from ML model"""

        if not self.ml_available:
            return None

        try:
            # Prepare features
            feature_dict = self.prepare_ml_features(applicant)

            # Convert to feature vector in correct order
            feature_vector = []
            for feature_name in self.feature_names:
                if feature_name.endswith('_encoded'):
                    # Handle categorical features
                    original_col = feature_name.replace('_encoded', '')
                    value = feature_dict.get(original_col, 'Unknown')
                    if original_col in self.label_encoders:
                        try:
                            encoded_value = self.label_encoders[original_col].transform([value])[0]
                        except:
                            encoded_value = 0
                        feature_vector.append(encoded_value)
                    else:
                        feature_vector.append(0)
                else:
                    feature_vector.append(feature_dict.get(feature_name, 0))

            # Scale and predict
            features_scaled = self.scaler.transform([feature_vector])
            probability = self.ml_model.predict_proba(features_scaled)[0][1]

            return probability

        except Exception as e:
            print(f"ML prediction failed: {e}")
            return None

    def get_hybrid_prediction(self, applicant, rule_based_probability: float) -> Dict:
        """
        Combine rule-based and ML predictions

        Strategy:
        - If ML model available: weighted average (70% ML, 30% rule-based)
        - If ML model not available: use rule-based only
        """

        ml_probability = self.get_ml_prediction(applicant)

        if ml_probability is not None:
            # Hybrid approach: weighted average
            final_probability = 0.7 * ml_probability + 0.3 * rule_based_probability

            return {
                'probability': final_probability,
                'ml_probability': ml_probability,
                'rule_based_probability': rule_based_probability,
                'method': 'hybrid',
                'ml_weight': 0.7,
                'rule_weight': 0.3
            }
        else:
            # Fallback to rule-based only
            return {
                'probability': rule_based_probability,
                'ml_probability': None,
                'rule_based_probability': rule_based_probability,
                'method': 'rule_based_only',
                'ml_weight': 0.0,
                'rule_weight': 1.0
            }


# Example usage in evaluator.py
"""
from ml_integration import HybridAdmissionsPredictor

class AdmissionsEvaluator:
    def __init__(self):
        self.schools_data = self._load_schools_data()
        self.hybrid_predictor = HybridAdmissionsPredictor('ml/admissions_model.pkl')

    def evaluate(self, applicant):
        # ... existing code to calculate scores ...

        # Get rule-based probability
        rule_based_prob = self._calculate_probability(total_score, school_data, applicant)

        # Get hybrid prediction
        hybrid_result = self.hybrid_predictor.get_hybrid_prediction(applicant, rule_based_prob)

        # Use hybrid probability
        admission_probability = hybrid_result['probability']

        # Add ML info to result
        result['ml_info'] = {
            'ml_available': hybrid_result['method'] == 'hybrid',
            'ml_probability': hybrid_result['ml_probability'],
            'rule_based_probability': hybrid_result['rule_based_probability'],
            'method': hybrid_result['method']
        }

        return result
"""
