# xEventGroupClearBitsFromISR()

[[Event Group API](00-Event-groups)]

event\_groups.h

```c
BaseType_t xEventGroupClearBitsFromISR(
                               EventGroupHandle_t xEventGroup,
                               const EventBits_t uxBitsToClear );
```

A version of [xEventGroupClearBits()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/07-xEventGroupClearBits) that can be called from an interrupt.
The clear operation is deferred to the RTOS daemon task - which is also known as the timer service task.
The priority of the daemon task is set by the [configTIMER\_TASK\_PRIORITY](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
setting in FreeRTOSConfig.h.

The RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the `xEventGroupClearBitsFromISR()` function to be available.


**Parameters:**

- *xEventGroup*

  The event group in which the bits are to be cleared. The event group must have previously been created
  using a call to [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).

- *uxBitsToClear*

  A bitwise value that indicates the bit or bits to clear in the event group. For example set `uxBitsToClear`
  to 0x08 to clear just bit 3. Set `uxBitsToClear` to 0x09 to clear bit 3 and bit 0.


**Returns:**

- `pdPASS` if the operation was successfully deferred to the RTOS daemon task.

- Otherwise `pdFALSE`. `pdFALSE` will only be returned if
  the [timer command queue](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task) is full.


**Example usage:**

```c
#define BIT_0	( 1 << 0 )
#define BIT_4	( 1 << 4 )

/* This code assumes the event group referenced by the
   xEventGroup variable has already been created using a call to
   xEventGroupCreate(). */
void anInterruptHandler( void )
{
    BaseType_t xSuccess;

    /* Clear bit 0 and bit 4 in xEventGroup. */
    xSuccess = xEventGroupClearBitsFromISR(
                                xEventGroup, /* The event group being updated. */
                                BIT_0 | BIT_4 );/* The bits being cleared. */

    if( xSuccess == pdPASS )
    {
        /* The command was sent to the daemon task. */
    }
    else
    {
        /* The clear bits command was not sent to the daemon task. */
    }
}
```
