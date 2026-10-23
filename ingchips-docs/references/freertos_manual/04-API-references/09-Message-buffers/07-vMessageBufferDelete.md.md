# vMessageBufferDelete()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
void vMessageBufferDelete( MessageBufferHandle_t xMessageBuffer );
```

Deletes a [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) that was previously created using a call 
to [xMessageBufferCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/01-xMessageBufferCreate) or [xMessageBufferCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/02-xMessageBufferCreateStatic).
If the message buffer was created using dynamic memory (that is, by `xMessageBufferCreate()`),
then the allocated memory is freed.

A message buffer handle must not be used after the message buffer has been deleted.

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:** 

- *xMessageBuffer*

  The handle of the message buffer to be deleted.
