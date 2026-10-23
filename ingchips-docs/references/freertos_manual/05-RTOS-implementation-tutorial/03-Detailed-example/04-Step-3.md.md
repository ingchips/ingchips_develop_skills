# RTOS Context Switch - Step 3

[[Detailed Example](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## The RTOS tick interrupt executes

The ISR source code is given below. The comments have been removed to ease reading, but can be viewed on a previous page.

```c
/* Interrupt service routine for the RTOS tick. */
void SIG_OUTPUT_COMPARE1A( void )
{
    vPortYieldFromTick();
    asm volatile ( "reti" );
}
/*--------------------------------------------------*/

void vPortYieldFromTick( void )
{
    portSAVE_CONTEXT();

    vTaskIncrementTick();
    vTaskSwitchContext();
    portRESTORE_CONTEXT();

    asm volatile ( "ret" );
}
/*--------------------------------------------------*/
```

SIG_OUTPUT_COMPARE1A() is a naked function, so the first instruction is a call to vPortYieldFromTick().
vPortYieldFromTick() is also a naked function so the AVR execution context is saved explicitly by a call to
portSAVE_CONTEXT().

portSAVE_CONTEXT() pushes the entire AVR execution context onto the stack of TaskA, resulting in the stack illustrated below.
The stack pointer for TaskA now points to the top of its own context. portSAVE_CONTEXT() completes by storing a copy of the
stack pointer. The real time kernel already has copy of the TaskB stack pointer - taken the last time TaskB was suspended.

![AtoB3.gif](https://www.freertos.org/media/2018/AtoB3.gif)

Next: [RTOS Implementation - Detailed Example Step 4](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/05-Step-4)
