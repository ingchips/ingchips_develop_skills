[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr.h

```c
SemaphoreHandle_t xSemaphoreCreateRecursiveMutex( void )
```

Creates a [recursive mutex](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/05-Recursive-mutexes), and returns a handle by which the mutex can be
referenced. Recursive mutexes cannot be used in interrupt service
routines. [configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) and
configUSE\_RECURSIVE\_MUTEXES must both be set to 1 in FreeRTOSConfig.h for xSemaphoreCreateRecursiveMutex()
to be available (configSUPPORT\_DYNAMIC\_ALLOCATION can also be left undefined, in which case it will
default to 1).

Each recursive mutex require a small amount of RAM that is used to hold the recursive mutex's state.
If a mutex is created using [xSemaphoreCreateRecursiveMutex()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If a recursive mutex is created using xSemaphoreCreateRecursiveMutexStatic()
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.

Recursive mutexes are 'taken' (obtained) using the [xSemaphoreTakeRecursive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/14-xSemaphoreTakeRecursive) and
given (released) using the [xSemaphoreGiveRecursive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/16-xSemaphoreGiveRecursive) API functions respectively.
xSemaphoreTake() and xSemaphoreGive() must not be used.

Non-recursive mutexes are created using xSemaphoreCreateMutex() and
xSemaphoreCreateMutexStatic(). A non-recursive mutex can only be 'taken' by a
task once. Any attempt by a task to take a non-recursive mutex that it already
holds will fail - and the mutex will always be given back the first time the
task 'gives' the mutex.

Contrary to non-recursive mutexes, a task can 'take' a recursive mutex multiple
times, and the recursive mutex will only be returned after the holding task has
'given' the mutex the same number of times it 'took' the mutex.

Like non-recursive mutexes, recursive mutexes implement a priority inheritance
algorithm. The priority of a task that 'takes' a mutex will be temporarily raised if another
task of higher priority attempts to obtain the same mutex. The task that owns
the mutex 'inherits' the priority of the task attempting to 'take' the same
mutex. This means the mutex must always be 'given' back - otherwise the higher
priority task will never be able to obtain the mutex, and the lower priority
task will never 'disinherit' the priority. For more on the priority inheritance 
mechanism see the [FreeRTOS Mutex documentation page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)


**Returns:**

If the recursive mutex was created successfully then a handle to the created mutex is returned. If the
recursive mutex was not created because the memory required to hold the
mutex [could not be allocated](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) then NULL is returned.


**Example usage:**

```c
 SemaphoreHandle_t xMutex;

 void vATask( void * pvParameters )
 {
    Create a recursive mutex.
    xMutex = xSemaphoreCreateRecursiveMutex();

    if( xMutex != NULL )
    {
        /* The recursive mutex was created successfully and
           can now be used. */
    }
 }
```
