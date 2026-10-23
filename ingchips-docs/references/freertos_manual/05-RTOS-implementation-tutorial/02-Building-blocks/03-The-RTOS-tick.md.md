# The RTOS Tick

[[RTOS Implementation Building Blocks](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks)]

When sleeping, an RTOS task will specify a time after which it requires 'waking'.
When blocking, an RTOS task can specify a maximum time it wishes to wait.
The FreeRTOS real time kernel measures time using a **tick** count variable. A timer interrupt
(the RTOS **tick interrupt**) increments the tick count with strict temporal accuracy -
allowing the real time kernel to measure time to a resolution of the chosen timer interrupt frequency.

Each time the tick count is incremented the real time kernel must check to see if it is now time to unblock or wake a task.
It is possible that a task woken or unblocked during the tick ISR will have a priority higher than that of the
interrupted task. If this is the case the tick ISR should return to the newly woken/unblocked task - effectively interrupting
one task but returning to another. This is depicted below:

![TickISR.gif](https://www.freertos.org/media/2018/TickISR.gif)

Referring to the numbers in the diagram above:

- At (1) the RTOS idle task is executing.
- At (2) the RTOS tick occurs, and control transfers to the tick ISR (3).
- The RTOS tick ISR makes vControlTask ready to run, and as vControlTask has a higher priority than the RTOS idle task,
  switches the context to that of vControlTask.
- As the execution context is now that of vControlTask, exiting the ISR (4) returns control to vControlTask,
  which starts executing (5).

A context switch occurring in this way is said to be **Preemptive**, as the interrupted task is preempted without
suspending itself voluntarily.

The AVR port of FreeRTOS uses a compare match event on timer 1 to generate the RTOS tick.
The following pages describe how the RTOS tick ISR is implemented using the WinAVR development tools.

Next: [RTOS Implementation - The GCC Signal Attribute](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/05-GCC-signal-attribute)
