<!-- user_guide_cn: 5 深入 SDK -->

# 5 深入 SDK {#dive-into-sdk}

本章介绍关于高效使用 SDK 的一些关键问题。

## 5.1 内存管理 {#内存管理}

有以下三种主要的内存管理方法：

1. 全局的静态分配
2. 在栈上的动态分配和释放
3. 在堆上的动态分配和释放

RAM 由 platform 和 app 共享使用。`Wizard` 创建的新项目 RAM 的位置、大小会自动得以配置。不建议开发者修改此设置。

### 5.1.1 全局分配 {#全局分配}

对于在 app 整个生命周期都存在的变量，这是推荐的分配方式。全局变量地址固定，用调试器可以方便地检查其中的数据。

### 5.1.2 使用栈 {#使用栈}

对于仅在有限范围内——比如一个函数内部——存在的变量，我们可以在栈上分配它们。

必须注意：栈的大小是有限的，如果分配的空间过多，栈会溢出。

1. `app_main` 函数及中断服务程序与 platform 的 `main` 使用同一个全局栈。

   对于 RTOS 软件包，这个栈由 platform 定义，其大小为 `1024` 字节。如果大小不合适，可利用 `platform_install_isr_stack` 做替换。

   对于 “NoOS” 软件包，这个栈由 app 定义。
2. 蓝牙协议栈的各种回调函数与协议栈使用同一个栈，其大小为 `1024` 字节，一般情况下， 进入回调函数时大致还有一半空间空闲。
3. 开发者可以创建新的 RTOS 任务。这时，栈的大小需要仔细核对。

用工具检查函数所需要的最大栈空间（栈的深度）。

### 5.1.3 使用堆 {#使用堆}

总体而言，不太建议在嵌入式应用里使用堆管理内存。这种方法至少存在以下不足：

- 空间开销

  对于每块空间，为了存储额外的信息，若干字节被浪费。
- 时间开销

  分配、释放内存块时需要消耗时间。
- 碎片

基于以上考虑，`Wizard` 创建项目时在默认情况下，堆大小设置为 0，完全禁用了 `malloc` 和 `free`。 如果确实需要使用堆，可以在创建项目时，把堆大小修改为合适的数值。 在使用 `malloc` 和 `free` 之前，请查看以下建议：

