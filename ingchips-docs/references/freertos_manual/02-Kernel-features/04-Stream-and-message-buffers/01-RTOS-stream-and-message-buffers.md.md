# FreeRTOS stream & message buffers

[**Available From FreeRTOS V10.0.0**](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)

## Introduction

Stream buffers are an [RTOS task](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines)
to RTOS task, and interrupt to task communication primitives. Unlike most other FreeRTOS communications
primitives, they are optimised for single reader single writer scenarios, such as passing data from an
interrupt service routine to a task, or from one microcontroller core to another on dual core CPUs. Data
is passed by copy - the data is copied into the buffer by the sender and out of the buffer by the read.

Stream buffers pass a continuous stream of bytes. Message buffers pass variable sized but discrete messages.
Message buffers use stream buffers for data transfer.

**IMPORTANT NOTE**: Uniquely among FreeRTOS objects, the stream buffer
implementation (so also the [message buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) implementation, as message buffers
are built on top of stream buffers) assumes there is only one task or
interrupt that will write to the buffer (the writer), and only one task or
interrupt that will read from the buffer (the reader). It is safe for the
writer and reader to be different tasks or interrupts, but, unlike other
FreeRTOS objects, it is not safe to have multiple different writers or
multiple different readers. If there are to be multiple different writers
then the application writer must serialize calls to writing API functions
(such as [xStreamBufferSend()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/03-xStreamBufferSend)). Likewise,
if there are to be multiple different readers then the application writer
must serialize calls to reading API functions (such as [xStreamBufferReceive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/05-xStreamBufferReceive)).
One way to achieve such serialization in single core or SMP kernel is to
place each API call inside a critical section and use a block time of 0.

### Further Reading

The following pages describe stream buffers and message buffers in more detail, and provide examples of
their use to implement interrupt to task and processor core to processor core communications respectively.

[More about Stream Buffers...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)

[More about Message Buffers...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)

[Blog on using message buffers for core to core communication...](https://www.freertos.org/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers)
