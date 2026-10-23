[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h

```c
 eSleepModeStatus eTaskConfirmSleepModeStatus( void );
```

Tick-less idle mode specific function.

Provided for use within [portSUPPRESS\_TICKS\_AND\_SLEEP()](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) to allow the port
specific sleep function to determine if it may proceed with the sleep, and if the sleep can be indefinite.

This function is necessary because `portSUPPRESS_TICKS_AND_SLEEP()` is only called with the scheduler 
suspended, not from within a critical section. It is therefore possible for an interrupt to request a 
context switch between `portSUPPRESS_TICKS_AND_SLEEP()` being called and the low power mode actually being
entered. `eTaskConfirmSleepModeStatus()` should be called from a short critical section between the timer 
being stopped and the sleep mode being entered.

The `configUSE_TICKLESS_IDLE` configuration constant must be set to 1 for `eTaskConfirmSleepModeStatus()` 
to be available.


**Parameters:** 

None.
 

**Returns:** 

If a task has been transitioned out of the Blocked state since `portSUPPRESS_TICKS_AND_SLEEP()` was called, 
or a context switch is being held pending (because the scheduler is suspended), then `eTaskConfirmSleepModeStatus()` 
will return `eAbortSleep` and sleep mode must not be entered.
 
If software timers are not being used, and all the application tasks are either Blocked with an indefinite 
timeout or Suspended, then `eTaskConfirmSleepModeStatus()` will return `eNoTasksWaitingTimeout` 
and `portSUPPRESS_TICKS_AND_SLEEP()` can enter a deep sleep state without first having to configure a timer 
to bring the microcontroller out of its sleep state at a pre-determined time in the future.
 
In all other cases `eTaskConfirmSleepModeStatus()` will return `eStandardSleep`.
 

**Example usage:**

`eTaskConfirmSleepModeStatus()` is used in 
the [example implementation of portSUPPRESS\_TICKS\_AND\_SLEEP().](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
  
