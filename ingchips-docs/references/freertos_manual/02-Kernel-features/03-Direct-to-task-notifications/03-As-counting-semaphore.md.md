# RTOS task notifications

Used As Light Weight Counting Semaphores

Unblocking an RTOS task with a direct notification is **45% faster** and **uses less RAM** than unblocking
a task with a semaphore. This page demonstrates how this is done.

A counting semaphore is a semaphore that can have a count value of zero up to a maximum value set when the
semaphore is created. A task can only 'take' the semaphore if it is available, and the semaphore is only
available if its count is greater than zero.

When a task notification is used in place of a counting semaphore the receiving
task's [notification value](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) is used in place of the counting semaphore's count value,
and the [ulTaskNotifyTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) (or ulTaskNotifyTakeIndexed()) API function is used in place
of the semaphore's xSemaphoreTake() API function. The ulTaskNotifyTake() function's xClearOnExit parameter is
set to pdFALSE so the count value is only decremented (rather than cleared) each time the notification
is taken - emulating a counting semaphore.

Likewise the [xTaskNotifyGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) (or xTaskNotifyGiveIndexed())
or [vTaskNotifyGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) (or vTaskNotifyGiveIndexedFromISR()) functions are
used in place of the semaphore's xSemaphoreGive() and xSemaphoreGiveFromISR() functions.

The first example below uses the receiving task's notification value as a counting
semaphore. The second example provides a more pragmatic and efficient implementation.

**Example 1:**

```c
/* An interrupt handler that does not process interrupts directly,
   but instead defers processing to a high priority RTOS task. The
   ISR uses RTOS task notifications to both unblock the RTOS task
   and increment the RTOS task's notification value. */
void vANInterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken;

    /* Clear the interrupt. */
    prvClearInterruptSource();

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE.
       If calling vTaskNotifyGiveFromISR() unblocks the handling
       task, and the priority of the handling task is higher than
       the priority of the currently running task, then
       xHigherPriorityTaskWoken will be automatically set to pdTRUE. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Unblock the handling task so the task can perform
       any processing necessitated by the interrupt. xHandlingTask
       is the task's handle, which was obtained when the task was
       created. vTaskNotifyGiveFromISR() also increments
       the receiving task's notification value. */
    vTaskNotifyGiveFromISR( xHandlingTask, &xHigherPriorityTaskWoken );

    /* Force a context switch if xHigherPriorityTaskWoken is now
       set to pdTRUE. The macro used to do this is dependent on
       the port and may be called portEND\_SWITCHING\_ISR. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* A task that blocks waiting to be notified that the peripheral
   needs servicing. */
void vHandlingTask( void *pvParameters )
{
BaseType_t xEvent;
const TickType_t xBlockTime = pdMS_TO_TICKS( 500 );
uint32_t ulNotifiedValue;

    for( ;; )
    {
        /* Block to wait for a notification. Here the RTOS
           task notification is being used as a counting semaphore.
           The task's notification value is incremented each time
           the ISR calls vTaskNotifyGiveFromISR(), and decremented
           each time the RTOS task calls ulTaskNotifyTake() - so in
           effect holds a count of the number of outstanding interrupts.
           The first parameter is set to pdFALSE, so the notification
           value is only decremented and not cleared to zero, and one
           deferred interrupt event is processed at a time. See
           example 2 below for a more pragmatic approach. */
        ulNotifiedValue = ulTaskNotifyTake( pdFALSE,
                                            xBlockTime );

        if( ulNotifiedValue > 0 )
        {
            /* Perform any processing necessitated by the interrupt. */
            xEvent = xQueryPeripheral();

            if( xEvent != NO_MORE_EVENTS )
            {
                vProcessPeripheralEvent( xEvent );
            }
        }
        else
        {
            /* Did not receive a notification within the expected
               time. */
            vCheckForErrorConditions();
        }
    }
}
```

**Example 2:**

This example shows a more pragmatic and efficient implementation for the
RTOS task. In this implementation the value returned from ulTaskNotifyTake() is
used to know how many outstanding ISR events must be processed, allowing the
RTOS task's notification count to be cleared back to zero each time ulTaskNotifyTake()
is called. The interrupt service routine (ISR) is assumed to be as demonstrated
in example 1 above.

```c
/* The index within the target task's array of task notifications
   to use. */
const UBaseType_t xArrayIndex = 0;

/* A task that blocks waiting to be notified that the peripheral
   needs servicing. */
void vHandlingTask( void *pvParameters )
{
BaseType_t xEvent;
const TickType_t xBlockTime = pdMS_TO_TICKS( 500 );
uint32_t ulNotifiedValue;

    for( ;; )
    {
        /* As before, block to wait for a notification form the ISR.
           This time however the first parameter is set to pdTRUE,
           clearing the task's notification value to 0, meaning each
           outstanding outstanding deferred interrupt event must be
           processed before ulTaskNotifyTake() is called again. */
        ulNotifiedValue = ulTaskNotifyTakeIndexed( xArrayIndex,
                                                   pdTRUE,
                                                   xBlockTime );

        if( ulNotifiedValue == 0 )
        {
            /* Did not receive a notification within the expected
               time. */
            vCheckForErrorConditions();
        }
        else
        {
            /* ulNotifiedValue holds a count of the number of
               outstanding interrupts. Process each in turn. */
            while( ulNotifiedValue > 0 )
            {
                xEvent = xQueryPeripheral();

                if( xEvent != NO_MORE_EVENTS )
                {
                    vProcessPeripheralEvent( xEvent );
                    ulNotifiedValue--;
                }
                else
                {
                    break;
                }
            }
        }
    }
}
```
