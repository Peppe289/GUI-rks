#ifndef __FAN_UTILS__
#define __FAN_UTILS__

#ifdef __cplusplus
extern "C"
{
#endif

    enum VendorMobo
    {
        ASUS_MOBO = 0,
        MOBO_SIZE
    };

    /**
     * Many laptops have specific modules in the kernel.
     * Here the list.
     */
    const char *motherboardStr[MOBO_SIZE] = {
        [ASUS_MOBO] = "asus",
    };

    int get_fan_speed(void);

#ifdef __cplusplus
}
#endif

#endif