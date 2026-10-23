task.h

```c
TaskHandle_t xTaskCreateStatic( TaskFunction_t pxTaskCode,
                                 const char * const pcName,
                                 const uint32_t ulStackDepth,
                                 void * const pvParameters,
                                 UBaseType_t uxPriority,
                                 StackType_t * const puxStackBuffer,
                                 StaticTask_t * const pxTaskBuffer );
```

Create a new [task](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines) 
and add it to the list of tasks that are ready to run. [configSUPPORT_STATIC_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
must be set to 1 in `FreeRTOSConfig.h` for this RTOS API function to be available.

Each task requires RAM that is used to hold the task state, and used by the task as its stack. If a task is 
created using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management). If a task is created 
using `xTaskCreateStatic()` then the RAM is provided by the application writer, which results in a greater 
number of parameters, but allows the RAM to be statically allocated at compile time. See 
the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.

If you are using [FreeRTOS-MPU](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit) then we recommend you 
use [xTaskCreateRestricted()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted) instead of `xTaskCreateStatic()`.


**Parameters:**
+ *pxTaskCode*     

  Pointer to the task entry function (just the name of the function that implements the task, see the 
  example below). 

  Tasks are normally [implemented as an infinite loop](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/05-Implementing-a-task); the function which 
  implements the task must never attempt to return or exit. Tasks can 
  however [delete themselves](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete).

+ *pcName*  

  A descriptive name for the task. This is mainly used to facilitate debugging, but can also be used 
  to [obtain a task handle](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities).

  The maximum length of a task's name is defined by `configMAX_TASK_NAME_LEN` in [FreeRTOSConfig.h](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization).                                                                                                                                                |
+ *ulStackDepth* 

  The `puxStackBuffer` parameter is used to pass an array of `StackType_t` variables 
  into `xTaskCreateStatic()`. `ulStackDepth` must be set to the number of indexes in the array.

  See the FAQ [How big should the stack be?](https://www.freertos.org/Why-FreeRTOS/FAQs/Memory-usage-boot-times-context#how-big-should-the-stack-be)                                                                                                                                                                  |
+ *pvParameters*  

  The value that is passed as the parameter to the created task.

  If `pvParameters` is set to the address of a variable then the variable must still exist when the created 
  task executes - so it is not valid to pass the address of a stack variable.                                                                                                                                                           |
+ *uxPriority* 

  The [priority](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities) at which the created task will execute.

  Systems that include MPU support can optionally create a task in a privileged (system) mode by setting 
  the bit `portPRIVILEGE_BIT` in `uxPriority`. For example, to create a privileged task at priority 2 
  set `uxPriority` to ( 2 | `portPRIVILEGE_BIT` ).

  Priorities are asserted to be less than `configMAX_PRIORITIES`. If `configASSERT` is undefined, priorities 
  are silently capped at (`configMAX_PRIORITIES` - 1).

+ *puxStackBuffer* 

  Must point to a `StackType_t` array that has at least `ulStackDepth` indexes (see the `ulStackDepth` 
  parameter above) - the array will be used as the task's stack, so it must be persistent (not declared 
  on the stack of a function).                                                                                                                                                                                   |
+ *pxTaskBuffer* 

  Must point to a variable of type `StaticTask_t`. The variable will be used to hold the new task's data 
  structures (TCB), so it must be persistent (not declared on the stack of a function).


**Returns:**

If neither `puxStackBuffer` or `pxTaskBuffer` are NULL then the task will be created, and the task's handle 
is returned. If either `puxStackBuffer` or `pxTaskBuffer` is NULL then the task will not be created and 
NULL will be returned.


**Example usage:**

```c
    /* Dimensions of the buffer that the task being created will use as its stack.
       NOTE: This is the number of words the stack will hold, not the number of
       bytes. For example, if each stack item is 32-bits, and this is set to 100,
       then 400 bytes (100 * 32-bits) will be allocated. */
    #define STACK_SIZE 200

    /* Structure that will hold the TCB of the task being created. */
    StaticTask_t xTaskBuffer;

    /* Buffer that the task being created will use as its stack. Note this is
       an array of StackType_t variables. The size of StackType_t is dependent on
       the RTOS port. */
    StackType_t xStack[ STACK_SIZE ];


    /* Function that implements the task being created. */
    void vTaskCode( void * pvParameters )
    {
        /* The parameter value is expected to be 1 as 1 is passed in the
           pvParameters value in the call to xTaskCreateStatic(). */
        configASSERT( ( uint32_t ) pvParameters == 1UL );

        for( ;; )
        {
            /* Task code goes here. */
        }
    }

    /* Function that creates a task. */
    void vOtherFunction( void )
    {
        TaskHandle_t xHandle = NULL;

        /* Create the task without using any dynamic memory allocation. */
        xHandle = xTaskCreateStatic(
                      vTaskCode,       /* Function that implements the task. */
                      "NAME",          /* Text name for the task. */
                      STACK_SIZE,      /* Number of indexes in the xStack array. */
                      ( void * ) 1,    /* Parameter passed into the task. */
                      tskIDLE_PRIORITY,/* Priority at which the task is created. */
                      xStack,          /* Array to use as the task's stack. */
                      &xTaskBuffer );  /* Variable to hold the task's data structure. */

        /* puxStackBuffer and pxTaskBuffer were not NULL, so the task will have
           been created, and xHandle will be the task's handle. Use the handle
           to suspend the task. */
        [vTaskSuspend](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/07-vTaskSuspend)( xHandle );
    }
```
