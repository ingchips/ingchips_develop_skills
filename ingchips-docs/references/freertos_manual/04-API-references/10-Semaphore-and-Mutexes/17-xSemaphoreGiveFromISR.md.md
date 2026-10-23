# xSemaphoreGiveFromISR

[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**TIP: In many usage scenarios it is faster and more memory efficient to use a direct to task notification instead of a semaphore**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)


semphr.h 

```c
xSemaphoreGiveFromISR
 (
 SemaphoreHandle_t xSemaphore,
 signed BaseType_t *pxHigherPriorityTaskWoken
 )
```

*Macro* to release a semaphore. The semaphore must have previously been
created with a call to xSemaphoreCreateBinary() or xSemaphoreCreateCounting().

Mutex type semaphores (those created using a call to xSemaphoreCreateMutex())
must not be used with this macro.

This macro can be used from an ISR.


**Parameters:**

+ *xSemaphore* 

  A handle to the semaphore being released. This is the handle returned when the semaphore was created.

+ *pxHigherPriorityTaskWoken* 

  xSemaphoreGiveFromISR() will set *pxHigherPriorityTaskWoken to pdTRUE if giving the semaphore caused a 
  task to unblock, and the unblocked task has a priority higher than the currently running task. 
  If xSemaphoreGiveFromISR() sets this value to pdTRUE then a context switch should be requested before 
  the interrupt is exited. From FreeRTOS V7.3.0 pxHigherPriorityTaskWoken is an optional parameter and 
  can be set to NULL.


**Returns:**

pdTRUE if the semaphore was successfully given, otherwise errQUEUE\_FULL.


**Example usage:**

Note the functionality shown below can often be achieved in a more efficient way by
using a [direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
in place of a semaphore.

```c
#define LONG_TIME 0xffff
#define TICKS_TO_WAIT 10

SemaphoreHandle_t xSemaphore = NULL;

/* Repetitive task. */
void vATask( void * pvParameters )
{
    /* We are using the semaphore for synchronisation so we create a binary
       semaphore rather than a mutex. We must make sure that the interrupt
       does not attempt to use the semaphore before it is created! */
    xSemaphore = xSemaphoreCreateBinary();

    for( ;; )
    {
        /* We want this task to run every 10 ticks of a timer. The semaphore
           was created before this task was started.

           Block waiting for the semaphore to become available. */
        if( xSemaphoreTake( xSemaphore, LONG\_TIME ) == pdTRUE )
        {
            /* It is time to execute. */

             ...

            /* We have finished our task. Return to the top of the loop where
               we will block on the semaphore until it is time to execute
               again. Note when using the semaphore for synchronisation with an
               ISR in this manner there is no need to 'give' the semaphore
               back. */
        }
    }
}

/* Timer ISR */
void vTimerISR( void * pvParameters )
{
static unsigned char ucLocalTickCount = 0;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* A timer tick has occurred. */

    ... Do other time functions.

    /* Is it time for vATask() to run? */
    xHigherPriorityTaskWoken = pdFALSE;
    ucLocalTickCount++;
    if( ucLocalTickCount >= TICKS_TO_WAIT )
    {
        /* Unblock the task by releasing the semaphore. */
        xSemaphoreGiveFromISR( xSemaphore, &xHigherPriorityTaskWoken );

        /* Reset the count so we release the semaphore again in 10 ticks
           time. */
        ucLocalTickCount = 0;
    }

    /* Yield if xHigherPriorityTaskWoken is true. The 
       actual macro used here is port specific. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
