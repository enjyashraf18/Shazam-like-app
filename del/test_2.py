import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
file_path = '../Data/Music.wav'  # Replace with your WAV file path
audio, sr = librosa.load(file_path, sr=None)  # sr=None to preserve original sampling rate

# Compute MFCCs
n_mfcc = 13  # Number of MFCCs to extract
mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

# Compute Chromagram
chromagram = librosa.feature.chroma_stft(y=audio, sr=sr)

# Plot MFCCs
plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, x_axis='time', sr=sr, cmap='coolwarm')
plt.colorbar(format='%+2.0f dB')
plt.title('MFCCs')
plt.tight_layout()
plt.show()

# Plot Chromagram
plt.figure(figsize=(10, 4))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', cmap='coolwarm', sr=sr)
plt.colorbar()
plt.title('Chromagram')
plt.tight_layout()
plt.show()

# Print MFCC and Chromagram arrays
print("MFCCs shape:", mfccs.shape)  # (n_mfcc, frames)
print("Chromagram shape:", chromagram.shape)  # (12, frames)


def compare_audios(self):
    csv_file = "database.csv"
    try:
        df = pd.read_csv(csv_file)
        if self.detect_first_upload and self.detect_second_upload:
            print("hell man it worked")
            self.mix_audios()

        input_hash_obj = imagehash.hex_to_hash(self.input_hashes[self.curr_idx])  # input hash to perceptual hash
        print(f"input_hash_obj: {input_hash_obj}")
        similarity_scores = []  # will carry song id & hamming distance with the uploaded song
        for index, row in df.iterrows():
            csv_hash_obj = imagehash.hex_to_hash(row['Hashed Feature'])
            # print(f"csv_hash_obj: {csv_hash_obj}")
            distance, hash_code = self.hamming_distance(input_hash_obj, csv_hash_obj)
            similarity = self.get_similarity_idx(distance, hash_code)
            print(f"Hamming distance  {distance}, song: {row["Song Name"]}")
            print(f"similarity  {similarity}")
            similarity_scores.append((row['Team ID'], distance, similarity))

        # sort 3la 7asb el distance
        # reminder en distance = 0 y3ni perfect match (no different bits)
        similarity_scores.sort(key=lambda x: x[1])
        self.display_results(similarity_scores)

    except Exception as e:
        print(f"Error: {e}")

    return similarity_scores  # to be used in showing results
