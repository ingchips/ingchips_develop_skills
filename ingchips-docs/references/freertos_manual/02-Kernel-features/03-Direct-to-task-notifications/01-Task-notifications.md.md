# FreeRTOS direct to task notifications

[**Available From FreeRTOS V8.2.0 <br /> <br />  Supports Multiple Notifications Per Task From V10.4.0**](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)

### Description

[Also see the blog post ["Decrease RAM Footprint and Accelerate Execution with FreeRTOS Notifications"](https://www.freertos.org/Community/Blogs/2020/decrease-ram-footprint-and-accelerate-execution-with-freertos-notifications)]

Each RTOS task has an array of _task notifications_. Each task notification has a _notification state_
that can be either 'pending' or 'not pending', and a 32-bit _notification value_. The
constant [configTASK_NOTIFICATION_ARRAY_ENTRIES](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) sets
the number of indexes in the task notification array. Prior to FreeRTOS V10.4.0 tasks only had a single
task notification, not an array of notifications.

A _direct to task notification_ is an event sent directly to a task, rather than indirectly to a task via an
intermediary object such as a queue, event group or semaphore. Sending a direct to task notification to a task
sets the state of the target task notification to 'pending'. Just as a task can block on an intermediary object
such as a semaphore to wait for that semaphore to be available, a task can block on a task notification to wait
for that notification's state to become pending.

Sending a direct to task notification to a task can also
optionally [update the value of the target notification in one of the following ways](#use-cases):

- Overwrite the value regardless of whether the receiving task has read the value being overwritten or not.
- Overwrite the value, but only if the receiving task has read the value being overwritten.
- Set one or more bits in the value.
- Increment (add one to) the value.

Calling [xTaskNotifyWait()/xTaskNotifyWaitIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) to read a notification value clears
that notification's state to 'not pending'. Notification states can also be explicitly set to 'not pending'
by calling [xTaskNotifyStateClear()/xTaskNotifyStateClearIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/09-xTaskNotifyStateClear).

**Note:** Each notification within the array operates independently - a task can only block on one
notification within the array at a time and will not be unblocked by a notification sent to any other
array index.

RTOS task notification functionality is enabled by default, and can be excluded from a build (saving 5
bytes per array index per task) by setting [configUSE_TASK_NOTIFICATIONS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
to 0 in [FreeRTOSConfig.h](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization).

**IMPORTANT NOTE:** FreeRTOS [Stream and Message Buffers](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers) use the task notification
at array index 0. If you want to maintain the state of a task notification across a call to a Stream or Message
Buffer API function then use a task notification at an array index greater than 0.

### Performance Benefits and Usage Restrictions

The flexibility of task notifications allows them to be used where otherwise it would have been necessary
to create a
separate [queue](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues), [binary semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores), [counting semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/03-Counting-semaphores)
or [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups). Unblocking an RTOS task with a direct notification is **45% faster**†
and **uses less RAM** than unblocking a task using an intermediary object such as a binary semaphore. As would
be expected, these performance benefits require some use case limitations:

1. RTOS task notifications can only be used when there is only one task that
   can be the recipient of the event. This condition is however met in the
   majority of real world use cases, such as an interrupt unblocking a task
   that will process the data received by the interrupt.

2. Only in the case where an RTOS task notification is used in place of
   a queue: While a receiving task can wait for a notification in the
   Blocked state (so not consuming any CPU time), a sending task cannot
   wait in the Blocked state for a send to complete if the send cannot
   complete immediately.

### Use Cases

Notifications are sent using the [xTaskNotifyIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify)
and [xTaskNotifyGiveIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) API functions (and
their [interrupt safe equivalents](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)),
and remain pending until the receiving RTOS task calls either of
the [xTaskNotifyWaitIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait)
or [ulTaskNotifyTakeIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) API functions.

Each of these API functions has an equivalent that does not have the "Indexed"
prefix. The non "Indexed" versions always operate on the task notification at
array index 0. For example xTaskNotifyGive( TargetTask ) is equivalent
to xTaskNotifyGiveIndexed( TargetTask, 0 ) - both increment the task notification
at index 0 of the task referenced by the task handled TargetTask.

#### Examples

- [Using RTOS task notifications as a light weight binary semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)
- [Using RTOS task notifications as a light weight counting semaphore](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)
- [Using RTOS task notifications as a light weight event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group)
- [Using RTOS task notifications as a light weight mailbox](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/05-As-mailbox)

---

†_Measured using the binary semaphore implementation from
FreeRTOS V8.1.2, compiled with GCC at -O2 optimisation, and without
configASSERT() defined. A 35% improvement can still be obtained using the improved
binary semaphore implementation found in FreeRTOS V8.2.0 and higher._
