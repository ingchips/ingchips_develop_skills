# xTaskGetApplicationTaskTag, xTaskGetApplicationTaskTagFromISR

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]


task.h 

```c
TaskHookFunction_t xTaskGetApplicationTaskTag( TaskHandle_t xTask );
TaskHookFunction_t xTaskGetApplicationTaskTagFromISR( TaskHandle_t xTask );
```

configUSE\_APPLICATION\_TASK\_TAG must be defined as 1 for these functions to be available.
See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

xTaskGetApplicationTaskTagFromISR() is a version of xTaskGetApplicationTaskTag() that
can be called from an interrupt service routine (ISR).

Returns the 'tag' value associated with a task. The meaning and use of the tag
value is defined by the application writer. The RTOS kernel itself will not normally
access the tag value.

This function is intended for advanced users only.

**Parameters:**

+ *xTask* 

  The handle of the task being queried. A task can query its own tag value by using NULL as the parameter value.


**Returns:** 

 The 'tag' value of the task being queried.
 

**Example usage:** 

```c
/* In this example, an integer is set as the task tag value. */
void vATask( void *pvParameters )
{
    /* Assign a tag value of 1 to the currently executing task.
       The (void *) cast is used to prevent compiler warnings. */
    vTaskSetApplicationTaskTag( NULL, ( void * ) 1 );

    for( ;; )
    {
        /* Rest of task code goes here. */
    }
}

void vAFunction( void )
{
TaskHandle_t xHandle;
int iReturnedTaskHandle;

    /* Create a task from the vATask() function, storing the handle to the
       created task in the xTask variable. */

    /* Create the task. */
    if( xTaskCreate(
                     vATask,        /* Pointer to the function that implements
                                       the task. */
                     "Demo task",   /* Text name given to the task. */
                     STACK_SIZE,    /* The size of the stack that should be created
                                       for the task. This is defined in words, not
                                        bytes. */
                     NULL,          /* The task does not use the parameter. */
                     TASK_PRIORITY, /* The priority to assign to the newly created
                                       task. */
                     &xHandle       /* The handle to the task being created will be
                                       placed in xHandle. */
                   ) == pdPASS )
    {
       /* The task was created successfully. Delay for a short period to allow
          the task to run. */
       vTaskDelay( 100 );

       /* What tag value is assigned to the task? The returned tag value is
          stored in an integer, so cast to an integer to prevent compiler
          warnings. */
       iReturnedTaskHandle = ( int ) xTaskGetApplicationTaskTag( xHandle );
    }
}
```
