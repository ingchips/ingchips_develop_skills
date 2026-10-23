# FreeRTOS software timers

[[More about software timers...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

### Configuring an application to use software timers

To make the [FreeRTOS software timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions) available in an application,
simply:

1. Add the FreeRTOS/Source/timers.c source file to your project, and
2. Define the constants detailed in the table below in the applications FreeRTOSConfig.h header file.

**Constants**

- configUSE_TIMERS

  Set to 1 to include timer functionality. The timer service task will be automatically created as the
  RTOS scheduler starts when configUSE_TIMERS is set to 1.

- configTIMER_TASK_PRIORITY

  Sets the priority of the timer service task. Like all tasks, the timer service task can run at any
  priority between 0 and ( configMAX_PRIORITIES - 1 ).

  This value needs to be chosen carefully to meet the requirements of the application. For example, if
  the timer service task is made the highest priority task in the system, then commands sent to the timer
  service task (when a timer API function is called) and expired timers will both get processed immediately.
  Conversely, if the timer service task is given a low priority, then commands sent to the timer service
  task and expired timers will not be processed until the timer service task is the highest priority task
  that is able to run. It is worth noting here however, that timer expiry times are calculated relative to
  when a command is sent, and not relative to when a command is processed.

- configTIMER_QUEUE_LENGTH

  This sets the maximum number of unprocessed commands that the timer command queue can hold at any one
  time. Reasons the timer command queue might fill up include:

  - Making multiple timer API function calls before the RTOS scheduler has been started, and therefore
    before the timer service task has been created.
  - Making multiple (interrupt safe) timer API function calls from an interrupt service routine (ISR).
  - Making multiple timer API function calls from a task that has a priority above that of the timer service task.

- configTIMER_TASK_STACK_DEPTH

  Sets the size of the stack (in words, not bytes) allocated to the<br /> timer service task. Timer callback
  functions execute in the context of the timer service task. The stack requirement of the timer service task
  therefore depends on the stack requirements of the timer callback functions.
