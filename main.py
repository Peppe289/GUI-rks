import sys
import ctypes
import time
import psutil

from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget, QScrollArea, QMainWindow, QCheckBox, QLabel, QPushButton, QMessageBox, QVBoxLayout, QGroupBox, QComboBox, QProgressBar, QTabWidget
from PyQt6.QtGui import QPalette, QColor, QFont, QPen, QPainter, QBrush
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QLegend

class get_ram_usage(QThread):
    update_label_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        while 1:
            text = [' ', 0]
            memstats = libRKM.memory_percentage
            memstats.restype = ctypes.c_float
            percent = memstats()
            text[0] = "Ram usage: " + str(float(f'{percent:.2f}')) + "%"
            text[1] = int(percent)
            self.update_label_signal.emit(text)
            time.sleep(1)


class set_current_gov_thread(QThread):
    update_label_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    def run(self):
        while 1:
            try:
                with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor") as f:
                    text = f.readlines()[0].strip().split(" ")
            except:
                print_on_label("Some error to read current gov\n")
                text = ['error']
                break

            self.update_label_signal.emit(text[0])
            time.sleep(1)

class get_online_cpu_usage(QThread):
    update_label_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        #cpu_usage = libRKM.cpu_load
        #cpu_usage.restype = ctypes.c_int
        while(1):
            #text = cpu_usage()
            text = ['', 0]
            text[1] = psutil.cpu_percent()
            # print(text)
            text[0] = "CPU Usage: " + str(text[1]) + "%"
            text[1] = int(text[1])
            # Emit the update_label_signal with the new label text
            self.update_label_signal.emit(text)
            time.sleep(1)

class get_cpu_online(QThread):
    update_label_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        cpu_online = libRKM.online_cpu
        cpu_online.restype = ctypes.c_int
        while(1):
            text = cpu_online()
            # print(text)
            text = "CPU Online: " + str(text)
            # Emit the update_label_signal with the new label text
            self.update_label_signal.emit(text)
            time.sleep(1)

def load_libRKM():
    global libRKM
    libRKM = ctypes.CDLL('./src/libRKM.so')

def set_dark_theme(app):
    # Create a dark color palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    app.setPalette(dark_palette)

def show_popup():
    message_box = QMessageBox()
    message_box.setWindowTitle("Some Error")
    message_box.setText("I can't make this. Maybe u need to start this as root")
    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

def print_on_label(data):
    print(data)

def clear_ram():
    clear_ram = libRKM.clear_ram
    clear_ram.restype = ctypes.c_int
    result = clear_ram()

    if result != 0:
        print_on_label("Clear RAM: error to clear ram\n")
        show_popup()
    else:
        print_on_label("Clear RAM: done\n")

def change_governor(data):
    try:
        file = open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor", "+r")
        file.write(data)
        file.close()
        print_on_label("Changed governor to " + data + "\n")
    except:
        print_on_label("You can't change governor\n")

def maxThread():
    core_thread = libRKM.max_Thread
    core_thread.restype = ctypes.c_int
    return core_thread()

def newFont():
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(13)
    font.setBold(False)
    return font

def SingleThreadMaxFreq(path):
    func = libRKM.SingleThreadMaxFreq
    func.argtypes = [ ctypes.c_int ]
    func.restype = ctypes.c_int
    return func(path)

def threadState(state, path):
    print(state)
    print(path.text())

