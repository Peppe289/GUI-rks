#ifndef __UTILS_RK_H__
#define __UTILS_RK_H__

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

#define ERROR_POPEN     (-1)

#define BUFFER_SIZE     400

#ifndef DT_DIR
#define DT_DIR  4
#endif

/**************************************
***************************************
***************************************/

/** directory utils **/

struct dir_data {
    int c_file; /** number of dir in directory **/
    char **n_file; /** directory name **/
};

typedef struct dir_data *DirData;

DirData collect_dir_info(const char *dir_path);
int get_dir_n(DirData data);
void free_dir_data(DirData data);

/** end direcotry utils **/

/**************************************
***************************************
***************************************/

/** memory utils **/

float memory_percentage();
int clear_ram(void);

/** end memory utils **/

#endif /** __UTILS_RK_H__ **/