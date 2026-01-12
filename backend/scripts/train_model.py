"""
ML Model Training Script
Trains Random Forest model for dementia risk prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support
)
import joblib
import os

def train_dementia_model():
    """Train ML model for dementia risk prediction"""
    
    print("=" * 70)
    print(" " * 15 + "DEMENTIA SCREENING MODEL TRAINING")
    print("=" * 70)
    
    # ==================== LOAD DATA ====================
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv')
    
    if not os.path.exists(data_path):
        print("\n❌ ERROR: Data file not found!")
        print(f"   Expected location: {data_path}")
        print("\n   Please run generate_data.py first to create training data:")
        print("   $ python scripts/generate_data.py")
        return
    
    print(f"\n[1/7] Loading data from {os.path.basename(data_path)}...")
    df = pd.read_csv(data_path)
    print(f"      ✓ Loaded {len(df)} samples with {len(df.columns)} features")
    
    # ==================== PREPARE FEATURES ====================
    print(f"\n[2/7] Preparing features...")
    
    feature_columns = [
        'word_score',
        'memory_score',
        'reaction_time',
        'errors',
        'completion_time'
    ]
    
    X = df[feature_columns].values
    
    # Create derived/engineered features
    X_enhanced = np.column_stack([
        X,
        X[:, 2] / 1000,              # reaction_time in seconds
        X[:, 1] / 9.0,               # normalized memory score (0-1)
        X[:, 0] / 100.0,             # normalized word score (0-1)
        X[:, 3] / np.maximum(X[:, 4], 1),  # error rate
    ])
    
    feature_names = feature_columns + [
        'reaction_sec',
        'memory_norm',
        'word_norm',
        'error_rate'
    ]
    
    print(f"      ✓ Created {X_enhanced.shape[1]} features (including {len(feature_names) - len(feature_columns)} derived features)")
    
    # Encode labels
    label_map = {'low': 0, 'moderate': 1, 'high': 2}
    y = df['risk_level'].map(label_map).values
    
    # ==================== SPLIT DATA ====================
    print(f"\n[3/7] Splitting data into training and test sets...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_enhanced, y,
        test_size=0.2,
        random_state=42,
        stratify=y  # Maintain class distribution
    )
    
    print(f"      ✓ Training set: {len(X_train)} samples ({len(X_train)/len(df)*100:.1f}%)")
    print(f"      ✓ Test set:     {len(X_test)} samples ({len(X_test)/len(df)*100:.1f}%)")
    
    # ==================== SCALE FEATURES ====================
    print(f"\n[4/7] Scaling features...")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"      ✓ Features scaled using StandardScaler")
    
    # ==================== TRAIN MODEL ====================
    print(f"\n[5/7] Training Random Forest Classifier...")
    
    model = RandomForestClassifier(
        n_estimators=100,        # Number of trees
        max_depth=10,            # Maximum tree depth
        min_samples_split=5,     # Minimum samples to split node
        min_samples_leaf=2,      # Minimum samples in leaf
        random_state=42,
        class_weight='balanced', # Handle class imbalance
        n_jobs=-1               # Use all CPU cores
    )
    
    model.fit(X_train_scaled, y_train)
    print(f"      ✓ Model trained with {model.n_estimators} trees")
    
    # ==================== EVALUATE MODEL ====================
    print(f"\n[6/7] Evaluating model performance...")
    
    # Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Accuracy
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    print(f"\n      {'─' * 60}")
    print(f"      ACCURACY SCORES")
    print(f"      {'─' * 60}")
    print(f"      Training Accuracy:   {train_accuracy:.2%}")
    print(f"      Test Accuracy:       {test_accuracy:.2%}")
    
    # Cross-validation
    try:
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        print(f"      Cross-Val Score:     {cv_scores.mean():.2%} (+/- {cv_scores.std()*2:.2%})")
    except ValueError as e:
        cv_scores = None
        print(f"      ⚠ Cross-Validation skipped: {e}")
    
    # Classification Report
    print(f"\n      {'─' * 60}")
    print(f"      CLASSIFICATION REPORT (Test Set)")
    print(f"      {'─' * 60}")
    target_names = ['Low Risk', 'Moderate Risk', 'High Risk']
    print(classification_report(y_test, y_test_pred, target_names=target_names))
    
    # Confusion Matrix
    print(f"      {'─' * 60}")
    print(f"      CONFUSION MATRIX (Test Set)")
    print(f"      {'─' * 60}")
    cm = confusion_matrix(y_test, y_test_pred)
    print(f"\n      Predicted →")
    print(f"      Actual ↓     Low    Mod    High")
    for i, label in enumerate(['Low', 'Mod', 'High']):
        print(f"      {label:8s}    {cm[i, 0]:4d}   {cm[i, 1]:4d}   {cm[i, 2]:4d}")
    
    # Feature Importance
    print(f"\n      {'─' * 60}")
    print(f"      FEATURE IMPORTANCE")
    print(f"      {'─' * 60}")
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    for i in range(min(10, len(feature_names))):
        idx = indices[i]
        print(f"      {i+1:2d}. {feature_names[idx]:20s} {importances[idx]:.4f}")
    
    # ==================== SAVE MODEL ====================
    print(f"\n[7/7] Saving model and scaler...")
    
    # Create models directory
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(models_dir, 'ai_model.pkl')
    joblib.dump(model, model_path)
    print(f"      ✓ Model saved to: {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"      ✓ Scaler saved to: {scaler_path}")
    
    # Save feature names
    feature_names_path = os.path.join(models_dir, 'feature_names.txt')
    with open(feature_names_path, 'w') as f:
        f.write('\n'.join(feature_names))
    print(f"      ✓ Feature names saved to: {feature_names_path}")
    
    # ==================== SUMMARY ====================
    print(f"\n{'=' * 70}")
    print(" " * 20 + "TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\n  Model Performance Summary:")
    print(f"  ├─ Test Accuracy:      {test_accuracy:.2%}")
    print(f"  ├─ Cross-Val Score:    {cv_scores.mean():.2%}")
    print(f"  └─ Number of Features: {len(feature_names)}")
    
    # Per-class performance
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_test_pred, labels=[0,1,2], zero_division=0)
    print(f"\n  Per-Class Performance:")
    for i, label in enumerate(target_names):
        print(f"  ├─ {label:15s} Precision: {precision[i]:.2%}  Recall: {recall[i]:.2%}  F1: {f1[i]:.2%}")
    
    print(f"\n  Files saved in: {models_dir}/")
    print(f"  ├─ ai_model.pkl")
    print(f"  ├─ scaler.pkl")
    print(f"  └─ feature_names.txt")
    
    print(f"\n{'=' * 70}")
    print("  Next step: Start the API server using 'python main.py'")
    print("=" * 70)
    
    return model, scaler, test_accuracy

def plot_results(y_test, y_test_pred):
    """
    Plot confusion matrix and feature importance
    (Requires matplotlib & seaborn - optional visualization)
    """
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("\n      ⚠ Matplotlib/seaborn not available - skipping plots")
        return

    # Confusion Matrix Plot
    cm = confusion_matrix(y_test, y_test_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
               xticklabels=['Low', 'Moderate', 'High'],
               yticklabels=['Low', 'Moderate', 'High'])
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'))
    print("\n      ✓ Confusion matrix plot saved")

if __name__ == "__main__":
    train_dementia_model()