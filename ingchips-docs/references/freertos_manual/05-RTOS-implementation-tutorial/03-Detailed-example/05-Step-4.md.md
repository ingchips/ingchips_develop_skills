# RTOS Context Switch - Step 4

[[Detailed Example](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## Incrementing the Tick Count

The RTOS function vTaskIncrementTick() executes after the TaskA context has been saved. For the purposes of this example
assume that incrementing the tick count has caused TaskB to become ready to run. TaskB has a higher priority than TaskA
so vTaskSwitchContext() selects TaskB as the task to be given processing time when the ISR completes.

Next: [RTOS Implementation - Detailed Example Step 5](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/06-Step-5)
