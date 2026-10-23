[[Task Utilities](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h

```c
void vTaskSetThreadLocalStoragePointer( TaskHandle_t xTaskToSet,
                                        BaseType_t xIndex,
                                        void *pvValue )
```

Sets a value in a task's [thread local storage array](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers).

This function is intended for advanced users only.


**Parameters:**

- *xTaskToSet*

  The handle of the task to which the thread local data is being written. A task can write to its own
  thread local data by using NULL as the parameter value.

- *xIndex*

  The index into the thread local storage array to which data is being written. The number of available array indexes is set by
  the [configNUM\_THREAD\_LOCAL\_STORAGE\_POINTERS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) compile time configuration
  constant in [FreeRTOSConfig.h](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization).

- *pvValue*

  The value to write into the index specified by the xIndex parameter.


**Example usage:**

See the examples provided on the [thread local storage array](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers)
documentation page.
