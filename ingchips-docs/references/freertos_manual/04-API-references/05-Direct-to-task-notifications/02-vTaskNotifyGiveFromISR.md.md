# vTaskNotifyGiveFromISR, vTaskNotifyGiveIndexedFromISR

[[RTOS Task Notification API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]
 
task.h

```c
void vTaskNotifyGiveFromISR( TaskHandle_t xTaskToNotify,
                             BaseType_t *pxHigherPriorityTaskWoken );

void vTaskNotifyGiveIndexedFromISR( TaskHandle_t xTaskHandle, 
                                    UBaseType_t uxIndexToNotify, 
                                    BaseType_t *pxHigherPriorityTaskWoken );
```

Versions of `xTaskNotifyGive()` and `xTaskNotifyGiveIndexed()` that can be used from an interrupt
service routine (ISR). See the documentation page for the [xTaskNotifyGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) 
API function for a description of their operation and the necessary
configuration parameters, as well as backward compatibility information.


**Parameters:** 

- *xTaskToNotify*

  The handle of the RTOS task being notified, and having its notification value incremented. To obtain a 
  task's handle create the task using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and make use of the `pxCreatedTask` 
  parameter, or create the task using [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) and store the returned 
  value, or use the task's name in a call to [xTaskGetHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities). The handle of 
  the currently executing RTOS task is returned by 
  the [xTaskGetCurrentTaskHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function.
  
- *uxIndexToNotify*

  The index within the target task's array of notification values to which the notification is to be 
  sent. `uxIndexToNotify` must be less than `configTASK_NOTIFICATION_ARRAY_ENTRIES`. `xTaskNotifyGiveFromISR()` 
  does not have this parameter and always sends notifications to index 0.
  
- *pxHigherPriorityTaskWoken*

  `*pxHigherPriorityTaskWoken` must be initialised to 0. `vTaskNotifyGiveFromISR()` will 
  set `*pxHigherPriorityTaskWoken` to `pdTRUE` if sending the notification caused a task to unblock,
  and the unblocked task has a priority higher than the currently running task. If `vTaskNotifyGiveFromISR()` 
  sets this value to `pdTRUE` then a context switch should be requested before the interrupt is exited. 
  See the example below. `pxHigherPriorityTaskWoken` is an optional parameter and can be set to NULL.


**Example usage:**

[More examples are referenced from the main [RTOS task notifications page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* This is an example of a transmit function in a generic peripheral driver. An  
   RTOS task calls the transmit function, then waits in the Blocked state (so not  
   using an CPU time) until it is notified that the transmission is complete. The  
   transmission is performed by a DMA, and the DMA end interrupt is used to notify  
   the task. */  
static TaskHandle_t xTaskToNotify = NULL;  

/* The peripheral driver's transmit function. */  
void StartTransmission( uint8_t *pcData, size_t xDataLength )  
{  
    /* At this point xTaskToNotify should be NULL as no transmission is in  
       progress. A mutex can be used to guard access to the peripheral if  
       necessary. */  
    configASSERT( xTaskToNotify == NULL );  

    /* Store the handle of the calling task. */  
    xTaskToNotify = xTaskGetCurrentTaskHandle();  

    /* Start the transmission - an interrupt is generated when the transmission  
       is complete. */  
    vStartTransmit( pcData, xDatalength );  
}  

/*-----------------------------------------------------------*/  

/* The transmit end interrupt. */  
void vTransmitEndISR( void )  
{  
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;  

    /* At this point xTaskToNotify should not be NULL as a transmission was  
       in progress. */  
    configASSERT( xTaskToNotify != NULL );  

    /* Notify the task that the transmission is complete. */  
    vTaskNotifyGiveIndexedFromISR( xTaskToNotify, 0, &xHigherPriorityTaskWoken );  

    /* There are no transmissions in progress, so no tasks to notify. */  
    xTaskToNotify = NULL;  

    /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context switch  
       should be performed to ensure the interrupt returns directly to the highest  
       priority task. The macro used for this purpose is dependent on the port in  
       use and may be called portEND_SWITCHING_ISR(). */  
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  

/*-----------------------------------------------------------*/  

/* The task that initiates the transmission, then enters the Blocked state (so  
   not consuming any CPU time) to wait for it to complete. */  
void vAFunctionCalledFromATask( uint8_t ucDataToTransmit, size_t xDataLength )  
{  
    uint32_t ulNotificationValue;  
    const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 200 );  

    /* Start the transmission by calling the function shown above. */  
    StartTransmission( ucDataToTransmit, xDataLength );  

    /* Wait for the transmission to complete. */  
    ulNotificationValue = ulTaskNotifyTakeIndexed( 0, pdFALSE, xMaxBlockTime );  

    if( ulNotificationValue == 1 )  
    {  
        /* The transmission ended as expected. */  
    }  
    else  
    {  
        /* The call to ulTaskNotifyTake() timed out. */  
    }  
}  
```
