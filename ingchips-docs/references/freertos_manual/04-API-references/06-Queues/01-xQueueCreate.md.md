[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h

```c
 QueueHandle_t xQueueCreate( UBaseType_t uxQueueLength,
                             UBaseType_t uxItemSize );
```

Creates a new [queue](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues) and returns a handle by which the queue can be
referenced.  [configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
must be set to 1 in FreeRTOSConfig.h, or left undefined (in which case it will
default to 1), for this RTOS API function to be available.

Each queue requires RAM that is used to hold the queue state, and to hold the
items that are contained in the queue (the queue storage area).
If a queue is created using `xQueueCreate()` then the required RAM is automatically
allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).  If a queue is created
using [xQueueCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic)
then the RAM is provided by the application writer, which results in a greater
number of parameters, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.


**Parameters:**

- *uxQueueLength*

  The maximum number of items the queue can hold at any one time.

- *uxItemSize*

  The size, in bytes, required to hold each item in the queue.

  Items are queued by copy, not by reference, so this is the number of bytes that will be copied for
  each queued item. Each item in the queue must be the same size.


**Returns:**

- If the queue is created successfully then a handle to the created queue is returned. If the memory
  required to create the queue [could not be allocated](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) then NULL is returned.


**Example usage:**

```c
struct AMessage
{
    char ucMessageID;
    char ucData[ 20 ];
};

void vATask( void *pvParameters )
{
QueueHandle_t xQueue1, xQueue2;

    /* Create a queue capable of containing 10 unsigned long values. */
    xQueue1 = xQueueCreate( 10, sizeof( unsigned long ) );

    if( xQueue1 == NULL )
    {
        /* Queue was not created and must not be used. */
    }

    /* Create a queue capable of containing 10 pointers to AMessage
       structures. These are to be queued by pointers as they are
       relatively large structures. */
    xQueue2 = xQueueCreate( 10, sizeof( struct AMessage * ) );

    if( xQueue2 == NULL )
    {
        /* Queue was not created and must not be used. */
    }

    /* ... Rest of task code. */
 }
```
