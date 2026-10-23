# xTaskDelayUntil()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h

```c
BaseType_t xTaskDelayUntil( TickType_t *pxPreviousWakeTime,
                            const TickType_t xTimeIncrement );
```

`INCLUDE_xTaskDelayUntil` must be defined as 1 for this function to be available.
See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Delay a task until a specified time. This function can be used by periodic
tasks to ensure a constant execution frequency.

This function differs from `vTaskDelay()` in one important aspect: `vTaskDelay()` will
cause a task to block for the specified number of ticks from the time `vTaskDelay()` is
called whereas `xTaskDelayUntil()` will cause a task to block for the specified number
of ticks from the time specified in the `pxPreviousWakeTime` parameter. It is difficult
to use `vTaskDelay()` by itself to generate a fixed execution frequency, as the time
between a task starting to execute and that task calling `vTaskDelay()` may not be
fixed [the task may take a different path through the code between calls, or may get
interrupted or preempted a different number of times each time it executes]. `xTaskDelayUntil()`
can be used to generate a constant execution frequency. 

Whereas `vTaskDelay()` specifies a wake time relative to the time at which the function
is called, `xTaskDelayUntil()` specifies the absolute (exact) time at which it wishes to
unblock.

The macro `pdMS_TO_TICKS()` can be used to calculate the number of ticks from a
time specified in milliseconds with a resolution of one tick period.

Note: If a task calling this function misses its deadline (due to higher priority tasks,
interrupts, or processing delays), it doesn't try to "make up" the lost time by 
delaying further. Instead, it:

1. Immediately continues execution without blocking
2. Updates pxPreviousWakeTime to the calculated wake time (even though it's in the past)
3. Returns pdFALSE to indicate the task was not delayed

This prevents periodic tasks from getting permanently out of sync and allows them to resume
their regular timing pattern from the next cycle.


**Parameters:**


+ *pxPreviousWakeTime* 

  Pointer to a variable that holds the time at which the task was last unblocked. The variable must be 
  initialised with the current time prior to its first use (see the example below). Following this the 
  variable is automatically updated within `xTaskDelayUntil()`.

+ *xTimeIncrement* 

  The cycle time period. The task will be unblocked at time `(*pxPreviousWakeTime + xTimeIncrement)`. Calling 
  `xTaskDelayUntil` with the same `xTimeIncrement` parameter value will cause the task to execute with a fixed 
  interval period.


**Returns:**

A value which can be used to check whether the task was actually delayed: `pdTRUE` if the task was delayed 
and `pdFALSE` otherwise. A task will not be delayed if the next expected wake time is in the past.

Note: A return value of `pdTRUE` does not guarantee that `pxPreviousWakeTime` to be greater than the current tick
count. If the calling task becomes unblocked but is not able to execute due to a higher priority task executing, drift
may occur.


**Example usage:** 

```c

// Perform an action every 10 ticks.
void vTaskFunction( void * pvParameters )
{
TickType_t xLastWakeTime;
const TickType_t xFrequency = 10;
BaseType_t xWasDelayed;

    // Initialise the xLastWakeTime variable with the current time.
    xLastWakeTime = xTaskGetTickCount ();
    for( ;; )
    {
        // Wait for the next cycle.
        xWasDelayed = xTaskDelayUntil( &xLastWakeTime, xFrequency );

        // Perform action here. xWasDelayed value can be used to determine
        // whether a deadline was missed if the code here took too long.
    }
}
```
