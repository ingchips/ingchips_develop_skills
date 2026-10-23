# FreeRTOS co-routines

[[More about co-routines...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### Co-Routine States

Co-routines are only intended for use on very small processors that have severe RAM constraints, and would not
normally be used on 32-bit microcontrollers. A co-routine can exist in one of the following states:

* **Running**   

  When a co-routine is actually executing it is said to be in the Running state. It is currently utilising the processor.
  
* **Ready**   

  Ready co-routines are those that are able to execute (they are not blocked) but are not currently executing. 
  A co-routine may be in the Ready state because:

  1. Another co-routine of equal or higher priority is already in the Running state, or
  2. A task is in the Running state - this can only be the case if the application uses both tasks and co-routines.
     
* **Blocked**   

  A co-routine is said to be in the Blocked state if it is currently waiting for either a temporal or 
  external event. For example, if a co-routine calls crDELAY() it will block (be placed into the Blocked 
  state) until the delay period has expired - a temporal event. Blocked co-routines are not available 
  for scheduling.

There is currently no co-routine equivalent to a tasks Suspended state.

*【图】***Valid co-routine state transitions**  
