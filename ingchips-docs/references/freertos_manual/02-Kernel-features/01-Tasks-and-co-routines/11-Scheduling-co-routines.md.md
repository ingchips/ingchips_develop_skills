# FreeRTOS co-routines

[[More about co-routines...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### Scheduling Co-Routines

Co-routines are scheduled by repeated calls to [vCoRoutineSchedule()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/14-Co-routines/07-vCoRoutineSchedule). The best place
to call vCoRoutineSchedule() is from the [idle task hook](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task). This is the case even
if your application only uses co-routines as the idle task will still automatically be created when
the scheduler is started. [See the later examples](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Scheduling-co-routines).

---
### Mixing Tasks and Co-Routines

Scheduling co-routines from within the idle task allows tasks and co-routines to be easily mixed within
the same application. When this is done the co-routines will only execute when there are no tasks of
priority higher than the idle task that are able to execute.

[See the later examples](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Scheduling-co-routines).
