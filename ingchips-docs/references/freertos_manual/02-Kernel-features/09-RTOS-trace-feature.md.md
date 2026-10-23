# Trace Hook Macros

[Also available: **FreeRTOS-Plus-Trace**, a third party trace tool for FreeRTOS - part of the FreeRTOS-Plus ecosystem](https://www.freertos.org/Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace)


### Description

Trace hook macros are a very powerful feature that permit you to collect data on how your embedded application is behaving.

Key points of interest within the FreeRTOS source code contain empty macros that an application can re-define
for the purpose of providing application specific trace facilities. The application need only implement those macros
of particular interest - with unused macros remaining empty and therefore not impacting the application timing.


### Examples

Following are some examples of how these macros can be used:

* Setting a digital output to indicate which task is executing - allowing a logic analyzer to be used to
  view and record the task execution sequence and timing.
* Similarly - setting an analogue output to a voltage that represents which task is executing - allowing
  an oscilloscope to be used to view and record the task execution sequence and timing.
* Logging task execution sequences, task timing, RTOS kernel events and API calls for offline analysis.
* Integrating RTOS kernel events into third party debuggers.


#### Example 1

The FreeRTOS task tag functionality provides a simple mechanism for setting up logging via digital or analogue outputs. For
example, the tag value can be set to a voltage that is unique to that task.
The traceSWITCHED\_IN() macro can then be defined to simply set an analogue output to the value associated with the
task being switched in. For example:

```c
 /* First task sets its tag value to 1. */
void vTask1( void *pvParameters )
{
 /* This task is going to be represented by a voltage scale of 1. */
 vTaskSetApplicationTaskTag( NULL, ( void * ) 1 );

 for( ;; )
 {
 /* Task code goes here. */
 }
}
/*************************************************/

/* Second task sets its tag value to 2. */
void vTask2( void *pvParameters )
{
 /* This task is going to be represented by a voltage scale of 2. */
 vTaskSetApplicationTaskTag( NULL, ( void * ) 2 );

 for( ;; )
 {
 /* Task code goes here. */
 }
}
/*************************************************/

/* Define the traceTASK_SWITCHED_IN() macro to output the voltage associated
   with the task being selected to run on port 0. */
#define traceTASK_SWITCHED_IN() vSetAnalogueOutput( 0, (int)pxCurrentTCB->pxTaskTag )
```


#### Example 2

API call logging can be used to record the reason a context switch occurred. RTOS kernel call logging can
be used to record the sequence in which tasks execute. For example:

```c
/* traceBLOCKING_ON_QUEUE_RECEIVE() is just one of the macros that can be used to
record why a context switch is about to occur. */
#define traceBLOCKING_ON_QUEUE_RECEIVE(xQueue)
 ulSwitchReason = reasonBLOCKING_ON_QUEUE_READ;

/* log_event() is an application defined function that logs which tasks ran when,
   and why. */
#define traceTASK_SWITCHED_OUT()
 log_event( pxCurrentTCB, ulSwitchReason );
```


### Defining

Macros that are called from within interrupts, particularly the tick interrupt, must execute quickly and
not use much stack space. Setting variables, writing to trace registers, or outputting to ports are all
acceptable. Attempting to fprintf() log data to a slow disk will not work!

Macro definitions must occur before the inclusion of FreeRTOS.h. The easiest place to define trace macros
is at the bottom of FreeRTOSConfig.h, or in a separate header file that is included from the bottom of
FreeRTOSConfig.h.

The table below describes the available macros. The macro parameters are used to indicate which task, queue,
semaphore or mutex was associated with the event being recorded.

| **Macro definition** | **Description** | **Source file** |
| --- | --- | --- |
| traceBLOCKING\_ON\_QUEUE\_PEEK( pxQueue ) | Called from within xQueuePeek() before blocking a task trying to peek an empty queue. | queue.c |
| traceBLOCKING\_ON\_QUEUE\_RECEIVE(xQueue) | Indicates that the currently executing task is about to block following an attempt to read from an empty queue, or an attempt to 'take' an empty semaphore or mutex. | queue.c |
| traceBLOCKING\_ON\_QUEUE\_SEND(xQueue) | Indicates that the currently executing task is about to block following an attempt to write to a full queue. | queue.c |
| traceBLOCKING\_ON\_STREAM\_BUFFER\_RECEIVE( xStreamBuffer ) | Called from within xStreamBufferReceive() when the stream buffer is full and a block time is specified. | stream\_buffer.c |
| traceBLOCKING\_ON\_STREAM\_BUFFER\_SEND( xStreamBuffer ) | Called from within xStreamBufferSend() when the stream buffer is full when a block time is specified. | stream\_buffer.c |
| traceCREATE\_COUNTING\_SEMAPHORE() | Called from within xSemaphoreCreateCounting() if the semaphore was successfully created. | queue.c |
| traceCREATE\_COUNTING\_SEMAPHORE\_FAILED() | Called from within xSemaphoreCreateCounting() if the semaphore was not successfully created due to insufficient heap memory being available. | queue.c |
| traceCREATE\_MUTEX(pxNewMutex) | Called from within xSemaphoreCreateMutex() if the mutex was successfully created. | queue.c |
| traceCREATE\_MUTEX\_FAILED() | Called from within xSemaphoreCreateMutex() if the mutex was not successfully created due to there being insufficient heap memory available. | queue.c |
| traceEVENT\_GROUP\_CLEAR\_BITS( xEventGroup, uxBitsToClear ) | Called from within xEventGroupClearBits() before clearing the selected event bits and returning the previous value. | event\_groups.c |
| traceEVENT\_GROUP\_CLEAR\_BITS\_FROM\_ISR( xEventGroup, uxBitsToClear ) | Called from within xEventGroupClearBitsFromISR() before calling xEventGroupClearBits() | event\_groups.c |
| traceEVENT\_GROUP\_CREATE( xEventGroup ) | Called from within xEventGroupCreate() when successfully allocating an event group. | event\_groups.c |
| traceEVENT\_GROUP\_CREATE\_FAILED() | Called from within xEventGroupCreate() when failing to allocate an event group. | event\_groups.c |
| traceEVENT\_GROUP\_DELETE( xEventGroup ) | Called from within vEventGroupDelete() before attempting to delete an event group. | event\_groups.c |
| traceEVENT\_GROUP\_SET\_BITS( xEventGroup, uxBitsToSet ) | Called from within xEventGroupSetBits() before raising the selected event bits and potentially unblocking tasks. | event\_groups.c |
| traceEVENT\_GROUP\_SET\_BITS\_FROM\_ISR( xEventGroup, uxBitsToSet ) | Called from within xEventGroupSetBitsFromISR() before calling xEventGroupSetBits(). | event\_groups.c |
| traceEVENT\_GROUP\_SYNC\_BLOCK( xEventGroup, uxBitsToSet, uxBitsToWaitFor ) | Called from within xEventGroupSync() before blocking to wait for the rendezvous bits to be set when a block time is specified. | event\_groups.c |
| traceEVENT\_GROUP\_WAIT\_BITS\_BLOCK( xEventGroup, uxBitsToWaitFor ) | Called from within xEventGroupWaitBits() before blocking to wait for the required event bits to be set. | event\_groups.c |
| traceFREE( pvAddress, uiSize ) | Called from within vPortFree() when freeing memory. | heap\_#.c |
| traceGIVE\_MUTEX\_RECURSIVE(xMutex) | Called from within xSemaphoreGiveRecursive() if the mutex was successfully 'given'. | queue.c |
| traceGIVE\_MUTEX\_RECURSIVE\_FAILED(xMutex) | Called from within xSemaphoreGiveRecursive() if the mutex was not successfully given as the calling task was not the mutex owner. | queue.c |
| traceINCREASE\_TICK\_COUNT( xTicksToJump ) | Called from within vTaskStepTick() after jumping the tick count. | tasks.c |
| traceLOW\_POWER\_IDLE\_BEGIN() | Called from within portTASK\_FUNCTION() before idling the processor. | tasks.c |
| traceLOW\_POWER\_IDLE\_END() | Called from within portTASK\_FUNCTION() after waking from idle. | tasks.c |
| traceMALLOC( pvAddress, uiSize ) | Called from within pvPortMalloc() when allocating memory. | heap\_#.c |
| traceMOVED\_TASK\_TO\_READY\_STATE(xTask) | Called when a task is transitioned into the Ready state. | tasks.c |
| tracePEND\_FUNC\_CALL( xFunctionToPend, pvParameter1, ulParameter2, ret ) | Called from within xTimerPendFunctionCall() after posting the pending function to the queue. | timers.c |
| tracePEND\_FUNC\_CALL\_FROM\_ISR( xFunctionToPend, pvParameter1, ulParameter2, ret ) | Called from within xTimerPendFunctionCallFromISR() after posting the pending function to the queue. | timers.c |
| tracePOST\_MOVED\_TASK\_TO\_READY\_STATE( pxTCB ) | Called from within the prvAddTaskToReadyList() macro after the task is successfully moved to end of the ready list. | tasks.c |
| traceQUEUE\_CREATE(pxNewQueue) | Called from within xQueueCreate() or xQueueCreateStatic() if the queue was successfully created. | queue.c |
| traceQUEUE\_CREATE\_FAILED() | Called from within xQueueCreate() or xQueueCreateStatic() if the queue was not successfully created due to there being insufficient heap memory available. | queue.c |
| traceQUEUE\_DELETE(xQueue) | Called from within vQueueDelete(). | queue.c |
| traceQUEUE\_PEEK(xQueue) | Called from within xQueuePeek() | queue.c |
| traceQUEUE\_PEEK\_FAILED( pxQueue ) | Called from within xQueuePeek() when the queue is empty even after waiting or with no wait specified. | queue.c |
| traceQUEUE\_PEEK\_FROM\_ISR( pxQueue ) | Called from within xQueuePeekFromISR() before an item is popped from the queue. | queue.c |
| traceQUEUE\_PEEK\_FROM\_ISR\_FAILED( pxQueue ) | Called from within xQueuePeekFromISR() when the queue is empty. | queue.c |
| traceQUEUE\_REGISTRY\_ADD( xQueue, pcQueueName ) | Called from within vQueueAddToRegistry() after successfully adding the queue to the registry. | queue.c |
| traceQUEUE\_RECEIVE(xQueue) | Called from within xQueueReceive() or any of the semaphore 'take' functions when the queue receive was successful. | queue.c |
| traceQUEUE\_RECEIVE\_FAILED(xQueue) | Called from within xQueueReceive() or any of the semaphore 'take' functions when the queue receive operation failed because the queue was empty (after any block time that was specified). | queue.c |
| traceQUEUE\_RECEIVE\_FROM\_ISR(xQueue) | Called from within xQueueReceiveFromISR() when the receive operation was successful. | queue.c |
| traceQUEUE\_RECEIVE\_FROM\_ISR\_FAILED(xQueue) | Called from within xQueueReceiveFromISR() when the receive operation failed due to the queue already being empty. | queue.c |
| traceQUEUE\_SEND(xQueue) | Called from within xQueueSend(), xQueueSendToFront(), xQueueSendToBack(), or any of the semaphore 'give' functions, when the queue send was successful. | queue.c |
| traceQUEUE\_SEND\_FAILED(xQueue) | Called from within xQueueSend(), xQueueSendToFront(), xQueueSendToBack(), or any of the semaphore 'give' functions when the queue send operation failed due to the queue being full (after any block time that was specified). | queue.c |
| traceQUEUE\_SEND\_FROM\_ISR(xQueue) | Called from within xQueueSendFromISR() when the send operation was successful. | queue.c |
| traceQUEUE\_SEND\_FROM\_ISR\_FAILED(xQueue) | Called from within xQueueSendFromISR() when the send operation failed due to the queue already being full. | queue.c |
| traceTAKE\_MUTEX\_RECURSIVE(xMutex) | Called from within xQueueTakeMutexRecursive(). | queue.c |
| traceTAKE\_MUTEX\_RECURSIVE\_FAILED(xMutex) | Called from xQueueTakeMutexRecursive() when the calling task does not hold the recursive mutex and fails to take it. | queue.c |
| traceTASK\_CREATE(xTask) | Called from within xTaskCreate() (or [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)) when the task is successfully created. | tasks.c |
| traceTASK\_CREATE\_FAILED(pxNewTCB) | Called from within xTaskCreate() (or [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)) when the task was not successfully created due to there being insufficient heap space available. | tasks.c |
| traceTASK\_DELAY() | Called from within vTaskDelay(). | tasks.c |
| traceTASK\_DELAY\_UNTIL() | Called from within vTaskDelayUntil(). | tasks.c |
| traceTASK\_DELETE(xTask) | Called from within vTaskDelete(). | tasks.c |
| traceTASK\_INCREMENT\_TICK(xTickCount) | Called during the tick interrupt. | tasks.c |
| traceTASK\_NOTIFY( uxIndexToNotify ) | Called from within xTaskGenericNotify() when notifying a task about a notified value. | tasks.c |
| traceTASK\_NOTIFY\_FROM\_ISR( uxIndexToNotify ) | Called from within xTaskGenericNotifyFromISR() before notifying a task about a notified value, from ISR. | tasks.c |
| traceTASK\_NOTIFY\_GIVE\_FROM\_ISR( uxIndexToNotify ) | Called from within vTaskGenericNotifyGiveFromISR() before notifying a task about an incremented, notified value, from ISR. | tasks.c |
| traceTASK\_NOTIFY\_TAKE( uxIndexToWait ) | Called from ulTaskGenericNotifyTake() when reading and decrementing the notified value. If the value is still zero, it is unchanged. | tasks.c |
| traceTASK\_NOTIFY\_TAKE\_BLOCK( uxIndexToWait ) | Called from within ulTaskGenericNotifyTake() when the task is blocked waiting on the notified value to become non-zero. | tasks.c |
| traceTASK\_NOTIFY\_WAIT( uxIndexToWait ) | Called from xTaskGenericNotifyWait() when reading and returning the notified value. The value may be unchanged. | tasks.c |
| traceTASK\_NOTIFY\_WAIT\_BLOCK( uxIndexToWait ) | Called from xTaskGenericNotifyWait() when the task is blocked and waiting on a notified value. | tasks.c |
| traceTASK\_PRIORITY\_DISINHERIT( pxTCBOfMutexHolder, uxOriginalPriority ) | Called from within xTaskPriorityDisinherit() before decereasing the priority of a task that has since unlocked the mutex. | tasks.c |
| traceTASK\_PRIORITY\_INHERIT( pxTCBOfMutexHolder, uxInheritedPriority ) | Called from within xTaskPriorityInherit() after increasing the priority of the task holding a mutex waited on by a higher-priority task. | tasks.c |
| traceTASK\_PRIORITY\_SET(xTask,uxNewPriority) | Called from within vTaskPrioritySet(). | tasks.c |
| traceTASK\_RESUME(xTask) | Called from within vTaskResume(). | tasks.c |
| traceTASK\_RESUME\_FROM\_ISR(xTask) | Called from within xTaskResumeFromISR(). | tasks.c |
| traceTASK\_SUSPEND(xTask) | Called from within vTaskSuspend(). | tasks.c |
| traceTASK\_SWITCHED\_IN() | Called after a task has been selected to run. At this point pxCurrentTCB contains the handle of the task about to enter the Running state. | tasks.c |
| traceTASK\_SWITCHED\_OUT() | Called before a new task is selected to run. At this point pxCurrentTCB contains the handle of the task about to leave the Running state. | tasks.c |
| traceTIMER\_COMMAND\_RECEIVED(pxTimer, xCommandID, xCommandValue) | Called within the timer service task each time it receives a command, before the command is actually processed. | timers.c |
| traceTIMER\_COMMAND\_SEND(pxTimer, xCommandID, xOptionalValue, xStatus) | Called from within any API function that sends a command to the timer service task, for example, xTimerReset(), xTimerStop(), etc. xStatus will be pdFAIL if the command was not successfully sent to the timer command queue. | timers.c |
| traceTIMER\_CREATE(pxNewTimer) | Called from within xTimerCreate() if the timer was successfully created. | timers.c |
| traceTIMER\_CREATE\_FAILED() | Called from within xTimerCreate() if the timer was not successfully created due to there being insufficient heap memory available. | timers.c |
| traceTIMER\_EXPIRED(pxTimer) | Called when a software timer expires, before the timer callback is executed. | timers.c |
| traceSTREAM\_BUFFER\_CREATE( xIsMessageBuffer ) | Called from within xStreamBufferGenericCreate() after successfully allocating and initializing a new stream buffer. | stream\_buffer.c |
| traceSTREAM\_BUFFER\_CREATE\_FAILED( xIsMessageBuffer ) | Called from within xStreamBufferGenericCreate() when failing to allocate a new stream buffer | stream\_buffer.c |
| traceSTREAM\_BUFFER\_CREATE\_STATIC\_FAILED( xReturn, xIsMessageBuffer ) | Called from within xStreamBufferGenericCreateStatic() when failing to specify the locations for the stream handle or storage area.  | stream\_buffer.c |
| traceSTREAM\_BUFFER\_DELETE( xStreamBuffer ) | Called from within vStreamBufferDelete() before attempting to delete the stream buffer. | stream\_buffer.c |
| traceSTREAM\_BUFFER\_RECEIVE( xStreamBuffer, xReceivedLength ) | Called from within xStreamBufferReceive() when any bytes are successfully received | stream\_buffer.c |
| traceSTREAM\_BUFFER\_RECEIVE\_FAILED( xStreamBuffer ) | Called from within xStreamBufferReceive() when no bytes are received. | stream\_buffer.c |
| traceSTREAM\_BUFFER\_RECEIVE\_FROM\_ISR( xStreamBuffer, xReceivedLength ) | Called from within xStreamBufferReceiveFromISR() after processing the receive request. | stream\_buffer.c |
| traceSTREAM\_BUFFER\_RESET( xStreamBuffer ) | Called from within xStreamBufferReset() after successfully resetting the stream buffer. | stream\_buffer.c |
| traceSTREAM\_BUFFER\_SEND( xStreamBuffer, xBytesSent ) | Called from within xStreamBufferSend() when any bytes are successfully sent and before notifying any tasks waiting on the stream buffer. | stream\_buffer.c |
| traceSTREAM\_BUFFER\_SEND\_FAILED( xStreamBuffer ) | Called from within xStreamBufferSend() when no bytes are sent. | stream\_buffer.c |
| traceSTREAM\_BUFFER\_SEND\_FROM\_ISR( xStreamBuffer, xBytesSent ) | Called from within xStreamBufferSendFromISR() after processing the send request. | stream\_buffer.c |
