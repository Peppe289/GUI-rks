// this software help user to change kernel settings
#include <iostream>
#include "include/tool.hpp"
#include "include/class.hpp"

static void _showinfo(info cpu) {
/*    for (int i = 0; i != (int)cpu.cluster.size(); ++i)
        std::cout<<cpu.cluster[i]<<"\n";*/

    std::cout<<"Number of cluster : "<<cpu.cluster.size()<<"\n";
    std::cout<<"Max freq : "<<cpu.maxfreq<<" Ghz\n";
    std::cout<<"Current governor : "<<readfile((std::string)CPUFREQ + "policy0/scaling_governor");
    std::cout<<"\nAvailable governor : ";
    for (int i = 0; i != (int)cpu.available_gov.size(); ++i)
        std::cout<<cpu.available_gov[i]<<" ";

    std::cout<<"\n\nKernel version : "<<cpu.kernelversion<<"\n";
}

int main (int argc, char *argv[]) {
    info cpu;

    // initialize
    cpu.SearchCluster();
    cpu.maxfreq = _cpu_maxfreq(cpu.cluster);
    cpu.kernelversion = readfile("/proc/version");
    cpu.uploadgovernor(readfile((std::string)CPUFREQ + "policy0/scaling_available_governors"));

    switch (argc) {
        case 2:
            if ((std::string)argv[1] == "--info") {
                _showinfo(cpu);
            }
        break;
        case 3:
            if (!(getuid() == 0)) {
                std::cout<<"To use this start with SU\n";
                return 0;
            }

            if ((std::string)argv[1] == "-set-gov" ) {
                for(int i = 0; i != (int)cpu.available_gov.size(); ++i) {
                    if ((std::string)argv[2] == cpu.available_gov[i]) {
                        // when find governor set it and break
                        for (int k = 0; k != (int)cpu.cluster.size(); ++k)
                            setgovernor((std::string)CPUFREQ + cpu.cluster[k] + "/scaling_governor", cpu.available_gov[i]);
                        break;
                    }
                }
            }
        break;
        default:
            std::cout<<"You have to run it with a command\n";
    }

    std::cout<<"\n";
    return 0;
}