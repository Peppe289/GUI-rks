#include <iostream>
#include <string.h>
#include "include/tool.hpp"
#include "include/class.hpp"
#include <sys/types.h>
#include <stdio.h>
#include <dirent.h>
#include <vector>

static bool _numer_equal_string(int x, std::string y) {
    return x == (int)y.length();
}

void info::uploadgovernor(std::string temp) {
    int c = 0;
    for (int i = 0; i != (int)temp.length(); ++i)
        if (isspace((char)temp[i]))
            c++;

    int i = 0;
    std::stringstream ssin(temp);
    std::string tem;
    while (ssin.good() && i < c){
        ssin >> tem;
        available_gov.push_back(tem);
        ++i;
    }
}

void info::SearchCluster() {
    DIR *dir;
    struct dirent *diread;
    std::vector<std::string> files;
    std::string policy = "policy";
    int counter;

    if ((dir = opendir(CPUFREQ)) != nullptr) {
        while ((diread = readdir(dir)) != nullptr) {

            counter = 0;
            std::string temp = diread->d_name;
            int length = (temp.size() < policy.size()) ? temp.size() : policy.size();
            for (int k = 0; k != length; ++k) {
                if (temp[k] == policy[k])
                    counter++;
            }

            if (_numer_equal_string(counter, policy))
                cluster.push_back(diread->d_name);
        }
        closedir (dir);
    } else {
        std::cout<<"Error\n";
        return;
    }
}
