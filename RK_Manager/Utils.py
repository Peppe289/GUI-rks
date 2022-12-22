import os


class Utils:
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
    def battery_level():
        try:
            with open("/sys/class/power_supply/BAT0/capacity") as f:
                temp_info = int(f.readlines()[0])
            return str(temp_info)
        except:
            return "Not available"
