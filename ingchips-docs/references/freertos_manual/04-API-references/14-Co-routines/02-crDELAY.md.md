[[Co-Routine Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
void crDELAY( CoRoutineHandle_t xHandle,
              TickType_t xTicksToDelay )
```

`crDELAY` is a macro. The data types in the prototype above are shown for reference only.

Delay a co-routine for a fixed period of time.

`crDELAY` can only be called from the co-routine function itself - not
from within a function called by the co-routine function. This is because
co-routines do not maintain their own stack.


**Parameters:**

- *xHandle*

  The handle of the co-routine to delay. This is the xHandle parameter of the co-routine function.

- *xTickToDelay*

  The number of ticks that the co-routine should delay for. The actual amount of time this equates to
  is defined by `configTICK_RATE_HZ` (set in FreeRTOSConfig.h). The constant `portTICK_PERIOD_MS` can be
  used to convert ticks to milliseconds.


**Example usage:**

```c
// Co-routine to be created.
void vACoRoutine( CoRoutineHandle_t xHandle,
                  UBaseType_t uxIndex )
{
    // Variables in co-routines must be declared static if they must maintain
    // value across a blocking call. This may not be necessary for const
    // variables. We are to delay for 200ms.
    static const xTickType xDelayTime = 200 / portTICK_PERIOD_MS;

    // Must start every co-routine with a call to crSTART();
    crSTART( xHandle );

    for( ;; )
    {
        // Delay for 200ms.
        crDELAY( xHandle, xDelayTime );

        // Do something here.
    }

    // Must end every co-routine with a call to crEND();
    crEND();
}
```
