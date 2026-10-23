# xMessageBufferSpacesAvailable()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
size_t xMessageBufferSpacesAvailable( MessageBufferHandle_t xMessageBuffer );
```

Queries a [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) to see how much free
space it contains, which is equal to the amount of data that can be sent to the
message buffer before it is full. The returned value is 4 bytes larger than the
maximum message size that can be sent to the message buffer.

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:** 

- *xMessageBuffer*

  The handle of the message buffer being queried.


**Returns:** 

 The number of bytes that can be written to the message buffer before
 the message buffer would be full. When a message is
 written to the message buffer an additional sizeof( size\_t ) bytes are also
 written to store the message's length. sizeof( size\_t ) is typically 4 bytes
 on a 32-bit architecture, so if xMessageBufferSpacesAvailable() returns 10,
 then the size of the largest message that can be written to the message
 buffer is 6 bytes.
 
