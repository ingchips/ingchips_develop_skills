# xMessageBufferReset()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
BaseType_t xMessageBufferReset( MessageBufferHandle_t xMessageBuffer );
```

Resets a [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) 
to its initial, empty, state. Any data that was in the message buffer is discarded. A message buffer 
can only be reset if there are no tasks blocked waiting to either send to or receive from the message
buffer.

Use `xMessageBufferReset()` to reset a message buffer from a task. Use `xMessageBufferResetFromISR()` to 
reset a message buffer from an interrupt service routine (ISR). 

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:** 

- *xMessageBuffer*

  The handle of the message buffer being reset.


**Returns:** 

+ If the message buffer is reset then pdPASS is returned. 

+ If there was a task blocked waiting to send to or read from the message buffer then the message buffer 
  will not be reset and pdFAIL is returned.
  
