import numpy as np
import os
from hashlib import sha256
from imagehash import phash
from scipy.ndimage import maximum_filter
from PIL import Image

class ExtractFeaturesAndHahsing:
    def _init_(self):
        self.input_folder = "Spectrograms"
        self.feature_folder = "Features"
        self.hash_folder = "Hashes"
        os.makedirs(self.feature_folder, exist_ok=True)
        os.makedirs(self.hash_folder, exist_ok=True)

    def extract_features(self, spectrogram, threshold=0.5):
        max_filtered = maximum_filter(spectrogram, size=10)
        peaks = (spectrogram == max_filtered) & (spectrogram > threshold * np.max(spectrogram))

        feature_indices = np.argwhere(peaks)
        feature_values = spectrogram[peaks]

        # Combine indices and values
        features = np.hstack((feature_indices, feature_values[:, None]))
        return features

    def features_phash(self, features, canvas_size=256):
        if features.shape[0] == 0:
            # Skip if no features
            return None

        # Normalize the feature values (positions and intensity)
        max_row, max_col = np.max(features[:, :2], axis=0)
        normalized_rows = (features[:, 0] / max_row * (canvas_size - 1)).astype(int)
        normalized_cols = (features[:, 1] / max_col * (canvas_size - 1)).astype(int)
        feature_grid = np.zeros((canvas_size, canvas_size), dtype=np.uint8)

        for row, col, value in zip(normalized_rows, normalized_cols, features[:, 2]):
            # Clip the feature values to be within 0-1 before scaling
            clipped_value = np.clip(value, 0, 1)
            feature_grid[row, col] = int(clipped_value * 255)  # Scale feature values to the 0-255 range

        feature_image = Image.fromarray(feature_grid)
        return str(phash(feature_image))

   # Written to be excuted once
    def extract_and_save_75_features(self):
        for filename in os.listdir(self.input_folder):
            if filename.endswith(".npy"):
                file_path = os.path.join(self.input_folder, filename)

                spectrogram = np.load(file_path)

                features = self.extract_features(spectrogram)

                feature_path = os.path.join(self.feature_folder, filename)
                np.save(feature_path, features)

        print("Feature extraction complete. Files saved in:", self.feature_folder)


    # Written to be excuted once
    def generate_and_save_hashes(self):
        for filename in os.listdir(self.feature_folder):
            if filename.endswith(".npy"):
                file_path = os.path.join(self.feature_folder, filename)
                features = np.load(file_path)

                feature_phash = self.features_phash(features)

                # Only save the hash if it's not None
                if feature_phash is not None:
                    # Save the hash
                    hash_path = os.path.join(self.hash_folder, f"{os.path.splitext(filename)[0]}_hash.txt")
                    with open(hash_path, "w") as hash_file:
                        hash_file.write(feature_phash)
                else:
                    print(f"No features found in {filename}, skipping hash generation.")

        print("Hash generation complete. Files saved in:", self.hash_folder)