#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <stdio.h>

#include "utils.h"
#include "cpuid_thermal.h"

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

#ifdef get_index
#undef get_index
#endif

/**
 * Through a table we record the names of the vendors and associate
 * the index values. find out which vendor it is.
 * If there are no strings registered it returns error.
 */
#define get_index(index, string, data_array, max)       \
    do                                                  \
    {                                                   \
        index = -1;                                     \
        for (index = 0; index != max; ++index)          \
        {                                               \
            if (strcmp(string, data_array[index]) == 0) \
                break;                                  \
        }                                               \
    } while (0);

/**
 * From the index value of my vendor database found,
 * the same index corresponds to the corresponding thermal driver.
 * 
 * Check in which of the nodes that driver is present
 * (then check which path is dedicated to the CPU).
 */
static char *get_thermal_drivers_path(const char *vendorID_drivers) {
    FILE *cmd, *read;
    int lenght;
    char path[250], buff[50];
    char *ret;

    /** find thermal node **/
    cmd = popen("find /sys/devices/ -name temp1_input", "r");

    if (cmd == NULL)
        return NULL;

    while (fscanf(cmd, "%s", path) != EOF)
    {
        lenght = strlen(path);
        lenght -= strlen("temp1_input");
        path[lenght] = '\0';
        strcat(path, "name");
        read = fopen(path, "r");

        fscanf(read, "%s", buff);

        if (read == NULL)
            continue;

        if (strcmp(buff, vendorID_drivers) == 0) {
            fclose(read);
            goto reg;
        }

        fclose(read);
    }

    return NULL;

reg:
    path[lenght] = '\0';
    pclose(cmd);

    ret = malloc(((lenght + 1) * sizeof(char)));
    strcpy(ret, path);

    return ret;
}

/**
 * Collect CPU temperature information using the cpuID.
 * The CPUID is needed to find the right driver to collect
 * the temperature.
 */
float get_cpu_temp()
{
    VendorCPUID cpuid;
    float ret = -1;
    int index;
    char *path;

    /** collect cpuid **/
    cpuid = get_cpu_id_cpp();
    /** get index for my "database" **/
    get_index(index, cpuid->vendorIDString, vendorIDStr, VENDOR_ID_SIZE);

    path = get_thermal_drivers_path(thermalDrivers[index]);
    if (path == NULL) {
        fprintf(stderr, "\nVendorID Unknown");
        goto exit;
    }

    printf("%s", path);
    free(path);
exit:

    free(cpuid->vendorIDString);
    free(cpuid->vendorName);
    free(cpuid);
    return ret;
}