# uxTaskBasePriorityGetFromISR()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h

```c
UBaseType_t uxTaskBasePriorityGetFromISR( const TaskHandle_t xTask );
```

`INCLUDE_uxTaskPriorityGet` and `configUSE_MUTEXES` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation 
for more information.

Obtain the base priority of any task. The base priority of a task is the priority to which the task 
will return if the task's current priority has been inherited to avoid unbounded priority inversion 
when obtaining a mutex. This function is safe to use from within an interrupt service routine (ISR).


**Parameters:**

+ `xTask`

  Handle of the task to be queried. Passing a NULL handle results in the base priority of the calling task being returned.


**Returns:**

+ The base priority of `xTask`.

