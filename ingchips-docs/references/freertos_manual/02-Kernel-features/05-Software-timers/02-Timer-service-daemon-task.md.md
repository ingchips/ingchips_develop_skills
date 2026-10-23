# FreeRTOS software timers

[[More about software timers...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

See also the [RTOS Daemon Task Startup Hook](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions) function.

### The timer service/daemon task, and the timer command queue

Timer functionality is optional, and not part of the core FreeRTOS kernel. It is instead
provided by a timer service (or daemon) task.

FreeRTOS provides a set of timer related API functions. Many of these functions
use a standard FreeRTOS queue to send commands to the timer service task. The
queue used for this purpose is called the 'timer command queue'. The 'timer
command queue' is private to the FreeRTOS timer implementation, and cannot be
accessed directly.

The diagram below demonstrates this scenario. The code on the left represents
a function that is part of a user application, and called from a task that is
created as part of the same user application. The code on the right represents
the timer service task implementation.
The timer command queue is the link between the application task and the timer service task.
In this demonstrated case, the xTimerReset() API function is called from the
application code. This results in a reset command being sent to the timer
command queue for processing by the timer service task. The application code
only calls the xTimerReset() API function - it does not (and cannot) access the
timer command queue directly.

![RTOS timer task and timer command queue](https://www.freertos.org/media/2018/rtos-timer-task-and-timer-command-queue.png)
The context of the application code, the FreeRTOS timer API, the timer command queue, and the timer service task.
