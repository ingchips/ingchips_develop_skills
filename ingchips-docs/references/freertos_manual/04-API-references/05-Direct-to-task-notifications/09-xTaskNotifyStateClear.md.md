# xTaskNotifyStateClear, xTaskNotifyStateClearIndexed

[[RTOS Task Notification API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h

```c
BaseType_t xTaskNotifyStateClear( TaskHandle_t xTask );
  
BaseType_t xTaskNotifyStateClearIndexed( TaskHandle_t xTask, 
                                         UBaseType_t uxIndexToClear );
```

Each RTOS task has an array of [*task notifications*](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications). Each task notification
has a *notification state* that can be either ‘pending’ or ‘not pending’,
and a 32-bit *notification value*. 

If a notification is sent to an index within the array of notifications then
the notification at that index is said to be 'pending' until the task reads
its notification value or explicitly clears the notification state to 'not pending'
by calling xTaskNotifyStateClear().

xTaskNotifyStateClear() and xTaskNotifyStateClearIndexed() are equivalent macros - the only difference
being xTaskNotifyStateClearIndexed() can operate on any task notification within the
array and xTaskNotifyStateClear() always operates on the task notification at array index 0.

[configUSE\_TASK\_NOTIFICATIONS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
must set to 1 in FreeRTOSConfig.h (or be left undefined) for these macros to be available. The 
constant [configTASK\_NOTIFICATION\_ARRAY\_ENTRIES](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
sets the number of indexes in each task's array of task notifications.


**Backward compatibility information:**  

Prior to FreeRTOS V10.4.0 each task had a single "notification value", and
all task notification API functions operated on that value. Replacing the
single notification value with an array of notification values necessitated a
new set of API functions that could address specific notifications within the
array. xTaskNotifyStateClear() is the original API function, and remains
backward compatible by always operating on the notification value at index 0
within the array. Calling xTaskNotifyStateClear() is equivalent to calling
xTaskNotifyStateClearIndexed() with the uxIndexToNotify parameter set to 0.


**Parameters:** 

* *xTask*

  The handle of the RTOS task that will have its notification state cleared. Set xTask to NULL to clear the notification 
  state of the calling task. To obtain a task's handle create the task using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and make use of 
  the pxCreatedTask parameter, or create the task using [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) and store the returned 
  value, or use the task's name in a call to [xTaskGetHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities). The handle of the currently 
  executing RTOS task is returned by the [xTaskGetCurrentTaskHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function.

* *uxIndexToClear*

  The index within the target task's array of notification values to act upon. For example, setting uxIndexToClear to 1
  will clear the state of the notification at index 1 within the array. uxIndexToClear must be less than
  configTASK\_NOTIFICATION\_ARRAY\_ENTRIES. ulTaskNotifyStateClear() does not have this parameter and always acts on the
  notification at index 0.


**Returns:** 

If the task referenced by xTask had a notification pending, and the notification
was cleared, then pdTRUE is returned. If the task referenced by xTask didn't
have a notification pending then pdFALSE is returned.
 

**Example usage:**

[More examples are referenced from the main [RTOS task notifications page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* An example UART send function. The function starts a UART transmission then  
   waits to be notified that the transmission is complete. The transmission  
   complete notification is sent from the UART interrupt. The calling task's  
   notification state is cleared before the transmission is started to ensure it is  
   not co-incidentally already pending before the task attempts to block on its  
   notification state. */  

void vSerialPutString( const char * const pcStringToSend,  
                       unsigned short usStringLength )  
{  
const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 5000 );  
  
    /* xSendingTask holds the handle of the task waiting for the transmission to  
       complete. If xSendingTask is NULL then a transmission is not in progress.  
       Don't start to send a new string unless transmission of the previous string  
       is complete. */  
    if( ( xSendingTask == NULL ) && ( usStringLength > 0 ) )  
    {  
        /* Ensure the calling task's 0th notification state is not already  
           pending. */  
        xTaskNotifyStateClearIndexed( NULL, 0 );  

        /* Store the handle of the transmitting task. This is used to unblock  
           the task when the transmission has completed. */  
        xSendingTask = xTaskGetCurrentTaskHandle();  

        /* Start sending the string - the transmission is then controlled by an  
           interrupt. */  
        UARTSendString( pcStringToSend, usStringLength );  

        /* Wait in the Blocked state (so not using any CPU time) until the UART  
           ISR sends the 0th notification to xSendingTask to notify (and unblock) the  
           task when the transmission is complete. */  
        ulTaskNotifyTake( 0, pdTRUE, xMaxBlockTime );  
    }  
}  
```
