[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
 BaseType_t xTimerReset( TimerHandle_t xTimer,
                         TickType_t xBlockTime );
```

[Software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) functionality is provided by a timer service/daemon task. Many of the
public FreeRTOS timer API functions send commands to the timer service task
through a queue called the timer command queue. The timer command queue is
private to the RTOS kernel itself and is not directly accessible to application
code. The length of the timer command queue is set by the `configTIMER_QUEUE_LENGTH` configuration constant.

`xTimerReset()` re-starts a timer that was previously created using the [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
API function. If the timer had already been started and was already in the active state, then `xTimerReset()`
will cause the timer to re-evaluate its expiry time so that it is relative to when `xTimerReset()` was
called. If the timer was in the dormant state then `xTimerReset()` has equivalent functionality to
the [xTimerStart()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart) API function.

Resetting a timer ensures the timer is in the active state. If the timer
is not stopped, deleted, or reset in the mean time, the callback function
associated with the timer will get called 'n' ticks after `xTimerReset()` was
called, where 'n' is the timers defined period.

It is valid to call `xTimerReset()` before the RTOS scheduler has been started, but
when this is done the timer will not actually start until the RTOS scheduler is
started, and the timers expiry time will be relative to when the RTOS scheduler is
started, not relative to when `xTimerReset()` was called.

The `configUSE_TIMERS` configuration constant must be set to 1 for `xTimerReset()`
to be available.


**Parameters:**

- *xTimer*

  The handle of the timer being reset/started/restarted.

- *xBlockTime*

  Specifies the time, in ticks, that the calling task should be held in the Blocked state to wait for
  the reset command to be successfully sent to the timer command queue, should the queue already be
  full when `xTimerReset()` was called. `xBlockTime` is ignored if `xTimerReset()` is called before
  the RTOS scheduler is started.


**Returns:**

- `pdFAIL` will be returned if the reset command could not be
  sent to the timer command queue even after `xBlockTime` ticks had passed.

- `pdPASS` will be returned if the command was successfully sent to the timer
  command queue. When the command is actually processed will depend on the priority of the
  timer service/daemon task relative to other tasks in the system, although the
  timers expiry time is relative to when `xTimerReset()` is actually called. The
  timer service/daemon task priority is set by the `configTIMER_TASK_PRIORITY`
  configuration constant.


**Example usage:**

```c
/* When a key is pressed, an LCD back-light is switched on. If 5 seconds pass
   without a key being pressed, then the LCD back-light is switched off. In
   this case, the timer is a one-shot timer. */

TimerHandle_t xBacklightTimer = NULL;

/* The callback function assigned to the one-shot timer. In this case the
   parameter is not used. */
void vBacklightTimerCallback( TimerHandle_t pxTimer )
{
    /* The timer expired, therefore 5 seconds must have passed since a key
       was pressed. Switch off the LCD back-light. */
    vSetBacklightState( BACKLIGHT_OFF );
}

/* The key press event handler. */
void vKeyPressEventHandler( char cKey )
{
    /* Reset the timer that is responsible for turning the back-light off after
       5 seconds of key inactivity. Wait 10 ticks for the command to be
       successfully sent if it cannot be sent immediately. */
    if( xTimerReset( xBacklightTimer, 10 ) == pdPASS )
    {
        /* Turn on the LCD back-light. It will be turned off in the
           vBacklightTimerCallback after 5 seconds of key inactivity. */
        vSetBacklightState( BACKLIGHT_ON );
    }
    else
    {
        /* The reset command was not executed successfully. Take appropriate
           action here. */
    }

    /* Perform the rest of the key processing here. */
}

void main( void )
{
    /* Create then start the one-shot timer that is responsible for turning
       the back-light off if no keys are pressed within a 5 second period. */
    xBacklightTimer = xTimerCreate( "BacklightTimer", /* Just a text name, not used by the RTOS kernel */
                                    pdMS_TO_TICKS( 5000 ), /* The timer period in ticks. */
                                    pdFALSE,  /* The timer is a one-shot timer. */
                                    0, /* The id is not used by the callback so can take any value */
                                    vBacklightTimerCallback /* The callback function that switches the LCD back-light off */
                                  );

    if( xBacklightTimer == NULL )
    {
        /* The timer was not created. */
    }
    else
    {
        /* Start the timer. No block time is specified, and even if one was it
           would be ignored because the RTOS scheduler has not yet been started */
        if( xTimerStart( xBacklightTimer, 0 ) != pdPASS )
        {
            /* The timer could not be set into the Active state */
        }
    }

    /* ...
       Create tasks here
    ... */

    /* Starting the RTOS scheduler will start the timer running as it has
       already been set into the active state. */
    vTaskStartScheduler();

    /* Should not reach here. */
    for( ;; );
}
```
