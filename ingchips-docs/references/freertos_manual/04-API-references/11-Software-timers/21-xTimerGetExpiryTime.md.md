[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h


```c
 TickType_t xTimerGetExpiryTime( TimerHandle_t xTimer );
```

Returns the time at which the [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) will expire, which is the time at which the
timer's callback function will execute.

If the value returned by xTimerGetExpiryTime() is less than the current time
then the timer will expire after the tick count has overflowed and wrapped back
to 0. Overflows are handled in the RTOS implementation itself, so a timer's
callback function will execute at the correct time whether it is before or after
the tick count overflows.


**Parameters:**

- *xTimer*

  The timer being queried.


**Returns:**

- If the timer referenced by xTimer is [active](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/03-xTimerIsTimerActive), then the time
  at which the timer will next expire is returned (which may be after the current tick count has
  overflowed, see the notes above).

- If the timer referenced by xTimer is not active
  then the return value is undefined.


**Example usage:**

```c
static void prvAFunction( TimerHandle_t xTimer )
{
TickType_t xRemainingTime;

    /* Calculate the time that remains before the timer referenced by xTimer
       expires. TickType_t is an unsigned type, so the subtraction will result in
       the correct answer even if the timer will not expire until after the tick
       count has overflowed. */
    xRemainingTime = xTimerGetExpiryTime( xTimer ) - xTaskGetTickCount();
}
```
