# RTOS Task Notifications

Used As Light Weight Binary Semaphores

Unblocking an RTOS task with a direct notification is **45% faster** and
**uses less RAM** than unblocking a task with a binary semaphore. This page
demonstrates how this is done.

A binary semaphore is a semaphore that has a maximum count of 1, hence the 'binary' name.
A task can only 'take' the semaphore if it is available, and the semaphore is only
available if its count is 1.

When a task notification is used in place of a binary semaphore the receiving
task's [notification value](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) is used in place of the binary semaphore's count
value, and the [ulTaskNotifyTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) (or ulTaskNotifyTakeIndexed()) API function is
used in place of the semaphore's xSemaphoreTake() API function. The ulTaskNotifyTake() function's
xClearOnExit parameter is set to pdTRUE so the count value is returned to zero each time the notification
is taken - emulating a binary semaphore.

Likewise the [xTaskNotifyGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) (or xTaskNotifyGiveIndexed())
or [vTaskNotifyGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) (or vTaskNotifyGiveIndexedFromISR()) functions are
used in place of the semaphore's xSemaphoreGive() and xSemaphoreGiveFromISR() functions.

See the example below.

```c
/* This is an example of a transmit function in a generic
   peripheral driver. An RTOS task calls the transmit function,
   then waits in the Blocked state (so not using an CPU time)
   until it is notified that the transmission is complete. The
   transmission is performed by a DMA, and the DMA end interrupt
   is used to notify the task. */

/* Stores the handle of the task that will be notified when the
   transmission is complete. */
static TaskHandle_t xTaskToNotify = NULL;

/* The index within the target task's array of task notifications
   to use. */
const UBaseType_t xArrayIndex = 1;

/* The peripheral driver's transmit function. */
void StartTransmission( uint8_t *pcData, size_t xDataLength )
{
    /* At this point xTaskToNotify should be NULL as no transmission
       is in progress. A mutex can be used to guard access to the
       peripheral if necessary. */
    configASSERT( xTaskToNotify == NULL );

    /* Store the handle of the calling task. */
    xTaskToNotify = xTaskGetCurrentTaskHandle();

    /* Start the transmission - an interrupt is generated when the
       transmission is complete. */
    vStartTransmit( pcData, xDatalength );
}
/*-----------------------------------------------------------*/

/* The transmit end interrupt. */
void vTransmitEndISR( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* At this point xTaskToNotify should not be NULL as
       a transmission was in progress. */
    configASSERT( xTaskToNotify != NULL );

    /* Notify the task that the transmission is complete. */
    vTaskNotifyGiveIndexedFromISR( xTaskToNotify,
                                   xArrayIndex,
                                   &xHigherPriorityTaskWoken );

    /* There are no transmissions in progress, so no tasks
       to notify. */
    xTaskToNotify = NULL;

    /* If xHigherPriorityTaskWoken is now set to pdTRUE then a
       context switch should be performed to ensure the interrupt
       returns directly to the highest priority task. The macro used
       for this purpose is dependent on the port in use and may be
       called portEND_SWITCHING_ISR(). */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* The task that initiates the transmission, then enters the
   Blocked state (so not consuming any CPU time) to wait for it
   to complete. */
void vAFunctionCalledFromATask( uint8_t ucDataToTransmit,
                                size_t xDataLength )
{
uint32_t ulNotificationValue;
const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 200 );

    /* Start the transmission by calling the function shown above. */
    StartTransmission( ucDataToTransmit, xDataLength );

    /* Wait to be notified that the transmission is complete. Note
       the first parameter is pdTRUE, which has the effect of clearing
       the task's notification value back to 0, making the notification
       value act like a binary (rather than a counting) semaphore. */
    ulNotificationValue = ulTaskNotifyTakeIndexed( xArrayIndex,
                                                   pdTRUE,
                                                   xMaxBlockTime );

    if( ulNotificationValue == 1 )
    {
        /* The transmission ended as expected. */
    }
    else
    {
        /* The call to ulTaskNotifyTake() timed out. */
    }
}
```
