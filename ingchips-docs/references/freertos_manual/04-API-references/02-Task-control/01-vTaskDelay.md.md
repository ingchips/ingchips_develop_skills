# vTaskDelay()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h 

```c
void vTaskDelay( const TickType_t xTicksToDelay );
```

`INCLUDE_vTaskDelay` must be defined as 1 for this function to be available.
See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Delay a task for a given number of ticks. The actual time that the task remains blocked depends on the 
tick rate. The constant `portTICK_PERIOD_MS` can be used to calculate real time from the tick rate - with 
the resolution of one tick period.

`vTaskDelay()` specifies a time at which the task wishes to unblock **relative to** the time at which `vTaskDelay()` 
is called. For example, specifying a block period of 100 ticks will cause the task to remain
blocked for 100 ticks after vTaskDelay() is called. The task will be unblocked on
the 100th tick after `vTaskDelay()` is called. 
`vTaskDelay()` does not therefore provide a good method of controlling the 
frequency of a periodic task as the path taken through the code, as well as other task and interrupt 
activity, will effect the frequency at which `vTaskDelay()` gets called and therefore the time at which 
the task next executes. See `vTaskDelayUntil()` for an alternative API function designed to facilitate 
fixed frequency execution. It does this by specifying an absolute time (rather than a relative time) at 
which the calling task should unblock. \
Passing 0 to `vTaskDelay()` shall yield to next ready task of equal priority.

**Parameters:**

- *xTicksToDelay*

  The amount of time, in tick periods, that the calling task should block.


**Example usage:** 

```c
void vTaskFunction( void * pvParameters )
{
    /* Block for 500ms. */
    const TickType_t xDelay = 500 / portTICK_PERIOD_MS;

    for( ;; )
    {
        /* Simply toggle the LED every 500ms, blocking between each toggle. */
        vToggleLED();
        vTaskDelay( xDelay );
    }
}
```
