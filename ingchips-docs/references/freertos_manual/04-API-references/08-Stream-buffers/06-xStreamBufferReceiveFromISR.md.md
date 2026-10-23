# xStreamBufferReceiveFromISR()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]


stream\_buffer.h

```c
size_t xStreamBufferReceiveFromISR( StreamBufferHandle_t xStreamBuffer,
                                    void *pvRxData,
                                    size_t xBufferLengthBytes,
                                    BaseType_t *pxHigherPriorityTaskWoken );
```

An interrupt safe version of the API function that receives bytes from a
[stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example).

**NOTE**:  Uniquely among FreeRTOS objects, the stream buffer
implementation (so also the message buffer implementation, as message buffers
are built on top of stream buffers) assumes there is only one task or
interrupt that will write to the buffer (the writer), and only one task or
interrupt that will read from the buffer (the reader).  It is safe for the
writer and reader to be different tasks or interrupts, but, unlike other
FreeRTOS objects, it is not safe to have multiple different writers or
multiple different readers.  If there are to be multiple different writers
then the application writer must serialize calls to writing API functions
(such as xStreamBufferSend()).  Likewise, if there are to be multiple
different readers then the application writer must serialize calls to reading
API functions (such as xStreamBufferReceive()).  One way to achieve such
serialization in single core or SMP kernel is to place each API call inside a
critical section and use a block time of 0.

Use xStreamBufferReceive() to read from a stream buffer from a task. Use
xStreamBufferReceiveFromISR() to read from a stream buffer from an
interrupt service routine (ISR).

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build.


**Parameters:**

+ *xStreamBuffer*

  The handle of the stream buffer from which bytes are to be received.

+ *pvRxData*

  A pointer to the buffer into which the received bytes will be copied.

+ *xBufferLengthBytes*

  The length of the buffer pointed to by the pvRxData parameter. This sets the maximum number of bytes
  to receive in one call. xStreamBufferReceive will return as many bytes as possible up to a maximum
  set by xBufferLengthBytes.

+ *pxHigherPriorityTaskWoken*

  (This is an optional parameter that can be set to NULL.) It is possible that a stream buffer will have
  a task blocked on it waiting for space to become available. Calling xStreamBufferReceiveFromISR() can
  make space available, and so cause a task that is waiting for space to leave the Blocked state. If calling
  xStreamBufferReceiveFromISR() causes a task to leave the Blocked state, and the unblocked task has a
  priority higher than the currently executing task (the task that was interrupted), then, internally,
  xStreamBufferReceiveFromISR() will set \*pxHigherPriorityTaskWoken to pdTRUE.

  If xStreamBufferReceiveFromISR() sets this value to pdTRUE, then normally a context switch should be
  performed before the interrupt is exited. That will ensure the interrupt returns directly to the highest
  priority Ready state task. \*pxHigherPriorityTaskWoken should be set to pdFALSE before it is passed
  into the function. See the code example below for an example.


**Returns:**

The number of bytes read from the stream buffer, if any.


**Example usage:**

```c
/* A stream buffer that has already been created. */
StreamBuffer_t xStreamBuffer;

void vAnInterruptServiceRoutine( void )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;  /* Initialised to pdFALSE. */

    /* Receive the next stream from the stream buffer. */
    xReceivedBytes = xStreamBufferReceiveFromISR( xStreamBuffer,
                                                  ( void * ) ucRxData,
                                                  sizeof( ucRxData ),
                                                  &xHigherPriorityTaskWoken );

    if( xReceivedBytes > 0 )
    {
        /* ucRxData contains xReceivedBytes read from the stream buffer.
           Process the stream here.... */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xStreamBufferReceiveFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD\_FROM\_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
