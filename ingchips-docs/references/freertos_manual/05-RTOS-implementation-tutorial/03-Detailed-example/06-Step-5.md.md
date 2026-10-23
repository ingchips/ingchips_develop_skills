# RTOS Context Switch - Step 5

[[Detailed Example](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## The TaskB stack pointer is retrieved

![AtoB4.gif](https://www.freertos.org/media/2018/AtoB4.gif)

The TaskB context must be restored. The first thing RTOS macro portRESTORE_CONTEXT does is retrieve the TaskB stack
pointer from the copy taken when TaskB was suspended. The TaskB stack pointer is loaded into the processor stack
pointer, so now the AVR stack points to the top of the TaskB context.

Next: [RTOS Implementation - Detailed Example Step 6](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/07-Step-6)
