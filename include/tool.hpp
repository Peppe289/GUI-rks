#include <fstream>
#include <vector>
#include <sstream>
#include <unistd.h>

std::string readfile(std::string filename);
float _cpu_maxfreq(std::vector<std::string> cluster);
void setgovernor(std::string directory, std::string governor);
void set_governor(std::string new_gov, std::vector<std::string> available_gov,
                                    std::vector<std::string> cluster);