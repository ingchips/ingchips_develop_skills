# ulTaskNotifyValueClear, ulTaskNotifyValueClearIndexed

[[RTOS Task Notification API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h

```c
uint32_t ulTaskNotifyValueClear( TaskHandle_t xTask, 
                                 uint32_t ulBitsToClear );
  
uint32_t ulTaskNotifyValueClearIndexed( TaskHandle_t xTask, 
                                        UBaseType_t uxIndexToClear,
                                        uint32_t ulBitsToClear );
```

Each RTOS task has an array of [*task notifications*](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications). Each task notification
has a *notification state* that can be either ‘pending’ or ‘not pending’,
and a 32-bit *notification value*. 

`ulTaskNotifyValueClearIndexed()` clears the bits specified by the `ulBitsToClear` bit mask in the notification
value at array index `uxIndexToClear` of the task referenced by `xTask`.

`ulTaskNotifyValueClear()` and `ulTaskNotifyValueClearIndexed()` are equivalent macros - the only difference
being `ulTaskNotifyValueClearIndexed()` can operate on any task notification within the
array and `ulTaskNotifyValueClear()` always operates on the task notification at array index 0.

[configUSE\_TASK\_NOTIFICATIONS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
must set to 1 in FreeRTOSConfig.h (or be left undefined) for these macros to be available.
The constant [configTASK\_NOTIFICATION\_ARRAY\_ENTRIES](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) sets the 
number of indexes in each task's array of task notifications.


**Parameters:**

- *xTask*

  The handle of the RTOS task that will have bits in its notification value cleared. Set `xTask` to NULL 
  to clear bits in the notification value of the calling task. To obtain a task’s handle, create the task 
  using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and make use of the `pxCreatedTask` parameter, or create the task 
  using [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) and store the returned value, or use the task’s name 
  in a call to [xTaskGetHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities).
  
  The handle of the currently executing RTOS task is returned by 
  the [xTaskGetCurrentTaskHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function.

- *uxIndexToClear*

  The index within the target task's array of notification values in which to clear the bits. `uxIndexToClear` 
  must be less than `configTASK_NOTIFICATION_ARRAY_ENTRIES`. `ulTaskNotifyValueClear()` does not have this 
  parameter and always clears bits in the notification value at index 0.

- *ulBitsToClear*

  Bit mask of the bits to clear in the notification value of `xTask`. Set a bit to 1 to clear the corresponding 
  bits in the task's notification value. Set `ulBitsToClear` to 0xffffffff (`UINT_MAX` on 32-bit architectures) 
  to clear the notification value to 0. Set `ulBitsToClear` to 0 to query the task's notification value without 
  clearing any bits.


**Returns:**

- The value of the target task's notification value before the bits specified by `ulBitsToClear` were cleared.


**Example usage:**

```c
    #define MESSAGE_RECEIVED_BIT 8  
    #define TICKS_UNTIL_TIMEOUT  100  

    unsigned long ulNotification, ulMessageReceivedMask;  

    /* Clear any message received events. */  
    ulMessageReceivedMask = 1u << MESSAGE_RECEIVED_BIT;  
    ulTaskNotifyValueClear( ulMessageReceivedMask );  

    /* Send a message that expects a response. */  
    send_message();  

    /* Block this task until it has another pending notification. In this example,  
       the task only ever uses the MESSAGE_RECEIVED_BIT of its notification value,   
       so the next event can only ever be on message received. */  

    xTaskNotifyWait( 0u, /* Don't clear any notification bits on entry. */  
                     0u, /* Don't clear any notification bits on exit. */  
                     &ulNotification,  
                     TICKS_UNTIL_TIMEOUT );  

    /* If there wasn't a timeout, then the only possible event was received.  
       In this example, that is the MESSAGE_RECEIVED_EVENT. */  
    if( ulNotification == 0u )   
    {  
        /* Handle the response timeout. */  
        process_response_timeout();  
    }   
    else if( ulNotification == ulMessageReceivedMask )  
    {  
        /* Process the response event. */  
        process_response();  

        ulTaskNotifyValueClear( ulMessageReceivedMask );  
    }   
    else   
    {  
        /* The example task should only ever receive MESSAGE\_RECEIVED\_EVENTS. */  
        process_error();  
    }  
```
