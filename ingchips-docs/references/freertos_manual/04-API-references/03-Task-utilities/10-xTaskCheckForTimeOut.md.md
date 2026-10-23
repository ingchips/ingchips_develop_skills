# xTaskCheckForTimeOut()

[[Task Utilities](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h

```c
BaseType_t xTaskCheckForTimeOut( TimeOut_t * const pxTimeOut,
                                 TickType_t * const pxTicksToWait );
```

This function is intended for advanced users only.

A task can enter the Blocked state to wait for an event. Typically, the task
will not wait in the Blocked state indefinitely, but instead a timeout period
will be specified. The task will be removed from the Blocked state if the
timeout period expires before the event the task is waiting for occurs.

If a task enters and exits the Blocked state more than once while it is waiting
for the event to occur then the timeout used each time the task enters the
Blocked state must be adjusted to ensure the total of all the time spent in the
Blocked state does not exceed the originally specified timeout period.
xTaskCheckForTimeOut() performs the adjustment, taking into account occasional
occurrences such as tick count overflows, which would otherwise make a manual
adjustment prone to error.

xTaskCheckForTimeOut() is used with vTaskSetTimeOutState().
vTaskSetTimeOutState() is called to set the initial condition, after which
xTaskCheckForTimeOut() can be called to check for a timeout condition, and
adjust the remaining block time if a timeout has not occurred.


**Parameters:** 

+ *pxTimeOut* 

   A pointer to a structure that holds information necessary to determine if a timeout has occurred. 
   pxTimeOut is initialized using vTaskSetTimeOutState().

+ *pxTicksToWait* 

  Used to pass out an adjusted block time, which is the block time that remains after taking into account 
  the time already spent in the Blocked state.


**Returns:** 

If pdTRUE is returned then no block time remains, and a timeout has occurred.

If pdFALSE is returned then some block time remains, so a timeout has not occurred.
 

**Example usage:**

```c
/* Driver library function used to receive uxWantedBytes from an Rx buffer that
   is filled by a UART interrupt. If there are not enough bytes in the Rx buffer
   then the task enters the Blocked state until it is notified that more data has
   been placed into the buffer. If there is still not enough data then the task
   re-enters the Blocked state, and xTaskCheckForTimeOut() is used to re-calculate
   the Block time to ensure the total amount of time spent in the Blocked state does
   not exceed MAX_TIME_TO_WAIT. This continues until either the buffer contains at
   least uxWantedBytes bytes, or the total amount of time spent in the Blocked state
   reaches MAX_TIME_TO_WAIT – at which point the task reads however many bytes are
   available up to a maximum of uxWantedBytes. */
size_t xUART_Receive( uint8_t *pucBuffer, size_t uxWantedBytes )
{
size_t uxReceived = 0;
TickType_t xTicksToWait = MAX_TIME_TO_WAIT;
TimeOut_t xTimeOut;

   /* Initialize xTimeOut. This records the time at which this function was
      entered. */
   vTaskSetTimeOutState( &xTimeOut );

   /* Loop until the buffer contains the wanted number of bytes, or a timeout
      occurs. */
   while( UART_bytes_in_rx_buffer( pxUARTInstance ) < uxWantedBytes )
   {
      /* The buffer didn't contain enough data so this task is going to
         enter the Blocked state. Adjusting xTicksToWait to account for any time
         that has been spent in the Blocked state within this function so far to
         ensure the total amount of time spent in the Blocked state does not exceed
         MAX_TIME_TO_WAIT. */
      if( xTaskCheckForTimeOut( &xTimeOut, &xTicksToWait ) != pdFALSE )
      {
         /* Timed out before the wanted number of bytes were available, exit the
            loop. */
         break;
      }

      /* Wait for a maximum of xTicksToWait ticks to be notified that the receive
         interrupt has placed more data into the buffer. */
      ulTaskNotifyTake( pdTRUE, xTicksToWait );
   }

   /* Attempt to read uxWantedBytes from the receive buffer into pucBuffer. The
      actual number of bytes read (which might be less than uxWantedBytes) is
      returned. */
   uxReceived = UART_read_from_receive_buffer( pxUARTInstance,
                                               pucBuffer,
                                               uxWantedBytes );

   return uxReceived;
}
```
