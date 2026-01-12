"""
Audio Feature Extraction Module
Extracts acoustic features from speech audio for dementia detection
"""
import numpy as np
import librosa
import io
from typing import Dict

def extract_audio_features(audio_data: bytes, sr: int = 22050) -> Dict[str, float]:
    """
    Extract acoustic features from audio for dementia detection
    
    Features extracted:
    - MFCCs (Mel-frequency cepstral coefficients) - Voice quality
    - Pitch variation (fundamental frequency) - Speech patterns
    - Speech rate (zero crossing rate) - Speaking speed
    - Spectral features - Voice characteristics
    - Energy features - Volume patterns
    - Pause patterns - Speech fluency
    
    Args:
        audio_data: Audio file bytes (WAV format)
        sr: Sample rate (default 22050 Hz)
    
    Returns:
        Dictionary of extracted features
    """
    try:
        # Load audio from bytes
        audio_io = io.BytesIO(audio_data)
        y, sr = librosa.load(audio_io, sr=sr)
        
        # Remove silence at beginning and end
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)
        
        features = {}
        
        # 1. MFCC Features (most important for speech analysis)
        mfccs = librosa.feature.mfcc(y=y_trimmed, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs, axis=1).tolist()
        features['mfcc_std'] = np.std(mfccs, axis=1).tolist()
        features['mfcc_mean_avg'] = float(np.mean(mfccs))
        features['mfcc_std_avg'] = float(np.std(mfccs))
        
        # 2. Pitch Features (F0 - fundamental frequency)
        pitches, magnitudes = librosa.piptrack(y=y_trimmed, sr=sr)
        pitch_values = pitches[pitches > 0]
        
        if len(pitch_values) > 0:
            features['pitch_mean'] = float(np.mean(pitch_values))
            features['pitch_std'] = float(np.std(pitch_values))
            features['pitch_min'] = float(np.min(pitch_values))
            features['pitch_max'] = float(np.max(pitch_values))
            features['pitch_range'] = features['pitch_max'] - features['pitch_min']
        else:
            features['pitch_mean'] = 0.0
            features['pitch_std'] = 0.0
            features['pitch_min'] = 0.0
            features['pitch_max'] = 0.0
            features['pitch_range'] = 0.0
        
        # 3. Zero Crossing Rate (speech rate indicator)
        zcr = librosa.feature.zero_crossing_rate(y_trimmed)
        features['zcr_mean'] = float(np.mean(zcr))
        features['zcr_std'] = float(np.std(zcr))
        
        # 4. Spectral Features (voice characteristics)
        spectral_centroids = librosa.feature.spectral_centroid(y=y_trimmed, sr=sr)
        features['spectral_centroid_mean'] = float(np.mean(spectral_centroids))
        features['spectral_centroid_std'] = float(np.std(spectral_centroids))
        
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y_trimmed, sr=sr)
        features['spectral_rolloff_mean'] = float(np.mean(spectral_rolloff))
        
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y_trimmed, sr=sr)
        features['spectral_bandwidth_mean'] = float(np.mean(spectral_bandwidth))
        
        # 5. Energy Features (volume patterns)
        rms = librosa.feature.rms(y=y_trimmed)
        features['rms_mean'] = float(np.mean(rms))
        features['rms_std'] = float(np.std(rms))
        
        # 6. Tempo (speech rate)
        tempo, _ = librosa.beat.beat_track(y=y_trimmed, sr=sr)
        features['tempo'] = float(tempo)
        
        # 7. Duration and Pause Features
        features['duration'] = float(len(y) / sr)
        features['trimmed_duration'] = float(len(y_trimmed) / sr)
        features['pause_ratio'] = float(1 - (len(y_trimmed) / len(y)))
        
        # 8. Chroma Features (pitch class distribution)
        chroma = librosa.feature.chroma_stft(y=y_trimmed, sr=sr)
        features['chroma_mean'] = float(np.mean(chroma))
        features['chroma_std'] = float(np.std(chroma))
        
        # 9. Spectral Contrast
        contrast = librosa.feature.spectral_contrast(y=y_trimmed, sr=sr)
        features['contrast_mean'] = float(np.mean(contrast))
        features['contrast_std'] = float(np.std(contrast))
        
        return features
        
    except Exception as e:
        print(f"Error extracting audio features: {e}")
        return get_default_features()

def get_default_features() -> Dict[str, float]:
    """Return default features if extraction fails"""
    return {
        'mfcc_mean': [0.0] * 13,
        'mfcc_std': [0.0] * 13,
        'mfcc_mean_avg': 0.0,
        'mfcc_std_avg': 0.0,
        'pitch_mean': 0.0,
        'pitch_std': 0.0,
        'pitch_min': 0.0,
        'pitch_max': 0.0,
        'pitch_range': 0.0,
        'zcr_mean': 0.0,
        'zcr_std': 0.0,
        'spectral_centroid_mean': 0.0,
        'spectral_centroid_std': 0.0,
        'spectral_rolloff_mean': 0.0,
        'spectral_bandwidth_mean': 0.0,
        'rms_mean': 0.0,
        'rms_std': 0.0,
        'tempo': 0.0,
        'duration': 0.0,
        'trimmed_duration': 0.0,
        'pause_ratio': 0.0,
        'chroma_mean': 0.0,
        'chroma_std': 0.0,
        'contrast_mean': 0.0,
        'contrast_std': 0.0
    }

def features_to_array(features: Dict[str, float]) -> np.ndarray:
    """
    Convert feature dictionary to numpy array for ML model input
    
    Args:
        features: Dictionary of extracted features
    
    Returns:
        Numpy array of features (1, n_features)
    """
    feature_list = []
    
    # Add scalar features in consistent order
    scalar_keys = [
        'mfcc_mean_avg', 'mfcc_std_avg',
        'pitch_mean', 'pitch_std', 'pitch_range',
        'zcr_mean', 'zcr_std',
        'spectral_centroid_mean', 'spectral_centroid_std',
        'spectral_rolloff_mean', 'spectral_bandwidth_mean',
        'rms_mean', 'rms_std',
        'tempo', 'duration', 'trimmed_duration', 'pause_ratio',
        'chroma_mean', 'chroma_std',
        'contrast_mean', 'contrast_std'
    ]
    
    for key in scalar_keys:
        feature_list.append(features.get(key, 0.0))
    
    return np.array(feature_list).reshape(1, -1)

def analyze_speech_quality(features: Dict[str, float]) -> Dict[str, str]:
    """
    Analyze speech quality indicators from features
    
    Returns:
        Dictionary with quality indicators
    """
    quality = {}
    
    # Analyze pitch variation
    if features['pitch_std'] < 20:
        quality['pitch_variation'] = 'Low (monotone speech)'
    elif features['pitch_std'] < 50:
        quality['pitch_variation'] = 'Normal'
    else:
        quality['pitch_variation'] = 'High (expressive speech)'
    
    # Analyze speech rate
    if features['zcr_mean'] < 0.05:
        quality['speech_rate'] = 'Slow'
    elif features['zcr_mean'] < 0.15:
        quality['speech_rate'] = 'Normal'
    else:
        quality['speech_rate'] = 'Fast'
    
    # Analyze pause patterns
    if features['pause_ratio'] > 0.3:
        quality['pause_pattern'] = 'Frequent pauses'
    elif features['pause_ratio'] > 0.1:
        quality['pause_pattern'] = 'Normal pauses'
    else:
        quality['pause_pattern'] = 'Continuous speech'
    
    return quality