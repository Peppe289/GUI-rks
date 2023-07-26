#ifndef __UTILS_RK_H__
#define __UTILS_RK_H__

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

#define ERROR_POPEN     (-1)

#define BUFFER_SIZE     255

#ifndef DT_DIR
#define DT_DIR  4
#endif

#ifndef DT_FILE
#define DT_FILE 8
#endif

#ifdef __cplusplus
extern "C" {
#endif

struct dir_data {
    int c_file; /** number of dir in directory **/
    char **n_file; /** directory name **/
};

typedef struct dir_data *DirData;

struct vendor_cpuid {
    unsigned int eax; /** thread **/
    char *vendorIDString;
    char *vendorName;
};

typedef struct vendor_cpuid *VendorCPUID;

/** directory utils **/
DirData collect_dir_info(const char *dir_path);
int get_dir_n(DirData data);
void free_dir_data(DirData data);
char *find_file(char *dir_path, const char *file);
/** end direcotry utils **/

/** memory utils **/
float memory_percentage();
int clear_ram(void);
/** end memory utils **/

/** GPU utils **/
int get_gpu_usage();
/** end GPU utils **/

/** Cpp **/
void *get_cpu_id_cpp();

#ifdef __cplusplus
}
#endif

#endif /** __UTILS_RK_H__ **/