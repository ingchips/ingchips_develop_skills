[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
BaseType_t xTimerChangePeriodFromISR(
                                     TimerHandle_t xTimer,
                                     TickType_t xNewPeriod,
                                     BaseType_t *pxHigherPriorityTaskWoken
                                    );
```

A version of [xTimerChangePeriod()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod) that can be called from an interrupt service
routine.


**Parameters:**

- *xTimer*

  The handle of the [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) that is having its period changed.

- *xNewPeriod*

  The new period for xTimer. Timer periods are specified in tick periods, so the constant portTICK\_PERIOD\_MS
  can be used to convert a time that has been specified in milliseconds. For example, if the timer must expire
  after 100 ticks, then xNewPeriod should be set to 100. Alternatively, if the timer must expire after 500ms,
  then xNewPeriod can be set to ( 500 / portTICK\_PERIOD\_MS ) provided configTICK\_RATE\_HZ is less than or
  equal to 1000.

- *pxHigherPriorityTaskWoken*

  The timer service/daemon task spends most of its time in the Blocked state, waiting for messages to
  arrive on the timer command queue. Calling xTimerChangePeriodFromISR() writes a message to the timer
  command queue, so has the potential to transition the timer service/daemon task out of the Blocked
  state. If calling xTimerChangePeriodFromISR() causes the timer service/daemon task to leave the Blocked
  state, and the timer service/daemon task has a priority equal to or greater than the currently executing
  task (the task that was interrupted), then *pxHigherPriorityTaskWoken* will get set to pdTRUE internally
  within the xTimerChangePeriodFromISR() function. If xTimerChangePeriodFromISR() sets this value to pdTRUE,
  then a context switch should be performed before the interrupt exits.


**Returns:**

- pdFAIL will be returned if the command to change the timers period could not be sent to the timer
  command queue.

- pdPASS will be returned if the command was successfully sent to the timer command queue.

- When the command is actually processed will depend on the priority of the timer service/daemon
  task relative to other tasks in the system. The timer service/daemon task
  priority is set by the configTIMER\_TASK\_PRIORITY configuration constant.


**Example usage:**

```c
/* This scenario assumes xTimer has already been created and started. When
   an interrupt occurs, the period of xTimer should be changed to 500ms. */

/* The interrupt service routine that changes the period of xTimer. */
void vAnExampleInterruptServiceRoutine( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* The interrupt has occurred - change the period of xTimer to 500ms.
       xHigherPriorityTaskWoken was set to pdFALSE where it was defined
       (within this function). As this is an interrupt service routine, only
       FreeRTOS API functions that end in "FromISR" can be used. */
    if( xTimerChangePeriodFromISR( xTimer,
                                   pdMS_TO_TICKS( 500 ),
                                   &xHigherPriorityTaskWoken ) != pdPASS )
    {
        /* The command to change the timers period was not executed
           successfully. Take appropriate action here. */
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
