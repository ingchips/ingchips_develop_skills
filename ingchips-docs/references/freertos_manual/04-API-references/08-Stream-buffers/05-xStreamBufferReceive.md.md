# xStreamBufferReceive()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
size_t xStreamBufferReceive( StreamBufferHandle_t xStreamBuffer,
                             void *pvRxData,
                             size_t xBufferLengthBytes,
                             TickType_t xTicksToWait );
```


Receives bytes from a [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example).

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

  The length of the buffer pointed to by the<br /> pvRxData parameter. This sets the maximum number of
  bytes to receive in one call. xStreamBufferReceive will return as many bytes as possible up to a maximum
  set by xBufferLengthBytes.

+ *xTicksToWait*

  The maximum amount of time the task should remain in the Blocked state to wait for data to become
  available if the stream buffer is empty. xStreamBufferReceive() will return immediately if xTicksToWait
  is zero. The block time is specified in tick periods, so the absolute time it represents is dependent
  on the tick frequency. The macro pdMS\_TO\_TICKS() can be used to convert a time specified in milliseconds
  into a time specified in ticks. Setting xTicksToWait to portMAX\_DELAY will cause the task to wait
  indefinitely (without timing out), provided INCLUDE\_vTaskSuspend is set to 1 in FreeRTOSConfig.h. A
  task does not use any CPU time when it is in the Blocked state.


**Returns:**

The number of bytes read from the stream buffer. This will be the number of bytes available up to a
maximum of xBufferLengthBytes. For example:

* If the trigger level is 1 (the trigger level is set [when the stream buffer is created](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/01-xStreamBufferCreate)) -

	+ If xBufferLengthBytes is 10 and the stream buffer contains 5 bytes when xStreamBufferReceive() is
      called - then xStreamBufferReceive() will not block, read 5 bytes from the buffer, and return 5.

	+ If xBufferLengthBytes is 10 and the stream buffer contains 50 bytes when xStreamBufferReceive() is
      called - then xStreamBufferReceive() will not block, read 10 bytes from the buffer, and return 10.

	+ If xBufferLengthBytes is 10, the stream buffer contains 0 bytes when xStreamBufferReceive() is called,
      xTicksToWait is 100, and 5 bytes are received into the buffer after 50 ticks - then xStreamBufferReceive()
      will enter the blocked state for 50 ticks (which is until data arrives in the buffer), after which
      it will read 5 bytes from the buffer, and return 5.

	+ If xBufferLengthBytes is 10, the stream buffer contains 0 bytes when xStreamBufferReceive() is called,
      xTicksToWait is 100, and no bytes are received into the buffer within 100 ticks - then xStreamBufferReceive()
      will enter the blocked state for the full block time of 100 ticks, after which it will return 0.

* If the trigger level is 6 -

	+ If xBufferLengthBytes is 10, the stream buffer contains 0 bytes when xStreamBufferReceive() is called,
      xTicksToWait is 100, and 10 bytes are received into the buffer after 50 ticks - then xStreamBufferReceive()
      will enter the blocked state for 50 ticks (which is until at least the trigger level number of bytes arrives
      in the buffer), after which it will read 10 bytes from the buffer, and return 10.

	+ If xBufferLengthBytes is 10, the stream buffer contains 0 bytes when xStreamBufferReceive() is called,
      xTicksToWait is 100, and 5 bytes are received into the buffer after 50 ticks - then xStreamBufferReceive()
      will remain blocked for the entire 100 tick block period (because the amount of data in the buffer never
      reached the trigger level), after which it will read 5 bytes from the buffer, and return 5.


**Example usage:**

```c
void vAFunction( StreamBuffer_t xStreamBuffer )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
const TickType_t xBlockTime = pdMS_TO_TICKS( 20 );

    /* Receive up to another sizeof( ucRxData ) bytes from the stream buffer.
       Wait in the Blocked state (so not using any CPU processing time) for a
       maximum of 100ms for the full sizeof( ucRxData ) number of bytes to be
       available. */
    xReceivedBytes = xStreamBufferReceive( xStreamBuffer,
                                           ( void * ) ucRxData,
                                           sizeof( ucRxData ),
                                           xBlockTime );

    if( xReceivedBytes > 0 )
    {
        /* A ucRxData contains another xRecievedBytes bytes of data, which can
           be processed here.... */
    }
}
```
