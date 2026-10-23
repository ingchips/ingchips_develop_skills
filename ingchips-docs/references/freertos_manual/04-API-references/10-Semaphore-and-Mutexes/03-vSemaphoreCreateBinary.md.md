[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr.h 

```c
vSemaphoreCreateBinary( SemaphoreHandle_t xSemaphore )
```

**NOTE:** The `vSemaphoreCreateBinary()` macro remains in the source code to ensure backward compatibility, 
but it should not be used in new designs. Use the [xSemaphoreCreateBinary()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary) 
function instead.
 
 Also, in many cases, it is faster and more memory efficient to use 
a [direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) in place of a binary semaphore.

*Macro* that creates a semaphore by using the existing queue mechanism. The queue length is 1 as this is 
a binary semaphore. The data size is 0 as we don't want to actually store any data - we just want to know 
if the queue is empty or full.

Binary semaphores and [mutexes](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex) are very similar but have some subtle differences: 
Mutexes include a priority inheritance mechanism, binary semaphores do not. This makes binary semaphores 
the better choice for implementing synchronisation (between tasks or between tasks and an interrupt), and 
mutexes the better choice for implementing simple mutual exclusion.

A binary semaphore need not be given back once obtained, so task synchronisation can be implemented by 
one task/interrupt continuously 'giving' the semaphore while another continuously 'takes' the semaphore. 
This is demonstrated by the sample code on the [xSemaphoreGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) documentation page.

The priority of a task that 'takes' a mutex can potentially be raised if another task of higher
priority attempts to obtain the same mutex. The task that owns the mutex 'inherits' the priority
of the task attempting to 'take' the same mutex. This means the mutex must always be 'given' back -
otherwise the higher priority task will never be able to obtain the mutex, and the lower priority
task will never 'disinherit' the priority. An example of a mutex being used to implement mutual
exclusion is provided on the [xSemaphoreTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) documentation page.

Both mutex and binary semaphores are assigned to variables of type `SemaphoreHandle_t` and can be used
in any API function that takes a parameter of this type.


**Parameters:**

- *xSemaphore*

  Handle to the created semaphore. Should be of type `SemaphoreHandle\_t`. 


**Example usage:** 

```c
 SemaphoreHandle_t xSemaphore;

 void vATask( void * pvParameters )
 {
    // Semaphore cannot be used before a call to vSemaphoreCreateBinary ().
    // This is a macro so pass the variable in directly.
    vSemaphoreCreateBinary( xSemaphore );

    if( xSemaphore != NULL )
    {
        // The semaphore was created successfully.
        // The semaphore can now be used.
    }
 }
 ```
