[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr.h

```c
UBaseType_t uxSemaphoreGetCount( SemaphoreHandle_t xSemaphore );
```

Returns the count of a semaphore.


**Parameters:** 

- *xSemaphore*

  The handle of the semaphore being queried.


**Returns:** 

If the semaphore is a counting semaphore then the semaphores current count value
is returned. If the semaphore is a binary semaphore then
1 is returned if the semaphore is available, and 0 is returned if the
semaphore is not available.
 
