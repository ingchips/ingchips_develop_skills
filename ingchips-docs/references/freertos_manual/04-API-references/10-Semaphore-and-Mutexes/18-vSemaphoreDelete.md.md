# vSemaphoreDelete

[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**TIP: In many usage scenarios it is faster and more memory efficient to use a direct to task notification instead of a binary semaphore**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)


semphr.h

```c
void vSemaphoreDelete( SemaphoreHandle_t xSemaphore );
```

Deletes a semaphore, including mutex type semaphores and recursive semaphores.

Do not delete a semaphore that has tasks blocked on it (tasks that are in the
Blocked state waiting for the semaphore to become available).

**Parameters:**

- *xSemaphore*

  The handle of the semaphore being deleted.
