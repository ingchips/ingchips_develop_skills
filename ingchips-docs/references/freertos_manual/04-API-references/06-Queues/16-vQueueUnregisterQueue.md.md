[[Queue Management](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
 void vQueueUnregisterQueue( QueueHandle_t xQueue );
```
 
Removes a queue from the queue registry.


**Parameters:**

- *xQueue*

  The handle of the queue being removed from the registry.


The queue registry has two purposes, both of which are associated with RTOS kernel aware debugging:

1. It allows a textual name to be associated with a queue for easy queue identification within a debugging GUI.
2. It contains the information required by a debugger to locate each registered queue and semaphore.

The queue registry has no purpose unless you are using a RTOS kernel aware debugger.

`configQUEUE_REGISTRY_SIZE` defines the maximum number of queues and semaphores that can be registered. 
Only the queues and semaphores that you want to view using a RTOS kernel aware debugger need to be registered. 


### Example 

```c
void vAFunction( void )
{
    QueueHandle_t xQueue;

    /* Create a queue big enough to hold 10 chars. */
    xQueue = xQueueCreate( 10, sizeof( char ) );

    /* We want this queue to be viewable in a RTOS kernel aware debugger, 
       so register it. */
    vQueueAddToRegistry( xQueue, "AMeaningfulName" );

    /* The queue gets used here. */

    /* At some later time, the queue is going to be deleted, first 
       remove it from the registry. */
    vQueueUnregisterQueue( xQueue );
    vQueueDelete( xQueue );
}
```
