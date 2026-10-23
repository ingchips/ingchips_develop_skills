# vTaskPrioritySet()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h 

```c
void vTaskPrioritySet( TaskHandle_t xTask,
                       UBaseType_t uxNewPriority );
```

`INCLUDE_vTaskPrioritySet` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Set the priority of any task.

A context switch will occur before the function returns if the priority being set is higher than the currently executing task.


**Parameters:**

- *xTask*

  Handle of the task whose priority is being set. A NULL handle sets the priority of the calling task.

- *uxNewPriority*

  The priority to which the task will be set. Priorities are asserted to be less than `configMAX_PRIORITIES`. 
  If `configASSERT` is undefined, priorities are silently capped at (`configMAX_PRIORITIES` - 1).


**Example usage:**

```c
void vAFunction( void )  
{  
    TaskHandle_t xHandle;  

    // Create a task, storing the handle.  
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );  

    // ...  

    // Use the handle to raise the priority of the created task.  
    vTaskPrioritySet( xHandle, tskIDLE_PRIORITY + 1 )  

    // ...  

    // Use a NULL handle to raise our priority to the same value.  
    vTaskPrioritySet( NULL, tskIDLE_PRIORITY + 1 );  
 }  
```
