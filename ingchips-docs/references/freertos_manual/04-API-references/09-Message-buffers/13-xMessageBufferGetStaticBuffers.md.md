# xMessageBufferGetStaticBuffers()

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]


message\_buffer.h

```c
BaseType_t xMessageBufferGetStaticBuffers( MessageBufferHandle_t xMessageBuffer,
                                           uint8_t ** ppucMessageBufferStorageArea,
                                           StaticMessageBuffer_t ** ppxStaticMessageBuffer );
```

configSUPPORT\_STATIC\_ALLOCATION must be defined as 1 for this function to be available. See the RTOS 
Configuration documentation for more information.

Retrieve pointers to a statically created message buffer's data structure buffer and storage area buffer. 
These are the same buffers that are supplied at the time of creation.


**Parameters:**

+ *xMessageBuffer*

  The message buffer whose data structure buffer and storage area buffer will be retrieved.

+ *ppucMessageBufferStorageArea*

  Used to return a pointer to the message buffer's storage area buffer.

+ *ppxStaticMessageBuffer*

   Used to return a pointer to the message buffer's data structure buffer.


**Returns:**

pdTRUE if the buffers were retrieved, pdFALSE otherwise. 


