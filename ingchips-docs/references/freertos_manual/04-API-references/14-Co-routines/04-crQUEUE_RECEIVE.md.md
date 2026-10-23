[[Co-Routine Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
void crQUEUE_RECEIVE(
                      CoRoutineHandle_t xHandle,
                      QueueHandle_t xQueue,
                      void *pvBuffer,
                      TickType_t xTicksToWait,
                      BaseType_t *pxResult
                    )
```

`crQUEUE_RECEIVE` is a macro. The data types are shown in the prototype above for reference only.

The macros `crQUEUE_SEND()` and `crQUEUE_RECEIVE()` are the co-routine
equivalent to the `xQueueSend()` and `xQueueReceive()` functions used by tasks.

`crQUEUE_SEND` and `crQUEUE_RECEIVE` can only be used from a co-routine whereas `xQueueSend()`
and `xQueueReceive()` can only be used from tasks. **Note** that co-routines
can only send data to other co-routines. A co-routine cannot use a queue to send data to a
task or vice versa.

`crQUEUE_RECEIVE` can only be called from the co-routine function itself - not
from within a function called by the co-routine function. This is because
co-routines do not maintain their own stack.

See the co-routine section of the web documentation for information on
passing data between tasks and co-routines and between ISR's and
co-routines.


**Parameters:**

- *xHandle*

  The handle of the calling co-routine. This is the `xHandle` parameter of the co-routine function.

- *xQueue*

  The handle of the queue from which the data will be received. The handle is obtained as the return
  value when the queue is created using the `xQueueCreate()` API function.

- *pvBuffer*

  The buffer into which the received item is to be copied. The number of bytes of each queued item is
  specified when the queue is created. This number of bytes is copied into `pvBuffer`.

- *xTickToDelay*

  The number of ticks that the co-routine should block to wait for data to become available from the
  queue, should data not be available immediately. The actual amount of time this equates to is defined
  by `configTICK_RATE_HZ` (set in FreeRTOSConfig.h). The constant `portTICK_PERIOD_MS` can be used to
  convert ticks to milliseconds (see the `crQUEUE_SEND` example).

- *pxResult*

  The variable pointed to by pxResult will be set to `pdPASS` if data was successfully retrieved from
  the queue, otherwise it will be set to an error code as defined within ProjDefs.h.


**Example usage:**

```c
// A co-routine receives the number of an LED to flash from a queue.  It
// blocks on the queue until the number is received.
static void prvCoRoutineFlashWorkTask( CoRoutineHandle_t xHandle,
                                       UBaseType_t uxIndex )
{
    // Variables in co-routines must be declared static if they must maintain
    // value across a blocking call.
    static BaseType_t xResult;
    static UBaseType_t uxLEDToFlash;

    // All co-routines must start with a call to crSTART().
    crSTART( xHandle );

    for( ;; )
    {
        // Wait for data to become available on the queue.
        crQUEUE_RECEIVE( xHandle,
                         xCoRoutineQueue,
                         &uxLEDToFlash,
                         portMAX_DELAY,
                         &xResult );

        if( xResult == pdPASS )
        {
            // We received the LED to flash - flash it!
            vParTestToggleLED( uxLEDToFlash );
        }
    }

    crEND();
}
```
