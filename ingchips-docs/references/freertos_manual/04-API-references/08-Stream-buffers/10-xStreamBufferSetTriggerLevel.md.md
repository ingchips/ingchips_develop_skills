# xStreamBufferSetTriggerLevel()

[[RTOS Stream Buffer API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
BaseType_t xStreamBufferSetTriggerLevel( StreamBufferHandle_t xStreamBuffer,
                                         size_t xTriggerLevel );
```

A [stream buffer's](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API) trigger level is the number of bytes that must be in 
the stream buffer before a task that is blocked on the stream buffer to wait for data is moved out of 
the blocked state. For example, if a task is blocked on a read of an empty stream buffer that has a 
trigger level of 1 then the task will be unblocked when a single byte is written to the buffer or the 
task's block time expires. As another example, if a task is blocked on a read of an empty stream buffer 
that has a trigger level of 10 then the task will not be unblocked until the stream buffer contains at 
least 10 bytes or the task's block time expires. If a reading task's block time expires before the trigger 
level is reached then the task will still receive however many bytes are actually available. Setting a 
trigger level of 0 will result in a trigger level of 1 being used. It is not valid to specify a trigger 
level that is greater than the buffer size.

A trigger level is set when the stream buffer is created, and can be modified using xStreamBufferSetTriggerLevel().

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c source file in the build.


**Parameters:** 

+ *xStreamBuffer* 

  The handle of the stream buffer being updated.

+ *xTriggerLevel* 

  The new trigger level for the stream buffer.


**Returns:** 

If xTriggerLevel was less than or equal to the stream buffer's length then the trigger level will be 
updated and pdTRUE is returned. Otherwise pdFALSE is returned.
