[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h 

```c
void vTaskEndScheduler( void );
```

NOTE: This has only been implemented for the x86 Real Mode PC port.

Stops the RTOS kernel tick. All created tasks will be automatically deleted and multitasking (either 
preemptive or cooperative) will stop. Execution then resumes from the point where `vTaskStartScheduler()` 
was called, as if `vTaskStartScheduler()` had just returned.

See the demo application file main. c in the demo/PC directory for an example that uses `vTaskEndScheduler()`.

`vTaskEndScheduler()` requires an exit function to be defined within the portable layer (see `vPortEndScheduler()` 
in port. c for the PC port). This performs hardware specific operations such as stopping the RTOS kernel tick.

`vTaskEndScheduler()` will cause all of the resources allocated by the RTOS kernel to be freed - but will not 
free resources allocated by application tasks.


**Example usage:** 

```c
void vTaskCode( void * pvParameters )
{
    for( ;; )
    {
        // Task code goes here.

        // At some point we want to end the real time kernel processing 
        // so call ...
        vTaskEndScheduler ();
    }
}

void vAFunction( void )
{
    // Create at least one task before starting the RTOS kernel.
    xTaskCreate( vTaskCode, "NAME", STACK\_SIZE, NULL, tskIDLE\_PRIORITY, NULL );

    // Start the real time kernel with preemption.
    vTaskStartScheduler();

    // Will only get here when the vTaskCode () task has called 
    // vTaskEndScheduler (). When we get here we are back to single task 
    // execution.
}
```
