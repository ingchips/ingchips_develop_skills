[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
 BaseType_t xTimerChangePeriod( TimerHandle_t xTimer,
                                TickType_t xNewPeriod,
                                TickType_t xBlockTime );
```

[Software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) functionality is provided by a timer service/daemon task. Many of the
public FreeRTOS timer API functions send commands to the timer service task
through a queue called the timer command queue. The timer command queue is
private to the RTOS kernel itself and is not directly accessible to application
code. The length of the timer command queue is set by the `configTIMER_QUEUE_LENGTH` configuration constant.

`xTimerChangePeriod()` changes the period of a timer that was previously
created using the [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate) API function.

`xTimerChangePeriod()` can be called to change the period of an active or
dormant state timer. Changing the period of a dormant timers will also start
the timer.

The `configUSE_TIMERS` configuration constant must be set to 1 for
`xTimerChangePeriod()` to be available.


**Parameters:** 

- *xTimer*

  The handle of the timer whose period will be changed.
  
- *xNewPeriod*

  The new period for `xTimer`. Timer periods are specified in tick periods, so the constant `portTICK_PERIOD_MS` 
  can be used to convert a time that has been specified in milliseconds. For example, if the timer must expire 
  after 100 ticks, then `xNewPeriod` should be set to 100. Alternatively, if the timer must expire after 500ms, 
  then `xNewPeriod` can be set to ( 500 / `portTICK_PERIOD_MS` ) provided `configTICK_RATE_HZ` is less than
  or equal to 1000. The timer period must be greater than 0.
  
- *xBlockTime*

  Specifies the time, in ticks, that the calling task should be held in the Blocked state to wait for the 
  change period command to be successfully sent to the timer command queue, should the queue already be full 
  when `xTimerChangePeriod()` was called. `xBlockTime` is ignored if `xTimerChangePeriod()` is called before 
  the RTOS scheduler is started.


**Returns:** 

- `pdFAIL` will be returned if the change period command could not be
  sent to the timer command queue even after `xBlockTime` ticks had passed.
  
- `pdPASS` will be returned if the command was successfully sent to the timer
  command queue. When the command is actually processed will depend on the
  priority of the timer service/daemon task relative to other tasks in the
  system. 
  
  The timer service/daemon task priority is set by the `configTIMER_TASK_PRIORITY` configuration constant.
 

**Example usage:**

```c
/* This function assumes xTimer has already been created. If the timer
   referenced by xTimer is already active when it is called, then the timer
   is deleted. If the timer referenced by xTimer is not active when it is
   called, then the period of the timer is set to 500ms and the timer is
   started. */
void vAFunction( TimerHandle_t xTimer )
{
    /* or more simply and equivalently
       "if( xTimerIsTimerActive( xTimer ) )" */
    if( xTimerIsTimerActive( xTimer ) != pdFALSE )
    {
        /* xTimer is already active - delete it. */
        xTimerDelete( xTimer );
    }
    else
    {
        /* xTimer is not active, change its period to 500ms. This will also
           cause the timer to start. Block for a maximum of 100 ticks if the
           change period command cannot immediately be sent to the timer
           command queue. */
        if( xTimerChangePeriod( xTimer, 500 / portTICK_PERIOD_MS, 100 )
                                                            == pdPASS )
        {
            /* The command was successfully sent. */
        }
        else
        {
            /* The command could not be sent, even after waiting for 100 ticks
               to pass. Take appropriate action here. */
        }
    }
}
```
