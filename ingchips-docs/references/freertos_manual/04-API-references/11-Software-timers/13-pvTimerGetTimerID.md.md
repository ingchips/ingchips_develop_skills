[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
 void *pvTimerGetTimerID( TimerHandle_t xTimer );
```

Returns the ID assigned to the [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).

IDs are assigned to timers using the `pvTimerID` parameter of the call to [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
that was used to create the timer.

An identifier (ID) is assigned to a timer when the timer is created, and can be
changed at any time using the [vTimerSetTimerID()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID) API function.

If the same callback function is assigned to multiple timers, the timer identifier
can be inspected inside the callback function to determine which timer actually
expired.

The timer identifier can also be used to store data in the timer between calls
to the timer’s callback function.


**Parameters:**

- *xTimer*

  The timer being queried.


**Returns:**

- The ID assigned to the timer being queried.


**Example usage:**

See the examples provided on the [xTimerCreate() documentation page](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
and the [vTimerSetTimerID() documentation page](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID).
