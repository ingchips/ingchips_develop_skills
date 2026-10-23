# xEventGroupSetBitsFromISR()

[[Event Group API](00-Event-groups)]


event\_groups.h

```c
BaseType_t xEventGroupSetBitsFromISR(
                         EventGroupHandle_t xEventGroup,
                         const EventBits_t uxBitsToSet,
                         BaseType_t *pxHigherPriorityTaskWoken );
```

Set bits (flags) within an RTOS [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups).
A version of [xEventGroupSetBits()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/05-xEventGroupSetBits) that can
be called from an interrupt service routine (ISR).

Setting bits in an event group will automatically unblock tasks that are
blocked waiting for the bits.

Setting bits in an event group is not a deterministic operation because there
are an unknown number of tasks that may be waiting for the bit or bits being
set. FreeRTOS does not allow non-deterministic operations to be performed in
interrupts or from critical sections. Therefore `xEventGroupSetBitFromISR()`
sends a message to the RTOS daemon task to have the set operation performed in the
context of the daemon task - where a scheduler lock is used in place of a
critical section.

**NOTE:** As mentioned in the paragraph above, setting bits from an ISR will
defer the set operation to the RTOS daemon task (also known as the timer service
task). The RTOS daemon task is scheduled according to its priority, just like
any other RTOS task. Therefore, if it is essential the set operation completes
immediately (before a task created by the application executes) then the priority
of the RTOS daemon task must be higher than the priority of any application task
that uses the event group. The priority of the RTOS daemon task is set by
the [configTIMER\_TASK\_PRIORITY](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/03-Timer-daemon-configuration)
definition in FreeRTOSConfig.h.

`configUSE_TIMERS` and `INCLUDE_xTimerPendFunctionCall` must be set to 1 in
FreeRTOSConfig.h for the `xEventGroupSetBitsFromISR()` function to be available.

The RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the `xEventGroupSetBitsFromISR()` function to be available.


**Parameters:**

- *xEventGroup*

  The event group in which the bits are to be set. The event group must have previously been created
  using a call to [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).

- *uxBitsToSet*

  A bitwise value that indicates the bit or bits to set. For example, set `uxBitsToSe`t to 0x08 to set
  only bit 3. Set `uxBitsToSet` to 0x09 to set bit 3 and bit 0.

- *pxHigherPriorityTaskWoken*

  As mentioned above, calling this function will result in a message being sent to the RTOS daemon task.
  If the priority of the daemon task is higher than the priority of the currently running task (the task
  the interrupt interrupted) then `*pxHigherPriorityTaskWoken` will be set to `pdTRUE`
  by `xEventGroupSetBitsFromISR()`, indicating that a context switch should be requested before the interrupt
  exits. For that reason `*pxHigherPriorityTaskWoken` must be initialised to `pdFALSE`. See the example
  code below.


**Returns:**

- If the message was sent to the RTOS daemon task then pdPASS is returned, otherwise `pdFAIL` is
  returned. `pdFAIL` will be returned if the [timer service queue](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)
  was full.


**Example usage:**

```c
#define BIT_0    ( 1 << 0 )
#define BIT_4    ( 1 << 4 )

/* An event group which it is assumed has already been created by a call to
   xEventGroupCreate(). */
EventGroupHandle_t xEventGroup;

void anInterruptHandler( void )
{
    BaseType_t xHigherPriorityTaskWoken, xResult;

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Set bit 0 and bit 4 in xEventGroup. */
    xResult = xEventGroupSetBitsFromISR(
                                xEventGroup,   /* The event group being updated. */
                                BIT_0 | BIT_4, /* The bits being set. */
                                &xHigherPriorityTaskWoken );

    /* Was the message posted successfully? */
    if( xResult != pdFAIL )
    {
        /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context
           switch should be requested. The macro used is port specific and will
           be either portYIELD_FROM_ISR() or portEND_SWITCHING_ISR() - refer to
           the documentation page for the port being used. */
        portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
    }
}
```
