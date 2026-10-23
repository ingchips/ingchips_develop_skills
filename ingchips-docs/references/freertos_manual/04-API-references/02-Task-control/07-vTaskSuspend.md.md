# vTaskSuspend()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h 

```c
void vTaskSuspend( TaskHandle_t xTaskToSuspend );
```

`INCLUDE_vTaskSuspend` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Suspend any task. When suspended a task will never get any microcontroller processing time, no matter what its priority.

Calls to `vTaskSuspend` are not accumulative - i.e. calling `vTaskSuspend()` twice on the same task 
still only requires one call to `vTaskResume()` to ready the suspended task.


**Parameters:**

- *xTaskToSuspend*

  Handle to the task being suspended. Passing a NULL handle will cause the calling task to be suspended.


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

    // Suspend ourselves.
    vTaskSuspend( NULL );
 
    // We cannot get here unless another task calls vTaskResume
    // with our handle as the parameter.
}
```
