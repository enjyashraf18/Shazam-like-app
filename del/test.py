# import librosa
# import librosa.display
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal import find_peaks
# file_path = '../Data/Music.wav'
# audio, sr = librosa.load(file_path, sr=None)
# S = librosa.stft(audio)
# S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
# plt.figure(figsize=(10, 5))
# librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
# plt.colorbar(format='%+2.0f dB')
# plt.title('Spectrogram')
# plt.xlabel('Time (s)')
# plt.ylabel('Frequency (Hz)')
# plt.show()
#
# # # Find peaks in the spectrogram (FEATURE??)
# # peaks = find_peaks(S_db.mean(axis=1), height=-40)
# # peak_freqs = librosa.fft_frequencies(sr=sr)[peaks[0]]
# #
# # print("Peak Frequencies:", peak_freqs)
#
# def create_spectrogram():
#
# def extract_mfccs():  # USE THIS
# # Extracts Mel-frequency cepstral coefficients (MFCCs) directly from the audio waveform.
# def extract_chroma():  # AND THIS
#
# def extract_zero_crossings():
#
# def extract_spectral_contrast():  # MAYBE THIS?
#
#
#
# def extract_features(self, signal_var, fs):
#     # You can use different feature extraction techniques here
#     # For example, use MFCCs
#     signal_var = signal_var / np.max(np.abs(signal_var))
#     mfcc_features = mfcc(signal_var, fs)
#     return mfcc_features
#
# def extract_combined_features(self):
#     x, sample_rate = librosa.load(self.audio_path)
#     normalized_x = librosa.util.normalize(x)
#     # MFCC extraction
#     mfcc = np.mean(
#         librosa.feature.mfcc(y=normalized_x, sr=sample_rate, n_mfcc=50), axis=1
#     )
#     # Chroma Features extraction
#     chroma = np.mean(
#         librosa.feature.chroma_stft(y=normalized_x, sr=sample_rate), axis=1
#     )
#     # Zero Crossing Rate (ZCR) calculation
#     zcr = np.mean(librosa.feature.zero_crossing_rate(y=normalized_x), axis=1)
#     # Spectral Centroid
#     spectrogram = np.mean((np.abs(librosa.stft(normalized_x))), axis=1)
#     # Spectral Contrast
#     contrast = np.mean(
#         librosa.feature.spectral_contrast(y=normalized_x, sr=sample_rate), axis=1
#     )
#     # Combine features
#     combined_features = np.concatenate([mfcc, zcr, contrast, spectrogram, chroma])
#
#     return combined_features
