[[FreeRTOS-MPU Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

task.h

```c
BaseType_t xTaskCreateRestricted(
                            TaskParameters_t *pxTaskDefinition,
                            TaskHandle_t *pxCreatedTask );
```

Create a new Memory Protection Unit (MPU) restricted task and add it to the list of tasks that are ready to run.

xTaskCreateRestricted() is intended for use with [FreeRTOS-MPU](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit),
the [demo applications](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos) for which contain
comprehensive and documented examples of xTaskCreateRestricted() being used.


**Parameters:**

* *pxTaskDefinition*

  Pointer to a structure that defines the task. The structure is described on this page.

* *pxCreatedTask*

  Used to pass back a handle by which the created task can be referenced.


**Returns:**

pdPASS if the task was successfully created and added to a ready list, otherwise an error code defined in the file projdefs.h

Tasks that include MPU support require even more parameters to create than those that don't. Passing each parameter to
xTaskCreateRestricted() individually would be unwieldy so instead the structure TaskParameters\_t is used to
allow the parameters to be configured statically at compile time. The structure is defined in task.h as:

---

```c
typedef struct xTASK_PARAMETERS
{
    TaskFunction_t pvTaskCode;
    const signed char * const pcName;
    unsigned short usStackDepth;
    void *pvParameters;
    UBaseType_t uxPriority;
    portSTACK_TYPE *puxStackBuffer;
    MemoryRegion_t xRegions[ portNUM_CONFIGURABLE_REGIONS ];
} TaskParameters_t;
```

....where MemoryRegion\_t is defined as:

```c
typedef struct xMEMORY_REGION
{
    void *pvBaseAddress;
    unsigned long ulLengthInBytes;
    unsigned long ulParameters;
} MemoryRegion_t;
```

---

Following is a description of each structure member:

* pvTaskCode to uxPriority

  These members are exactly the same as the parameters to [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) of the same name.
  In particular uxPriority is used to set both the priority of the task and the mode in which the task will execute.
  For example, to create a User mode task at priority 2 simply set uxPriority to 2, to create a Privileged mode task
  at priority 2 set uxPriority to ( 2 | portPRIVILEGE\_BIT ).

* puxStackBuffer

  Each time a task is switched in the MPU is dynamically re-configured to define a region that provides the task
  read and write access to its own stack.
  MPU regions must meet a number of constraints - in particular, the
  size and alignment of each region must both be equal to the same power of two value.

  Standard FreeRTOS ports use pvPortMalloc() to allocate a new stacks each time a task is created. Providing
  a pvPortMalloc() implementation that took care of the MPU data alignment requirements would be possible but
  would also be complex and inefficient in its RAM usage. To remove the need for this complexity FreeRTOS-MPU
  allows stacks to be declared statically at compile time. This allows the alignment to be managed using compiler
  extensions and RAM usage efficiency to be managed by the linker. For example, if using GCC a stack could be
  declared and correctly aligned using the following code:

  ```c
  char cTaskStack[ 1024 ] __attribute__((aligned(1024));
  ```

  puxStackBuffer would normally be set to the address of the statically declared stack. As an alternative
  puxStackBuffer can be set to NULL - in which case pvPortMallocAligned() will be called to allocate the task
  stack and it is the application writers responsibility to provide an implementation of pvPortMallocAligned()
  that meets the alignment requirements of the MPU.

* xMemoryRegions

  xRegions is an array of MemoryRegion\_t structures, each of which defines a single user definable
  memory region for use by the task being created. The ARM Cortex-M3 FreeRTOS-MPU port defines
  portNUM\_CONFIGURABLE\_REGIONS to be 3.

  The pvBaseAddress and ulLengthInBytes members are self explanatory as the start of the memory
  region and the length of the memory region respectively. ulParameters defines how the task is
  permitted to access the memory region and can take the bitwise OR of the following values:

  ```c
  portMPU_REGION_READ_WRITE
  portMPU_REGION_PRIVILEGED_READ_ONLY
  portMPU_REGION_READ_ONLY
  portMPU_REGION_PRIVILEGED_READ_WRITE
  portMPU_REGION_CACHEABLE_BUFFERABLE
  portMPU_REGION_EXECUTE_NEVER
  ```

  **Note - the MPU region API differs between ARMv7-M and ARMv8-M ports.**
  The `portMPU_REGION_*` macros listed above apply to the **ARMv7-M** FreeRTOS-MPU
  ports: the ARM Cortex-M3 and Cortex-M4 ports (`ARM_CM3_MPU`, `ARM_CM4_MPU`,
  `ARM_CM4F_MPU`). On these ports `ulParameters` is a single pre-formatted value
  that maps directly onto the ARMv7-M MPU Region Attribute and Size Register
  (RASR), so the permissions are combined as the bitwise OR of the
  `portMPU_REGION_*` macros defined in the port's `portmacro.h`.

  The **ARMv8-M** ports - Cortex-M23, Cortex-M33, Cortex-M35P, Cortex-M55,
  Cortex-M85 and later (`ARM_CM23`, `ARM_CM33`, `ARM_CM35P`, `ARM_CM52`,
  `ARM_CM55`, `ARM_CM85`, `ARM_STAR_MC3`, with or without TrustZone) - use a
  different, port-independent set of macros declared in `task.h`. On ARMv8-M the
  region attributes are spread across several registers (RBAR, RLAR and the MAIR
  memory-attribute-indirection registers) and therefore cannot be expressed as a
  bitwise OR into a single register value. On these ports `ulParameters` is the
  bitwise OR of the following `tskMPU_REGION_*` values:

  ```c
  tskMPU_REGION_READ_ONLY                /* Read-only region. Omit for read/write access. */
  tskMPU_REGION_EXECUTE_NEVER            /* Region cannot be executed. */
  tskMPU_REGION_PRIVILEGED_EXECUTE_NEVER /* ARMv8.1-M (and later) ports only. */
  tskMPU_REGION_DEVICE_MEMORY            /* Device memory. Omit for normal (cacheable) memory. */
  ```

  Read/write access and normal memory are the defaults applied when the
  corresponding macro is omitted. Note that the shareability macros
  `tskMPU_REGION_NON_SHAREABLE`, `tskMPU_REGION_OUTER_SHAREABLE` and
  `tskMPU_REGION_INNER_SHAREABLE` are declared in `task.h` but are not currently
  applied by the ARMv8-M ports - all configurable regions are created as
  non-shareable (see [FreeRTOS-Kernel issue #1383](https://github.com/FreeRTOS/FreeRTOS-Kernel/issues/1383)).

  **Which macros does my port use?** If the port's `portmacro.h` defines the
  `portMPU_REGION_*` macros (the Cortex-M3 and Cortex-M4 MPU ports), use those.
  If you are building for an ARMv8-M port (Cortex-M23, Cortex-M33 and later), use
  the `tskMPU_REGION_*` macros from `task.h`.

---

Example usage (please refer to the FreeRTOS-MPU [demo applications](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)
for a much more complete and comprehensive example):

```c
/* Declare the stack that will be used by the task. The stack alignment must
   match its size and be a power of 2, so if 128 words are reserved for the stack
   then it must be aligned to ( 128 * 4 ) bytes. This example used GCC syntax. */
static portSTACK_TYPE xTaskStack[ 128 ] __attribute__((aligned(128*4)));

/* Declare an array that will be accessed by the task. The task should only
   be able to read from the array, and not write to it. */
char cReadOnlyArray[ 512 ] __attribute__((aligned(512)));

/* Fill in a TaskParameters_t structure to define the task - this is the
   structure passed to the xTaskCreateRestricted() function. */
static const TaskParameters_t xTaskDefinition =
{
    vTaskFunction, /* pvTaskCode */
    "A task", /* pcName */
    128, /* usStackDepth - defined in words, not bytes. */
    NULL, /* pvParameters */
    1, /* uxPriority - priority 1, start in User mode. */
    xTaskStack, /* puxStackBuffer - the array to use as the task stack. */

    /* xRegions - In this case only one of the three user definable regions is
       actually used. The parameters are used to set the region to read only. */
    {
        /* Base address Length Parameters */
        { cReadOnlyArray, mainREAD\_ONLY_ALIGN_SIZE, portMPU_REGION_READ_ONLY },
        { 0, 0, 0 },
        { 0, 0, 0 },
    }
};

void main( void )
{
    /* Create the task defined by xTaskDefinition. NULL is used as the second
       parameter as a task handle is not required. */
    xTaskCreateRestricted( &xTaskDefinition, NULL );

    /* Start the RTOS scheduler. */
    vTaskStartScheduler();

    /* Should not reach here! */
}
```
