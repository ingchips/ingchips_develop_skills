[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h

```c
 QueueHandle_t xQueueCreateStatic(
                             UBaseType_t uxQueueLength,
                             UBaseType_t uxItemSize,
                             uint8_t *pucQueueStorageBuffer,
                             StaticQueue_t *pxQueueBuffer );
```

Creates a new [queue](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues) and returns a handle by which the queue can be
referenced.  [configSUPPORT\_STATIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
must be set to 1 in FreeRTOSConfig.h for this RTOS API function to be available.

Each queue requires RAM that is used to hold the queue state, and to hold the
items that are contained in the queue (the queue storage area).
If a queue is created using [xQueueCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate) then this
RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If a queue is created using xQueueCreateStatic()
then the RAM is provided by the application writer, which results in a greater
number of parameters, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.


**Parameters:**

+ *uxQueueLength*

  The maximum number of items the queue can hold at any one time.

+ *uxItemSize*

  The size, in bytes, required to hold each item in the queue.

  Items are queued by copy, not by reference, so this is the number of bytes that will be copied for each
  queued item. Each item in the queue must be the same size.

+ *pucQueueStorageBuffer*

  If uxItemSize is not zero then pucQueueStorageBuffer must point to a uint8\_t array that is at least
  large enough to hold the maximum number of items that can be in the queue at any one time - which
  is ( uxQueueLength * uxItemSize ) bytes. If uxItemSize is zero then pucQueueStorageBuffer can be NULL.

+ *pxQueueBuffer*

   Must point to a variable of type StaticQueue\_t, which will be used to hold the queue's data structure.


**Returns:**

If the queue is created successfully then a handle to the created queue
is returned. If pxQueueBuffer is NULL then NULL is returned.


**Example usage:**

```c

/* The queue is to be created to hold a maximum of 10 uint64\_t
   variables. */
#define QUEUE_LENGTH    10
#define ITEM_SIZE       sizeof( uint64_t )

/* The variable used to hold the queue's data structure. */
static StaticQueue_t xStaticQueue;

/* The array to use as the queue's storage area. This must be at least
   uxQueueLength * uxItemSize bytes. */
uint8_t ucQueueStorageArea[ QUEUE_LENGTH * ITEM_SIZE ];

void vATask( void *pvParameters )
{
QueueHandle_t xQueue;

    /* Create a queue capable of containing 10 uint64_t values. */
    xQueue = xQueueCreateStatic( QUEUE_LENGTH,
                                 ITEM_SIZE,
                                 ucQueueStorageArea,
                                 &xStaticQueue );

    /* pxQueueBuffer was not NULL so xQueue should not be NULL. */
    configASSERT( xQueue );
 }
```

