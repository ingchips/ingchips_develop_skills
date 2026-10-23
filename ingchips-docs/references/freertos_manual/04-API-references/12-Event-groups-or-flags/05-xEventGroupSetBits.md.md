# xEventGroupSetBits()

[[Event Group API](00-Event-groups)]

event\_groups.h

```c
EventBits_t xEventGroupSetBits( EventGroupHandle_t xEventGroup,
                                const EventBits_t uxBitsToSet );
```

Set bits (flags) within an RTOS [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups). This function cannot be called
from an interrupt. [xEventGroupSetBitsFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/06-xEventGroupSetBitsFromISR) is a version that can
be called from an interrupt.

Setting bits in an event group will automatically unblock tasks that are blocked waiting for the bits.

The RTOS source file FreeRTOS/source/event\_groups.c must be included in the build for the `xEventGroupSetBits()`
function to be available.


**Parameters:**

- *xEventGroup*

  The event group in which the bits are to be set. The event group must have previously been created
  using a call to [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).

- *uxBitsToSet*

  A bitwise value that indicates the bit or bits to set in the event group. For example, set `uxBitsToSet`
  to 0x08 to set only bit 3. Set `uxBitsToSet` to 0x09 to set bit 3 and bit 0.


**Returns:**

- The value of the event group **at the time the call to `xEventGroupSetBits()` returns**.

  There are two reasons why the returned value might have the bits specified by the `uxBitsToSet`
  parameter cleared:

  1. If setting a bit results in a task that was waiting for the bit leaving the blocked state then it
     is possible the bit will have been cleared automatically (see the `xClearBitOnExit` parameter
     of [xEventGroupWaitBits()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/04-xEventGroupWaitBits)).

  2. Any unblocked (or otherwise Ready state) task that has a priority above that of the task that
     called `xEventGroupSetBits()` will execute and may change the event group value before the call
     to `xEventGroupSetBits()` returns.


**Example usage:**

```c
#define BIT_0	( 1 << 0 )
#define BIT_4	( 1 << 4 )

void aFunction( EventGroupHandle_t xEventGroup )
{
    EventBits_t uxBits;

    /* Set bit 0 and bit 4 in xEventGroup. */
    uxBits = xEventGroupSetBits(
                                 xEventGroup,    /* The event group being updated. */
                                 BIT_0 | BIT_4 );/* The bits being set. */

    if( ( uxBits & ( BIT_0 | BIT_4 ) ) == ( BIT_0 | BIT_4 ) )
    {
        /* Both bit 0 and bit 4 remained set when the function returned. */
    }
    else if( ( uxBits & BIT_0 ) != 0 )
    {
        /* Bit 0 remained set when the function returned, but bit 4 was
           cleared. It might be that bit 4 was cleared automatically as a
           task that was waiting for bit 4 was removed from the Blocked
           state. */
    }
    else if( ( uxBits & BIT_4 ) != 0 )
    {
        /* Bit 4 remained set when the function returned, but bit 0 was
           cleared. It might be that bit 0 was cleared automatically as a
           task that was waiting for bit 0 was removed from the Blocked
           state. */
    }
    else
    {
        /* Neither bit 0 nor bit 4 remained set. It might be that a task
           was waiting for both of the bits to be set, and the bits were cleared
           as the task left the Blocked state. */
    }
}
```
