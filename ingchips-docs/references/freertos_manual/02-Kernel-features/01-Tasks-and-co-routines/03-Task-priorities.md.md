[[More about tasks...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines)]

The [FreeRTOS Tutorial Books](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book) provide additional detailed information on
tasks and their behaviour.


### Task Priorities

Each task is assigned a priority from 0 to ( configMAX_PRIORITIES - 1 ), where configMAX_PRIORITIES
is defined within FreeRTOSConfig.h.

If the port in use implements a port optimised task selection mechanism that uses a 'count leading zeros'
type instruction (for task selection in a single instruction) and configUSE\_PORT\_OPTIMISED\_TASK\_SELECTION
is set to 1 in FreeRTOSConfig.h, then configMAX\_PRIORITIES cannot be higher than 32. In all other cases
configMAX\_PRIORITIES can take any value within reason - but for reasons of RAM usage efficiency should
be kept to the minimum value actually necessary.

Low priority numbers denote low priority tasks. The [idle task](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task) has priority zero (tskIDLE\_PRIORITY).

The FreeRTOS scheduler ensures that tasks in the Ready or Running [state](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states) will always
be given processor (CPU) time in preference to tasks of a lower priority that are also in the ready state.
In other words, the task placed into the Running state is always the highest priority task that is able to run.

Any number of tasks can share the same priority. If configUSE\_TIME\_SLICING is not defined, or if
configUSE\_TIME\_SLICING is set to 1, then Ready state tasks of equal priority will share the available
processing time using a time sliced round robin scheduling scheme.