def main():
    # Create the application
    app = QApplication(sys.argv)
    # some init here
    load_libRKM()
    set_dark_theme(app)

    # take screen info
    # in this way i can spawn window at center of display
    screen_geometry = app.primaryScreen().geometry()
    width = screen_geometry.width()
    height = screen_geometry.height()
    width = width / 2
    height = height / 2
    
    window_height = int(height)
    window_width = int(width)

    #global counter
    #counter = 0

    # Create a main window
    global window
    window = QMainWindow()
    window.setWindowTitle("System Manager")
    window.setGeometry(int(width) - int(window_width / 2), int(height) - int(window_height / 2), window_width, window_height)
    window.setMinimumSize(window_width, window_height)

    # create main tab
    tab_widget = QTabWidget(window)
    control = QWidget() # sched for control
    #advanced = QWidget() # more option
    info = QWidget() # sched for info
    tab_widget.addTab(control, "Control")
    #tab_widget.addTab(advanced, "Advanced")
    tab_widget.addTab(info, "Stats")
    screen_sched = QVBoxLayout()
    screen_sched.addWidget(tab_widget)
    control_sched = QWidget()
    control_sched.setLayout(screen_sched)
    window.setCentralWidget(control_sched)

    # main Box of Controll
    ctrlMainLayout = QVBoxLayout(control)

    # set top box
    group_box_top = QGroupBox("")
    layout_top = QVBoxLayout(group_box_top)
    group_box_top.setMinimumSize(window_width - 10, int(window_height / 2) - 10)
    ctrlMainLayout.addWidget(group_box_top)

    widthCTRLMainSize = window_width - 40

    btn_ram = QPushButton("Clear RAM")
    btn_ram.setMaximumSize(200, 30)
    btn_ram.clicked.connect(clear_ram)
    layout_top.addWidget(btn_ram)
    layout_top.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    layout_top.setContentsMargins(0, 0, 40, 0)

    # set bottom box
    group_box_bottom = QGroupBox("")
    layout_bottom = QVBoxLayout(group_box_bottom)
    group_box_bottom.setMinimumSize(window_width - 10, int(window_height / 2) - 10)
    layout_bottom.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    layout_bottom.setContentsMargins(0, 0, 40, 0)
    ctrlMainLayout.addWidget(group_box_bottom)

    # show CPU usage
    online_cpu = QLabel()
    online_cpu.setMinimumSize(int(width / 2) - 2, 20)
    layout_bottom.addWidget(online_cpu)

    cpu_usage_bar = QProgressBar()
    cpu_usage_bar.setMinimumSize(widthCTRLMainSize - 2, 15)
    cpu_usage_bar.setMinimum(0)
    cpu_usage_bar.setMaximum(100)
    layout_bottom.addWidget(cpu_usage_bar)

    online_cpu_thread = get_online_cpu_usage()
    online_cpu_thread.update_label_signal.connect(lambda new_text: online_cpu.setText(new_text[0]))
    online_cpu_thread.update_label_signal.connect(lambda new_text: cpu_usage_bar.setValue(new_text[1]))
    online_cpu_thread.start()

    # show ram usage
    ram_usage = QLabel()

    ram_usage.setMinimumSize(int(width / 2) - 2, 30)
    layout_bottom.addWidget(ram_usage)

    ram_usage_thread = get_ram_usage()
    ram_usage_thread.update_label_signal.connect(lambda new_text: ram_usage.setText(new_text[0]))

    ram_usage_bar = QProgressBar()
    ram_usage_bar.setMinimumSize(widthCTRLMainSize - 2, 15)
    ram_usage_bar.setMinimum(0)
    ram_usage_bar.setMaximum(100)
    layout_bottom.addWidget(ram_usage_bar)
    ram_usage_thread.update_label_signal.connect(lambda new_text: ram_usage_bar.setValue(new_text[1]))
    ram_usage_thread.start()

    # show governor profile
    try:
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors") as f:
            text = f.readlines()[0].strip().split(" ")
    except:
        print_on_label("Some error to read governos\n")
        text = ['error']

    cpu_governor = QComboBox()
    cpu_governor.setMaximumSize(200, 30)
    layout_top.addWidget(cpu_governor)
    cpu_current_gov = set_current_gov_thread()
    cpu_current_gov.update_label_signal.connect(lambda new_text: cpu_governor.setCurrentText(new_text))
    cpu_current_gov.start()
    cpu_governor.addItems(text)
    cpu_governor.currentTextChanged.connect(change_governor)


    # info tab
    infoStats_layout = QVBoxLayout(info)
    infoStats_label = QLabel()
    infoStats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # massive import
    # add series for CPU usage graph
    cpuUsageSeries = QLineSeries()
    cpuUsageChart = QChart()
    cpuUsageChart.addSeries(cpuUsageSeries)
    #cpuUsageChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
    axis_x = QValueAxis()
    axis_x.setTitleText("X")
    cpuUsageChart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
    cpuUsageSeries.attachAxis(axis_x)
    axis_y = QValueAxis()
    axis_y.setTitleText("Y")
    cpuUsageChart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
    cpuUsageSeries.attachAxis(axis_y)
    pen = QPen()
    pen.setWidth(3)
    cpuUsageSeries.setPen(pen)
    chart_viewCPU = QChartView(cpuUsageChart)
    chart_viewCPU.setRenderHint(QPainter.RenderHint.Antialiasing)
    #chart_viewCPU.resize(100, 300)
    infoStats_layout.addWidget(chart_viewCPU)
    max_points = 10
    x_min, x_max = 0, max_points - 1
    y_min, y_max = 0, 100
    axis_x.setRange(x_min, x_max)
    axis_y.setRange(y_min, y_max)
    axis_x.setLabelsVisible(False)
    axis_x.setGridLineVisible(False)
    axis_x.setTitleVisible(False)
    axis_x.setShadesVisible(False)
    axis_y.setTitleVisible(False)
    axis_y.setShadesVisible(False)
    cpuUsageChart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
    axis_x.setLabelsColor(Qt.GlobalColor.white)
    axis_y.setLabelsColor(Qt.GlobalColor.white)

    axis_x.setGridLineColor(QColor(70, 70, 70))
    axis_y.setGridLineColor(QColor(70, 70, 70))

    cpuUsageChart.legend().hide()

    cpuUsageSeries.setColor(Qt.GlobalColor.white)
    cpuUsageSeries.setPointLabelsColor(Qt.GlobalColor.white)

    def updateSeriesCPU():
        # Genera un nuovo valore casuale per l'asse Y
        y = psutil.cpu_percent()
        cpuUsageSeries.append(cpuUsageSeries.count(), y)
        x_min, x_max = cpuUsageSeries.count() - max_points, cpuUsageSeries.count() - 1
        axis_x.setRange(x_min, x_max)

        # Ridisegna il grafico
        chart_viewCPU.repaint()
    
    timer = QTimer()
    timer.timeout.connect(updateSeriesCPU)
    timer.start(1000)  # 1000 millisecondi = 1 secondo
    # END GRAPH

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()