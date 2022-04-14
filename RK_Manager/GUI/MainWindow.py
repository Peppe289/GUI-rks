from ..Utils import Utils

import time
from threading import Thread
from .UpdateThread import UpdateThread
from tkinter import *
from tkinter import ttk
from numpy import size


class MainWindow:
    def __init__(self):
        self.root = Tk()

        # governor and freq strings
        self.cur_governor = StringVar()
        self.cur_governor.set("Loading...")
        self.cur_freq = StringVar()
        self.cur_freq.set("Loading...")

        max_freq_dir = Utils.find_files(
            "cpuinfo_max_freq", "/sys/devices/system/cpu/cpufreq/"
        )

        # number of cluster:
        clus_num = size(max_freq_dir)

        with open(max_freq_dir[0]) as f:
            max_freq = int(f.readlines()[0])

        # save available governors
        with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors") as f:
            available_governors = f.readlines()

        # UI setup
        self.root.title("Rave Tool")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="black", padx=10, pady=10)
        self.root.tk.call('source', r'./themes/azure.tcl')
        self.root.tk.call("set_theme", "dark")
        frm = ttk.Frame(self.root)
        frm.grid()
        frm2 = ttk.Frame(self.root)
        frm2.grid()
        frm2.place(relx=0.0, rely=1.0, anchor="sw")
        ttk.Label(frm, text="Number of cluster: ").grid(column=0, row=0)
        ttk.Label(frm, text=clus_num).grid(column=1, row=0)

        # convert max_freq to Ghz
        show_max_freq = max_freq / 1000000
        ttk.Label(frm, text="Max Freq: ").grid(column=0, row=1)
        ttk.Label(frm, text=str(show_max_freq) + " Ghz").grid(column=1, row=1)
        ttk.Label(frm, text="Governor: ").grid(column=0, row=2)
        ttk.Label(frm, textvariable=self.cur_governor).grid(column=1, row=2)
        ttk.Label(frm, text="Available Gov: ").grid(column=0, row=4)
        for x in range (size(available_governors)):
            ttk.Label(frm, text=available_governors[x]).grid(column=1, row=x+4)

        # current freq label
        ttk.Label(frm, text="Current freq: ").grid(column=0, row=3)
        ttk.Label(frm, textvariable=self.cur_freq).grid(column=1, row=3)
        ttk.Button(frm2, text="Quit", command=self.stop).grid(column=1, row=0)

    def start(self):
        self.update_thread = UpdateThread(self.cur_governor, self.cur_freq)
        # self.threads.append(main_thread)
        self.update_thread.start()

        self.root.mainloop()

        # DISABLED THIS FOR NOW
        # freq_thread = Thread(target=self.update_freq)
        # freq_thread.start()
        # self.threads.append(freq_thread)

        # gov_thread = Thread(target=self.update_gov)
        # gov_thread.start()
        # self.threads.append(gov_thread)

    def stop(self):
        self.update_thread.stop()
        self.root.destroy()
