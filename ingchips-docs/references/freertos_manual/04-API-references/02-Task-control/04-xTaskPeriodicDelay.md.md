# xTaskPeriodicDelay()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h

```c
TickType_t xTaskPeriodicDelay( TickType_t * const pxPreviousWakeTime,
                               const TickType_t xTimeIncrement );
```

`INCLUDE_xTaskDelayUntil` must be defined as 1 for this function to be available.
See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Periodic task delay to ensure a constant execution frequency. Like
`xTaskDelayUntil()`, this function is intended to be called from the body of a
periodic task so that the task runs at a fixed interval, rather than at a fixed
delay after each iteration finishes.

`xTaskPeriodicDelay()` is intended to supersede `xTaskDelayUntil()` and differs
from it in three important respects:

1. `pxPreviousWakeTime` always holds the most recent wake time that is in the
   past, so it cannot "run away" ahead of the tick count.
2. If the calling task is prevented from running for longer than
   `xTimeIncrement` (for example because it was suspended, or because a higher
   priority task ran for a long time), `pxPreviousWakeTime` immediately catches
   up all of the skipped increments instead of the task being released
   repeatedly with no delay to work through the backlog.
3. The number of increments that were added to `pxPreviousWakeTime` is returned,
   so the caller can detect both missed periods and the case where it was called
   too early.

Unlike `xTaskDelayUntil()`, which returns immediately without blocking when the
next expected wake time has already passed, `xTaskPeriodicDelay()` always blocks
until the next wake time. The number of ticks it blocks for is
`xTimeIncrement - ( ( xTickCount - *pxPreviousWakeTime ) % xTimeIncrement )`,
which is always in the range 1 to `xTimeIncrement` inclusive. This means that if
the function is called before a full period has elapsed it returns 0 and still
waits until the next period boundary, rather than skipping a period.

The macro `pdMS_TO_TICKS()` can be used to calculate the number of ticks from a
time specified in milliseconds with a resolution of one tick period.

Note: `xTimeIncrement` must be greater than zero. `configASSERT()` is called on
both `pxPreviousWakeTime` and `xTimeIncrement`.


**Parameters:**


+ *pxPreviousWakeTime* 

  Pointer to a variable that holds the time at which the task was last unblocked. The variable must be 
  initialised with the current time prior to its first use (see the example below). Following this the 
  variable is automatically updated within `xTaskPeriodicDelay()`, and is always advanced by a whole number 
  of `xTimeIncrement` periods.

+ *xTimeIncrement* 

  The cycle time period. The task will be unblocked at time `(*pxPreviousWakeTime + xTimeIncrement)`. Calling 
  `xTaskPeriodicDelay` with the same `xTimeIncrement` parameter value will cause the task to execute with a 
  fixed interval period. Must be greater than zero.


**Returns:**

The number of times `xTimeIncrement` was added to `pxPreviousWakeTime`:

+ 0 on the first call, or if less than one full `xTimeIncrement` has elapsed since the last call.
+ 1 in normal circumstances, meaning exactly one period elapsed and no deadline was missed.
+ Greater than 1 if one or more periods were skipped, for example because the calling task was suspended 
  for more than `xTimeIncrement` ticks. The returned value is the number of periods that were caught up, so 
  a value of *n* means *n - 1* periods were missed.


**Example usage:** 

```c

// Perform an action every 10 ticks.
void vTaskFunction( void * pvParameters )
{
TickType_t xLastWakeTime;
const TickType_t xFrequency = 10;
TickType_t xPeriodsElapsed;

    // Initialise the xLastWakeTime variable with the current time.
    xLastWakeTime = xTaskGetTickCount ();
    for( ;; )
    {
        // Wait for the next cycle. This call always blocks until the next
        // period boundary.
        xPeriodsElapsed = xTaskPeriodicDelay( &xLastWakeTime, xFrequency );

        if( xPeriodsElapsed > 1 )
        {
            // ( xPeriodsElapsed - 1 ) periods were missed, for example because
            // this task was suspended or starved of processing time. The missed
            // periods have already been accounted for in xLastWakeTime.
        }

        // Perform action here.
    }
}
```
