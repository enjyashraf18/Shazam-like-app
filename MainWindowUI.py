import sys
import os
import csv

import imagehash
import pandas as pd
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QSlider
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper import extract_and_hash_features


def hamming_distance(hash1, hash2):
    # Compute Hamming distance between two perceptual hashes (stored & the one to be compared)
    return bin(hash1 - hash2).count('1')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load the UI file
        uic.loadUi('main.ui', self)
        self.setWindowTitle("BEATSEEK")
        self.setWindowIcon(QIcon("Deliverables/icon.png"))

        self.browse_song_btn_one = self.findChild(QPushButton, "browse_song1")
        self.browse_song_btn_two = self.findChild(QPushButton, "browse_song2")
        self.match_button = self.findChild(QPushButton, "match_button")
        self.play_mix_btn = self.findChild(QPushButton, "mix_play")
        self.song_one_cover = self.findChild(QLabel, "song_cover1")
        self.song_two_cover = self.findChild(QLabel, "song_cover2")
        self.generic_song_cover = QPixmap("Cover Photos/Generic Cover.png")
        self.song_one_cover.setPixmap(self.generic_song_cover)
        self.song_two_cover.setPixmap(self.generic_song_cover)
        self.input_one_label = self.findChild(QLabel, "song_name1")
        self.input_two_label = self.findChild(QLabel, "song_name2")

        self.browse_song_btn_one.clicked.connect(lambda: self.upload_song(0))
        self.browse_song_btn_two.clicked.connect(lambda: self.upload_song(1))
        self.match_button.clicked.connect(self.compare_audios)
        self.play_mix_btn.clicked.connect(self.play_mix)

        song1_slider = self.findChild(QSlider, "song_slider1")
        song1_slider.setRange(0, 100)
        song1_slider.setValue(100)
        song1_slider.valueChanged.connect(lambda value, index=0: self.update_weights(value, index))

        song2_slider = self.findChild(QSlider, "song_slider2")
        song2_slider.setRange(0, 100)
        song2_slider.setValue(100)
        song2_slider.valueChanged.connect(lambda value, index=1: self.update_weights(value, index))

        self.input_hashes = [""] * 2
        self.song_names = {
            1: "Save Your Tears",
            3: "Someone Like You",
            5: "Nina Cried Power",
            6: "Alkanas",
            7: "Sweet Dreams",
            8: "A Thousand Years",
            9: "Please Please Please",
            10: "Wen Elkhael",
            11: "FE!IN",
            13: "Let Her Go",
            14: "Sky Full of Stars",
            15: "Ya Lala",
            16: "Something Just Like That",
            17: "Shake it Out",
            18: "Rolling in the Deep",
            19: "Shadow of Mine",
            20: "Hit the Road Jack"
        }

        self.weights = [100] * 2
        self.audio_files = [None, None]

    def upload_song(self, index):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav)")
        if file_path:
            # extracting features of the song to be compared
            song_name = Path(file_path)
            song_name = song_name.stem
            if index == 0:
                # self.songs_files[index] = file_path
                self.input_one_label.setText(song_name)
            elif index == 1:
                # self.songs_files[index] = file_path
                self.input_two_label.setText(song_name)
            QApplication.processEvents()  # to change label before extracting features
            uploaded_features_hashed = extract_and_hash_features(file_path)
            self.input_hashes[index] = uploaded_features_hashed

    def compare_audios(self):
        csv_file = "database.csv"
        try:
            df = pd.read_csv(csv_file)

            input_hash_obj = imagehash.hex_to_hash(self.input_hashes[0])  # input hash to perceptual hash

            similarity_scores = []  # will carry song id & hamming distance with the uploaded song
            for index, row in df.iterrows():
                csv_hash_obj = imagehash.hex_to_hash(row['Hashed Feature'])
                distance = hamming_distance(input_hash_obj, csv_hash_obj)
                # similarity_scores.append((row['Team ID'], distance))
                similarity_scores.append((row['Song Name'], distance))

            similarity_scores.sort(key=lambda x: x[1])  # smaller distance means more similar

            # THIS IS WHAT WE WILL SHOW IN UI
            for song_id, dist in similarity_scores:
                similarity_percentage = max(0, 100 - dist * 10)  # ADJUST THIS SCALE?
                # print(f"Song: {self.song_names[song_id]}, Similarity: {similarity_percentage}%, Hamming Distance: {dist}")
                print(
                    f"Song: {song_id} || Similarity: {similarity_percentage}% || Hamming Distance: {dist}")

        except Exception as e:
            print(f"Error: {e}")

        return similarity_scores  # to be used in showing results

    def display_results(self, stored_song_id):
        print(f"Match found: {self.song_names[int(stored_song_id)]}")
        cover_photos_dir = Path("Cover Photos/")
        image_paths = list(cover_photos_dir.glob(f"{self.song_names[int(stored_song_id)]}.*"))
        if image_paths:
            image_path = image_paths[0]
        else:
            image_path = "Cover Photos/Generic Cover.png"
        cover_photo = QPixmap(str(image_path))
        self.song_one_cover.setPixmap(cover_photo.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def play_mix(self):
        print("Play Mix Here")

    def update_weights(self, value, idx):
        self.weights[idx] = value
        self.combine_features()

    def combine_features(self):
        song1_weight = self.weights[0] / 100
        song2_weight = self.weights[1] / 100

    def convert_hex_to_bin(self, hex_string):
        pass

    # def hamming_distance(self, hash_code1, hash_code2):  # THIS IS YOURS YA ENJY
    #     song1_bin = self.convert_hex_to_bin(hash_code1)
    #     song2_bin = self.convert_hex_to_bin(hash_code2)

    # msh 3arfa bs from that --> similarity index
    # pass for now

    def get_similarity_idx(self):
        # nakhod result el hamming_distance
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
