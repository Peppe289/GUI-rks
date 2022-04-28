#include <iostream>
#include <string.h>
#include <vector>
#include "include/class.hpp"
#include "include/tool.hpp"

std::string readfile(std::string filename) {
    std::fstream isfile;
    std::string input;
    isfile.open(filename, std::ios::in);

    if (!isfile)
        goto error;

    isfile>>input;
    isfile.close();

    return input;

error:
    return "Error";
}

float _cpu_maxfreq(std::vector<std::string> cluster) {
    // use int because is in Khz
    int maxfreq = 0;
    std::string temp;
    for (int i = 0; i != (int)cluster.size(); ++i) {
        temp = readfile(CPUFREQ + cluster[i] + "/cpuinfo_max_freq");
        if (maxfreq < stoi(temp))
            maxfreq = stoi(temp);
    }

    // return in Ghz
    return maxfreq / 1000000;
}