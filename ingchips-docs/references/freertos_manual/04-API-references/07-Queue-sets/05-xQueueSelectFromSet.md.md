[[Queue Set API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

queue.h

```c
QueueSetMemberHandle_t xQueueSelectFromSet(
                                           QueueSetHandle_t xQueueSet,
                                           const TickType_t xTicksToWait
                                          );
```

configUSE\_QUEUE\_SETS must be set to 1 in FreeRTOSConfig.h for the xQueueSelectFromSet() API function to be available.

xQueueSelectFromSet() selects from the members of a queue set a queue or
semaphore that either contains data (in the case of a queue) or is available
to take (in the case of a semaphore). xQueueSelectFromSet() effectively
allows a task to block (pend) on a read operation on all the queues and
semaphores in a queue set simultaneously.

Notes:

* There are simpler alternatives to using queue sets. See the
  [Blocking on Multiple Objects](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/10-Blocking-on-multiple-RTOS-objects) page for
  more information.

* Blocking on a queue set that contains a mutex will not cause the
  mutex holder to inherit the priority of the blocked task.

* A receive (in the case of a queue) or take (in the case of a
  semaphore) operation must not be performed on a member of a queue set unless
  a call to xQueueSelectFromSet() has first returned a handle to that set member.


**Parameters:** 

+ *xQueueSet* 

  The queue set on which the task will (potentially) block.

+ *xTicksToWait* 

  The maximum time, in ticks, that the calling task will remain in the Blocked state (with other tasks 
  executing) to wait for a member of the queue set to be ready for a successful queue read or semaphore 
  take operation.


**Returns:** 

xQueueSelectFromSet() will return the handle of a queue (cast to
a QueueSetMemberHandle\_t type) contained in the queue set that contains data,
or the handle of a semaphore (cast to a QueueSetMemberHandle\_t type) contained
in the queue set that is available, or NULL if no such queue or semaphore
exists before the specified block time expires.
 

**Example usage:**

See the example on the [xQueueCreateSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) documentation page.  
