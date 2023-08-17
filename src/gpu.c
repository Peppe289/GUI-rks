#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

#include "utils.h"

int get_gpu_usage()
{
    char *path;
    int ret = -1;
    FILE *fp;

    /**
     * The GPUs running in standard systems is only 1.
     * So use this function which only finds the first reference.
     */
    path = find_file("/sys/devices/", "gpu_busy_percent");

    if (path == NULL)
        goto error;

    fp = fopen(path, "r");

    if (fp == NULL)
        goto error;

    fscanf(fp, "%d", &ret);

    fclose(fp);
    free(path);

error:
    return ret;
}

/**
 * Check in which of the nodes that driver name is present
 * (then check which path is dedicated to the GPU).
 * 
 * Find possible thermal nodes, then check what drivers they use.
 * In case of amd gpu in node/name must be "amdgpu".
 * 
 * Once found, return the root path.
 */
static char *get_thermal_drivers_path_gpu(const char *vendorID_drivers_gpu)
{
    FILE *cmd, *read;
    int lenght;
    char path[BUFFER_SIZE], buff[BUFFER_SIZE / 2];
    char *ret;

    /** find thermal node **/
    cmd = popen("find /sys/devices/ -name temp1_input", "r");

    if (cmd == NULL)
        return NULL;

    /**
     * Read the driver name in each path where a thermal node was found.
     */
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

        /**
         * Check the drivers node to see if it is the correct path.
         */
        if (strcmp(buff, vendorID_drivers_gpu) == 0)
        {
            fclose(read);
            goto reg;
        }

        fclose(read);
    }

    pclose(cmd);
    return NULL;

reg:
    path[lenght] = '\0';
    pclose(cmd);

    ret = malloc(((lenght + 1) * sizeof(char)));
    strcpy(ret, path);

    return ret;
}

/**
 * Returns the thermal value in degrees Celsius as an integer.
 * For now only for amdgpu.
 */
int get_gpu_thermal()
{
    FILE *fp;
    int ret = -1;
    char *path;

    /** now is only for amdgpu **/
    path = get_thermal_drivers_path_gpu("amdgpu");

    if (path == NULL)
        return ret;

    path = realloc(path, (strlen(path) +
                          strlen("temp1_input")) *
                             sizeof(char));
    strcat(path, "temp1_input");

    if (path == NULL)
        return ret;

    fp = fopen(path, "r");

    if (fp == NULL)
    {
        free(path);
        return ret;
    }
    fscanf(fp, "%d", &ret);

    free(path);
    fclose(fp);

    /** explicit the cast to integer **/
    return (int)(ret / 1000);
}
