[[Co-Routine Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
BaseType_t crQUEUE_SEND_FROM_ISR( QueueHandle_t xQueue,
                                  void *pvItemToQueue,
                                  BaseType_t xCoRoutinePreviouslyWoken )
```

`crQUEUE_SEND_FROM_ISR()` is a macro. The data types are shown in the prototype above for reference only.

The macros `crQUEUE_SEND_FROM_ISR()` and `crQUEUE_RECEIVE_FROM_ISR()` are the
co-routine equivalent to the `xQueueSendFromISR()` and `xQueueReceiveFromISR()`
functions used by tasks.

`crQUEUE_SEND_FROM_ISR()` and `crQUEUE_RECEIVE_FROM_ISR()` can only be used to
pass data between a co-routine and an ISR, whereas `xQueueSendFromISR()`
and `xQueueReceiveFromISR()` can only be used to pass data between a task and an
ISR.

`crQUEUE_SEND_FROM_ISR` can only be called from an ISR to send data to a queue
that is being used from within a co-routine.

See the co-routine section of the web documentation for information on
passing data between tasks and co-routines and between ISR's and
co-routines.


**Parameters:**

- *xQueue*

  The handle to the queue on which the item is to be posted.

- *pvItemToQueue*

  A pointer to the item that is to be placed on the queue. The size of the items the queue will hold
  was defined when the queue was created, so this many bytes will be copied from `pvItemToQueue` into
  the queue storage area.

- *xCoRoutinePreviouslyWoken*

  This is included so an ISR can post onto the same queue multiple times from a single interrupt. The
  first call should always pass in `pdFALSE`. Subsequent calls should pass in the value returned from
  the previous call.


**Returns:**

- *pdTRUE* if a co-routine was woken by posting onto the queue. This is used by the ISR to determine
  if a context switch may be required following the ISR.


**Example usage:**

```c
// A co-routine that blocks on a queue waiting for characters to be received.
static void vReceivingCoRoutine( CoRoutineHandle_t xHandle,
                                 UBaseType_t uxIndex )
{
    char cRxedChar;
    BaseType_t xResult;

    // All co-routines must start with a call to crSTART().
    crSTART( xHandle );

    for( ;; )
    {
        // Wait for data to become available on the queue.  This assumes the
        // queue xCommsRxQueue has already been created!
        crQUEUE_RECEIVE( xHandle,
                         xCommsRxQueue,
                         &uxLEDToFlash,
                         portMAX_DELAY,
                         &xResult );

        // Was a character received?
        if( xResult == pdPASS )
        {
            // Process the character here.
        }
    }

    // All co-routines must end with a call to crEND().
    crEND();
}

// An ISR that uses a queue to send characters received on a serial port to
// a co-routine.
void vUART_ISR( void )
{
    char cRxedChar;
    BaseType_t xCRWokenByPost = pdFALSE;

    // We loop around reading characters until there are none left in the UART.
    while( UART_RX_REG_NOT_EMPTY() )
    {
        // Obtain the character from the UART.
        cRxedChar = UART_RX_REG;

        // Post the character onto a queue.  xCRWokenByPost will be pdFALSE
        // the first time around the loop.  If the post causes a co-routine
        // to be woken (unblocked) then xCRWokenByPost will be set to pdTRUE.
        // In this manner we can ensure that if more than one co-routine is
        // blocked on the queue only one is woken by this ISR no matter how
        // many characters are posted to the queue.
        xCRWokenByPost = crQUEUE_SEND_FROM_ISR( xCommsRxQueue,
                                                 &cRxedChar,
                                                 xCRWokenByPost );
    }
}
```
