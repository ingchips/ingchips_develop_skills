[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h

```c
 void vTaskStepTick( TickType_t xTicksToJump );
```

If the RTOS is configured to use [tickless idle functionality](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
then the tick interrupt will be stopped, and the microcontroller placed into a low power state,
whenever the Idle task is the only task able to execute. Upon exiting the low
power state the tick count value must be corrected to account for the time that
passed while it was stopped.

If a FreeRTOS port includes a default [portSUPPRESS\_TICKS\_AND\_SLEEP()](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
implementation, then `vTaskStepTick()` is used internally to ensure the correct
tick count value is maintained. `vTaskStepTick()` is a public API function to
allow the default `portSUPPRESS_TICKS_AND_SLEEP()` implementation to be overridden,
and for a `portSUPPRESS_TICKS_AND_SLEEP()` to be provided if the port being used does not
provide a default.

The `configUSE_TICKLESS_IDLE` configuration constant must be set to 1 for
`vTaskStepTick()` to be available.


**Parameters:** 

- *xTicksToJump*

  The number of RTOS ticks that have passed since the tick interrupt was stopped. For correct operation the 
  parameter must be less than or equal to the `portSUPPRESS_TICKS_AND_SLEEP()` parameter.


**Returns:** 

*None.*
 

**Example usage:**

The example shows calls being made to several functions. Only `vTaskStepTick()`
is part of the FreeRTOS API. The other functions are specific to the clocks
and power saving modes available on the hardware in use, and as such, must be
provided by the application writer.

```c
/* First define the portSUPPRESS_TICKS_AND_SLEEP(). The parameter is the time,
   in ticks, until the kernel next needs to execute. */
#define portSUPPRESS_TICKS_AND_SLEEP( xIdleTime ) vApplicationSleep( xIdleTime )

/* Define the function that is called by portSUPPRESS_TICKS_AND_SLEEP(). */
void vApplicationSleep( TickType_t xExpectedIdleTime )
{
    unsigned long ulLowPowerTimeBeforeSleep, ulLowPowerTimeAfterSleep;

    /* Read the current time from a time source that will remain operational
       while the microcontroller is in a low power state. */
    ulLowPowerTimeBeforeSleep = ulGetExternalTime();

    /* Stop the timer that is generating the tick interrupt. */
    prvStopTickInterruptTimer();

    /* Configure an interrupt to bring the microcontroller out of its low power
       state at the time the kernel next needs to execute. The interrupt must be
       generated from a source that is remains operational when the microcontroller
       is in a low power state. */
    vSetWakeTimeInterrupt( xExpectedIdleTime );

    /* Enter the low power state. */
    prvSleep();

    /* Determine how long the microcontroller was actually in a low power state
       for, which will be less than xExpectedIdleTime if the microcontroller was
       brought out of low power mode by an interrupt other than that configured by
       the vSetWakeTimeInterrupt() call. Note that the scheduler is suspended
       before portSUPPRESS_TICKS_AND_SLEEP() is called, and resumed when
       portSUPPRESS_TICKS_AND_SLEEP() returns. Therefore no other tasks will
       execute until this function completes. */
    ulLowPowerTimeAfterSleep = ulGetExternalTime();

    /* Correct the kernels tick count to account for the time the microcontroller
       spent in its low power state. */
    vTaskStepTick( ulLowPowerTimeAfterSleep - ulLowPowerTimeBeforeSleep );

    /* Restart the timer that is generating the tick interrupt. */
    prvStartTickInterruptTimer();
}
```
