# FreeRTOS idle task

[[More about tasks...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview)]

The [FreeRTOS Tutorial Books](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
provide additional detailed information on tasks and their behaviour.


### The Idle Task

The idle task is created automatically when the RTOS scheduler is started to ensure there is always at least
one task that is able to run. It is created at the lowest possible [priority](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities) 
to ensure it does not use any CPU time if there are higher priority application tasks in the ready [state](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states).

The idle task is responsible for freeing memory [allocated by the RTOS](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 
to tasks that have since been deleted. It is therefore important in applications that make 
use of the [vTaskDelete()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete) function to ensure the idle task is not starved of 
processing time.
The idle task has no other active functions so can legitimately be starved of microcontroller time under all 
other conditions.

It is possible for application tasks to share the idle task priority (tskIDLE\_PRIORITY).
See the configIDLE\_SHOULD\_YIELD [configuration parameter](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) for information on how this
behaviour can be configured.


---

### The Idle Task Hook

An idle task hook is a function that is called during each cycle of the idle task. If you want application 
functionality to run at the idle priority then there are two options:

1. Implement the functionality in an idle task hook.

   There must always be at least one task that is ready to run. It is therefore imperative that the hook 
   function does not call any API functions that might cause the idle task to block (vTaskDelay(), or
   a [queue](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues) or [semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores) function with a block time, for example). It is 
   ok for co-routines to block within the hook function.

2. Create an idle priority task to implement the functionality.

   This is a more flexible solution but has a higher RAM usage overhead.

See the [Embedded software application design](https://www.freertos.org/Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design) section for more information on
using an idle hook.


To create an idle hook:

1. Set configUSE\_IDLE\_HOOK to 1 in [FreeRTOSConfig.h](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization).
2. Define a function that has the following name and prototype: `void vApplicationIdleHook( void );`

It is common to use the idle hook function to place the microcontroller CPU into a power saving mode.
