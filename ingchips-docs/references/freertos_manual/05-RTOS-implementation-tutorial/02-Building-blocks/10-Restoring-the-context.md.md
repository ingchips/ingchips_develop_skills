# Restoring the Context

[[RTOS Implementation Building Blocks](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks)]

The RTOS macro portRESTORE_CONTEXT() is the reverse of portSAVE_CONTEXT(). The context of the task
being resumed was previously stored in the tasks stack. The real time kernel retrieves the stack pointer
for the task then POP's the context back into the correct processor registers.

```c
#define portRESTORE_CONTEXT()
asm volatile (
  "lds r26, pxCurrentTCB nt" (1)
  "lds r27, pxCurrentTCB + 1 nt" (2)
  "ld r28, x+ nt"
  "out __SP_L__, r28 nt" (3)
  "ld r29, x+ nt"
  "out __SP_H__, r29 nt" (4)
  "pop r31 nt"
  "pop r30 nt"

 :
 :
 :

  "pop r1 nt"
  "pop r0 nt" (5)
  "out __SREG__, r0 nt" (6)
  "pop r0 nt" (7)
);
```

Referring to the code above:

- The FreeRTOS pxCurrentTCB variable holds the address from where the tasks stack pointer can be retrieved.
  This is loaded into the X register (1 and 2).
- The stack pointer for the task being resumed is loaded into the AVR stack pointer, first the low byte (3), then the high
  nibble (4).
- The processor registers are then popped from the stack in reverse numerical order, down to R1.
- The status register stored on the stack between registers R1 and R0, so is restored (6) before R0 (7).

Next: [RTOS Implementation - Putting It All Together](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/01-Putting-it-all-together)
