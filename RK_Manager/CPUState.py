import os

class CPUState:
    @staticmethod
    def changeGov(newgovernor, cluster):
        for x in range(cluster):
            with open("/sys/devices/system/cpu/cpufreq/policy" + str(x) + "/scaling_governor", 'w') as f:
                f.write(newgovernor)

    @staticmethod
    def get_current_freq(cpun):
        calc = 0
        # in this way when can see stimate freq of all cpu
        for x in range(cpun):
            with open("/sys/devices/system/cpu/cpufreq/policy" + str(x) + "/scaling_cur_freq") as f:
                calc = int(f.readlines()[0]) + calc

        current_freq = calc / cpun
        # return in Mhz
        return str(int(int(current_freq) / 1000)).strip()

    @staticmethod
    def get_current_gov():
        with open(
            "/sys/devices/system/cpu/cpufreq/policy0/scaling_governor"
        ) as f:
            gov = f.readlines()[0]
        return str(gov).strip()