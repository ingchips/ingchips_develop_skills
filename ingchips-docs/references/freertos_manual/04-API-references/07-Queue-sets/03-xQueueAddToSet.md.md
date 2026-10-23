[[Queue Set API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

queue.h

```c
BaseType_t xQueueAddToSet(
                          QueueSetMemberHandle_t xQueueOrSemaphore,
                          QueueSetHandle_t xQueueSet
                         );
```

configUSE\_QUEUE\_SETS must be set to 1 in FreeRTOSConfig.h for the xQueueAddToSet() API function to be available.

Adds an RTOS queue or semaphore to a queue set that was previously created by a
call to [xQueueCreateSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet).

A receive (in the case of a queue) or take (in the case of a
semaphore) operation must not be performed on a member of a queue set unless
a call to xQueueSelectFromSet() has first returned a handle to that set member.


**Parameters:** 

- *xQueueOrSemaphore*

  The handle of the queue or semaphore being added to the queue set (cast to an QueueSetMemberHandle\_t type).

- *xQueueSet*

  The handle of the queue set to which the queue or semaphore is being added.


**Returns:** 

If the queue or semaphore was successfully added to the queue set
then pdPASS is returned. If the queue could not be successfully added to the
queue set because it is already a member of a different queue set then pdFAIL
is returned.
 

**Example usage:**

See the example on the [xQueueCreateSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) documentation page.
  
