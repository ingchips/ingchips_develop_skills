[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
 void vTimerSetTimerID( TimerHandle_t xTimer, void *pvNewID );
```

An identifier (ID) is assigned to a [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) when the timer is created, and can be
changed at any time using the `vTimerSetTimerID()` API function.

If the same callback function is assigned to multiple timers, the timer identifier
can be inspected inside the callback function to determine which timer actually
expired.

The timer identifier can also be used to store data in the timer between calls
to the timer's callback function.


**Parameters:**

- *xTimer*

  The timer being updated.


- *pvNewID*

  The handle to which the timer's identifier will be set.


**Example usage:**

```c
/* A callback function assigned to a timer. */
void TimerCallbackFunction( TimerHandle_t pxExpiredTimer )
{
uint32_t ulCallCount;

    /* A count of the number of times this timer has expired
       and executed its callback function is stored in the
       timer's ID. Retrieve the count, increment it, then save
       it back into the timer's ID. */
    ulCallCount =
        ( uint32_t ) [pvTimerGetTimerID](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID)( pxExpiredTimer );
    ulCallCount++;
    vTimerSetTimerID( pxExpiredTimer, ( void * ) ulCallCount );
}
```
