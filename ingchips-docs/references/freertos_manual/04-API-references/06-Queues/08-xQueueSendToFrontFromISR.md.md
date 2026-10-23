[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h 

```c
BaseType_t xQueueSendToFrontFromISR(
                                    QueueHandle_t xQueue,
                                    const void *pvItemToQueue,
                                    BaseType_t *pxHigherPriorityTaskWoken
                                   );
```
 
This is a macro that calls xQueueGenericSendFromISR().

Post an item to the front of a queue. It is safe to use this function from within an interrupt service routine.

Items are queued by copy not reference so it is preferable to either only send small items, or alternatively 
send a pointer to the item.


**Parameters:**

+ *xQueue* 

  The handle to the queue on which the item is to be posted.

+ *pvItemToQueue* 

  A pointer to the item that is to be placed on the queue. The size of the items the queue will hold 
  was defined when the queue was created, so this many bytes will be copied from pvItemToQueue into the 
  queue storage area.

+ *pxHigherPriorityTaskWoken* 

  xQueueSendToFrontFromISR() will set *pxHigherPriorityTaskWoken to pdTRUE if sending to the queue caused 
  a task to unblock, and the unblocked task has a priority higher than the currently running task. If 
  xQueueSendToFrontFromISR() sets this value to pdTRUE then a context switch should be requested before 
  the interrupt is exited. From FreeRTOS V7.3.0 pxHigherPriorityTaskWoken is an optional parameter and 
  can be set to NULL.


**Returns:**

pdPass if data was successfully sent to the queue, otherwise errQUEUE\_FULL.


**Example usage:** 

```c
void vBufferISR( void )
{
char cIn;
BaseType_t xHigherPriorityTaskWoken;

    /* We have not woken a task at the start of the ISR. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Obtain a byte from the buffer. */
    cIn = portINPUT\_BYTE( RX\_REGISTER\_ADDRESS );

    if( cIn == EMERGENCY\_MESSAGE )
    {
        /* Post the byte to the front of the queue. */
        xQueueSendToFrontFromISR( xRxQueue, &cIn, &xHigherPriorityTaskWoken );
    }
    else
    {
        /* Post the byte to the back of the queue. */
        xQueueSendToBackFromISR( xRxQueue, &cIn, &xHigherPriorityTaskWoken );
    }

    /* Did sending to the queue unblock a higher priority task? */
    if( xHigherPriorityTaskWoken )
    {
        /* Actual macro used here is port specific. */
        taskYIELD\_FROM\_ISR ();
    }
}
```
