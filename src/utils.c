#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

#include "utils.h"

int clear_ram(void)
{
    FILE *cmd;

    cmd = popen("sync; echo 3 > /proc/sys/vm/drop_caches", "r");

    if (cmd == NULL)
        return ERROR_POPEN;

    return pclose(cmd);
}

int online_cpu(void)
{
    return sysconf(_SC_NPROCESSORS_ONLN);
}