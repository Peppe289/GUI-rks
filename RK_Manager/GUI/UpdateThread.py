from ..Utils import Utils

from threading import Thread
import time
import psutil

class UpdateThread(Thread):
    def __init__(self, cur_governor, cur_freq, used_ram):
        Thread.__init__(self)
        self.is_stopped = False
        self.cur_governor = cur_governor
        self.cur_freq = cur_freq
        self.used_ram = used_ram

    def run(self):
        try:
            while not self.is_stopped:
                time.sleep(1)
                self.cur_governor.set(Utils.get_current_gov())
                self.cur_freq.set(Utils.get_current_freq())
                self.used_ram.set(str(psutil.virtual_memory().percent) + "%");
        except RuntimeError:
            pass

    def stop(self):
        self.is_stopped = True
