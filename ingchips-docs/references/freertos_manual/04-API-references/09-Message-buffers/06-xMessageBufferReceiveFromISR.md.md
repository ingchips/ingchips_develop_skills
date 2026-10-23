# xMessageBufferReceiveFromISR()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
size_t xMessageBufferReceiveFromISR( MessageBufferHandle_t xMessageBuffer,
                                     void *pvRxData,
                                     size_t xBufferLengthBytes,
                                     BaseType_t *pxHigherPriorityTaskWoken );
```

An interrupt safe version of the API function that receives a discrete
message from a [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example). Messages can be of variable length and are
copied out of the buffer.

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

Use [xMessageBufferReceive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/05-xMessageBufferReceive) to read from a message buffer from a task. Use
xMessageBufferReceiveFromISR() to read from a message buffer from an
interrupt service routine (ISR).

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:**

- *xMessageBuffer*

  The handle of the message buffer from which a message is being received.

- *pvRxData*

  A pointer to the buffer into which the received message will be copied.

- *xBufferLengthBytes*

  The length of the buffer pointed to by the pvRxData parameter. This sets the maximum length of the
  message that can be received. If xBufferLengthBytes is too small to hold the next message then the
  message will be left in the message buffer and 0 will be returned.

- *pxHigherPriorityTaskWoken*

  (This is an optional parameter that can be set to NULL.) It is possible that a message buffer will
  have a task blocked on it waiting for space to become available. Calling xMessageBufferReceiveFromISR()
  can make space available, and so cause a task that is waiting for space to leave the Blocked state.
  If calling xMessageBufferReceiveFromISR() causes a task to leave the Blocked state, and the unblocked
  task has a priority higher than the currently executing task (the task that was interrupted), then,
  internally, xMessageBufferReceiveFromISR() will set *pxHigherPriorityTaskWoken to pdTRUE. If
  xMessageBufferReceiveFromISR() sets this value to pdTRUE, then normally a context switch should be
  performed before the interrupt is exited. That will ensure the interrupt returns directly to the
  highest priority Ready state task. *pxHigherPriorityTaskWoken should be set to pdFALSE before it is
  passed into the function. See the code example below for an example.


**Returns:**

The length, in bytes, of the message read from the message buffer, if any.


**Example usage:**

```c
/* A message buffer that has already been created. */
MessageBuffer_t xMessageBuffer;

void vAnInterruptServiceRoutine( void )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;  /* Initialised to pdFALSE. */

    /* Receive the next message from the message buffer. */
    xReceivedBytes = xMessageBufferReceiveFromISR( xMessageBuffer,
                                                  ( void * ) ucRxData,
                                                  sizeof( ucRxData ),
                                                  &xHigherPriorityTaskWoken );

    if( xReceivedBytes > 0 )
    {
        /* A ucRxData contains a message that is xReceivedBytes long. Process
           the message here.... */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xMessageBufferReceiveFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD\_FROM\_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
