# xEventGroupSync()

[[Event Group API](00-Event-groups)]

event\_groups.h

```c
EventBits_t xEventGroupSync( EventGroupHandle_t xEventGroup,
                             const EventBits_t uxBitsToSet,
                             const EventBits_t uxBitsToWaitFor,
                             TickType_t xTicksToWait );
```

Atomically set bits (flags) within an RTOS [event group](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups), then wait for a combination of
bits to be set within the same event group. This functionality is typically
used to synchronise multiple tasks (often called a task rendezvous), where each
task has to wait for the other tasks to reach a synchronisation point before proceeding.

This function cannot be used from an interrupt.

The function will return before its block time expires if the bits specified
by the `uxBitsToWait` parameter are set, or become set within that time. In
this case all the bits specified by `uxBitsToWait` will be automatically
cleared before the function returns.

The RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the `xEventGroupSync()` function to be available.


**Parameters:**

- *xEventGroup*

  The event group in which the bits are being set and tested. The event group must have previously been
  created using a call to [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).

- *uxBitsToSet*

  The bit or bits to set in the event group before determining if (and possibly waiting for), all the
  bits specified by the `uxBitsToWait` parameter are set. For example, set `uxBitsToSet` to 0x04 to set
  bit 2 within the event group.

- *uxBitsToWaitFor*

  A bitwise value that indicates the bit or bits to test inside the event group. For example, set `uxBitsToWaitFor`
  to 0x05 to wait for bits 0 and bit 2. Set `uxBitsToWaitFor` to 0x07 to wait for bit 0 and bit 1 and bit 2. Etc.

- *xTicksToWait*

  The maximum amount of time (specified in 'ticks') to wait for all the bits specified by the `uxBitsToWaitFor`
  parameter value to become set.


**Returns:**

- The value of the event group at the time either the bits being waited
  for became set, or the block time expired. Test the return value to know
  which bits were set.

  If `xEventGroupSync()` returned because its timeout
  expired then not all the bits being waited for will be set.

  If `xEventGroupSync()` returned because all the bits it was waiting for were
  set then the returned value is the event group value **before** any bits were
  automatically cleared.


**Example usage:**

```c
/* Bits used by the three tasks. */
#define TASK_0_BIT        ( 1 << 0 )
#define TASK_1_BIT        ( 1 << 1 )
#define TASK_2_BIT        ( 1 << 2 )

#define ALL_SYNC_BITS ( TASK_0_BIT | TASK_1_BIT | TASK_2_BIT )

/* Use an event group to synchronise three tasks. It is assumed this event
   group has already been created elsewhere. */
EventGroupHandle_t xEventBits;

void vTask0( void *pvParameters )
{
    EventBits_t uxReturn;
    TickType_t xTicksToWait = 100 / portTICK_PERIOD_MS;

    for( ;; )
    {
        /* Perform task functionality here. */
        **. . .**

        /* Set bit 0 in the event group to note this task has reached the
           sync point. The other two tasks will set the other two bits defined
           by ALL_SYNC_BITS. All three tasks have reached the synchronisation
           point when all the ALL_SYNC_BITS are set. Wait a maximum of 100ms
           for this to happen. */
        uxReturn = xEventGroupSync( xEventBits,
                                    TASK_0_BIT,
                                    ALL_SYNC_BITS,
                                    xTicksToWait );

        if( ( uxReturn & ALL_SYNC_BITS ) == ALL_SYNC_BITS )
        {
            /* All three tasks reached the synchronisation point before the call
               to xEventGroupSync() timed out. */
        }
    }
}

void vTask1( void *pvParameters )
{
    for( ;; )
    {
        /* Perform task functionality here. */
        **. . .**

        /* Set bit 1 in the event group to note this task has reached the
           synchronisation point. The other two tasks will set the other two
           bits defined by ALL_SYNC_BITS. All three tasks have reached the
           synchronisation point when all the ALL_SYNC_BITS are set. Wait
           indefinitely for this to happen. */
        xEventGroupSync( xEventBits, TASK_1_BIT, ALL_SYNC_BITS, portMAX_DELAY );

        /* xEventGroupSync() was called with an indefinite block time, so
           this task will only reach here if the synchronisation was made by all
           three tasks, so there is no need to test the return value. */
    }
}

void vTask2( void *pvParameters )
{
    for( ;; )
    {
        /* Perform task functionality here. */
        **. . .**

        /* Set bit 2 in the event group to note this task has reached the
           synchronisation point. The other two tasks will set the other two
           bits defined by ALL_SYNC_BITS. All three tasks have reached the
           synchronisation point when all the ALL_SYNC_BITS are set. Wait
           indefinitely for this to happen. */
        xEventGroupSync( xEventBits, TASK_2_BIT, ALL_SYNC_BITS, portMAX_DELAY );

        /* xEventGroupSync() was called with an indefinite block time, so
           this task will only reach here if the synchronisation was made by all
           three tasks, so there is no need to test the return value. */
    }
}
```
