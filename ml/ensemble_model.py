"""
Ensemble Model: Combines XGBoost + Neural Network
Achieves highest accuracy by leveraging strengths of both approaches
"""

import numpy as np
import joblib
from tensorflow import keras
from typing import Dict, Tuple
from train_model import AdmissionsMLModel
from train_neural_network import NeuralNetworkAdmissionsModel

class EnsembleAdmissionsModel:
    """
    Ensemble that combines:
    1. XGBoost (good at capturing feature interactions)
    2. Neural Network (good at learning complex patterns)
    3. Rule-based system (domain expertise)

    Final prediction = weighted average of all three
    """

    def __init__(self, xgb_path: str = None, nn_path: str = None):
        self.xgb_model = None
        self.nn_model = None
        self.xgb_available = False
        self.nn_available = False

        # Load XGBoost model
        if xgb_path:
            try:
                self.xgb_model = AdmissionsMLModel()
                self.xgb_model.load_model(xgb_path)
                self.xgb_available = True
                print("XGBoost model loaded successfully")
            except Exception as e:
                print(f"Failed to load XGBoost model: {e}")

        # Load Neural Network model
        if nn_path:
            try:
                self.nn_model = NeuralNetworkAdmissionsModel()
                self.nn_model.load_model(nn_path)
                self.nn_available = True
                print("Neural Network model loaded successfully")
            except Exception as e:
                print(f"Failed to load Neural Network model: {e}")

    def predict(self, applicant_data: Dict, rule_based_probability: float = None) -> Dict:
        """
        Make ensemble prediction combining all available models

        Weighting strategy:
        - If all 3 available: 40% NN + 30% XGBoost + 30% Rules
        - If NN + XGBoost: 60% NN + 40% XGBoost
        - If only NN: 70% NN + 30% Rules
        - If only XGBoost: 70% XGBoost + 30% Rules
        - If only Rules: 100% Rules
        """

        predictions = {}
        weights = {}

        # Get Neural Network prediction
        if self.nn_available:
            try:
                nn_prob, _ = self.nn_model.predict(applicant_data)
                predictions['neural_network'] = nn_prob
                print(f"Neural Network prediction: {nn_prob:.3f}")
            except Exception as e:
                print(f"Neural Network prediction failed: {e}")
                self.nn_available = False

        # Get XGBoost prediction
        if self.xgb_available:
            try:
                xgb_prob, _ = self.xgb_model.predict(applicant_data)
                predictions['xgboost'] = xgb_prob
                print(f"XGBoost prediction: {xgb_prob:.3f}")
            except Exception as e:
                print(f"XGBoost prediction failed: {e}")
                self.xgb_available = False

        # Get Rule-based prediction
        if rule_based_probability is not None:
            predictions['rule_based'] = rule_based_probability
            print(f"Rule-based prediction: {rule_based_probability:.3f}")

        # Determine weighting strategy
        if self.nn_available and self.xgb_available and rule_based_probability is not None:
            # All three available: NN is best, XGBoost second, Rules third
            weights = {
                'neural_network': 0.40,
                'xgboost': 0.30,
                'rule_based': 0.30
            }
            method = "Full Ensemble (NN + XGBoost + Rules)"

        elif self.nn_available and self.xgb_available:
            # NN + XGBoost: NN slightly better
            weights = {
                'neural_network': 0.60,
                'xgboost': 0.40
            }
            method = "ML Ensemble (NN + XGBoost)"

        elif self.nn_available and rule_based_probability is not None:
            # NN + Rules
            weights = {
                'neural_network': 0.70,
                'rule_based': 0.30
            }
            method = "Hybrid (NN + Rules)"

        elif self.xgb_available and rule_based_probability is not None:
            # XGBoost + Rules
            weights = {
                'xgboost': 0.70,
                'rule_based': 0.30
            }
            method = "Hybrid (XGBoost + Rules)"

        elif self.nn_available:
            # NN only
            weights = {'neural_network': 1.0}
            method = "Neural Network Only"

        elif self.xgb_available:
            # XGBoost only
            weights = {'xgboost': 1.0}
            method = "XGBoost Only"

        elif rule_based_probability is not None:
            # Rules only
            weights = {'rule_based': 1.0}
            method = "Rule-Based Only"

        else:
            return {
                'error': 'No models available for prediction',
                'probability': 0.0
            }

        # Calculate weighted average
        final_probability = sum(predictions[model] * weights[model]
                               for model in predictions if model in weights)

        # Calculate confidence (agreement between models)
        if len(predictions) > 1:
            probs = list(predictions.values())
            std_dev = np.std(probs)
            confidence = 1.0 - min(std_dev * 2, 1.0)  # Lower std = higher confidence
        else:
            confidence = 0.7  # Single model has moderate confidence

        return {
            'probability': final_probability,
            'predictions': predictions,
            'weights': weights,
            'method': method,
            'confidence': confidence,
            'agreement': f"Models agree within {std_dev*100:.1f}%" if len(predictions) > 1 else "Single model"
        }


