import os
import glob
import librosa
import numpy as np
import hashlib
import csv


def process_files():
    for i in range(1, 21):
        team_directory = f"Data/Team_{i}"
        files = glob.glob(os.path.join(team_directory, '*'))  # the 3 files for each song

        for index, file in enumerate(files):
            # Index: 0 (Full) | 1 (Music) | 2 (Vocals)
            # NOTE: teams 1, 8, 10, 11, 13, 15, 16, 17, 18 are NOT following this format
            # SIDE NOTE: I'm not sure if we need to store the type of song (but it's easier to track this way)
            feature_dict = extract_features(file)
            hashed_features = hash_features(feature_dict)
            save_to_csv(hashed_features, i, index)


def extract_features(file_path, sr=22050, n_mfcc=13):
    """
    Mood (MFCC, Tonnetz)
    Melody or chords (Chromagram, Tonnetz)
    Energy or noisiness (ZCR, Spectral Centroid, Roll-Off)
    Richness or complexity (Spectral Contrast).

    """
    print(f"Processing file: {file_path}")
    audio, sr = librosa.load(file_path, sr=sr)

    # Useful to recognize type of instrument or voice
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

    # Useful for musical notes (C, D, C#) etc.
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)

    # Useful for the difference bet. the loud and quiet parts in a song
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)

    # Harmony of notes (happy, sad, etc.)
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sr)

    # How quickly the sound changes
    zcr = librosa.feature.zero_crossing_rate(y=audio)

    # Tells us if the song has more low-pitch (bass - drums) or high pitch (cymbal - whistle)
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)

    # Tells us the "balance of energy in the song" (whatever that means lol)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)

    return {
        'mfccs': mfccs,
        'chroma': chroma,
        'spectral_contrast': spectral_contrast,
        'tonnetz': tonnetz,
        'zcr': zcr,
        'spectral_centroid': spectral_centroid,
        'spectral_rolloff': spectral_rolloff
    }  # return dict of features to be hashed


def hash_features(features):
    combined_features = np.concatenate(
        [features['mfccs'].flatten(),
         features['chroma'].flatten(),
         features['spectral_contrast'].flatten(),
         features['tonnetz'].flatten(),
         features['zcr'].flatten(),
         features['spectral_centroid'].flatten(),
         features['spectral_rolloff'].flatten()]
    )

    feature_string = combined_features.tobytes()
    feature_hash = hashlib.sha256(feature_string).hexdigest()

    return feature_hash


def save_to_csv(hashed_feature, team_id, song_id, csv_file='song_features.csv'):
    file_exists = os.path.isfile(csv_file)  # check if file exists (not really necessary)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:  # write header if the file doesn't exist
            writer.writerow(['Team ID', 'Feature Hash'])

        writer.writerow([team_id, song_id, hashed_feature])

    print(f"Saved features for team: {team_id}")


process_files()  # Start the process
# ENSURE FILES ARE CORRECT FIRST BEFORE RUNNING
# BEC. THIS PROCESS TAKES TIME

