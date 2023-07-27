import time, psutil, ctypes
from PyQt6.QtCore import pyqtSignal, QObject
from middleWare import show_popup_error

class GetRamUsageWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def run(self):
        while 1:
            memstats = self.libRKM.memory_percentage
            memstats.restype = ctypes.c_float
            percent = memstats()
            text = str(float(f'{percent:.2f}'))
            self.progress.emit(text)
            time.sleep(1)
        self.finished.emit()

class GetGpuInfoWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def run(self):
        while 1:
            gpu_percentage = self.libRKM.get_gpu_usage
            gpu_percentage.restype = ctypes.c_float
            gpu_percentage = str(gpu_percentage())
            text = ";".join([gpu_percentage,])
            self.progress.emit(text)
            time.sleep(1)
        self.finished.emit()

class GetCpuInfoWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def run(self):
        while 1:
            cpu_percentage = str(psutil.cpu_percent(percpu=False))
            cpu_temp = self.libRKM.get_cpu_temp
            cpu_temp.restype = ctypes.c_float
            cpu_temp = str(cpu_temp())
            text = ";".join([cpu_percentage, cpu_temp])
            time.sleep(1)
            self.progress.emit(text)
        self.finished.emit()

class GetCurrentGovWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
    
    def run(self):
        while 1:
            try:
                with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor") as f:
                    text = f.readlines()[0].strip().split(" ")
            except:
                show_popup_error()
                text = ['error']
                break

            self.progress.emit(text[0])
            time.sleep(1)
        self.finished.emit()