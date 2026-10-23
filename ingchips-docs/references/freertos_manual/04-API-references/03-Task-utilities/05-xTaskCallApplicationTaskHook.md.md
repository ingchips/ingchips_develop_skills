[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]


task.h 

```c
BaseType_t xTaskCallApplicationTaskHook(
                                         TaskHandle_t xTask,
                                         void *pvParameter );
```

configUSE\_APPLICATION\_TASK\_TAG must be defined as 1 for this function to be available.
See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

A 'tag' value can be assigned to each task. Normally this value is for the use of the application only 
and the RTOS kernel does not access it. However, it is possible to use the tag to assign a hook (or callback) 
function to a task - the hook function being executed by calling xTaskCallApplicationTaskHook(). Each 
task can define its own callback, or simply not define a callback at all.

Although it is possible to use the first function parameter to call the hook function of any task, the most 
common use of task hook function is with the trace hook macros, as per the example given below.

Task hook functions must have type TaskHookFunction\_t, that is take a void * parameter, and return a 
value of type BaseType\_t. The void * parameter can be used to pass any information into the hook function.


**Parameters:**

+ *xTask* 

  The handle of the task whose hook function is being called. Passing NULL as xTask will call the hook 
  function associated with the currently executing task.

+ *pvParameter* 

  The value to pass to the hook function. This can be a pointer to a structure, or simply a numeric value.


**Example usage:** 

```c
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

/* As an example use of the hook (callback) we can get the RTOS kernel to
   call the hook function of each task that is being switched out during a
   reschedule. */
#define traceTASK_SWITCHED_OUT() xTaskCallApplicationTaskHook( pxCurrentTCB, 0 )
```
