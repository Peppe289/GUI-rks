import time, psutil, ctypes, logging
from PyQt6.QtCore import pyqtSignal, QObject
from middleWare import show_popup_error


class GeneralWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.isRunning = True

    def stop(self):
        logging.debug("stop")
        self.isRunning = False

class GetRamUsageWorker(GeneralWorker):
    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def get_ram_usage(self):
        memstats = self.libRKM.memory_percentage
        memstats.restype = ctypes.c_float
        percent = memstats()
        text = str(float(f'{percent:.2f}'))
        return text

    def run(self):
        while self.isRunning:
            text = self.get_ram_usage()
            time.sleep(1)
            self.progress.emit(text)
        self.finished.emit()

class GetGpuInfoWorker(GeneralWorker):
    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def get_gpu_usage(self):
        gpu_percentage = self.libRKM.get_gpu_usage
        gpu_percentage.restype = ctypes.c_int
        gpu_percentage = str(gpu_percentage())
        text = ";".join([gpu_percentage,])
        return text

    def run(self):
        while self.isRunning:
            text = self.get_gpu_usage()
            time.sleep(1)
            self.progress.emit(text)
        self.finished.emit()

class GetCpuInfoWorker(GeneralWorker):
    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def get_cpu_usage(self):
        cpu_percentage = str(psutil.cpu_percent(percpu=False))
        cpu_temp = self.libRKM.get_cpu_temp
        cpu_temp.restype = ctypes.c_float
        cpu_temp = str(cpu_temp())
        text = ";".join([cpu_percentage, cpu_temp])
        return text

    def run(self):
        while self.isRunning:
            text = self.get_cpu_usage()
            time.sleep(1)
            self.progress.emit(text)
        self.finished.emit()

class GetCurrentGovWorker(GeneralWorker):
    def __init__(self):
        super().__init__()

    def get_current_governor(self):
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor") as f:
            text = f.readlines()[0].strip().split(" ")
        return text[0]
    
    def run(self):
        while self.isRunning:
            try:
                text = self.get_current_governor()
            except:
                show_popup_error()
                text = ['error']
                break
            time.sleep(1)
            self.progress.emit(text[0])
        self.finished.emit()