task.h 

```c
void vTaskDelete( TaskHandle_t xTask );
```

`INCLUDE_vTaskDelete` must be defined as 1 for this function to be available. See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
documentation for more information.

Remove a task from the RTOS kernels management. The task being deleted will be removed from all ready, 
blocked, suspended and event lists.

NOTE: If a task deletes another task, the RTOS kernel allocated memory is freed in the API itself. If a task 
deletes itself, the idle task is responsible for freeing the RTOS kernel allocated memory. It is therefore 
important that the idle task is not starved of microcontroller processing time if your application makes any 
calls to `vTaskDelete()`. Memory allocated by the task code is not automatically freed, and should be freed 
before the task is deleted.

See the demo application file death.c for sample code that utilises `vTaskDelete()`.


**Parameters:**

- *xTask*

  The handle of the task to be deleted. Passing NULL will cause the calling task to be deleted.


**Example usage:** 

```c
void vOtherFunction( void )
{
    TaskHandle_t xHandle = NULL;

    // Create the task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // Use the handle to delete the task.
    if( xHandle != NULL )
    {
        vTaskDelete( xHandle );
    }
}
```
