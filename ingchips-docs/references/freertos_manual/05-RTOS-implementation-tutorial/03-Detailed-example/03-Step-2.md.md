# RTOS Context Switch - Step 2

[[Detailed Example](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## The RTOS tick interrupt occurs

The RTOS tick occurs just as TaskA is about to execute an LDI instruction. When the interrupt occurs the AVR
microcontroller automatically places the current program counter (PC) onto the stack before jumping to the
start of the RTOS tick ISR.

![AtoB2.gif](https://www.freertos.org/media/2018/AtoB2.gif)

Next: [RTOS Implementation - Detailed Example Step 3](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/04-Step-3)
