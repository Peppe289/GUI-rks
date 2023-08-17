#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <stdio.h>

#include "utils.h"
#include "fan_utils.h"

/**
 * Searches for all possible fan control nodes.
 * Check which one is inherent to the motherboard.
 */
static char *get_mobo_module_path(const char *ModuleID)
{
    FILE *cmd, *read;
    int lenght;
    char path[BUFFER_SIZE], buff[BUFFER_SIZE / 2];
    char *ret;

    /** find thermal node **/
    cmd = popen("find /sys/devices/ -name fan1_input", "r");

    if (cmd == NULL)
        return NULL;

    /**
     * Read the driver name in each path where a thermal node was found.
     */
    while (fscanf(cmd, "%s", path) != EOF)
    {
        lenght = strlen(path);
        lenght -= strlen("fan1_input");
        path[lenght] = '\0';
        strcat(path, "name");
        read = fopen(path, "r");

        fscanf(read, "%s", buff);

        if (read == NULL)
            continue;

        /**
         * Check the drivers node to see if it is the correct path.
         */
        if (strcmp(buff, ModuleID) == 0)
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
 * Get the speed of the fans.
 */
int get_fan_speed()
{
    char *path;
    int index, ret = -1;
    FILE *fp;

    for (index = 0; index != MOBO_SIZE; ++index)
    {
        path = get_mobo_module_path(motherboardStr[index]);

        if (path != NULL)
            break;
    }

    if (path == NULL)
        return ret;

    path = realloc(path, (strlen(path) +
                          strlen("fan1_input")) *
                             sizeof(char));

    strcat(path, "fan1_input");

    fp = fopen(path, "r");

    if (fp == NULL) {
        free(path);
        return ret;
    }

    fscanf(fp, "%d", &ret);

    free(path);
    fclose(fp);

    return ret;
}