# xStreamBatchingBufferCreate() / xStreamBatchingBufferCreateWithCallback()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
StreamBufferHandle_t xStreamBatchingBufferCreate( size_t xBufferSizeBytes,
                                                  size_t xTriggerLevelBytes );

StreamBufferHandle_t xStreamBatchingBufferCreateWithCallback( 
                         size_t xBufferSizeBytes,
                         size_t xTriggerLevelBytes
                         StreamBufferCallbackFunction_t pxSendCompletedCallback,
                         StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

Creates a new stream batching buffer using dynamically allocated memory. 
See [xStreamBatchingBufferCreateStatic()](19-xStreamBatchingBufferCreateStatic) for a version that uses 
statically allocated memory (memory that is allocated at compile time).

`configSUPPORT_DYNAMIC_ALLOCATION` must be set to 1 or left undefined in FreeRTOSConfig.h 
for `xStreamBatchingBufferCreate()` to be available. `configUSE_STREAM_BUFFERS` must be set to 1 in 
FreeRTOSConfig.h for `xStreamBatchingBufferCreate()` to be available. 
Additionally, `configUSE_SB_COMPLETED_CALLBACK` must be set to 1 in FreeRTOSConfig.h 
for `xStreamBatchingBufferCreateWithCallback()` to be available.

Enable stream buffer functionality by including the FreeRTOS/source/stream_buffer.c source file in the build.

The difference between a stream buffer and a stream batching buffer is when a task performs a read on 
a non-empty buffer:

+ A task that reads from a non-empty stream buffer returns immediately regardless of the amount of data 
  in the buffer.

+ A task that reads from a non-empty stream batching buffer blocks until the amount of data in the buffer 
  exceeds the trigger level or the block time expires.


**Parameters:**

+ `xBufferSizeBytes`

  The total number of bytes the stream batching buffer will be able to hold at any one time.

+ `xTriggerLevelBytes`

  The number of bytes that must be in the stream batching buffer to unblock a task 
  calling `xStreamBufferReceive` before the block time expires.

+ `pxSendCompletedCallback`

  The callback invoked when a number of bytes at least equal to the trigger level are sent to the 
  stream batching buffer. If the parameter is NULL, it will use the default implementation provided 
  by the `sbSEND_COMPLETED` macro. To enable the callback, `configUSE_SB_COMPLETED_CALLBACK` must be 
  set to 1 in FreeRTOSConfig.h. The send completed callback function must have the prototype defined 
  by `StreamBufferCallbackFunction_t`, which is:

  ```c
  void vSendCallbackFunction( StreamBufferHandle_t xStreamBuffer,
                              BaseType_t xIsInsideISR,
                              BaseType_t * const pxHigherPriorityTaskWoken );
  ```

+ `pxReceiveCompletedCallback`

  The callback invoked when more than zero bytes are read from a stream batching buffer. If the parameter 
  is NULL, it will use the default implementation provided by the `sbRECEIVE_COMPLETED` macro. To enable 
  the callback, `configUSE_SB_COMPLETED_CALLBACK` must be set to 1 in FreeRTOSConfig.h. The receive completed 
  callback function must have the prototype defined by `StreamBufferCallbackFunction_t`, which is:

  ```c
  void vReceiveCallbackFunction( StreamBufferHandle_t xStreamBuffer,
                                 BaseType_t xIsInsideISR,
                                 BaseType_t * const pxHigherPriorityTaskWoken );
  ```


**Returns:**

+ If NULL is returned, then the stream batching buffer cannot be created because there is insufficient 
  heap memory available for FreeRTOS to allocate the stream batching buffer data structures and storage 
  area. 

+ The return of a non-NULL value indicates that the stream batching buffer has been created successfully - 
  the returned value should be stored as the handle to the created stream batching buffer.


**Example use:**

```c
void vAFunction( void )
{
StreamBufferHandle_t xStreamBatchingBuffer;
const size_t xStreamBufferSizeBytes = 100, xTriggerLevel = 10;
 
    // Create a stream batching buffer that can hold 100 bytes.  The memory used
    // to hold both the stream batching buffer structure and the data in the stream
    // batching buffer is allocated dynamically.
    xStreamBatchingBuffer = xStreamBatchingBufferCreate( xStreamBufferSizeBytes, xTriggerLevel );
 
    if( xStreamBatchingBuffer == NULL )
    {
        // There was not enough heap memory space available to create the
        // stream batching buffer.
    }
    else
    {
        // The stream batching buffer was created successfully and can now be used.
    }
}
```

