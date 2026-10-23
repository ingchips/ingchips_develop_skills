# xStreamBatchingBufferCreateStatic() / xStreamBatchingBufferCreateStaticWithCallback()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
StreamBufferHandle_t xStreamBatchingBufferCreateStatic( size_t xBufferSizeBytes,
                                                        size_t xTriggerLevelBytes,
                                                        uint8_t *pucStreamBufferStorageArea,
                                                        StaticStreamBuffer_t *pxStaticStreamBuffer );

StreamBufferHandle_t xStreamBatchingBufferCreateStaticWithCallback(
                                    size_t xBufferSizeBytes,
                                    size_t xTriggerLevelBytes,
                                    uint8_t *pucStreamBufferStorageArea,
                                    StaticStreamBuffer_t *pxStaticStreamBuffer,
                                    StreamBufferCallbackFunction_t pxSendCompletedCallback,
                                    StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

Creates a new stream batching buffer using statically allocated memory. 
See [xStreamBatchingBufferCreate()](18-xStreamBatchingBufferCreate) for a version that uses dynamically 
allocated memory.

`configSUPPORT_STATIC_ALLOCATION` must be set to 1 in FreeRTOSConfig.h for `xStreamBatchingBufferCreateStatic()` 
to be available. `configUSE_STREAM_BUFFERS` must be set to 1 in FreeRTOSConfig.h 
for `xStreamBatchingBufferCreateStatic()` to be available. Additionally, `configUSE_SB_COMPLETED_CALLBACK` 
must be set to 1 in FreeRTOSConfig.h for `xStreamBatchingBufferCreateStaticWithCallback()` to be available.

Enable stream buffer functionality by including the FreeRTOS/source/stream_buffer.c source file in the build.

The difference between a stream buffer and a stream batching buffer is when a task performs a read on 
a non-empty buffer:

+ A task that reads from a non-empty stream buffer returns immediately regardless of the amount of data 
  in the buffer.

+ A task that reads from a non-empty stream batching buffer blocks until the amount of data in the buffer 
  exceeds the trigger level or the block time expires.


**Parameters:**

+ `xBufferSizeBytes`

  The size, in bytes, of the buffer pointed to by the pucStreamBufferStorageArea parameter.

+ `xTriggerLevelBytes`

  The number of bytes that must be in the stream batching buffer to unblock a task 
  calling `xStreamBufferReceive` before the block time expires.

+ `pucStreamBufferStorageArea`

  Must point to a `uint8_t` array that is at least `xBufferSizeBytes` big. This is the array to which 
  streams are copied when they are written to the stream batching buffer.

+ `pxStaticStreamBuffer`

  Must point to a variable of type `StaticStreamBuffer_t`, which will be used to hold the stream batching 
  buffer's data structure.

+ `pxSendCompletedCallback`

  The callback invoked when a number of bytes at least equal to the trigger level are sent to the stream 
  batching buffer. If the parameter is NULL, it will use the default implementation provided by 
  the `sbSEND_COMPLETED` macro. To enable the callback, `configUSE_SB_COMPLETED_CALLBACK` must be set to 1 
  in FreeRTOSConfig.h. The send completed callback function must have the prototype defined 
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

+ If the stream batching buffer is created successfully, then a handle to the created stream batching 
  buffer is returned. 

+ If either `ppucStreamBufferStorageArea` or `ppxStaticStreamBuffer` are NULL, then NULL is returned.


**Example use:**

```c
// Used to dimension the array used to hold the streams.  The available space
// will actually be one less than this, so 999.
#define STORAGE_SIZE_BYTES 1000
 
// Defines the memory that will actually hold the streams within the stream
// batching buffer.
static uint8_t ucStorageBuffer[ STORAGE_SIZE_BYTES ];
 
// The variable used to hold the stream batching buffer structure.
StaticStreamBuffer_t xStreamBufferStruct;
 
void MyFunction( void )
{
StreamBufferHandle_t xStreamBatchingBuffer;
const size_t xTriggerLevel = 1;
 
    xStreamBatchingBuffer = xStreamBatchingBufferCreateStatic( sizeof( ucStorageBuffer ),
                                                               xTriggerLevel,
                                                               ucStorageBuffer,
                                                               &xStreamBufferStruct );
 
    // As neither the pucStreamBufferStorageArea or pxStaticStreamBuffer
    // parameters were NULL, xStreamBatchingBuffer will not be NULL, and can be
    // used to reference the created stream batching buffer in other stream
    // buffer API calls.
 
    // Other code that uses the stream batching buffer can go here.
}
```

