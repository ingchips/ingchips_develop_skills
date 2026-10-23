# Task Creation

## Modules

- [xTaskCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)
- [xTaskCreateStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
- [xTaskCreateRestrictedStatic](https://www.freertos.org/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/02-xTaskCreateRestrictedStatic)
- [vTaskDelete](https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete)


## Detailed Description

### TaskHandle_t

task.h

Type by which tasks are referenced. For example, a call to `xTaskCreate` returns (via a pointer parameter) 
an `TaskHandle_t` variable that can then be used as a parameter to `vTaskDelete` to delete the task.
