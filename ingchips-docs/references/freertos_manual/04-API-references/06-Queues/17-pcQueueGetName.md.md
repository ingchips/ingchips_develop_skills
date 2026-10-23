[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h

```c
const char *pcQueueGetName( QueueHandle_t xQueue )
```

Look up a queue name from the queue's handle.

A queue will only have a name if it has been added to the [queue registry](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/15-vQueueAddToRegistry).


**Parameters:** 

+ *xQueue*  

  The handle of the queue being queried.


**Returns:** 

If the queue referenced by xQueue is in the queue registry, then the
text name of the queue is returned, otherwise NULL is returned.
 
