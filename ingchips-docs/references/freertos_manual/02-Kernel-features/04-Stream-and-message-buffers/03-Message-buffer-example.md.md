# FreeRTOS stream & message buffers

[[Stream Buffers and Message Buffers](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)]

[**Available From FreeRTOS V10.0.0**](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)

## Introduction

Message buffers allow variable length discrete messages to be passed from an interrupt service
routine to a task, or from one task to another task. For example, messages of
length 10, 20 and 123 bytes can all be written to, and read from, the same
message buffer. Unlike when using a [stream buffer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example),
a 10 byte message can only be read out as a 10 byte message, not as individual
bytes. Message buffers are built on top of stream buffers (that is, they use
the stream buffer implementation).

Data is passed through a message buffer by copy - the data is copied into the
buffer by the sender and out of the buffer by the read.

Also see the definition of the [configMESSAGE_BUFFER_LENGTH_TYPE](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
configuration parameter.

Unlike most other FreeRTOS communications primitives, stream buffers, and therefore also message buffers,
are optimised for single reader single writer scenarios, such as passing data from an interrupt service
routine to a task, or from one microcontroller core to another on a dual core CPU.

Message buffer functionality is enabled by including the FreeRTOS/source/stream_buffer.c source file
in the build.

The message buffer implementation uses [direct to task notifications](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications). Therefore,
calling a message buffer API function that places the calling task into the Blocked state can change the
calling task's notification state and value.

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

## Getting Started

The **FreeRTOS/Demo/Common/Minimal/MessageBufferAMP.c** source file
provides a heavily commented example of how to use a message buffer to pass variable
length data from one MCU core to another on a multi-core MCU. That is quite an
advanced scenario, but the mechanism for creating, sending to and receiving from
the message buffer is the same in simpler single core scenarios where, unlike
in the demo, it is not necessary
to override the [sbSEND_COMPLETE()](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) macros.

See the [message buffer section](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API) of the user documentation for a list of message
buffer related API functions, in many cases including code snippets that demonstrate the functions being used.

## Sizing a Message Buffer

To enable message buffers to handle variable sized messages the length of each message is written into
the message buffer before the message itself (that happens internally with the FreeRTOS API functions).
The length is stored in a variable, the type of which is set by the configMESSAGE_BUFFER_LENGTH_TYPE
constant in FreeRTOSConfig.h. configMESSAGE_BUFFER_LENGTH_TYPE defaults to be of type size_t
if left undefined. size_t is typically 4-bytes on a 32-bit architecture. Therefore, as an example, writing
a 10 byte message into a message buffer will actually consume 14 bytes of buffer space when
configMESSAGE_BUFFER_LENGTH_TYPE is 4-bytes. Likewise writing a 100 byte message into a message buffer
will actually store 104 bytes of buffer space.

## Blocking Reads and Writes

[xMessageBufferReceive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/05-xMessageBufferReceive)) is used to read data from a message buffer from an RTOS
task. [xMessageBufferReceiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/06-xMessageBufferReceiveFromISR)) is used to read data from a message
buffer from an interrupt service routine (ISR). [xMessageBufferSend()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/03-xMessageBufferSend)) is used to send
data to a message buffer from an RTOS task. [xMessageBufferSendFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Message-buffers/04-xMessageBufferSendFromISR)) is
used to send data to a message buffer from an interrupt service routine (ISR).

If a non zero block time is specified when a task uses xMessageBufferReceive() to read from a message buffer
that happens to be empty the task will be placed into the Blocked state (so it is not consuming any CPU time
and other tasks can run) until either data becomes available in the message buffer, or the block time expires.

If a non zero block time is specified when a task uses xMessageBufferSend() to
write to a message buffer that happens to be full the task will be placed into
the Blocked state (so it is not consuming any CPU time and other tasks can run)
until either space becomes available in the message buffer, or the block time
expires.

## Send Complete and Receive Complete Macros

As message buffers are built on stream buffers the sbSEND_COMPLETE() and sbRECEIVE_COMPLETE() macros behave
exactly as described on the [page that describes stream buffers](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example).
