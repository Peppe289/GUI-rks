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

#define print_err(...)                     \
    do                                     \
    {                                      \
        fprintf(stderr, "%s: ", __func__); \
        fprintf(stderr, __VA_ARGS__);      \
    } while (0);

#define print_info(...)                    \
    do                                     \
    {                                      \
        fprintf(stdout, "%s: ", __func__); \
        fprintf(stdout, __VA_ARGS__);      \
    } while (0);


#ifdef __cplusplus
extern "C" {
#endif

#define _likely(x)      __builtin_expect((x), 1)
#define _unlikely(x)    __builtin_expect((x), 0)

struct dir_data {
    int c_file; /** number of dir in directory **/
    char **n_file; /** directory name **/
};

typedef struct dir_data *DirData;

struct policy_attr {
    char **governor;
    int max_governor;
};

typedef struct policy_attr *Policy;

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
int get_gpu_thermal();
/** end GPU utils **/

/** CPU Utils **/
float get_cpu_temp();
int SingleThreadMaxFreq();
int max_Thread(void);
Policy get_possible_governor();
/** end CPU Utils **/

/** Cpp **/
void *get_cpu_id_cpp();

#ifdef __cplusplus
}
#endif

#endif /** __UTILS_RK_H__ **/