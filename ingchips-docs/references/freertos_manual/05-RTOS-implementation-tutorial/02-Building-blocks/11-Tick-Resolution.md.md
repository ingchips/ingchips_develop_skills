# Tick Resolution

## The resolution of Ticks

As described on the [RTOS Tick documentation page](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/03-The-RTOS-tick), 
RTOS time is based upon a periodic tick interrupt. When an RTOS task wants to wait for a specific time to pass, for example by calling [vTaskDelay()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/01-vTaskDelay), 
or for an event to occur, for example by specifying a block time in a call to [xQueueReceive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/09-xQueueReceive), 
the task specifies the maximum time to block (that is, to [wait, without using any CPU cycles](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)) as a tick count. The macro pdMS_TO_TICKS() converts 
milliseconds to ticks. The requested block time starts at the time the API is called, which will be between two tick interrupts. The tick count is 
an integer that can't count partial tick periods, so the time between the API call and the next tick interrupt is counted as the first tick of the 
delay (block) period. This will result in slight differences in the observed block time (in wall-clock time) between different API calls that request 
the same block time.

The diagrams below demonstrate this using a call to vTaskDelay( 2 ) as an example, assuming a tick period of 1ms.


The first diagram shows the situation when the call to vTaskDelay() occurs immediately after a tick interrupt. The observed block time will be nearly 2 
milliseconds (most of the time between Tick 1 and Tick 2, plus all of the time between Tick 2 and Tick 3).

[![](https://www.freertos.org/media/2023/tick-diagram1.png)](/media/2023/tick-diagram1.png)


The second diagram shows the situation when the call to vTaskDelay() instead occurs immediately before a tick interrupt. The observed block time will be 
just over 1 millisecond (a small part of the time between Tick 1 and Tick 2, plus all the time between Tick 2 and Tick 3).

[![](https://www.freertos.org/media/2023/tick-diagram2.png)](/media/2023/tick-diagram2.png)


With these examples in mind, it can be seen that the actual time delayed when a delay of N ticks is specified will always fall between `(N-1 ticks * tick_period)` 
and `(N * tick_period)`. For this specific example, that means a total delay between 1.0000000001ms and 1.99999999999ms.

A few important notes regarding delay time:
-  Tick resolution is always up to the tick count specified as a parameter, but no less than `(N-1)` ticks. Essentially, the range is from `N-1` ticks to `N` ticks (non-inclusive).
-  To guarantee a minimum delay of N time, you'll need to delay for `(N / (tick_period)) + 1` ticks.
-  The duration (in time) of a delay is based on the point between RTOS ticks when the delay is called — the closer the call to the upcoming tick, the shorter the delay will be in time.