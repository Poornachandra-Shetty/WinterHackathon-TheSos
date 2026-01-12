import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
import os

print("Creating synthetic training dataset...")

# Create synthetic training data matching frontend inputs
# Features: word_score, memory_score, reaction_time
training_data = pd.DataFrame({
    "word_score": [95, 88, 92, 85, 30, 25, 35, 28, 90, 75, 20, 40, 87, 78, 22, 38, 93, 82, 18, 45],
    "memory_score": [6, 5, 7, 5, 2, 1, 2, 1, 6, 4, 1, 3, 5, 4, 1, 2, 7, 5, 1, 3],
    "reaction_time": [250, 280, 230, 350, 1200, 1400, 1100, 1300, 200, 400, 1500, 900, 300, 420, 1450, 1000, 240, 380, 1550, 850]
})

# Binary labels: 0 = Low risk, 1 = High risk
labels = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]

print(f"Dataset created: {len(training_data)} samples")
print(f"Features: {list(training_data.columns)}")
print(f"Class distribution: {pd.Series(labels).value_counts().to_dict()}")

# Initialize and train the LogisticRegression model
print("\nTraining LogisticRegression model...")
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(training_data, labels)

print("Model training complete!")

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Save the trained model
model_path = "models/ai_model.pkl"
joblib.dump(model, model_path)

print(f"\n✅ Model saved successfully to '{model_path}'")
print("Training complete! Model is ready for inference.")