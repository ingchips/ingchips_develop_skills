# xStreamBufferSend()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]


stream\_buffer.h

```c
size_t xStreamBufferSend( StreamBufferHandle_t xStreamBuffer,
                          const void *pvTxData,
                          size_t xDataLengthBytes,
                          TickType_t xTicksToWait );
```

Sends bytes to a [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example).
The bytes are copied into the stream buffer.

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

+ *xTicksToWait*

  The maximum amount of time the task should remain in the Blocked state to wait for enough space to
  become available in the stream buffer, should the stream buffer contain too little space to hold the
  another xDataLengthBytes bytes. The block time is specified in tick periods, so the absolute time it
  represents is dependent on the tick frequency. The macro pdMS\_TO\_TICKS() can be used to convert a
  time specified in milliseconds into a time specified in ticks. Setting xTicksToWait to portMAX\_DELAY
  will cause the task to wait indefinitely (without timing out), provided INCLUDE\_vTaskSuspend is set
  to 1 in FreeRTOSConfig.h. If a task times out before it can write all xDataLengthBytes into the buffer
  it will still write as many bytes as possible. A task does not use any CPU time when it is in the
  blocked state.


**Returns:**

The number of bytes written to the stream buffer. If a task times
out before it can write all xDataLengthBytes into the buffer it will still
write as many bytes as possible.


**Example usage:**

```c
void vAFunction( StreamBufferHandle_t xStreamBuffer )
{
size_t xBytesSent;
uint8_t ucArrayToSend[] = { 0, 1, 2, 3 };
char *pcStringToSend = "String to send";
const TickType_t x100ms = pdMS_TO_TICKS( 100 );

    /* Send an array to the stream buffer, blocking for a maximum of 100ms to
       wait for enough space to be available in the stream buffer. */
    xBytesSent = xStreamBufferSend( xStreamBuffer,
                                   ( void * ) ucArrayToSend,
                                   sizeof( ucArrayToSend ),
                                   x100ms );

    if( xBytesSent != sizeof( ucArrayToSend ) )
    {
        /* The call to xStreamBufferSend() times out before there was enough
           space in the buffer for the data to be written, but it did
           successfully write xBytesSent bytes. */
    }

    /* Send the string to the stream buffer. Return immediately if there is not
       enough space in the buffer. */
    xBytesSent = xStreamBufferSend( xStreamBuffer,
                                    ( void * ) pcStringToSend,
                                    strlen( pcStringToSend ), 0 );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* The entire string could not be added to the stream buffer because
           there was not enough free space in the buffer, but xBytesSent bytes
           were sent. Could try again to send the remaining bytes. */
    }
}
```
