### What is deferred interrupt handling?

In FreeRTOS, a deferred interrupt handler refers to an RTOS task that is unblocked (triggered)
by an interrupt service routine (ISR) so the processing necessitated by the
interrupt can be performed in the unblocked task, rather than directly in the
ISR. The mechanism differs from standard interrupt processing, in which all the
processing is performed within the ISR, because the majority of the processing
is deferred until after the ISR has exited:

* **Standard ISR Processing** 

  Standard ISR processing will typically involve recording the reason for the interrupt, clearing the
  interrupt, then performing any processing necessitated by the interrupt, all within the ISR itself.

* **Deferred Interrupt Processing** 

  Deferred interrupt processing will typically involve recording the reason
  for the interrupt and clearing the interrupt within the ISR, but then
  unblocking an RTOS task so the processing necessitated by the interrupt
  can be performed by the unblocked task, rather than within the ISR.
 
  If the task to which interrupt processing is deferred is assigned a high
  enough priority then the ISR will return directly to the unblocked task
  (the interrupt will interrupt one task, but then return to a different
  task), resulting in all the processing necessitated by the interrupt being
  performed contiguously in time (without a gap), just as if all the processing
  had been performed in the ISR itself. This can be see in the image below,
  where all the interrupt processing occurs between times t2 and t4,
  even though part of the processing is performed by a task.
 
  ![Using an rtos to defer interrupt processing](https://www.freertos.org/media/2018/rtos_deferred_interrupt_processing.jpg)   
  *Deferred interrupt processing execution sequence when the deferred handling task has a high priority* 

  With reference to the image above:
 
  1. At time t2: A low priority task is pre-empted by an interrupt.

  2. At time t3: The ISR returns directly to a task that was unblocked from within
     the ISR. The majority of interrupt processing is performed within the unblocked task.

  3. At time t4: The task that was unblocked by the ISR returns to the
     Blocked state to wait for the next interrupt, allowing the lower
     priority application task to continue its execution.


### When to use deferred interrupt handling

Most embedded engineers will strive to minimise the amount of time spent inside
an ISR (to minimise jitter in the system, enable other interrupts of the same or lower
priority to execute, maximise interrupt responsiveness, etc.), and the technique
of deferring interrupt processing to a task provides a convenient method of
achieving this. However, the mechanics of first unblocking, and then switching
to, an RTOS task itself takes a finite amount of time, so typically an application
will only benefit from deferring interrupt processing if the processing:

* Needs to perform lengthy operations, or

* Would benefit from using the full RTOS API, rather than just the ISR safe API, or

* Needs to perform an action that is not deterministic, within reasonable bounds.


### Techniques for deferring interrupt processing to a task

Methods of deferring interrupts to tasks fall into two categories:

1. **Centralised Deferred Interrupt Handling** 

   Centralised deferred interrupt handling is so called because each interrupt that uses this method 
   executes in the context of the same RTOS daemon task. The RTOS daemon task is created by FreeRTOS, 
   and is also known as the [timer service task](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task).
 
   To defer interrupt processing to the RTOS daemon task pass a pointer to the interrupt processing 
   function as the xFunctionToPend parameter in a call 
   to [xTimerPendFunctionCallFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/18-xTimerPendFunctionCallFromISR) API function. See the 
   xTimerPendFunctionCallFromISR() documentation page for a worked example.
 
   Advantages of centralised deferred interrupt handling include minimal resource usage,
   as each deferred interrupt handler uses the same task.
 
   Disadvantages of centralised deferred interrupt handling include:
 
   * All the deferred interrupt handler functions execute in the context of the
     same RTOS daemon task, and therefore execute with the same RTOS
     task priority.

   * xTimerPendFunctionCallFromISR() sends pointers to the deferred
     interrupt handling functions to the RTOS daemon task over the
     timer command queue. Therefore the RTOS daemon task processes the
     functions in the order in which they are received on the queue,
     not necessarily in interrupt priority order.

   * Writing to, and then subsequently reading from, the timer command
     queue adds an additional latency.

2. **Application Controlled Deferred Interrupt Handling** 

   Application controlled deferred interrupt handling is so called because each interrupt that uses this 
   method executes in the context of a task created by the application writer. See 
   the [Using an RTOS Task Notification as a Light Weight Counting Semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)
   documentation page for a worked example.
 
   Advantages of application controlled deferred interrupt handling include:
 
   * Reduced latency (function pointers are not passed through a queue).

   * The ability to assign a different priority to each deferred
     interrupt handling RTOS task - allowing the relative priority of
     deferred interrupt task to match the relative priority of their
     respective interrupts.
    
   Disadvantages of application controlled deferred interrupt handling include
   the greater consumption of resources as typically more tasks are required.
