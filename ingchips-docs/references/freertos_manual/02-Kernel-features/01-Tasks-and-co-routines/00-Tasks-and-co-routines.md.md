# Tasks and Co-routines

See the [How FreeRTOS Works](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation) section for an introduction to basic multitasking concepts.

The [Tasks](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview)
and [Co-Routine](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)
documentation pages provide information to allow you to determine when co-routine use may and may not be
appropriate. Below is a brief summary. Note that an application can be designed using just tasks, just
co-routines, or a mixture of both - however tasks and co-routines use different API functions and therefore
a queue (or semaphore) cannot be used to pass data from a task to a co-routine or vice versa.

Co-routines are really only intended for use on very small processors that have severe RAM constraints.


### Characteristics of a 'Task'

**In brief**: A real time application that uses an RTOS can be structured as a set of independent tasks. Each task
executes within its own context with no coincidental dependency on other tasks within the system or the RTOS scheduler
itself. Only one task within the application can be executing at any point in time and the real time RTOS scheduler is
responsible for deciding which task this should be. The RTOS scheduler may therefore repeatedly start and stop each
task (swap each task in and out) as the application executes. As a task has no knowledge of the RTOS scheduler
activity it is the responsibility of the real time RTOS scheduler to ensure that the processor context (register
values, stack contents, etc) when a task is swapped in is exactly the same as when the same task was swapped out.
To achieve this each task is provided with its own stack. When the task is swapped out the execution context is
saved to the stack of that task so it can also be exactly restored when the same task is later swapped back in. See
the [How FreeRTOS Works](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation) section for more information.


#### Task Summary

+ Simple.

+ No restrictions on use.

+ Supports full preemption.

+ Fully prioritised.

+ Each task maintains its own stack resulting in higher RAM usage.

+ Re-entrancy must be carefully considered if using preemption.


### Characteristics of a 'Co-routine'

**Note:** Co-routines were implemented for use on very small devices, but are very rarely used in the field these days.
For that reason, while there are no plans to remove co-routines from the code, there are also no plans to develop them
further.

Co-routines are conceptually similar to tasks but have the following fundamental differences (elaborated further on
the [co-routine documentation page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)):

1. **Stack usage**

   All the co-routines within an application share a single stack. This greatly reduces the amount of RAM required
   compared to a similar application written using tasks.

2. **Scheduling and priorities**

   Co-routines use prioritised cooperative scheduling with respect to other co-routines, but can be included in an
   application that uses preemptive tasks.

3. **Macro implementation**

   The co-routine implementation is provided through a set of macros.

4. **Restrictions on use**

   The reduction in RAM usage comes at the cost of some stringent restrictions in how co-routines can be structured.


#### Co-Routine Summary

+ Sharing a stack between co-routines results in much lower RAM usage.

+ Cooperative operation makes re-entrancy less of an issue.

+ Very portable across architectures.

+ Fully prioritised relative to other co-routines, but can always be preempted by tasks if the two are mixed.

+ Lack of stack requires special consideration.

+ Restrictions on where API calls can be made.

+ Co-operative operation only amongst co-routines themselves.
