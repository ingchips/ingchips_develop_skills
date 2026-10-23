# xTaskNotifyGive, xTaskNotifyGiveIndexed

[[RTOS Task Notification API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h

```c
 BaseType_t xTaskNotifyGive( TaskHandle_t xTaskToNotify );

 BaseType_t xTaskNotifyGiveIndexed( TaskHandle_t xTaskToNotify, 
                                    UBaseType_t uxIndexToNotify );
```

Each task has an array of 'task notifications' (or just 'notifications'), each
of which has a state and a 32-bit value. A [direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) is an event sent
directly to a task that can unblock the receiving task, and
optionally update one of the receiving task’s notification values in a number of different ways. 
For example, a notification may overwrite one of the receiving task's notification values, or just set one or 
more bits in one of the receiving task's notification values.

xTaskNotifyGive() is a macro intended for use when a task notification is 
being [used as a light weight and faster binary or counting semaphore](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications) 
alternative. FreeRTOS semaphores are given using the xSemaphoreGive() API function, xTaskNotifyGive()
is the equivalent that uses one of the receiving RTOS task’s notification values in place of a semaphore.

xTaskNotifyGive() and xTaskNotifyGiveIndexed() are equivalent macros - the only difference being 
xTaskNotifyGiveIndexed() can operate on any task notification within the array and xTaskNotifyGive() 
always operates on the task notification at array index 0.

When a task notification value is being used as a binary or counting semaphore equivalent then the task 
being notified should wait for the notification using the [ulTaskNotifyTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) API
function rather than the [xTaskNotifyWait()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) API function.

**Note:** Each notification within the array operates independently – a task can only block on one notification 
within the array at a time and will not be unblocked by a notification sent to any other array index.

xTaskNotifyGive() must not be called from an interrupt service routine. 
Use [vTaskNotifyGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) instead.

[configUSE\_TASK\_NOTIFICATIONS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must set to 1 in FreeRTOSConfig.h (or 
be left undefined) for these macros to be available. The 
constant [configTASK\_NOTIFICATION\_ARRAY\_ENTRIES](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) sets 
the number of indexes in each task's array of task notifications.


**Backward compatibility information:**  

Prior to FreeRTOS V10.4.0 each task had a single "notification value", and
all task notification API functions operated on that value. Replacing the
single notification value with an array of notification values necessitated a
new set of API functions that could address specific notifications within the
array. xTaskNotifyGive() is the original API function, and remains backward
compatible by always operating on the notification value at index 0 in the
array. Calling xTaskNotifyGive() is equivalent to calling
xTaskNotifyGiveIndexed() with the uxIndexToNotify parameter set to 0.


**Parameters:** 

* *xTaskToNotify*

  The handle of the RTOS task being notified, and having its notification value incremented. To obtain a task's
  handle create the task using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and make use of the pxCreatedTask parameter, or create
  the task using [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) and store the returned value, or use the task's
  name in a call to [xTaskGetHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities). The handle of the currently executing RTOS
  task is returned by the [xTaskGetCurrentTaskHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function.

* *uxIndexToNotify*

  The index within the target task's array of notification values to which the notification is to be sent.
  uxIndexToNotify must be less than configTASK\_NOTIFICATION\_ARRAY\_ENTRIES. xTaskNotifyGive() does not
  have this parameter and always sends notifications to index 0.


**Returns:** 

xTaskNotifyGiveIndexed() is a macro that calls [xTaskNotifyIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) with the
eAction parameter set to eIncrement, so all calls returning pdPASS.
 

**Example usage:**

[More examples are referenced from the main [RTOS task notifications page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* Prototypes of the two tasks created by main(). */  
static void prvTask1( void *pvParameters );  
static void prvTask2( void *pvParameters );  

 
/* Handles for the tasks create by main(). */  
static TaskHandle_t xTask1 = NULL, xTask2 = NULL;  

/* Create two tasks that send notifications back and forth to each other,   
   then start the RTOS scheduler. */  
void main( void )  
{  
    xTaskCreate( prvTask1, "Task1", 200, NULL, tskIDLE_PRIORITY, &xTask1 );  
    xTaskCreate( prvTask2, "Task2", 200, NULL, tskIDLE_PRIORITY, &xTask2 );  
    vTaskStartScheduler();  
}  

/*-----------------------------------------------------------*/  

/* prvTask1() uses the 'indexed' version of the API. */  
static void prvTask1( void *pvParameters )  
{  
    for( ;; )  
    {  
        /* Send notification to prvTask2(), bringing it out of the   
           Blocked state. */  
        xTaskNotifyGiveIndexed( xTask2, 0 );  

        /* Block to wait for prvTask2() to notify this task. */  
        ulTaskNotifyTakeIndexed( 0, pdTRUE, portMAX_DELAY );  
    }  
}  

/*-----------------------------------------------------------*/  

/* prvTask2() uses the original version of the API (without the   
   'Indexed'). */  
static void prvTask2( void *pvParameters )  
{  
    for( ;; )  
    {  
        /* Block to wait for prvTask1() to notify this task. */  
        ulTaskNotifyTake( pdTRUE, portMAX_DELAY );  

        /* Send a notification to prvTask1(), bringing it out of the   
           Blocked state. */  
        xTaskNotifyGive( xTask1 );  
    }  
}  
```
