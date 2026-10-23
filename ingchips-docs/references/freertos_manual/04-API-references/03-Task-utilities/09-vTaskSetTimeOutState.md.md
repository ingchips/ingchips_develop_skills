# vTaskSetTimeOutState()

[[Task Utilities](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h

```c
void vTaskSetTimeOutState( TimeOut_t * const pxTimeOut );
```

This function is intended for advanced users only.

A task can enter the Blocked state to wait for an event. Typically, the task will not wait in the Blocked 
state indefinitely, but instead a timeout period will be specified. The task will be removed from the 
Blocked state if the timeout period expires before the event the task is waiting for occurs.

If a task enters and exits the Blocked state more than once while it is waiting for the event to occur 
then the timeout used each time the task enters the Blocked state must be adjusted to ensure the total 
of all the time spent in the Blocked state does not exceed the originally specified timeout 
period. `xTaskCheckForTimeOut()` performs the adjustment, taking into account occasional occurrences such 
as tick count overflows, which would otherwise make a manual adjustment prone to error.

`vTaskSetTimeOutState()` is used with `xTaskCheckForTimeOut()`. `vTaskSetTimeOutState()` is called to set 
the initial condition, after which `xTaskCheckForTimeOut()` can be called to check for a timeout condition, 
and adjust the remaining block time if a timeout has not occurred.


**Parameters:** 

- *pxTimeOut*

  A pointer to a structure that will be initialized to hold information necessary to determine if a timeout has occurred.


**Example usage:**

An example is provided on the [xTaskCheckForTimeOut()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/10-xTaskCheckForTimeOut)
documentation page.
  
