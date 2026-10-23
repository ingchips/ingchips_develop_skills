# FreeRTOS stream & message buffers

[[Stream Buffers and Message Buffers](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)]

[**Available From FreeRTOS V10.0.0**](https://www.freertos.org/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)

## Introduction

Stream buffers allow a stream of bytes to be passed from an interrupt service routine to a task, or
from one task to another task. A byte stream can be of arbitrary length and does not necessarily have
a beginning or end. Any number of bytes can be written in one go, and any number of bytes can be
read in one go. Data is passed by copy - the data is copied into the buffer by the sender and out of
the buffer by the read.

Unlike most other FreeRTOS communications primitives, stream buffers are optimised for single reader
single writer scenarios, such as passing data from an interrupt service routine to a task, or
from one microcontroller core to another on a dual core CPU.

Stream buffer functionality is enabled by including the FreeRTOS/source/stream_buffer.c
source file in the build.

The stream buffer implementation uses [direct to task notifications](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications). Therefore,
calling a stream buffer API function that places the calling task into the Blocked state can change the
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

### Getting Started

The **FreeRTOS/Demo/Common/Minimal/StreamBufferInterrupt.c** source file
provides a heavily commented example of how to use a stream buffer to pass data
from an interrupt service routine to a task.

See the [stream buffer section](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API) of the user documentation for a list of stream buffer
related API functions, in many cases including code snippets that demonstrate the functions being used.

## Blocking Reads and Trigger Levels

[xStreamBufferReceive()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/05-xStreamBufferReceive) is used to read data out of a stream buffer from an RTOS
task. [xStreamBufferReceiveFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/06-xStreamBufferReceiveFromISR)) is used to read data out of a stream
buffer from an interrupt service routine (ISR).

xStreamBufferReceive() allows a block time to be specified. If a non zero block time is specified when a
task uses xStreamBufferReceive() to read from a stream buffer that happens to be empty the task will be
placed into the Blocked state (so it is not consuming any CPU time and other tasks can run) until either
a specified amount of data becomes available in the stream buffer, or the block time expires. The amount
of data that must be in the stream buffer before a task that is waiting for data is removed from the blocked
state is called the stream buffer's Trigger Level. For example:

- If a task is blocked on a read of an empty stream buffer that has a
  trigger level of 1 then the task will be unblocked when a single byte is
  written to the buffer or the task's block time expires.
- If a task is blocked on a read of an empty stream buffer that has a
  trigger level of 10 then the task will not be unblocked until the stream
  buffer contains at least 10 bytes or the task's block time expires.

If a reading task's block time expires before the trigger level is reached then the task will still
receive however many bytes are actually available.

**Notes:**

- It is not valid to set the trigger level to 0. Attempting to set the
  trigger level to 0 will result in a trigger level of 1 being used.

- It is also not valid to specify a trigger level that is greater than the
  stream buffer's size.

The stream buffer's trigger level is initially set when the stream buffer is [created](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/01-xStreamBufferCreate),
and can then be changed using the [xStreamBufferSetTriggerLevel()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/10-xStreamBufferSetTriggerLevel) API function.

## Blocking Writes

[xStreamBufferSend()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/03-xStreamBufferSend)) is used to send data to a stream buffer from an RTOS
task. [xStreamBufferSendFromISR()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/08-Stream-buffers/04-xStreamBufferSendFromISR)) is used to send data to a stream buffer from
an interrupt service routine (ISR).

If a non zero block time is specified when a task uses xStreamBufferSend() to
write to a stream buffer that happens to be full the task will be placed into
the Blocked state (so it is not consuming any CPU time and other tasks can run)
until either space becomes available in the stream buffer, or the block time
expires.

## Send Complete and Receive Complete Callbacks

[Also see the [blog on using message buffers for dual core - core to core communication](https://www.freertos.org/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers).]

Stream and message buffers execute a callback upon completion of each send and receive operation:

- Stream and message buffers created using the xStreamBufferCreate() and xMessageBufferCreate() API functions
  (and their statically allocated equivalents) share the same callback functions, which are defined using the
  sbSEND_COMPLETED() and sbRECEIVE_COMPLETED() macros. The following sections provide more information on these macros.

- Stream and message buffers created using the xStreamBufferCreateWithCallback() and xMessageBufferCreateWithCallback()
  API functions (and their statically allocated equivalents) can each have their own unique callback function.

### sbSEND_COMPLETED() (and sbSEND_COMPLETED_FROM_ISR())

sbSEND_COMPLETED() is a macro that is called (internally within the FreeRTOS API functions) when data is
written to a stream buffer created using the xStreamBufferCreate() or xStreamBufferCreateStatic()
API. It takes a single parameter, which is the handle of the stream buffer that was updated.

By default (if the application writer doesn't provide their own implementation of the
macro) sbSEND_COMPLETED() checks to see if there is a task blocked on the stream
buffer to wait for data, and if so, removes the task from the Blocked state.

It is possible for the application writer to change this default behaviour by providing their
own implementation of sbSEND_COMPLETED() in FreeRTOSConfig.h. That is useful
when a stream buffer is used to pass data between cores on a multicore processor. In
that scenario, sbSEND_COMPLETED() can be implemented to generate an interrupt in
the other CPU core, and the interrupt's service routine can then use the
xStreamBufferSendCompletedFromISR() API function to check, and if necessary
unblock, a task that was waiting for the data.

The FreeRTOS/Demo/Common/Minimal/MessageBufferAMP.c source file provides a heavily
commented example of exactly that scenario.

Create the stream buffer using the xStreamBufferCreateStaticWithCallback() or
xStreamBufferCreateStaticWithCallback() API functions if you need each stream buffer
to have its own “send completed” behaviour.

### sbRECEIVE_COMPLETED() (and sbRECEIVE_COMPLETED_FROM_ISR())

sbRECEIVE_COMPLETED() is the receive equivalent of sbSEND_COMPLETED(). It is
called (internally within the FreeRTOS API functions) when data is read from a stream
buffer. By default (if the application writer doesn’t provide their own implementation of
the macro) the macro checks to see if there is a task blocked on the stream buffer to
wait for space to become available within the buffer, and if so, removes the task from
the Blocked state.

Just as with sbSEND_COMPLETED(), the application writer can change the default
behaviour of sbRECEIVE_COMPLETED() by providing an alternative implementation in
FreeRTOSConfig.h. Create the stream buffer using the
xStreamBufferCreateWithCallback() or xStreamBufferCreateStaticWithCallback() API
functions if you need each stream buffer to have its own "receive completed" behaviour.
