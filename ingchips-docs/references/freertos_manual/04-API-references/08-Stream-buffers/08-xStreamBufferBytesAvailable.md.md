# xStreamBufferBytesAvailable()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
size_t xStreamBufferBytesAvailable( StreamBufferHandle_t xStreamBuffer );
```

Queries a [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) to see how much data
it contains, which is equal to the number of bytes that can be read from the
stream buffer before the stream buffer would be empty.

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build.


**Parameters:** 

+ *xStreamBuffer* 

  The handle of the stream buffer being queried.


**Returns:** 

The number of bytes that can be read from the stream buffer before
the stream buffer would be empty.
 
