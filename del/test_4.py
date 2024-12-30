# import librosa
# import librosa.display
# import numpy as np
# from PIL import Image
# import imagehash
# import matplotlib.pyplot as plt
#
#
# def compute_perceptual_hash(audio_path):
#     # Load the audio file
#     y, sr = librosa.load(audio_path, sr=None)
#
#     # Generate Mel spectrogram
#     S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
#     S_dB = librosa.power_to_db(S, ref=np.max)
#
#     # Save the spectrogram as an image in memory (no file needed)
#     fig = plt.figure(figsize=(10, 4))
#     librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000, cmap='magma')
#     plt.axis('off')  # Hide axes
#     plt.tight_layout(pad=0)
#
#     # Convert the spectrogram to a PIL image using buffer_rgba
#     fig.canvas.draw()
#     image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
#     image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # RGBA has 4 channels
#     plt.close(fig)
#
#     # Convert to RGB (dropping alpha channel) and create a PIL image
#     pil_image = Image.fromarray(image[..., :3])
#
#     # Compute the perceptual hash
#     hash_value = imagehash.phash(pil_image)
#     return str(hash_value)
#
#
# if __name__ == "__main__":
#     path = "../Data/Team_1/save-your-tears(original).wav"
#     perceptual_hash = compute_perceptual_hash(path)
#     print("Perceptual Hash:", perceptual_hash)
