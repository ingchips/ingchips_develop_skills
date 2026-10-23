# vStreamBufferDelete()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream_buffer.h

```c
void vStreamBufferDelete( StreamBufferHandle_t xStreamBuffer );
```

Deletes a [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) that was previously created using a call 
to [xStreamBufferCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/01-xStreamBufferCreate) or [xStreamBufferCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/02-xStreamBufferCreateStatic).
If the stream buffer was created using dynamic memory (that is, by xStreamBufferCreate()),
then the allocated memory is freed.

A stream buffer handle must not be used after the stream buffer has been deleted.

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build.


**Parameters:** 

- *xStreamBuffer*

  The handle of the stream buffer to be deleted.
