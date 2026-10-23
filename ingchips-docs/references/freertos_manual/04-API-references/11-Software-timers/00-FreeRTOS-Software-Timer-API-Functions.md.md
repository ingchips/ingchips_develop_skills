# Software Timers

## FreeRTOS Software Timer API Functions

* [xTimerCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
* [xTimerCreateStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic)
* [xTimerIsTimerActive](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/03-xTimerIsTimerActive)
* [pvTimerGetTimerID](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID)
* [pcTimerGetName](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/19-pcTimerGetName)
* [vTimerSetReloadMode](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/14-vTimerSetReloadMode)
* [xTimerStart](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)
* [xTimerStop](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/05-xTimerStop)
* [xTimerChangePeriod](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod)
* [xTimerDelete](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/07-xTimerDelete)
* [xTimerReset](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset)
* [xTimerStartFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/09-xTimerStartFromISR)
* [xTimerStopFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/10-xTimerStopFromISR)
* [xTimerChangePeriodFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR)
* [xTimerResetFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/12-xTimerResetFromISR)
* [vTimerResetState](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)
* [pvTimerGetTimerID](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID)
* [vTimerSetTimerID](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID)
* [xTimerGetTimerDaemonTaskHandle](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)
* [xTimerPendFunctionCall](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/17-xTimerPendFunctionCall)
* [xTimerPendFunctionCallFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/18-xTimerPendFunctionCallFromISR)
* [xTimerGetPeriod](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/20-xTimerGetPeriod)
* [xTimerGetExpiryTime](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/21-xTimerGetExpiryTime)
* [xTimerGetReloadMode](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/23-xTimerGetReloadMode)

---


### xTimerGetTimerDaemonTaskHandle

timers.h
 
```c
TaskHandle_t xTimerGetTimerDaemonTaskHandle( void );
```

**Returns:** 

Returns the task handle associated with the software timer daemon
(or service) task. If configUSE\_TIMERS is set to 1 in
FreeRTOSConfig.h, then the timer daemon task is created
automatically when the RTOS scheduler is started.
 
---


### pcTimerGetName

timers.h
 
```c
const char * pcTimerGetName( TimerHandle_t xTimer )
```

Returns the human readable name assigned to a timer when the timer was
created.
 

**Parameters:** 

+ *xTimer*  

  The handle of the timer being queried.


**Returns:** 

A pointer to the timer's name, which is a standard NULL terminated C string.
 
---

### vTimerResetState

timers.h
 
```c
void vTimerResetState( void );
```

This function resets the internal state of the timer module. 
It must be called by the application before restarting the scheduler.
 
---
