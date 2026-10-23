# ulTaskNotifyTake, ulTaskNotifyTakeIndexed

[[RTOS Task Notification API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h

```c
uint32_t ulTaskNotifyTake( BaseType_t xClearCountOnExit,
                           TickType_t xTicksToWait );
   
uint32_t ulTaskNotifyTakeIndexed( UBaseType_t uxIndexToWaitOn, 
                                  BaseType_t xClearCountOnExit, 
                                  TickType_t xTicksToWait );
```

Each task has an array of 'task notifications' (or just 'notifications'), each
of which has a state and a 32-bit value. A [direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) 
is an event sent directly to a task that can unblock the receiving task, and
optionally update one of the receiving task’s notification values in a number of different ways. 
For example, a notification may overwrite one of the receiving task's notification values, or just set one or 
more bits in one of the receiving task's notification values.

`ulTaskNotifyTake()` is a macro intended for use when a task notification 
is [used as a faster and lighter weight binary or counting semaphore](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications) 
alternative. FreeRTOS semaphores are taken using the `xSemaphoreTake()` API function, `ulTaskNotifyTake()`
is the equivalent that uses a notification value in place of a semaphore.

`ulTaskNotifyTake()` and `ulTaskNotifyTakeIndexed()` are equivalent macros - the only difference
being `ulTaskNotifyTakeIndexed()` can operate on any task notification within the
array and `ulTaskNotifyTake()` always operates on the task notification at array index 0.

When a task is using a notification value as a binary or counting semaphore other tasks and interrupts 
should send notifications to it using either the [xTaskNotifyGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) macro, or 
the [xTaskNotify()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) function with the function’s eAction parameter set to eIncrement (the 
two are equivalent).

`ulTaskNotifyTake()` can either clear the task’s notification value to zero on exit, in which case the 
notification value acts like a binary semaphore, or decrement the task’s notification value on exit, in 
which case the notification value acts more like a counting semaphore.

An RTOS task can use `ulTaskNotifyTake()` to [optionally] block to wait for a task’s notification value. 
The task does not consume any CPU time while it is in the Blocked state.

**Note:** Each notification within the array operates independently – a task can only block on one 
notification within the array at a time and will not be unblocked by a notification sent to any other 
array index.

Whereas [xTaskNotifyWait()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) will return when a notification is pending, `ulTaskNotifyTake()` 
will return when the task’s notification value is not zero, decrementing the task’s notification value 
before it returns.

[configUSE\_TASK\_NOTIFICATIONS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must set to 1 in FreeRTOSConfig.h (or 
be left undefined) for these macros to be available. The 
constant [configTASK\_NOTIFICATION\_ARRAY\_ENTRIES](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
sets the number of indexes in each task's array of task notifications.


**Backward compatibility information:**  

Prior to FreeRTOS V10.4.0 each task had a single "notification value", and
all task notification API functions operated on that value. Replacing the
single notification value with an array of notification values necessitated a
new set of API functions that could address specific notifications within the
array. `ulTaskNotifyTake()` is the original API function, and remains backward
compatible by always operating on the notification value at index 0 in the
array. Calling `ulTaskNotifyTake()` is equivalent to calling
`ulTaskNotifyTakeIndexed()` with the `uxIndexToWaitOn` parameter set to 0.


**Parameters:** 

- *uxIndexToWaitOn*

  The index within the calling task's array of notification values on which the calling task will wait 
  for a notification to be non-zero. `uxIndexToWaitOn` must be less than `configTASK_NOTIFICATION_ARRAY_ENTRIES`. 
  
  `xTaskNotifyTake()` does not have this parameter and always waits for notifications on index 0.

- *xClearCountOnExit*

  If an RTOS task notification is received and `xClearCountOnExit` is set to `pdFALSE` then the RTOS task's 
  notification value is decremented before `ulTaskNotifyTake()` exits. This is equivalent to the value of a 
  counting semaphore being decremented by a successful call to `xSemaphoreTake()`. If an RTOS task notification 
  is received and `xClearCountOnExit` is set to `pdTRUE` then the RTOS task's notification value is reset 
  to 0 before `ulTaskNotifyTake()` exits. This is equivalent to the value of a binary semaphore being left
  at zero (or empty, or 'not available') after a successful call to `xSemaphoreTake()`.

- *xTicksToWait*

  The maximum time to wait in the Blocked state for a notification to be received if a notification is not 
  already pending when `ulTaskNotifyTake()` is called. The RTOS task does not consume any CPU time when it is 
  in the Blocked state. The time is specified in RTOS tick periods. The `pdMS_TO_TICKS()` macro can be used to 
  convert a time specified in milliseconds into a time specified in ticks.


**Returns:** 

 - The value of the task's notification value before it is decremented or
   cleared (see the description of `xClearCountOnExit`).
 

**Example usage:**

[More examples are referenced from the main [RTOS task notifications page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
 /* An interrupt handler. The interrupt handler does not perform any processing,  
    instead it unblocks a high priority task in which the event that generated the  
    interrupt is processed. If the priority of the task is high enough then the  
    interrupt will return directly to the task (so it will interrupt one task but  
    return to a different task), so the processing will occur contiguously in time -  
    just as if all the processing had been done in the interrupt handler itself. */  
void vANInterruptHandler( void )  
{  
    BaseType_t xHigherPriorityTaskWoken;  

    /* Clear the interrupt. */  
    prvClearInterruptSource();  

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE. If calling  
       vTaskNotifyGiveFromISR() unblocks the handling task, and the priority of  
       the handling task is higher than the priority of the currently running task,  
       then xHigherPriorityTaskWoken will automatically get set to pdTRUE. */  
    xHigherPriorityTaskWoken = pdFALSE;  

    /* Unblock the handling task so the task can perform any processing necessitated  
       by the interrupt. xHandlingTask is the task's handle, which was obtained  
       when the task was created. */  
    vTaskNotifyGiveIndexedFromISR( xHandlingTask, 0, &xHigherPriorityTaskWoken );  

    /* Force a context switch if xHigherPriorityTaskWoken is now set to pdTRUE.  
       The macro used to do this is dependent on the port and may be called  
       portEND_SWITCHING_ISR. */  
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  

/*-----------------------------------------------------------*/  

/* A task that blocks waiting to be notified that the peripheral needs servicing,  
   processing all the events pending in the peripheral each time it is notified to   
   do so. */  
void vHandlingTask( void *pvParameters )  
{  
    BaseType_t xEvent;  

    for( ;; )  
    {  
        /* Block indefinitely (without a timeout, so no need to check the function's  
           return value) to wait for a notification. Here the RTOS task notification  
           is being used as a binary semaphore, so the notification value is cleared  
           to zero on exit. NOTE! Real applications should not block indefinitely,  
           but instead time out occasionally in order to handle error conditions  
           that may prevent the interrupt from sending any more notifications. */  
        ulTaskNotifyTakeIndexed( 0,               /* Use the 0th notification */  
                                 pdTRUE,          /* Clear the notification value   
                                                     before exiting. */  
                                 portMAX_DELAY ); /* Block indefinitely. */  

        /* The RTOS task notification is used as a binary (as opposed to a  
           counting) semaphore, so only go back to wait for further notifications  
           when all events pending in the peripheral have been processed. */  
        do  
        {  
            xEvent = xQueryPeripheral();  

            if( xEvent != NO_MORE_EVENTS )  
            {  
                vProcessPeripheralEvent( xEvent );  
            }  
        } while( xEvent != NO_MORE_EVENTS );  
    }  
}  
```
