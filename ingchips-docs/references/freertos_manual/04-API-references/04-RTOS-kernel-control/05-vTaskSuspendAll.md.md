[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h 

```c
void vTaskSuspendAll( void );
```

Suspends the scheduler. Suspending the scheduler prevents a context switch from occurring but leaves 
interrupts enabled. If an interrupt requests a context switch while the scheduler is suspended, then 
the request is held pending and is performed only when the scheduler is resumed (un-suspended).

Calls to [xTaskResumeAll()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/06-xTaskResumeAll) transition the scheduler out of the Suspended state following 
a previous call to `vTaskSuspendAll()`.

Calls to `vTaskSuspendAll()` can be nested. The same number of calls must be made to `xTaskResumeAll()` 
as have previously been made to `vTaskSuspendAll()` before the scheduler will leave the Suspended state 
and re-enter the Active state.

`xTaskResumeAll()` must only be called from an executing task and therefore must not be called while 
the scheduler is in the Initialization state (prior to the scheduler being started).

Other FreeRTOS API functions must not be called while the scheduler is suspended.

API functions that have the potential to cause a context switch (for example, `vTaskDelayUntil()`, `xQueueSend()`, 
etc.) must **not** be called while the scheduler is suspended.


**Example usage:**

```c
/* A function that suspends then resumes the scheduler. */
void vDemoFunction( void )
{
    /* This function suspends the scheduler. When it is called from vTask1 the 
       scheduler is already suspended, so this call creates a nesting depth of 2. */
    vTaskSuspendAll();
 
    /* Perform an action here. */
 
    /* As calls to vTaskSuspendAll() are nested, resuming the scheduler here will 
       not cause the scheduler to re-enter the active state. */
    xTaskResumeAll();
}


void vTask1( void * pvParameters )
{
    for( ;; )
    {
        /* Perform some actions here. */
 
        /* At some point the task wants to perform an operation during which it does 
           not want to get swapped out, or it wants to access data which is also 
           accessed from another task (but not from an interrupt). It cannot use
           taskENTER_CRITICAL()/taskEXIT_CRITICAL() as the length of the operation may
           cause interrupts to be missed. */
 
        /* Prevent the scheduler from performing a context switch. */
        vTaskSuspendAll();
 
        /* Perform the operation here. There is no need to use critical sections as 
           the task has all the processing time other than that utilized by interrupt 
           service routines.*/ 
 
        /* Calls to vTaskSuspendAll() can be nested so it is safe to call a (non API) 
           function which also contains calls to vTaskSuspendAll(). API functions 
           should not be called while the scheduler is suspended. */
        vDemoFunction();

        /* The operation is complete. Set the scheduler back into the Active 
           state. */
        if( xTaskResumeAll() == pdTRUE )
        {
            /* A context switch occurred within xTaskResumeAll(). */
        }
        else
        {
            /* A context switch did not occur within xTaskResumeAll(). */
        }
    }
}
```
