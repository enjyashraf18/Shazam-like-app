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
