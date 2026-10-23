# xEventGroupCreate()

[[Event Group API](00-Event-groups)]

[**TIP: 'Task Notifications' can provide a light weight alternative to event groups in many situations**](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group)

event\_groups.h

```c
 EventGroupHandle_t xEventGroupCreate( void );
```

Creates a new RTOS [event group](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups), and
returns a handle by which the newly created event group can be referenced.

For this RTOS API function to be available:

1. [configSUPPORT\_DYNAMIC\_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
   must be set to 1 in FreeRTOSConfig.h, or left undefined (in which case it will
   default to 1).

2. The RTOS source file FreeRTOS/source/event\_groups.c must be
   included in the build.

Each event group requires a (very) small amount of RAM that is used to hold the
event group's state. If an event group is created using `xEventGroupCreate()`
then the required RAM is automatically allocated from the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If an event group is created using [xEventGroupCreateStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/02-xEventGroupCreateStatic)()
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.

Event groups are stored in variables of type `EventBits_t`. The number of
bits (or flags) implemented within an event group is 8 if [configUSE\_16\_BIT\_TICKS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
is set to 1, or 24 if `configUSE_16_BIT_TICKS` is set to 0. The dependency on
`configUSE_16_BIT_TICKS` results from the data type used for thread local storage
in the internal implementation of RTOS tasks.


**Parameters:**

*None*


**Returns:**

- If the event group was created then a handle to the event group is returned.
- If there was insufficient [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) available to create the event group then NULL is returned.


**Example usage:**

```c
    /* Declare a variable to hold the created event group. */
    EventGroupHandle_t xCreatedEventGroup;

    /* Attempt to create the event group. */
    xCreatedEventGroup = xEventGroupCreate();

    /* Was the event group created successfully? */
    if( xCreatedEventGroup == NULL )
    {
        /* The event group was not created because there was insufficient
           FreeRTOS heap available. */
    }
    else
    {
        /* The event group was created. */
    }
```
