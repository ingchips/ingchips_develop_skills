# xMessageBufferCreate, xMessageBufferCreateWithCallback

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
MessageBufferHandle_t xMessageBufferCreate( size_t xBufferSizeBytes );

MessageBufferHandle_t xMessageBufferCreateWithCallback( 
                          size_t xBufferSizeBytes,
                          StreamBufferCallbackFunction_t pxSendCompletedCallback,
                          StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

Creates a new [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) that uses dynamically allocated memory. Message 
buffers execute a callback upon completion of each send and receive operation. Message buffers created using 
the `xMessageBufferCreate()` API share the same send and receive completed callback functions, which are 
defined using the `sbSEND_COMPLETED()` and `sbRECEIVE_COMPLETED()` macros. Message buffers created using 
the `xMessageBufferCreateWithCallback()` API can each have their own unique send and receive completed callback 
functions. See `xMessageBufferCreateStatic()` and `xMessageBufferCreateStaticWithCallback()` for corresponding 
versions that use statically allocated memory (memory that is allocated at compile time).

[configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set to 1 or left 
undefined in FreeRTOSConfig.h for `xMessageBufferCreate()` to be available. Additionally, `configUSE_SB_COMPLETED_CALLBACK` 
must be set to 1 in FreeRTOSConfig.h for `xMessageBufferCreateWithCallback()` to be available.

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c source file in the 
build (as message buffers use stream buffers).


**Parameters:**

- *xBufferSizeBytes*

  The total number of bytes (not messages) the message buffer will be able to hold at any one time. When a message is written 
  to the message buffer an additional `sizeof( size_t )` bytes are also written to store the message's length. `sizeof( size_t )` 
  is typically 4 bytes on a 32-bit architecture, so on most 32-bit architectures a 10 byte message will take up 14 bytes of 
  message buffer space.
  
- *pxSendCompletedCallback*

  The callback function invoked when a message is written to the message buffer. If the parameter is NULL, the default 
  implementation provided by the `sbSEND_COMPLETED` macro is used. The send completed callback function must have the prototype
  defined by `StreamBufferCallbackFunction_t`, which is:
 
  ```c
  void vSendCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                              BaseType_t xIsInsideISR,  
                              BaseType_t * const pxHigherPriorityTaskWoken );  
  ```

- *pxReceiveCompletedCallback*

  The callback function invoked when a message is read from a message buffer. If the parameter is NULL, the default 
  implementation provided by the `sbRECEIVE_COMPLETED` macro is used. The receive completed callback function must have the 
  prototype defined by `StreamBufferCallbackFunction_t`, which is:
 
  ```c
  void vReceiveCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                                 BaseType_t xIsInsideISR,  
                                 BaseType_t * const pxHigherPriorityTaskWoken );  
  ```


**Returns:**

- If NULL is returned, then the message buffer cannot be created because there is insufficient heap memory available for FreeRTOS 
  to allocate the message buffer data structures and storage area. 
  
- A non-NULL value being returned indicates that the message 
  buffer has been created successfully - the returned value should be stored as the handle to the created message buffer.


**Example usage:**

```c
void vSendCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                            BaseType_t xIsInsideISR,  
                            BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when a message is written to  
     * the message buffer.  
     * This is useful when a message buffer is used to pass messages between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xMessageBufferSendCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting for message. */  
}  

  
void vReceiveCallbackFunction( MessageBufferHandle_t xMessageBuffer,  
                               BaseType_t xIsInsideISR,  
                               BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when a message is read from a message  
     * buffer.  
     * This is useful when a message buffer is used to pass messages between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xMessageBufferReceiveCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting to send message. */  
}  

  
void vAFunction( void )  
{  
    MessageBufferHandle_t xMessageBuffer, xMessageBufferWithCallback;  
    const size_t xMessageBufferSizeBytes = 100;  

    /* Create a message buffer that can hold 100 bytes and uses the  
     * functions defined using the sbSEND_COMPLETED() and  
     * sbRECEIVE_COMPLETED() macros as send and receive completed  
     * callback functions. The memory used to hold both the message  
     * buffer structure and the data in the message buffer is  
     * allocated dynamically. */  
    xMessageBuffer = xMessageBufferCreate( xMessageBufferSizeBytes );  

    if( xMessageBuffer == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
         * message buffer. */  
    }  
    else  
    {  
        /* The message buffer was created successfully and can now be used. */  
    }  

    /* Create a message buffer that can hold 100 bytes and uses the  
     * functions vSendCallbackFunction and vReceiveCallbackFunction  
     * as send and receive completed callback functions. The memory  
     * used to hold both the message buffer structure and the data  
     * in the message buffer is allocated dynamically. */  
    xMessageBufferWithCallback = xMessageBufferCreateWithCallback(   
                                     xMessageBufferSizeBytes,  
                                     vSendCallbackFunction,  
                                     vReceiveCallbackFunction );  

    if( xMessageBufferWithCallback == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
         * message buffer. */  
    }  
    else  
    {  
        /* The message buffer was created successfully and can now be used. */  
    }  
}  
```
