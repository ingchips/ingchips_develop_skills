# vTaskDelayUntil()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h

```c
void vTaskDelayUntil( TickType_t *pxPreviousWakeTime,
                      const TickType_t xTimeIncrement );
```

Prefer `INCLUDE_xTaskDelayUntil` for new projects. More on this API can be found
[here](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/03-xTaskDelayUntil).
This API performs the same as `vTaskDelayUntil` while providing additional information
through the returned value.

`INCLUDE_vTaskDelayUntil` must be defined as 1 for this function to be available.
See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Delay a task until a specified time. This function can be used by periodic
tasks to ensure a constant execution frequency.

This function differs from `vTaskDelay()` in one important aspect: `vTaskDelay()` specifies a time at
which the task wishes to unblock *relative* to the time at which `vTaskDelay()` is called, 
whereas `vTaskDelayUntil()` specifies an *absolute* time at which the task wishes to unblock.

`vTaskDelay()` will cause a task to block for the specified number of ticks from the time `vTaskDelay()` is
called. It is therefore difficult to use `vTaskDelay()` by itself to generate a fixed
execution frequency as the time between a task unblocking following a call to `vTaskDelay()` and that task
next calling `vTaskDelay()` may not be fixed (the task may take a different path through the
code between calls, or may get interrupted or preempted a different number of times
each time it executes).

Whereas `vTaskDelay()` specifies a wake time relative to the time at which the function
is called, `vTaskDelayUntil()` specifies the absolute (exact) time at which it wishes to
unblock.

It should be noted that `vTaskDelayUntil()` will return immediately (without blocking) if
it is used to specify a wake time that is already in the past. Therefore a task using
`vTaskDelayUntil()` to execute periodically will have to re-calculate its required wake time
if the periodic execution is halted for any reason (for example, the task is temporarily
placed into the Suspended state) causing the task to miss one or more periodic
executions. This can be detected by checking the variable passed by reference as 
the `pxPreviousWakeTime` parameter against the current tick count. This is however not necessary
under most usage scenarios.

The constant `portTICK_PERIOD_MS` can be used to calculate real time from the tick
rate - with the resolution of one tick period.

This function must not be called while the RTOS scheduler has been suspended by a call to `vTaskSuspendAll()`.


**Parameters:**

- *pxPreviousWakeTime*

  Pointer to a variable that holds the time at which the task was last unblocked. The variable must be 
  initialised with the current time prior to its first use (see the example below). Following this the 
  variable is automatically updated within `vTaskDelayUntil()`.
  
- *xTimeIncrement*

  The cycle time period. The task will be unblocked at time `(*pxPreviousWakeTime + xTimeIncrement)`. 
  Calling `vTaskDelayUntil` with the same `xTimeIncrement` parameter value will cause the task to execute 
  with a fixed interval period.


**Example usage:** 

```c
// Perform an action every 10 ticks.
void vTaskFunction( void * pvParameters )
{
    TickType_t xLastWakeTime;
    const TickType_t xFrequency = 10;

    // Initialise the xLastWakeTime variable with the current time.
    xLastWakeTime = xTaskGetTickCount();

    for( ;; )
    {
        // Wait for the next cycle.
        vTaskDelayUntil( &xLastWakeTime, xFrequency );

        // Perform action here.
    }
}
```
