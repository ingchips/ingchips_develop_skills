# uxTaskGetSystemState()

[[Task Utilities](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h


```c
UBaseType_t uxTaskGetSystemState(
                       TaskStatus_t * const pxTaskStatusArray,
                       const UBaseType_t uxArraySize,
                       unsigned long * const pulTotalRunTime );
```

`configUSE_TRACE_FACILITY` must be defined as 1 in FreeRTOSConfig.h for `uxTaskGetSystemState()` to be available.


`uxTaskGetSystemState()` populates an `TaskStatus_t` structure for each task in the
system. `TaskStatus_t` structures contain, among other things, members for the task handle, task name,
task priority, task state, and total amount of run time consumed by the task.

See [vTaskGetInfo()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-vTaskGetInfo) for a version that populates a `TaskStatus_t` structure for a
single task, instead of every task.

**NOTE**: This function is intended for debugging use only as its use results in the scheduler remaining
suspended for an extended period.


**Parameters:**

- *pxTaskStatusArray*

  A pointer to an array of `TaskStatus_t` structures. The array must contain at least
  one `TaskStatus_t` structure for each task that is under the control of the RTOS. The number of tasks
  under the control of the RTOS can be determined using
  the [uxTaskGetNumberOfTasks()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function.

- *uxArraySize*

  The size of the array pointed to by the `pxTaskStatusArray` parameter. The size is specified as the
  number of indexes in the array (the number of `TaskStatus_t` structures contained in
  the array), not by the number of bytes in the array.

- *pulTotalRunTime*

  If `configGENERATE_RUN_TIME_STATS` is set to 1 in FreeRTOSConfig.h then `*pulTotalRunTime` is set
  by `uxTaskGetSystemState()` to the total run time (as defined by
  the [run time stats clock](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)) since the target booted. `pulTotalRunTime` can
  be set to NULL to omit the total run time value.


**Returns:**

- The number of `TaskStatus_t` structures that were populated
  by `uxTaskGetSystemState()`. This should equal the number returned by the `uxTaskGetNumberOfTasks()`
  API function, but will be zero if the value passed in the `uxArraySize` parameter was too small.


**Example usage:**

```c
/* This example demonstrates how a human readable table of run time stats
   information is generated from raw data provided by uxTaskGetSystemState().
   The human readable table is written to pcWriteBuffer. (see the vTaskList()
   API function which actually does just this). */
void vTaskGetRunTimeStats( char *pcWriteBuffer )
{
    TaskStatus_t *pxTaskStatusArray;
    volatile UBaseType_t uxArraySize, x;
    unsigned long ulTotalRunTime, ulStatsAsPercentage;

   /* Make sure the write buffer does not contain a string. */
   *pcWriteBuffer = 0x00;

   /* Take a snapshot of the number of tasks in case it changes while this
      function is executing. */
   uxArraySize = uxTaskGetNumberOfTasks();

   /* Allocate a TaskStatus_t structure for each task. An array could be
      allocated statically at compile time. */
   pxTaskStatusArray = pvPortMalloc( uxArraySize * sizeof( TaskStatus_t ) );

   if( pxTaskStatusArray != NULL )
   {
      /* Generate raw status information about each task. */
      uxArraySize = uxTaskGetSystemState( pxTaskStatusArray,
                                 uxArraySize,
                                 &ulTotalRunTime );

      /* For percentage calculations. */
      ulTotalRunTime /= 100UL;

      /* Avoid divide by zero errors. */
      if( ulTotalRunTime > 0 )
      {
         /* For each populated position in the pxTaskStatusArray array,
            format the raw data as human readable ASCII data. */
         for( x = 0; x < uxArraySize; x++ )
         {
            /* What percentage of the total run time has the task used?
               This will always be rounded down to the nearest integer.
               ulTotalRunTimeDiv100 has already been divided by 100. */
            ulStatsAsPercentage =
                  pxTaskStatusArray[ x ].ulRunTimeCounter / ulTotalRunTime;

            if( ulStatsAsPercentage > 0UL )
            {
               sprintf( pcWriteBuffer, "%stt%lutt%lu%%rn",
                                 pxTaskStatusArray[ x ].pcTaskName,
                                 pxTaskStatusArray[ x ].ulRunTimeCounter,
                                 ulStatsAsPercentage );
            }
            else
            {
               /* If the percentage is zero here then the task has
                  consumed less than 1% of the total run time. */
               sprintf( pcWriteBuffer, "%stt%lutt<1%%rn",
                                 pxTaskStatusArray[ x ].pcTaskName,
                                 pxTaskStatusArray[ x ].ulRunTimeCounter );
            }

            pcWriteBuffer += strlen( ( char * ) pcWriteBuffer );
         }
      }

      /* The array is no longer needed, free the memory it consumes. */
      vPortFree( pxTaskStatusArray );
   }
}
```

 
 ### The TaskStatus\_t definition

```c
typedef struct xTASK_STATUS
{
   /* The handle of the task to which the rest of the information in the
      structure relates. */
   TaskHandle_t xHandle;

   /* A pointer to the task's name. This value will be invalid if the task was
      deleted since the structure was populated! */
   const char *pcTaskName;

   /* A number unique to the task. */
   UBaseType_t xTaskNumber;

   /* The state in which the task existed when the structure was populated. */
   eTaskState eCurrentState;

   /* The priority at which the task was running (may be inherited) when the
      structure was populated. */
   UBaseType_t uxCurrentPriority;

   /* The priority to which the task will return if the task's current priority
      has been inherited to avoid unbounded priority inversion when obtaining a
      mutex. Only valid if configUSE_MUTEXES is defined as 1 in
      FreeRTOSConfig.h. */
   UBaseType_t uxBasePriority;

   /* The total run time allocated to the task so far, as defined by the run time stats clock. 
      Only valid when configGENERATE_RUN_TIME_STATS is defined as 1 in FreeRTOSConfig.h. */
   unsigned long ulRunTimeCounter;

   /* Points to the lowest address of the task's stack area. */
   StackType_t *pxStackBase;

   #if ( configRECORD_STACK_HIGH_ADDRESS == 1 )
       /* Points to the top address of the task's stack area. */
       StackType_t * pxTopOfStack;

       /* Points to the bottom address of the task's stack area. */
       StackType_t * pxEndOfStack;
   #endif

   /* The minimum amount of stack space that has remained for the task since
      the task was created. The closer this value is to zero the closer the task
      has come to overflowing its stack. */
   configSTACK_DEPTH_TYPE usStackHighWaterMark;
} TaskStatus_t;
```
