# xEventGroupGetBitsFromISR()

[[Event Group API](00-Event-groups)]

event\_groups.h

```c
EventBits_t xEventGroupGetBitsFromISR(
                              EventGroupHandle_t xEventGroup );
```

A version of [xEventGroupGetBits()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/09-xEventGroupGetBits) that can be called from an interrupt.

The RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the `xEventGroupGetBitsFrom()` function to be available.


**Parameters:**

- *xEventGroup*

  The event group being queried. The event group must have previously been created using a call
  to [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).


**Returns:**

- The value of the event bits in the event group at the time `xEventGroupGetBitsFromISR()`
  was called.
