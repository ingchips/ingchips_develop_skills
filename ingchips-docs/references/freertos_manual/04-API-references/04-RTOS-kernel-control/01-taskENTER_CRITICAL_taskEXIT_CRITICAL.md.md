# taskENTER_CRITICAL(), taskEXIT_CRITICAL()

[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]


task.h

```c
void taskENTER_CRITICAL( void );
void taskEXIT_CRITICAL( void );
```

Critical sections are entered by calling taskENTER\_CRITICAL(), and subsequently
exited by calling taskEXIT\_CRITICAL().

The taskENTER\_CRITICAL() and taskEXIT\_CRITICAL() macros provide a basic critical
section implementation that works by simply disabling interrupts, either globally,
or up to a specific interrupt priority level. See the [vTaskSuspendAll()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/05-vTaskSuspendAll)
RTOS API function for information on creating a critical section without disabling
interrupts.


If the FreeRTOS port being used does not make use of
the [configMAX\_SYSCALL\_INTERRUPT\_PRIORITY](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) kernel configuration constant (also
called configMAX\_API\_CALL\_INTERRUPT\_PRIORITY), then calling taskENTER\_CRITICAL() will leave interrupts
globally disabled. If the FreeRTOS port being used does make use of the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
kernel configuration constant, then calling taskENTER\_CRITICAL() will leave interrupts at and below the
interrupt priority set by configMAX\_SYSCALL\_INTERRUPT\_PRIORITY disabled, and all higher priority interrupt
enabled.

Preemptive context switches only occur inside an interrupt, so will not occur when interrupts are disabled.
Therefore, the task that called taskENTER\_CRITICAL() is guaranteed to remain in the Running state until the
critical section is exited, unless the task explicitly attempts to block or yield (which it should not do
from inside a critical section).

Calls to taskENTER\_CRITICAL() and taskEXIT\_CRITICAL() are designed to nest. Therefore, a critical section
will only be exited when one call to taskEXIT\_CRITICAL() has been executed for every preceding call to
taskENTER\_CRITICAL().

Critical sections must be kept very short, otherwise they will adversely affect interrupt response times.
Every call to taskENTER\_CRITICAL() must be closely paired with a call to taskEXIT\_CRITICAL().

FreeRTOS API functions must not be called from within a critical section.

taskENTER\_CRITICAL() and taskEXIT\_CRITICAL() must not be called from an interrupt service routine (ISR) -
see [taskENTER\_CRITICAL\_FROM\_ISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/02-taskENTER_CRITICAL_FROM_ISR_taskEXIT_CRITICAL_FROM_ISR) and
taskEXIT\_CRITICAL\_FROM\_ISR() for interrupt safe equivalents.


**Parameters:**

*None*


**Returns:**

*None*


**Example usage:**

```c
/* A function that makes use of a critical section. */
void vDemoFunction( void )
{
    /* Enter the critical section. In this example, this function is itself called
       from within a critical section, so entering this critical section will result
       in a nesting depth of 2. */
    taskENTER_CRITICAL();

    /* Perform the action that is being protected by the critical section here. */

    /* Exit the critical section. In this example, this function is itself called
       from a critical section, so this call to taskEXIT_CRITICAL() will decrement the
       nesting count by one, but not result in interrupts becoming enabled. */
    taskEXIT_CRITICAL();
}

/* A task that calls vDemoFunction() from within a critical section. */
void vTask1( void * pvParameters )
{
    for( ;; )
    {
        /* Perform some functionality here. */

        /* Call taskENTER_CRITICAL() to create a critical section. */
        taskENTER_CRITICAL();


        /* Execute the code that requires the critical section here. */

        /* Calls to taskENTER_CRITICAL() can be nested so it is safe to call a
           function that includes its own calls to taskENTER_CRITICAL() and
           taskEXIT_CRITICAL(). */
        vDemoFunction();

        /* The operation that required the critical section is complete so exit the
           critical section. After this call to taskEXIT_CRITICAL(), the nesting depth
           will be zero, so interrupts will have been re-enabled. */
        taskEXIT_CRITICAL();
    }
}
```
