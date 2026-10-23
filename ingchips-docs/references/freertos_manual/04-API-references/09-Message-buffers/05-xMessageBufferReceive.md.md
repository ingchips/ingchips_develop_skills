# xMessageBufferReceive()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
size_t xMessageBufferReceive( MessageBufferHandle_t xMessageBuffer,
                              void *pvRxData,
                              size_t xBufferLengthBytes,
                              TickType_t xTicksToWait );
```

Receives a discrete message from an RTOS [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example). Messages can be of
variable length and are copied out of the buffer.

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

Use xMessageBufferReceive() to read from a message buffer from a task.
Use [xMessageBufferReceiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/06-xMessageBufferReceiveFromISR) to read from a message buffer from an
interrupt service routine (ISR).

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:**

- *xMessageBuffer*

  The handle of the message buffer from which a message is being received.

- *pvRxData*

  A pointer to the buffer into which the received message is to be copied.

- *xBufferLengthBytes*

  The length of the buffer pointed to by the pvRxData parameter. This sets the maximum length
  of the message that can be received. If xBufferLengthBytes is too small to hold the next
  message then the message will be left in the message buffer and 0 will be returned.

- *xTicksToWait*

  The maximum amount of time the task should remain in the Blocked state to wait for a message,
  should the message buffer be empty when xMessageBufferReceive() was called. xMessageBufferReceive()
  will return immediately if xTicksToWait is zero and the message buffer is empty. The block time
  is specified in tick periods, so the absolute time it represents is dependent on the tick
  frequency. The macro pdMS\_TO\_TICKS() can be used to convert a time specified in milliseconds
  into a time specified in ticks. Setting xTicksToWait to portMAX\_DELAY will cause the task to
  wait indefinitely (without timing out), provided INCLUDE\_vTaskSuspend is set to 1 in
  FreeRTOSConfig.h. Tasks do not use any CPU time when they are in the Blocked state.


**Returns:**

The length, in bytes, of the message read from the message buffer, if
any. If xMessageBufferReceive() times out before a message became available
then zero is returned. If the length of the message is greater than
xBufferLengthBytes then the message will be left in the message buffer and
zero is returned.


**Example usage:**

```c
void vAFunction( MessageBuffer_t xMessageBuffer )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
const TickType_t xBlockTime = pdMS_TO_TICKS( 20 );

    /* Receive the next message from the message buffer. Wait in the Blocked
       state (so not using any CPU processing time) for a maximum of 100ms for
       a message to become available. */
    xReceivedBytes = xMessageBufferReceive( xMessageBuffer,
                                            ( void * ) ucRxData,
                                            sizeof( ucRxData ),
                                            xBlockTime );

    if( xReceivedBytes > 0 )
    {
        /* A ucRxData contains a message that is xReceivedBytes long. Process
           the message here.... */
    }
}
```
