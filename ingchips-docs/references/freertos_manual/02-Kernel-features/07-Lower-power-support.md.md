# Low Power Support

*Tickless Idle Mode*

[**See also [Low Power Features For ARM Cortex-M MCUs](https://www.freertos.org/low-power-ARM-cortex-rtos)**]

[**See also Tickless Demos on [SAM4L](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM4L-EK_Low_Power_Tick-less_RTOS_Demo), [RX100](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX100_RSK_Low_Power_Tick-less_RTOS_Demo),
[STM32L](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32L-discovery-low-power-tickless-RTOS-demo),
[CEC1302](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/Microchip_CEC1302_ARM_Cortex-M4F_Low_Power_Demo)
and [EFM32](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32-Giant-Gecko-Pearl-Gecko-tickless-RTOS-demo) MCUs** ]


## Power Saving Introduction

It is common to reduce the power consumed by the microcontroller on which
FreeRTOS is running by using the [Idle task hook](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions) to place the
microcontroller into a low power state. The power saving that can be achieved
by this simple method is limited by the necessity to periodically exit and then
re-enter the low power state to process tick interrupts. Further, if the frequency
of the tick interrupt is too high, the energy and time consumed entering and then
exiting a low power state for every tick will outweigh any potential power saving
gains for all but the lightest power saving modes.

The FreeRTOS tickless idle mode stops the periodic tick interrupt during
idle periods (periods when there are no application tasks that are able to execute),
then makes a correcting adjustment to the RTOS tick count value when the tick
interrupt is restarted.

Stopping the tick interrupt allows the microcontroller to remain in a deep
power saving state until either an interrupt occurs, or it is time for the RTOS
kernel to transition a task into the Ready state.

 
## The portSUPPRESS\_TICKS\_AND\_SLEEP() Macro

```c
    portSUPPRESS_TICKS_AND_SLEEP( xExpectedIdleTime )
```

Built in tickless idle functionality is enabled by defining
configUSE\_TICKLESS\_IDLE as 1 in FreeRTOSConfig.h (for ports that support this
feature). User defined tickless idle functionality can be provided for any
FreeRTOS port (including those that include a built in implementation) by
defining configUSE\_TICKLESS\_IDLE to 2 in FreeRTOSConfig.h.

When the tickless idle functionality is enabled the kernel will call the
portSUPPRESS\_TICKS\_AND\_SLEEP() macro when the following two conditions are both
true:

1. The Idle task is the only task able to run because all the application
   tasks are either in the Blocked state or in the Suspended state.

2. At least *n* further complete tick periods will pass before the kernel
   is due to transition an application task out of the Blocked state, where
   *n* is set by the configEXPECTED\_IDLE\_TIME\_BEFORE\_SLEEP definition in
   FreeRTOSConfig.h.

The value of portSUPPRESS\_TICKS\_AND\_SLEEP()'s single parameter equals
the total number of tick periods before a task is
due to be moved into the Ready state. The parameter value is therefore the time the
microcontroller can safely remain in a deep sleep state, with the tick interrupt
stopped (suppressed).

**Note**: If [eTaskConfirmSleepModeStatus()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/11-eTaskConfirmSleepModeStatus) returns eNoTasksWaitingTimeout when
it is called from within portSUPPRESS\_TICKS\_AND\_SLEEP() then the microcontroller
can remain in a deep sleep state indefinitely. eTaskConfirmSleepModeStatus() will only return
eNoTasksWaitingTimeout when the following conditions are true:

1. Software timers are not being used, so the scheduler is not due to
   execute a timer callback function at any time in the future.

2. All the application tasks are either in the Suspended state, or in the
   Blocked state with an infinite timeout (a timeout value of portMAX\_DELAY),
   so the scheduler is not due to transition a task out of the Blocked state
   at any fixed time in the future.

To avoid race conditions the RTOS scheduler is suspended before
portSUPPRESS\_TICKS\_AND\_SLEEP() is called, and resumed when portSUPPRESS\_TICKS\_AND\_SLEEP()
completes. This ensures application tasks cannot execute between the microcontroller exiting
its low power state and portSUPPRESS\_TICKS\_AND\_SLEEP() completing its execution.
Further, it is necessary for the portSUPPRESS\_TICKS\_AND\_SLEEP() function to create
a small critical section between the tick source being stopped and the microcontroller
entering the sleep state. eTaskConfirmSleepModeStatus() should be called from
this critical section.

All GCC, IAR and Keil ARM Cortex-M ports now provide a default
portSUPPRESS\_TICKS\_AND\_SLEEP() implementation. Important information on using
the ARM Cortex-M implementation is provided on
the [Low Power Features For ARM Cortex-M MCUs](https://www.freertos.org/low-power-ARM-cortex-rtos) page.

Default implementations will be added to other FreeRTOS ports
over time. In the mean time, the hooks described below can be used to add
tickless functionality to any port.

 
## Implementing portSUPPRESS\_TICKS\_AND\_SLEEP()

If the FreeRTOS port in use does not provide a default implementation of
portSUPPRESS\_TICKS\_AND\_SLEEP(), then the application writer can provide their own
implementation by defining portSUPPRESS\_TICKS\_AND\_SLEEP() in FreeRTOSConfig.h.

If the FreeRTOS port in use does provide a default implementation of
portSUPPRESS\_TICKS\_AND\_SLEEP(), then the application writer can override the
default implementation by defining portSUPPRESS\_TICKS\_AND\_SLEEP() in
FreeRTOSConfig.h.

The following source code is an example of how
portSUPPRESS\_TICKS\_AND\_SLEEP() might be implemented by an application writer.
The example is basic, and will introduce some slippage between the time
maintained by the kernel and calendar time. Official FreeRTOS versions
attempt to remove any slippage (as far as is possible) by providing a more
intricate implementation.

Of the functions calls shown in the example, only [vTaskStepTick()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick)
and [eTaskConfirmSleepModeStatus()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/11-eTaskConfirmSleepModeStatus)
are part of the FreeRTOS API. The other functions are specific to the clocks
and power saving modes available on the hardware in use, and as such, must be
provided by the application writer.

---

```c
/* First define the portSUPPRESS_TICKS_AND_SLEEP() macro. The parameter is the
   time, in ticks, until the kernel next needs to execute. */
#define portSUPPRESS_TICKS_AND_SLEEP( xIdleTime ) vApplicationSleep( xIdleTime )

/* Define the function that is called by portSUPPRESS_TICKS_AND_SLEEP(). */
void vApplicationSleep( TickType_t xExpectedIdleTime )
{
unsigned long ulLowPowerTimeBeforeSleep, ulLowPowerTimeAfterSleep;
eSleepModeStatus eSleepStatus;

    /* Read the current time from a time source that will remain operational
       while the microcontroller is in a low power state. */
    ulLowPowerTimeBeforeSleep = ulGetExternalTime();

    /* Stop the timer that is generating the tick interrupt. */
    prvStopTickInterruptTimer();

    /* Enter a critical section that will not effect interrupts bringing the MCU
       out of sleep mode. */
    disable_interrupts();

    /* Ensure it is still ok to enter the sleep mode. */
    eSleepStatus = eTaskConfirmSleepModeStatus();

    if( eSleepStatus == eAbortSleep )
    {
        /* A task has been moved out of the Blocked state since this macro was
           executed, or a context siwth is being held pending. Do not enter a
           sleep state. Restart the tick and exit the critical section. */
        prvStartTickInterruptTimer();
        enable_interrupts();
    }
    else
    {
        if( eSleepStatus == eNoTasksWaitingTimeout )
        {
            /* It is not necessary to configure an interrupt to bring the
               microcontroller out of its low power state at a fixed time in the
               future. */
            prvSleep();
        }
        else
        {
            /* Configure an interrupt to bring the microcontroller out of its low
               power state at the time the kernel next needs to execute. The
               interrupt must be generated from a source that remains operational
               when the microcontroller is in a low power state. */
            vSetWakeTimeInterrupt( xExpectedIdleTime );

            /* Enter the low power state. */
            prvSleep();

            /* Determine how long the microcontroller was actually in a low power
               state for, which will be less than xExpectedIdleTime if the
               microcontroller was brought out of low power mode by an interrupt
               other than that configured by the vSetWakeTimeInterrupt() call.
               Note that the scheduler is suspended before
               portSUPPRESS_TICKS_AND_SLEEP() is called, and resumed when
               portSUPPRESS_TICKS_AND_SLEEP() returns. Therefore no other tasks will
               execute until this function completes. */
            ulLowPowerTimeAfterSleep = ulGetExternalTime();

            /* Correct the kernels tick count to account for the time the
               microcontroller spent in its low power state. */
            vTaskStepTick( ulLowPowerTimeAfterSleep - ulLowPowerTimeBeforeSleep );
        }

        /* Exit the critical section - it might be possible to do this immediately
           after the prvSleep() calls. */
        enable_interrupts();

        /* Restart the timer that is generating the tick interrupt. */
        prvStartTickInterruptTimer();
    }
}
```
*An example user defined implementation of portSUPPRESS\_TICKS\_AND\_SLEEP()*

---
