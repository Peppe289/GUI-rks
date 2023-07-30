#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include "utils.h"

int get_gpu_usage() {
  char *path;
  int ret = -1;
  FILE *fp;

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