import sys, ctypes, logging
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread
from MainWindow import Ui_MainWindow
from ThreadWorkers import GetRamUsageWorker, GetCpuInfoWorker, GetGpuInfoWorker, GetCurrentGovWorker
import middleWare

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.statistics = {
            "ram_usage": [],
            "cpu_usage": [],
            "gpu_usage": [],
        }

        self.libRKM = ctypes.CDLL('./src/libRKM.so')
        
        # fill governors combobox
        self.curr_gov_combobox.addItems(middleWare.get_governors())

        # Connect buttons and combobox
        self.clear_ram_btn.clicked.connect(lambda: middleWare.clear_ram(self.libRKM))
        self.curr_gov_combobox.currentTextChanged.connect(lambda: middleWare.change_governor(self.curr_gov_combobox.currentText()))

        # hide graph x axis
        self.ram_graph.hideAxis("bottom")
        self.ram_graph.setLabel('left', 'Usage (%)')
        self.cpu_graph.hideAxis("bottom")
        self.cpu_graph.setLabel('left', 'Usage (%)')
        self.gpu_graph.hideAxis("bottom")
        self.gpu_graph.setLabel('left', 'Usage (%)')

        # Connect threads
        self.create_threads()

    def create_threads(self):
        self.threads, self.workers = [], []

        self.workers.append(GetRamUsageWorker(self.libRKM))
        self.workers[-1].progress.connect(self.update_ram_usage_graph)
        self.threads.append(QThread(self))

        self.workers.append(GetCpuInfoWorker(self.libRKM))
        self.workers[-1].progress.connect(self.update_cpu_info)
        self.threads.append(QThread(self))

        self.workers.append(GetGpuInfoWorker(self.libRKM))
        self.workers[-1].progress.connect(self.update_gpu_info)
        self.threads.append(QThread(self))

        self.workers.append(GetCurrentGovWorker())
        self.workers[-1].progress.connect(self.update_curr_gov_combobox)
        self.threads.append(QThread(self))

        for i in range(len(self.threads)):
            self.workers[i].moveToThread(self.threads[i])
            self.threads[i].started.connect(self.workers[i].start)
            self.workers[i].finished.connect(self.threads[i].quit)
            if self.threads[i].isRunning():
                self.workers[i].start()
            else:
                self.threads[i].start()

    def closeEvent(self, event):
        self.terminate_threads()
        super().closeEvent(event)

    def terminate_threads(self):
        for i in range(len(self.threads)):
            if self.threads[i].isRunning():
                self.workers[i].stop()
            self.threads[i].quit()
            self.threads[i].wait()

    def update_curr_gov_combobox(self, text: str):
        self.curr_gov_combobox.setCurrentText(text)

    def update_ram_usage_graph(self, text: str):
        self.statistics["ram_usage"].append(float(text))
        if len(self.statistics["ram_usage"]) > 10:
            self.statistics["ram_usage"].pop(0)
        self.ram_graph.plot(y=self.statistics["ram_usage"], clear=True)

    def update_cpu_info(self, text: str):
        percent, temp = text.split(";")
        self.statistics["cpu_usage"].append(float(percent))
        if len(self.statistics["cpu_usage"]) > 10:
            self.statistics["cpu_usage"].pop(0)
        self.cpu_temp_label.setText(str(temp) + "°C")
        self.cpu_graph.plot(y=self.statistics["cpu_usage"], clear=True)

    def update_gpu_info(self, text: str):
        percent = text.split(";")[0]
        self.statistics["gpu_usage"].append(float(percent))
        if len(self.statistics["gpu_usage"]) > 10:
            self.statistics["gpu_usage"].pop(0)
        self.gpu_graph.plot(y=self.statistics["gpu_usage"], clear=True)
    

if __name__ == "__main__":
    # setup logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())