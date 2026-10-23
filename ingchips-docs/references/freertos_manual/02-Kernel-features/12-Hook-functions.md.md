# Hook Functions

### Idle Hook Function

The idle task can optionally call an application defined hook (or callback) function - the idle hook.
The idle task runs at the very lowest priority, so such an idle hook function will only get executed
when there are no tasks of higher priority that are able to run. This makes the idle hook function an
ideal place to put the processor into a low power state - providing an automatic power saving whenever
there is no processing to be performed.

The idle hook will only get called if configUSE\_IDLE\_HOOK is set to 1 within FreeRTOSConfig.h. When
this is set the application must provide the hook function with the following prototype:

```c
void vApplicationIdleHook( void );
```

The idle hook is called repeatedly as long as the idle task is running. It is paramount that the idle
hook function does not call any API functions that could cause it to block. Also, if the application makes
use of the vTaskDelete() API function then the idle task hook must be allowed to periodically return (this
is because the idle task is responsible for cleaning up the resources that were allocated by the RTOS
kernel to the task that has been deleted).

---

### Tick Hook Function

The tick interrupt can optionally call an application defined hook (or callback) function - the tick hook.
The tick hook provides a convenient place to implement timer functionality.

The tick hook will only get called if configUSE\_TICK\_HOOK is set to 1 within FreeRTOSConfig.h. When this
is set the application must provide the hook function with the following prototype:

```c
void vApplicationTickHook( void );
```

vApplicationTickHook() executes from within an ISR so must be very short, not use much stack, and not
call any API functions that don't end in "FromISR" or "FROM\_ISR".

See the [demo application file crhook.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Common/Minimal/crhook.c) for an example of how to use a tick hook.

---

### Malloc Failed Hook Function

The memory allocation schemes implemented by [heap\_1.c, heap\_2.c, heap\_3.c, heap\_4.c and heap\_5.c](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
can optionally include a malloc() failure hook (or callback) function that can be configured to get called if
pvPortMalloc() ever returns NULL.

Defining the malloc() failure hook will help identify problems caused by lack of heap memory - especially when
a call to pvPortMalloc() fails within an API function.

The malloc failed hook will only get called if configUSE\_MALLOC\_FAILED\_HOOK is set to 1 within FreeRTOSConfig.h.
When this is set the application must provide the hook function with the following prototype:

```c
void vApplicationMallocFailedHook( void );
```

---

### Stack Overflow Hook Function

See the [Stack Overflow Protection](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking) page for details.

---

### Daemon Task Startup Hook

The RTOS daemon task is the same as the [Timer Service Task](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task).
Sometimes it is referred to as the daemon task because the task is now used for more than just servicing timers.

If configUSE\_DAEMON\_TASK\_STARTUP\_HOOK is set to 1 in FreeRTOSConfig.h then the
Daemon Task Startup Hook will be called as soon as the Daemon Task starts executing
for the first time. This is useful if the application includes initialisation code
that would benefit from executing after the scheduler has been started, which allows
the initialisation code to make use of the RTOS functionality.

If configUSE\_DAEMON\_TASK\_STARTUP\_HOOK is set to 1 then the application writer must
provide an implementation of the Daemon Task startup hook function with the following
name an prototype.

```c
void vApplicationDaemonTaskStartupHook( void );
```
