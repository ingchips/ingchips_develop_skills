# uxTaskPriorityGetFromISR()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]


task.h

```c
UBaseType_t uxTaskPriorityGetFromISR( const TaskHandle_t xTask );
```

`INCLUDE_uxTaskPriorityGet` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation 
for more information.

Obtain the priority of any task. This function is safe to use from within an interrupt service routine (ISR).


**Parameters:**

+ `xTask`   

  Handle of the task to be queried. Passing a NULL handle results in the priority of the calling task being returned.


**Returns:**

+ The priority of `xTask`. 

