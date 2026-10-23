# uxTaskGetStackHighWaterMark, uxTaskGetStackHighWaterMark2

[[Task Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task.h

```c
UBaseType_t uxTaskGetStackHighWaterMark
 ( TaskHandle_t xTask );

configSTACK_DEPTH_TYPE uxTaskGetStackHighWaterMark2
 ( TaskHandle_t xTask );
```

`INCLUDE_uxTaskGetStackHighWaterMark` must be defined as 1 for the `uxTaskGetStackHighWaterMark` function 
to be available and `INCLUDE_uxTaskGetStackHighWaterMark2` must be defined as 1 for the `uxTaskGetStackHighWaterMark2` 
function to be available. See the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

`uxTaskGetStackHighWaterMark2()` is a version of `uxTaskGetStackHighWaterMark()` that
returns a user definable type to remove the data type width restriction of `UBaseType_t` types on 8-bit architectures.

The stack used by a task will grow and shrink as the task executes and interrupts are processed. `uxTaskGetStackHighWaterMark()` 
returns the minimum amount of remaining stack space that was available to the task since the task started executing - 
that is the amount of stack that remained unused when the task stack was at its greatest (deepest) value. This is 
what is referred to as the stack 'high water mark'.


**Parameters:**

- *xTask*

  The handle of the task being queried. A task may query its own high water mark by passing NULL as the xTask parameter. 


**Returns:**

The value returned is the high water mark in words (for example, on a 32 bit machine a return value 
of 1 would indicate that 4 bytes of stack were unused). If the return value is zero then the task has 
likely overflowed its stack. If the return value is close to zero then the task has come close to overflowing 
its stack.


**Example usage:** 

```c
    void vTask1( void * pvParameters )
    {
        UBaseType_t uxHighWaterMark;

        /* Inspect our own high water mark on entering the task. */
        uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );

        for( ;; )
        {
            /* Call any function. */
            vTaskDelay( 1000 );

            /* Calling the function will have used some stack space, we would 
               therefore now expect uxTaskGetStackHighWaterMark() to return a 
               value lower than when it was called on entering the task. */
            uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );
        }
    }
```
   
