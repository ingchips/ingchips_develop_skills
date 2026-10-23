# FreeRTOS mutexes

[See also [Blocking on Multiple RTOS Objects](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

The [FreeRTOS tutorial book](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
provides additional information on queues, binary semaphores, mutexes, counting
semaphores and recursive semaphores, along with simple worked examples in a set of accompanying example projects.

### FreeRTOS Mutexes

Mutexes are [binary semaphores](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores) that include a priority inheritance
mechanism. Whereas binary semaphores are the better choice for implementing synchronisation (between
tasks or between tasks and an interrupt), mutexes are the better choice for implementing simple mutual
exclusion (hence 'MUT'ual 'EX'clusion).

When used for mutual exclusion the mutex acts like a token that is used to guard a resource. When a
task wishes to access the resource it must first obtain ('take') the token. When it has finished with
the resource it must 'give' the token back - allowing other tasks the opportunity to access the
same resource.

Mutexes use the same semaphore access API functions so also permit a block time to be specified. The
block time indicates the maximum number of 'ticks' that a task should enter the Blocked state when
attempting to 'take' a mutex if the mutex is not immediately available. Unlike binary semaphores
however - mutexes employ priority inheritance. This means that if a high priority task blocks while
attempting to obtain a mutex (token) that is currently held by a lower priority task, then the priority
of the task holding the token is temporarily raised to that of the blocking task. This mechanism is
designed to ensure the higher priority task is kept in the blocked state for the shortest time possible,
and in so doing minimise the 'priority inversion' that has already occurred.

Priority inheritance does not cure priority inversion! It just minimises its effect in some situations. 
(See [Simplified priority inheritance](#simplified-priority-inheritance) below.)
Hard real time applications should be designed such that priority inversion does not happen in the first place.

Mutexes should not be used from an interrupt because:

- They include a priority inheritance mechanism which only makes sense if
  the mutex is given and taken from a task, not an interrupt.
- An interrupt cannot block to wait for a resource that is guarded by a
  mutex to become available.

*【图】*  
_Using a mutex to guard access to a shared resource._

### Simplified priority inheritance 

FreeRTOS implements a basic priority inheritance mechanism which was designed to optimize both space 
and execution cycles. A full priority inheritance mechanism requires significantly more data and processor 
cycles to determine inherited priority at any moment, especially when a task holds more than one mutex 
at a time.

Keep in mind these specific behaviors of the priority inheritance mechanism:

- A task can have its inherited priority raised further if 
  it takes a mutex without first releasing mutexes it already holds.
- A task remains at its highest inherited priority until it has released all the mutexes it holds. 
  This is regardless of the order the mutexes are released.
- A task will remain at the highest inherited priority if 
  multiple mutexes are held regardless of tasks waiting on any of the held mutexes completing their 
  wait (timing out).

