# xTaskNotifyFromISR, xTaskNotifyIndexedFromISR

[[RTOS Task Notification API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h


```c
 BaseType_t xTaskNotifyFromISR( TaskHandle_t xTaskToNotify,
                                uint32_t ulValue,
                                eNotifyAction eAction,
                                BaseType_t *pxHigherPriorityTaskWoken );

 BaseType_t xTaskNotifyIndexedFromISR( TaskHandle_t xTaskToNotify,
                                       UBaseType_t uxIndexToNotify,
                                       uint32_t ulValue,
                                       eNotifyAction eAction,
                                       BaseType_t *pxHigherPriorityTaskWoken );
```

Versions of xTaskNotify() and xTaskNotifyIndexed() that can be used from an interrupt service
routine (ISR). See the documentation page for the [xTaskNotify()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) API function
for a description of their operation and the necessary configuration parameters, as well as
backward compatibility information.


**Parameters:**

* *xTaskToNotify*

  The handle of the RTOS task being notified. This is the *target* task.  To obtain a task's
  handle create the task using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and make use of the pxCreatedTask parameter,
  or create the task using [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) and store the returned value,
  or use the task's name in a call to [xTaskGetHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities). The handle of the
  currently executing RTOS task is returned by
  the [xTaskGetCurrentTaskHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function.

* *uxIndexToNotify*

  The index within the target task's array of notification values to which the notification
  is to be sent. uxIndexToNotify must be less than configTASK\_NOTIFICATION\_ARRAY\_ENTRIES.
  xTaskNotifyFromISR() does not have this parameter and always sends notifications to index 0.

* *ulValue*

  Used to update the notification value of the target task. See the description of the eAction
  parameter below.

* *eAction*

  An enumerated type that can take one of the values documented below in order to perform the associated action.

* *pxHigherPriorityTaskWoken*

  *pxHigherPriorityTaskWoken must be initialised to 0. xTaskNotifyFromISR() will set
  *pxHigherPriorityTaskWoken to pdTRUE if sending the notification caused a task to unblock,
  and the unblocked task has a priority higher than the currently running task. If
  xTaskNotifyFromISR() sets this value to pdTRUE then a context switch should be requested
  before the interrupt is exited. See the example below. pxHigherPriorityTaskWoken is an
  optional parameter and can be set to NULL.


**eAction values and associated actions**

+ eNoAction

  The target task receives the event, but its notification value is not updated. In this case ulValue
  is not used.

+ eSetBits

  The notification value of the target task will be bitwise ORed with ulValue. For example, if ulValue
  is set to 0x01, then bit 0 will get set within the target task's notification value. Likewise if ulValue
  is 0x04 then bit 2 will get set in the target task's notification value. In this way the RTOS task
  notification mechanism can be used as a light weight alternative to an [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups).

+ eIncrement

  The notification value of the target task will be incremented by one, making the call to xTaskNotifyFromISR()
  equivalent to a call to [vTaskNotifyGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR). In this case ulValue is not used.

+ eSetValueWithOverwrite

  The notification value of the target task is unconditionally set to ulValue. In this way the RTOS task
  notification mechanism is being used as a light weight alternative to [xQueueOverwrite()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite).

+ eSetValueWithoutOverwrite

  If the target task does not already have a notification pending then its notification value will be
  set to ulValue.  If the target task already has a notification pending then its notification value
  is not updated as to do so would overwrite the previous value before it was used. In this case the
  call to xTaskNotify() fails.  In this way the RTOS task notification mechanism is being used as a light
  weight alternative to [xQueueSend()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend) on a queue of length 1.


**Returns:**

pdPASS is returned in all cases other than when eAction is set to
eSetValueWithoutOverwrite and the target task's notification value
cannot be updated because the target task already had a notification
pending.


**Example usage:**

[More examples are referenced from the main [RTOS task notifications page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

This example demonstrates how to use xTaskNotifyFromISR() with the eSetBits
action. See the [xTaskNotify()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) API documentation
page for examples showing how to use the eNoAction, eSetValueWithOverwrite and
eSetValueWithoutOverwrite actions.


```c
/* The interrupt handler does not perform any processing itself. Instead it
   it unblocks a high priority task in which the events that generated the
   interrupt are processed. If the priority of the task is high enough then the
   interrupt will return directly to the task (so it will interrupt one task but
   return to a different task), so the processing will occur contiguously in time -
   just as if all the processing had been done in the interrupt handler itself.
   The status of the interrupting peripheral is sent to the task using an RTOS task
   notification. */
void vANInterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken;
uint32_t ulStatusRegister;

    /* Read the interrupt status register which has a bit for each interrupt
       source (for example, maybe an Rx bit, a Tx bit, a buffer overrun bit, etc. */
    ulStatusRegister = ulReadPeripheralInterruptStatus();

    /* Clear the interrupts. */
    vClearPeripheralInterruptStatus( ulStatusRegister );

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE. If calling
       xTaskNotifyFromISR() unblocks the handling task, and the priority of
       the handling task is higher than the priority of the currently running task,
       then xHigherPriorityTaskWoken will automatically get set to pdTRUE. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Unblock the handling task so the task can perform any processing necessitated
       by the interrupt. xHandlingTask is the task's handle, which was obtained
       when the task was created. The handling task's 0th notification value
       is bitwise ORed with the interrupt status - ensuring bits that are already
       set are not overwritten. */
    xTaskNotifyIndexedFromISR( xHandlingTask,
                               0,
                               ulStatusRegister,
                               eSetBits,
                               &xHigherPriorityTaskWoken );

    /* Force a context switch if xHigherPriorityTaskWoken is now set to pdTRUE.
       The macro used to do this is dependent on the port and may be called
       portEND_SWITCHING_ISR. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

/* ----------------------------------------------------------- */


/* A task that blocks waiting to be notified that the peripheral needs servicing,
   processing all the events pending in the peripheral each time it is notified to
   do so. */

void vHandlingTask( void *pvParameters )
{
uint32_t ulInterruptStatus;

    for( ;; )
    {
        /* Block indefinitely (without a timeout, so no need to check the function's
           return value) to wait for a notification. NOTE! Real applications
           should not block indefinitely, but instead time out occasionally in order
           to handle error conditions that may prevent the interrupt from sending
           any more notifications. */
        xTaskNotifyWaitIndexed( 0,                  /* Wait for 0th Notificaition */
                                0x00,               /* Don't clear any bits on entry. */
                                ULONG_MAX,          /* Clear all bits on exit. */
                                &ulInterruptStatus, /* Receives the notification value. */
                                portMAX_DELAY );    /* Block indefinitely. */

        /* Process any bits set in the received notification value. This assumes
           the peripheral sets bit 1 for an Rx interrupt, bit 2 for a Tx interrupt,
           and bit 3 for a buffer overrun interrupt. */
        if( ( ulInterruptStatus & 0x01 ) != 0x00 )
        {
            prvProcessRxInterrupt();
        }

        if( ( ulInterruptStatus & 0x02 ) != 0x00 )
        {
            prvProcessTxInterrupt();
        }

        if( ( ulInterruptStatus & 0x04 ) != 0x00 )
        {
            prvClearBufferOverrun();
        }
    }
}
```
