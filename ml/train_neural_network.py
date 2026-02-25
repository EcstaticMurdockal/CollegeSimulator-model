"""
Neural Network Model for College Admissions Prediction
Implements deep learning approach with TensorFlow/Keras
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import json
from typing import Dict, Tuple

class NeuralNetworkAdmissionsModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.history = None

    def build_model(self, input_dim: int, architecture: str = 'deep') -> keras.Model:
        """
        Build neural network architecture

        Architectures:
        - 'simple': 2 hidden layers (good for <1k examples)
        - 'medium': 3 hidden layers (good for 1k-5k examples)
        - 'deep': 4 hidden layers (good for 5k+ examples)
        - 'very_deep': 5 hidden layers (good for 10k+ examples)
        """

        if architecture == 'simple':
            model = keras.Sequential([
                layers.Input(shape=(input_dim,)),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(1, activation='sigmoid')
            ])

        elif architecture == 'medium':
            model = keras.Sequential([
                layers.Input(shape=(input_dim,)),
                layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.4),
                layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.2),
                layers.Dense(1, activation='sigmoid')
            ])

        elif architecture == 'deep':
            model = keras.Sequential([
                layers.Input(shape=(input_dim,)),
                layers.Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.4),
                layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.2),
                layers.Dense(1, activation='sigmoid')
            ])

        elif architecture == 'very_deep':
            model = keras.Sequential([
                layers.Input(shape=(input_dim,)),
                layers.Dense(1024, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.4),
                layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.2),
                layers.Dense(1, activation='sigmoid')
            ])

        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.AUC(name='auc'), keras.metrics.Precision(), keras.metrics.Recall()]
        )

        return model

    def train_model(self, X: np.ndarray, y: np.ndarray, architecture: str = 'deep',
                   epochs: int = 100, batch_size: int = 32, validation_split: float = 0.2) -> Dict:
        """Train neural network model"""

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print(f"\nTraining Neural Network ({architecture} architecture)...")
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Input features: {X_train.shape[1]}")

        # Build model
        self.model = self.build_model(X_train.shape[1], architecture)

        print(f"\nModel Architecture:")
        self.model.summary()

        # Callbacks
        callbacks = [
            # Early stopping: stop if validation loss doesn't improve for 15 epochs
            EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            # Reduce learning rate when validation loss plateaus
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.00001,
                verbose=1
            ),
            # Save best model
            ModelCheckpoint(
                'best_nn_model.h5',
                monitor='val_auc',
                save_best_only=True,
                mode='max',
                verbose=1
            )
        ]

        # Handle class imbalance
        class_weight = self._calculate_class_weights(y_train)

        # Train
        print(f"\nTraining for up to {epochs} epochs...")
        self.history = self.model.fit(
            X_train_scaled, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=callbacks,
            class_weight=class_weight,
            verbose=1
        )

        # Evaluate on test set
        print(f"\nEvaluating on test set...")
        y_pred_proba = self.model.predict(X_test_scaled).flatten()
        y_pred = (y_pred_proba >= 0.5).astype(int)

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }

        print(f"\nNeural Network Performance:")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall: {metrics['recall']:.3f}")
        print(f"F1 Score: {metrics['f1']:.3f}")
        print(f"ROC AUC: {metrics['roc_auc']:.3f}")

        return metrics

    def _calculate_class_weights(self, y: np.ndarray) -> Dict:
        """Calculate class weights to handle imbalanced data"""
        from sklearn.utils.class_weight import compute_class_weight

        classes = np.unique(y)
        weights = compute_class_weight('balanced', classes=classes, y=y)
        class_weight = dict(zip(classes, weights))

        print(f"\nClass weights (to handle imbalance): {class_weight}")
        return class_weight

    def predict(self, applicant_data: Dict) -> Tuple[float, str]:
        """Predict admission probability for a new applicant"""

        # Convert applicant data to feature vector
        features = []
        for feature_name in self.feature_names:
            if feature_name.endswith('_encoded'):
                original_col = feature_name.replace('_encoded', '')
                value = applicant_data.get(original_col, 'Unknown')
                if original_col in self.label_encoders:
                    try:
                        encoded_value = self.label_encoders[original_col].transform([value])[0]
                    except:
                        encoded_value = 0
                    features.append(encoded_value)
                else:
                    features.append(0)
            else:
                features.append(applicant_data.get(feature_name, 0))

        # Scale features
        features_scaled = self.scaler.transform([features])

        # Predict
        probability = self.model.predict(features_scaled, verbose=0)[0][0]
        decision = "Accepted" if probability >= 0.5 else "Rejected"

        return float(probability), decision

    def save_model(self, filepath: str):
        """Save trained model to disk"""
        # Save Keras model
        self.model.save(f"{filepath}_keras.h5")

        # Save preprocessing objects
        preprocessing = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }
        joblib.dump(preprocessing, f"{filepath}_preprocessing.pkl")

        print(f"Model saved to {filepath}_keras.h5 and {filepath}_preprocessing.pkl")

    def load_model(self, filepath: str):
        """Load trained model from disk"""
        # Load Keras model
        self.model = keras.models.load_model(f"{filepath}_keras.h5")

        # Load preprocessing objects
        preprocessing = joblib.load(f"{filepath}_preprocessing.pkl")
        self.scaler = preprocessing['scaler']
        self.label_encoders = preprocessing['label_encoders']
        self.feature_names = preprocessing['feature_names']

        print(f"Model loaded from {filepath}")

    def plot_training_history(self):
        """Plot training history"""
        import matplotlib.pyplot as plt

        if self.history is None:
            print("No training history available")
            return

        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Train')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # Loss
        axes[0, 1].plot(self.history.history['loss'], label='Train')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # AUC
        axes[1, 0].plot(self.history.history['auc'], label='Train')
        axes[1, 0].plot(self.history.history['val_auc'], label='Validation')
        axes[1, 0].set_title('Model AUC')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('AUC')
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        # Precision & Recall
        axes[1, 1].plot(self.history.history['precision'], label='Train Precision')
        axes[1, 1].plot(self.history.history['val_precision'], label='Val Precision')
        axes[1, 1].plot(self.history.history['recall'], label='Train Recall')
        axes[1, 1].plot(self.history.history['val_recall'], label='Val Recall')
        axes[1, 1].set_title('Precision & Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Score')
        axes[1, 1].legend()
        axes[1, 1].grid(True)

        plt.tight_layout()
        plt.savefig('nn_training_history.png', dpi=300, bbox_inches='tight')
        print("Training history plot saved to nn_training_history.png")
        plt.show()


def main():
    """Main training pipeline for neural network"""

    print("=" * 60)
    print("Neural Network College Admissions Model Training")
    print("=" * 60)

    # Load data (reuse preprocessing from train_model.py)
    from train_model import AdmissionsMLModel

    ml_model = AdmissionsMLModel()
    df = pd.read_csv('reddit_admissions_data.csv')
    df = ml_model.engineer_features(df)
    X, y, df_processed = ml_model.prepare_features(df)

    # Initialize neural network
    nn_model = NeuralNetworkAdmissionsModel()
    nn_model.feature_names = ml_model.feature_names
    nn_model.label_encoders = ml_model.label_encoders

    # Determine architecture based on data size
    data_size = len(X)
    if data_size < 1000:
        architecture = 'simple'
        print(f"\nData size: {data_size} - Using SIMPLE architecture")
    elif data_size < 5000:
        architecture = 'medium'
        print(f"\nData size: {data_size} - Using MEDIUM architecture")
    elif data_size < 10000:
        architecture = 'deep'
        print(f"\nData size: {data_size} - Using DEEP architecture")
    else:
        architecture = 'very_deep'
        print(f"\nData size: {data_size} - Using VERY DEEP architecture")

    # Train model
    metrics = nn_model.train_model(
        X, y,
        architecture=architecture,
        epochs=100,
        batch_size=32,
        validation_split=0.2
    )

    # Save model
    nn_model.save_model('admissions_nn_model')

    # Save metrics
    with open('nn_model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    # Plot training history
    nn_model.plot_training_history()

    print("\n" + "=" * 60)
    print("Neural Network Training Complete!")
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

    test_df = pd.DataFrame([test_applicant])
    test_df = ml_model.engineer_features(test_df)
    test_dict = test_df.iloc[0].to_dict()

    probability, decision = nn_model.predict(test_dict)
    print(f"Admission probability: {probability:.1%}")
    print(f"Predicted decision: {decision}")


if __name__ == "__main__":
    main()
