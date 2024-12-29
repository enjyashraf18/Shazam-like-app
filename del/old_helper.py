import librosa
import numpy as np
import hashlib


def extract_features(audio_path, sr=22050, n_mfcc=13):
    audio, sr = librosa.load(audio_path, sr=sr)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    return mfccs, chroma


def hash_features(mfccs, chroma):
    mfccs_flat = mfccs.flatten()
    chroma_flat = chroma.flatten()
    combined_features = np.concatenate((mfccs_flat, chroma_flat))
    feature_string = combined_features.tobytes()
    feature_hash = hashlib.sha256(feature_string).hexdigest()
    return feature_hash