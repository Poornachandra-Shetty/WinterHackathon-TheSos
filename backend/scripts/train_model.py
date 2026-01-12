import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the training data from CSV file (path resolved relative to script file)
print("Loading training data...")
data_file = Path(__file__).resolve().parent.parent / 'data' / 'data.csv'
print(f"Reading data from {data_file}")
data = pd.read_csv(data_file)

# Display basic information about the dataset
print(f"Dataset loaded: {data.shape[0]} samples, {data.shape[1]} columns")
print(f"Column names: {list(data.columns)}")
print(f"\nClass distribution:")
print(data['label'].value_counts())

# Separate features (X) and target labels (y)
feature_columns = ['memory_score', 'reaction_time', 'errors', 'completion_time']
X = data[feature_columns]
y = data['label']

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Ensure balanced class distribution in train/test splits
)

print(f"\nTraining set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# Initialize the machine learning model
# RandomForestClassifier is chosen for:
# - High accuracy and robustness
# - Explainability (feature importance)
# - Good performance with small datasets
model = RandomForestClassifier(
    n_estimators=100,      # Number of trees in the forest
    max_depth=10,          # Maximum depth of each tree
    random_state=42,       # For reproducibility
    n_jobs=-1              # Use all CPU cores for faster training
)

# Train the model on the training data
print("\nTraining the model...")
model.fit(X_train, y_train)

# Evaluate the model on the test set
print("\nEvaluating model performance...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Low Risk', 'High Risk']))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Display feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)

# Save the trained model to a file
model_filename = 'ai_model.pkl'
joblib.dump(model, model_filename)
print(f"\nModel saved successfully as '{model_filename}'")
print("Training complete!")

