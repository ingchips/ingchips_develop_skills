# taskENTER_CRITICAL_FROM_ISR(), taskEXIT_CRITICAL_FROM_ISR()

[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]


task.h

```c
UBaseType_t taskENTER_CRITICAL_FROM_ISR( void );
void taskEXIT_CRITICAL_FROM_ISR( UBaseType_t uxSavedInterruptStatus );
```

Versions of [taskENTER\_CRITICAL() and taskEXIT\_CRITICAL()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL)
that can be used in an interrupt service routine (ISR).

In an ISR critical sections are entered by calling taskENTER\_CRITICAL\_FROM\_ISR(),
and subsequently exited by calling taskEXIT\_CRITICAL\_FROM\_ISR().

The taskENTER\_CRITICAL\_FROM\_ISR() and taskEXIT\_CRITICAL\_FROM\_ISR() macros provide
a basic critical section implementation that works by simply disabling interrupts,
either globally, or up to a specific interrupt priority level.

If the FreeRTOS port being used supports interrupt nesting then calling
taskENTER\_CRITICAL\_FROM\_ISR() will disable interrupts at and below the interrupt
priority set by the [configMAX\_SYSCALL\_INTERRUPT\_PRIORITY](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
(or configMAX\_API\_CALL\_INTERRUPT\_PRIORITY) kernel configuration constant, and leave
all other interrupt priorities enabled.
If the FreeRTOS port being used does not support interrupt nesting then
taskENTER\_CRITICAL\_FROM\_ISR() and taskEXIT\_CRITICAL\_FROM\_ISR() will have no effect.

Calls to taskENTER\_CRITICAL\_FROM\_ISR() and taskEXIT\_CRITICAL\_FROM\_ISR() are
designed to nest, but the semantics of how the macros are used is different to
the taskENTER\_CRITICAL() and taskEXIT\_CRITICAL()
equivalents.

Critical sections must be kept very short, otherwise they will adversely affect
the response times of higher priority interrupts that would otherwise nest.
Every call to taskENTER\_CRITICAL\_FROM\_ISR() must be closely paired with a call to
taskEXIT\_CRITICAL\_FROM\_ISR().

FreeRTOS API functions must not be called from within a critical section.


**Parameters:**


+ *uxSavedInterruptStatus*

  taskEXIT\_CRITICAL\_FROM\_ISR() takes uxSavedInterruptStatus as its only parameter. The value used as
  the uxSavedInterruptStatus parameter must be the value returned from the matching call to
  taskENTER\_CRITICAL\_FROM\_ISR().

  taskENTER\_CRITICAL\_FROM\_ISR() does not take any parameters.


**Returns:**

 taskENTER\_CRITICAL\_FROM\_ISR() returns the interrupt mask state as it was
 before the macro was called. The value returned by taskENTER\_CRITICAL\_FROM\_ISR()
 must be used as the uxSavedInterruptStatus parameter in the matching call
 to taskEXIT\_CRITICAL\_FROM\_ISR().

 taskEXIT\_CRITICAL\_FROM\_ISR() does not return a value.


**Example usage:**

```c
/* A function called from an ISR. */
void vDemoFunction( void )
{
UBaseType_t uxSavedInterruptStatus;

    /* Enter the critical section. In this example, this function is itself called from
       within a critical section, so entering this critical section will result in a nesting
       depth of 2. Save the value returned by taskENTER_CRITICAL_FROM_ISR() into a local
       stack variable so it can be passed into taskEXIT_CRITICAL_FROM_ISR(). */
    uxSavedInterruptStatus = taskENTER_CRITICAL_FROM_ISR();

    /* Perform the action that is being protected by the critical section here. */

    /* Exit the critical section. In this example, this function is itself called from a
       critical section, so interrupts will have already been disabled before a value was
       stored in uxSavedInterruptStatus, and therefore passing uxSavedInterruptStatus into
       taskEXIT_CRITICAL_FROM_ISR() will not result in interrupts being re-enabled. */
    taskEXIT_CRITICAL_FROM_ISR( uxSavedInterruptStatus );
}

/* A task that calls vDemoFunction() from within an interrupt service routine. */
void vDemoISR( void )
{
UBaseType_t uxSavedInterruptStatus;

    /* Call taskENTER_CRITICAL_FROM_ISR() to create a critical section, saving the
       returned value into a local stack variable. */
    uxSavedInterruptStatus = taskENTER_CRITICAL_FROM_ISR();


    /* Execute the code that requires the critical section here. */


    /* Calls to taskENTER_CRITICAL_FROM_ISR() can be nested so it is safe to call a
       function that includes its own calls to taskENTER_CRITICAL_FROM_ISR() and
       taskEXIT_CRITICAL_FROM_ISR(). */
    vDemoFunction();

    /* The operation that required the critical section is complete so exit the
       critical section. Assuming interrupts were enabled on entry to this ISR, the value
       saved in uxSavedInterruptStatus will result in interrupts being re-enabled.*/
    taskEXIT_CRITICAL_FROM_ISR( uxSavedInterruptStatus );
}
```
