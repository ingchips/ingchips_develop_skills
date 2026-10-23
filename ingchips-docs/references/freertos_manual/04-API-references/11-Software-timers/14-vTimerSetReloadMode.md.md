[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h


```c
 void vTimerSetReloadMode( TimerHandle_t xTimer,
                           const UBaseType_t uxAutoReload );
```

Updates the 'mode' of a [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) to be either an auto reload timer or a one-shot
timer.

An auto reload timer resets itself each time it expires, causing the timer to
expire (and therefore execute its callback) periodically.

A one shot timer does not automatically reset itself, so will only expire (and
therefore execute its callback) once unless it is manually restarted.

This API function is only available if the FreeRTOS/Source/timers.c source file
is included in the built project.


**Parameters:** 

- *xTimer* 

  The handle of the timer to update. The handle will have been returned from the call 
  to [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
  or [xTimerCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic) used to create the timer.

- *uxAutoReload*

  Set `uxAutoReload` to `pdTRUE` to set the timer into auto reload mode, or `pdFALSE` to set the timer into one shot mode.
