// this software help user to change kernel settings
#include <iostream>
#include "include/tool.hpp"
#include "include/class.hpp"

static void _showinfo(info cpu) {
/*    for (int i = 0; i != (int)cpu.cluster.size(); ++i)
        std::cout<<cpu.cluster[i]<<"\n";*/

    std::cout<<"Number of cluster : "<<cpu.cluster.size()<<"\n";
    std::cout<<"Max freq : "<<cpu.maxfreq<<" Ghz\n";
    std::cout<<"Kernel version : "<<cpu.kernelversion<<"\n";
}

int main (int argc, char *argv[]) {
    info cpu;

    // initialize
    cpu.SearchCluster();
    cpu.maxfreq = _cpu_maxfreq(cpu.cluster);
    cpu.kernelversion = readfile("/proc/version");

    switch (argc) {
        case 2:
            if ((std::string)argv[1] == "--info") {
                _showinfo(cpu);
            }
        break;
//        case 3:
//        break;
        default:
            std::cout<<"You have to run it with a command\n";
    }

    std::cout<<"\n";
    return 0;
}