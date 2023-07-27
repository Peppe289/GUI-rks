import sys
import ctypes
import time
import psutil

from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget, QScrollArea, QMainWindow, QCheckBox, QLabel, QPushButton, QMessageBox, QVBoxLayout, QGroupBox, QComboBox, QProgressBar, QTabWidget
from PyQt6.QtGui import QPalette, QColor, QFont, QPen, QPainter, QBrush
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QLegend

def main():
    # Create the application
    app = QApplication(sys.argv)
    # some init here

    # take screen gpu_ctrl
    # in this way i can spawn window at center of display
    screen_geometry = app.primaryScreen().geometry()
    width = screen_geometry.width()
    height = screen_geometry.height()
    width = width / 2
    height = height / 2
    
    window_height = int(height)
    window_width = int(width)

    # Create a main window
    window = QMainWindow()
    window.setWindowTitle("System Manager")
    window.setGeometry(int(width) - int(window_width / 2), int(height) - int(window_height / 2), window_width, window_height)
    window.setMinimumSize(window_width, window_height)

    # create main tab
    tab_widget = QTabWidget(window)
    main_ctrl = QWidget() # sched for main_ctrl
    gpu_ctrl = QWidget() # sched for gpu_ctrl
    tab_widget.addTab(main_ctrl, "Main")
    tab_widget.addTab(gpu_ctrl, "GPU")
    screen_sched = QVBoxLayout()
    screen_sched.addWidget(tab_widget)
    control_sched = QWidget()
    control_sched.setLayout(screen_sched)
    window.setCentralWidget(control_sched)

    # main Box of Controll
    ctrlMainLayout = QVBoxLayout(main_ctrl)

    # set top box
    group_box_top = QGroupBox("")
    layout_top = QVBoxLayout(group_box_top)
    group_box_top.setMinimumSize(window_width - 10, int(window_height / 4) - 60)
    ctrlMainLayout.addWidget(group_box_top)

    widthCTRLMainSize = window_width - 40

    btn_ram = QPushButton("Clear RAM")
    btn_ram.setMaximumSize(200, 30)
    btn_ram.clicked.connect(clear_ram)
    layout_top.addWidget(btn_ram)
    layout_top.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    layout_top.setContentsMargins(0, 0, 0, 0)

    # set bottom box
    group_box_bottom = QGroupBox("")
    layout_bottom = QVBoxLayout(group_box_bottom)
    group_box_bottom.setMinimumSize(window_width - 40, int((window_height / 4)*3) - 10)
    layout_bottom.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    layout_bottom.setContentsMargins(0, 0, 0, 0)
    ctrlMainLayout.addWidget(group_box_bottom)

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
    layout_bottom.addWidget(chart_viewCPU)
    max_points = 100
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
    timer.start(500)  # 0.5 sec
    # END GRAPH

    # massive import
    # add series for CPU usage graph
    cpuUsageSeriesTemp = QLineSeries()
    cpuUsageChartTemp = QChart()
    cpuUsageChartTemp.addSeries(cpuUsageSeriesTemp)
    #cpuUsageChartTemp.setAnimationOptions(QChart.AnimationOption.AllAnimations)
    axis_x_temp = QValueAxis()
    axis_x_temp.setTitleText("X")
    cpuUsageChartTemp.addAxis(axis_x_temp, Qt.AlignmentFlag.AlignBottom)
    cpuUsageSeriesTemp.attachAxis(axis_x_temp)
    axis_y_temp = QValueAxis()
    axis_y_temp.setTitleText("Y")
    cpuUsageChartTemp.addAxis(axis_y_temp, Qt.AlignmentFlag.AlignLeft)
    cpuUsageSeriesTemp.attachAxis(axis_y_temp)
    pen_temp = QPen()
    pen_temp.setWidth(3)
    cpuUsageSeriesTemp.setPen(pen_temp)
    chart_viewCPUTemp = QChartView(cpuUsageChartTemp)
    chart_viewCPUTemp.setRenderHint(QPainter.RenderHint.Antialiasing)
    #chart_viewCPUTemp.resize(100, 300)
    layout_bottom.addWidget(chart_viewCPUTemp)
    max_points = 100
    x_min_temp, x_max_temp = 0, max_points - 1
    y_min_temp, y_max_temp = 0, 100
    axis_x_temp.setRange(x_min_temp, x_max_temp)
    axis_y_temp.setRange(y_min_temp, y_max_temp)
    axis_x_temp.setLabelsVisible(False)
    axis_x_temp.setGridLineVisible(False)
    axis_x_temp.setTitleVisible(False)
    axis_x_temp.setShadesVisible(False)
    axis_y_temp.setTitleVisible(False)
    axis_y_temp.setShadesVisible(False)
    cpuUsageChartTemp.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
    axis_x_temp.setLabelsColor(Qt.GlobalColor.white)
    axis_y_temp.setLabelsColor(Qt.GlobalColor.white)

    axis_x_temp.setGridLineColor(QColor(70, 70, 70))
    axis_y_temp.setGridLineColor(QColor(70, 70, 70))

    cpuUsageChartTemp.legend().hide()

    cpuUsageSeriesTemp.setColor(Qt.GlobalColor.white)
    cpuUsageSeriesTemp.setPointLabelsColor(Qt.GlobalColor.white)

    cpu_temp = libRKM.get_cpu_temp
    cpu_temp.restype = ctypes.c_float

    def updateSeriesCPU_temp():
        # Genera un nuovo valore casuale per l'asse Y
        y = cpu_temp()
        cpuUsageSeriesTemp.append(cpuUsageSeriesTemp.count(), y)
        x_min_temp, x_max_temp = cpuUsageSeriesTemp.count() - max_points, cpuUsageSeriesTemp.count() - 1
        axis_x_temp.setRange(x_min_temp, x_max_temp)

        # Ridisegna il grafico
        chart_viewCPUTemp.repaint()
    
    timer_cpu_temp = QTimer()
    timer_cpu_temp.timeout.connect(updateSeriesCPU_temp)
    timer_cpu_temp.start(500)  # 0.5 sec
    # END GRAPH

    # show ram usage
    ram_usage = QLabel()

    ram_usage.setMinimumSize(int(width / 2) - 2, 30)
    layout_bottom.addWidget(ram_usage)

    ram_usage_thread = GetRamUsageWorker()
    ram_usage_thread.update_label_signal.connect(lambda new_text: ram_usage.setText(new_text[0]))

    ram_usage_bar = QProgressBar()
    ram_usage_bar.setMinimumSize(widthCTRLMainSize - 2, 15)
    ram_usage_bar.setMaximumHeight(20)
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
        show_popup()

    cpu_governor = QComboBox()
    cpu_governor.setMaximumSize(200, 30)
    layout_top.addWidget(cpu_governor)
    cpu_current_gov = set_current_gov_thread()
    cpu_current_gov.update_label_signal.connect(lambda new_text: cpu_governor.setCurrentText(new_text))
    cpu_current_gov.start()
    cpu_governor.addItems(text)
    cpu_governor.currentTextChanged.connect(change_governor)

    # GPU tab
    GPU_box = QVBoxLayout(gpu_ctrl)

    # massive import
    # add series for CPU usage graph
    gpuUsageSeries = QLineSeries()
    gpuUsageChart = QChart()
    gpuUsageChart.addSeries(gpuUsageSeries)
    #cpuUsageChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
    gpu_axis_x = QValueAxis()
    gpu_axis_x.setTitleText("X")
    gpuUsageChart.addAxis(gpu_axis_x, Qt.AlignmentFlag.AlignBottom)
    gpuUsageSeries.attachAxis(gpu_axis_x)
    gpu_axis_y = QValueAxis()
    gpu_axis_y.setTitleText("Y")
    gpuUsageChart.addAxis(gpu_axis_y, Qt.AlignmentFlag.AlignLeft)
    gpuUsageSeries.attachAxis(gpu_axis_y)
    gpu_pen = QPen()
    gpu_pen.setWidth(3)
    gpuUsageSeries.setPen(gpu_pen)
    chart_viewGPU = QChartView(gpuUsageChart)
    chart_viewGPU.setRenderHint(QPainter.RenderHint.Antialiasing)
    GPU_box.addWidget(chart_viewGPU)
    gpu_max_points = 100
    gpu_x_min, gpu_x_max = 0, gpu_max_points - 1
    gpu_y_min, gpu_y_max = 0, 100
    gpu_axis_x.setRange(gpu_x_min, gpu_x_max)
    gpu_axis_y.setRange(gpu_y_min, gpu_y_max)
    gpu_axis_x.setLabelsVisible(False)
    gpu_axis_x.setGridLineVisible(False)
    gpu_axis_x.setTitleVisible(False)
    gpu_axis_x.setShadesVisible(False)
    gpu_axis_y.setTitleVisible(False)
    gpu_axis_y.setShadesVisible(False)
    gpuUsageChart.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
    gpu_axis_x.setLabelsColor(Qt.GlobalColor.white)
    gpu_axis_y.setLabelsColor(Qt.GlobalColor.white)

    gpu_axis_x.setGridLineColor(QColor(70, 70, 70))
    gpu_axis_y.setGridLineColor(QColor(70, 70, 70))

    gpuUsageChart.legend().hide()

    gpuUsageSeries.setColor(Qt.GlobalColor.white)
    gpuUsageSeries.setPointLabelsColor(Qt.GlobalColor.white)

    def updateSeriesGPU():
        # Genera un nuovo valore casuale per l'asse Y
        get_gpu_usage = libRKM.get_gpu_usage
        get_gpu_usage.restype = ctypes.c_int
        y = get_gpu_usage()
        gpuUsageSeries.append(gpuUsageSeries.count(), y)
        gpu_x_min, gpu_x_max = gpuUsageSeries.count() - gpu_max_points, gpuUsageSeries.count() - 1
        gpu_axis_x.setRange(gpu_x_min, gpu_x_max)

        # Ridisegna il grafico
        chart_viewGPU.repaint()
    
    timer_gpu = QTimer()
    timer_gpu.timeout.connect(updateSeriesGPU)
    timer_gpu.start(500)  # 0.5 sec
    # END GRAPH

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()