# xTimerPendFunctionCall()

[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]


timers.h

```c
 BaseType_t xTimerPendFunctionCall(
                            PendedFunction_t xFunctionToPend,
                            void *pvParameter1,
                            uint32_t ulParameter2,
                            TickType_t xTicksToWait );
```

Used to pend the execution of a function to the RTOS daemon task (the timer
service task, hence this function is pre-fixed with 'Timer').

Functions that can be deferred to the RTOS daemon task must have the following
prototype:

```c
 void vPendableFunction( void * pvParameter1, uint32_t ulParameter2 );
```

The pvParameter1 and ulParameter2 are provided for use by the application code.

INCLUDE\_xTimerPendFunctionCall() and configUSE\_TIMERS must both be set to 1 for xTimerPendFunctionCall() 
to be available.


**Parameters:** 

+ *xFunctionToPend* 

  The function to execute from the timer service/daemon task. The function must conform to the PendedFunction\_t 
  prototype as shown above.

+ *pvParameter1* 

  The value of the callback function's first parameter. The parameter has a void \* type to allow it to 
  be used to pass any type. For example, integer types can be cast to a void \*, or the void \* can be 
  used to point to a structure.

+ *ulParameter2* 

  The value of the callback function's second parameter.

+ *xTicksToWait* 

  Calling this function will result in a message being sent to the timer daemon task on a queue. xTicksToWait 
  is the amount of time the calling task should remain in the Blocked state (so not using any processing time) 
  for space to become available on the timer queue if the queue is found to be full. The length of the queue 
  is set by the value of configTIMER\_QUEUE\_LENGTH in FreeRTOSConfig.h.


**Returns:** 

pdPASS is returned if the message was successfully sent to the RTOS timer daemon task, otherwise pdFALSE 
is returned.
 
