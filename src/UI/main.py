import sys, ctypes, logging
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSlot
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
        # this is used as backup if we can't change the governor
        # short explanation: if we fail to change governor, the combobox will be updated using the "wrong" value
        # but the governor will remain the same. We need to keep track of the current governor
        # and if the change fails, we will just revert the combobox text to the old one
        self.curr_gov: str = GetCurrentGovWorker.get_current_governor()
        self.curr_gov_combobox.setCurrentText(self.curr_gov)

        # Connect buttons and combobox
        self.clear_ram_btn.clicked.connect(lambda: self.clear_ram())
        self.curr_gov_combobox.currentTextChanged.connect(self.change_governor)

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

        self.workers.append(GetCpuInfoWorker(self.libRKM))
        self.workers[-1].progress.connect(self.update_cpu_info)

        self.workers.append(GetGpuInfoWorker(self.libRKM))
        self.workers[-1].progress.connect(self.update_gpu_info)

        self.workers.append(GetCurrentGovWorker())
        self.workers[-1].progress.connect(self.update_curr_gov_combobox)

        for i in range(len(self.workers)):
            self.threads.append(QThread())
            self.workers[i].moveToThread(self.threads[-1])
            self.threads[i].started.connect(self.workers[i].start)
            self.workers[i].finished.connect(self.threads[-1].quit)
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

    def clear_ram(self):
        try:
            middleWare.clear_ram(self.libRKM)
        except Exception as e:
            middleWare.show_popup_error(e)

    def change_governor(self):
        if self.curr_gov_combobox.currentText() == self.curr_gov:
            return
        logging.info(f"Changing governor. New={self.curr_gov_combobox.currentText()}, Old={self.curr_gov}")
        try:
            middleWare.change_governor(self.curr_gov_combobox.currentText())
        except Exception as e:
            self.curr_gov_combobox.setCurrentText(self.curr_gov)
            logging.debug("Failed to change governor")
            middleWare.show_popup_error(e)
        else:
            # if we successfully changed the governor, we need to update the string that keeps track of the change
            self.curr_gov = self.curr_gov_combobox.currentText()

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
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())