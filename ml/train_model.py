"""
Machine Learning Model Training Pipeline
Trains admission prediction models using collected data
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import xgboost as xgb
import joblib
import json
from typing import Dict, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class AdmissionsMLModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.school_models = {}  # Separate model for each school

    def load_data(self, csv_path: str) -> pd.DataFrame:
        """Load and initial preprocessing of data"""
        df = pd.DataFrame(csv_path)

        print(f"Loaded {len(df)} records")
        print(f"Columns: {df.columns.tolist()}")
        print(f"\nData shape: {df.shape}")
        print(f"\nMissing values:\n{df.isnull().sum()}")

        return df

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create additional features from raw data"""

        # GPA features
        if 'gpa_weighted' in df.columns and 'gpa_unweighted' in df.columns:
            df['gpa_difference'] = df['gpa_weighted'] - df['gpa_unweighted']

        # Test score features
        if 'sat_math' in df.columns and 'sat_ebrw' in df.columns:
            df['sat_balance'] = abs(df['sat_math'] - df['sat_ebrw'])

        # Convert ACT to SAT equivalent for unified scoring
        if 'act_composite' in df.columns:
            act_to_sat = {
                36: 1600, 35: 1560, 34: 1520, 33: 1480, 32: 1440,
                31: 1400, 30: 1360, 29: 1330, 28: 1290, 27: 1260,
                26: 1220, 25: 1190, 24: 1160, 23: 1130, 22: 1100,
                21: 1060, 20: 1030, 19: 990, 18: 960, 17: 920,
                16: 880, 15: 840, 14: 800, 13: 760, 12: 710
            }
            df['sat_equivalent'] = df['act_composite'].map(act_to_sat)

            # Use SAT if available, otherwise use ACT equivalent
            df['standardized_test'] = df['sat_total'].fillna(df['sat_equivalent'])

        # Academic strength index
        df['academic_index'] = 0
        if 'gpa_unweighted' in df.columns:
            df['academic_index'] += (df['gpa_unweighted'] / 4.0) * 40
        if 'standardized_test' in df.columns:
            df['academic_index'] += (df['standardized_test'] / 1600) * 40
        if 'num_ap_courses' in df.columns:
            df['academic_index'] += np.minimum(df['num_ap_courses'] / 10, 1.0) * 20

        return df

    def prepare_features(self, df: pd.DataFrame, target_school: str = None) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features and target for training"""

        # Filter by school if specified
        if target_school:
            df = df[df['school'] == target_school].copy()
            print(f"Filtered to {len(df)} records for {target_school}")

        # Encode target variable
        df['decision_binary'] = (df['decision'] == 'accepted').astype(int)

        # Select features
        feature_columns = [
            'gpa_unweighted',
            'gpa_weighted',
            'sat_total',
            'sat_math',
            'sat_ebrw',
            'act_composite',
            'num_ap_courses',
            'standardized_test',
            'academic_index',
            'gpa_difference',
            'sat_balance'
        ]

        # Add categorical features
        categorical_features = ['ethnicity', 'gender', 'intended_major']

        for col in categorical_features:
            if col in df.columns:
                # Encode categorical variables
                le = LabelEncoder()
                df[f'{col}_encoded'] = le.fit_transform(df[col].fillna('Unknown'))
                self.label_encoders[col] = le
                feature_columns.append(f'{col}_encoded')

        # Add boolean features
        boolean_features = ['first_gen', 'legacy']
        for col in boolean_features:
            if col in df.columns:
                df[col] = df[col].fillna(False).astype(int)
                feature_columns.append(col)

        # Keep only available features
        available_features = [col for col in feature_columns if col in df.columns]
        self.feature_names = available_features

        print(f"\nUsing {len(available_features)} features: {available_features}")

        # Prepare X and y
        X = df[available_features].fillna(df[available_features].median())
        y = df['decision_binary']

        print(f"\nClass distribution:")
        print(f"Accepted: {y.sum()} ({y.mean()*100:.1f}%)")
        print(f"Rejected: {len(y) - y.sum()} ({(1-y.mean())*100:.1f}%)")

        return X.values, y.values, df

    def train_model(self, X: np.ndarray, y: np.ndarray, model_type: str = 'xgboost') -> Dict:
        """Train the admission prediction model"""

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print(f"\nTraining {model_type} model...")
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")

        # Train model based on type
        if model_type == 'xgboost':
            self.model = xgb.XGBClassifier(
                max_depth=6,
                learning_rate=0.05,
                n_estimators=300,
                objective='binary:logistic',
                eval_metric='auc',
                random_state=42,
                use_label_encoder=False
            )

        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42
            )

        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=6,
                random_state=42
            )

        elif model_type == 'logistic':
            self.model = LogisticRegression(
                max_iter=1000,
                random_state=42
            )

        # Train
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }

        print(f"\nModel Performance:")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall: {metrics['recall']:.3f}")
        print(f"F1 Score: {metrics['f1']:.3f}")
        print(f"ROC AUC: {metrics['roc_auc']:.3f}")

        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Rejected', 'Accepted']))

        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)

            print(f"\nTop 10 Most Important Features:")
            print(feature_importance.head(10))

        return metrics

    def hyperparameter_tuning(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Perform hyperparameter tuning using GridSearchCV"""

        X_scaled = self.scaler.fit_transform(X)

        param_grid = {
            'max_depth': [4, 6, 8],
            'learning_rate': [0.01, 0.05, 0.1],
            'n_estimators': [200, 300, 500],
            'min_child_weight': [1, 3, 5]
        }

        xgb_model = xgb.XGBClassifier(
            objective='binary:logistic',
            eval_metric='auc',
            random_state=42,
            use_label_encoder=False
        )

        grid_search = GridSearchCV(
            xgb_model,
            param_grid,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        )

        print("Performing hyperparameter tuning...")
        grid_search.fit(X_scaled, y)

        print(f"\nBest parameters: {grid_search.best_params_}")
        print(f"Best ROC AUC: {grid_search.best_score_:.3f}")

        self.model = grid_search.best_estimator_

        return grid_search.best_params_

    def predict(self, applicant_data: Dict) -> Tuple[float, str]:
        """Predict admission probability for a new applicant"""

        # Convert applicant data to feature vector
        features = []
        for feature_name in self.feature_names:
            if feature_name.endswith('_encoded'):
                # Handle categorical features
                original_col = feature_name.replace('_encoded', '')
                value = applicant_data.get(original_col, 'Unknown')
                if original_col in self.label_encoders:
                    try:
                        encoded_value = self.label_encoders[original_col].transform([value])[0]
                    except:
                        encoded_value = 0  # Unknown category
                    features.append(encoded_value)
                else:
                    features.append(0)
            else:
                features.append(applicant_data.get(feature_name, 0))

        # Scale features
        features_scaled = self.scaler.transform([features])

        # Predict
        probability = self.model.predict_proba(features_scaled)[0][1]
        decision = "Accepted" if probability >= 0.5 else "Rejected"

        return probability, decision

    def save_model(self, filepath: str):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_names = model_data['feature_names']
        print(f"Model loaded from {filepath}")


