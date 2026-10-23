# xSemaphoreCreateCounting

[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]


[**TIP: 'Task Notifications' can provide a light weight alternative to counting semaphores in many situations**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)

semphr.h


```c
SemaphoreHandle_t xSemaphoreCreateCounting( UBaseType_t uxMaxCount,
                                            UBaseType_t uxInitialCount);
```

Creates a [counting semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/03-Counting-semaphores) and returns a handle by
which the newly created semaphore can be
referenced. [configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set
to 1 in FreeRTOSConfig.h, or left undefined (in which case it will default to 1), for this RTOS API function
to be available.

Each counting semaphore require a small amount of RAM that is used to hold the
semaphore's state. If a counting semaphore is created using xSemaphoreCreateCounting()
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If a counting semaphore is created using [xSemaphoreCreateCountingStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/05-xSemaphoreCreateCountingStatic)
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.

Counting semaphores are typically used for two things:

- Counting events.

  In this usage scenario an event handler will 'give' a semaphore each time
  an event occurs (incrementing the semaphore count value), and a handler
  task will 'take' a semaphore each time it processes an event
  (decrementing the semaphore count value). The count value is therefore
  the difference between the number of events that have occurred and the
  number that have been processed. In this case it is desirable for the
  initial count value to be zero.

  Note the same functionality can often be achieved in a more efficient way
  using a [direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications).

- Resource management.

  In this usage scenario the count value indicates the number of resources
  available. To obtain control of a resource a task must first obtain a
  semaphore - decrementing the semaphore count value. When the count value
  reaches zero there are no free resources. When a task finishes with the
  resource it 'gives' the semaphore back - incrementing the semaphore count
  value. In this case it is desirable for the initial count value to be
  equal to the maximum count value, indicating that all resources are free.


**Parameters:**

- *uxMaxCount*

  The maximum count value that can be reached. When the semaphore reaches this value it can no longer be 'given'.

- *uxInitialCount*

  The count value assigned to the semaphore when it is created.

**Returns:**

- If the semaphore is created successfully then a handle to the semaphore
  is returned.

- If the semaphore cannot be created because the RAM required
  to hold the semaphore [cannot be allocated](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
  then NULL is returned.


**Example usage:**

```c
void vATask( void * pvParameters )
{
SemaphoreHandle_t xSemaphore;

    /* Create a counting semaphore that has a maximum count of 10 and an
       initial count of 0. */
    xSemaphore = xSemaphoreCreateCounting( 10, 0 );

    if( xSemaphore != NULL )
    {
        /* The semaphore was created successfully. */
    }
}
```
