[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h


```c
 TimerHandle_t xTimerCreateStatic
                 ( const char * const pcTimerName,
                   const TickType_t xTimerPeriod,
                   const UBaseType_t uxAutoReload,
                   void * const pvTimerID,
                   TimerCallbackFunction_t pxCallbackFunction
                   StaticTimer_t *pxTimerBuffer );
```

Creates a new [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) instance and
returns a handle by which the timer can be referenced.

For this RTOS API function to be available:

1. configUSE\_TIMERS and [configSUPPORT\_STATIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
   must both be set to 1 in FreeRTOSConfig.h.
2. The FreeRTOS/Source/timer.c C source file must be included in the build.

Each software timer requires a small amount of RAM that is used to hold the
timer's state. If a timer is created using [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If a software timer is created using xTimerCreateStatic()
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile time. See
the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.

Timers are created in the dormant state.
The [xTimerStart()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart),
 [xTimerReset()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset),
 [xTimerStartFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/09-xTimerStartFromISR),
 [xTimerResetFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/12-xTimerResetFromISR),
 [xTimerChangePeriod()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod),
 and [xTimerChangePeriodFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR) API functions can all be
 used to transition a timer into the active state.


**Parameters:**

+ *pcTimerName*

  A human readable text name that is assigned to the timer. This is done purely to assist debugging. The
  RTOS kernel itself only ever references a timer by its handle, and never by its name.

+ *xTimerPeriod*

  The period of the timer. The period is specified in ticks, and the macro pdMS\_TO\_TICKS() can be used
  to convert a time specified in milliseconds to a time specified in ticks. For example, if the timer must
  expire after 100 ticks, then simply set xTimerPeriod to 100. Alternatively, if the timer must expire
  after 500ms, then set xTimerPeriod to pdMS\_TO\_TICKS( 500 ). pdMS\_TO\_TICKS() can only be used
  if [configTICK\_RATE\_HZ](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) is less than or equal to 1000. The timer period
  must be greater than 0.

+ *uxAutoReload*

  If uxAutoReload is set to pdTRUE, then the timer will expire repeatedly with a frequency set by the
  xTimerPeriod parameter. If uxAutoReload is set to pdFALSE, then the timer will be a one-shot and enter
  the dormant state after it expires.

+ *pvTimerID*

  An identifier that is assigned to the timer being created. Typically this would be used in the timer
  callback function to identify which timer expired when the same callback function is assigned to more
  than one timer, or together with the [vTimerSetTimerID()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID)
  and [pvTimerGetTimerID()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID)API functions to save a value
  between calls to the timer's callback function.

+ *pxCallbackFunction*

  The function to call when the timer expires. Callback functions must have the prototype defined by
  TimerCallbackFunction\_t, which is:

  ```c
  void vCallbackFunction( TimerHandle_t xTimer );
  ```

+ *pxTimerBuffer*

  Must point to a variable of type StaticTimer\_t, which is then used to hold the timer's state.


**Returns:**

If the timer is created successfully then a handle to the newly created timer is returned. If pxTimerBuffer
is NULL then the timer will not be created and NULL is returned.


**Example usage:**

```c
 pxTimerBuffer #define NUM_TIMERS 5

 /* An array to hold handles to the created timers. */
 TimerHandle_t xTimers[ NUM_TIMERS ];

 /* An array of StaticTimer_t structures, which are used to store
    the state of each created timer. */
 StaticTimer_t xTimerBuffers[ NUM_TIMERS ];

 /* Define a callback function that will be used by multiple timer
    instances. The callback function does nothing but count the number
    of times the associated timer expires, and stop the timer once the
    timer has expired 10 times. The count is saved as the ID of the
    timer. */
 void vTimerCallback( TimerHandle_t xTimer )
 {
 const uint32_t ulMaxExpiryCountBeforeStopping = 10;
 uint32_t ulCount;

    /* Optionally do something if the pxTimer parameter is NULL. */
    configASSERT( pxTimer );

    /* The number of times this timer has expired is saved as the
       timer's ID. Obtain the count. */
    ulCount = ( uint32_t ) pvTimerGetTimerID( xTimer );

    /* Increment the count, then test to see if the timer has expired
       ulMaxExpiryCountBeforeStopping yet. */
    ulCount++;

    /* If the timer has expired 10 times then stop it from running. */
    if( ulCount >= ulMaxExpiryCountBeforeStopping )
    {
        /* Do not use a block time if calling a timer API function
           from a timer callback function, as doing so could cause a
           deadlock! */
        xTimerStop( xTimer, 0 );
    }
    else
    {
       /* Store the incremented count back into the timer's ID field
          so it can be read back again the next time this software timer
          expires. */
       vTimerSetTimerID( xTimer, ( void * ) ulCount );
    }
 }

 void main( void )
 {
 long x;

    /* Create then start some timers. Starting the timers before
       the RTOS scheduler has been started means the timers will start
       running immediately that the RTOS scheduler starts. */
    for( x = 0; x < NUM_TIMERS; x++ )
    {
        xTimers[ x ] = xTimerCreateStatic
                  ( /* Just a text name, not used by the RTOS kernel. */
                    "Timer",
                    /* The timer period in ticks, must be greater than 0. */
                    ( 100 * x ) + 100,
                    /* The timers will auto-reload themselves when they expire. */
                    pdTRUE,
                    /* The ID is used to store a count of the number of times
                       the timer has expired, which is initialised to 0. */
                    ( void * ) 0,
                    /* Each timer calls the same callback when it expires. */
                    vTimerCallback,
                    /* Pass in the address of a StaticTimer_t variable, which
                       will hold the data associated with the timer being
                       created. */
                    &( xTimerBuffers[ x ] );
                  );

        if( xTimers[ x ] == NULL )
        {
            /* The timer was not created. */
        }
        else
        {
            /* Start the timer. No block time is specified, and
               even if one was it would be ignored because the RTOS
               scheduler has not yet been started. */
            if( [xTimerStart](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)( xTimers[ x ], 0 ) != pdPASS )
            {
                /* The timer could not be set into the Active state. */
            }
        }
    }

    /* ...
 Create tasks here.
 ... */

    /* Starting the RTOS scheduler will start the timers running as they have
       already been set into the active state. */
    vTaskStartScheduler();

    /* Should not reach here. */
    for( ;; );
 }
```
