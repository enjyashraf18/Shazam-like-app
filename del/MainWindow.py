import sys
import os
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog
from helper import extract_features, hash_features


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = {}  # dictionary to store audio hashes
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Shazam")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        # self.upload_button = QPushButton("Upload and Add to Database")
        self.compare_button = QPushButton("Upload and Compare to Database")
        self.result_label = QLabel("")
        # self.icon_label = QIcon("Deliverables/icon.png")

        # self.upload_button.clicked.connect(self.add_to_database)
        self.compare_button.clicked.connect(self.compare_audio)

        # layout.addWidget(self.upload_button)
        layout.addWidget(self.compare_button)
        layout.addWidget(self.result_label)

        # layout.addWidget(self.icon_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def compare_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav)")
        if file_path:
            # extracting features of the song to be compared
            uploaded_features_dict = extract_features(file_path)
            uploaded_features_hash = hash_features(uploaded_features_dict)

            csv_file_path = "song_features.csv"  # Replace with the actual path to your CSV file
            try:
                with open(csv_file_path, mode="r", newline="", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        if len(row) < 3:
                            continue  # skip invalid rows (probably not necessary)
                        stored_song_name, stored_hash = row[1], row[2]
                        if uploaded_features_hash == stored_hash:
                            self.result_label.setText(f"Match found: {os.path.basename(stored_song_name)}")
                            # We want to return multiple matches
                            return

                self.result_label.setText("No match found in the database.")
            except FileNotFoundError:
                self.result_label.setText("CSV file not found.")
            except Exception as e:
                self.result_label.setText(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
