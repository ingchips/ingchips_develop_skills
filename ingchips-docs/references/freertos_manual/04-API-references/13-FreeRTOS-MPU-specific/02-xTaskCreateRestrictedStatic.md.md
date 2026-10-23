[[FreeRTOS-MPU Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

task.h

```c
BaseType_t xTaskCreateRestrictedStatic( TaskParameters_t *pxTaskDefinition,
                                        TaskHandle_t *pxCreatedTask );
```

Create a new Memory Protection Unit (MPU) restricted task and add it to the list of tasks that are ready to
run. [configSUPPORT\_STATIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set to 1
in `FreeRTOSConfig.h` for this RTOS API function to be available.

Internally, within the FreeRTOS implementation, each task requires two blocks of memory. The first block is
used to hold the task's data structures. The second block is used as the task's stack. If a task is created
using xTaskCreateRestricted() then the memory for the task's stack is provided by the application writer, and
the memory for the task's data structures is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management). If
a task is created using xTaskCreateRestrictedStatic() then the application writer must provide the memory for
the task's data structures too. xTaskCreateRestrictedStatic() therefore allows a memory protected task to be
created without using any dynamic memory allocation.

xTaskCreateRestrictedStatic() is intended for use with [FreeRTOS-MPU](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit),
the [demo applications](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos) which contain
comprehensive and documented examples of how to use the similar function, xTaskCreateRestricted().


**Parameters:**

* *pxTaskDefinition*

  Pointer to a structure that defines the task. The structure is described on this page.

* *pxCreatedTask*

  Used to pass back a handle by which the created task can be referenced.


**Returns:**

pdPASS if the task was successfully created and added to a ready list, otherwise an error code defined in the file projdefs.h


Tasks that include MPU support require even more parameters to create than those that don't. Passing each parameter to
xTaskCreateRestrictedStatic() individually would be unwieldy so instead the structure TaskParameters\_t is used to
allow the parameters to be configured statically at compile time. The structure is defined in task.h as:


---

```c
typedef struct xTASK_PARAMETERS
{
    TaskFunction_t pvTaskCode;
    const char * const pcName;
    unsigned short usStackDepth;
    void *pvParameters;
    UBaseType_t uxPriority;
    portSTACK_TYPE *puxStackBuffer;
    MemoryRegion_t xRegions[ portNUM_CONFIGURABLE_REGIONS ];
    #if ( ( portUSING_MPU_WRAPPERS == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) )
        StaticTask_t * const pxTaskBuffer;
    #endif
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

Following is a description of each structure member:


* pvTaskCode to uxPriority

  These members are exactly the same as the parameters of the same name sent to [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate).
  In particular uxPriority is used to set both the priority of the task and the mode in which the task will execute.
  For example, to create a User mode task at priority 2, simply set uxPriority to 2, to create a Privileged mode task
  at priority 2 set uxPriority to ( 2 | portPRIVILEGE\_BIT ).

* puxStackBuffer

  Each time a task is switched in, the MPU is dynamically re-configured to define a region that provides the task
  read and write access to its own stack.
  MPU regions must meet a number of constraints - in particular, the
  size and alignment of all such regions must be equal to the same power of two value.

  Standard FreeRTOS ports use pvPortMalloc() to allocate a new stack each time a task is created. Providing
  a pvPortMalloc() implementation that took care of the MPU data alignment requirements would be possible but
  would also be complex and inefficient in its RAM usage. To remove the need for this complexity FreeRTOS-MPU
  allows stacks to be declared statically at compile time. This allows the alignment to be managed using compiler
  extensions and RAM usage efficiency to be managed by the linker. For example, if using GCC, a stack could be
  declared and correctly aligned using the following code:

  ```c
  char cTaskStack[ 1024 ] __attribute__((aligned(1024));
  ```

  puxStackBuffer would normally be set to the address of the statically declared stack. As an alternative
  puxStackBuffer can be set to NULL - in which case pvPortMallocAligned() will be called to allocate the task
  stack and it is the application writer's responsibility to provide an implementation of pvPortMallocAligned()
  that meets the alignment requirements of the MPU.

* xRegions

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

* pxTaskBuffer

  Must point to a variable of type `StaticTask_t`. The variable will be used to hold the new task's
  data structures, so it must be persistent (not declared on the stack of a function).


**Example usage:**

```c
/* Create an TaskParameters_t structure that defines the task to be created.
 * The StaticTask_t variable is only included in the structure when
 * configSUPPORT_STATIC_ALLOCATION is set to 1. The PRIVILEGED_DATA macro can
 * be used to force the variable into the RTOS kernel's privileged data area. */
static PRIVILEGED_DATA StaticTask_t xTaskBuffer;
static const TaskParameters_t xCheckTaskParameters =
{
    vATask,     /* pvTaskCode - the function that implements the task. */
    "ATask",    /* pcName - just a text name for the task to assist debugging. */
    100,        /* usStackDepth - the stack size DEFINED IN WORDS. */
    NULL,       /* pvParameters - passed into the task function as the function parameters. */
    ( 1UL | portPRIVILEGE_BIT ), /* uxPriority - task priority, set the portPRIVILEGE_BIT
                                    if the task should run in a privileged state. */
    cStackBuffer, /* puxStackBuffer - the buffer to be used as the task stack. */

    /* xRegions - Allocate up to three separate memory regions for access by
     * the task, with appropriate access permissions. Different processors have
     * different memory alignment requirements - refer to the FreeRTOS documentation
     * for full information. */
    {
        /* Base address Length Parameters */
        { cReadWriteArray,              32,     portMPU_REGION_READ_WRITE },
        { cReadOnlyArray,               32,     portMPU_REGION_READ_ONLY },
        { cPrivilegedOnlyAccessArray,   128,    portMPU_REGION_PRIVILEGED_READ_WRITE }
    }

    &xTaskBuffer; /* Holds the task's data structure. */
};

 int main( void )
 {
 TaskHandle_t xHandle;

    /* Create a task from the const structure defined above. The task handle
     * is requested (the second parameter is not NULL) but in this case just for
     * demonstration purposes as its not actually used. */
    xTaskCreateRestricted( &xRegTest1Parameters, &xHandle );

    /* Start the scheduler. */
    vTaskStartScheduler();

    /* Will only get here if there was insufficient memory to create the idle
     * and/or timer task. */
    for( ;; );
}
```
