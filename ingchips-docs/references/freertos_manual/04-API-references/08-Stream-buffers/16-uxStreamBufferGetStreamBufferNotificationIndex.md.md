# uxStreamBufferGetStreamBufferNotificationIndex()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
UBaseType_t uxStreamBufferGetStreamBufferNotificationIndex( StreamBufferHandle_t xStreamBuffer );
```

Retrieves the task notification index used for the 
supplied [stream buffer](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API), 
which can be set using [vStreamBufferSetStreamBufferNotificationIndex](17-vStreamBufferSetStreamBufferNotificationIndex). 
If the task notification index for the stream buffer is not changed using `vStreamBufferSetStreamBufferNotificationIndex`, 
this function returns the default value `tskDEFAULT_INDEX_TO_NOTIFY`.

Enable stream buffer functionality by including the FreeRTOS/source/stream\_buffer.c source file in the 
build and by setting the `configUSE_STREAM_BUFFERS` configuration constant to 1 in FreeRTOSConfig.h.


**Parameters:**

+ `xStreamBuffer`

  The handle of the stream buffer for which the task notification index is retrieved.


**Returns:**

+ The task notification index used for the stream buffer.

