import librosa
import numpy as np
from pathlib import Path


def extract_audio_features(file_path):
    """
    Extract numeric features from a .wav audio file for machine learning.

    Args:
        file_path (str or Path): Path to the .wav audio file

    Returns:
        list: A 1D array of 17 numeric features
    """

    try:
        # Convert to Path object (safe for Windows/Linux)
        file_path = Path(file_path)

        # Check if file exists BEFORE loading
        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # Load audio
        y, sr = librosa.load(file_path, sr=None)

        # Check if audio is valid
        if y is None or len(y) == 0:
            raise ValueError("Loaded audio is empty")

        # -------- Feature Extraction --------

        # 1–13: MFCCs (mean over time)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs, axis=1)

        # 14: Zero Crossing Rate (mean)
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = np.mean(zcr)

        # 15: Spectral Centroid (mean)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_centroid_mean = np.mean(spectral_centroid)

        # 16: Spectral Bandwidth (mean)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        spectral_bandwidth_mean = np.mean(spectral_bandwidth)

        # 17: RMS Energy (mean)
        rms = librosa.feature.rms(y=y)
        rms_mean = np.mean(rms)

        # Combine all features
        features = np.concatenate([
            mfccs_mean,
            [zcr_mean, spectral_centroid_mean, spectral_bandwidth_mean, rms_mean]
        ])

        return features.tolist()

    except Exception as e:
        print("❌ Audio feature extraction failed!")
        print(e)
        return [0.0] * 17


# ---------------- usage ----------------
if __name__ == "__main__":
    audio_folder = Path(__file__).parent / "audio_data"

for wav_file in audio_folder.glob("*.wav"):
    print(f"\nProcessing: {wav_file.name}")
    features = extract_audio_features(wav_file)
    print(features)


