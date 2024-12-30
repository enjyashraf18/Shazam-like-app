# import os
# import glob
# import librosa
# import numpy as np
# # import hashlib
# import csv
# import pandas as pd  # used for checking for duplicates only
# from sklearn.preprocessing import MinMaxScaler
# from imagehash import phash
# from PIL import Image
#
#
# def process_files():
#     for i in range(1, 21):
#         team_directory = f"Data/Team_{i}"
#         files = glob.glob(os.path.join(team_directory, '*'))  # the 3 files for each song
#
#         for index, file in enumerate(files):
#             song_name = file.split("\\")[1]
#             print(f"Song name: {song_name}")
#             hashed_features = extract_and_hash_features(file)
#             save_to_csv(hashed_features, i, song_name)
#
#
# def extract_features(file_path, sr=22050, n_mfcc=13):
#     """
#     Mood (MFCC, Tonnetz)
#     Melody or chords (Chromagram, Tonnetz)
#     Energy or noisiness (ZCR, Spectral Centroid, Roll-Off)
#     Richness or complexity (Spectral Contrast).
#
#     """
#     print(f"Processing file: {file_path}")
#     audio, sr = librosa.load(file_path, sr=sr)
#
#     # Useful to recognize type of instrument or voice
#     mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
#
#     # Useful for musical notes (C, D, C#) etc.
#     chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
#
#     # Useful for the difference bet. the loud and quiet parts in a song
#     spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
#
#     # Harmony of notes (happy, sad, etc.)
#     tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sr)
#
#     # How quickly the sound changes
#     zcr = librosa.feature.zero_crossing_rate(y=audio)
#
#     # Tells us if the song has more low-pitch (bass - drums) or high pitch (cymbal - whistle)
#     spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
#
#     # Tells us the "balance of energy in the song" (whatever that means lol)
#     spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)
#
#     return {
#         'mfccs': mfccs,
#         'chroma': chroma,
#         'spectral_contrast': spectral_contrast,
#         'tonnetz': tonnetz,
#         'zcr': zcr,
#         'spectral_centroid': spectral_centroid,
#         'spectral_rolloff': spectral_rolloff
#     }  # return dict of features to be hashed
#
#
# def aggregate_features(features_dict):
#     aggregated_features = {}
#     for key, value in features_dict.items():
#         # Compute mean and variance along the time axis
#         aggregated_features[key] = {
#             'mean': np.mean(value, axis=1),
#             'variance': np.var(value, axis=1)
#         }
#     return aggregated_features
#
#
# def normalize_features(aggregated_features):
#     flattened_features = []
#     for key, stats in aggregated_features.items():
#         flattened_features.extend(stats['mean'])
#         flattened_features.extend(stats['variance'])
#
#     flattened_features = np.array(flattened_features).reshape(-1, 1)
#     scaler = MinMaxScaler()  # normalize between 0 and 1
#     normalized_features = scaler.fit_transform(flattened_features).flatten()
#     return normalized_features
#
#
# def generate_perceptual_hash(feature_vector, hash_size=8):
#     size = int(np.ceil(np.sqrt(len(feature_vector))))  # reshape the feature vector into a square image
#     padded_vector = np.pad(feature_vector, (0, size ** 2 - len(feature_vector)), mode='constant')
#     feature_image = padded_vector.reshape((size, size))
#
#     # Convert to an image and compute perceptual hash
#     image = Image.fromarray((feature_image * 255).astype(np.uint8))
#     return phash(image, hash_size=hash_size)
#
#
# def extract_and_hash_features(file_path, sr=22050, n_mfcc=13):  # To be called when comparing
#     features = extract_features(file_path, sr=sr, n_mfcc=n_mfcc)
#     aggregated = aggregate_features(features)
#     normalized = normalize_features(aggregated)
#     return generate_perceptual_hash(normalized)
#
#
# def save_to_csv(hashed_feature, team_id, song_name, csv_file='song_features.csv'):
#     file_exists = os.path.isfile(csv_file)  # check if file exists (not really necessary)
#
#     with open(csv_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#
#         if not file_exists:  # write header if the file doesn't exist
#             writer.writerow(['Team ID', 'Song Name', 'Feature Hash'])
#
#         writer.writerow([team_id, song_name, hashed_feature])
#
#     print(f"Saved features for team: {team_id}")
#
#
# def find_duplicates(csv_file_path, column_name):
#     try:
#         df = pd.read_csv(csv_file_path)
#         duplicates = df[df.duplicated(column_name, keep=False)]
#         duplicates.to_csv('duplicates.csv', index=False)
#         if not duplicates.empty:
#             return duplicates
#         else:
#             return "No duplicate hashes found."
#     except Exception as e:
#         return f"Error finding duplicates: {e}"
#
# # Start the process ( ALREADY DONE)
# # process_files()
#
# # Checking if there are duplicate hashing
# # csv_file = "song_features.csv"
# # column = "Feature Hash"
# # result = find_duplicates(csv_file, column)
# #
# # print(result)
#
#
