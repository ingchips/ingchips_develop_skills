# RTOS task notifications

Used As Light Weight Event Group

An [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups) is a set of binary flags (or bits),
to each of which the application writer can assign a meaning. An RTOS task can
enter the Blocked state to wait for one or more flags within the group to become active. The RTOS
task does not consume any CPU time while it is in the Blocked state.

When a task notification is used in place of an event group the receiving
task's [notification value](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) is used in place of the event group, bits within
the receiving task's notification value are used as event flags, and the [xTaskNotifyWait()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait)
API function is used in place of the event group's xEventGroupWaitBits() API function.

Likewise, bits are set using the [xTaskNotify()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) and [xTaskNotifyFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/07-xTaskNotifyFromISR)
API functions (with their eAction parameter set to eSetBits) in place of the xEventGroupSetBits() and
xEventGroupSetBitsFromISR() functions respectively.

xTaskNotifyFromISR() has **significant performance benefits** when compared to xEventGroupSetBitsFromISR()
because xTaskNotifyFromISR() executes entirely in the ISR, whereas xEventGroupSetBitsFromISR() must defer
some processing to the RTOS daemon task.

Unlike when using an event group the receiving task cannot specify that it only wants to leave the Blocked
state when a combination of bits are active at the same time. Instead the task is unblocked when any bit
becomes active, and must test for bit combinations itself.

See the example below:

```c
/* This example demonstrates a single RTOS task being used to process
   events that originate from two separate interrupt service routines -
   a transmit interrupt and a receive interrupt. Many peripherals will
   use the same handler for both, in which case the peripheral's
   interrupt status register can simply be bitwise ORed with the
   receiving task's notification value.

   First, bits are defined to represent each interrupt source. */
#define TX_BIT    0x01
#define RX_BIT    0x02

/* The handle of the task that will receive notifications from the
   interrupts. The handle was obtained when the task was created. */
static TaskHandle_t xHandlingTask;

/*-----------------------------------------------------------*/

/* The implementation of the transmit interrupt service routine. */
void vTxISR( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

   /* Clear the interrupt source. */
   prvClearInterrupt();

   /* Notify the task that the transmission is complete by setting the TX_BIT
      in the task's notification value. */
   xTaskNotifyFromISR( xHandlingTask,
                       TX_BIT,
                       eSetBits,
                       &xHigherPriorityTaskWoken );

   /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context switch
      should be performed to ensure the interrupt returns directly to the highest
      priority task. The macro used for this purpose is dependent on the port in
      use and may be called portEND_SWITCHING_ISR(). */
   portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* The implementation of the receive interrupt service routine is identical
   except for the bit that gets set in the receiving task's notification value. */
void vRxISR( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

   /* Clear the interrupt source. */
   prvClearInterrupt();

   /* Notify the task that the reception is complete by setting the RX\_BIT
      in the task's notification value. */
   xTaskNotifyFromISR( xHandlingTask,
                       RX_BIT,
                       eSetBits,
                       &xHigherPriorityTaskWoken );

   /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context switch
      should be performed to ensure the interrupt returns directly to the highest
      priority task. The macro used for this purpose is dependent on the port in
      use and may be called portEND_SWITCHING_ISR(). */
   portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* The implementation of the task that is notified by the interrupt service
   routines. */
static void prvHandlingTask( void *pvParameter )
{
const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 500 );
BaseType_t xResult;

   for( ;; )
   {
      /* Wait to be notified of an interrupt. */
      xResult = xTaskNotifyWait( pdFALSE,          /* Don't clear bits on entry. */
                                 ULONG_MAX,        /* Clear all bits on exit. */
                                 &ulNotifiedValue, /* Stores the notified value. */
                                 xMaxBlockTime );

      if( xResult == pdPASS )
      {
         /* A notification was received. See which bits were set. */
         if( ( ulNotifiedValue & TX_BIT ) != 0 )
         {
            /* The TX ISR has set a bit. */
            prvProcessTx();
         }

         if( ( ulNotifiedValue & RX_BIT ) != 0 )
         {
            /* The RX ISR has set a bit. */
            prvProcessRx();
         }
      }
      else
      {
         /* Did not receive a notification within the expected time. */
         prvCheckForErrors();
      }
   }
}
```
