<!-- user_guide: 5 Dive Into SDK -->

# Chapter 5 Dive Into SDK {#dive-into-sdk}

This chapter discusses some important topics that are critical to use SDK efficiently.

## 5.1 Memory Management {#memory-management}

There are mainly three type of memory management methods:

1. Statically allocated global variables
2. Dynamically allocated and freed on stack
3. Manually allocated and freed on heap

RAM is shared between platform and user applications. When a new project is created by `Wizard`, RAM settings is configured properly. Developers are not suggested to modify these settings.

### 5.1.1 Global Variables {#global-variables}

This is the *recommended* way to define variables that have a full lift span in the app. They are allocated in the fixed location and their content can be checked easily in debugger.

### 5.1.2 Using Stack {#using-stack}

For variables that are only used within a limited scope, such as a function, we can allocated them on stack.

Cares must be taken that size of stack is limited, and it might overflow if too much memory is allocated.

1. The `app_main` function & interrupts serving routines shares the same global stack with platform’s `main` function.

   For RTOS bundles, this stack is defined in platform binaries as `1024` bytes, and can be replaced by a user defined one with the help of `platform_install_isr_stack`.

   For “NoOS” bundles, this stack is defined in app binariy as usual.
2. Callback functions registered into Bluetooth stack shares the same task stack with the stack task, whose size is defined as `1024` bytes, and about half is left to be used by app.
3. Developers can create new tasks by calling RTOS APIs. In these cases, stack size should be carefully examined.

Use tools to check required stack maximum depth of functions.

### 5.1.3 Using Heap {#using-heap}

Generally, heap is not a recommended way for memory management in embedded applications. There are several cons included but not limited to:

- Space Overhead

  Some bytes are *wasted* to store extra information and extra program.
- Time Overhead

  It costs cycles to allocate and free memory blocks.
- Fragmentation

Based on these considerations, the heap used by `malloc` & `free` has been totally disabled by setting its size to `0`. If such heap is *TRULY* required, it can be re-enabled by changing its size to a proper value when creating projects. Be sure to check follow alternatives before using `malloc` & `free`:

