# FreeRTOS event groups

## Event Bits (or *flags*) and Event Groups

[**TIP: 'Task Notifications' can provide a light weight alternative to event groups in many situations**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group)
 
### Event Bits (Event Flags)

Event bits are used to indicate if an event has occurred
or not. Event bits are often referred to as event *flags*. For example, an
application may:

* Define a bit (or flag) that means "A message has been received
  and is ready for processing" when it is set to 1, and "there are no
  messages waiting to be processed" when it is set to 0.

* Define a bit (or flag) that means "The application has queued a
  message that is ready to be sent to a network" when it is set to 1, and
  "there are no messages queued ready to be sent to the network" when it
  is set to 0.

* Define a bit (or flag) that means "It is time to send a heartbeat message
  onto a network" when it is set to 1, and "it is not yet time to send
  another heartbeat message" when it is set to 0.


### Event Groups

An event group is a set of event bits. Individual event bits within an event
group are referenced by a bit number. Expanding the example provided above:

* The event bit that means "A message has been received and is ready for processing"
  might be bit number 0 within an event group.

* The event bit that means "The application has queued a message that is ready to be
  sent to a network" might be bit number 1 within the same event group.

* The event bit that means "It is time to send a heartbeat message onto a
  network" might be bit number 2 within the same event group.


### Event Group and Event Bits Data Types

Event groups are referenced by variables of type EventGroupHandle\_t.

The number of bits (or flags) stored within an event group is 8 
if [configUSE\_16\_BIT\_TICKS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
is set to 1, or 24 if configUSE\_16\_BIT\_TICKS is set to 0.
The dependency on configUSE\_16\_BIT\_TICKS results from the data type used for
thread local storage in the internal implementation of tasks.

All the event bits in an event group are stored in a single unsigned variable of
type EventBits\_t. Event bit 0 is stored in bit position 0, event bit 1 is
stored in bit position 1, and so on.

The image below represents a 24-bit event group that uses three bits to
hold the three example events already described. In the image only event bit 2
is set.

![An event group containing 24 event flags](https://www.freertos.org/media/2018/24-bit-event-group.gif)   
*An event group containing 24-event bits, only three of which are in use* 


### Event Group RTOS API Functions

Event group [API functions](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups) are provided that allow a task to, 
among other things, [set](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/05-xEventGroupSetBits) one or more event bits within an 
event group, [clear](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/07-xEventGroupClearBits) one or more event bits within an event group,
and [pend](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/04-xEventGroupWaitBits) (enter the Blocked state so the
task does not consume any processing time) to wait for a set of one or more event bits
to become set within an event group.

Event groups can also be used to [synchronise](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/11-xEventGroupSync) tasks,
creating what is often referred to as a task 'rendezvous'. A task synchronisation
point is a place in application code at which a task will wait in the Blocked
state (not consuming any CPU time) until all the other tasks taking part
in the synchronisation also reached their synchronisation point.


### The Challenges an RTOS Must Overcome When Implementing Event Groups

The two main challenges an RTOS must overcome when implementing event groups are:

1. Avoiding the creation of race conditions in the user's application:   
   An event group implementation will create a race condition in the
   application if:
   
   * It is not clear who is responsible for clearing individual bits (or flags).

   * It is not clear when a bit is to be cleared.

   * It is not clear if a bit was set or clear at the time a task
     exited the API function that tested the bit's value (it could be
     that another task or interrupt has since changed the bit's state).
     
   The FreeRTOS event groups implementation removes the potential for race conditions by including built in
   intelligence to ensure setting, testing and clearing of bits appears atomic. Thread local storage and
   careful use of API function return values make this possible.

2. Avoiding non-determinism:

   The event group concept implies non-deterministic behaviour because
   it is not know how many tasks are blocked on an event group, and therefore
   it is not known how many conditions will need to be tested or tasks
   unblocked when an event bit is set.
 
   The FreeRTOS quality standards do **not** permit non-deterministic
   actions to be performed while interrupts are disabled, or from within
   interrupt service routines. To ensure these strict quality standards are
   not breached when an event bit is set:
 
   * The RTOS scheduler's locking mechanism is used to ensure
     interrupts remain enabled when an event bit is set from an RTOS task.
     
   * The centralised deferred interrupt mechanism is used to defer
     the action of setting a bit to a task when an attempt is made to
     set an event bit from an interrupt service routine.


### Example Code

Example code snippets are provided in the [API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)
documentation, and a comprehensive example is provided in the EventGroupsDemo.c
set of standard demo tasks (the source file is located in the FreeRTOS/Demo/Common/Minimal
directory of the main [FreeRTOS download](https://www.freertos.org/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)).
