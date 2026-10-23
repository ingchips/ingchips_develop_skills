# FreeRTOS counting semaphores

[See also [Blocking on Multiple RTOS Objects](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

The [FreeRTOS tutorial book](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
provides additional information on queues, binary semaphores, mutexes, counting
semaphores and recursive semaphores, along with simple worked examples in a set of accompanying example projects.

### FreeRTOS Counting Semaphores

[**TIP: 'Task Notifications' can provide a light weight alternative to counting semaphores in many situations**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)

Just as binary semaphores can be thought of as queues of length one, counting semaphores can be thought of
as queues of length greater than one. Again, users of the semaphore are not interested in the data that is
stored in the queue - just whether or not the queue is empty or not.

Counting semaphores are typically used for two things:

1. Counting events.

   In this usage scenario an event handler will 'give' a semaphore each time an event occurs (incrementing
   the semaphore count value), and a handler task will 'take' a semaphore each time it processes an
   event (decrementing the semaphore count value). The count value is therefore the difference between the
   number of events that have occurred and the number that have been processed. In this case it is desirable
   for the count value to be zero when the semaphore is created.

1. Resource management.

   In this usage scenario the count value indicates the number of resources available. To obtain control
   of a resource a task must first obtain a semaphore - decrementing the semaphore count value. When the
   count value reaches zero there are no free resources. When a task finishes with the resource it 'gives'
   the semaphore back - incrementing the semaphore count value. In this case it is desirable for the count
   value to be equal the maximum count value when the semaphore is created.

See the [Semaphores/Mutexes](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores) section of the user documentation for a list of semaphore related API
functions. Searching the files in the FreeRTOS/Demo/Common/Minimal directory will reveal multiple examples of their usage.
Note that interrupts must NOT use API functions that do not end in "FromISR".
