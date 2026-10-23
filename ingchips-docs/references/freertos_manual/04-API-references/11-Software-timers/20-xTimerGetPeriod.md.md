[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
 TickType_t xTimerGetPeriod( TimerHandle_t xTimer );
```

Returns the period of a [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers). The period is specified in ticks.

The period of a timer is initially set using the xTimerPeriod parameter of the call
to [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate) used to create the timer. It can then be changed
using the [xTimerChangePeriod()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod) and [xTimerChangePeriodFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR) API functions.


**Parameters:**

- *xTimer*

  The timer being queried.


**Returns:**

- The period of the timer, in ticks.


**Example usage:**

```c
/* A callback function assigned to a software timer. */
static void prvExampleTimerCallback( TimerHandle_t xTimer )
{
TickType_t xTimerPeriod;

    /* Query the period of the timer that expires. */
    xTimerPeriod = xTimerGetPeriod( xTimer );
}
```
