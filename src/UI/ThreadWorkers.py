import time, psutil, ctypes
from PyQt6.QtCore import QThread, pyqtSignal
from middleWare import show_popup_error

class get_ram_usage(QThread):
    update_label_signal = pyqtSignal(list)

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def run(self):
        while 1:
            text = [' ', 0]
            memstats = self.libRKM.memory_percentage
            memstats.restype = ctypes.c_float
            percent = memstats()
            text[0] = "Ram usage: " + str(float(f'{percent:.2f}')) + "%"
            text[1] = int(percent)
            self.update_label_signal.emit(text)
            time.sleep(1)

class get_gpu_info(QThread):
    update_label_signal = pyqtSignal(list)

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def run(self):
        while 1:
            gpu_percentage = self.libRKM.get_gpu_usage
            gpu_percentage.restype = ctypes.c_float
            gpu_percentage = str(gpu_percentage())
            text = [gpu_percentage,].join(";")
            self.update_label_signal.emit(text)
            time.sleep(1)

class get_cpu_info(QThread):
    update_label_signal = pyqtSignal(list)

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def run(self):
        while 1:
            cpu_percentage = str(psutil.cpu_percent(percpu=False))
            cpu_temp = self.libRKM.get_cpu_temp
            cpu_temp.restype = ctypes.c_float
            cpu_temp = str(cpu_temp())
            text = [cpu_percentage, cpu_temp].join(";")
            time.sleep(1)
            self.update_label_signal.emit(text)


class get_current_gov_thread(QThread):
    update_label_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    def run(self):
        while 1:
            try:
                with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor") as f:
                    text = f.readlines()[0].strip().split(" ")
                    print(text)
            except:
                show_popup_error()
                text = ['error']
                break

            self.update_label_signal.emit(text[0])
            time.sleep(1)