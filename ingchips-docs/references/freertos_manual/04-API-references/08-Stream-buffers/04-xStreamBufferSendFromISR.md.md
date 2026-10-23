# xStreamBufferSendFromISR()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]


stream\_buffer.h

```c
size_t xStreamBufferSendFromISR( StreamBufferHandle_t xStreamBuffer,
                                 const void *pvTxData,
                                 size_t xDataLengthBytes,
                                 BaseType_t *pxHigherPriorityTaskWoken );
```

Interrupt safe version of the API function that sends a stream of bytes to
the [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example).

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

Use xStreamBufferSend() to write to a stream buffer from a task. Use
xStreamBufferSendFromISR() to write to a stream buffer from an interrupt
service routine (ISR).

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build.


**Parameters:**

+ *xStreamBuffer*

  The handle of the stream buffer to which a stream is being sent.

+ *pvTxData*

  A pointer to the buffer that holds the bytes to be copied into the stream buffer.

+ *xDataLengthBytes*

  The maximum number of bytes to copy from pvTxData into the stream buffer.

+ *pxHigherPriorityTaskWoken*

  (This is an optional parameter that can be set to NULL.) It is possible that a stream buffer will have
  a task blocked on it waiting for data. Calling xStreamBufferSendFromISR() can make data available, and
  so cause a task that was waiting for data to leave the Blocked state. If calling xStreamBufferSendFromISR()
  causes a task to leave the Blocked state, and the unblocked task has a priority higher than the currently
  executing task (the task that was interrupted), then, internally, xStreamBufferSendFromISR() will set
  \*pxHigherPriorityTaskWoken to pdTRUE. If xStreamBufferSendFromISR() sets this value to pdTRUE, then
  normally a context switch should be performed before the interrupt is exited. This will ensure that the
  interrupt returns directly to the highest priority Ready state task. \*pxHigherPriorityTaskWoken should
  be set to pdFALSE before it is passed into the function. See the example code below for an example.


**Returns:**

The number of bytes written to the stream buffer.


**Example usage:**

```c
/* A stream buffer that has already been created. */
StreamBufferHandle_t xStreamBuffer;

void vAnInterruptServiceRoutine( void )
{
size_t xBytesSent;
char *pcStringToSend = "String to send";
BaseType_t xHigherPriorityTaskWoken = pdFALSE; /* Initialised to pdFALSE. */

    /* Attempt to send the string to the stream buffer. */
    xBytesSent = xStreamBufferSendFromISR( xStreamBuffer,
                                           ( void * ) pcStringToSend,
                                           strlen( pcStringToSend ),
                                           &xHigherPriorityTaskWoken );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* There was not enough free space in the stream buffer for the entire
           string to be written, ut xBytesSent bytes were written. */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xStreamBufferSendFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD\_FROM\_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
