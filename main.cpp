// this software help user to change kernel settings
#include <iostream>
#include "include/tool.hpp"
#include "include/class.hpp"

bool RootCheck() {
    if (getuid() == 0)
        return ROOTACCESS;

    return ERUSER;
}

void helper(std::string arg) {
    std::cout<<"Welcome to helper\n"
                "use "<<arg<<" with: \n";
    std::cout<<"-set-gov\t\t\tTo change current governor\n";
    std::cout<<"--info\t\t\t\tTo see all info about CPU and kernel\n";
}

int cmd_argc(int argc, char *argv[]) {

    // no cmd argv
    if (argc == 1)
        return 0;

    if (argc == 2 && (std::string)argv[1] == "--info")
        return 1;

    if (argc == 2 && (std::string)argv[1] == "--help")
        return 3;

    /*
     * is:
            1         2        3
     * ./programm -set-gov <governor>
     */
    if (argc == 2 && (std::string)argv[1] == "-set-gov") {
        /* 
         * is error bcs isn't used with governor name.
         * so, wen can't return value to set governor 
         */
        return 0;
    }
    else if (argc == 3 && (std::string)argv[1] == "-set-gov")
        return 2;

    return 0;
}

static void _showinfo(info cpu) {
    int i;

    std::cout<<"Number of cluster : "<<cpu.cluster.size()<<"\n";
    std::cout<<"Max freq : "<<cpu.maxfreq<<" Ghz";

    for (i = 0; i != (int)cpu.cluster.size(); ++i)
        std::cout<<"\nGovernor "<<cpu.cluster[i]<<" : "<<readfile((std::string)CPUFREQ + "policy" + std::to_string(i) + "/scaling_governor");

    std::cout<<"\nAvailable governor : ";
    for (i = 0; i != (int)cpu.available_gov.size(); ++i)
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

    /*
     * Switch DOC:
     * case 1: show info of CPU structure and kernel
     * case 2: change governor setting
     * default case: show message to run with command
     */
    switch (cmd_argc(argc, argv)) {
        case 1:
            _showinfo(cpu);
        break;
        case 2:
            if (!RootCheck()) {
                std::cout<<"Run as root. bye!\n";
                return 0;
            }
            set_governor((std::string)argv[2], cpu.available_gov, cpu.cluster);
        break;
        case 3:
            helper((std::string)argv[0]);
        break;
        default:
            std::cout<<"You have to run it with a command\n"
                        "To show all cmd use --help";
    }

    std::cout<<"\n";
    return 0;
}