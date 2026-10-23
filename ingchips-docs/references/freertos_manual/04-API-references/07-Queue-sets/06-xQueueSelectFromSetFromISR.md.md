[[Queue Set API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

queue.h

```c
QueueSetMemberHandle_t xQueueSelectFromSetFromISR(
                                                  QueueSetHandle_t xQueueSet
                                                 );
```

configUSE\_QUEUE\_SETS must be set to 1 in FreeRTOSConfig.h for the xQueueSelectFromSetFromISR() API function to be available.

A version of [xQueueSelectFromSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/04-xQueueSelectFromSet) that
can be used from an interrupt service routine (ISR).


**Parameters:** 

+ *xQueueSet* 

  The queue set being queried. It is not possible to block on a read as this function is designed to be 
  used from an interrupt.


**Returns:** 

xQueueSelectFromSetFromISR() will return the handle of a queue (cast to
a QueueSetMemberHandle\_t type) contained in the queue set that contains data,
or the handle of a semaphore (cast to a QueueSetMemberHandle\_t type) contained
in the queue set that is available, or NULL if no such queue or semaphore
exists.
 
