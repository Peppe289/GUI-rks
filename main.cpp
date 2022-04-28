// this software help user to change kernel settings
#include <iostream>
#include "include/tool.hpp"
#include "include/class.hpp"

int main (int argc, char *argv[]) {
    info cpu;
    cpu.SearchCluster();

/*  for (int i = 0; i != (int)cpu.cluster.size(); ++i)
        std::cout<<cpu.cluster[i]<<"\n";

    std::cout<<"Number of cluster : "<<cpu.cluster.size()<<"\n"; */

    cpu.maxfreq = _cpu_maxfreq(cpu.cluster);

//  std::cout<<"Max CPU freq : "<<cpu.maxfreq<<" Ghz";

    std::cout<<"\n";
    return 0;
}