#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "utils.h"

struct meminfo {
    unsigned long int total;
    unsigned long int available;
};

/**
 * init meminfo struct.
 */
static struct meminfo *initMemInfo() {
    struct meminfo *data = malloc(sizeof(struct meminfo));
    data->total = 0;
    data->available = 0;

    return data;
}

/**
 * Go to date and read lines to collect memory usage data.
 */
static struct meminfo *collect_memory_usage()
{
    FILE *fp = fopen("/proc/meminfo", "r");
    struct meminfo *ret;
    char line[BUFFER_SIZE];
    char *ptr;

    if (fp == NULL) {
        fprintf(stderr, "Error to read memory info");
        return NULL;
    }

    ret = initMemInfo();

    /**
     * Read all line of this path
     */
    while (fgets(line, sizeof(line), fp)) {

        /** if isn't this value continue **/
        int memtot = strncmp(line, "MemTotal", strlen("MemTotal"));
        int memav = strncmp(line, "MemAvailable", strlen("MemAvailable"));
        if (memtot && memav)
            continue;

        if (memtot == 0) {
            ptr = strchr(line, ':') + 1;
            sscanf(ptr, " %ld", &ret->total);
        } else {
            ptr = strchr(line, ':') + 1;
            sscanf(ptr, "%ld", &ret->available);
        }
    }

    fclose(fp);
    return ret;
}

/**
 * We don't need all this precision. we can reduce to mb
 */
void convert_kb_to_mb(struct meminfo *data) {
    data->available /= 1024;
    data->total /= 1024;
}

/**
 * This function takes care of providing the value
 * of the RAM used as a percentage.
 */
float memory_percentage() {
    struct meminfo *data;
    unsigned long int buff;
    double ret;

    data = collect_memory_usage();

    if (data == NULL)
        return 0;

    buff = data->total - data->available;
    ret = ((float)buff / (float)data->total) * 100;

    free(data);

    return ret;
}