- Use global variables
- Use memory pool[21](#fn21)

  This is probably the choice for most cases.
- Use `FreeRTOS`’s heap and memory functions, `pvPortMalloc` & `pvPortFree`

  Note that this heap is used by platform & `FreeRTOS` itself, and it may not have too much free space left for apps. The standard `malloc` & `free` can be configured to be overridden and backed by `pvPortMalloc` & `pvPortFree` when setting up heap in `Wizard`. Once overridden, the allocator from libc is omitted, and `malloc` & `free` are implemented by `pvPortMalloc` & `pvPortFree` respectively.

## 5.2 Multitasking {#multitasking}

It is recommend to have a check on *Mastering the FreeRTOS™ Real Time Kernel*. Some tips:

1. Do not do too much processing in interrupt handlers, but defer it to tasks as soon as possible
2. Callback functions registered into Bluetooth stack are executed in the context of the stack task, so do not do too much processing in these functions either
3. Use message passing function `btstack_push_user_msg` or other special functions[22](#fn22) to get synchronized with Bluetooth stack (see [Inter-task Communication](https://ingchips.github.io/user_guide/tutorial.html#inter-task-comm))

## 5.3 Interrupt Management {#interrupt-management}

To create traditional ISR for interrupts, apps only need to register callback functions through a platform API [`platform_set_irq_callback`](https://ingchips.github.io/user_guide/api-ref.html#platform_set_irq_callback).

Apps can use following APIs to modify interrupts configuration and states:

- `NVIC_SetPriority`

  Note that the highest allowed priority is `configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY + 2`, i.e. that priority parameter must be *larger* than or *equal* to this value, indicating a *lower* or *equal* priority.
- `NVIC_EnableIRQ`
- `NVIC_DisableIRQ`
- `NVIC_ClearPendingIRQ`
- etc…

## 5.4 Power Management {#power-management}

In most case, platform manages the power saving feature of ING918xx/ING9186xx SoC automatically and tries the minimize the power consumption in all circumstances, with only one exception, *deep sleep*.

In deep sleep, all components, except those required for power saving control and real-time clocks, are powered down. Some peripherals may be used by apps, and platform does not know how to configure them. So, apps have to get involved in the waking up process after deep sleep. Platform will also check with app if deep sleep is allowed, and fall back to less aggressive power saving modes when deep sleep is not allowed.

To use deep sleep, two callback functions are needed, see [`platform_set_evt_callback`](https://ingchips.github.io/user_guide/api-ref.html#platform_set_evt_callback). To ease development & debug, power saving can be turned on or off by calling [`platform_config`](https://ingchips.github.io/user_guide/api-ref.html#platform_config).

Besides the above automatic power management schema, apps can also shutdown the whole system and reboot after a specified duration. In shutdown state the whole system has the least power consumption. See [`platform_shutdown`](https://ingchips.github.io/user_guide/api-ref.html#platform_shutdown). In shutdown state, a portion of data can be kept optionally at the cost of a little more power consumption. In case of only a little piece of data needs to be kept, SDK provides a pair of APIs for this, [`platform_write_persistent_reg`](https://ingchips.github.io/user_guide/api-ref.html#platform_write_persistent_reg) and [`platform_read_persistent_reg`](https://ingchips.github.io/user_guide/api-ref.html#platform_read_persistent_reg).

## 5.5 CMSIS API {#cmsis-api}

SDK tries to encapsulate CMSIS APIs to ease the development. Be careful when calling these APIs in apps as it may affect the platform program.

Following operations are strictly forbidden:

1. Changing the vector table offset register.
2. Modify configurations of internal interrupts.

## 5.6 Debugging & Tracing {#debugging-tracing}

Besides online debugging, SDK provides two methods to assist debugging.

1. `printf`

   `printf` is the most convenient way to check program’s behaviour. `Wizard` can generate necessary code to use `printf`.
2. Trace

   Internal state & HCI messages can be recorded through this trace machenism. `Wizard` can generate necessary code to use trace, too. There are several types of trace data, which are predefined and can’t be changed. Which types of trace data are going to be recorded is programmable. Use

   [Tracer](#ingtracer) to view the recorded trace data.

*Table 5.1: Comparison of printf and Trace*
| Debug Option | Pros | Cons |
| --- | --- | --- |
| printf | Universal | *slow* |
| Trace | Binary data, fast | Data types are predefined |

Both `printf` and trace can be directed to UART ports or SEGGER RTT[23](#fn23). Table [5.2](https://ingchips.github.io/user_guide/dive-into-sdk.html#tab:ch3-port-compare) is a comparison of these two transport options.

*Table 5.2: Comparison of UART and SEGGER RTT*
| Transport Option | Pros | Cons |
| --- | --- | --- |
| UART | Universal, easy to use | Slower, consume more CPU cycles |
| SEGGER RTT | Fast | J-Link is required, hard to capture power up log |

### 5.6.1 Tips on SEGGER RTT {#tips-on-segger-rtt}

- Use `J-LINK RTT Viewer` to view `printf` outputs in real-time.
- Use `J-LINK RTT Logger` to record trace outputs to files.

  This logger will ask for the settings of RTT. Device name is “CORTEX-M3”. Target interface is “SWD”. RTT Control Block address is the address of a variable named `_SEGGER_RTT`, which can be found in `.map` file. RTT channel index is `0`. Blow is a sample session.

  ```
  ------------------------------------------------------------

  Device name. Default: CORTEX-M3 >
  Target interface. > SWD
  Interface speed [kHz]. Default: 4000 kHz >
  RTT Control Block address. Default: auto-detection > 0x2000xxxx
  RTT Channel name or index. Default: channel 1 > 0
  Output file. Default: RTT_<ChannelName>_<Time>.log >

  ------------------------------------------------------------
  Connected to:
    J-Link ...
    S/N: ...

  Searching for RTT Control Block...OK. 1 up-channels found.
  RTT Channel description:
    Index: 0
    Name:  Terminal
    Size:  500 bytes.

  Output file: .....log

  Getting RTT data from target. Press any key to quit.
  ```

  Alternativaly, this tool can be called from command line. Address of`_SEGGER_RTT` can be specified by a range, and the tool will search for it automatically. For examples,

  ```shell
  JLinkRTTLogger.exe -If SWD -Device CORTEX-M3 -Speed 4000
  -RTTSearchRanges "0x20005000 0x8000"
  -RTTChannel 0
  file_name
  ```

### 5.6.2 Memory Dump {#memory-dump}

We are committed to delivery high quality platform binary. If an assertion or hard fault had occurred in platform binary, it is suggested to create a full memory dump and save all registers. Check out Developers’ Guide for addresses of all memory regions. After a dump is got, use [Axf Tool](https://ingchips.github.io/user_guide/core-tools.html#ch2-axf-tool) to analyze it. If the problem can not be resolved, contact technical support.

Memory can be dumped through debuggers:

- Keil μVision

  In debug session, open the Command Window, use `save` to save each memory region. Take ING918xx as an example:

  ```
  save sysm.hex  0x20000000,0x2000FFFF
  save share.hex 0x400A0000,0x400AFFFF
  ```
- J-Link Commander

  Once connected, use `regs` to shows all current register values, and `savebin` to save target memory into binary file. Take ING918xx as an example:

  ```
  savebin sysm.bin  0x20000000 0x10000
  savebin share.bin 0x400A0000 0x10000
  ```
- IAR Embedded Workbench

  In debug session, open a Memory window, and select “Memory Save …” from popup menu.
- Rowley Crossworks for ARM & SEGGER Embedded Studio for ARM

  In debug session, open a Memory window, for each memory region:

  1. Fill in the start address and size;
  2. Use “Memory Save …” from popup menu.
- GDB (GNU Arm Embedded Toolchain)

  In GDB debug session, use `dump` command to save each memory region.

Memory can be also dumped by a piece of specific code. For example, in the event handler of `PLATFORM_CB_EVT_ASSERTION`, dump all memory data to UART.

---

1. <a id="fn21"></a>[https://en.wikipedia.org/wiki/Memory_pool](https://en.wikipedia.org/wiki/Memory_pool)[↩︎](https://ingchips.github.io/user_guide/dive-into-sdk.html#fnref21)
2. <a id="fn22"></a>`btstack_push_user_runnable`. See *Thread Safety* in *Developer’s Guide for Bluetooth LE*.[↩︎](https://ingchips.github.io/user_guide/dive-into-sdk.html#fnref22)
3. <a id="fn23"></a>[https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/](https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/)[↩︎](https://ingchips.github.io/user_guide/dive-into-sdk.html#fnref23)