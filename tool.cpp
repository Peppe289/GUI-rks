#include <iostream>
#include <string.h>
#include <vector>
#include "include/class.hpp"
#include "include/tool.hpp"

void set_governor(std::string new_gov, std::vector<std::string> available_gov,
                                    std::vector<std::string> cluster) {
    int ret = 0;

    for(int i = 0; i != (int)available_gov.size(); ++i) {
        if (new_gov == available_gov[i]) {
            // when find governor set it and break
            for (int k = 0; k != (int)cluster.size(); ++k)
                setgovernor((std::string)CPUFREQ + cluster[k] + "/scaling_governor", available_gov[i]);

            break;
        } else {
            ++ret;
        }
    }

    if (ret == (int)available_gov.size())
        std::cout<<"Governor not found! bye.";
    else
        std::cout<<"Governor set!";

}

std::string readfile(std::string filename) {
    std::fstream isfile;
    std::string input = "";

    isfile.open(filename, std::ios::in);

    if (!isfile)
        return "0";

    std::string temp;
    while (1) {
        isfile >> temp;
        if (isfile.eof())
            break;

        input = input + temp + " ";
    }
    isfile.close();

    return input;
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

void setgovernor(std::string directory, std::string governor) {
    std::fstream write;
    
    try {
        write.open(directory, std::ios::out);
        write << governor;
        write.close();
    } catch(const std::exception& e) {
        std::cerr << e.what() << '\n';
    }
}