// this software help user to change kernel settings
#include <iostream>
#include "include/tool.hpp"
#include "include/class.hpp"

static void _showinfo(info cpu) {
/*    for (int i = 0; i != (int)cpu.cluster.size(); ++i)
        std::cout<<cpu.cluster[i]<<"\n";*/

    std::cout<<"Number of cluster : "<<cpu.cluster.size()<<"\n";

    std::cout<<"Max freq : "<<cpu.maxfreq<<" Ghz\n";
}

int main (int argc, char *argv[]) {
    info cpu;
    cpu.SearchCluster();

    cpu.maxfreq = _cpu_maxfreq(cpu.cluster);

    if (argc == 2) {
        std::string cmd(argv[1]);

        if (cmd == "--info") {
            _showinfo(cpu);
        }
    }

    std::cout<<"\n";
    return 0;
}