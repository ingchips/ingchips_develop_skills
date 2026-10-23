# vTaskGetInfo()

[[Task Utilities](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h

```c
void vTaskGetInfo( TaskHandle_t xTask,
                   TaskStatus_t *pxTaskStatus,
                   BaseType_t xGetFreeStackSpace,
                   eTaskState eState );
```

`configUSE_TRACE_FACILITY` must be defined as 1 in FreeRTOSConfig.h for `vTaskGetInfo()` to be available.

Whereas [uxTaskGetSystemState](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)() populates a [TaskStatus_t](#the-taskstatus_t-definition)
structure for each task in the system, `vTaskGetInfo()` populates a `TaskStatus_t` structures for just 
a single task. The `TaskStatus_t` structure contains, among other things, members for the task handle, 
task name, task priority, task state, and total amount of run time consumed by the task.

NOTE: This function is intended for debugging use only as its use results in the scheduler remaining 
suspended for an extended period.


**Parameters:** 

- *xTask*

  The handle of the task being queried. Setting xTask to NULL will return information on the calling task.
  
- *pxTaskStatus*

  The `TaskStatus_t` structure pointed to by `pxTaskStatus` will be filled with information about the 
  task referenced by the handle passed in the `xTask` parameter.
  
- *xGetFreeStackSpace* 

  The `TaskStatus_t` structure contains a member to report the stack high water mark of the task being 
  queried. The stack high water mark is the minimum amount of stack space that has ever existed, so the 
  closer the number is to zero the closer the task has come to overflowing its stack. Calculating the 
  stack high water mark takes a relatively long time, and can make the system temporarily unresponsive - 
  so the `xGetFreeStackSpace` parameter is provided to allow the high water mark checking to be skipped. 
  The high watermark value will only be written to the `TaskStatus_t` structure if `xGetFreeStackSpace` 
  is not set to `pdFALSE`.
  
- *eState*

  The `TaskStatus_t` structure contains a member to report the state of the task being queried. Obtaining 
  the task state is not as fast as a simple assignment - so the `eState` parameter is provided to allow the 
  state information to be omitted from the `TaskStatus_t` structure. To obtain state information then set 
  eState to `eInvalid` - otherwise the value passed in `eState` will be reported as the task state in 
  the `TaskStatus_t` structure.


**Example usage:**

```c
void vAFunction( void )
{
    TaskHandle_t xHandle;
    TaskStatus_t xTaskDetails;

    /* Obtain the handle of a task from its name. */
    xHandle = xTaskGetHandle( "Task_Name" );

    /* Check the handle is not NULL. */
    configASSERT( xHandle );

    /* Use the handle to obtain further information about the task. */
    vTaskGetInfo( /* The handle of the task being queried. */
                  xHandle,
                  /* The TaskStatus_t structure to complete with information
                     on xTask. */
                  &xTaskDetails,
                  /* Include the stack high water mark value in the
                     TaskStatus_t structure. */
                  pdTRUE,
                  /* Include the task state in the TaskStatus_t structure. */
                  eInvalid );
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

    /* The total run time allocated to the task so far, as defined by the run
       time stats clock. Only valid when configGENERATE_RUN_TIME_STATS is
       defined as 1 in FreeRTOSConfig.h. */
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
