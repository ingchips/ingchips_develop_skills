# FreeRTOS co-routines

[[More about co-routines...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### Co-Routine Priorities

Each co-routine is assigned a priority from 0 to ( configMAX\_CO\_ROUTINE\_PRIORITIES - 1 ). 
configMAX\_CO\_ROUTINE\_PRIORITIES is defined within FreeRTOSConfig.h and can be set on an application 
by application basis.

Low priority numbers denote low priority co-routines.

Co-routine priorities are only with respect to other co-routines. Tasks will always take priority over 
co-routines should you mix tasks and co-routines within the same application.
