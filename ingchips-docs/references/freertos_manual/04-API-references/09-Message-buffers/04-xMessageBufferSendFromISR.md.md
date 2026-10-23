# xMessageBufferSendFromISR()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
size_t xMessageBufferSendFromISR( MessageBufferHandle_t xMessageBuffer,
                                  const void *pvTxData,
                                  size_t xDataLengthBytes,
                                  BaseType_t *pxHigherPriorityTaskWoken );
```

Interrupt safe version of the API function that sends a discrete message to
the [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example). The message can be any length that fits within the
buffer's free space, and is copied into the buffer.

**NOTE**:  Uniquely among FreeRTOS objects, the stream buffer
implementation (so also the message buffer implementation, as message buffers
are built on top of stream buffers) assumes there is only one task or
interrupt that will write to the buffer (the writer), and only one task or
interrupt that will read from the buffer (the reader).  It is safe for the
writer and reader to be different tasks or interrupts, but, unlike other
FreeRTOS objects, it is not safe to have multiple different writers or
multiple different readers.  If there are to be multiple different writers
then the application writer must serialize calls to writing API functions
(such as xMessageBufferSend()).  Likewise, if there are to be multiple
different readers then the application writer must serialize calls to reading
API functions (such as xMessageBufferReceive()).  One way to achieve such
serialization in single core or SMP kernel is to place each API call inside a
critical section and use a block time of 0.

Use [xMessageBufferSend()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/03-xMessageBufferSend) to write to a message buffer from a task. Use
xMessageBufferSendFromISR() to write to a message buffer from an interrupt
service routine (ISR).

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:**

- *xMessageBuffer*

  The handle of the message buffer to which a message is being sent.

- *pvTxData*

  A pointer to the message that is to be copied into the message buffer.

- *xDataLengthBytes*

  The length of the message. That is, the number of bytes to copy from pvTxData into the message buffer.
  When a message is written to the message buffer an additional sizeof( size\_t ) bytes are also written
  to store the message's length. sizeof( size\_t ) is typically 4 bytes on a 32-bit architecture, so on
  most 32-bit architecture setting xDataLengthBytes to 20 will reduce the free space in the message buffer
  by 24 bytes (20 bytes of message data and 4 bytes to hold the message length).

- *pxHigherPriorityTaskWoken*

  (This is an optional parameter that can be set to NULL.) It is possible that a message buffer will
  have a task blocked on it waiting for data. Calling xMessageBufferSendFromISR() can make data
  available, and so cause a task that was waiting for data to leave the Blocked state. If calling
  xMessageBufferSendFromISR() causes a task to leave the Blocked state, and the unblocked task has
  a priority higher than the currently executing task (the task that was interrupted), then,
  internally, xMessageBufferSendFromISR() will set *pxHigherPriorityTaskWoken to pdTRUE. If
  xMessageBufferSendFromISR() sets this value to pdTRUE, then normally a context switch should be
  performed before the interrupt is exited. This will ensure that the interrupt returns directly to
  the highest priority Ready state task. \*pxHigherPriorityTaskWoken should be set to pdFALSE before
  it is passed into the function. See the code example below for an example.


**Returns:**

The number of bytes actually written to the message buffer. If the
message buffer didn't have enough free space for the message to be stored
then 0 is returned, otherwise xDataLengthBytes is returned.


**Example usage:**

```c
/* A message buffer that has already been created. */
MessageBufferHandle_t xMessageBuffer;

void vAnInterruptServiceRoutine( void )
{
size_t xBytesSent;
char *pcStringToSend = "String to send";
BaseType_t xHigherPriorityTaskWoken = pdFALSE; /* Initialised to pdFALSE. */

    /* Attempt to send the string to the message buffer. */
    xBytesSent = xMessageBufferSendFromISR( xMessageBuffer,
                                            ( void * ) pcStringToSend,
                                            strlen( pcStringToSend ),
                                            &xHigherPriorityTaskWoken );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* The string could not be added to the message buffer because there was
           not enough free space in the buffer. */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xMessageBufferSendFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD\_FROM\_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
