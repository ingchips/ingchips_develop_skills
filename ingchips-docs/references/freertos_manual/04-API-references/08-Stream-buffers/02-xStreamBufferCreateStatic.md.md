# xStreamBufferCreateStatic, xStreamBufferCreateStaticWithCallback

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
StreamBufferHandle_t xStreamBufferCreateStatic(
                                    size_t xBufferSizeBytes,
                                    size_t xTriggerLevelBytes,
                                    uint8_t *pucStreamBufferStorageArea,
                                    StaticStreamBuffer_t *pxStaticStreamBuffer );

StreamBufferHandle_t xStreamBufferCreateStaticWithCallback(
                                    size_t xBufferSizeBytes,
                                    size_t xTriggerLevelBytes,
                                    uint8_t *pucStreamBufferStorageArea,
                                    StaticStreamBuffer_t *pxStaticStreamBuffer,
                                    StreamBufferCallbackFunction_t pxSendCompletedCallback,
                                    StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

Creates a new [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) using statically allocated memory. Stream 
buffers execute a callback upon completion of each send and receive operation. Stream buffers created 
using the xStreamBufferCreateStatic() API share the same send and receive completed callback functions, 
which are defined using the sbSEND\_COMPLETED() and sbRECEIVE\_COMPLETED() macros. Stream buffers created 
using xStreamBufferCreateStaticWithCallback() API can each have their own unique send and receive 
completed callback functions. See [xStreamBufferCreate() and xStreamBufferCreateWithCallback()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/01-xStreamBufferCreate) 
for corresponding versions that use dynamically allocated memory.

[configSUPPORT\_STATIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set to 1 in FreeRTOSConfig.h 
for xStreamBufferCreateStatic() to be available. Additionally, [configUSE\_SB\_COMPLETED\_CALLBACK](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
must be set to 1 in FreeRTOSConfig.h for xStreamBufferCreateStaticWithCallback() to be available.

Enable stream buffer functionality by including the FreeRTOS/source/stream\_buffer.c source file in the build.


**Parameters:**

+ *xBufferSizeBytes*

  The total number of bytes the stream buffer will be able to hold at any one time.

+ *xTriggerLevelBytes*

  The number of bytes that must be in the stream buffer before a task that is blocked on the stream buffer 
  waiting for data is moved out of the blocked state. For example, if a task is blocked on a read of an 
  empty stream buffer that has a trigger level of 1 then the task will be unblocked when a single byte is 
  written to the buffer or the task's block time expires. As another example, if a task is blocked on a 
  read of an empty stream buffer that has a trigger level of 10, then the task will not be unblocked until 
  the stream buffer contains at least 10 bytes or the task's block time expires. If a reading task's block 
  time expires before the trigger level is reached, then the task will still receive as many bytes as are 
  actually available. Setting a trigger level of 0 will result in a trigger level of 1 being used. It is 
  not valid to specify a trigger level that is greater than the buffer size.

+ *pucStreamBufferStorageArea*

  Must point to a uint8\_t array that is at least xBufferSizeBytes + 1 big. This is the array to which 
  streams are copied when they are written to the stream buffer.

+ *pxStaticStreamBuffer*

  Must point to a variable of type StaticStreamBuffer\_t, which will be used to hold the stream buffer's 
  data structure.

+ *pxSendCompletedCallback*

  The callback function invoked when a data write to the stream buffer causes the number of bytes in the 
  buffer to be more than the trigger level. If the parameter is NULL, the default implementation provided 
  by the sbSEND\_COMPLETED macro is used. The send completed callback function must have the prototype 
  defined by StreamBufferCallbackFunction\_t, which is:
 
  ```c
  void vSendCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                              BaseType_t xIsInsideISR,  
                              BaseType_t * const pxHigherPriorityTaskWoken );  
  ```

+ *pxReceiveCompletedCallback*

  The callback function invoked when data (more than zero bytes) is read from a stream buffer. If the 
  parameter is NULL, the default implementation provided by the sbRECEIVE\_COMPLETED macro is used. The 
  receive completed callback function must have the prototype defined by StreamBufferCallbackFunction\_t, 
  which is:
 
  ```c
  void vReceiveCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                                 BaseType_t xIsInsideISR,  
                                 BaseType_t * const pxHigherPriorityTaskWoken );  
  ```


**Returns:**

If the stream buffer is created successfully, then a handle to the created stream buffer is returned. 
If either pucStreamBufferStorageArea or pxStaticstreamBuffer are NULL then NULL is returned.


**Example usage:**

```c
/* The total number of bytes the stream buffer will be able to hold at any one time. */  
#define STREAM_BUFFER_SIZE_BYTES 1000  
  
/* Defines the memory that will actually hold the streams within the  
 * stream buffer. Note that it needs to be of size (STREAM_BUFFER_SIZE_BYTES + 1). */  
static uint8_t ucStreamBufferStorage[ STREAM_BUFFER_SIZE_BYTES + 1 ];  
static uint8_t ucStreamBufferWithCallbackStorage[ STREAM_BUFFER_SIZE_BYTES + 1 ];  

/* The variable used to hold the stream buffer structure. */  
StaticStreamBuffer_t xStreamBufferStruct;  
StaticStreamBuffer_t xStreamBufferWithCallbackStruct;  

void vSendCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                            BaseType_t xIsInsideISR,  
                            BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when a data write operation  
     * to the stream buffer causes the number of bytes in the buffer  
     * to be more then the trigger level.  
     * This is useful when a stream buffer is used to pass data between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xStreamBufferSendCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting for the data. */  
}  

void vReceiveCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                               BaseType_t xIsInsideISR,  
                               BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when data is read from a stream  
     * buffer.  
     * This is useful when a stream buffer is used to pass data between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xStreamBufferReceiveCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting to send the data. */  
}  


void MyFunction( void )  
{  
StreamBufferHandle_t xStreamBuffer, xStreamBufferWithCallback;  
const size_t xTriggerLevel = 1;  
  
    /* Create a stream buffer that uses the functions defined  
     * using the sbSEND\COMPLETED() and sbRECEIVE_COMPLETED()  
     * macros as send and receive completed callback functions. */  
    xStreamBuffer = xStreamBufferCreateStatic( STREAM_BUFFER_SIZE_BYTES,  
                                               xTriggerLevel,  
                                               ucStreamBufferStorage,  
                                               &xStreamBufferStruct );  

    /* Create a stream buffer that uses the functions  
     * vSendCallbackFunction and vReceiveCallbackFunction as send  
     * and receive completed callback functions. */  
    xStreamBufferWithCallback = xStreamBufferCreateStaticWithCallback(  
                                    STREAM_BUFFER_SIZE_BYTES,  
                                    xTriggerLevel,  
                                    ucStreamBufferWithCallbackStorage,  
                                    &xStreamBufferWithCallbackStruct,  
                                    vSendCallbackFunction,  
                                    vReceiveCallbackFunction );  
  
    /* As neither the pucStreamBufferStorageArea or pxStaticStreamBuffer  
     * parameters were NULL, xStreamBuffer and xStreamBufferWithCallback  
     * will not be NULL, and can be used to reference the created stream  
     * buffers in other stream buffer API calls. */  

    /* Other code that uses the stream buffers can go here. */  
}  
```
