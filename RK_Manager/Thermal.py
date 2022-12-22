import os

class Thermal:
    @staticmethod
    def get_themal():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                temp_info = int(f.readlines()[0])
            # to show with Celsius
            return str(temp_info / 1000) + "°"
        except:
            return "Not available"

