# RTOS Context Switch - Step 6

[[Detailed Example](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## Restore the TaskB context

![AtoB5.gif](https://www.freertos.org/media/2018/AtoB5.gif)

portRESTORE_CONTEXT() completes by restoring the TaskB context from its stack into the appropriate processor registers.

Only the program counter remains on the stack.

Next: [RTOS Implementation - Detailed Example Step 7](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/08-Step-7)
