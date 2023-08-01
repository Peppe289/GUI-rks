import ctypes, logging
from PyQt6.QtWidgets import QMessageBox

def show_popup_error(e: Exception):
    message_box = QMessageBox()
    message_box.setWindowTitle("Some Error")
    message_box.setText("I can't make this. Maybe u need to start this as root\n" + str(e))
    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

def clear_ram(libRKM: ctypes.CDLL):
    clear_ram = libRKM.clear_ram
    clear_ram.restype = ctypes.c_int
    result = clear_ram()
    if result != 0:
        raise Exception("generic error")
    logging.info("RAM cleared")

def change_governor(data):
    file = open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor", "w")
    file.write(data)
    file.close()

def get_governors():
    with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors") as f:
        text = f.readlines()[0].strip().split(" ")
    return text