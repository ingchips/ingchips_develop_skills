# xSemaphoreCreateCountingStatic

[[Semaphores](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**TIP: 'Task Notifications' can provide a light weight alternative to counting semaphores in many situations**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)


semphr.h

```c
SemaphoreHandle_t xSemaphoreCreateCountingStatic(
                                 UBaseType_t uxMaxCount,
                                 UBaseType_t uxInitialCount
                                 StaticSemaphore_t *pxSemaphoreBuffer );
```

Creates a [counting semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/03-Counting-semaphores) and returns a handle by
which the newly created semaphore can be
referenced. [configSUPPORT\_STATIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set
to 1 in FreeRTOSConfig.h for this RTOS API function to be available.

Each counting semaphore require a small amount of RAM that is used to hold the
semaphore's state. If a counting semaphore is created using [xSemaphoreCreateCounting()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting)
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If a counting semaphore is created using xSemaphoreCreateCountingStatic()
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.


Counting semaphores are typically used for two things:

1. Counting events.

   In this usage scenario an event handler will 'give' a semaphore each time
   an event occurs (incrementing the semaphore count value), and a handler
   task will 'take' a semaphore each time it processes an event
   (decrementing the semaphore count value). The count value is therefore
   the difference between the number of events that have occurred and the
   number that have been processed. In this case it is desirable for the
   initial count value to be zero.

   Note the same functionality can often be achieved in a more efficient way
   using a [direct to task notification](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications).

2. Resource management.

   In this usage scenario the count value indicates the number of resources
   available. To obtain control of a resource a task must first obtain a
   semaphore - decrementing the semaphore count value. When the count value
   reaches zero there are no free resources. When a task finishes with the
   resource it 'gives' the semaphore back - incrementing the semaphore count
   value. In this case it is desirable for the initial count value to be
   equal to the maximum count value, indicating that all resources are free.


**Parameters:**

+ *uxMaxCount*

  The maximum count value that can be reached. When the semaphore reaches this value it can no longer
  be 'given'.

+ *uxInitialCount*

  The count value assigned to the semaphore when it is created.

+ *pxSemaphoreBuffer*

  Must point to a variable of type StaticSemaphore\_t, which is then used to hold the semaphore's data structures.


**Returns:**

If the semaphore is created successfully then a handle to the semaphore is returned. If pxSemaphoreBuffer is
NULL then NULL is returned.


**Example usage:**

```c
static StaticSemaphore_t xSemaphoreBuffer;

void vATask( void * pvParameters )
{
SemaphoreHandle_t xSemaphore;

    /* Create a counting semaphore that has a maximum count of 10 and an
       initial count of 0. The semaphore's data structures are stored in the
       xSemaphoreBuffer variable - no dynamic memory allocation is performed. */
    xSemaphore = xSemaphoreCreateCountingStatic( 10, 0, &xSemaphoreBuffer );

    /* pxSemaphoreBuffer was not NULL so it is expected that the semaphore
       will be created. */
    [configASSERT](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)( xSemaphore );
}
```
