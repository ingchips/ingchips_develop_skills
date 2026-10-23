# xStreamBufferCreate, xStreamBufferCreateWithCallback

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

  
stream\_buffer.h

```c
StreamBufferHandle_t xStreamBufferCreate( size_t xBufferSizeBytes,
                                           size_t xTriggerLevelBytes );

StreamBufferHandle_t xStreamBufferCreateWithCallback( 
                         size_t xBufferSizeBytes,
                         size_t xTriggerLevelBytes
                         StreamBufferCallbackFunction_t pxSendCompletedCallback,
                         StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

Creates a new [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) that uses dynamically allocated memory. 
Stream buffers execute a callback upon completion of each send and receive operation. Stream buffers 
created using the xStreamBufferCreate() API share the same send and receive completed callback functions, 
which are defined using the sbSEND\_COMPLETED() and sbRECEIVE\_COMPLETED() macros. Stream buffers created 
using the xStreamBufferCreateWithCallback() API can each have their own unique send and receive completed 
callback functions. See [xStreamBufferCreateStatic() and xStreamBufferCreateStaticWithCallback()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/02-xStreamBufferCreateStatic) 
for corresponding versions that use statically allocated memory (memory that is allocated at compile time).

[configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set to 1 or left undefined 
in FreeRTOSConfig.h for xStreamBufferCreate() to be available. 
Additionally, [configUSE\_SB\_COMPLETED\_CALLBACK](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set to 1 in 
FreeRTOSConfig.h for xStreamBufferCreateWithCallback() to be available.

Enable stream buffer functionality by including the FreeRTOS/source/stream\_buffer.c source file in the build.


**Parameters:**

+ *xBufferSizeBytes*

  The total number of bytes the stream buffer will be able to hold at any one time.

+ *xTriggerLevelBytes*

  The number of bytes that must be in the stream buffer before a task that is blocked on the stream buffer 
  to wait for data is moved out of the blocked state. For example, if a task is blocked on a read of an empty 
  stream buffer that has a trigger level of 1, then the task will be unblocked when a single byte is written 
  to the buffer or the task's block time expires. As another example, if a task is blocked on a read of an 
  empty stream buffer that has a trigger level of 10, then the task will not be unblocked until the stream 
  buffer contains at least 10 bytes or the task's block time expires. If a reading task's block time expires 
  before the trigger level is reached then the task will still receive as many bytes as are actually available. 
  Setting a trigger level of 0 will result in a trigger level of 1 being used. It is not valid to specify 
   a trigger level that is greater than the buffer size.

+ *pxSendCompletedCallback*

  The callback function invoked when a data write to the stream buffer causes the number of bytes in 
  the buffer to be more than the trigger level. If the parameter is NULL, the default implementation provided 
  by the sbSEND\_COMPLETED macro is used. The send completed callback function must have the prototype defined 
  by StreamBufferCallbackFunction\_t, which is:
 
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

If NULL is returned, the stream buffer cannot be created because there is insufficient heap memory available 
for FreeRTOS to allocate the stream buffer data structures and storage area. If a non-NULL value is returned, 
the stream buffer has been created successfully - the returned value should be stored as the handle to the 
created stream buffer.


**Example usage:**

```c
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

void vAFunction( void )  
{  
StreamBufferHandle_t xStreamBuffer, xStreamBufferWithCallback;  
const size_t xStreamBufferSizeBytes = 100, xTriggerLevel = 10;  
  
    /* Create a stream buffer that can hold 100 bytes and uses the  
     * functions defined using the sbSEND_COMPLETED() and  
     * sbRECEIVE_COMPLETED() macros as send and receive completed  
     * callback functions. The memory used to hold both the stream  
     * buffer structure and the data in the stream buffer is  
     * allocated dynamically. */  
    xStreamBuffer = xStreamBufferCreate( xStreamBufferSizeBytes,  
                                         xTriggerLevel );  

    if( xStreamBuffer == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
           stream buffer. */  
    }  
    else  
    {  
        /* The stream buffer was created successfully and can now be used. */  
    }  
      
    /* Create a stream buffer that can hold 100 bytes and uses the  
     * functions vSendCallbackFunction and vReceiveCallbackFunction  
     * as send and receive completed callback functions. The memory  
     * used to hold both the stream buffer structure and the data  
     * in the stream buffer is allocated dynamically. */  
    xStreamBufferWithCallback = xStreamBufferCreateWithCallback(   
                                    xStreamBufferSizeBytes,  
                                    xTriggerLevel,  
                                    vSendCallbackFunction,  
                                    vReceiveCallbackFunction );  

    if( xStreamBufferWithCallback == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
         * stream buffer. */  
    }  
    else  
    {  
        /* The stream buffer was created successfully and can now be used. */  
    }  
}  
```
