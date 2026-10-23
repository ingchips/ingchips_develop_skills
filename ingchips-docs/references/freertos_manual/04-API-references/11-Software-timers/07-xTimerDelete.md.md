[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h


```c
 BaseType_t xTimerDelete( TimerHandle_t xTimer,
                          TickType_t xBlockTime );
```

[Software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) functionality is provided by a timer service/daemon task. Many
of the public FreeRTOS timer API functions send commands to the timer service task through a queue called
the timer command queue. The timer command queue is private to the RTOS kernel itself and is not directly
accessible to application code. The length of the timer command queue is set by the configTIMER\_QUEUE\_LENGTH
configuration constant.

xTimerDelete() deletes a timer that was previously created using the [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
API function. Note, when deleting a statically allocated timer, its static memory cannot be reused until
that timer is indicated inactive by [xTimerIsTimerActive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/03-xTimerIsTimerActive).

The configUSE\_TIMERS configuration constant must be set to 1 for xTimerDelete() to be available.


**Parameters:**

- *xTimer*

  The handle of the timer being deleted.

- *xBlockTime*

  Specifies the time, in ticks, that the calling task should be held in the Blocked state to wait for
  the delete command to be successfully sent to the timer command queue, should the queue already be
  full when xTimerDelete() was called. xBlockTime is ignored if xTimerDelete() is called before the
  RTOS scheduler is started.


**Returns:**

- pdFAIL will be returned if the delete command could not be sent to the timer command queue even
  after xBlockTime ticks had passed.

- pdPASS will be returned if the command was successfully sent to the timer command queue. When the command
  is actually processed will depend on the priority of the timer service/daemon task relative to other tasks
  in the system. The timer service/daemon task priority is set by the configTIMER\_TASK\_PRIORITY configuration
  constant.


**Example usage:**

See the example on the [xTimerChangePeriod() documentation page](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod).
