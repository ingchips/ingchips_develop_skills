# The AVR Context

[[RTOS Implementation Building Blocks](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks)]

A context switch requires the entire execution context to be saved. On the AVR microcontroller the context consists
of:

- 32 general purpose processor registers. The gcc development tools assume register R1 is set to zero.
- Status register. The value of the status register affects instruction execution, and must be preserved across
  context switches.
- Program counter. Upon resumption, a task must continue execution from the instruction that was about to be
  executed immediately prior to its suspension.
- The two stack pointer registers.

![AVRContext.gif](https://www.freertos.org/media/2018/AVRContext.gif)

Next: [RTOS Implementation - Saving The Context](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/09-Saving-the-RTOS-task-context)
