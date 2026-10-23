[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr.h

```c
SemaphoreHandle_t xSemaphoreCreateMutexStatic(
                            StaticSemaphore_t *pxMutexBuffer );
```

Creates a [mutex](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), and returns
a handle by which the created mutex can be referenced. Mutexes cannot be used
in interrupt service routines.

[configSUPPORT\_STATIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
and [configUSE\_MUTEXES](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must both be set to 1 in FreeRTOSConfig.h for
xSemaphoreCreateMutexStatic() to be available.

Each mutex require a small amount of RAM that is used to hold the
mutex's state. If a mutex is created using [xSemaphoreCreateMutex](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)()
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If a mutex is created using xSemaphoreCreateMutexStatic()
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.

Mutexes are taken using [xSemaphoreTake](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)(), and given
using [xSemaphoreGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive).
xSemaphoreTakeRecursive() and xSemaphoreGiveRecursive() can only be used on
mutexes created using [xSemaphoreCreateResursiveMutex](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)().

Mutexes and [binary semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/03-vSemaphoreCreateBinary) are very similar but
have some subtle differences: Mutexes include a priority inheritance mechanism,
binary semaphores do not. This makes binary semaphores the better choice for
implementing synchronisation (between tasks or between tasks and an interrupt),
and mutexes the better choice for implementing simple mutual exclusion.

The priority of a task that 'takes' a mutex will be temporarily raised if another
task of higher priority attempts to obtain the same mutex. The task that owns
the mutex 'inherits' the priority of the task attempting to 'take' the same
mutex. This means the mutex must always be 'given' back - otherwise the higher
priority task will never be able to obtain the mutex, and the lower priority
task will never 'disinherit' the priority. For more on the priority inheritance 
mechanism see the [FreeRTOS Mutex documentation page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)

An example of a mutex being used to implement mutual
exclusion is provided on the [xSemaphoreTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) documentation page.

A binary semaphore need not be given back once obtained, so task synchronisation
can be implemented by one task/interrupt continuously 'giving' the semaphore
while another continuously 'takes' the semaphore. This is demonstrated by
the sample code on the [xSemaphoreGiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) documentation page.
Note that the same functionality can be achieved in a more efficient way using
a direct to task notification.

Handles to both mutexes and binary semaphores are assigned to variables of type
SemaphoreHandle\_t, and can be used in any task level (as opposed to interrupt
safe) API function that takes a parameter of that type.


**Parameters:**

+ *pxMutexBuffer*

  Must point to a variable of type StaticSemaphore\_t, which will be used to hold the mutex type semaphore's state.


**Return:**

If the mutex type semaphore was created successfully then a handle to the created mutex is returned.
If the mutex was not created because pxMutexBuffer was NULL then NULL is returned.


**Example usage:**

```c
 SemaphoreHandle_t xSemaphore = NULL;
 StaticSemaphore_t xMutexBuffer;

 void vATask( void * pvParameters )
 {
    /* Create a mutex semaphore without using any dynamic memory
       allocation. The mutex's data structures will be saved into
       the xMutexBuffer variable. */
    xSemaphore = xSemaphoreCreateMutexStatic( &xMutexBuffer );

    /* The pxMutexBuffer was not NULL, so it is expected that the
       handle will not be NULL. */
    [configASSERT](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)( xSemaphore );

    /* Rest of the task code goes here. */
 }
```
