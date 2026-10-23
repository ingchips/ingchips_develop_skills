[[Queue Set API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

queue.h

```c
BaseType_t xQueueRemoveFromSet(
                               QueueSetMemberHandle_t xQueueOrSemaphore,
                               QueueSetHandle_t xQueueSet
                              );
```

configUSE\_QUEUE\_SETS must be set to 1 in FreeRTOSConfig.h for the xQueueRemoveFromSet() API function to be available.

Remove an RTOS queue or semaphore from a queue set.

An RTOS queue or semaphore can only be removed from a queue set if the queue or
semaphore is empty.


**Parameters:** 

- *xQueueOrSemaphore*

  The handle of the queue or semaphore being removed from the queue set (cast to an QueueSetMemberHandle\_t type).
  
- *xQueueSet*

  The handle of the queue set in which the queue or semaphore is included.


**Returns:** 

If the queue or semaphore was successfully removed from the queue set
then pdPASS is returned. If the queue was not in the queue set, or the
queue (or semaphore) was not empty, then pdFAIL is returned.
 

**Example usage:**

This example assumes xQueueSet is a queue set that has already been created,
and xQueue is a queue that has already been created and added to xQueueSet.

```c
    if( xQueueRemoveFromSet( xQueue, xQueueSet ) != pdPASS )
    {
        /* Either xQueue was not a member of the xQueueSet set, or xQueue is
           not empty and therefore cannot be removed from the set. */
    }
    else
    {
        /* The queue was successfully removed from the set. */
    }
```
