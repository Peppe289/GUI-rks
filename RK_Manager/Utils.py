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
    def changeFanState(val):
        if val == 'Max':
            val = 0
        elif val == 'Auto':
            val = 2
        if val == 'none':
            Utils.get_fan_state()
            return
        with open("/sys/bus/platform/drivers/asus-nb-wmi/asus-nb-wmi/hwmon/hwmon5/pwm1_enable", 'w') as f:
                f.write(str(val))

    @staticmethod
    def get_themal():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                temp_info = int(f.readlines()[0])
            # to show with Celsius
            return str(temp_info / 1000) + "°"
        except:
            return "Not available"

    @staticmethod
    def battery_level():
        try:
            with open("/sys/class/power_supply/BAT0/capacity") as f:
                temp_info = int(f.readlines()[0])
            return str(temp_info)
        except:
            return "Not available"

    @staticmethod
    def get_fan_state():
        try:
            with open("/sys/bus/platform/drivers/asus-nb-wmi/asus-nb-wmi/hwmon/hwmon5/pwm1_enable") as f:
                temp_info = int(f.readline()[0])
            if temp_info == 2:
                return "Auto"
            elif temp_info == 0:
                return "Max"
        except:
            return "none"

    @staticmethod
    def get_fan_speed():
        try:
            with open("/sys/bus/platform/drivers/asus-nb-wmi/asus-nb-wmi/hwmon/hwmon5/fan1_input") as f:
                temp_info = str(f.readline())
            return str(temp_info)
        except:
            return "Not available"