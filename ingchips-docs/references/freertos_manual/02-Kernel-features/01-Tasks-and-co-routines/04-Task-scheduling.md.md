# FreeRTOS scheduling (single-core, AMP and SMP)

This page provides an overview of the FreeRTOS scheduling algorithm for single-core, asymmetric multicore (AMP), 
and symmetric multicore (SMP) RTOS configurations. The scheduling algorithm is the software routine that 
decides which RTOS task should be in the [Running state](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states). There can only be one task in 
the Running state per processor core at any given time. AMP is where 
each [processor core runs its own instance of FreeRTOS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32H7_Dual_Core_AMP_RTOS_demo). SMP is where there 
is [one instance of FreeRTOS that schedules RTOS tasks across multiple cores](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction).

The free-to-download [FreeRTOS book](https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book) contains a more complete
description of the base FreeRTOS scheduling algorithm, with diagrams and examples.


## The default RTOS scheduling policy (single-core)

By default, FreeRTOS uses a fixed-priority preemptive
scheduling policy, with round-robin time-slicing of [equal priority tasks](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities):


* "Fixed priority" means the scheduler will not permanently change the priority of a
  task, although it may temporarily boost the priority of a task due to 
  [priority inheritance](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes).
  
* "Preemptive" means the scheduler always runs the highest priority RTOS task that is able to run,
  regardless of when a task becomes able to run.  For example, if an interrupt
  service routine (ISR) changes the highest priority task that is able to run, the
  scheduler will stop the currently running lower priority task and start the
  higher priority task - even if that occurs within a
  time slice.  In this case, the lower priority task is said to have been
  "preempted" by the higher priority task.
  
* "Round-robin" means tasks that share a priority take turns entering the Running state.
  
* "Time sliced" means the scheduler will switch between tasks of equal priority on each
  tick interrupt - the time between tick interrupts being one time slice. (The tick
  interrupt is the periodic interrupt used by the RTOS to measure time.)


#### Using a prioritised preemptive scheduler - avoiding task starvation

A consequence of always running the highest priority task that is able to run is that a high priority 
task that never enters the [Blocked or Suspended](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states) state will permanently starve all 
lower priority tasks of any execution time.  That is one reason why, normally, it is best to create tasks
that are event-driven.  For example, if a high-priority task is waiting for an event, it should not sit 
in a loop (poll) for the event because by polling it is always running, and so never in the Blocked or 
Suspended state. Instead, the task should enter the Blocked state to wait for the event. The event can 
be sent to the task using one of the many [FreeRTOS inter-task communication and synchronisation primitives](https://www.freertos.org/Why-FreeRTOS/highlighted-features).  
Receiving the event automatically removes the higher priority task from the Blocked state. Lower priority 
tasks will run while the higher priority task is in the Blocked state.


#### Configuring the RTOS scheduling policy

The following FreeRTOSConfig.h settings change the default scheduling behaviour:

* `configUSE_PREEMPTION`

  If [configUSE\_PREEMPTION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) is 0 then preemption is off and a
  context switch will only occur if the Running state task enters the Blocked or
  Suspended state, the Running state task calls `taskYIELD()`, or an interrupt
  service routine (ISR) manually requests a context switch.
  
* `configUSE_TIME_SLICING`

  If [configUSE\_TIME\_SLICING](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) is 0 then time slicing is off, so
  the scheduler will not switch between equal priority tasks on each tick interrupt.


## The FreeRTOS AMP scheduling policy

Asymmetric multiprocessing (AMP) with FreeRTOS is where each
core of a multicore device runs its own independent instance of FreeRTOS.  The
cores do not all need to have the same architecture, but do need to share
some memory if the FreeRTOS instances need to communicate with each other. 

Each core runs its own instance of FreeRTOS so the
scheduling algorithm on any given core is exactly as described above for a single-core
system.  You can use a [stream or message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) as the inter-core communication
primitive so that tasks on one core may enter the Blocked state to wait for data
or events sent from a different core.


## The FreeRTOS SMP scheduling policy

Symmetric multiprocessing (SMP) with FreeRTOS is 
where [one instance of FreeRTOS schedules RTOS tasks across multiple processor cores](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction).
As there is only one instance of FreeRTOS running, only one port of FreeRTOS can be used at a time, so 
each core must have the same processor architecture and share the same memory space.

The FreeRTOS SMP scheduling policy uses the same algorithm
as the single-core scheduling policy but, unlike the single-core and AMP
scenarios, SMP results in more than one task being in the Running state at any
given time (there is one Running state task per core).  That means the assumption no longer holds 
that a lower priority task will only ever run when there are no higher priority
tasks that are able to run.  To understand why, consider how the SMP
scheduler will select tasks to run on a dual-core microcontroller when,
initially, there is one high priority task and two medium priority tasks which are all in 
the [Ready state](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states).  The scheduler needs to select two tasks, one for each core. 
First, the high priority task is the highest priority task that is able to run, so
it gets selected for the first core. That leaves two medium priority tasks as the
highest priority tasks that are able to run, so one gets selected for the second
core. The result is that both a high and medium priority task run simultaneously.


#### Configuring the SMP RTOS scheduling policy

The following configuration options help when moving code written for single-core or AMP RTOS configurations 
to an SMP RTOS configuration when that code relies on the assumption that a lower priority task will not run 
if there is a higher priority task that is able to run.

* `configRUN_MULTIPLE_PRIORITIES`

  If `configRUN_MULTIPLE_PRIORITIES` is set to 0 in `FreeRTOSConfig.h` then the scheduler will only run 
  multiple tasks at the same time if the tasks have the same priority. This may fix code written with 
  the assumption that only one task will run at a time, but only at the cost of losing some of the
  benefits of the SMP configuration.
  
* `configUSE_CORE_AFFINITY`

  If `configUSE_CORE_AFFINITY` is set to 1 in `FreeRTOSConfig.h`,
  then the `vTaskCoreAffinitySet()` API function can be used to define which cores
  a task can and cannot run on.  Using this, the application writer can prevent
  two tasks that make assumptions about their respective execution order from
  executing at the same time.
