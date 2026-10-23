[[Queue Set API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

queue.h

```c
QueueSetHandle_t xQueueCreateSetStatic( const UBaseType_t uxEventQueueLength,
                                        uint8_t * pucQueueStorage,
                                        StaticQueue_t * pxStaticQueue );
```

configUSE\_QUEUE\_SETS and configSUPPORT\_STATIC\_ALLOCATION must be set to 1 in FreeRTOSConfig.h for the xQueueCreateSetStatic() API function to be available.

Creates a new queue set using statically allocated memory. Queue sets provide a mechanism to allow an RTOS task to block (pend) on a read operation from multiple 
RTOS queues or semaphores simultaneously. Note that there are simpler alternatives to using queue sets. See the [Blocking on Multiple Objects](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/10-Blocking-on-multiple-RTOS-objects) page for more information.

A queue set must be explicitly created using a call to xQueueCreateSet() or xQueueCreateSetStatic() before it can be used. Once created, standard FreeRTOS queues and semaphores can be added to the set using calls to [xQueueAddToSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/02-xQueueAddToSet). [xQueueSelectFromSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/04-xQueueSelectFromSet) is then used to determine which, if any, of the queues or semaphores contained in the set is in a state where a queue read or semaphore take operation would be successful.

Notes:

* Queues and semaphores **must be empty** when they are added to a
  queue set. Take particular care when adding objects such as binary
  semaphores which are created with the semaphore already available [this
  is the case if the semaphore is created using the vSemaphoreCreateBinary()
  macro, but not the case if the semaphore is created using the preferred
  xSemaphoreCreateBinary() function].

* Blocking on a queue set that contains a mutex will not cause the
  mutex holder to inherit the priority of the blocked task.

* An additional 4 bytes of RAM are required for each space in every
  queue added to a queue set. Therefore a counting semaphore that has a
  high maximum count value should not be added to a queue set.

* A receive (in the case of a queue) or take (in the case of a
  semaphore) operation must not be performed on a member of a queue set unless
  a call to xQueueSelectFromSet() has first returned a handle to that set member.


**Parameters:** 

- *uxEventQueueLength*

  Queue sets store events that occur on the queues and semaphores contained in the set. uxEventQueueLength
  specifies the maximum number of events that can be queued at once.

  To be absolutely certain that events are not lost uxEventQueueLength must be set to the sum of the
  lengths of the queues added to the set, where binary semaphores and mutexes have a length of 1, and
  counting semaphores have a length set by their maximum count value. For example:

  * If a queue set is to hold a queue of length 5, another queue of length 12, and a binary semaphore,
    then uxEventQueueLength should be set to (5 + 12 + 1), or 18.

  * If a queue set is to hold three binary semaphores then uxEventQueueLength should be set to (1 + 1 + 1 ),
    or 3.

  * If a queue set is to hold a counting semaphore that has a maximum count of 5, and a counting semaphore
    that has a maximum count of 3, then uxEventQueueLength should be set to (5 + 3), or 8.

- *pucQueueStorage*

  pucQueueStorage must point to a uint8_t array that is at least large enough to hold uxEventQueueLength events.

- *pxQueueBuffer*

  Must point to a variable of type StaticQueue_t, which will be used to hold the queue's data structure.  


**Returns:** 

If the queue set is created successfully then a handle to the created
queue set is returned. If pxQueueBuffer is NULL then NULL is returned.
 

**Example usage:**

```c
/* Define the lengths of the queues that will be added to the queue set. */
#define QUEUE_LENGTH_1       10
#define QUEUE_LENGTH_2       10

/* Binary semaphores have an effective length of 1. */
#define BINARY_SEMAPHORE_LENGTH 1

/* Define the size of the item to be held by queue 1 and queue 2 respectively. */
#define ITEM_SIZE_QUEUE_1    sizeof( uint32_t )
#define ITEM_SIZE_QUEUE_2    sizeof( something_else_t )

/* The combined length of the two queues and binary semaphore that will be
   added to the queue set. */
#define COMBINED_LENGTH ( QUEUE_LENGTH_1 + \
                          QUEUE_LENGTH_2 + \
                          BINARY_SEMAPHORE_LENGTH )

/* Define the maximum item size for the queue set */
#define MAX_ITEM_SIZE ( (ITEM_SIZE_QUEUE_1 > ITEM_SIZE_QUEUE_2) ? \
                         ITEM_SIZE_QUEUE_1 : ITEM_SIZE_QUEUE_2 )

/* Static storage for the queue set */
static StaticQueueSet_t xStaticQueueSet;
static uint8_t ucQueueSetStorage[COMBINED_LENGTH * MAX_ITEM_SIZE];

/* Static storage for Queue 1 */
static StaticQueue_t xStaticQueue1;
static uint8_t ucQueue1Storage[QUEUE_LENGTH_1 * ITEM_SIZE_QUEUE_1];

/* Static storage for Queue 2 */
static StaticQueue_t xStaticQueue2;
static uint8_t ucQueue2Storage[QUEUE_LENGTH_2 * ITEM_SIZE_QUEUE_2];

/* Static storage for the semaphore */
static StaticSemaphore_t xStaticSemaphore;

void vAFunction( void )
{
    static QueueSetHandle_t xQueueSet;
    QueueHandle_t xQueue1, xQueue2, xSemaphore;
    QueueSetMemberHandle_t xActivatedMember;
    uint32_t xReceivedFromQueue1;
    something_else_t xReceivedFromQueue2;

    /* Create the queue set using static allocation */
    xQueueSet = xQueueCreateSetStatic( COMBINED_LENGTH, ucQueueSetStorage, &xStaticQueueSet );

    /* Create the queues that will be contained in the set using static allocation */
    xQueue1 = xQueueCreateStatic( QUEUE_LENGTH_1, ITEM_SIZE_QUEUE_1, ucQueue1Storage, &xStaticQueue1 );
    xQueue2 = xQueueCreateStatic( QUEUE_LENGTH_2, ITEM_SIZE_QUEUE_2, ucQueue2Storage, &xStaticQueue2 );

    /* Create the semaphore that is being added to the set using static allocation */
    xSemaphore = xSemaphoreCreateBinaryStatic( &xStaticSemaphore );

    /* Check everything was created. */
    configASSERT( xQueueSet );
    configASSERT( xQueue1 );
    configASSERT( xQueue2 );
    configASSERT( xSemaphore );

    /* Add the queues and semaphores to the set */
    xQueueAddToSet( xQueue1, xQueueSet );
    xQueueAddToSet( xQueue2, xQueueSet );
    xQueueAddToSet( xSemaphore, xQueueSet );

    for( ;; )
    {
        /* Block to wait for something to be available from the queues or
           semaphore that have been added to the set. Don't block longer than
           200ms. */
        xActivatedMember = xQueueSelectFromSet( xQueueSet, pdMS_TO_TICKS(200) );

        /* Which set member was selected? */
        if( xActivatedMember == xQueue1 )
        {
            xQueueReceive( xActivatedMember, &xReceivedFromQueue1, 0 );
            vProcessValueFromQueue1( xReceivedFromQueue1 );
        }
        else if( xActivatedMember == xQueue2 )
        {
            xQueueReceive( xActivatedMember, &xReceivedFromQueue2, 0 );
            vProcessValueFromQueue2( &xReceivedFromQueue2 );
        }
        else if( xActivatedMember == xSemaphore )
        {
            /* Take the semaphore to make sure it can be "given" again. */
            xSemaphoreTake( xActivatedMember, 0 );
            vProcessEventNotifiedBySemaphore();
            break;
        }
        else
        {
            /* The 200ms block time expired without an RTOS queue or semaphore
               being ready to process. */
        }
    }
}
```