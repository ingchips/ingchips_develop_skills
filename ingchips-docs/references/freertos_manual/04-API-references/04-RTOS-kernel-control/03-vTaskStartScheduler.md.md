[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h 

```c
void vTaskStartScheduler( void );
```

Starts the RTOS scheduler. After calling the RTOS kernel has control over which tasks are executed and when.

The [idle task](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task) and optionally the [timer daemon task](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task) 
are created automatically when the RTOS scheduler is started.

`vTaskStartScheduler()` will only return if there is insufficient [RTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) available
to create the idle or timer daemon tasks.

All the RTOS demo application projects contain examples of using `vTaskStartScheduler()`, normally
in the `main()` function within main.c.


**Example usage:** 

```c
void vAFunction( void )
{
    // Tasks can be created before or after starting the RTOS scheduler
    xTaskCreate( vTaskCode,
                 "NAME",
                 STACK_SIZE,
                 NULL,
                 tskIDLE_PRIORITY,
                 NULL );

    // Start the real time scheduler.
    vTaskStartScheduler();

    // Will not get here unless there is insufficient RAM.
}
```
