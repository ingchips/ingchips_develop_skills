# Blocking on Multiple RTOS Objects

### Introduction to Queue Sets

[Queue sets](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets) are a FreeRTOS feature that
enables an RTOS task to block (pend) when receiving from multiple queues and/or
semaphores at the same time. Queues and semaphores are grouped into sets, then, instead of blocking on an
individual queue or semaphore, a task instead blocks on the set.

**Note:** While it is sometimes necessary to block (pend) on more than one queue if you
are integrating FreeRTOS with third party of legacy code, designs that are free
from such restrictions can normally achieve the same functionality in a more
efficient way using the alternative design pattern that 
is [documented at the bottom of this page](#alternatives-to-using-queue-sets).


### Using Queue Sets

Queue sets are used in a similar way to the select() API function, and related
functions, that are part of the standard Berkeley sockets networking API.

Queue sets can contain queues and semaphores, which together are known as
queue set members. API function parameters and return values that can take either
a queue handle or a semaphore handle use the QueueSetMemberHandle\_t type.
Variables of type QueueHandle\_t and SemaphoreHandle\_t can normally be implicitly
converted to an QueueSetMemberHandle\_t parameter or return value without compiler
warnings being generated (explicit casting to and from the QueueSetMemberHandle\_t
type is not normally required).

+ **Creating a queue set**  

  Before a queue set can be used it must be created using the [xQueueCreateSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) 
  API function. Once created the queue set is referenced by a variable of type QueueSetHandle\_t.

+ **Adding a member to a queue set**  

  The [xQueueAddToSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/02-xQueueAddToSet) API function is used to add a queue or semaphore to a queue set.

+ **Blocking (pending) on a queue set**  

  The [xQueueSelectFromSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/04-xQueueSelectFromSet) API function is used to test whether any of the set 
  members are ready for reading - where reading means 'receiving' when the member is a queue, and 'taking'
  when the member is a semaphore.

  Just like when using the [xQueueReceive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/09-xQueueReceive) and [xSemaphoreTake()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) API functions, 
  xQueueSelectFromSet() allows the calling task to optionally block until a member of the queue set is ready
  for reading.

  NULL is returned if a call to xQueueSelectFromSet() times out. Otherwise xQueueSelectFromSet() returns 
  the handle of the queue set member that is ready for reading, allowing the calling task to immediately 
  call xQueueReceive() or xSemaphoreTake() (on a queue handle or semaphore handle respectively) with the 
  guarantee that the operation will succeed.


### Source Code Examples

The [xQueueCreateSet()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) API function documentation page includes a source code example.

The standard demo/test file called QueueSet.c (located in the FreeRTOS/Demo/Common/Minimal/ directory of the 
main FreeRTOS zip file download) contains a comprehensive example.


### Alternatives to Using Queue Sets

Unless there is a specific integration issue that necessitates blocking on multiple queues, the same 
functionality can normally be achieved with a lower code size, RAM size, and run time overhead using 
a single queue. The FreeRTOS-Plus-UDP implementation provides a convenient example of how this is 
done, and is described in the following sub-sections.


#### UDP/IP Stack: Problem Definition

The task that manages the FreeRTOS-Plus-UDP stack is event driven. There are multiple
event sources. Some events do not have any data associated with them. Some events have
a variable amount of data associated with them. Events include:

* The Ethernet hardware receiving a frame. Frames contain large and variable amounts of data.
* The Ethernet hardware completing the transmission of a frame, freeing network and DMA buffers.
* An application task sending a packet. Packets can contain a large and variable amount of data.
* Various software timers, including the ARP timer. Timer events are not associated with any data.


#### UDP/IP Stack: Solution

The UDP/IP stack *could* use a different queue for each event source, then
use a queue set to block on all the queues at once. Instead, the UDP/IP stack:

1. Defines a structure that contains a member to hold the event type, and another member to hold the 
   data (or a pointer to the data) that is associated with the event.
2. Uses a single queue that is created to hold the defined structure. Each event source posts to the 
   same queue.

The structure definition is shown below.

```c
typedef struct IP_TASK_COMMANDS
{
    eIPEvent_t eEventType; /* Tells the receiving task what the event is. */
    void *pvData; /* Holds or points to any data associated with the event. */

} xIPStackEvent_t;
```

Examples of how this structure is used:

* When the ARP timer expires it sends an event to the queue with eEventType set to eARPTimerEvent (an 
  enumerated type). ARP timer events are not associated with any data so pvData is not set.
* When the Ethernet driver receives a frame it sends an event to the queue with eEventType set to eEthernetRxEvent, 
  and pvData set to point to the frame buffer.
* Etc.

The UDP/IP task processes events using a simple loop:

```c
/* The variable used to receive from the queue. */
xIPStackEvent_t xReceivedEvent;

for( ;; )
{
    /* Wait until there is something to do. */
    xQueueReceive( xNetworkEventQueue, &xReceivedEvent, portMAX_DELAY );

    /* Perform a different action for each event type. */
    switch( xReceivedEvent.eEventType )
    {
        case eNetworkDownEvent :
            prvProcessNetworkDownEvent();
            break;

        case eEthernetRxEvent :
            prvProcessEthernetFrame( xReceivedEvent.pvData );
            break;

        case eARPTimerEvent :
            prvAgeARPCache();
            break;

        case eStackTxEvent :
            prvProcessGeneratedPacket( xReceivedEvent.pvData );
            break;

        case eDHCPEvent:
            vDHCPProcess();
            break;

        default :
            /* Should not get here. */
            break;
    }
}
```
