import sys, ctypes
from PyQt6 import QtWidgets
from MainWindow import Ui_MainWindow
from ThreadWorkers import get_ram_usage, get_cpu_info, get_gpu_info, get_current_gov_thread
import middleWare

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.libRKM = ctypes.CDLL('./src/libRKM.so')
        
        # Connect buttons and combobox
        self.clear_ram_btn.clicked.connect(lambda: middleWare.clear_ram(self.libRKM))
        self.curr_gov_combobox.currentTextChanged.connect(lambda: middleWare.change_governor(self.curr_gov_combobox.currentText()))

        # Connect threads
        self.get_ram_usage_thread = get_ram_usage(self.libRKM)
        self.get_ram_usage_thread.update_label_signal.connect(lambda: self.update_ram_usage_graph)
        self.get_ram_usage_thread.start()

        self.get_cpu_info_thread = get_cpu_info(self.libRKM)
        self.get_cpu_info_thread.update_label_signal.connect(lambda: self.update_cpu_info)
        self.get_cpu_info_thread.start()

        self.get_gpu_info_thread = get_gpu_info(self.libRKM)
        self.get_gpu_info_thread.update_label_signal.connect(lambda: self.update_gpu_info)
        self.get_gpu_info_thread.start()

        self.get_current_gov_thread = get_current_gov_thread()
        self.get_current_gov_thread.update_label_signal.connect(lambda: self.update_curr_gov_combobox)
        self.get_current_gov_thread.start()
        

    def update_curr_gov_combobox(self, text):
        self.curr_gov_combobox.setCurrentText(text)

    def update_ram_usage_graph(self, text):
        self.ram_usage_graph.setText(text[0])
        self.ram_usage_graph.setValue(text[1])

    def update_cpu_info(self, text):
        percent, temp = text.split(";")
        self.cpu_temp_label.setText(temp)
        self.cpu_usage_graph.setText(percent)

    def update_gpu_info(self, text):
        percent, temp = text.split(";")
        # self.gpu_temp_label.setText(temp)
        # self.gpu_usage_graph.setText(percent)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow(main_window)
    ui.setupUi(main_window)
    ui.show()
    sys.exit(app.exec())