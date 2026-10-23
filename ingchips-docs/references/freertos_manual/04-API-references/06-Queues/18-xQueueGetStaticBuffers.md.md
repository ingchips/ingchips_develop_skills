# xQueueGetStaticBuffers()

[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h

```c
 BaseType_t xQueueGetStaticBuffers( QueueHandle_t xQueue,
                                    uint8_t ** ppucQueueStorage,
                                    StaticQueue_t ** ppxStaticQueue );
```

`configSUPPORT_STATIC_ALLOCATION` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation for more information.

Retrieve pointers to a statically created queue's data structure buffer and storage area buffer. These 
are the same buffers that are supplied at the time of creation.

**Parameters:**

+ `xQueue`

  The queue whose data structure buffer and storage area buffer will be retrieved.

+ `ppucQueueStorage`

  Used to return a pointer to the queue's storage area buffer.

+ `ppxStaticQueue`

  Used to return a pointer to the queue's data structure buffer.

**Returns:**

+ `pdTRUE` if the buffers were retrieved, 
+ `pdFALSE` otherwise. 


