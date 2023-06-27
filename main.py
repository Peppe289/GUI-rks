import sys
import ctypes
import time
import psutil

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QVBoxLayout, QGroupBox, QComboBox, QProgressBar
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class get_ram_usage(QThread):
    update_label_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
    
    def run(self):
        while 1:
            text = [' ', 0]
            text[0] = "Ram usage: " + str(psutil.virtual_memory().percent) + "%"
            text[1] = int(psutil.virtual_memory().percent)
            self.update_label_signal.emit(text)
            time.sleep(1)


class set_current_gov_thread(QThread):
    update_label_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    def run(self):
        while 1:
            try:
                with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor") as f:
                    text = f.readlines()[0].strip().split(" ")
                #file = open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor")
                #text = file.read()
                #file.close()
            except:
                print_on_label("Some error to read current gov\n")
                text = ['error']
                break

            self.update_label_signal.emit(text[0])
            time.sleep(1)

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

def print_on_label(data):
    global counter
    counter = counter + 1

    if counter > 10:
        label.setText("")
        counter = 1
    
    text = label.text()
    text = text + data
    label.setText(text)

def clear_ram():
    clear_ram = libRKM.clear_ram
    # clear_ram.argtypes = [ctypes.c_int]
    clear_ram.restype = ctypes.c_int
    result = clear_ram()

    if result != 0:
        #text = text + "Clear RAM: error to clear ram\n"
        print_on_label("Clear RAM: error to clear ram\n")
        show_popup()
    else:
        print_on_label("Clear RAM: done\n")
        #text = text + "Clear RAM: done\n"

def change_governor(data):
    #cpu_governor.setCurrentText(data)
    #print(data)
    try:
        file = open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor", "w")
        file.write(data)
        file.close()
        print_on_label("Changed governor to " + data + "\n")
    except:
        print_on_label("You can't change governor\n")

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
    group_size = group_box_left.size()

    # Create a layout for the group box
    layout_left = QVBoxLayout()
    layout_right = QVBoxLayout()
    group_box_left.setLayout(layout_left)
    group_box_right.setLayout(layout_right)

    layout_left.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    layout_right.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    btn_ram = QPushButton("Clear RAM")
    btn_ram.setMinimumSize(int(group_size.width() / 2) - 2, 30)
    btn_ram.clicked.connect(clear_ram)
    layout_left.addWidget(btn_ram)

    # show cpu usage
    cpu_label = QLabel()
    cpu_label.setMinimumSize(int(group_size.width() / 2) - 2, 30)
    layout_right.addWidget(cpu_label)
    cpu_thread = get_cpu_thread()
    cpu_thread.update_label_signal.connect(lambda new_text: cpu_label.setText(new_text))
    cpu_thread.start()

    # show CPU online
    online_cpu = QLabel()
    online_cpu.setMinimumSize(int(group_size.width() / 2) - 2, 30)
    layout_right.addWidget(online_cpu)
    online_cpu_thread = get_online_cpu_thread()
    online_cpu_thread.update_label_signal.connect(lambda new_text: online_cpu.setText(new_text))
    online_cpu_thread.start()

    # show ram usage
    ram_usage = QLabel()

    ram_usage.setMinimumSize(int(group_size.width() / 2) - 2, 30)
    layout_right.addWidget(ram_usage)

    ram_usage_thread = get_ram_usage()
    ram_usage_thread.update_label_signal.connect(lambda new_text: ram_usage.setText(new_text[0]))

    ram_usage_bar = QProgressBar()
    ram_usage_bar.setMaximumSize(group_size.width() - 2, 15)
    ram_usage_bar.setMinimum(0)
    ram_usage_bar.setMaximum(100)
    layout_right.addWidget(ram_usage_bar)

    ram_usage_thread.update_label_signal.connect(lambda new_text: ram_usage_bar.setValue(new_text[1]))
    ram_usage_thread.start()

    # show governor profile
    try:
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors") as f:
            text = f.readlines()[0].strip().split(" ")
    except:
        print_on_label("Some error to read governos\n")
        text = ['error']

    cpu_governor = QComboBox()
    cpu_governor.setMinimumSize(int(group_size.width() / 2) - 2, 30)
    layout_left.addWidget(cpu_governor)
    cpu_current_gov = set_current_gov_thread()
    cpu_current_gov.update_label_signal.connect(lambda new_text: cpu_governor.setCurrentText(new_text))
    cpu_current_gov.start()
    cpu_governor.addItems(text)
    cpu_governor.currentTextChanged.connect(change_governor)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()