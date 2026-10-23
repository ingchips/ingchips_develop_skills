[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]


semphr.h

```c
SemaphoreHandle_t xSemaphoreCreateMutex( void )
```

Creates a [mutex](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), and returns
a handle by which the created mutex can be referenced. Mutexes cannot be used
in interrupt service routines.

[configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
and [configUSE\_MUTEXES](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must both be set to 1 in FreeRTOSConfig.h
for `xSemaphoreCreateMutex()` to be available. (`configSUPPORT_DYNAMIC_ALLOCATION` can also be left undefined,
in which case it will default to 1.)

Each mutex require a small amount of RAM that is used to hold the
mutex's state. If a mutex is created using `xSemaphoreCreateMutex()`
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If a mutex is created using [xSemaphoreCreateMutexStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic)
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.


Mutexes are taken using [xSemaphoreTake](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)(), and given
using [xSemaphoreGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive). `xSemaphoreTakeRecursive()` and `xSemaphoreGiveRecursive()` can
only be used on mutexes created using [xSemaphoreCreateRecursiveMutex](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)().

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
`SemaphoreHandle_t`, and can be used in any task level (as opposed to interrupt
safe) API function that takes a parameter of that type.


**Returns:**

- If the mutex type semaphore was created successfully then a handle to the created mutex is returned.

- If the mutex was not created because the memory required to hold the mutex [could not be allocated](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) then NULL is returned.


**Example usage:**

```c
SemaphoreHandle_t xSemaphore;

void vATask( void * pvParameters )
{
   /* Create a mutex type semaphore. */
   xSemaphore = xSemaphoreCreateMutex();

   if( xSemaphore != NULL )
   {
       /* The semaphore was created successfully and
          can be used. */
   }
}
```
