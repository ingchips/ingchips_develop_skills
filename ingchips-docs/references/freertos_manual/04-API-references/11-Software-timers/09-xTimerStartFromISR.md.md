[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h


```c
BaseType_t xTimerStartFromISR(
                              TimerHandle_t xTimer,
                              BaseType_t *pxHigherPriorityTaskWoken
                             );
```

A version of [xTimerStart()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart) that can be called from an interrupt service
routine.


**Parameters:**

+ *xTimer*

  The handle of the timer being started/restarted.

+ *pxHigherPriorityTaskWoken*

  The timer service/daemon task spends most of its time in the Blocked state, waiting for messages to
  arrive on the timer command queue. Calling xTimerStartFromISR() writes a message to the timer command
  queue, so has the potential to transition the timer service/daemon task out of the Blocked state. If
  calling xTimerStartFromISR() causes the timer service/daemon task to leave the Blocked state, and the
  timer service/daemon task has a priority equal to or greater than the currently executing task (the
  task that was interrupted), then \*pxHigherPriorityTaskWoken will get set to pdTRUE internally
  within the xTimerStartFromISR() function. If xTimerStartFromISR() sets this value to pdTRUE,
  then a context switch should be performed before the interrupt exits.


**Returns:**

 pdFAIL will be returned if the start command could not be sent to
 the timer command queue. pdPASS will be returned if the command was
 successfully sent to the timer command queue. When the command is actually
 processed will depend on the priority of the timer service/daemon task
 relative to other tasks in the system, although the timers expiry time is
 relative to when xTimerStartFromISR() is actually called. The timer service/daemon
 task priority is set by the configTIMER\_TASK\_PRIORITY configuration constant.


**Example usage:**

```c
/* This scenario assumes xBacklightTimer has already been created. When a
   key is pressed, an LCD back-light is switched on. If 5 seconds pass
   without a key being pressed, then the LCD back-light is switched off. In
   this case, the timer is a one-shot timer, and unlike the example given for
   the xTimerReset() function, the key press event handler is an interrupt
   service routine. */

/* The callback function assigned to the one-shot timer. In this case the
   parameter is not used. */
void vBacklightTimerCallback( TimerHandle_t pxTimer )
{
    /* The timer expired, therefore 5 seconds must have passed since a key
       was pressed. Switch off the LCD back-light. */
    vSetBacklightState( BACKLIGHT_OFF );
}

/* The key press interrupt service routine. */
void vKeyPressEventInterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Ensure the LCD back-light is on, then restart the timer that is
       responsible for turning the back-light off after 5 seconds of
       key inactivity. This is an interrupt service routine so can only
       call FreeRTOS API functions that end in "FromISR". */
    vSetBacklightState( BACKLIGHT_ON );

    /* xTimerStartFromISR() or xTimerResetFromISR() could be called here
       as both cause the timer to re-calculate its expiry time.
       xHigherPriorityTaskWoken was initialised to pdFALSE when it was
       declared (in this function). */
    if( xTimerStartFromISR( xBacklightTimer,
        &xHigherPriorityTaskWoken ) != pdPASS )
    {
        /* The start command was not executed successfully. Take appropriate
           action here. */
    }

    /* Perform the rest of the key processing here. */

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
