#ifndef __CPU_ID_UTILS_H__
#define __CPU_ID_UTILS_H__

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

#ifdef __cplusplus
extern "C" {
#endif

enum vendorIDcpu
{
    VENDOR_ID_INTEL     = 0,
    VENDOR_ID_AMD       = 1,
    VENDOR_ID_SIZE
};

const char *vendorIDStr[VENDOR_ID_SIZE] = {
    [VENDOR_ID_INTEL]   = "GenuineIntel",
    [VENDOR_ID_AMD]     = "AuthenticAMD",
};

const char *thermalDrivers[VENDOR_ID_SIZE] = {
    [VENDOR_ID_INTEL]   = "coretemp",
    /**
     * Athlon processor have same vendorIDstring
     * with AMD but use k8temp driver.
     * Check this in other part of code.
     */
    [VENDOR_ID_AMD]     = "k10temp",
};

#ifdef __cplusplus
}
#endif

#endif /** end __CPU_ID_UTILS_H__ **/
