from ..Utils import Utils

from threading import Thread
import time


class UpdateThread(Thread):
    def __init__(self, cur_governor, cur_freq):
        Thread.__init__(self)
        self.is_stopped = False
        self.cur_governor = cur_governor
        self.cur_freq = cur_freq

    def run(self):
        try:
            while not self.is_stopped:
                time.sleep(1)
                self.cur_governor.set(Utils.get_current_gov())
                self.cur_freq.set(Utils.get_current_freq())
        except RuntimeError:
            pass

    def stop(self):
        self.is_stopped = True
