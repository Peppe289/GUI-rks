import os


class Utils:
    @staticmethod
    def get_current_gov():
        with open(
            "/sys/devices/system/cpu/cpufreq/policy0/scaling_governor"
        ) as f:
            gov = f.readlines()[0]
        return str(gov).strip()

    @staticmethod
    def get_current_freq():
        with open(
            "/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq"
        ) as f:
            current_freq = f.readlines()[0]
        # return in Mhz
        return str(int(int(current_freq) / 1000)).strip()

    @staticmethod
    def find_files(filename, search_path):
        """
        Finds all files with the given filename in the given search_path
        """
        result = []
        for root, dir, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result

    @staticmethod
    def changeGov(newgovernor, cluster):
        for x in range(cluster):
            with open("/sys/devices/system/cpu/cpufreq/policy" + str(x) + "/scaling_governor", 'w') as f:
                f.write(newgovernor)

    @staticmethod
    def get_themal():
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp_info = int(f.readlines()[0])
        return str(temp_info / 1000)

