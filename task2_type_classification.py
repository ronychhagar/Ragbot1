"""
Task 2: Binary Classification of Type Column
This module handles:
1. Loading and merging two CSV tables on ID column
2. Analyzing the Type column
3. Binary classification model training and inference
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, List
import pickle
import logging

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TypeClassifier:
    """Binary classifier for Type column"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.classifier = None
        self.label_encoder = LabelEncoder()
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.type_counts = {}
    
    def load_and_merge_data(self, table1_path: str = "table_1.csv", table2_path: str = "table_2.csv") -> pd.DataFrame:
        """
        Load two CSV tables and merge them on ID column.
        
        Args:
            table1_path: Path to first CSV file
            table2_path: Path to second CSV file
            
        Returns:
            Merged DataFrame
        """
        try:
            # Load tables
            table1_path_full = self.data_dir / table1_path
            table2_path_full = self.data_dir / table2_path
            
            logger.info(f"Loading table 1: {table1_path_full}")
            df1 = pd.read_csv(table1_path_full)
            
            logger.info(f"Loading table 2: {table2_path_full}")
            df2 = pd.read_csv(table2_path_full)
            
            # Merge on ID
            logger.info("Merging tables on ID column")
            merged = pd.merge(df1, df2, on="ID", how="inner")
            
            logger.info(f"Merged shape: {merged.shape}")
            logger.info(f"Columns: {merged.columns.tolist()}")
            
            return merged
        
        except Exception as e:
            logger.error(f"Error loading/merging data: {e}")
            raise
    
    def analyze_type_column(self, df: pd.DataFrame) -> Dict:
        """
        Analyze the Type column for classification potential.
        
        Args:
            df: Merged DataFrame
            
        Returns:
            Analysis results dictionary
        """
        analysis = {
            "total_records": len(df),
            "unique_types": df["Type"].nunique(),
            "type_distribution": df["Type"].value_counts().to_dict(),
            "missing_values": df["Type"].isna().sum(),
            "is_binary": df["Type"].nunique() == 2
        }
        
        logger.info(f"Type Column Analysis:")
        logger.info(f"  - Total records: {analysis['total_records']}")
        logger.info(f"  - Unique types: {analysis['unique_types']}")
        logger.info(f"  - Missing values: {analysis['missing_values']}")
        logger.info(f"  - Binary classification: {analysis['is_binary']}")
        logger.info(f"  - Distribution: {analysis['type_distribution']}")
        
        self.type_counts = analysis['type_distribution']
        return analysis
    
    def prepare_data(self, df: pd.DataFrame, feature_columns: List[str] = None) -> Tuple:
        """
        Prepare data for classification.
        
        Args:
            df: DataFrame with Type column to classify
            feature_columns: List of feature columns (if None, uses all except ID and Type)
            
        Returns:
            X_train, X_test, y_train, y_test
        """
        # Remove rows with missing Type values
        df_clean = df.dropna(subset=["Type"])
        
        # Identify feature columns
        if feature_columns is None:
            feature_columns = [col for col in df_clean.columns if col not in ["ID", "Type"]]
        
        logger.info(f"Using features: {feature_columns}")
        
        # Prepare features and target
        X = df_clean[feature_columns].fillna(0)
        y = df_clean["Type"]
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        logger.info(f"Data split - Train: {X_train.shape}, Test: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def train_classifier(self, X_train, y_train) -> Dict:
        """
        Train the binary classifier.
        
        Args:
            X_train: Training features
            y_train: Training labels
            
        Returns:
            Training metrics
        """
        logger.info("Training Random Forest classifier...")
        
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.classifier.fit(X_train, y_train)
        
        logger.info("✅ Classifier trained successfully")
        
        # Get feature importance
        feature_names = X_train.columns.tolist()
        importances = self.classifier.feature_importances_
        importance_dict = dict(zip(feature_names, importances))
        
        logger.info("Top 5 important features:")
        for feat, imp in sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
            logger.info(f"  - {feat}: {imp:.4f}")
        
        return importance_dict
    
    def evaluate_classifier(self, X_test, y_test) -> Dict:
        """
        Evaluate the classifier on test data.
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Evaluation metrics
        """
        if self.classifier is None:
            raise ValueError("Classifier not trained yet")
        
        y_pred = self.classifier.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        logger.info(f"\n✅ Model Evaluation:")
        logger.info(f"  - Accuracy: {accuracy:.4f}")
        logger.info(f"  - Confusion Matrix:\n{cm}")
        
        # Classification report
        class_names = self.label_encoder.classes_
        report = classification_report(y_test, y_pred, target_names=class_names)
        logger.info(f"Classification Report:\n{report}")
        
        return {
            "accuracy": accuracy,
            "confusion_matrix": cm.tolist(),
            "classification_report": report
        }
    
    def predict(self, X_new) -> Tuple[List, List[float]]:
        """
        Make predictions on new data.
        
        Args:
            X_new: New feature data
            
        Returns:
            Predictions and probabilities
        """
        if self.classifier is None:
            raise ValueError("Classifier not trained yet")
        
        predictions = self.classifier.predict(X_new)
        probabilities = self.classifier.predict_proba(X_new)
        
        # Decode labels back to original type names
        predictions_decoded = self.label_encoder.inverse_transform(predictions)
        
        return predictions_decoded, probabilities
    
    def save_model(self, model_path: str = "type_classifier.pkl"):
        """Save trained model to file"""
        if self.classifier is None:
            raise ValueError("No trained classifier to save")
        
        model_data = {
            "classifier": self.classifier,
            "label_encoder": self.label_encoder,
            "vectorizer": self.vectorizer
        }
        
        with open(model_path, "wb") as f:
            pickle.dump(model_data, f)
        
        logger.info(f"✅ Model saved to {model_path}")
    
    def load_model(self, model_path: str = "type_classifier.pkl"):
        """Load trained model from file"""
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
        
        self.classifier = model_data["classifier"]
        self.label_encoder = model_data["label_encoder"]
        self.vectorizer = model_data["vectorizer"]
        
        logger.info(f"✅ Model loaded from {model_path}")


def run_classification_pipeline() -> Tuple[TypeClassifier, Dict]:
    """
    Run complete classification pipeline.
    
    Returns:
        Classifier object and results dictionary
    """
    logger.info("\n" + "="*60)
    logger.info("TASK 2: Binary Classification of Type Column")
    logger.info("="*60)
    
    classifier = TypeClassifier()
    results = {}
    
    try:
        # Load and merge data
        df_merged = classifier.load_and_merge_data()
        
        # Analyze Type column
        analysis = classifier.analyze_type_column(df_merged)
        results["analysis"] = analysis
        
        # Prepare data
        X_train, X_test, y_train, y_test = classifier.prepare_data(df_merged)
        
        # Train classifier
        importance = classifier.train_classifier(X_train, y_train)
        results["feature_importance"] = importance
        
        # Evaluate classifier
        eval_metrics = classifier.evaluate_classifier(X_test, y_test)
        results["evaluation"] = eval_metrics
        
        # Save model
        classifier.save_model()
        
        logger.info("\n✅ Classification pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        results["error"] = str(e)
    
    return classifier, results


if __name__ == "__main__":
    classifier, results = run_classification_pipeline()
