# FreeRTOS software timers

From this page:

- [Software timers in a nutshell](#software-timers-in-a-nutshell)
- [Efficiency considerations in software timer implementations](#efficiency-considerations-in-software-timer-implementations)
- [Important information on writing timer callback functions](#important-information-on-writing-timer-callback-functions)
- [The timer service/daemon task, and the timer command queue](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)
- [Configuring an application to use software timers](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/03-Timer-daemon-configuration)
- [One-shot timers versus auto-reload timers](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/04-One-shot-vs-auto-load)
- [Resetting a software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/05-Resetting-a-timer)
- [API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)

### Software timers in a nutshell

A software timer (or just a 'timer') allows a function to be executed at a set
time in the future. The function executed by the timer is called the timer's
callback function. The time between a timer being started, and its callback
function being executed, is called the timer's period. Put simply, the timer's
callback function is executed when the timer's period expires.

Note, a software timer must be explicitly created before it can be used.

### Efficiency considerations in software timer implementations

Software timer functionality is easy to implement, but difficult to implement
efficiently. The FreeRTOS implementation does not execute timer callback
functions from an interrupt context, does not consume **any** processing time
unless a timer has actually expired, does not add any processing overhead to the
tick interrupt, and does not walk any link list structures while interrupts are
disabled.

The timer service task (primarily) makes use of existing FreeRTOS features,
allowing timer functionality to be added to an application with minimal impact
on the size of the application's executable binary.

### Important information on writing timer callback functions

Timer callback functions execute in the context of the timer service task. It
is therefore **essential** that timer callback functions never attempt to
block. For example, a timer callback function must not call vTaskDelay(),
vTaskDelayUntil(), or specify a non zero block time when accessing a queue or a
semaphore.
