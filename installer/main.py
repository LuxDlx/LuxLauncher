import sys
import os
import ctypes
import subprocess
import requests
import zipfile
import shutil
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox,
                             QFileDialog, QLineEdit, QLabel, QProgressBar, QHBoxLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    class InstallerThread(QThread):
        progress_signal = pyqtSignal(str, int)
        finished_signal = pyqtSignal()

        def __init__(self, install_path):
            super().__init__()
            self.install_path = install_path

        def run(self):
            self.progress_signal.emit("Downloading Java...", 0)
            java_url = "https://github.com/adoptium/temurin23-binaries/releases/download/jdk-23.0.1%2B11/OpenJDK23U-jdk_x64_windows_hotspot_23.0.1_11.zip"
            response = requests.get(java_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            written = 0

            with open("java.zip", "wb") as f:
                for data in response.iter_content(block_size):
                    written += len(data)
                    f.write(data)
                    progress = int((written / total_size) * 100)
                    self.progress_signal.emit("Downloading Java...", progress)

            self.progress_signal.emit("Creating directories...", 50)
            try:
                if os.path.exists(os.path.join(self.install_path, ".qwertz", "java")):
                    shutil.rmtree(os.path.join(self.install_path, ".qwertz", "java"))
            except:
                pass
            os.makedirs(os.path.join(self.install_path, ".qwertz", "java"), exist_ok=True)

            self.progress_signal.emit("Extracting Java...", 60)
            with zipfile.ZipFile("java.zip", "r") as zip_ref:
                for file in zip_ref.namelist():
                    if file.startswith("jdk-23.0.1+11/") and not len(file) <= len("jdk-23.0.1+11/"): # prevent moving dir
                        extracted_path = zip_ref.extract(file, os.path.join(self.install_path, ".qwertz", "java"))
                        renamed_path = os.path.join(os.path.join(self.install_path, ".qwertz", "java"), file.replace("jdk-23.0.1+11/", ""))
                        if not os.path.exists(renamed_path):
                            os.renames(extracted_path, renamed_path)
            
            jdk_folder = os.path.join(os.path.join(self.install_path, ".qwertz", "java"), "jdk-23.0.1+11")
            if os.path.exists(jdk_folder):
                os.rmdir(jdk_folder)
                    
            self.progress_signal.emit("Copying LuxLauncher...", 80)
            launcher_path = resource_path("LuxLauncher.exe")
            shutil.copy(launcher_path, os.path.join(self.install_path, "Lux Delux.exe"))

            self.progress_signal.emit("Cleaning up...", 90)
            os.remove("java.zip")

            self.progress_signal.emit("Installation Complete!", 100)
            self.finished_signal.emit()

    class InstallerWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowIcon(QIcon(resource_path("icon.ico")))
            self.initUI()

        def initUI(self):
            self.setWindowTitle('LuxLauncher Installer')
            self.setFixedSize(500, 300)
            self.setStyleSheet("""
                QWidget {
                    background-color: #2E3440;
                    color: #ECEFF4;
                    font-family: 'Segoe UI', sans-serif;
                }
                QPushButton {
                    background-color: #5E81AC;
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #81A1C1;
                }
                QPushButton:pressed {
                    background-color: #4C566A;
                }
                QLineEdit {
                    background-color: #3B4252;
                    border: 1px solid #4C566A;
                    padding: 5px;
                    border-radius: 3px;
                }
                QProgressBar {
                    border: 2px solid #4C566A;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #88C0D0;
                    width: 10px;
                    margin: 0.5px;
                }
            """)

            layout = QVBoxLayout()

            self.question_label = QLabel("Do you want to install LuxLauncher?")
            self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.question_label.setFont(QFont('Segoe UI', 16))
            layout.addWidget(self.question_label)

            button_layout = QHBoxLayout()
            self.yes_button = QPushButton('Yes')
            self.yes_button.clicked.connect(self.on_yes)
            button_layout.addWidget(self.yes_button)

            self.no_button = QPushButton('No')
            self.no_button.clicked.connect(self.close)
            button_layout.addWidget(self.no_button)
            layout.addLayout(button_layout)

            self.path_label = QLabel("Installation Path:")
            self.path_label.hide()
            layout.addWidget(self.path_label)

            path_layout = QHBoxLayout()
            self.path_entry = QLineEdit()
            self.path_entry.setText(r"C:\Program Files (x86)\Lux")
            self.path_entry.hide()
            path_layout.addWidget(self.path_entry)

            self.browse_button = QPushButton('Browse')
            self.browse_button.clicked.connect(self.browse_path)
            self.browse_button.hide()
            path_layout.addWidget(self.browse_button)
            layout.addLayout(path_layout)

            self.install_button = QPushButton('Install')
            self.install_button.clicked.connect(self.start_installation)
            self.install_button.hide()
            layout.addWidget(self.install_button)

            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            self.progress_bar.hide()
            layout.addWidget(self.progress_bar)

            self.progress_label = QLabel("")
            self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.progress_label)
            footer_layout = QHBoxLayout()
            footer_text = QLabel("Developed by QWERTZ")
            footer_text.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
            footer_layout.addWidget(footer_text)
            layout.addLayout(footer_layout)
            self.setLayout(layout)

        def on_yes(self):
            self.question_label.hide()
            self.yes_button.hide()
            self.no_button.hide()
            self.path_label.show()
            self.path_entry.show()
            self.browse_button.show()
            self.install_button.show()
            self.progress_bar.show()

        def browse_path(self):
            path = QFileDialog.getExistingDirectory(self, "Select Installation Directory")
            if path:
                self.path_entry.setText(path)

        def start_installation(self):
            install_path = self.path_entry.text()
            self.install_thread = InstallerThread(install_path)
            self.install_thread.progress_signal.connect(self.update_progress)
            self.install_thread.finished_signal.connect(self.installation_finished)
            self.install_thread.start()
            self.install_button.setEnabled(False)

        def update_progress(self, message, value):
            self.progress_label.setText(message)
            self.progress_bar.setValue(value)

        def installation_finished(self):
            QMessageBox.information(self, "Installation Complete", "LuxLauncher has been installed successfully!")
            self.close()

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        installer = InstallerWindow()
        installer.show()
        sys.exit(app.exec())
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)