[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h 

```c
void vTaskSetApplicationTaskTag(
                                 TaskHandle_t xTask,
                                 TaskHookFunction_t pxTagValue );
```

`configUSE_APPLICATION_TASK_TAG` must be defined as 1 for this function to be available.
See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

A 'tag' value can be assigned to each task. This value is for the use of the application only - the 
RTOS kernel itself does not make use of it in any way. The [RTOS trace macros](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature) 
documentation page provides a good example of how an application might make use of this feature.


**Parameters:**

- *xTask*

  The handle of the task to which a tag value is being assigned. Passing `xTask` as NULL causes the tag 
  to be assigned to the calling task.
  
- *pxTagValue*

  The value being assigned to the task tag. This is of type `TaskHookFunction_t` to permit a function 
  pointer to be assigned as the tag, although any value can actually be assigned. See the example below.


**Example usage:** 

```c
/* In this example an integer is set as the task tag value. 
   See the RTOS trace hook macros documentation page for an 
   example how such an assignment can be used. */
void vATask( void *pvParameters )
{
    /* Assign a tag value of 1 to myself. */
    vTaskSetApplicationTaskTag( NULL, ( void * ) 1 );

    for( ;; )
    {
        /* Rest of task code goes here. */
    }
}
/***********************************************/

/* In this example a callback function is being assigned as the task tag.
   First define the callback function - this must have type TaskHookFunction_t
   as per this example. */
static BaseType_t prvExampleTaskHook( void * pvParameter )
{
    /* Perform some action - this could be anything from logging a value,
       updating the task state, outputting a value, etc. */
    return 0;
}

/* Now define the task that sets prvExampleTaskHook as its hook/tag value.
   This is in fact registering the task callback, as described on the
   xTaskCallApplicationTaskHook() documentation page. */
void vAnotherTask( void *pvParameters )
{
    /* Register our callback function. */
    vTaskSetApplicationTaskTag( NULL, prvExampleTaskHook );

    for( ;; )
    {
        /* Rest of task code goes here. */
    }
}

/* As an example use of the hook (callback) we can get the RTOS kernel to call the
   hook function of each task that is being switched out during a reschedule. */
#define traceTASK_SWITCHED_OUT() xTaskCallApplicationTaskHook( pxCurrentTCB, 0 )
```
