# vGrantAccessTo / vRevokeAccessTo

[[FreeRTOS-MPU Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

mpu\_wrappers.h

## Overview

The `vGrantAccessTo*` and `vRevokeAccessTo*` family of macros control which
unprivileged tasks are permitted to use a particular kernel object. They are
part of the Access Control List (ACL) mechanism introduced in FreeRTOS V10.6.0
alongside the new MPU wrappers (v2).

These macros are available when all three of the following configuration options
are set:

```c
#define portUSING_MPU_WRAPPERS          1
#define configUSE_MPU_WRAPPERS_V1       0
#define configENABLE_ACCESS_CONTROL_LIST 1
```

## API Variants

Each macro grants or revokes a specific task's access to a specific kernel
object type. All variants share the same signature pattern:

```c
vGrantAccessTo<Type>( TaskHandle_t xTask, <Handle_t> xObjectToGrantAccess );
vRevokeAccessTo<Type>( TaskHandle_t xTask, <Handle_t> xObjectToRevokeAccess );
```

The full set of macros is:

| Macro | Object Type |
|-------|-------------|
| `vGrantAccessToTask` / `vRevokeAccessToTask` | Task |
| `vGrantAccessToQueue` / `vRevokeAccessToQueue` | Queue |
| `vGrantAccessToQueueSet` / `vRevokeAccessToQueueSet` | Queue Set |
| `vGrantAccessToSemaphore` / `vRevokeAccessToSemaphore` | Semaphore or Mutex |
| `vGrantAccessToEventGroup` / `vRevokeAccessToEventGroup` | Event Group |
| `vGrantAccessToStreamBuffer` / `vRevokeAccessToStreamBuffer` | Stream Buffer |
| `vGrantAccessToMessageBuffer` / `vRevokeAccessToMessageBuffer` | Message Buffer |
| `vGrantAccessToTimer` / `vRevokeAccessToTimer` | Software Timer |

All macros expand to calls to `vGrantAccessToKernelObject()` or
`vRevokeAccessToKernelObject()`, which operate on opaque integer handles.

## Parameters

- *xTask*

  The handle of the task that is being granted or revoked access. Pass `NULL` to
  refer to the calling task.

- *xObjectToGrantAccess* / *xObjectToRevokeAccess*

  The handle of the kernel object (queue, semaphore, event group, etc.) to
  grant or revoke access to.

## Important Usage Rules

### When to Grant Access

Access to a kernel object **must** be granted in one of two contexts:

1. **Before the scheduler has been started** — typically in `main()` after
   creating the tasks and kernel objects but before calling
   `vTaskStartScheduler()`.

2. **By a privileged task after the scheduler has been started** — only a task
   running with elevated privilege (`portPRIVILEGE_BIT` set in its priority)
   may call `vGrantAccessTo*` at run time.

An unprivileged task cannot grant itself or other tasks access to kernel objects.

### When to Revoke Access

A privileged task **must** revoke access to a kernel object before deleting that
object. Because kernel object handles are opaque integers backed by a fixed-size
pool, a deleted object's index may be reused for a newly created object. If
access was not revoked prior to deletion, a task that previously held a grant
may inadvertently gain access to the new, unrelated object that reuses the same
index.

**In summary:** always revoke before delete to prevent accidental permissions
from index reuse.

### Who Can Call These Macros

Only **privileged** code may call these macros. This means either:

- Code executing before the scheduler starts (which runs in privileged mode).
- A task created with `portPRIVILEGE_BIT` set in its `uxPriority` field.

## Example Usage

```c
/* Handles for a queue and two unprivileged tasks. */
static QueueHandle_t xSharedQueue;
static TaskHandle_t xProducerTask;
static TaskHandle_t xConsumerTask;

void main( void )
{
    /* Create the shared queue. */
    xSharedQueue = xQueueCreate( 10, sizeof( uint32_t ) );

    /* Create unprivileged tasks using xTaskCreateRestricted(). */
    xTaskCreateRestricted( &xProducerTaskParams, &xProducerTask );
    xTaskCreateRestricted( &xConsumerTaskParams, &xConsumerTask );

    /* Grant both tasks access to the shared queue.
     * This is done before the scheduler starts, so it executes in
     * privileged mode. */
    vGrantAccessToQueue( xProducerTask, xSharedQueue );
    vGrantAccessToQueue( xConsumerTask, xSharedQueue );

    /* Start the scheduler. */
    vTaskStartScheduler();
}
```

### Revoking Access Before Deletion

```c
/* A privileged task that tears down a shared resource. */
void vPrivilegedCleanupTask( void * pvParameters )
{
    /* Revoke access from all tasks that were granted access. */
    vRevokeAccessToQueue( xProducerTask, xSharedQueue );
    vRevokeAccessToQueue( xConsumerTask, xSharedQueue );

    /* Now it is safe to delete the queue. The index can be reused
     * without risk of accidental permissions. */
    vQueueDelete( xSharedQueue );

    vTaskDelete( NULL );
}
```

### Granting Access at Run Time from a Privileged Task

```c
/* A privileged task that dynamically creates a semaphore and shares it
 * with an unprivileged worker task. */
void vPrivilegedSetupTask( void * pvParameters )
{
    SemaphoreHandle_t xSem = xSemaphoreCreateBinary();

    /* Grant access to the worker task at run time. */
    vGrantAccessToSemaphore( xWorkerTask, xSem );

    /* Signal the worker to proceed. */
    xSemaphoreGive( xSem );

    /* ... */
}
```

## Background

In FreeRTOS V10.6.0, the MPU wrappers were redesigned so that kernel object
handles are opaque integers rather than raw pointers. This prevents unprivileged
tasks from deriving memory addresses of internal kernel structures. The ACL
mechanism provides a second layer of protection: even if a task holds a valid
handle value, it cannot use the corresponding kernel object unless it has been
explicitly granted access via these macros.

See also:
- [FreeRTOS-MPU Memory Protection Unit](https://www.freertos.org/Security/04-FreeRTOS-MPU-memory-protection-unit)
- [xTaskCreateRestricted()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted)
