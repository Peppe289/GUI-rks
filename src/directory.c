#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

#include "utils.h"

#define d_alloc(ptr, size)            \
    do                                \
    {                                 \
        if (ptr == NULL)              \
            ptr = malloc(size);       \
        else                          \
            ptr = realloc(ptr, size); \
    } while (0);

/**
 * Add strings dynamically into pointer.
 */
static DirData add_new_dir(DirData dir_data, const char *data)
{
    int length = strlen(data);
    size_t index = dir_data->c_file - 1;
    d_alloc(dir_data->n_file, dir_data->c_file * sizeof(char *));

    dir_data->n_file[index] = malloc((length + 1) * sizeof(char));
    memcpy(dir_data->n_file[index], data, length * sizeof(char));

    return dir_data;
}

/**
 * init DirData.
 */
static DirData initDirData()
{
    DirData ret;
    ret = malloc(sizeof(struct dir_data) * 1);
    ret->c_file = 0;
    ret->n_file = NULL;

    return ret;
}

/**
 * This public function provides an interface to the modules
 * to obtain the number of folders present in the path.
 */
int get_dir_n(DirData data) {
    return data->c_file;
}

/**
 * This public function takes care of collecting the information
 * of the name and quantity of folders present in the directory.
 */
DirData collect_dir_info(const char *dir_path)
{
    DIR *directory;
    struct dirent *entry;
    DirData ret = initDirData();

    directory = opendir(dir_path);
    if (directory == NULL)
    {
        fprintf(stderr, "Error to open %s", dir_path);
        return NULL;
    }

    /**
     * Browse all files and identify folders only.
     */
    while ((entry = readdir(directory)) != NULL)
    {
        /** check if is direcotry. **/
        if (entry->d_type == DT_DIR)
        {
            /** skip special dir "." and ".." **/
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0)
            {
                ret->c_file++;
                ret = add_new_dir(ret, entry->d_name);
            }
        }
    }

    closedir(directory);

    return ret;
}

void free_dir_data(DirData data)
{
    int i;

    for (i = 0; i != data->c_file; ++i) {
        free(data->n_file[i]);
    }

    free(data->n_file);
    free(data);
}