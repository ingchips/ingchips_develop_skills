# xStreamBufferReset()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
BaseType_t xStreamBufferReset( StreamBufferHandle_t xStreamBuffer );
```

Resets a [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) to its initial, empty, state. Any data that was in
the stream buffer is discarded. A stream buffer can only be reset if there
are no tasks blocked waiting to either send to or receive from the stream
buffer.

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build.


**Parameters:** 

+ *xStreamBuffer* 

  The handle of the stream buffer being reset.


**Returns:** 

If the stream buffer is reset then pdPASS is returned. If there was
a task blocked waiting to send to or read from the stream buffer then the
stream buffer will not be reset and pdFAIL is returned.
 
