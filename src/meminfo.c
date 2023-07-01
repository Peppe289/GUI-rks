#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "utils.h"

struct meminfo {
    unsigned long int total;
    unsigned long int available;
};

void initMemInfo(struct meminfo *data) {
    data->total = 0;
    data->available = 0;
}

struct meminfo MemoryStats() {

    FILE *fp = fopen("/proc/meminfo", "r");
    struct meminfo ret;
    char line[BUFFER_SIZE];
    char *ptr;

    initMemInfo(&ret);

    if (fp == NULL) {
        //fprintf(stderr, "\nError for read memory info\n");
        return ret;
    }

    while (fgets(line, sizeof(line), fp)) {

        // if isn't this value continue
        int memtot = strncmp(line, "MemTotal", strlen("MemTotal"));
        int memav = strncmp(line, "MemAvailable", strlen("MemAvailable"));
        if (memtot && memav)
            continue;

        if (memtot == 0) {
            ptr = strchr(line, ':') + 1;
            sscanf(ptr, " %ld", &ret.total);
        } else {
            ptr = strchr(line, ':') + 1;
            sscanf(ptr, "%ld", &ret.available);
        }
    }

    fclose(fp);
    return ret;
}

void convert_kb_to_mb(struct meminfo *data) {
    data->available /= 1024;
    data->total /= 1024;
}

float memory_percentage() {
    struct meminfo data;
    unsigned long int buff;
    double ret;

    data = MemoryStats();
    buff = data.total - data.available;
    ret = ((float)buff / (float)data.total) * 100;

    return ret;
}