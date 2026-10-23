# Static Vs Dynamic Memory Allocation

### Introduction

FreeRTOS versions prior to V9.0.0 allocate the memory used by the RTOS objects
listed below from the [special FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
FreeRTOS V9.0.0 and onwards gives the application writer the ability to instead provide
the memory themselves, allowing the following objects to optionally be created without
any memory being allocated dynamically:

- Tasks
- Software Timers
- Queues
- Event Groups
- Binary Semaphores
- Counting Semaphores
- Recursive Semaphores
- Mutexes

Whether it is preferable to use static or dynamic memory allocation is dependent
on the application, and the preference of the application writer. Both methods
have pros and cons, and both methods can be used within the same RTOS application.

The simple Win32 
example [located in the FreeRTOS/Source/WIN32-MSVC-Static-Allocation-Only directory](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo) 
of the main FreeRTOS download demonstrates how a FreeRTOS application can be created without including any 
of the [FreeRTOS heap](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) implementations in a project.


### Creating an RTOS Object Using Dynamically Allocated RAM

Creating RTOS objects dynamically has the benefit of greater simplicity, and the
potential to minimise the application's maximum RAM usage:

- Fewer function parameters are required when an object is created.

- The memory allocation occurs automatically, within the RTOS API functions.

- The application writer does not need to concern themselves with allocating memory themselves.

- The RAM used by an RTOS object can be re-used if the object is deleted, potentially reducing 
  the application's maximum RAM footprint.

- RTOS API functions are provided to return information on heap usage, allowing the heap size to be 
  optimised.

- The memory allocation scheme used can be chosen to best suite the application,
  be that heap\_1.c for simplicity and determinism often necessary for
  safety critical applications, heap\_4.c for fragmentation protection, heap\_5.c
  to split the heap across multiple RAM regions, or an allocation scheme
  provided by the application writer themselves.

The following API functions, which are available 
if [configSUPPORT_DYNAMIC_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) is set to 1 or left undefined, 
create RTOS objects using dynamically allocated RAM:

- [xTaskCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)
- [xQueueCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)
- [xTimerCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate)
- [xEventGroupCreate()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate)
- [xSemaphoreCreateBinary()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary)
- [xSemaphoreCreateCounting()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting)
- [xSemaphoreCreateMutex()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)
- [xSemaphoreCreateRecursiveMutex()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)


### Creating an RTOS Object Using Statically Allocated RAM

Creating RTOS objects using statically allocated RAM has the benefit of providing the application writer 
with more control:

- RTOS objects can be placed at specific memory locations.

- The maximum RAM footprint can be determined at link time, rather than run time.

- The application writer does not need to concern themselves with graceful handling of memory allocation 
  failures.

- It allows the RTOS to be used in applications that simply don't allow any dynamic memory allocation (although 
  FreeRTOS includes allocation schemes that can overcome most objections).

The following API functions, which are available 
if [configSUPPORT_STATIC_ALLOCATION](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) is set to 1, allow RTOS objects 
to be created using memory provided by the application writer. To provide memory the application writer
simply needs to declare a variable of the appropriate object type, then pass the address of the variable into
the RTOS API function. 
The [StaticAllocation.c](https://sourceforge.net/p/freertos/code/HEAD/tree/trunk/FreeRTOS/Demo/Common/Minimal/StaticAllocation.c)
standard demo/test task is provided to demonstrate how the functions are used:

- [xTaskCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
- [xQueueCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic)
- [xTimerCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic)
- [xEventGroupCreateStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/02-xEventGroupCreateStatic)
- [xSemaphoreCreateBinaryStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic)
- [xSemaphoreCreateCountingStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/05-xSemaphoreCreateCountingStatic)
- [xSemaphoreCreateMutexStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic)
- [xSemaphoreCreateRecursiveMutexStatic()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/09-xSemaphoreCreateRecursiveMutexStatic)
