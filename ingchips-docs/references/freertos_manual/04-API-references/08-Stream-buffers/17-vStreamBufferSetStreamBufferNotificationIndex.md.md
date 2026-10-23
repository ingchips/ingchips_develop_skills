# vStreamBufferSetStreamBufferNotificationIndex()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
void vStreamBufferSetStreamBufferNotificationIndex( StreamBufferHandle_t xStreamBuffer,
                                                    UBaseType_t uxNotificationIndex );
```

Sets the task notification index used for the 
supplied [stream buffer](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API). 
Successive calls to stream buffer APIs (like [xStreamBufferSend](03-xStreamBufferSend) 
or [xStreamBufferReceive](05-xStreamBufferReceive)) for this stream buffer will use this new index for 
their task notifications.

Enable stream buffer functionality by including the FreeRTOS/source/stream\_buffer.c source file in the 
build and by setting the `configUSE_STREAM_BUFFERS` configuration constant to 1 in FreeRTOSConfig.h.


**Parameters:**

+ `xStreamBuffer`

  The handle of the stream buffer for which the task notification index is set.

+ `uxNotificationIndex`

  The task notification index to set.

