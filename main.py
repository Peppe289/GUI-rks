import sys
import ctypes
import time
import psutil

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QVBoxLayout, QGroupBox
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class get_online_cpu_thread(QThread):
    update_label_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        #cpu_usage = libRKM.cpu_load
        #cpu_usage.restype = ctypes.c_int
        while(1):
            #text = cpu_usage()
            text = psutil.cpu_percent()
            # print(text)
            text = "CPU Usage: " + str(text) + "%"
            # Emit the update_label_signal with the new label text
            self.update_label_signal.emit(text)
            time.sleep(1)

class get_cpu_thread(QThread):
    update_label_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        cpu_online = libRKM.online_cpu
        cpu_online.restype = ctypes.c_int
        while(1):
            text = cpu_online()
            # print(text)
            text = "CPU Online: " + str(text)
            # Emit the update_label_signal with the new label text
            self.update_label_signal.emit(text)
            time.sleep(1)

def load_libRKM():
    global libRKM
    libRKM = ctypes.CDLL('./src/libRKM.so')

def set_dark_theme(app):
    # Create a dark color palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    app.setPalette(dark_palette)

def show_popup():
    message_box = QMessageBox()
    message_box.setWindowTitle("Some Error")
    message_box.setText("I can't make this. Maybe u need to start this as root")
    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

def clear_label():
    global counter
    counter = counter + 1

    if counter > 10:
        label.setText("")
        counter = 1

def clear_ram():
    clear_ram = libRKM.clear_ram
    # clear_ram.argtypes = [ctypes.c_int]
    clear_ram.restype = ctypes.c_int
    result = clear_ram()

    clear_label()

    text = label.text()

    if result != 0:
        text = text + "Clear RAM: error to clear ram\n"
        show_popup()
    else:
        text = text + "Clear RAM: done\n"

    text = text
    label.setText(text)

def main():
    # Create the application
    app = QApplication(sys.argv)

    # some init here
    load_libRKM()
    set_dark_theme(app)

    # take screen info
    # in this way i can spawn window at center of display
    screen_geometry = app.primaryScreen().geometry()
    width = screen_geometry.width()
    height = screen_geometry.height()
    width = width / 2
    height = height / 2
    
    window_height = 500
    window_width = 700

    global counter
    counter = 1

    # Create a main window
    global window
    window = QMainWindow()
    window.setWindowTitle("System Manager")
    window.setGeometry(int(width) - int(window_width / 2), int(height) - int(window_height / 2), window_width, window_height)
    window.setFixedSize(window_width, window_height)

    # Create a label widget
    global label
    label = QLabel(window)
    label_height = 300
    label_width = window_width - 4
    lab_y = window_height - label_height
    label.setGeometry(2, lab_y, label_width, label_height)

    # Create a font for the label
    font = QFont("Arial", 10, QFont.Weight.Bold)
    label.setFont(font)
    # Set text alignment
    label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    label.setStyleSheet("background-color: black; color: white; border-radius; border-radius: 25px; margin: auto")

    # Create a group box
    group_box_left = QGroupBox("", window)
    group_box_right = QGroupBox("", window)
    group_box_left.setGeometry(0, 0, int(window_width / 2), window_height - label_height - 3)
    group_box_right.setGeometry(int(window_width / 2), 0, int(window_width / 2), window_height - label_height - 3)

    # Create a layout for the group box
    layout_left = QVBoxLayout()
    layout_right = QVBoxLayout()
    group_box_left.setLayout(layout_left)
    group_box_right.setLayout(layout_right)

    btn_ram = QPushButton("Clear RAM")
    #button2 = QPushButton("Nice")
    
    btn_ram.setMaximumSize(100, 30)

    btn_ram.clicked.connect(clear_ram)

    layout_left.addWidget(btn_ram)

    # show cpu usage
    cpu_label = QLabel()
    cpu_label.setMaximumSize(int(window_width / 2) - 1, 30)
    layout_right.addWidget(cpu_label)
    cpu_thread = get_cpu_thread()
    cpu_thread.update_label_signal.connect(lambda new_text: cpu_label.setText(new_text))
    cpu_thread.start()

    # show CPU online
    online_cpu = QLabel()
    online_cpu.setMaximumSize(int(window_width / 2) - 1, 30)
    layout_right.addWidget(online_cpu)
    online_cpu_thread = get_online_cpu_thread()
    online_cpu_thread.update_label_signal.connect(lambda new_text: online_cpu.setText(new_text))
    online_cpu_thread.start()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()