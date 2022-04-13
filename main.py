from cgitb import text
import os
from tkinter.tix import COLUMN
from tokenize import String
from turtle import bgcolor
from unittest import result
from webbrowser import BackgroundBrowser
from numpy import size
import time
import asyncio
import array as arr
from time import sleep, perf_counter
from threading import Thread
from tkinter import *
from tkinter import ttk

def update_gov():
    try:
        while True:
            with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_governor") as f:
                cur = f.readlines()[0]
            time.sleep(1)
            cur_governor.set(str(cur))
    except RuntimeError:
        return

def update_freq():
    try:
        while True:
            with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq") as f:
                current_freq = f.readlines()[0]
            time.sleep(1)
            cur_freq.set(str(current_freq))
    except RuntimeError:
        return

def find_files(filename, search_path):
    result = []
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result


max_freq_dir = find_files("cpuinfo_max_freq", "/sys/devices/system/cpu/cpufreq/")
# number of cluster:
ctr_num = size(max_freq_dir)

with open(max_freq_dir[0]) as f:
    max_freq = int(f.readlines()[0])

root = Tk()
root.title('Rave Tool')
root.geometry("400x200")
root.resizable(True, True)
root.configure(bg="white")
frm = ttk.Frame(root)
frm.grid()
frm2 = ttk.Frame(root)
frm2.grid()
frm2.place(relx = 0.0, rely = 1.0, anchor='sw')
ttk.Label(frm, text="Number of cluster: ", background="white").grid(column=0, row=0)
ttk.Label(frm, text=ctr_num, background="white").grid(column=1, row=0)

# convert max_freq to Ghz
show_max_freq = max_freq/1000000
ttk.Label(frm, text="Max Freq: ", background="white").grid(column=0, row=1)
ttk.Label(frm, text=str(show_max_freq) + " Ghz", background="white").grid(column=1, row=1)

cur_governor = StringVar()
cur_governor.set("Loading...")
t0 = Thread(target=update_gov)
t0.start()

ttk.Label(frm, text="Governor: ", background="white").grid(column=0, row=2)
ttk.Label(frm, textvariable=cur_governor, background="white").grid(column=1, row=2)

# create a StringVar class
cur_freq = StringVar()
cur_freq.set("Loading...")

# current freq label
ttk.Label(frm, text="Current freq: ", background="white").grid(column=0, row=3)
ttk.Label(frm, background="white", textvariable=cur_freq).grid(column=1, row=3)

# start thread
t1 = Thread(target=update_freq)
t1.start()

ttk.Button(frm2, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()