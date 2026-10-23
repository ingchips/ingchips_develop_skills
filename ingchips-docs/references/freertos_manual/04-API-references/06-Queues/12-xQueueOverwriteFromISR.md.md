# xQueueOverwriteFromISR

[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
BaseType_t xQueueOverwrite(
                           QueueHandle_t xQueue,
                           const void * pvItemToQueue,
                           BaseType_t *pxHigherPriorityTaskWoken
                          );
```
 
This is a macro that calls the xQueueGenericSendFromISR() function.

A version of [xQueueOverwrite()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite) that can
be used in an ISR. xQueueOverwriteFromISR() is similar to xQueueSendToBackFromISR(),
but will write to the queue even if the queue is full, overwriting data that is already
held in the queue.

xQueueOverwriteFromISR() is intended for use with queues that have a length of one,
meaning the queue is either empty or full.


**Parameters:**

+ *xQueue*  

  The handle of the queue to which the data is to be sent.

+ *pvItemToQueue*  

  A pointer to the item that is to be placed in the queue. The size of the items the queue will hold 
  was defined when the [queue was created](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate), and that many bytes will be copied from 
  pvItemToQueue into the queue storage area.

+ *pxHigherPriorityTaskWoken*  

  xQueueOverwriteFromISR() will set *pxHigherPriorityTaskWoken to pdTRUE if sending to the queue caused a 
  task to unblock, and the unblocked task has a priority higher than the currently running task. If 
  xQueueOverwriteFromISR() sets this value to pdTRUE then a context switch should be requested before 
  the interrupt is exited. Refer to the Interrupt Service Routines section of the documentation for the 
  port being used to see how that is done.

**Returns:** 

xQueueOverwriteFromISR() is a macro that calls xQueueGenericSendFromISR(), and
therefore has the same return values as
xQueueSendToFrontFromISR(). However, pdPASS is the only value that can be
returned because xQueueOverwriteFromISR() will write to the queue even when
the queue is already full.
 

**Example usage:**

```c
QueueHandle_t xQueue;

void vFunction( void *pvParameters )
{
    /* Create a queue to hold one unsigned long value. It is strongly
       recommended **not** to use xQueueOverwriteFromISR() on queues that can
       contain more than one value, and doing so will trigger an assertion
       if configASSERT() is defined. */
    xQueue = xQueueCreate( 1, sizeof( unsigned long ) );
}

void vAnInterruptHandler( void )
{
/* xHigherPriorityTaskWoken must be set to pdFALSE before it is used. */
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
unsigned long ulVarToSend, ulValReceived;

    /* Write the value 10 to the queue using xQueueOverwriteFromISR(). */
    ulVarToSend = 10;
    xQueueOverwriteFromISR( xQueue, &ulVarToSend, &xHigherPriorityTaskWoken );

    /* The queue is full, but calling xQueueOverwriteFromISR() again will still
       pass because the value held in the queue will be overwritten with the
       new value. */
    ulVarToSend = 100;
    xQueueOverwriteFromISR( xQueue, &ulVarToSend, &xHigherPriorityTaskWoken );

    /* Reading from the queue will now return 100. */

    /* ... */

    if( xHigherPrioritytaskWoken == pdTRUE )
    {
        /* Writing to the queue caused a task to unblock and the unblocked task
           has a priority higher than or equal to the priority of the currently
           executing task (the task this interrupt interrupted). Perform a
           context switch so this interrupt returns directly to the unblocked
           task. */
        portYIELD_FROM_ISR(); /* or portEND_SWITCHING_ISR() depending on the
                                 port.*/
    }
}
```
