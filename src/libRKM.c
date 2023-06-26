#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#include "utils.h"

int clear_ram(void)
{
    FILE *cmd;

    cmd = popen("sync; echo 3 > /proc/sys/vm/drop_caches", "r");

    if (cmd == NULL)
        return ERROR_POPEN;

    return pclose(cmd);
}

int cpu_load(void)
{
    unsigned long long prev_total_time = 0;
    unsigned long long prev_idle_time = 0;

    FILE *fp = fopen("/proc/stat", "r");
    if (fp == NULL)
    {
        perror("Error opening /proc/stat");
        return 1;
    }

    char buffer[BUFFER_SIZE];
    fgets(buffer, BUFFER_SIZE, fp);
    fclose(fp);

    // Parse CPU usage information from the first line
    char *token = strtok(buffer, " ");
    unsigned long long user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice;
    sscanf(token, "%*s %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu", &user, &nice, &system, &idle, &iowait, &irq, &softirq, &steal, &guest, &guest_nice);

    unsigned long long total_time = user + nice + system + idle + iowait + irq + softirq + steal;
    unsigned long long idle_time = idle + iowait;

    unsigned long long total_time_diff = total_time - prev_total_time;
    unsigned long long idle_time_diff = idle_time - prev_idle_time;

    double cpu_usage = 100.0 * (total_time_diff - idle_time_diff) / total_time_diff;

    printf("CPU Usage: %.2f%%\n", cpu_usage);

    prev_total_time = total_time;
    prev_idle_time = idle_time;

    sleep(1); // Sleep for 1 second before reading CPU usage again

    return 0;
}

int online_cpu(void)
{
    return sysconf(_SC_NPROCESSORS_ONLN);
}