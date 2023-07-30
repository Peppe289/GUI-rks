import ctypes
from PyQt6.QtWidgets import QMessageBox

def show_popup_error():
    message_box = QMessageBox()
    message_box.setWindowTitle("Some Error")
    message_box.setText("I can't make this. Maybe u need to start this as root")
    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

def clear_ram(libRKM: ctypes.CDLL):
    clear_ram = libRKM.clear_ram
    clear_ram.restype = ctypes.c_int
    result = clear_ram()
    if result != 0:
        show_popup_error()

def change_governor(data):
    try:
        file = open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor", "+r")
        file.write(data)
        file.close()
    except:
        show_popup_error()

def get_governors():
    # show governor profile
    try:
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors") as f:
            text = f.readlines()[0].strip().split(" ")
    except:
        show_popup_error()

    return text