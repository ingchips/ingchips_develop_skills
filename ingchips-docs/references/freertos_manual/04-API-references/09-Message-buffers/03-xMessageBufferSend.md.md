# xMessageBufferSend()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
size_t xMessageBufferSend( MessageBufferHandle_t xMessageBuffer,
                           const void *pvTxData,
                           size_t xDataLengthBytes,
                           TickType_t xTicksToWait );
```

Sends a discrete message to a [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example). The message can be any
length that fits within the buffer's free space, and is copied into the buffer.

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

Use xMessageBufferSend() to write to a message buffer from a task.
Use [xMessageBufferSendFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/04-xMessageBufferSendFromISR) to write to a message buffer from an interrupt
service routine (ISR).

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:**

- *xMessageBuffer*

  The handle of the message buffer to which a message is being sent.

- *pvTxData*

  A pointer to the message that is to be copied into the message buffer.

- *xDataLengthBytes*

  The length of the message. That is, the number of bytes to copy from pvTxData into the message buffer. When a
  message is written to the message buffer an additional sizeof( size\_t ) bytes are also written to store the
  message's length. sizeof( size\_t ) is typically 4 bytes on a 32-bit architecture, so on most 32-bit
  architecture setting xDataLengthBytes to 20 will reduce the free space in the message buffer by 24 bytes
  (20 bytes of message data and 4 bytes to hold the message length).

- *xTicksToWait*

  xTicksToWait The maximum amount of time the calling task should remain in the Blocked state to wait for enough
  space to become available in the message buffer, should the message buffer have insufficient space when
  xMessageBufferSend() is called. The calling task will never block if xTicksToWait is zero. The block time is
  specified in tick periods, so the absolute time it represents is dependent on the tick frequency. The macro
  pdMS\_TO\_TICKS() can be used to convert a time specified in milliseconds into a time specified in ticks.
  Setting xTicksToWait to portMAX\_DELAY will cause the task to wait indefinitely (without timing out), provided
  INCLUDE\_vTaskSuspend is set to 1 in FreeRTOSConfig.h. Tasks do not use any CPU time when they are in the
  Blocked state.


**Returns:**

The number of bytes written to the message buffer. If the call to
xMessageBufferSend() times out before there was enough space to write the
message into the message buffer then zero is returned. If the call did not
time out then xDataLengthBytes is returned.


**Example usage:**

```c
void vAFunction( MessageBufferHandle_t xMessageBuffer )
{
size_t xBytesSent;
uint8_t ucArrayToSend[] = { 0, 1, 2, 3 };
char *pcStringToSend = "String to send";
const TickType_t x100ms = pdMS_TO_TICKS( 100 );

    /* Send an array to the message buffer, blocking for a maximum of 100ms to
       wait for enough space to be available in the message buffer. */
    xBytesSent = xMessageBufferSend( xMessageBuffer,
                                     ( void * ) ucArrayToSend,
                                     sizeof( ucArrayToSend ),
                                     x100ms );

    if( xBytesSent != sizeof( ucArrayToSend ) )
    {
        /* The call to xMessageBufferSend() times out before there was enough
           space in the buffer for the data to be written. */
    }

    /* Send the string to the message buffer. Return immediately if there is
       not enough space in the buffer. */
    xBytesSent = xMessageBufferSend( xMessageBuffer,
                                    ( void * ) pcStringToSend,
                                    strlen( pcStringToSend ), 0 );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* The string could not be added to the message buffer because there was
           not enough free space in the buffer. */
    }
}
```
