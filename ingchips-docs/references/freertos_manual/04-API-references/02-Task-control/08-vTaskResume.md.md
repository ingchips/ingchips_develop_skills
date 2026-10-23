# vTaskResume()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h 

```c
void vTaskResume( TaskHandle_t xTaskToResume );
```

`INCLUDE_vTaskSuspend` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Resumes a suspended task.

A task that has been suspended by one or more calls to `vTaskSuspend(`) will be made available for running 
again by a single call to `vTaskResume()`.


**Parameters:**


- *xTaskToResume*

  Handle to the task being readied.


**Example usage:** 

```c
void vAFunction( void )
{
    TaskHandle_t xHandle;

    // Create a task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // ...

    // Use the handle to suspend the created task.
    vTaskSuspend( xHandle );

    // ...

    // The created task will not run during this period, unless
    // another task calls vTaskResume( xHandle ).

    //...

    // Resume the suspended task ourselves.
    vTaskResume( xHandle );

    // The created task will once again get microcontroller processing
    // time in accordance with its priority within the system.
}
```