def main():
    """Main training pipeline"""

    print("=" * 60)
    print("College Admissions ML Model Training")
    print("=" * 60)

    # Initialize model
    ml_model = AdmissionsMLModel()

    # Load data
    print("\n1. Loading data...")
    df = pd.read_csv('reddit_admissions_data.csv')

    # Engineer features
    print("\n2. Engineering features...")
    df = ml_model.engineer_features(df)

    # Prepare features
    print("\n3. Preparing features...")
    X, y, df_processed = ml_model.prepare_features(df)

    # Train model
    print("\n4. Training model...")
    metrics = ml_model.train_model(X, y, model_type='xgboost')

    # Optional: Hyperparameter tuning (takes longer)
    # print("\n5. Hyperparameter tuning...")
    # best_params = ml_model.hyperparameter_tuning(X, y)

    # Save model
    print("\n5. Saving model...")
    ml_model.save_model('admissions_model.pkl')

    # Save metrics
    with open('model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)

    # Example prediction
    print("\nExample prediction:")
    test_applicant = {
        'gpa_unweighted': 3.9,
        'gpa_weighted': 4.3,
        'sat_total': 1520,
        'sat_math': 780,
        'sat_ebrw': 740,
        'num_ap_courses': 8,
        'ethnicity': 'Asian',
        'gender': 'Female',
        'intended_major': 'Computer Science',
        'first_gen': False,
        'legacy': False
    }

    # Re-engineer features for test applicant
    test_df = pd.DataFrame([test_applicant])
    test_df = ml_model.engineer_features(test_df)
    test_dict = test_df.iloc[0].to_dict()

    probability, decision = ml_model.predict(test_dict)
    print(f"Admission probability: {probability:.1%}")
    print(f"Predicted decision: {decision}")


if __name__ == "__main__":
    main()
