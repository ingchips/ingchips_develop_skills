# xEventGroupClearBits()

[[Event Group API](00-Event-groups)]

event\_groups.h


```c
EventBits_t xEventGroupClearBits(
                                  EventGroupHandle_t xEventGroup,
                                  const EventBits_t uxBitsToClear );
```

Clear bits (flags) within an RTOS [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups). This function cannot be called from an
interrupt. See [xEventGroupClearBitsFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/08-xEventGroupClearBitsFromISR) for a version that can be
called from an interrupt.

The RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the `xEventGroupClearBits()` function to be available.


**Parameters:**

- *xEventGroup*

  The event group in which the bits are to be cleared. The event group must have previously been created
  using a call to [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).

- *uxBitsToClear*

  A bitwise value that indicates the bit or bits to clear in the event group. For example set `uxBitsToClear`
  to 0x08 to clear just bit 3. Set `uxBitsToClear` to 0x09 to clear bit 3 and bit 0.


**Returns:**

- The value of the event group **before** the specified bits were cleared.


**Example usage:**

```c
#define BIT_0	( 1 << 0 )
#define BIT_4	( 1 << 4 )

void aFunction( EventGroupHandle_t xEventGroup )
{
    EventBits_t uxBits;

    /* Clear bit 0 and bit 4 in xEventGroup. */
    uxBits = xEventGroupClearBits(
                                   xEventGroup,  /* The event group being updated. */
                                   BIT_0 | BIT_4 ); /* The bits being cleared. */

    if( ( uxBits & ( BIT_0 | BIT_4 ) ) == ( BIT_0 | BIT_4 ) )
    {
        /* Both bit 0 and bit 4 were set before xEventGroupClearBits()
           was called. Both will now be clear (not set). */
    }
    else if( ( uxBits & BIT_0 ) != 0 )
    {
        /* Bit 0 was set before xEventGroupClearBits() was called. It will
           now be clear. */
    }
    else if( ( uxBits & BIT_4 ) != 0 )
    {
        /* Bit 4 was set before xEventGroupClearBits() was called. It will
           now be clear. */
    }
    else
    {
        /* Neither bit 0 nor bit 4 were set in the first place. */
    }
}
```
