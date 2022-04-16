from ..Utils import Utils

from threading import Thread
import time
import psutil


class UpdateThread(Thread):
    def __init__(self, cur_governor, cur_freq, used_ram, cpu_used, gov_combo, clus_num):
        Thread.__init__(self)
        self.is_stopped = False
        self.cur_governor = cur_governor
        self.cur_freq = cur_freq
        self.used_ram = used_ram
        self.cpu_used = cpu_used
        self.gov_combo = gov_combo
        self.clus_num = clus_num

    def run(self):
        try:
            while not self.is_stopped:
                time.sleep(1)
                self.cur_governor.set(Utils.get_current_gov())
                self.used_ram.set(str(psutil.virtual_memory().percent) + "%")
                self.cpu_used.set(str(psutil.cpu_percent()) + "%")
                # write all file with this directory:
                # /sys/devices/system/cpu/cpufreq/policy<X>/scaling_governor
                # change governor
                for x in range(self.clus_num):
                    with open("/sys/devices/system/cpu/cpufreq/policy" + str(x) + "/scaling_governor", 'w') as f:
                        f.write(self.gov_combo.get())

                self.cur_freq.set(Utils.get_current_freq())
        except RuntimeError:
            pass

    def stop(self):
        self.is_stopped = True
