#include <string.h>
#include <iostream>
#include <vector>

#define CPUFREQ     "/sys/devices/system/cpu/cpufreq/"

class info {
    public:
        float maxfreq; //max freq of cpu
        std::string kernelversion; // full name of kernel from /proc/version 
        std::vector<std::string> cluster; // cluster name
        void SearchCluster();
};