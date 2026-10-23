# xMessageBufferIsFull()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
BaseType_t xMessageBufferIsFull( MessageBufferHandle_t xMessageBuffer );
```

Queries a [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) to see if it is full.
A message buffer is full if it cannot accept any more messages, of any size,
until space is made available by a message being removed from the message buffer.

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build (as message buffers use stream buffers).


**Parameters:** 

- *xMessageBuffer*

  The handle of the message buffer being queried.


**Returns:** 

If the message buffer is full then pdTRUE is returned. Otherwise pdFALSE is returned.
 
