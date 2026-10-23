# FreeRTOS scheduling (single-core, AMP and SMP)

[[More about tasks...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines)]

### Implementing a Task

A task should have the following structure:

```c
void vATaskFunction( void *pvParameters )
{
    for( ;; )
    {
        -- Task application code here. --
    }

    /* Tasks must not attempt to return from their implementing
       function or otherwise exit. In newer FreeRTOS port
       attempting to do so will result in an configASSERT() being
       called if it is defined. If it is necessary for a task to
       exit then have the task call vTaskDelete( NULL ) to ensure
       its exit is clean. */
    vTaskDelete( NULL );
}
```

The type TaskFunction_t is defined as a function that returns void and takes a void pointer as its
only parameter. All functions that implement a task should be of this type. The parameter can be used
to pass information of any type into the task - this is demonstrated by several of
the [standard demo application tasks](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview).

Task functions should never return so are typically implemented as a continuous loop. However, as
noted [on the page that describes the RTOS scheduling algorithm](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling),
normally it is best to create tasks that are event-driven so as not to starve lower priority tasks of
processing time, making the structure:

```c
void vATaskFunction( void *pvParameters )
{
    for( ;; )
    {
        /* Psudeo code showing a task waiting for an event
           with a block time. If the event occurs, process it.
           If the timeout expires before the event occurs, then
           the system may be in an error state, so handle the
           error. Here the pseudo code "WaitForEvent()" could
           replaced with xQueueReceive(), ulTaskNotifyTake(),
           xEventGroupWaitBits(), or any of the other FreeRTOS
           communication and synchronisation primitives. */
        if( WaitForEvent( EventObject, TimeOut ) == pdPASS )
        {
            -- Handle event here. --
        }
        else
        {
            -- Clear errors, or take actions here. --
        }
    }

    /* As per the first code listing above. */
    vTaskDelete( NULL );
}
```

Again, see the RTOS demo application for numerous examples.

Tasks are created by calling [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 
or [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic), and deleted by 
calling [vTaskDelete()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete).


---

### Task Creation Macros

Task functions can _optionally_ be defined using the portTASK_FUNCTION and portTASK\_FUNCTION\_PROTO
macros. These macro are provided to allow compiler specific syntax to be added to the function definition
and prototype respectively. Their use is not required unless specifically stated in documentation for the
port being used (currently only the PIC18 fedC port).

The prototype for the function shown above can be written as:

```c
void vATaskFunction( void *pvParameters );
```

Or,

```c
portTASK_FUNCTION_PROTO( vATaskFunction, pvParameters );
```

Likewise the function above could equally be written as:

```c
portTASK_FUNCTION( vATaskFunction, pvParameters )
{
    for( ;; )
    {
        -- Task application code here. --
    }
}
```
