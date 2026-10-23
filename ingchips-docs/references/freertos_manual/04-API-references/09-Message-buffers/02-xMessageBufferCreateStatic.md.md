# xMessageBufferCreateStatic, xMessageBufferCreateStaticWithCallback

[[RTOS Message Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message\_buffer.h

```c
MessageBufferHandle_t xMessageBufferCreateStatic(
                          size_t xBufferSizeBytes,
                          uint8_t *pucMessageBufferStorageArea,
                          StaticMessageBuffer_t *pxStaticMessageBuffer );

MessageBufferHandle_t xMessageBufferCreateStaticWithCallback(
                          size_t xBufferSizeBytes,
                          uint8_t *pucMessageBufferStorageArea,
                          StaticMessageBuffer_t *pxStaticMessageBuffer,
                          StreamBufferCallbackFunction_t pxSendCompletedCallback,
                          StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

Creates a new [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) using statically allocated memory. Message
buffers execute a callback upon completion of each send and receive operation. Message buffers created using
xMessageBufferCreateStatic() API share the same send and receive completed callback functions, which are
defined using the sbSEND\_COMPLETED() and sbRECEIVE\_COMPLETED() macros. Message buffers created using the
xMessageBufferCreateStaticWithCallback() API can each have their own unique send and receive completed
callback functions. See [xMessageBufferCreate() and xMessageBufferCreateWithCallback()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/01-xMessageBufferCreate)
for corresponding versions that use dynamically allocated memory.

[configSUPPORT\_STATIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) must be set to 1 in FreeRTOSConfig.h
for xMessageBufferCreateStatic() to be available. Additionally, configUSE\_SB\_COMPLETED\_CALLBACK must be set
to 1 in FreeRTOSConfig.h for xMessageBufferCreateStaticWithCallback() to be available.

Message buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c source file in
the build (as message buffers use stream buffers).


**Parameters:**

- *xBufferSizeBytes*

  The size, in bytes, of the buffer pointed to by the pucMessageBufferStorageArea parameter. When a message is written to the
  message buffer an additional sizeof( size\_t ) bytes are also written to store the message's length. sizeof( size\_t ) is
  typically 4 bytes on a 32-bit architecture, so on most 32-bit architecture a 10 byte message will take up 14 bytes of message
  buffer space. The maximum number of bytes that can be stored in the message buffer is actually (xBufferSizeBytes - 1).

- *pucMessageBufferStorageArea*

  Must point to a uint8\_t array that is at least xBufferSizeBytes big. This is the array to which messages are copied when
  they are written to the message buffer.

- *pxStaticMessageBuffer*

  Must point to a variable of type StaticMessageBuffer\_t, which will be used to hold the message buffer's data structure.

- *pxSendCompletedCallback*

  The callback function invoked when a message is written to the message buffer. If the parameter is NULL, the default
  implementation provided by the sbSEND\_COMPLETED macro is used. The send completed callback function must have the
  prototype defined by StreamBufferCallbackFunction\_t, which is:

  ```c
  void vSendCallbackFunction( MessageBufferHandle_t xMessageBuffer,
                              BaseType_t xIsInsideISR,
                              BaseType_t * const pxHigherPriorityTaskWoken );
  ```

- *pxReceiveCompletedCallback*

  The callback function invoked when a message is read from a message buffer. If the parameter is NULL, the default
  implementation provided by the sbRECEIVE\_COMPLETED macro is used. The receive completed callback function must
  have the prototype defined by StreamBufferCallbackFunction\_t, which is:

  ```c
  void vReceiveCallbackFunction( MessageBufferHandle_t xMessageBuffer,
                                 BaseType_t xIsInsideISR,
                                 BaseType_t * const pxHigherPriorityTaskWoken );
  ```

**Returns:**

If the message buffer is created successfully, then a handle to the created message buffer is returned. If either
pucMessageBufferStorageArea or pxStaticMessageBuffer are NULL then NULL is returned.


**Example usage:**

```c
/* Used to dimension the array used to hold the messages. The available
 * space will actually be one less than this, so 999. */
#define STORAGE_SIZE_BYTES 1000

/* Defines the memory that will actually hold the messages within the message
 * buffer. Should be one more than the value passed in the xBufferSizeBytes
 * parameter. */
static uint8_t ucMessageBufferStorage[ STORAGE_SIZE_BYTES ];
static uint8_t ucMessageBufferWithCallbackStorage[ STORAGE_SIZE_BYTES ];

/* The variable used to hold the message buffer structure. */
StaticMessageBuffer_t xMessageBufferStruct;
StaticMessageBuffer_t xMessageBufferWithCallbackStruct;

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

void MyFunction( void )
{
MessageBufferHandle_t xMessageBuffer, xMessageBufferWithCallback;

    /* Create a message buffer that uses the functions defined
     * using the sbSEND_COMPLETED() and sbRECEIVE_COMPLETED()
     * macros as send and receive completed callback functions. */
    xMessageBuffer = xMessageBufferCreateStatic( sizeof( ucMessageBufferStorage ),
                                                 ucMessageBufferStorage,
                                                 &xMessageBufferStruct );


    /* Create a message buffer that uses the functions
     * vSendCallbackFunction and vReceiveCallbackFunction as send
     * and receive completed callback functions. */
    xMessageBufferWithCallback = xMessageBufferCreateStaticWithCallback(
                                     sizeof( ucMessageBufferWithCallbackStorage ),
                                     ucMessageBufferWithCallbackStorage,
                                     &xMessageBufferWithCallbackStruct,
                                     vSendCallbackFunction,
                                     vReceiveCallbackFunction );

    /* As neither the pucMessageBufferStorageArea or pxStaticMessageBuffer
     * parameters were NULL, xMessageBuffer and xMessageBufferWithCallback
     * will not be NULL, and can be used to reference the created message
     * buffers in other message buffer API calls. */

    /* Other code that uses the message buffers can go here. */
}
```
