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

void info::SearchCluster() {
    DIR *dir; struct dirent *diread;
    std::vector<std::string> files;
    std::string policy = "policy";
    int counter;

    if ((dir = opendir(CPUFREQ)) != nullptr) {
        while ((diread = readdir(dir)) != nullptr) {

            counter = 0;
            std::string temp = diread->d_name;
            for (int k = 0; k != (int)temp.length() - 1; ++k) {
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
