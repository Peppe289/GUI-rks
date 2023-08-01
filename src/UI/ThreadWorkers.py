import psutil, ctypes
from PyQt6.QtCore import pyqtSignal, QObject, QThread
from middleWare import show_popup_error


class GeneralWorker(QObject):

    def __init__(self):
        super().__init__()
        self._isRunning = False

    def start(self):
        self._isRunning = True
        self._run()

    def stop(self):
        self._isRunning = False

    def _run(self):
        # This method should be overriden by the child class
        pass

class GetRamUsageWorker(GeneralWorker):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def get_ram_usage(self) -> str:
        memstats = self.libRKM.memory_percentage
        memstats.restype = ctypes.c_float
        percent = memstats()
        text = str(float(f'{percent:.2f}'))
        return text

    def _run(self):
        while self._isRunning:
            QThread.msleep(1000)
            text = self.get_ram_usage()
            self.progress.emit(text)
        self.finished.emit()
        self.stop()

class GetGpuInfoWorker(GeneralWorker):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def get_gpu_usage(self) -> str:
        gpu_percentage = self.libRKM.get_gpu_usage
        gpu_percentage.restype = ctypes.c_int
        gpu_percentage = str(gpu_percentage())
        text = ";".join([gpu_percentage,])
        return text

    def _run(self):
        while self._isRunning:
            QThread.msleep(1000)
            text = self.get_gpu_usage()
            self.progress.emit(text)
        self.finished.emit()

class GetCpuInfoWorker(GeneralWorker):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL):
        super().__init__()
        self.libRKM = libRKM

    def get_cpu_usage(self) -> str:
        cpu_percentage = str(psutil.cpu_percent(percpu=False))
        cpu_temp = self.libRKM.get_cpu_temp
        cpu_temp.restype = ctypes.c_float
        cpu_temp = str(cpu_temp())
        text = ";".join([cpu_percentage, cpu_temp])
        return text

    def _run(self):
        while self._isRunning:
            QThread.msleep(1000)
            text = self.get_cpu_usage()
            self.progress.emit(text)
        self.finished.emit()

class GetCurrentGovWorker(GeneralWorker):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_current_governor() -> str:
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor", "r") as f:
            text = f.readlines()[0].strip().split(" ")
        return text[0]
    
    def _run(self):
        while self._isRunning:
            QThread.msleep(1000)
            try:
                text = self.get_current_governor()
            except Exception as e:
                show_popup_error(e)
                break
            self.progress.emit(text)
        self.finished.emit()