[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
 const char * pcTimerGetName( TimerHandle_t xTimer );
```

Returns the human readable text name of a [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).

Text names are assigned to timers using the `pcTimerName` parameter of the call 
to [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate) used to create the timer.


**Parameters:** 

- *xTimer*

  The timer being queried.

**Returns:**

- A pointer to the text name of the timer as a standard NULL terminated C string.
 

**Example usage:**

```c
const char *pcTimerName = "ExampleTimer";

/* A function that creates a timer. */
static void prvCreateTimer( void )
{
TimerHandle_t xTimer;

    /* Create a timer. */
    xTimer = xTimerCreate( pcTimerName,           /* Text name. */
                           pdMS_TO_TICKS( 500 ),  /* Period. */
                           pdTRUE,                /* Autoreload. */
                           NULL,                  /* No ID. */
                           prvExampleCallback );  /* Callback function. */

    if( xTimer != NULL )
    {
        xTimerStart( xTimer, portMAX_DELAY );

        /* Just to demonstrate pcTimerGetName(), query the timer's name and
           assert if it does not equal pcTimerName. */
        configASSERT( strcmp( pcTimerGetName( xTimer ), pcTimerName ) == 0 );
    }
}
```
