# Semaphores

**TIP**: ['Task Notifications'](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) can provide a light weight alternative to semaphores in many situations


## Modules

* [xSemaphoreCreateBinary](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary)
* [xSemaphoreCreateBinaryStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic)
* [vSemaphoreCreateBinary](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/03-vSemaphoreCreateBinary) [use [xSemaphoreCreateBinary()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary) for new designs]
* [xSemaphoreCreateCounting](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting)
* [xSemaphoreCreateCountingStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/05-xSemaphoreCreateCountingStatic)
* [xSemaphoreCreateMutex](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)
* [xSemaphoreCreateMutexStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic)
* [xSemaphoreCreateRecursiveMutex](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)
* [xSemaphoreCreateRecursiveMutexStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/09-xSemaphoreCreateRecursiveMutexStatic)
* [vSemaphoreDelete](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/18-vSemaphoreDelete)
* [xSemaphoreGetMutexHolder](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/10-xSemaphoreGetMutexHolder)
* [xSemaphoreTake](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)
* [xSemaphoreTakeFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/13-xSemaphoreTakeFromISR)
* [xSemaphoreTakeRecursive](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/14-xSemaphoreTakeRecursive)
* [xSemaphoreGive](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive)
* [xSemaphoreGiveRecursive](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/16-xSemaphoreGiveRecursive)
* [xSemaphoreGiveFromISR](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)
* [uxSemaphoreGetCount](https://www.freertos.org/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/11-uxSemaphoreGetCount)
