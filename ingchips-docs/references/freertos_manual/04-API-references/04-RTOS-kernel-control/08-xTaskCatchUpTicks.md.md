[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h


```c
BaseType_t xTaskCatchUpTicks( TickType_t xTicksToCatchUp );
```

Corrects the tick count value after the application code has held interrupts disabled for an extended period.

This function is similar to [vTaskStepTick()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick), however, 
unlike [vTaskStepTick()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick), this function may move the tick count forward past a
time at which a task should be remove from the blocked state. That means xTaskCatchUpTicks()
may remove tasks from the blocked state.


**Parameters:**

+ *xTicksToCatchUp* 

  The number of tick interrupts that have been missed due to interrupts being disabled. Its value is not 
  computed automatically, so must be computed by the application writer.


**Returns:**

pdTRUE if moving the tick count forward resulted in a task leaving the blocked state and a context switch 
being performed. Otherwise pdFALSE.


**Example usage:**

```c
void vExampleFunction( void )
{
    unsigned long ulTimeBefore, ulTimeAfter;

    /* Read the current time before arbitrary processing takes place. */
    ulTimeBefore = ulGetExternalTime();

    /* Stop the timer that is generating the tick interrupt. */
    prvStopTickInterruptTimer();
 
    /* Perform some arbitrary processing. */
    arbitrary_processing();
    
    /* Read the current time for computing elapsed time since ticks 
       were disabled. */
    ulTimeAfter = ulGetExternalTime();

    if ( xTaskCatchUpTicks( ulTimeAfter - ulTimeBefore ) == pdTRUE ) 
    {
        /* Moving the tick count forward resulted in a context switch. */
    }
    
    /* Restart the timer that is generating the tick interrupt. */
    prvStartTickInterruptTimer();

}
```
