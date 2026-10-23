[[RTOS Kernel Control](https://www.freertos.org/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h 

```c
BaseType_t xTaskResumeAll( void );
```

Resumes the scheduler after it was suspended using a call to vTaskSuspendAll().

xTaskResumeAll() only resumes the scheduler. It does not unsuspend tasks
that were previously suspended by a call to vTaskSuspend().

**Returns:**

If resuming the scheduler caused a context switch then pdTRUE is returned, otherwise pdFALSE is returned.


**Example usage:**

```c
 void vTask1( void * pvParameters )
 {
     for( ;; )
     {
         /* Task code goes here. */

         /* ... */

         /* At some point the task wants to perform a long operation
            during which it does not want to get swapped out. It cannot
            use taskENTER_CRITICAL()/taskEXIT_CRITICAL() as the length
            of the operation may cause interrupts to be missed -
            including the ticks.

            Prevent the RTOS kernel swapping out the task. */
         vTaskSuspendAll();

         /* Perform the operation here. There is no need to use critical
            sections as we have all the microcontroller processing time.
            During this time interrupts will still operate and the real
            time RTOS kernel tick count will be maintained. */

         /* ... */

         /* The operation is complete. Restart the RTOS kernel. We want to force
            a context switch - but there is no point if resuming the scheduler
            caused a context switch already. */
         if( !xTaskResumeAll () )
         {
              taskYIELD ();
         }
     }
 }
```
