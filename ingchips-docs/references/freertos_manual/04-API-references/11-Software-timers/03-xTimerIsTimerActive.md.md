[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h


```c
 BaseType_t xTimerIsTimerActive( TimerHandle_t xTimer );
```

Queries a [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) to see if it is active or dormant.

A timer will be dormant if:

1. It has been created but not started, or
2. It is an expired one-shot timer that has not been restarted.


Timers are created in the dormant state. The [xTimerStart()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart),
 [xTimerReset()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset),
 [xTimerStartFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/09-xTimerStartFromISR),
 [xTimerResetFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/12-xTimerResetFromISR),
 [xTimerChangePeriod()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod),
 and [xTimerChangePeriodFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR) API functions can all
 be used to transition a timer into the active state.


**Parameters:**

- *xTimer*

  The timer being queried.


**Returns:**

- pdFALSE will be returned if the timer is dormant.

- A value other than pdFALSE will be returned if the timer is active.


**Example usage:**

```c
 /* This function assumes xTimer has already been created. */
 void vAFunction( TimerHandle_t xTimer )
 {
     /* or more simply and equivalently
        "if( xTimerIsTimerActive( xTimer ) )" */
     if( xTimerIsTimerActive( xTimer ) != pdFALSE )
     {
         /* xTimer is active, do something. */
     }
     else
     {
         /* xTimer is not active, do something else. */
     }
 }
```
