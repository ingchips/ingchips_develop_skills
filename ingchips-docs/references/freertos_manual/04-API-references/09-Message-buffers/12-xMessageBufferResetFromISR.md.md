# xMessageBufferResetFromISR()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
BaseType_t xMessageBufferResetFromISR( MessageBufferHandle_t xMessageBuffer );
```

An interrupt safe version of the xMessageBufferReset() API function.

Resets a message buffer to its initial, empty state. Any data that was in the message buffer is discarded. 
A message buffer can only be reset if there are no tasks blocked waiting to either send to or receive from 
the message buffer.

Use xMessageBufferReset() to reset a message buffer from a task. Use xMessageBufferResetFromISR() to reset 
a message buffer from an interrupt service routine (ISR).

Message buffer functionality is enabled by including the FreeRTOS/source/stream_buffer.c source file in 
the build (as message buffers use stream buffers).


**Parameters:**

+ *xMessageBuffer*

  The handle of the message buffer to reset.


**Returns:**

If the message buffer is reset then pdPASS is returned. If there was a task blocked waiting to send to 
or read from the message buffer then the message buffer will not be reset and pdFAIL is returned.

