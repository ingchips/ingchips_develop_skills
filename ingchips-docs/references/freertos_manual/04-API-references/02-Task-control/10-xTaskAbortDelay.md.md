# xTaskAbortDelay()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h

```c
BaseType_t xTaskAbortDelay( TaskHandle_t xTask );
```

Forces a task to leave the [Blocked state](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states), and
enter the Ready state, even if the event the task was in the Blocked state to wait
for has not occurred, and any specified timeout has not expired.

INCLUDE\_xTaskAbortDelay must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.


**Parameters:** 

+ *xTask* 

  The handle of the task that will be forced out of the Blocked state. 

  To obtain a task's handle create the task using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and make use of the pxCreatedTask 
  parameter, or create the task using [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) and store the returned value, 
  or use the task's name in a call to [xTaskGetHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities).


**Returns:** 

If the task referenced by xTask was not in the Blocked state then pdFAIL is returned. Otherwise pdPASS is returned.
 
