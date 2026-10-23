# uxTaskPriorityGet()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h 

```c
UBaseType_t uxTaskPriorityGet( const TaskHandle_t xTask );
```

`INCLUDE_uxTaskPriorityGet` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Obtain the priority of any task.


**Parameters:**

- *xTask*

  Handle of the task to be queried. Passing a NULL handle results in the priority of the calling task being returned.


**Returns:**

- The priority of `xTask`.


**Example usage:** 

```c
void vATaskFunction( void * pvParams )
{
    TaskHandle_t xHandle;

    ( void ) pvParams;

    // Create a task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // ...

    // Use the handle to obtain the priority of the created task.
    // It was created with tskIDLE_PRIORITY, but may have changed
    // it itself.
    if( uxTaskPriorityGet( xHandle ) != tskIDLE_PRIORITY )
    {
        // The task has changed its priority.
    }

    // ...

    // Is our priority higher than the created task?
    if( uxTaskPriorityGet( xHandle ) < uxTaskPriorityGet( NULL ) )
    {
        // Our priority (obtained using NULL handle) is higher.
    }
}
```
