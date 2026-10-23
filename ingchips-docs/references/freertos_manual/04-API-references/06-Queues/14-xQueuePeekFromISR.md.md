[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h 

```c
BaseType_t xQueuePeekFromISR(
                              QueueHandle_t xQueue,
                              void *pvBuffer,
                             );
```

A version of [xQueuePeek()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/13-xQueuePeek) that can be used from an
interrupt service routine (ISR).

Receive an item from a queue without removing the item from the queue.
The item is received by copy so a buffer of adequate size must be
provided. The number of bytes copied into the buffer was defined when
the queue was created.

Successfully received items remain on the queue so will be returned again
by the next call, or a call to any queue receive function.


**Parameters:** 


+ *xQueue*  

  The handle to the queue from which the item is to be received.

+ *pvBuffer*  

  Pointer to the buffer into which the received item will be copied. This must be at least large enough 
  to hold the size of the queue item defined when the queue was created.


**Returns:** 

+ pdPASS if an item was successfully received (peeked) from the queue,
+ otherwise pdFAIL.
 
