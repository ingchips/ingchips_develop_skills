[[FreeRTOS-MPU Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

task.h

```c
void vTaskAllocateMPURegions(
               TaskHandle_t xTaskToModify,
               const MemoryRegion_t * const xRegions );
```

Memory regions are assigned to a restricted task when the task is created using
a call to `xTaskCreateRestricted()`. The regions can then be modified or redefined
at run time using `vTaskAllocateMPURegions()`.

`vTaskAllocateMPURegions()` is intended for use with [FreeRTOS-MPU](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit),
the [demo applications](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos) for which contain
an example of `vTaskAllocateMPURegions()` being used.


**Parameters:**

- *xTask*

  The handle of the task being updated.

- *xRegions*

  A pointer to an array of `MemoryRegion_t` structures, each of which contains a single new memory region definitions.
  The array should be dimensioned using the constant `portNUM_CONFIGURABLE_REGIONS`, which on the ARM Cortex-M3 is set to 3.

`MemoryRegion_t` is defined in task.h as:

```c
typedef struct xMEMORY_REGION
{
    void *pvBaseAddress;
    unsigned long ulLengthInBytes;
    unsigned long ulParameters;
} MemoryRegion_t;
```

The `pvBaseAddress` and `ulLengthInBytes` members are self explanatory as the start of the memory
region and the length of the memory region respectively.
It is important to note that MPU regions must meet a number of constraints - in particular, the
size and alignment of each region must both be equal to the same power of two value.

`ulParameters` defines how the task is permitted to access the memory region and can take the bitwise OR
of the following values:

```c
    portMPU_REGION_READ_WRITE
    portMPU_REGION_PRIVILEGED_READ_ONLY
    portMPU_REGION_READ_ONLY
    portMPU_REGION_PRIVILEGED_READ_WRITE
    portMPU_REGION_CACHEABLE_BUFFERABLE
    portMPU_REGION_EXECUTE_NEVER
```

Example usage (please refer to the FreeRTOS-MPU [demo applications](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)
for a much more complete and comprehensive example):

```c
/* Define an array that the task will both read from and write to. Make sure
   the size and alignment are appropriate for an MPU region (note this uses GCC
   syntax). */
static unsigned char ucOneKByte[ 1024 ] __attribute__((align( 1024 )));

/* Define an array of MemoryRegion\_t structures that configures an MPU region
   allowing read/write access for 1024 bytes starting at the beginning of the
   ucOneKByte array. The other two of the maximum 3 definable regions are
   unused so set to zero. */
static const MemoryRegion_t xAltRegions[ portNUM_CONFIGURABLE_REGIONS ] =
{
    /* Base address Length Parameters */
    { ucOneKByte, 1024, portMPU_REGION_READ_WRITE },
    { 0, 0, 0 },
    { 0, 0, 0 }
};

void vATask( void *pvParameters )
{
    /* This task was created such that it has access to certain regions of
       memory as defined by the MPU configuration. At some point it is
       desired that these MPU regions are replaced with that defined in the
       xAltRegions const struct above. Use a call to vTaskAllocateMPURegions()
       for this purpose. NULL is used as the task handle to indicate that this
       function should modify the MPU regions of the calling task. */
    vTaskAllocateMPURegions( NULL, xAltRegions );

    /* Now the task can continue its function, but from this point on can only
       access its stack and the ucOneKByte array (unless any other statically
       defined or shared regions have been declared elsewhere). */
}
```
