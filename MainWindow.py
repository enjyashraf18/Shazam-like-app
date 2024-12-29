import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog
from old_helper import extract_features, hash_features


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


    # def add_to_database(self):
    #     file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav)")
    #     if file_path:
    #         mfccs, chroma = extract_features(file_path)
    #         feature_hash = hash_features(mfccs, chroma)
    #         self.database[file_path] = feature_hash
    #         self.result_label.setText(f"Added to database: {os.path.basename(file_path)}")

    def compare_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav)")
        if file_path:
            features_dict = extract_features(file_path)
            feature_hash = hash_features(features_dict)

            for stored_path, stored_hash in self.database.items():
                if feature_hash == stored_hash:
                    self.result_label.setText(f"Match found: {os.path.basename(stored_path)}")
                    return

            self.result_label.setText("No match found in the database.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
