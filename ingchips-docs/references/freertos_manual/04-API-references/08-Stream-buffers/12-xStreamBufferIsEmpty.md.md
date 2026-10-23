# xStreamBufferIsEmpty()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]


stream\_buffer.h

```c
BaseType_t xStreamBufferIsEmpty( StreamBufferHandle_t xStreamBuffer );
```

Queries a [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) to see if it is empty.
A stream buffer is empty if it does not contain any data.

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build.


**Parameters:** 

+ *xStreamBuffer* 

  The handle of the stream buffer being queried.


**Returns:** 

If the stream buffer is empty then pdTRUE is returned. Otherwise
pdFALSE is returned.
 
