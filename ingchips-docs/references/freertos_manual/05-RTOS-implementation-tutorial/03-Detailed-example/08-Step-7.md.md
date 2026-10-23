# RTOS Context Switch - Step 7

[[Detailed Example](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## The RTOS tick exits

vPortYieldFromTick() returns to SIG_OUTPUT_COMPARE1A() where the final instruction is a return from interrupt (RETI).
A RETI instruction assumes the next value on the stack is a return address placed onto the stack when the interrupt occurred.

![AtoB6.gif](https://www.freertos.org/media/2018/AtoB6.gif)

When the RTOS tick interrupt started the AVR automatically placed the TaskA return address onto the stack - the address of the
next instruction to execute in **TaskA**. The RTOS tick handler altered the stack pointer so it now points to the **TaskB**
stack. Therefore the return address POP'ed from the stack by the RETI instruction is actually the address of the instruction **TaskB**
was going to execute immediately before it was suspended.

The RTOS tick interrupt interrupted **TaskA**, but is returning to **TaskB** - the context switch is complete!
