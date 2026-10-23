# xTimerGetReloadMode, uxTimerGetReloadMode

[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

task.h

```c
BaseType_t  xTimerGetReloadMode( TimerHandle_t xTimer );
UBaseType_t uxTimerGetReloadMode( TimerHandle_t xTimer );
```

Queries the 'mode' of the [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) referenced by the xTimer handle. 

The mode can be either an auto-reloaded timer, which automatically resets itself each time it expires, or a one-shot timer, 
which will expire only once unless it is manually restarted.

xTimerGetReloadMode and uxTimerGetReloadMode only differ in their return type. xTimerGetReloadMode returns BaseType\_t 
to match the type of the actual return value pdTRUE/pdFALSE. uxTimerGetReloadMode is provided for backward compatibility 
and new applications should use xTimerGetReloadMode instead.

These API functions are only available if the FreeRTOS 'timers.c' source file is included in the built project, and 
configUSE\_TIMERS is set to 1 in FreeRTOSConfig.h.


**Parameters:**

+ *xTimer* 

  The handle of the timer to query. The handle will have been returned from the call 
  to [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate) or [xTimerCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic) 
  which are used to create the timer.


**Returns:**

pdTRUE if the timer with handle xTimer is an auto-reload timer, otherwise pdFALSE.
