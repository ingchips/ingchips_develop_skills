# xSemaphoreCreateBinary

[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**TIP: In many usage scenarios it is faster and more memory efficient to use a direct to task notification instead of a binary semaphore**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)


semphr.h


```c
SemaphoreHandle_t xSemaphoreCreateBinary( void );
```

Creates a [binary semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores), and returns a handle by which the
semaphore can be referenced. [configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
must be set to 1 in FreeRTOSConfig.h, or left undefined (in which case it will default to 1), for this
RTOS API function to be available.

Each binary semaphore require a small amount of RAM that is used to hold the semaphore's state. If a
binary semaphore is created using xSemaphoreCreateBinary() then the required RAM is automatically allocated
from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management). If a binary semaphore is created
using [xSemaphoreCreateBinaryStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic) then the RAM is provided by the
application writer, which requires an additional parameter, but allows the RAM to be statically allocated
at compile time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for
more information.

The semaphore is created in the 'empty' state, meaning the semaphore must first
be given using the [xSemaphoreGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive) API function
before it can subsequently be taken (obtained) using the [xSemaphoreTake](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)() function.

Binary semaphores and [mutexes](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex) are very similar but
have some subtle differences: Mutexes include a priority inheritance mechanism,
binary semaphores do not. This makes binary semaphores the better choice for
implementing synchronisation (between tasks or between tasks and an interrupt),
and mutexes the better choice for implementing simple mutual exclusion.

A binary semaphore need not be given back once obtained, so task synchronisation
can be implemented by one task/interrupt continuously 'giving' the semaphore
while another continuously 'takes' the semaphore. This is demonstrated by
the sample code on the [xSemaphoreGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) documentation page.
Note the same functionality can often be achieved in a more efficient way
using a [direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore).

The priority of a task that 'takes' a mutex can potentially be raised if another task of higher
priority attempts to obtain the same mutex. The task that owns the mutex 'inherits' the priority
of the task attempting to 'take' the same mutex. This means the mutex must always be 'given' back -
otherwise the higher priority task will never be able to obtain the mutex, and the lower priority
task will never 'disinherit' the priority. An example of a mutex being used to implement mutual
exclusion is provided on the [xSemaphoreTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) documentation page.

Both mutex and binary semaphores are referenced by variables of type SemaphoreHandle\_t and can be used
in any task level API function that takes a parameter of that type. Unlike mutexes,
binary semaphores can be used in interrupt service routines.


**Return values:**

+ *NULL*

  The semaphore could not be created because there was insufficient [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) available.

+ *Any other value*

  The semaphore was created successfully. The returned value is a handle by which the semaphore can
  be referenced.


**Example usage:**

```c
SemaphoreHandle_t xSemaphore;

void vATask( void * pvParameters )
{
    /* Attempt to create a semaphore. */
    xSemaphore = xSemaphoreCreateBinary();

    if( xSemaphore == NULL )
    {
        /* There was insufficient FreeRTOS heap available for the semaphore to
           be created successfully. */
    }
    else
    {
        /* The semaphore can now be used. Its handle is stored in the
           xSemahore variable. Calling xSemaphoreTake() on the semaphore here
           will fail until the semaphore has first been given. */
    }
}
```
