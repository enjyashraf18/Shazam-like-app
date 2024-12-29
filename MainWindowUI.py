import sys
import os
import csv
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from helper import extract_features, hash_features


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

    def upload_song(self, index):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav)")
        if file_path:
            # extracting features of the song to be compared
            song_name = Path(file_path)
            song_name = song_name.stem
            if index == 0:
                self.input_one_label.setText(song_name)
            elif index == 1:
                self.input_two_label.setText(song_name)
            QApplication.processEvents()  # to change label before extracting features
            uploaded_features_dict = extract_features(file_path)
            uploaded_features_hash = hash_features(uploaded_features_dict)
            self.input_hashes[index] = uploaded_features_hash

    def compare_audios(self):
        csv_file_path = "song_features.csv"
        try:
            with open(csv_file_path, mode="r", newline="", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if len(row) < 3:
                        continue  # skip invalid rows (probably not necessary)
                    stored_song_id, stored_hash = row[0], row[2]
                    if self.input_hashes[0] == stored_hash:  # MODIFY TO USE SIMILARITY (ENJY)
                        self.display_results(stored_song_id)  # REPLACE WITH LIST OF MATCHES IDS
                        # We want to return multiple matches
                        return
            print("No match found in the database.")
        except FileNotFoundError:
            print("CSV file not found.")
        except Exception as e:
            print(f"Error: {e}")

    def display_results(self, stored_song_id):
        print(f"Match found: {self.song_names[int(stored_song_id)]}")
        cover_photos_dir = Path("Cover Photos/")
        image_paths = list(cover_photos_dir.glob(f"{self.song_names[int(stored_song_id)]}.*"))
        if image_paths:
            image_path = image_paths[0]
        else:
            image_path = "Cover Photos/Generic Cover.png"
        cover_photo = QPixmap(str(image_path))
        self.song_one_cover.setPixmap(cover_photo.scaled(130, 130))
    def play_mix(self):
        print("Play Mix Here")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