def compare_models(X, y):
    """
    Compare XGBoost vs Neural Network vs Ensemble on same test set
    """
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, roc_auc_score

    print("=" * 60)
    print("Model Comparison: XGBoost vs Neural Network vs Ensemble")
    print("=" * 60)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results = {}

    # Train and evaluate XGBoost
    print("\n1. Training XGBoost...")
    xgb_model = AdmissionsMLModel()
    xgb_model.feature_names = ['gpa_unweighted', 'sat_total', 'num_ap_courses']  # Simplified
    xgb_metrics = xgb_model.train_model(X, y, model_type='xgboost')
    results['XGBoost'] = xgb_metrics

    # Train and evaluate Neural Network
    print("\n2. Training Neural Network...")
    nn_model = NeuralNetworkAdmissionsModel()
    nn_model.feature_names = xgb_model.feature_names
    nn_metrics = nn_model.train_model(X, y, architecture='deep', epochs=50)
    results['Neural Network'] = nn_metrics

    # Evaluate Ensemble
    print("\n3. Evaluating Ensemble...")
    ensemble = EnsembleAdmissionsModel()
    ensemble.xgb_model = xgb_model
    ensemble.nn_model = nn_model
    ensemble.xgb_available = True
    ensemble.nn_available = True

    # Make predictions on test set
    X_test_scaled_xgb = xgb_model.scaler.transform(X_test)
    X_test_scaled_nn = nn_model.scaler.transform(X_test)

    xgb_preds = xgb_model.model.predict_proba(X_test_scaled_xgb)[:, 1]
    nn_preds = nn_model.model.predict(X_test_scaled_nn, verbose=0).flatten()

    # Ensemble prediction (60% NN + 40% XGBoost)
    ensemble_preds = 0.6 * nn_preds + 0.4 * xgb_preds
    ensemble_binary = (ensemble_preds >= 0.5).astype(int)

    ensemble_metrics = {
        'accuracy': accuracy_score(y_test, ensemble_binary),
        'roc_auc': roc_auc_score(y_test, ensemble_preds)
    }
    results['Ensemble'] = ensemble_metrics

    # Print comparison
    print("\n" + "=" * 60)
    print("RESULTS COMPARISON")
    print("=" * 60)
    print(f"{'Model':<20} {'Accuracy':<12} {'ROC-AUC':<12}")
    print("-" * 60)
    for model_name, metrics in results.items():
        print(f"{model_name:<20} {metrics['accuracy']:<12.3f} {metrics['roc_auc']:<12.3f}")

    print("\n" + "=" * 60)

    # Determine winner
    best_model = max(results.items(), key=lambda x: x[1]['roc_auc'])
    print(f"WINNER: {best_model[0]} with ROC-AUC of {best_model[1]['roc_auc']:.3f}")
    print("=" * 60)

    return results


def main():
    """
    Train both models and create ensemble
    """
    print("=" * 60)
    print("Ensemble Model Training")
    print("=" * 60)

    # Load data
    from train_model import AdmissionsMLModel
    import pandas as pd

    ml_model = AdmissionsMLModel()
    df = pd.read_csv('reddit_admissions_data.csv')
    df = ml_model.engineer_features(df)
    X, y, df_processed = ml_model.prepare_features(df)

    # Compare models
    results = compare_models(X, y)

    # Save comparison results
    import json
    with open('model_comparison.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nComparison results saved to model_comparison.json")


if __name__ == "__main__":
    main()
