# FreeRTOS binary semaphores

[See also [Blocking on Multiple RTOS Objects](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

The [FreeRTOS tutorial book](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
provides additional information on queues, binary semaphores, mutexes, counting
semaphores and recursive semaphores, along with simple worked examples in a set of
accompanying example projects.

### FreeRTOS Binary Semaphores

[**TIP: 'Task Notifications' can provide a light weight alternative to binary semaphores in many situations**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)

Binary semaphores are used for both mutual exclusion and synchronisation purposes.

Binary semaphores and mutexes are very similar but have some subtle differences: Mutexes include a priority
inheritance mechanism, binary semaphores do not. This makes binary semaphores the better choice for
implementing synchronisation (between tasks or between tasks and an interrupt), and mutexes the better
choice for implementing simple mutual exclusion. The [description](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)
of how a mutex can be used as a mutual exclusion mechanism holds equally for binary semaphores. This sub-section
will only describe using binary semaphores for synchronisation.

Semaphore API functions permit a block time to be specified. The block time indicates the maximum number
of 'ticks' that a task should enter the Blocked state when attempting to 'take' a semaphore, should the
semaphore not be immediately available. If more than one task blocks on the same semaphore then the task
with the highest priority will be the task that is unblocked the next time the semaphore becomes available.

Think of a binary semaphore as a queue that can only hold one item. The queue can therefore only be empty
or full (hence binary). Tasks and interrupts using the queue don't care what the queue holds - they only
want to know if the queue is empty or full. This mechanism can be exploited to synchronise (for example)
a task with an interrupt.

Consider the case where a task is used to service a peripheral. Polling the peripheral would be wasteful
of CPU resources, and prevent other tasks from executing. It is therefore preferable that the task spends
most of its time in the Blocked state (allowing other tasks to execute) and only execute itself when there
is actually something for it to do. This is achieved using a binary semaphore by having the task Block
while attempting to 'take' the semaphore. An interrupt routine is then written for the peripheral that
just 'gives' the semaphore when the peripheral requires servicing. The task always 'takes' the
semaphore (reads from the queue to make the queue empty), but never 'gives' it. The interrupt
always 'gives' the semaphore (writes to the queue to make it full) but never takes it. The source code
provided on the [xSemaphoreGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) documentation page should make this clearer. Also
see [RTOS task notifications](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications), which can be used as a faster and lighter
weight binary semaphore alternaitve in some situations.

Task prioritisation can be used to ensure peripherals get services in a timely manner - effectively generating
a 'deferred interrupt' scheme. (note FreeRTOS also has
a [built in deferred interrupt mechanism](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/18-xTimerPendFunctionCallFromISR)). An alternative approach is to
use a queue in place of the semaphore. When this is done the interrupt routine can capture the data
associated with the peripheral event and send it on a queue to the task. The task unblocks when data
becomes available on the queue, retrieves the data from the queue, then performs any data processing
that is required. This second scheme permits interrupts to remain as short as possible, with all post
processing instead occurring within a task.

See the [Semaphores/Mutexes](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores) section of the user documentation for a list of semaphore related API
functions. Searching the files in the FreeRTOS/Demo/Common/Minimal directory will reveal multiple examples
of their usage. Note that interrupts must NOT use API functions that do not end in "FromISR".

*【图】*  
_Using a semaphore to synchronise a task with an interrupt. The interrupt only ever 'gives' the
semaphore, while the task only ever 'takes' the semaphore._
