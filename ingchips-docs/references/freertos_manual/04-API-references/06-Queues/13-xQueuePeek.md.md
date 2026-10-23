[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h 

```c
 BaseType_t xQueuePeek(
 QueueHandle_t xQueue,
 void *pvBuffer,
 TickType_t xTicksToWait
 );
```
 
This is a macro that calls the xQueueGenericReceive() function.

Receive an item from a queue without removing the item from the queue.
The item is received by copy so a buffer of adequate size must be
provided. The number of bytes copied into the buffer was defined when
the queue was created.

Successfully received items remain on the queue so will be returned again
by the next call, or a call to xQueueReceive().

This macro must not be used in an interrupt service routine.


**Parameters:**

+ *xQueue* 

  The handle to the queue from which the item is to be received.

+ *pvBuffer* 

  Pointer to the buffer into which the received item will be copied. This must be at least large enough 
  to hold the size of the queue item defined when the queue was created.

+ *xTicksToWait* 

  The maximum amount of time the task should block waiting for an item to receive should the queue be 
  empty at the time of the call. The time is defined in tick periods so the constant portTICK\_PERIOD\_MS 
  should be used to convert to real time if this is required.<br /> If [INCLUDE\_vTaskSuspend](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
  is set to '1' then specifying the block time as portMAX\_DELAY will cause the task to block 
  indefinitely (without a timeout).


**Returns:**

pdPASS if an item was successfully received (peeked) from the queue, otherwise errQUEUE\_EMPTY.


**Example usage:** 

```c
struct AMessage
{
    char ucMessageID;
    char ucData[ 20 ];
} xMessage;

QueueHandle_t xQueue;

// Task to create a queue and post a value.
void vATask( void *pvParameters )
{
struct AMessage *pxMessage;

    // Create a queue capable of containing 10 pointers to AMessage structures.
    // These should be passed by pointer as they contain a lot of data.
    xQueue = xQueueCreate( 10, sizeof( struct AMessage * ) );
    if( xQueue == 0 )
    {
        // Failed to create the queue.
    }

    // ...

    // Send a pointer to a struct AMessage object.  Don't block if the
    // queue is already full.
    pxMessage = & xMessage;
    xQueueSend( xQueue, ( void * ) &pxMessage, ( TickType_t ) 0 );

    // ... Rest of task code.
}

// Task to peek the data from the queue.
void vADifferentTask( void *pvParameters )
{
struct AMessage *pxRxedMessage;

    if( xQueue != 0 )
    {
        // Peek a message on the created queue.  Block for 10 ticks if a
        // message is not immediately available.
        if( xQueuePeek( xQueue, &( pxRxedMessage ), ( TickType_t ) 10 ) )
        {
            // pcRxedMessage now points to the struct AMessage variable posted
            // by vATask, but the item still remains on the queue.
        }
    }

    // ... Rest of task code.
}
```
