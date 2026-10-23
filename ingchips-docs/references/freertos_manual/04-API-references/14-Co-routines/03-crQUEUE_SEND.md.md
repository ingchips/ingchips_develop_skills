[[Co-Routine Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
crQUEUE_SEND(
              CoRoutineHandle_t xHandle,
              QueueHandle_t xQueue,
              void *pvItemToQueue,
              TickType_t xTicksToWait,
              BaseType_t *pxResult
            )
```

`crQUEUE_SEND` is a macro. The data types are shown in the prototype above for reference only.

The macro's `crQUEUE_SEND()` and `crQUEUE_RECEIVE()` are the co-routine
equivalent to the `xQueueSend()` and `xQueueReceive()` functions used by tasks.

`crQUEUE_SEND` and `crQUEUE_RECEIVE` can only be used from a co-routine whereas `xQueueSend()`
and `xQueueReceive()` can only be used from tasks. **Note** that co-routines
can only send data to other co-routines. A co-routine cannot use a queue to send data to a
task or vice versa.

`crQUEUE_SEND` can only be called from the co-routine function itself - not
from within a function called by the co-routine function. This is because
co-routines do not maintain their own stack.

See the co-routine section of the web documentation for information on
passing data between tasks and co-routines and between ISR's and
co-routines.


**Parameters:**

- *xHandle*

  The handle of the calling co-routine. This is the `xHandle` parameter of the co-routine function.

- *xQueue*

  The handle of the queue on which the data will be posted. The handle is obtained as the return value
  when the queue is created using the `xQueueCreate()` API function.

- *pvItemToQueue*

  A pointer to the data being posted onto the queue. The number of bytes of each queued item is specified
  when the queue is created. This number of bytes is copied from `pvItemToQueue` into the queue itself.

- *xTickToDelay*

  The number of ticks that the co-routine should block to wait for space to become available on the queue,
  should space not be available immediately. The actual amount of time this equates to is defined
  by `configTICK_RATE_HZ` (set in FreeRTOSConfig.h). The constant `portTICK_PERIOD_MS` can be used to
  convert ticks to milliseconds (see example below).

- *pxResult*

  The variable pointed to by `pxResult` will be set to `pdPASS` if data was successfully posted onto the
  queue, otherwise it will be set to an error defined within ProjDefs.h.


**Example usage:**

```c
// Co-routine function that blocks for a fixed period then posts a number onto
// a queue.
static void prvCoRoutineFlashTask( CoRoutineHandle_t xHandle,
                                   UBaseType_t uxIndex )
{
    // Variables in co-routines must be declared static if they must maintain
    // value across a blocking call.
    static BaseType_t xNumberToPost = 0;
    static BaseType_t xResult;

    // Co-routines must begin with a call to crSTART().
    crSTART( xHandle );

    for( ;; )
    {
        // This assumes the queue has already been created.
        crQUEUE_SEND( xHandle,
                      xCoRoutineQueue,
                      &xNumberToPost,
                      NO_DELAY,
                      &xResult );

        if( xResult != pdPASS )
        {
            // The message was not posted!
        }

        // Increment the number to be posted onto the queue.
        xNumberToPost++;

        // Delay for 100 ticks.
        crDELAY( xHandle, 100 );
    }

    // Co-routines must end with a call to crEND().
    crEND();
 }
```
