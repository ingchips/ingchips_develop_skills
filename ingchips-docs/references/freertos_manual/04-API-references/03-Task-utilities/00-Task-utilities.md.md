# Task Utilities

## Modules

* [uxTaskGetSystemState](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)
* [vTaskGetInfo](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-vTaskGetInfo)
* [xTaskGetCurrentTaskHandle](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [xTaskGetIdleTaskHandle](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [uxTaskGetStackHighWaterMark](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)
* [eTaskGetState](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [pcTaskGetName](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [xTaskGetHandle](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [xTaskGetTickCount](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [xTaskGetTickCountFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [xTaskGetSchedulerState](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [uxTaskGetNumberOfTasks](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [vTaskList](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [vTaskListTasks](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [vTaskStartTrace](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [ulTaskEndTrace](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [vTaskGetRunTimeStats](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [vTaskGetRunTimeStatistics](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [vTaskGetIdleRunTimeCounter](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [ulTaskGetRunTimeCounter](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [ulTaskGetRunTimePercent](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [ulTaskGetIdleRunTimeCounter](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [ulTaskGetIdleRunTimePercent](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
* [vTaskSetApplicationTaskTag](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/06-vTaskSetApplicationTag)
* [xTaskGetApplicationTaskTag](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/03-xTaskGetApplicationTaskTag)
* [xTaskCallApplicationTaskHook](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/05-xTaskCallApplicationTaskHook)
* [pvTaskGetThreadLocalStoragePointer](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/08-pvTaskGetThreadLocalStoragePointer)
* [vTaskSetThreadLocalStoragePointer](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/07-vTaskSetThreadLocalStoragePointer)
* [vTaskSetTimeOutState](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/09-vTaskSetTimeOutState)
* [xTaskCheckForTimeOut](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/10-xTaskCheckForTimeOut)
* [vTaskResetState](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)

### xTaskGetCurrentTaskHandle

task.h

```c
TaskHandle_t xTaskGetCurrentTaskHandle( void );
```

`INCLUDE_xTaskGetCurrentTaskHandle` or `configUSE_RECURSIVE_MUTEXES` must be set to 1 for this function to be available.

**Returns:**

- The handle of the currently running (calling) task.

---

### xTaskGetIdleTaskHandle

task.h

```c
TaskHandle\_t xTaskGetIdleTaskHandle( void );
```

`INCLUDE_xTaskGetIdleTaskHandle` must be set to 1 for this function to be available.

**Returns:**

- The task handle associated with the Idle task. The Idle task is created automatically when the RTOS scheduler is started.

---

### eTaskGetState

task.h

```c
eTaskState eTaskGetState( TaskHandle_t xTask );
```

Returns as an enumerated type the state in which a task existed at the time `eTaskGetState()` was executed.

`INCLUDE_eTaskGetState` must be set to 1 in FreeRTOSConfig.h for `eTaskGetState()` to be available.

See also [vTaskGetInfo()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-vTaskGetInfo).

**Parameters:**

- *xTask*

The handle of the subject task (the task being queried).

**Returns:**

The table below lists the value that `eTaskGetState()` will return for each
possible state that the task referenced by the `xTask` parameter can exist in.

| **State** | **Returned Value** |
| --- | --- |
|  Ready  | eReady  |
|  Running  | eRunning (the calling task is querying its own priority)  |
|  Blocked  | eBlocked  |
|  Suspended  | eSuspended  |
|  Deleted  | eDeleted (the tasks TCB is waiting to be cleaned up)  |

---

### pcTaskGetName

task.h

```c
char * pcTaskGetName( TaskHandle_t xTaskToQuery );
```

Looks up the name of a task from the task's handle.

**Parameters:**

- *xTaskToQuery*

  The handle of the task being queried. xTaskToQuery can be set to NULL to query the name of the calling task.

**Returns:**

- A pointer to the subject task's name, which is a standard NULL terminated C string.

---

### xTaskGetHandle

task.h

```c
TaskHandle_t xTaskGetHandle( const char *pcNameToQuery );
```

Looks up the handle of a task from the task's name.

NOTE: This function takes a relatively long time to complete and should only be
called once for each task. Once the handle of a task has been obtained it can be
stored locally for re-use.

`INCLUDE_xTaskGetHandle` must be set to 1 in FreeRTOSConfig.h for `xTaskGetHandle()` to be available.

**Parameters:**

- *pcNameToQuery*

  The text name (as a standard C NULL terminated string) of the task for which the handle will be returned.

  See the `pcName` parameter of the [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) and [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
  API functions for information on setting the text name of a task.

**Returns:**

- If a task that has the name passed in `pcNameToQuery` can be located then
  the handle of the task is returned, otherwise NULL is returned.

---

### xTaskGetTickCount

task.h

```c
volatile TickType_t xTaskGetTickCount( void );
```

This function cannot be called from an ISR. Use `xTaskGetTickCountFromISR()` instead.

**Returns:**

- The count of ticks since vTaskStartScheduler was called.

---

### xTaskGetTickCountFromISR

task.h

```c
volatile TickType_t xTaskGetTickCountFromISR( void );
```

A version of xTaskGetTickCount() that can be called from an ISR.

**Returns:**

- The count of ticks since vTaskStartScheduler was called.

---

### xTaskGetSchedulerState

task.h

```c
BaseType_t xTaskGetSchedulerState( void );
```

**Returns:**

- One of the following constants (defined within task.h): `taskSCHEDULER_NOT_STARTED`, `taskSCHEDULER_RUNNING`, `taskSCHEDULER_SUSPENDED`.

`INCLUDE_xTaskGetSchedulerState` or `configUSE_TIMERS` must be set to 1 in FreeRTOSConfig.h for this function to be available.

---

### uxTaskGetNumberOfTasks

task.h

```c
UBaseType_t uxTaskGetNumberOfTasks( void );
```

**Returns:**

- The number of tasks that the RTOS kernel is currently managing. This includes all ready, blocked and
  suspended tasks. A task that has been deleted but not yet freed by the idle task will also be included
  in the count.

---

### vTaskList

task.h

```c
void vTaskList( char *pcWriteBuffer );
```

`configUSE_TRACE_FACILITY` and `configUSE_STATS_FORMATTING_FUNCTIONS` must be
defined as 1 in FreeRTOSConfig.h for this function to be available.
See the [configuration section](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) for more information.

NOTE: This function will disable interrupts for its duration. It is not intended
for normal application runtime use but as a debug aid.

`vTaskList()` calls [uxTaskGetSystemState()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState), then formats the raw data generated
by `uxTaskGetSystemState()` into a human readable (ASCII) table that shows the state of each task, including
the task's stack high water mark (the smaller the high water mark number the closer the task has come to
overflowing its stack).

[Click here to see an example of the output generated](https://www.freertos.org/media/2018/log.gif).

In the ASCII table the following letters are used to denote the state of a task:

* 'B' - Blocked
* 'R' - Ready
* 'D' - Deleted (waiting clean up)
* 'S' - Suspended, or Blocked without a timeout

`vTaskList()` is a utility function provided for convenience only. It is not considered part of the kernel.
See [vTaskGetRunTimeStats()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) for a utility function that generates a similar
table of run time task utilisation information.

**Parameters:**

- *pcWriteBuffer*

  A buffer into which the above mentioned details will be written, in ASCII form. This buffer is assumed
  to be large enough to contain the generated report. Approximately 40 bytes per task should be sufficient.

---

### vTaskListTasks

task.h

```c
void vTaskListTasks( char *pcWriteBuffer, size_t uxBufferLength );
```

`configUSE_TRACE_FACILITY` and `configUSE_STATS_FORMATTING_FUNCTIONS` must be
defined as 1 in FreeRTOSConfig.h for this function to be available.
See the [configuration section](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) for more information.

NOTE: This function will disable interrupts for its duration. It is not intended
for normal application runtime use but as a debug aid.

`vTaskListTasks()` calls [uxTaskGetSystemState()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState), then formats the raw data generated
by `uxTaskGetSystemState()` into a human readable (ASCII) table that shows the state of each task, including
the task's stack high water mark (the smaller the high water mark number the closer the task has come to
overflowing its stack).

[Click here to see an example of the output generated](https://www.freertos.org/media/2018/log.gif).

In the ASCII table the following letters are used to denote the state of a task:

* 'B' - Blocked
* 'R' - Ready
* 'D' - Deleted (waiting clean up)
* 'S' - Suspended, or Blocked without a timeout

`vTaskListTasks()` is a utility function provided for convenience only. It is not considered part of the kernel.

**Parameters:**

- *pcWriteBuffer*

  A buffer into which the above mentioned details will be written, in ASCII form. This buffer is assumed
  to be large enough to contain the generated report. Approximately 40 bytes per task should be sufficient.

- *uxBufferLength*

  Length of the pcWriteBuffer.

---

### vTaskStartTrace

task.h

```c
void vTaskStartTrace( char * pcBuffer, unsigned long ulBufferSize );
```

[The function relates to the legacy trace utility - which was removed in FreeRTOS V7.1.0 - users may
find the newer [Trace Hook Macros](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature) easier and more powerful to use.]

Starts a RTOS kernel activity trace. The trace logs the identity of which task is running when.

The trace file is stored in binary format. A separate DOS utility called convtrce.exe is used to convert
this into a tab delimited text file which can be viewed and plotted in a spread sheet.

**Parameters:**

- *pcBuffer*

  The buffer into which the trace will be written.

- *ulBufferSize*

  The size of pcBuffer in bytes. The trace will continue until either the buffer in full, or `ulTaskEndTrace()`
  is called.

---

### ulTaskEndTrace

task.h

```c
unsigned long ulTaskEndTrace( void );
```

[The function relates to the legacy trace utility - which was removed in FreeRTOS V7.1.0 - users may
find the newer [Trace Hook Macros](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature) easier and more powerful to use.]

Stops an RTOS kernel activity trace. See vTaskStartTrace().


**Returns:**

- The number of bytes that have been written into the trace buffer.

---

### vTaskGetRunTimeStats

task.h

```c
void vTaskGetRunTimeStats( char *pcWriteBuffer );
```

See the [Run Time Stats](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics) page for a full description of this feature.

`configGENERATE_RUN_TIME_STATS`, `configUSE_STATS_FORMATTING_FUNCTIONS` and `configSUPPORT_DYNAMIC_ALLOCATION`
must all be defined as 1 for this function to be available. The application must also then provide definitions
for `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` and `portGET_RUN_TIME_COUNTER_VALUE` to configure a peripheral
timer/counter and return the timer's current count value respectively. The counter should be at least 10 times
the frequency of the tick count.

NOTE: This function will disable interrupts for its duration. It is
not intended for normal application runtime use but as a debug aid.

`vTaskGetRunTimeStats()` calls [uxTaskGetSystemState()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState),
then formats the raw data generated by `uxTaskGetSystemState()` into a human
readable (ASCII) table that shows the amount of time each task has spent in the
Running state (how much CPU time each task has consumed). The data is provided
as both an absolute and a percentage value. The resolution of the absolute value
is dependent on the frequency of the run time stats clock provided by the application.

`vTaskGetRunTimeStats()` is a utility function provided for convenience only. It is not
considered part of the kernel. See [vTaskList()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
for a utility function that generates information on the state of each task.

**Parameters:**

- *pcWriteBuffer*

  A buffer into which the execution times will be written, in ASCII form. This buffer is assumed to
  be large enough to contain the generated report. Approximately 40 bytes per task should be sufficient.

---

### vTaskGetRunTimeStatistics

task.h

```c
void vTaskGetRunTimeStatistics( char *pcWriteBuffer, size_t uxBufferLength );
```

See the [Run Time Stats](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics) page for a full description of this feature.

`configGENERATE_RUN_TIME_STATS`, `configUSE_STATS_FORMATTING_FUNCTIONS` and `configSUPPORT_DYNAMIC_ALLOCATION`
must all be defined as 1 for this function to be available. The application must also then provide definitions
for `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` and `portGET_RUN_TIME_COUNTER_VALUE` to configure a peripheral
timer/counter and return the timer's current count value respectively. The counter should be at least 10 times
the frequency of the tick count.

NOTE: This function will disable interrupts for its duration. It is
not intended for normal application runtime use but as a debug aid.

`vTaskGetRunTimeStats()` calls [uxTaskGetSystemState()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState),
then formats the raw data generated by `uxTaskGetSystemState()` into a human
readable (ASCII) table that shows the amount of time each task has spent in the
Running state (how much CPU time each task has consumed). The data is provided
as both an absolute and a percentage value. The resolution of the absolute value
is dependent on the frequency of the run time stats clock provided by the application.

`vTaskGetRunTimeStatistics()` is a utility function provided for convenience only. It is not
considered part of the kernel. See [vTaskListTasks()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)
for a utility function that generates information on the state of each task.

**Parameters:**

- *pcWriteBuffer*

  A buffer into which the execution times will be written, in ASCII form. This buffer is assumed to
  be large enough to contain the generated report. Approximately 40 bytes per task should be sufficient.

- *uxBufferLength*

  Length of the pcWriteBuffer.

---

### vTaskGetIdleRunTimeCounter

task.h

```c
TickType_t xTaskGetIdleRunTimeCounter( void );
```

Returns the run-time counter for the Idle task. This function can be used to determine how much CPU time
the idle task receives. See the [Run Time Stats](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics) page for a full description of
the run-time-stats feature.

`configGENERATE_RUN_TIME_STATS` and `INCLUDE_xTaskGetIdleTaskHandle` must both be defined as 1 for this
function to be available. The application must also then provide definitions for `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
and `portGET_RUN_TIME_COUNTER_VALUE` to configure a peripheral timer/counter and return the timer's current
count value respectively. It is recommended to make the timer at least 10 times the frequency of the tick count.

**Returns:**
  The run-time counter for the Idle task. This function can be used to determine how much CPU time the idle task receives.
  See the [Run Time Stats](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics) page for a full description of the run-time-stats feature.

---

### ulTaskGetRunTimeCounter

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetRunTimeCounter( const TaskHandle_t xTask );
```

`configGENERATE_RUN_TIME_STATS` must both be defined as 1 for this function to be available.
The application must also then provide definitions for `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
and `portGET_RUN_TIME_COUNTER_VALUE()` to configure a peripheral timer/counter and return the timer's current
count value respectively. The counter should be at least 10 times the frequency of the tick count.

Setting `configGENERATE_RUN_TIME_STATS` to 1 will result in a total accumulated execution time being stored for each task.
`ulTaskGetRunTimeCounter()` returns the total execution time of the given task.

**Returns:**
  The total run time of the given task. This is the amount of time the task has actually been executing.
  The unit of time is dependent on the frequency configured using the
  `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` and `portGET_RUN_TIME_COUNTER_VALUE()` macros.

---

### ulTaskGetRunTimePercent

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetRunTimePercent( const TaskHandle_t xTask );
```

`configGENERATE_RUN_TIME_STATS` must both be defined as 1 for this function to be available.
The application must also then provide definitions for `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
and `portGET_RUN_TIME_COUNTER_VALUE()` to configure a peripheral timer/counter and return the timer's current
count value respectively. The counter should be at least 10 times the frequency of the tick count.

Setting `configGENERATE_RUN_TIME_STATS` to 1 will result in a total accumulated execution time being stored for each task.
`ulTaskGetRunTimePercent())` returns the percentage of the CPU time used by the given task.

**Returns:**
  The percentage of the CPU time used by the given task.

---

### ulTaskGetIdleRunTimeCounter

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetIdleRunTimeCounter( void );
```

`configGENERATE_RUN_TIME_STATS` must both be defined as 1 for this function to be available.
The application must also then provide definitions for `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
and `portGET_RUN_TIME_COUNTER_VALUE()` to configure a peripheral timer/counter and return the timer's current
count value respectively. The counter should be at least 10 times the frequency of the tick count.

Setting `configGENERATE_RUN_TIME_STATS` to 1 will result in a total accumulated execution time being stored for each task.
`ulTaskGetIdleRunTimeCounter()` returns the total execution time of the Idle task.

Note the amount of idle time is only a good measure of the slack time in a system
if there are no other tasks executing at the idle priority, tickless idle is not used, and configIDLE_SHOULD_YIELD is set to 0.

**Returns:**
  The total run time of the Idle task. This is the amount of time the Idle task has actually been executing.
  The unit of time is dependent on the frequency configured using the `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
  and `portGET_RUN_TIME_COUNTER_VALUE()` macros.

---

### ulTaskGetIdleRunTimePercent

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetIdleRunTimePercent( void );
```

`configGENERATE_RUN_TIME_STATS` must both be defined as 1 for this function to be available.
The application must also then provide definitions for `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
and `portGET_RUN_TIME_COUNTER_VALUE()` to configure a peripheral timer/counter and return the timer's current
count value respectively. The counter should be at least 10 times the frequency of the tick count.

Setting `configGENERATE_RUN_TIME_STATS` to 1 will result in a total accumulated execution time being stored for each task.
`ulTaskGetIdleRunTimePercent()` returns the percentage of the CPU time used by the Idle task.

Note the amount of idle time is only a good measure of the slack time in a system if
there are no other tasks executing at the idle priority, tickless idle is not used, and `configIDLE_SHOULD_YIELD` is set to 0.

**Returns:**
  The percentage of the CPU time used by the Idle task.

---

### vTaskResetState

task.h

```c
void vTaskResetState( void );
```

This function resets the internal state of the task module. It must be called by the application before restarting the scheduler.

---

