[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr.h 

```c
xSemaphoreTakeFromISR
 (
 SemaphoreHandle_t xSemaphore,
 signed BaseType_t *pxHigherPriorityTaskWoken
 )
```

A version of [xSemaphoreTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) that can be called from
an ISR. Unlike xSemaphoreTake(), xSemaphoreTakeFromISR() does not permit a block
time to be specified.


**Parameters:**

+ *xSemaphore* 

  The semaphore being 'taken'. A semaphore is referenced by a variable of type SemaphoreHandle\_t and must be 
  explicitly created before being used.

+ *pxHigherPriorityTaskWoken* 

  It is possible (although unlikely, and dependent on the semaphore type) that a semaphore will have 
  one or more tasks blocked on it waiting to give the semaphore. Calling xSemaphoreTakeFromISR() will 
  make a task that was blocked waiting to give the semaphore leave the Blocked state. If calling the 
  API function causes a task to leave the Blocked state, and the unblocked task has a priority equal 
  to or higher than the currently executing task (the task that was interrupted), then, internally, the 
  API function will set *pxHigherPriorityTaskWoken to pdTRUE.If xSemaphoreTakeFromISR() 
  sets *pxHigherPriorityTaskWoken to pdTRUE, then a context switch should be performed before the interrupt 
  is exited. This will ensure that the interrupt returns directly to the highest priority Ready state 
  task. The mechanism is identical to that used in the xQueueReceiveFromISR() function, and readers are 
  referred to the [xQueueReceiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/10-xQueueReceiveFromISR) documentation for further explanation. From FreeRTOS 
  V7.3.0 pxHigherPriorityTaskWoken is an optional parameter and can be set to NULL.


**Returns:**

pdTRUE if the semaphore was successfully taken. pdFALSE if the semaphore was not successfully taken 
because it was not available.
  
