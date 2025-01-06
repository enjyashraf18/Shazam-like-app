import os
import glob
import csv
import pandas as pd  # used for checking for duplicates only
import librosa
import librosa.display
import numpy as np
from PIL import Image
import imagehash
import matplotlib.pyplot as plt


def process_files():
    for i in range(1, 21):
        team_directory = f"Data/Team_{i}"
        files = glob.glob(os.path.join(team_directory, '*'))  # the 3 files for each song

        for index, file in enumerate(files):
            song_name = file.split("\\")[1]
            print(f"Song name: {song_name}")
            y, sr = librosa.load(file, sr=None)
            hashed_features = extract_and_hash_features(y, sr)
            save_to_csv(hashed_features, i, song_name)


def extract_and_hash_features(y, sr):
    # y, sr = librosa.load(audio_path, sr=None)

    # Mel spectrogram: time-frequency representation where the frequency axis
    # is mapped to the Mel scale (a perceptual scale of frequencies)
    mel_spectro = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    mel_spectro_dB = librosa.power_to_db(mel_spectro, ref=np.max)

    # Heatmap of spectrogram
    fig = plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spectro_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000, cmap='magma')
    plt.axis('off')
    plt.tight_layout(pad=0)

    # Converting out plot to image arr
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    plt.close(fig)

    # Then convert arr to pil imagew
    pil_image = Image.fromarray(image[..., :3])

    hash_value = imagehash.phash(pil_image)  # perceptual hash
    return str(hash_value)


def save_to_csv(hashed_feature, team_id, song_name, csv_file='database.csv'):
    file_exists = os.path.isfile(csv_file)  # check if file exists (not really necessary)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:  # write header if the file doesn't exist
            writer.writerow(['Team ID', 'Song Name', 'Hashed Feature'])

        writer.writerow([team_id, song_name, hashed_feature])

    print(f"Saved features for team: {team_id}")



def find_duplicates(csv_file_path, column_name):
    try:
        df = pd.read_csv(csv_file_path)
        duplicates = df[df.duplicated(column_name, keep=False)]
        duplicates.to_csv('duplicates.csv', index=False)
        if not duplicates.empty:
            return duplicates
        else:
            return "No duplicate hashes found."
    except Exception as e:
        return f"Error finding duplicates: {e}"

# Start the process (ALREADY DONE)
# process_files()

# Checking if there are duplicate hashing (NONE)
# csv_file = "song_features.csv"
# column = "Feature Hash"
# result = find_duplicates(csv_file, column)
#
# print(result)


