from ..Utils import Utils

from .UpdateThread import UpdateThread
from tkinter import *
from tkinter import ttk
import re
import os

class MainWindow:
    def __init__(self):
        self.root = Tk()

        # governor and freq strings
        self.cur_governor = StringVar()
        self.cur_governor.set("Loading...")
        self.cur_freq = StringVar()
        self.cur_freq.set("Loading...")
        self.used_ram = StringVar()
        self.used_ram.set("Loading...")
        self.cpu_used = StringVar()
        self.cpu_used.set("Loading...")
        self.cpu_temperature = StringVar()
        self.cpu_temperature.set("Loading...")
        self.battery = StringVar()
        self.battery.set("Loading...")
        self.fan_speed = StringVar()
        self.fan_speed.set("Loading...")

        max_freq_dir = Utils.find_files(
            "cpuinfo_max_freq", "/sys/devices/system/cpu/cpufreq/"
        )

        # search name of CPU
        proc_info = open("/proc/cpuinfo", "r")
        for line in proc_info:
            if re.search("model name", line):
                cpuinfo = line
                break

        # number of cluster:
        self.clus_num = len(max_freq_dir)

        # Auto = 2
        # Max = 0
        fan_state = ['Max', 'Auto', 'none']

        with open(max_freq_dir[0]) as f:
            max_freq = int(f.readlines()[0])

        # save available governors
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors") as f:
            available_governors = f.readlines()[0].strip().split(" ")

        # UI setup
        self.root.title("Rave Tool")
        self.root.resizable(False, False)
        self.root.configure(bg="black", padx=10, pady=10)
        self.root.tk.call('source', r'./themes/azure.tcl')
        self.root.tk.call("set_theme", "dark")
        frm = ttk.Frame(self.root)
        frm.grid()
        ttk.Label(frm, text="Number of cluster: ").grid(column=0, row=0)
        ttk.Label(frm, text=self.clus_num).grid(column=1, row=0)

        # convert max_freq from Khz to Ghz
        show_max_freq = max_freq / 1000000

        ttk.Label(frm, text="CPU model: ", borderwidth=20).grid(column=0, row=1)
        ttk.Label(frm, text=cpuinfo.replace("model name\t: ", ""), borderwidth=20).grid(column=1, row=1)

        ttk.Label(frm, text="Max Freq: ", borderwidth=20).grid(column=0, row=2)
        ttk.Label(frm, text=str(show_max_freq) + " Ghz").grid(column=1, row=2)
        
        ttk.Label(frm, text="Current freq: ", borderwidth=20).grid(column=0, row=3)
        ttk.Label(frm, textvariable=self.cur_freq).grid(column=1, row=3)
        
        ttk.Label(frm, text="RAM used: ", borderwidth=20).grid(column=0, row=4)
        ttk.Label(frm, textvariable=self.used_ram).grid(column=1, row=4)

        ttk.Label(frm, text="CPU used: ", borderwidth=20).grid(column=0, row=5)
        ttk.Label(frm, textvariable=self.cpu_used).grid(column=1, row=5)
        
        ttk.Label(frm, text="Available Gov: ", borderwidth=20).grid(column=0, row=6)        
        # Governors combobox
        self.temp = Utils.get_current_gov()
        self.gov_combo = ttk.Combobox(frm, values=available_governors, state="readonly")
        self.gov_combo.grid(column=1, row=6)
        # Set current governor as default
        self.gov_combo.current(available_governors.index(Utils.get_current_gov()))

        ttk.Label(frm, text="CPU temperature: ", borderwidth=20).grid(column=0, row=7)
        ttk.Label(frm, textvariable=self.cpu_temperature).grid(column=1, row=7)

        ttk.Label(frm, text="Battery level: ", borderwidth=20).grid(column=0, row=8)
        ttk.Label(frm, textvariable=self.battery).grid(column=1, row=8)

        self.fan_temp = Utils.get_fan_state()
        ttk.Label(frm, text="Fan controll", borderwidth=20).grid(column=0, row=9)
        self.fan_combo = ttk.Combobox(frm, values=fan_state, state="readonly")
        self.fan_combo.grid(column=1, row=9)
        self.fan_combo.current(fan_state.index(Utils.get_fan_state()))

        ttk.Label(frm, text="Fan speed: ", borderwidth=20).grid(column=0, row=10)
        ttk.Label(frm, textvariable= self.fan_speed, borderwidth=20).grid(column=1, row=10)

        if os.geteuid() != 0:
            ttk.Label(frm, text="Watch out. If you run without root some functions will not be available", foreground="red", borderwidth=20).grid(column=0, row=11)

    def start(self):
        self.update_thread = UpdateThread(self.cur_governor, self.cur_freq, self.used_ram, self.cpu_used, self.gov_combo, self.clus_num, self.temp, self.cpu_temperature, self.battery, self.fan_temp, self.fan_combo, self.fan_speed)
        # self.threads.append(main_thread)
        self.update_thread.start()

        self.root.mainloop()

    def stop(self):
        self.update_thread.stop()
        self.root.destroy()
