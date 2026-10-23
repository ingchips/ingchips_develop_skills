# xTaskNotifyAndQuery, xTaskNotifyAndQueryIndexed

[[RTOS Task Notification API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h

```c
 BaseType_t xTaskNotifyAndQuery( TaskHandle_t xTaskToNotify,
                                 uint32_t ulValue,
                                 eNotifyAction eAction,
                                 uint32_t *pulPreviousNotifyValue );

 BaseType_t xTaskNotifyAndQueryIndexed( TaskHandle_t xTaskToNotify,
                                        UBaseType_t uxIndexToNotify,
                                        uint32_t ulValue,
                                        eNotifyAction eAction,
                                        uint32_t *pulPreviousNotifyValue );
```

See [RTOS Task Notifications](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) for more details.

xTaskNotifyAndQueryIndexed() performs the same operation as [xTaskNotifyIndexed()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) with
the addition that it also returns the target task's prior notification value (the notification value at
the time the function is called rather than when the function returns) in the additional
pulPreviousNotifyValue parameter.

xTaskNotifyAndQuery() performs the same operation as [xTaskNotify()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) with the addition that
it also returns the target task's prior notification value (the notification value as it was at the time
the function is called, rather than when the function returns) in the additional pulPreviousNotifyValue
parameter.

This function must not be called from an interrupt service routine (ISR).
Use [xTaskNotifyAndQueryFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/06-xTaskNotifyAndQueryFromISR) instead.


**Parameters:**

* *xTaskToNotify*

  The handle of the RTOS task being notified. This is the *target* task. To obtain a task's handle create the task
  using [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and make use of the pxCreatedTask parameter, or create the task
  using [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) and store the returned value, or use the task's name in a call
  to [xTaskGetHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities). The handle of the currently executing RTOS task is returned
  by the [xTaskGetCurrentTaskHandle()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function.

* *uxIndexToNotify*

  The index within the target task's array of notification values to which the notification is to be sent. uxIndexToNotify
  must be less than configTASK\_NOTIFICATION\_ARRAY\_ENTRIES.

* *ulValue*
  Used to update the notification value of the target task. See the description of the eAction parameter below.

* *eAction*

  An enumerated type that can take one of the values documented below in order to perform the associated action.

* *pulPreviousNotifyValue*

  Can be used to pass out the target task's notification value before any bits are modified by the action of xTaskNotifyAndQuery().
  pulPreviousNotifyValue is an optional parameter, and can be set to NULL if it is not required. If pulPreviousNotifyValue is not
  used then consider using [xTaskNotify()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) in place of xTaskNotifyAndQuery().


**eAction values and associated actions**

+ eNoAction

  The target task receives the event, but its notification value is not updated. In this case ulValue
  is not used.

+ eSetBits

  The notification value of the target task will be bitwise ORed with ulValue. For example, if ulValue
  is set to 0x01, then bit 0 will get set within the target task's notification value. Likewise if ulValue
  is 0x04 then bit 2 will get set in the target task's notification value. In this way the RTOS task
  notification mechanism can be used as a light weight alternative to an [event group](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups).

+ eIncrement

  The notification value of the target task will be incremented by one, making the call to xTaskNotify()
  equivalent to a call to [xTaskNotifyGive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive). In this case ulValue is not used.

+ eSetValueWithOverwrite

  The notification value of the target task is unconditionally set to ulValue. In this way the RTOS task
  notification mechanism is being used as a light weight alternative to [xQueueOverwrite()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite).

+ eSetValueWithoutOverwrite

  If the target task does not already have a notification pending then its notification value will be
  set to ulValue. If the target task already has a notification pending then its notification value is
  not updated as to do so would overwrite the previous value before it was used. In this case the call
  to xTaskNotify() fails and pdFALSE is returned. In this way the RTOS task notification mechanism is
  being used as a light weight alternative to [xQueueSend()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend) on a queue of length 1.


**Returns:**

 pdPASS is returned in all cases other than when eAction is set to
 eSetValueWithoutOverwrite and the target task's notification value
 cannot be updated because the target task already had a notification
 pending.


**Example usage:**

```c
uint32_t ulPreviousValue;

/* Set bit 8 in the 0th notification value of the task referenced
   by xTask1Handle. Store the task's previous 0th notification
   value (before bit 8 is set) in ulPreviousValue. */
xTaskNotifyAndQueryIndexed( xTask1Handle,
                            0,
                            ( 1UL << 8UL ),
                            eSetBits,
                            &ulPreviousValue );

/* Send a notification to the task referenced by xTask2Handle,
   potentially removing the task from the Blocked state, but without
   updating the task's notification value. Store the tasks notification
   value in ulPreviousValue. */
xTaskNotifyAndQuery( xTask2Handle, 0, eNoAction, &ulPreviousValue );

/* Set the notification value of the task referenced by xTask3Handle
   to 0x50, even if the task had not read its previous notification value.
   The task's previous notification value is of no interest so the last
   parameter is set to NULL. */
xTaskNotifyAndQuery( xTask3Handle, 0x50, eSetValueWithOverwrite,  NULL );

/* Set the notification value of the task referenced by xTask4Handle
   to 0xfff, but only if to do so would not overwrite the task's existing
   notification value before the task had obtained it (by a call to
   xTaskNotifyWait()) or ulTaskNotifyTake(). The task's previous
   notification value is saved in ulPreviousValue. */
if( xTaskNotifyAndQuery( xTask4Handle,
                         0xfff,
                         eSetValueWithoutOverwrite,
                         &ulPreviousValue ) == pdPASS )
{
    /* The task's notification value was updated. */
}
else
{
    /* The task's notification value was not updated. */
}
```
