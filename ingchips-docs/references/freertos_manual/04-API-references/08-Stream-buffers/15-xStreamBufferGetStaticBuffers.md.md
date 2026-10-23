# xStreamBufferGetStaticBuffers()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]


stream\_buffer.h

```c
 BaseType_t xStreamBufferGetStaticBuffers( StreamBufferHandle_t xStreamBuffer,
                                           uint8_t ** ppucStreamBufferStorageArea,
                                           StaticStreamBuffer_t ** ppxStaticStreamBuffer );
```

`configSUPPORT_STATIC_ALLOCATION` must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation 
for more information.

Retrieve pointers to a statically created stream buffer's data structure buffer and storage area buffer. 
These are the same buffers that are supplied at the time of creation.


**Parameters:**

+ `xStreamBuffer`

  The stream buffer whose data structure buffer and storage area buffer will be retrieved.

+ `ppucStreamBufferStorageArea`

  Used to return a pointer to the stream buffer's storage area buffer.

+ `ppxStaticStreamBuffer`

  Used to return a pointer to the stream buffer's data structure buffer.


**Returns:**

+ `pdTRUE` if the buffers were retrieved, 
+ `pdFALSE` otherwise. 


