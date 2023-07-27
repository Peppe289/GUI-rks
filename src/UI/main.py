import sys, ctypes
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread
from MainWindow import Ui_MainWindow
from ThreadWorkers import GetRamUsageWorker, GetCpuInfoWorker, GetGpuInfoWorker, GetCurrentGovWorker
import middleWare

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.libRKM = ctypes.CDLL('./src/libRKM.so')
        
        # fill governors combobox
        self.curr_gov_combobox.addItems(middleWare.get_governors())

        # Connect buttons and combobox
        self.clear_ram_btn.clicked.connect(lambda: middleWare.clear_ram(self.libRKM))
        self.curr_gov_combobox.currentTextChanged.connect(lambda: middleWare.change_governor(self.curr_gov_combobox.currentText()))

        # Connect threads
        self.create_threads()
        
    def create_threads(self):
        self.threads, self.workers = [], []

        self.workers.append(GetRamUsageWorker(self.libRKM))
        self.workers[0].progress.connect(self.update_ram_usage_graph)
        self.threads.append(QThread())

        self.workers.append(GetCpuInfoWorker(self.libRKM))
        self.workers[1].progress.connect(self.update_cpu_info)
        self.threads.append(QThread())

        self.workers.append(GetGpuInfoWorker(self.libRKM))
        self.workers[2].progress.connect(self.update_gpu_info)
        self.threads.append(QThread())

        self.workers.append(GetCurrentGovWorker())
        self.workers[3].progress.connect(self.update_curr_gov_combobox)
        self.threads.append(QThread())

        for i in range(len(self.threads)):
            self.workers[i].moveToThread(self.threads[i])
            self.threads[i].started.connect(self.workers[i].run)
            self.workers[i].finished.connect(self.threads[i].quit)
            self.workers[i].finished.connect(self.workers[i].deleteLater)
            self.threads[i].finished.connect(self.threads[i].deleteLater)
            self.threads[i].start()

    def update_curr_gov_combobox(self, text):
        self.curr_gov_combobox.setCurrentText(text)

    def update_ram_usage_graph(self, text):
        pass
        # self.ram_usage_graph.setText(text[0])
        # self.ram_usage_graph.setValue(text[1])

    def update_cpu_info(self, text):
        percent, temp = text.split(";")
        self.cpu_temp_label.setText(str(temp))
        # self.cpu_usage_graph.setText(percent)

    def update_gpu_info(self, text):
        percent = text.split(";")[0]
        # self.gpu_temp_label.setText(temp)
        # self.gpu_usage_graph.setText(percent)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow(main_window)
    ui.setupUi(main_window)
    ui.show()
    sys.exit(app.exec())