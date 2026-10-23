[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
 BaseType_t xQueueSend(
                        QueueHandle_t xQueue,
                        const void * pvItemToQueue,
                        TickType_t xTicksToWait
                      );
```

This is a macro that calls `xQueueGenericSend()`. It is included for backward compatibility with versions 
of FreeRTOS that did not include the `xQueueSendToFront()` and `xQueueSendToBack()` macros. It is
equivalent to `xQueueSendToBack()`.

Post an item on a queue. The item is queued by copy, not by reference. This function must not be called 
from an interrupt service routine. See `xQueueSendFromISR()` for an alternative which may be used in an ISR.


**Parameters:**
 
- *xQueue*

  The handle to the queue on which the item is to be posted.

- *pvItemToQueue*

  A pointer to the item that is to be placed on the queue. The size of the items the queue will hold was 
  defined when the queue was created, so this many bytes will be copied from `pvItemToQueue` into the queue 
  storage area.

- *xTicksToWait*

  The maximum amount of time the task should block waiting for space to become available on the queue, 
  should it already be full. The call will return immediately if the queue is full and `xTicksToWait` is 
  set to 0. The time is defined in tick periods so the constant `portTICK_PERIOD_MS` should be used to 
  convert to real time if this is required. 

  If [INCLUDE\_vTaskSuspend](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) is set to '1' then specifying the block time as `portMAX_DELAY` 
  will cause the task to block indefinitely (without a timeout).


**Returns:**

- *pdPASS* if the item was successfully posted, 
- *errQUEUE\_FULL* otherwise.


**Example usage:**

```c
struct AMessage
 {
    char ucMessageID;
    char ucData[ 20 ];
 } xMessage;

 unsigned long ulVar = 10UL;

 void vATask( void *pvParameters )
 {
 QueueHandle_t xQueue1, xQueue2;
 struct AMessage *pxMessage;

    /* Create a queue capable of containing 10 unsigned long values. */
    xQueue1 = xQueueCreate( 10, sizeof( unsigned long ) );

    /* Create a queue capable of containing 10 pointers to AMessage structures.
       These should be passed by pointer as they contain a lot of data. */
    xQueue2 = xQueueCreate( 10, sizeof( struct AMessage * ) );

    /* ... */

    if( xQueue1 != 0 )
    {
        /* Send an unsigned long. Wait for 10 ticks for space to become
           available if necessary. */
        if( xQueueSend( xQueue1,
                       ( void * ) &ulVar,
                       ( TickType_t ) 10 ) != pdPASS )
        {
            /* Failed to post the message, even after 10 ticks. */
        }
    }

    if( xQueue2 != 0 )
    {
        /* Send a pointer to a struct AMessage object. Don't block if the
           queue is already full. */
        pxMessage = & xMessage;
        xQueueSend( xQueue2, ( void * ) &pxMessage, ( TickType_t ) 0 );
    }

	/* ... Rest of task code. */
 }
```
