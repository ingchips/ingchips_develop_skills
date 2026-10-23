# xEventGroupGetBits()

[[Event Group API](00-Event-groups)]

event\_groups.h

```c
EventBits_t xEventGroupGetBits( EventGroupHandle_t xEventGroup );
```

Returns the current value of the event bits (event flags) in an RTOS [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups).
This function cannot be used from an interrupt. See [xEventGroupGetBitsFromISR()](10-xEventGroupGetBitsFromISR)
for a version that can be used in an interrupt.

The RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the `xEventGroupGetBits()` function to be available.


**Parameters:**

- *xEventGroup*

  The event group being queried. The event group must have previously been created using a call
  to [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).


**Returns:**

- The value of the event bits in the event group at the time `xEventGroupGetBits()` was called.
