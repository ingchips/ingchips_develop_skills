# FreeRTOS recursive mutexes

[See also [Blocking on Multiple RTOS Objects](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]


The [FreeRTOS tutorial book](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book) provides additional information on queues, binary
semaphores, mutexes, counting semaphores and recursive semaphores, along with simple worked examples in a
set of accompanying example projects.

### FreeRTOS Recursive Mutexes

A mutex used recursively can be 'taken' repeatedly by the owner. The mutex doesn't become available again until the owner has called
xSemaphoreGiveRecursive() for each successful xSemaphoreTakeRecursive() request. For example, if a task successfully 'takes' the same
mutex 5 times then the mutex will not be available to any other task until it has also 'given' the mutex back exactly five times.

This type of semaphore uses a priority inheritance mechanism so a task 'taking' a semaphore MUST ALWAYS 'give' the semaphore back once
the semaphore it is no longer required.

Mutex type semaphores cannot be used from within interrupt service routines.

Mutexes should not be used from an interrupt because:

- They include a priority inheritance mechanism which only makes sense if
  the mutex is given and taken from a task, not an interrupt.
- An interrupt cannot block to wait for a resource that is guarded by a
  mutex to become available.