- 使用全局变量
- 使用内存池[20](#fn20)

  这可能是一种适用于多数场景的方案。
- 使用 RTOS 的堆内存接口，如 `pvPortMalloc` 和 `pvPortFree`

  注意，这个堆由 platform 和 `FreeRTOS` 共用，留给 app 的空间可能不多。标准的 `malloc` & `free` 在 `Wizard` 的堆设置里可配置为由 `pvPortMalloc` & `pvPortFree` 实现，此时，libc 里的堆分配器不会链接到程序里， `malloc` & `free` 完全依赖 `pvPortMalloc` & `pvPortFree` 实现。

## 5.2 多任务 {#多任务}

建议先阅读《Mastering the FreeRTOS™ Real Time Kernel》。 几点建议：

1. 不要在中断服务程序里做过多处理，应该尽快延续到任务里，
2. 蓝牙协议栈的回调函数在协议栈任务的上下文里运行，所以也不要做过多处理，
3. 调用蓝牙协议栈 API （除了 `btstack_push_user_msg` 本身）之前先利用消息传递函数 `btstack_push_user_msg` 或其它特殊函数[21](#fn21) 与协议栈同步（参见 [任务间通信](https://ingchips.github.io/user_guide_cn/tutorial.html#inter-task-comm)）

## 5.3 中断管理 {#中断管理}

Apps 通过 platform API [`platform_set_irq_callback`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_set_irq_callback) 创建经典的中断服务程序。

Apps 可以使用下列 API 修改中断配置或者状态：

- `NVIC_SetPriority`

  注意，对于 RTOS 软件包，中断优先级最高为 `configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY + 2`， 也就是说，优先级参数必须**大于**或者**等于**该值，以表示 *更低* 或者 *相等* 的优先级。
- `NVIC_EnableIRQ`
- `NVIC_DisableIRQ`
- `NVIC_ClearPendingIRQ`
- 等等……

## 5.4 功耗管理 {#功耗管理}

在大多数情况下，platform 负责自动管理系统的省电功能，尽量降低功能。只有一个例外， *深睡眠*。

在深睡眠模式下，芯片内除低功耗管理及 RTC 时钟以外的所有部件都会掉电或者进入其它最省电状态。 由于 platform 无法知晓 app 用到了哪些外设、如何配置这些外设， 所以，app 需要参与从深睡眠退出时的唤醒流程。 Platform 会询问 app 当前是否允许进入深睡眠，如果不允许，则进入其它相对不激进的省电模式。

为了使用深睡眠，需要定义两个回调函数，参见 [`platform_set_evt_callback`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_set_evt_callback)。 为了方便开发和调试，提供 [`platform_config`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_config) API 控制是否开启省电功能。

除了上面的自动省电机制，app 还可以主动将整个芯片系统关闭一段时间然后重启。关闭状态下芯片功耗降至最低， 在关闭状态下，可以维持一段内存里的数据不丢失，代价是需要增加一点功耗。参见 [`platform_shutdown`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_shutdown)。如果仅有很少量的数据需要保持：

如果只需要保存少量的几个比特，SDK 提供了一对 API 可供使用[`platform_write_persistent_reg`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_write_persistent_reg) 和 [`platform_read_persistent_reg`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_read_persistent_reg)。

## 5.5 CMSIS API {#cmsis-api}

SDK 尝试对一些 CMSIS API 做了封装以便开发。当直接使用 CMSIS API 时务必小心，因为可能会影响系统的运行。

以下操作严格禁止：

1. 修改中断向量表相关的寄存器
2. 修改中断的配置

## 5.6 调试与跟踪 {#debugging-tracing}

除了在线调试外，SDK 提供以下两种辅助调试的方法：

1. `printf`

   `printf` 是检查程序行为最方便的方法。`Wizard` 能够为 `printf` 生成支撑代码.
2. 跟踪（Trace）

   内部状态和 HCI 接口消息可通过 Trace 记录下来。`Wizard` 也能够为 Trace 生成支撑代码。Trace 包含几种预先定义的数据类型，可以编程选择记录哪些数据类型。使用 [Tracer](https://ingchips.github.io/user_guide_cn/core-tools.html#ingtracer) 查看 Trace 数据。

*Table 5.1: printf 和 Trace 的对比*
| 方法 | 优点 | 缺点 |
| --- | --- | --- |
| printf | 通用 | *慢* |
| Trace | 二进制数据，速度快 | 数据类型为预先定义 |

`printf` 和 trace 都可以配置成从 UART 口或者 SEGGER RTT[22](#fn22) 输出。 表 [5.2](https://ingchips.github.io/user_guide_cn/dive-into-sdk.html#tab:ch3-port-compare) 对比了两种传输方式。

*Table 5.2: UART 的 SEGGER RTT 的对比*
| 传输方式 | 优点 | 缺点 |
| --- | --- | --- |
| UART | 通用，使用简单 | 慢，占用更多的 CPU 时间 |
| SEGGER RTT | 速度快 | 需要 J-Link 等工具，难以抓取上电阶段的数据 |

### 5.6.1 有关 SEGGER RTT 的使用提示 {#有关-segger-rtt-的使用提示}

- 使用 `J-LINK RTT Viewer` 实时查看 `printf` 输出
- 使用 `J-LINK RTT Logger` 将 trace 记录到文件

  这个工具会询问有关 RTT 的设置：设备名称（Device name）为 “CORTEX-M3”； 目标接口（Target interface）为 “SWD”； RTT 控制块（RTT Control Block）的地址即名为 `_SEGGER_RTT` 的变量的地址，可从 `.map` 文件中找到； RTT 通道号为 `0`。 以下是一个示例：

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
    J-Link Lite ..........
    S/N: ......

  Searching for RTT Control Block...OK. 1 up-channels found.
  RTT Channel description:
    Index: 0
    Name:  Terminal
    Size:  500 bytes.

  Output file: .....log

  Getting RTT data from target. Press any key to quit.
  ```

  或者，这个工具可以从命令行启动，通过参数设定 `_SEGGER_RTT` 的地址范围，工具会自动搜索实际地址。例如：

  ```shell
  JLinkRTTLogger.exe -If SWD -Device CORTEX-M3 -Speed 4000
  -RTTSearchRanges "0x20005000 0x8000"
  -RTTChannel 0
  file_name
  ```

  对于 ING916xx，将上面的 CORTEX-M3 替换为 CORTEX-M4。

### 5.6.2 内存转储 {#内存转储}

我们致力于提供高质量的 platform 软件包。如果在 platform 二进制文件内发生断言（assertion）错误， 建议转储全部内存，记录各寄存器的值。请从开发者手册获得各内存区域的地址范围。 使用 [Axf Tool](https://ingchips.github.io/user_guide_cn/core-tools.html#ch2-axf-tool) 分析内存转储。如果问题无法解决，请联系技术支持。

- Keil μVision

  在调试状态下，打开命令窗口用 `save` 命令保存每个区域。以 ING918xx 为例：

  ```
  save sysm.hex  0x20000000,0x2000FFFF
  save share.hex 0x400A0000,0x400AFFFF
  ```
- J-Link Commander

  连接到设备后，使用 `regs` 查看所有寄存器的当前值，使用 `savebin` 将每个区域保存到文件。以 ING918xx 为例：

  ```
  savebin sysm.bin  0x20000000 0x10000
  savebin share.bin 0x400A0000 0x10000
  ```
- IAR Embedded Workbench

  在调试状态下，打开内存窗口，打开快捷菜单，用 “Memory Save …” 保存数据。
- Rowley Crossworks for ARM & SEGGER Embedded Studio for ARM

  在调试状态下，打开内存窗口，对于每个区域：

  1. 填写起始地址和大小；
  2. 打开快捷菜单，用 “Memory Save …” 保存数据。
- GDB (GNU Arm Embedded Toolchain)

  在 GDB 调试模式下，使用 `dump` 命令保存每个区域。

内存也可以使用一小段专门的代码导出。例如在 `PLATFORM_CB_EVT_ASSERTION` 事件的回调里，将整个内存数据通过 UART 导出。

---

1. <a id="fn20"></a>[https://en.wikipedia.org/wiki/Memory_pool](https://en.wikipedia.org/wiki/Memory_pool)[↩︎](https://ingchips.github.io/user_guide_cn/dive-into-sdk.html#fnref20)
2. <a id="fn21"></a>请参考《低功耗蓝牙开发者手册》“线程安全性”一节。[↩︎](https://ingchips.github.io/user_guide_cn/dive-into-sdk.html#fnref21)
3. <a id="fn22"></a>[https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/](https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/)[↩︎](https://ingchips.github.io/user_guide_cn/dive-into-sdk.html#fnref22)