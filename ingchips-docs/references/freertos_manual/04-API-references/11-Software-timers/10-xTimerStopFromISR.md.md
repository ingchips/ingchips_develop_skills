[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h


```c
BaseType_t xTimerStopFromISR(
                             TimerHandle_t xTimer,
                             BaseType_t *pxHigherPriorityTaskWoken
                            );
```

A version of [xTimerStop()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/05-xTimerStop) that can be called from an interrupt service
routine.


**Parameters:**

- *xTimer*

  The handle of the timer being stopped.

- *pxHigherPriorityTaskWoken*

  The timer service/daemon task spends most of its time in the Blocked state, waiting for messages to
  arrive on the timer command queue. Calling `xTimerStopFromISR()` writes a message to the timer command
  queue, so has the potential to transition the timer service/daemon task out of the Blocked state. If
  calling `xTimerStopFromISR()` causes the timer service/daemon task to leave the Blocked state, and the
  timer service/daemon task has a priority equal to or greater than the currently executing task (the
  task that was interrupted), then `pxHigherPriorityTaskWoken` will get set to `pdTRUE` internally within
  the `xTimerStopFromISR()` function. If `xTimerStopFromISR()` sets this value to `pdTRUE`, then a context
  switch should be performed before the interrupt exits.


**Returns:**

- *pdFAIL*

  `pdFAIL` will be returned if the stop command could not be sent to the timer command queue.

- *pdPASS*

  `pdPASS` will be returned if the command was
  successfully sent to the timer command queue. When the command is actually
  processed will depend on the priority of the timer service/daemon task
  relative to other tasks in the system. The timer service/daemon
  task priority is set by the `configTIMER_TASK_PRIORITY` configuration constant.


**Example usage:**

```c
/* This scenario assumes xTimer has already been created and started. When
   an interrupt occurs, the timer should be simply stopped. */

/* The interrupt service routine that stops the timer. */
void vAnExampleInterruptServiceRoutine( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* The interrupt has occurred - simply stop the timer.
       xHigherPriorityTaskWoken was set to pdFALSE where it was defined
       (within this function). As this is an interrupt service routine, only
       FreeRTOS API functions that end in "FromISR" can be used. */
    if( xTimerStopFromISR( xTimer, &xHigherPriorityTaskWoken ) != pdPASS )
    {
        /* The stop command was not executed successfully. Take appropriate
           action here. */
    }

    /* If xHigherPriorityTaskWoken equals pdTRUE, then a context switch
       should be performed. The syntax required to perform a context switch
       from inside an ISR varies from port to port, and from compiler to
       compiler. Inspect the demos for the port you are using to find the
       actual syntax required. */
    if( xHigherPriorityTaskWoken != pdFALSE )
    {
        /* Call the interrupt safe yield function here (actual function
           depends on the FreeRTOS port being used). */
    }
}
```
