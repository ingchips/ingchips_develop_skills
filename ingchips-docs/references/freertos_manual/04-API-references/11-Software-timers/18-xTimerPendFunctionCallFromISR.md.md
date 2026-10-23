# xTimerPendFunctionCallFromISR()

[[Timer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions)]

timers.h

```c
 BaseType_t xTimerPendFunctionCallFromISR(
                       PendedFunction_t xFunctionToPend,
                       void *pvParameter1,
                       uint32_t ulParameter2,
                       BaseType_t *pxHigherPriorityTaskWoken );
```

Used from application interrupt service routines to defer the execution of a
function to the RTOS daemon task (the timer service task, hence this function is
implemented in timers.c and is prefixed with 'Timer').

Ideally an interrupt service routine (ISR) is kept as short as possible, but
sometimes an ISR either has a lot of processing to do, or needs to perform
processing that is not deterministic. In these cases xTimerPendFunctionCallFromISR()
can be used to defer processing of a function to the RTOS daemon task.

A mechanism is provided that allows the interrupt to return directly to the
task that will subsequently execute the pended function. This
allows the callback function to execute contiguously in time with the
interrupt - just as if the callback had executed in the interrupt itself.

Functions that can be deferred to the RTOS daemon task must have the following
prototype:

```c
 void vPendableFunction( void * pvParameter1, uint32_t ulParameter2 );
```

The pvParameter1 and ulParameter2 are provided for use by the application code.

INCLUDE\_xTimerPendFunctionCall() and configUSE\_TIMERS must both be set to
1 for xTimerPendFunctionCallFromISR() to be available.


**Parameters:** 

+ *xFunctionToPend* 

  The function to execute from the timer service/daemon task. The function must conform to the PendedFunction\_t 
  prototype as shown above.

+ *pvParameter1* 

  The value of the callback function's first parameter. The parameter has a void \* type to allow it to be 
  used to pass any type. For example, integer types can be cast to a void \*, or the void \* can be used 
  to point to a structure.

+ *ulParameter2* 

  The value of the callback function's second parameter.

+ *pxHigherPriorityTaskWoken* 

  As mentioned above, calling xTimerPendFunctionCallFromISR() will result in a message being sent to 
  the RTOS timer daemon task. If the priority of the daemon task (which is set 
  using [configTIMER\_TASK\_PRIORITY](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) in FreeRTOSConfig.h) is 
  higher than the priority of the currently running task (the task the interrupt interrupted) 
  then \*pxHigherPriorityTaskWoken will be set to pdTRUE within xTimerPendFunctionCallFromISR(), indicating 
  that a context switch should be requested before the interrupt exits. For that reason \*pxHigherPriorityTaskWoken 
  must be initialised to pdFALSE. See the example code below.


**Returns:** 

pdPASS is returned if the message was successfully sent to the RTOS timer daemon task, otherwise pdFALSE is returned.
 

**Example usage:**

```c
/* The callback function that will execute in the context of the daemon task.
   Note callback functions must all use this same prototype. */
void vProcessInterface( void *pvParameter1, uint32_t ulParameter2 )
{
BaseType_t xInterfaceToService;

    /* The interface that requires servicing is passed in the second
       parameter. The first parameter is not used in this case. */
    xInterfaceToService = ( BaseType_t ) ulParameter2;

    /* ...Perform the processing here... */
}

/* An ISR that receives data packets from multiple interfaces */
void vAnISR( void )
{
BaseType_t xInterfaceToService, xHigherPriorityTaskWoken;

    /* Query the hardware to determine which interface needs processing. */
    xInterfaceToService = prvCheckInterfaces();

    /* The actual processing is to be deferred to a task. Request the
       vProcessInterface() callback function is executed, passing in the
       number of the interface that needs processing. The interface to
       service is passed in the second parameter. The first parameter is
       not used in this case. */
    xHigherPriorityTaskWoken = pdFALSE;
    xTimerPendFunctionCallFromISR( vProcessInterface,
                                   NULL,
                                   ( uint32_t ) xInterfaceToService,
                                   &xHigherPriorityTaskWoken );

    /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context
       switch should be requested. The macro used is port specific and will
       be either portYIELD_FROM_ISR() or portEND_SWITCHING_ISR() - refer to
       the documentation page for the port being used. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
