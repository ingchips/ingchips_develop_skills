[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
 BaseType_t xQueueOverwrite(
 QueueHandle_t xQueue,
 const void * pvItemToQueue
 );
```
 
This is a macro that calls the xQueueGenericSend() function.

A version of [xQueueSendToBack()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/05-xQueueSendToBack) that will 
write to the queue even if the queue is full, overwriting data that is already 
held in the queue.

xQueueOverwrite() is intended for use with queues that have a length of one, 
meaning the queue is either empty or full.

This function must not be called from an interrupt service routine (ISR).
See xQueueOverwriteFromISR() for an alternative which may be used in an ISR.

If the application uses xQueueOverwrite to write to a queue which is already 
full and the queue happens to be a member of queue set, the queue handle will 
not be returned from xQueueSetSelect as the number of items in the queue does 
not change.


**Parameters:**

+ *xQueue*  

  The handle of the queue to which the data is to be sent.

+ *pvItemToQueue*  

  A pointer to the item that is to be placed in the queue. The size of the items the queue will hold was 
  defined when the [queue was created](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate), and that many bytes will be copied from pvItemToQueue 
  into the queue storage area.


**Returns:** 

xQueueOverwrite() is a macro that calls xQueueGenericSend(), and
therefore has the same return values as 
xQueueSendToFront(). However, pdPASS is the only value that can be
returned because xQueueOverwrite() will write to the queue even when
the queue was already full.
 

**Example usage:**

```c
void vFunction( void *pvParameters )
{
QueueHandle_t xQueue;
unsigned long ulVarToSend, ulValReceived;

   /* Create a queue to hold one unsigned long value. It is strongly
      recommended *not* to use xQueueOverwrite() on queues that can
      contain more than one value, and doing so will trigger an assertion
if configASSERT() is defined. */
    xQueue = xQueueCreate( 1, sizeof( unsigned long ) );

    /* Write the value 10 to the queue using xQueueOverwrite(). */
    ulVarToSend = 10;
    xQueueOverwrite( xQueue, &ulVarToSend );

    /* Peeking the queue should now return 10, but leave the value 10 in
       the queue. A block time of zero is used as it is known that the
       queue holds a value. */
    ulValReceived = 0;
    xQueuePeek( xQueue, &ulValReceived, 0 );

    if( ulValReceived != 10 )
    {
        /* Error, unless another task removed the value. */
    }

    /* The queue is still full. Use xQueueOverwrite() to overwrite the
       value held in the queue with 100. */
    ulVarToSend = 100;
    xQueueOverwrite( xQueue, &ulVarToSend );

    /* This time read from the queue, leaving the queue empty once more.
       A block time of 0 is used again. */
    xQueueReceive( xQueue, &ulValReceived, 0 );

    /* The value read should be the last value written, even though the
       queue was already full when the value was written. */
    if( ulValReceived != 100 )
    {
        /* Error unless another task is using the same queue. */
    }

    /* ... */
}
```
