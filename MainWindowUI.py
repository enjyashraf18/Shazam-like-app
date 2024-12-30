import sys
import os
import csv

import imagehash
import librosa
import pandas as pd
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QSlider, \
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper import extract_and_hash_features

#
# def hamming_distance(hash1, hash2):
#     # Compute Hamming distance between two perceptual hashes (stored & the one to be compared)
#     return bin(hash1 - hash2).count('1')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load the UI file
        uic.loadUi('main.ui', self)
        self.setWindowTitle("BEATSEEK")
        self.setWindowIcon(QIcon("Deliverables/logo.png"))

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

        self.table = self.findChild(QTableWidget, "table")
        self.table.setRowCount(5)
        self.table.setColumnCount(3)

        # Set the headers for columns
        self.table.setHorizontalHeaderLabels(['Icon', 'Song', 'Similarity'])

        # Add data to the table
        # self.table.setItem(0, 0, QTableWidgetItem('Alice'))
        # self.table.setItem(0, 1, QTableWidgetItem('30'))
        #
        # self.table.setItem(1, 0, QTableWidgetItem('Bob'))
        # self.table.setItem(1, 1, QTableWidgetItem('25'))
        #
        # self.table.setItem(2, 0, QTableWidgetItem('Charlie'))
        # self.table.setItem(2, 1, QTableWidgetItem('35'))

        # Disable header clicks
        self.table.horizontalHeader().setSectionsClickable(False)
        self.table.verticalHeader().setSectionsClickable(False)

        # Set row and column sizes programmatically

        self.table.setColumnWidth(1, 494)
        self.table.setColumnWidth(0, 150)
        self.table.horizontalHeader().setFixedHeight(50)

        # Prevent user from resizing rows and columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Change the header color and match it with the first column
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #225971;
                border-radius: 10px;
                color: #f7e1d7;
                gridline-color: #16425b;
                font-size: 18px;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #f7e1d7;
                color: #16425b;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #16425b;
                font-size: 16px;
            }
            
            QTableWidget::item {
                padding: 5px;
            }
            
        """)

        self.table.horizontalHeader().setStyleSheet("""QHeaderView::section {
                background-color: #f7e1d7;
                color: #16425b;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #16425b;
                font-size: 16px;
            }
            QHeaderView::section:last{
            border-top-right-radius: 10px;
            }
            
        }""")

        corner_widget = self.table.findChild(QAbstractButton)
        if corner_widget:
            corner_widget.setStyleSheet("""
                    background-color: #f7e1d7;
                    border-top-left-radius: 10px;
                """)
            corner_widget.setEnabled(False)

        self.table.verticalHeader().setStyleSheet("""QHeaderView::section {
                background-color: #f7e1d7;
                color: #16425b;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #16425b;
                font-size: 16px;
            }
            QHeaderView::section:last{
            border-bottom-left-radius: 10px;
            }
            """)

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Access items in column 1
            if item:
                item.setTextAlignment(Qt.AlignCenter)
            self.table.setRowHeight(row, 150)

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

        self.input_hashes = [""] * 3
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

        self.weights = [100, 100]
        self.audio_files = None
        self.songs_path_file = [None, None]
        self.mixed_song_output = None
        self.curr_idx = 0
        self.detect_first_upload = False
        self.detect_second_upload = False

    def upload_song(self, index):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav)")
        if file_path:
            # extracting features of the song to be compared
            song_name = Path(file_path)
            song_name = song_name.stem
            if index == 0:
                self.songs_path_file[0] = file_path
                self.input_one_label.setText(song_name)
                self.curr_idx = 0
                self.detect_first_upload = True
            elif index == 1:
                self.songs_path_file[1] = file_path
                self.input_two_label.setText(song_name)
                self.curr_idx = 1
                self.detect_second_upload = True
            QApplication.processEvents()  # to change label before extracting features
            y, sr = librosa.load(file_path, sr=None)
            self.main_features_extractionn(index, y, sr)

    def main_features_extractionn(self,index, y, sr):
        uploaded_features_hashed = extract_and_hash_features(y, sr)
        self.input_hashes[index] = uploaded_features_hashed

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
                print(f"Hamming distance  {distance}")
                print(f"similarity  {similarity}")
                similarity_scores.append((row['Song Name'], distance, similarity))


            # sort 3la 7asb el distance
            # reminder en distance = 0 y3ni perfect match (no different bits)
            similarity_scores.sort(key=lambda x: x[1])
            self.display_results(similarity_scores)

        except Exception as e:
            print(f"Error: {e}")

        return similarity_scores  # to be used in showing results

    def display_results(self, similarity_scores):
        cover_photos_dir = Path("Cover Photos/")

        for row, (song_name, distance, similarity) in enumerate(similarity_scores):
            print(song_name)
            image_paths = list(cover_photos_dir.glob(f"{song_name}.*"))
            if image_paths:
                image_path = image_paths[0]
            else:
                image_path = "Cover Photos/Generic Cover.png"

            label = QLabel()
            cover_photo = QPixmap(str(image_path))

            label.setPixmap(cover_photo.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Center-align the image
            label.setAlignment(Qt.AlignCenter)

            # Add the QLabel to the table as a widget
            self.table.setCellWidget(row, 0, label)
            song_item = QTableWidgetItem(f"  {song_name}")
            similarity_item = QTableWidgetItem(f"{similarity * 100:.2f}%")  # Format similarity percentage
            similarity_item.setTextAlignment(Qt.AlignCenter)
            song_item.setFlags(song_item.flags() & ~Qt.ItemIsEditable)
            similarity_item.setFlags(similarity_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, song_item)
            self.table.setItem(row, 2, similarity_item)
            # print(f"Song: {song_id} || Similarity: {similarity_percentage}% || Hamming Distance:{distance} ")

    def play_mix(self):
        print("Play Mix Here")

    def update_weights(self, value, idx):
        self.weights[idx] = value
        self.mix_audios()

    def mix_audios(self):
        if self.input_hashes[0] is None or self.input_hashes[1] is None:
            print("one missinggg")
            return

        print("weslna henaaa 1")
        song1, sr1 = librosa.load(self.songs_path_file[0], sr=None)
        song2, sr2 = librosa.load(self.songs_path_file[1], sr=None)


        # some concerns
        if sr1 != sr2:
            song2 = librosa.resample(song2, orig_sr=sr2, target_sr=sr1)
            sr2 = sr1

        # match lengths
        min_length = min(len(song1), len(song2))
        song1 = song1[:min_length]
        song2 = song2[:min_length]



        song1_weight = self.weights[0] / 100
        song2_weight = self.weights[1] / 100
        new_song = (song1_weight * song1 + song2 * song2_weight) / (song1_weight + song2_weight)
        index = 2
        self.curr_idx = index

        self.main_features_extractionn(index, new_song, sr2)

    def convert_hex_to_bin(self, hex_string):
        # return bin(int(hex_string, 16))[2:].zfill(256)
        return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

    def hamming_distance(self, hash_code1, hash_code2):
        distance = 0

        hash_code1 = str(hash_code1)

        hash_code2 = str(hash_code2)

        # print(f"hena hash code 1 w  2 {hash_code1} + {hash_code2}")

        song1_bin = self.convert_hex_to_bin(hash_code1)
        song2_bin = self.convert_hex_to_bin(hash_code2)
        # print(f"hena hash code 1 w  2 binary {song1_bin} + {song2_bin}")

        for b1, b2 in zip(song1_bin, song2_bin):
            if b1 != b2:
                distance+=1
        return distance, hash_code1

    def get_similarity_idx(self, distance, hash_code1):
        # im not sure of total_bits tbh
        total_bits = len(hash_code1) * 4
        return 1- (distance / total_bits)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
