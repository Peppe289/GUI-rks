import psutil, ctypes, logging
from PyQt6.QtCore import pyqtSignal, QObject, QThread
from middleWare import show_popup_error


class GeneralWorker(QObject):

    def __init__(self, timeout: int = 1000):
        super().__init__()
        self._isRunning = False
        self._timeout = timeout

    def start(self):
        self._isRunning = True
        self._run()

    def stop(self):
        self._isRunning = False

    def _run(self):
        # This method should be overriden by the child class
        pass

class GetRamInfoWorker(GeneralWorker):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL, timeout: int = 1000):
        super().__init__(timeout=timeout)
        self.libRKM = libRKM

    def get_ram_info(self) -> str:
        memstats = self.libRKM.memory_percentage
        memstats.restype = ctypes.c_float
        usage = str(float(f'{memstats():.2f}'))
        return {
            "usage": usage,
        }

    def _run(self):
        while self._isRunning:
            QThread.msleep(self._timeout)
            data = self.get_ram_info()
            self.progress.emit(data)
        self.finished.emit()
        self.stop()

class GetGpuInfoWorker(GeneralWorker):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL, timeout: int = 1000):
        super().__init__(timeout=timeout)
        self.libRKM = libRKM

    def get_gpu_info(self) -> str:
        gpu_percentage = self.libRKM.get_gpu_usage
        gpu_percentage.restype = ctypes.c_int
        usage = str(gpu_percentage())
        gpu_temp = self.libRKM.get_gpu_thermal
        gpu_temp.restype = ctypes.c_int
        temp = str(gpu_temp())
        return {
            "usage": usage,
            "temperature": temp,
        }

    def _run(self):
        while self._isRunning:
            QThread.msleep(self._timeout)
            data = self.get_gpu_info()
            self.progress.emit(data)
        self.finished.emit()

class GetCpuInfoWorker(GeneralWorker):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, libRKM: ctypes.CDLL, timeout: int = 1000):
        super().__init__(timeout=timeout)
        self.libRKM = libRKM

    def get_cpu_info(self) -> str:
        cpu_percentage = str(psutil.cpu_percent(percpu=False))
        cpu_temp = self.libRKM.get_cpu_temp
        cpu_temp.restype = ctypes.c_float
        cpu_temp = str(cpu_temp())
        return {
            "usage": cpu_percentage,
            "temperature": cpu_temp,
        }

    def _run(self):
        while self._isRunning:
            QThread.msleep(self._timeout)
            data = self.get_cpu_info()
            self.progress.emit(data)
        self.finished.emit()

class GetCurrentGovWorker(GeneralWorker):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, timeout: int = 1000):
        super().__init__(timeout=timeout)

    @staticmethod
    def get_governor_info() -> str:
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor", "r") as f:
            data = f.readlines()[0].strip().split(" ")
        return {
            "current_governor": data[0],
        }
    
    def _run(self):
        while self._isRunning:
            QThread.msleep(self._timeout)
            try:
                data = self.get_governor_info()
            except Exception as e:
                show_popup_error(e)
                break
            self.progress.emit(data)
        self.finished.emit()