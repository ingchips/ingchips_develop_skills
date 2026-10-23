[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr.h 

```c
TaskHandle_t xSemaphoreGetMutexHolder( SemaphoreHandle_t xMutex );
```

INCLUDE\_xSemaphoreGetMutexHolder must be set to 1 in FreeRTOSConfig.h for this
function to be available.

Return the handle of the task that holds the mutex specified by the function parameter, if any.

xSemaphoreGetMutexHolder() can be used reliably to determine if the calling task
is the mutex holder, but cannot be used reliably if the mutex is held by any task
other than the calling task. This is because the mutex holder might change
between the calling task calling the function, and the calling task testing the
function's return value.

configUSE\_MUTEXES must be set to 1 in FreeRTOSConfig.h for xSemaphoreGetMutexHolder() to be available.


**Parameters:**

+ *xMutex* 

  The handle of the mutex being queried.


**Returns:**

The handle of the task that holds the mutex specified by the xMutex parameter. NULL is returned if the 
semaphore passed in the xMutex parameter is not a mutex type semaphore, or if the mutex is available 
and so not held by any task.
  
