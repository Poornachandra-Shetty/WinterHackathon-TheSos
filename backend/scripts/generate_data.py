"""
Training Data Generation Script
Generates synthetic dementia screening data for model training

WARNING: This generates synthetic data for development/testing only.
Do NOT use for actual medical diagnosis or research.
"""
import pandas as pd
import numpy as np
import os

def generate_synthetic_data(n_samples=1000, output_file='data.csv'):
    """
    Generate synthetic dementia screening data
    
    Creates realistic but synthetic patient data with different risk levels
    
    Args:
        n_samples: Number of samples to generate (default 1000)
        output_file: Output CSV filename (default 'data.csv')
    
    Returns:
        DataFrame with generated data
    """
    print("=" * 60)
    print("GENERATING SYNTHETIC DEMENTIA SCREENING DATA")
    print("=" * 60)
    print(f"\nGenerating {n_samples} samples...")
    
    np.random.seed(42)  # For reproducibility
    
    data = []
    
    for i in range(n_samples):
        # Randomly assign actual risk level for this sample
        actual_risk = np.random.choice(
            ['low', 'moderate', 'high'],
            p=[0.50, 0.30, 0.20]  # 50% low, 30% moderate, 20% high
        )
        
        # Generate features based on risk level
        if actual_risk == 'low':
            # Low risk - Good performance
            word_score = np.random.randint(70, 100)
            memory_score = np.random.randint(6, 10)
            reaction_time = np.random.randint(200, 450)
            errors = np.random.randint(0, 3)
            completion_time = np.random.randint(60, 180)
            
        elif actual_risk == 'moderate':
            # Moderate risk - Average performance with some concerns
            word_score = np.random.randint(40, 75)
            memory_score = np.random.randint(3, 7)
            reaction_time = np.random.randint(400, 650)
            errors = np.random.randint(2, 8)
            completion_time = np.random.randint(150, 300)
            
        else:  # high risk
            # High risk - Poor performance
            word_score = np.random.randint(0, 50)
            memory_score = np.random.randint(0, 4)
            reaction_time = np.random.randint(600, 1200)
            errors = np.random.randint(5, 20)
            completion_time = np.random.randint(250, 600)
        
        # Add realistic noise/variation
        word_score = np.clip(word_score + np.random.randint(-10, 10), 0, 100)
        memory_score = np.clip(memory_score + np.random.randint(-1, 2), 0, 9)
        reaction_time = max(100, reaction_time + np.random.randint(-50, 50))
        errors = max(0, errors + np.random.randint(-1, 2))
        completion_time = max(30, completion_time + np.random.randint(-20, 20))
        
        # Add age factor (older age correlates with higher risk)
        age = np.random.randint(50, 90)
        
        data.append({
            'patient_id': f'P{i:04d}',
            'age': age,
            'word_score': word_score,
            'memory_score': memory_score,
            'reaction_time': reaction_time,
            'errors': errors,
            'completion_time': completion_time,
            'risk_level': actual_risk
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(data_dir, output_file)
    df.to_csv(output_path, index=False)
    
    # Print statistics
    print(f"\n✓ Generated {n_samples} samples successfully")
    print(f"✓ Saved to: {output_path}")
    
    print(f"\n{'-' * 60}")
    print("RISK LEVEL DISTRIBUTION:")
    print(f"{'-' * 60}")
    risk_counts = df['risk_level'].value_counts()
    for risk, count in risk_counts.items():
        percentage = (count / len(df)) * 100
    print(f"  {str(risk).upper():12s}: {count:4d} samples ({percentage:5.1f}%)")
    
    print(f"\n{'-' * 60}")
    print("FEATURE STATISTICS:")
    print(f"{'-' * 60}")
    stats_df = df[['word_score', 'memory_score', 'reaction_time', 'errors', 'completion_time']].describe()
    print(stats_df)
    
    print(f"\n{'-' * 60}")
    print("SAMPLE DATA (First 5 rows):")
    print(f"{'-' * 60}")
    print(df.head())
    
    print(f"\n{'-' * 60}")
    print("AVERAGE VALUES BY RISK LEVEL:")
    print(f"{'-' * 60}")
    grouped = df.groupby('risk_level')[['word_score', 'memory_score', 'reaction_time', 'errors']].mean()
    print(grouped)
    
    print(f"\n{'=' * 60}")
    print("DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nNext step: Run train_model.py to train the ML model")
    
    return df

def validate_data(df):
    """
    Validate generated data for quality
    
    Args:
        df: DataFrame to validate
    
    Returns:
        Boolean indicating if data is valid
    """
    issues = []
    
    # Check for missing values
    if df.isnull().any().any():
        issues.append("Missing values detected")
    
    # Check value ranges
    if (df['word_score'] < 0).any() or (df['word_score'] > 100).any():
        issues.append("word_score out of range [0, 100]")
    
    if (df['memory_score'] < 0).any() or (df['memory_score'] > 9).any():
        issues.append("memory_score out of range [0, 9]")
    
    if (df['reaction_time'] < 0).any():
        issues.append("reaction_time has negative values")
    
    if (df['errors'] < 0).any():
        issues.append("errors has negative values")
    
    if issues:
        print("\n⚠ VALIDATION ISSUES:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n✓ Data validation passed")
        return True

if __name__ == "__main__":
    # Generate data
    df = generate_synthetic_data(n_samples=1000, output_file='data.csv')
    
    # Validate data
    validate_data(df)