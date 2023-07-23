#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <stdio.h>

#include "utils.h"

/**
 * This func read from "/sys/devices/system/cpu/cpufreq/" the node called policyX
 *
 * In x86 the cores are treated separately, so each thread has a policy.
 * For example:
 * $ ls /sys/devices/system/cpu/cpufreq/
 * output: policy0 policy1 policy2 policy3
 * aka 4 thread.
 */
int max_Thread(void)
{
    DirData dir_info = collect_dir_info("/sys/devices/system/cpu/cpufreq/");
    int ret;

    /**
     * We just need to know the quantity of the directories only.
     * After we can free the heap.
     */
    ret = get_dir_n(dir_info); /** collect number data **/
    free_dir_data(dir_info);   /** make free heap memory **/

    return ret;
}

/**
 * Through the node, identify the single policy and return
 * the value of the maximum frequency.
 */
int SingleThreadMaxFreq(int thread)
{
    FILE *fp;
    char path[BUFFER_SIZE];
    int value;

    /** save full path from argv int and open **/
    sprintf(path, "/sys/devices/system/cpu/cpufreq/policy%d/cpuinfo_max_freq", thread);
    fp = fopen(path, "r");

    /** Error to open file **/
    if (fp == NULL)
    {
        fprintf(stderr, "Error to open %s", path);
        return -1;
    }

    /** read node value as int **/
    fscanf(fp, "%d", &value);
    fclose(fp);

    return value;
}
