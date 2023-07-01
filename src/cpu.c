#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <stdio.h>

#include "utils.h"

int max_Thread(void) {

    DIR* directory;
    struct dirent* entry;
    int count = 0;

    // Apri la directory specificata
    directory = opendir("/sys/devices/system/cpu/cpufreq/");
    if (directory == NULL) {
        perror("Errore durante l'apertura della directory");
        return -1;
    }

    // Conta le cartelle nella directory
    while ((entry = readdir(directory)) != NULL) {
        if (entry->d_type == DT_DIR) {
            // Ignora le cartelle speciali "." e ".."
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
                count++;
            }
        }
    }

    closedir(directory);

    return count;
}

int cpuOnlineCheck(int dir) {
    FILE *fp;
    char buff[BUFFER_SIZE];
    int value;

    sprintf(buff, "/sys/devices/system/cpu/cpu%d/online", dir);

    fp = fopen(buff, "r");

    if (fp == NULL)
        return 0;
    
    fscanf(fp, "%d", &value);

    return value;
}

void cpuOnlineCheck(int dir) {
    FILE *fp;
    char buff[BUFFER_SIZE];
    int value;

    sprintf(buff, "/sys/devices/system/cpu/cpu%d/online", dir);

    fp = fopen(buff, "r");

    if (fp == NULL)
        return 0;
    
    fscanf(fp, "%d", &value);

    return value;
}

void cpuOnlineChange(int dir) {
    FILE *fp;
    char buff[BUFFER_SIZE];
    int value;

    sprintf(buff, "/sys/devices/system/cpu/cpu%d/online", dir);

    fp = fopen(buff, "w");

    if (fp == NULL)
        return 0;
    
    fscanf(fp, "%d", &value);

    return value;
}