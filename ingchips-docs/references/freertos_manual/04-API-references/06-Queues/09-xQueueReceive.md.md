[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
BaseType_t xQueueReceive(
                          QueueHandle_t xQueue,
                          void *pvBuffer,
                          TickType_t xTicksToWait
);
```
 
This is a macro that calls the `xQueueGenericReceive()` function.

Receive an item from a queue. The item is received by copy so a buffer of adequate size must be provided. 
The number of bytes copied into the buffer was defined when the queue was created.

This function must not be used in an interrupt service routine. See xQueueReceiveFromISR for an alternative 
that can.

**Parameters:**

- *xQueue*

  The handle to the queue from which the item is to be received.
  
- *pvBuffer*

  Pointer to the buffer into which the received item will be copied.
  
- *xTicksToWait*

  The maximum amount of time the task should block waiting for an item to receive should the queue be 
  empty at the time of the call. Setting `xTicksToWait` to 0 will cause the function to return immediately 
  if the queue is empty. The time is defined in tick periods so the constant `portTICK_PERIOD_MS` should 
  be used to convert to real time if this is required. If [INCLUDE\_vTaskSuspend](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) is set to '1' 
  then specifying the block time as `portMAX_DELAY` will cause the task to block indefinitely (without 
  a timeout).


**Returns:**

- *pdPASS* if an item was successfully received from the queue, 
- *errQUEUE\_EMPTY* otherwise.


**Example usage:**

```c
/* Define a variable of type struct AMMessage. The examples below demonstrate
   how to pass the whole variable through the queue, and as the structure is
   moderately large, also how to pass a reference to the variable through a queue. */
struct AMessage
{
    char ucMessageID;
    char ucData[ 20 ];
} xMessage;

/* Queue used to send and receive complete struct AMessage structures. */
QueueHandle_t xStructQueue = NULL;

/* Queue used to send and receive pointers to struct AMessage structures. */
QueueHandle_t xPointerQueue = NULL;

void vCreateQueues( void )
{
    xMessage.ucMessageID = 0xab;
    memset( &( xMessage.ucData ), 0x12, 20 );
    
    /* Create the queue used to send complete struct AMessage structures. This can
       also be created after the schedule starts, but care must be task to ensure
       nothing uses the queue until after it has been created. */
    xStructQueue = xQueueCreate(
        /* The number of items the queue can hold. */
        10,
        /* Size of each item is big enough to hold the<br /> whole structure. */
        sizeof( xMessage ) );
        
    /* Create the queue used to send pointers to struct AMessage structures. */
    xPointerQueue = xQueueCreate(
        /* The number of items the queue can hold. */
        10,
        /* Size of each item is big enough to hold only a pointer. */
        sizeof( &xMessage ) );
                          
    if( ( xStructQueue == NULL ) || ( xPointerQueue == NULL ) )
    {
        /* One or more queues were not created successfully as there was not enough
           heap memory available. Handle the error here. Queues can also be created
           statically. */
    }
}

/* Task that writes to the queues. */
void vATask( void *pvParameters )
{
    struct AMessage *pxPointerToxMessage;
    
    /* Send the entire structure to the queue created to hold 10 structures. */
    xQueueSend( /* The handle of the queue. */
                xStructQueue,
                /* The address of the xMessage variable. sizeof( struct AMessage )
                    bytes are copied from here into the queue. */
                ( void * ) &xMessage,
                /* Block time of 0 says don't block if the queue is already full.
                   Check the value returned by xQueueSend() to know if the message
                   was sent to the queue successfully. */
                ( TickType_t ) 0 );
                             
    /* Store the address of the xMessage variable in a pointer variable. */
    pxPointerToxMessage = &xMessage;
    
    /* Send the address of xMessage to the queue created to hold 10 pointers. */
    xQueueSend( /* The handle of the queue. */
                xPointerQueue,
                /* The address of the variable that holds the address of xMessage.
                   sizeof( &xMessage ) bytes are copied from here into the queue. As the
                   variable holds the address of xMessage it is the address of xMessage
                   that is copied into the queue. */
                ( void * ) &pxPointerToxMessage,
                ( TickType_t ) 0 );
                
    /* ... Rest of task code goes here. */
}

/* Task that reads from the queues. */
void vADifferentTask( void *pvParameters )
{
    struct AMessage xRxedStructure, *pxRxedPointer;
    
    if( xStructQueue != NULL )
    {
        /* Receive a message from the created queue to hold complex struct AMessage
           structure. Block for 10 ticks if a message is not immediately available.
           The value is read into a struct AMessage variable, so after calling
           xQueueReceive() xRxedStructure will hold a copy of xMessage. */
        if( xQueueReceive( xStructQueue,
                           &( xRxedStructure ),
                           ( TickType_t ) 10 ) == pdPASS )
        {
            /* xRxedStructure now contains a copy of xMessage. */
        }
    }
   
    if( xPointerQueue != NULL )
    {
        /* Receive a message from the created queue to hold pointers. Block for 10
           ticks if a message is not immediately available. The value is read into a
           pointer variable, and as the value received is the address of the xMessage
           variable, after this call pxRxedPointer will point to xMessage. */
        if( xQueueReceive( xPointerQueue,
                          &( pxRxedPointer ),
                          ( TickType_t ) 10 ) == pdPASS )
        {
            /* *pxRxedPointer now points to xMessage. */
        }
    }
   
    /* ... Rest of task code goes here. */
}   
```
*A demonstration of how to send and receive structures and pointers to structures*
