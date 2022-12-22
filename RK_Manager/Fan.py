import os

class FanControl:
    @staticmethod
    def get_fan_speed():
        try:
            with open("/sys/bus/platform/drivers/asus-nb-wmi/asus-nb-wmi/hwmon/hwmon6/fan1_input") as f:
                temp_info = str(f.readline())
            return str(temp_info)
        except:
            return "Not available"

    @staticmethod
    def get_fan_state():
        try:
            with open("/sys/bus/platform/drivers/asus-nb-wmi/asus-nb-wmi/hwmon/hwmon6/pwm1_enable") as f:
                temp_info = int(f.readline()[0])
            if temp_info == 2:
                return "Auto"
            elif temp_info == 0:
                return "Max"
            else:
                "none"
        except:
            return "none"

    @staticmethod
    def changeFanState(val):
        if val == 'Max':
            val = 0
        elif val == 'Auto':
            val = 2
        if val == 'none':
            Utils.get_fan_state()
            return
        with open("/sys/bus/platform/drivers/asus-nb-wmi/asus-nb-wmi/hwmon/hwmon6/pwm1_enable", 'w') as f:
                f.write(str(val))