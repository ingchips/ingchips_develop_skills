[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
BaseType_t xQueueReceiveFromISR(
                                 QueueHandle_t xQueue,
                                 void *pvBuffer,
                                 BaseType_t *pxHigherPriorityTaskWoken
                               );
```

Receive an item from a queue. It is safe to use this function from within an interrupt service routine.


**Parameters:**

- *xQueue*

  The handle to the queue from which the item is to be received.

- *pvBuffer* 

  Pointer to the buffer into which the received item will be copied. 

- *pxHigherPriorityTaskWoken*

  A task may be blocked waiting for space to become available on the queue. If `xQueueReceiveFromISR` causes 
  such a task to unblock `*pxHigherPriorityTaskWoken` will get set to `pdTRUE`, otherwise `*pxHigherPriorityTaskWoken` 
  will remain unchanged. From FreeRTOS V7.3.0 `pxHigherPriorityTaskWoken` is an optional parameter and 
  can be set to NULL.


**Returns:**

- *pdPASS* if an item was successfully received from the queue,
- *pdFAIL* otherwise.


**Example usage:** 

```c
QueueHandle_t xQueue;

/* Function to create a queue and post some values. */
void vAFunction( void *pvParameters )
{
    char cValueToPost;
    const TickType_t xTicksToWait = ( TickType_t )0xff;

    /* Create a queue capable of containing 10 characters. */
    xQueue = xQueueCreate( 10, sizeof( char ) );
    if( xQueue == 0 )
    {
        /* Failed to create the queue. */
    }

    /* ... */

    /* Post some characters that will be used within an ISR. If the queue
       is full then this task will block for xTicksToWait ticks. */
    cValueToPost = 'a';
    xQueueSend( xQueue, ( void * ) &cValueToPost, xTicksToWait );
    cValueToPost = 'b';
    xQueueSend( xQueue, ( void * ) &cValueToPost, xTicksToWait );

    /* ... keep posting characters ... this task may block when the queue
       becomes full. */

    cValueToPost = 'c';
    xQueueSend( xQueue, ( void * ) &cValueToPost, xTicksToWait );
}

/* ISR that outputs all the characters received on the queue. */
void vISR_Routine( void )
{
BaseType_t xTaskWokenByReceive = pdFALSE;
char cRxedChar;

    while( xQueueReceiveFromISR( xQueue,
                                ( void * ) &cRxedChar,
                                &xTaskWokenByReceive) )
    {
        /* A character was received. Output the character now. */
        vOutputCharacter( cRxedChar );

        /* If removing the character from the queue woke the task that was
           posting onto the queue xTaskWokenByReceive will have been set to
           pdTRUE. No matter how many times this loop iterates only one
           task will be woken. */
    }

    if( xTaskWokenByReceive != pdFALSE )
    {
        /* We should switch context so the ISR returns to a different task.
           NOTE: How this is done depends on the port you are using. Check
           the documentation and examples for your port. */
        taskYIELD ();
    }
}
```
  
