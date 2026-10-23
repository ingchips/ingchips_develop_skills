# xTaskResumeFromISR()

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h 

```c
BaseType_t xTaskResumeFromISR( TaskHandle_t xTaskToResume );
```

`INCLUDE_vTaskSuspend` and `INCLUDE_xTaskResumeFromISR` must be defined as 1 for this function to be 
available. See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

A function to resume a suspended task that can be called from within an ISR.

A task that has been suspended by one of more calls to `vTaskSuspend()` will be made available for running 
again by a single call to `xTaskResumeFromISR()`.

`xTaskResumeFromISR()` is generally considered a dangerous function because its
actions are not latched. For this reason it should definitely not be used to
synchronise a task with an interrupt if there is a chance that the interrupt
could arrive prior to the task being suspended, and therefore the interrupt being
lost. Use of a semaphore, or preferable
a direct to task notification, would avoid this eventuality.
A [worked example that uses a direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)
is provided.


**Parameters:**

- *xTaskToResume*

  Handle to the task being readied.


**Returns:**

- *pdTRUE* if resuming the task should result in a context switch,
- *pdFALSE* otherwise. This is used by the ISR to determine if a context switch may be required following the ISR.


**Example usage:** 

```c
TaskHandle_t xHandle;

void vAFunction( void )
{
    // Create a task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // ... Rest of code.
}

void vTaskCode( void *pvParameters )
{
    // The task being suspended and resumed.
    for( ;; )
    {
        // ... Perform some function here.

        // The task suspends itself.
        vTaskSuspend( NULL );

        // The task is now suspended, so will not reach here until the ISR resumes it.
    }
}

void vAnExampleISR( void )
{
    BaseType_t xYieldRequired;

    // Resume the suspended task.
    xYieldRequired = xTaskResumeFromISR( xHandle );

    // We should switch context so the ISR returns to a different task.
    // NOTE:  How this is done depends on the port you are using.  Check
    // the documentation and examples for your port.
    portYIELD_FROM_ISR( xYieldRequired );
}
```
