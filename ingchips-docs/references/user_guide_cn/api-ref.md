<!-- user_guide_cn: 6 Platform API 参考 -->

# 6 Platform API 参考 {#api-ref}

本章节介绍 platform API。

## 6.1 配置与信息 {#配置与信息}

### 6.1.1 platform_config {#platform_config}

配置一些 platform 功能。

#### 6.1.1.1 原型 {#原型}

```c
void platform_config(const platform_cfg_item_t item,
                     const uint32_t flag);
```

#### 6.1.1.2 参数 {#参数}

- `const platform_cfg_item_t item`

  指定要配置的项目。可以是以下值之一：

  - `PLATFORM_CFG_LOG_HCI`：打印主机控制器接口消息。默认：禁用。

    仅在 ING918 上可用。HCI 日志仅用于对 BLE 行为进行快速检查。请考虑使用跟踪（参见 [调试与跟踪](https://ingchips.github.io/user_guide_cn/dive-into-sdk.html#debugging-tracing)）。
  - `PLATFORM_CFG_POWER_SAVING`：省电模式。默认：禁用。
  - `PLATFORM_CFG_TRACE_MASK`：选定的跟踪项的位图。默认：`0`。

    ```c
    typedef enum
    {
        PLATFORM_TRACE_ID_EVENT                 = 0,
        PLATFORM_TRACE_ID_HCI_CMD               = 1,
        PLATFORM_TRACE_ID_HCI_EVENT             = 2,
        PLATFORM_TRACE_ID_HCI_ACL               = 3,
        PLATFORM_TRACE_ID_LLCP                  = 4,
        //..
    } platform_trace_item_t;
    ```
  - `PLATFORM_CFG_RT_RC_EN`：启用/禁用实时 RC 时钟。默认：启用。
  - `PLATFORM_CFG_RT_OSC_EN`：启用/禁用实时晶体振荡器。默认：启用。
  - `PLATFORM_CFG_RT_CLK`：实时时钟选择。标志为`platform_rt_clk_src_t`。默认：`PLATFORM_RT_RC`

    ```c
    typedef enum
    {
        PLATFORM_RT_OSC,           // 外部实时晶体振荡器
        PLATFORM_RT_RC             // 内部实时 RC 时钟
    } platform_rt_clk_src_t;
    ```

    对于 ING918，修改此配置时，RT_RC 和 RT_OSC 都应**启用**并**运行**：

    ```
      * 对于 RT_OSC，等待直到 RT_OSC 的状态为 OK；
      * 对于 RT_RC，启用后等待 100μs。
    ```

    并在禁用未使用的时钟之前再等待 100μs。
  - `PLATFORM_CFG_RT_CLK_ACC`：配置实时时钟精度（ppm）。
  - `PLATFORM_CFG_RT_CALI_PERIOD`：实时时钟自动校准周期（秒）。默认：3600 * 2（2小时）。
  - `PLATFORM_CFG_DEEP_SLEEP_TIME_REDUCTION`：睡眠时间缩减（深度睡眠模式）（微秒）。ING918默认：~550μs。
  - `PLATFORM_CFG_SLEEP_TIME_REDUCTION`：睡眠时间缩减（其他睡眠模式）（微秒）。ING918默认：~450μs。
  - `PLATFORM_CFG_LL_DBG_FLAGS`：链路层标志。`ll_cfg_flag_t`中的位组合。详见 《低功耗蓝牙开发者手册》[23](#fn23)。
  - `PLATFORM_CFG_LL_LEGACY_ADV_INTERVAL`：链路层传统广告间隔，高占空比模式（高16位）和正常占空比模式（低16位）（微秒）。高占空比模式默认：1250；正常占空比模式默认：1500。
  - `PLATFORM_CFG_RTOS_ENH_TICK`：启用 RTOS 的增强型滴答。默认：禁用。启用后，当外设频繁生成中断请求时，可以保持滴答的准确性。
  - `PLATFORM_CFG_LL_DELAY_COMPENSATION`：链路层的延迟补偿。

    当系统以较低频率运行时，链路层需要更多时间（以 μs 为单位）来调度RF任务。例如，如果 ING916 以 24MHz 运行，则需要约 2500μs 的补偿。
  - `PLATFORM_CFG_24M_OSC_TUNE`：24M OSC 调谐。不适用于ING918。

    对于 ING916，调谐值可能在 0x16~0x2d 之间。
  - `PLATFORM_CFG_ALWAYS_CALL_WAKEUP`：无论深度睡眠过程是否完成或中止（失败），始终触发 `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP` 事件。ING918默认：禁用以保持向后兼容性。ING916默认：启用。
  - `PLATFORM_CFG_FAST_DEEP_SLEEP_TIME_REDUCTION`：快速深度睡眠模式的睡眠时间减少（微秒）。不适用于ING918。

    此配置必须小于或等于 `PLATFORM_CFG_DEEP_SLEEP_TIME_REDUCTION`。当等于 `PLATFORM_CFG_DEEP_SLEEP_TIME_REDUCTION` 时，不使用快速深度睡眠模式。

    ING916 默认：~2000μs。
  - `PLATFORM_CFG_AUTO_REDUCE_CLOCK_FREQ`：在这些情况下自动降低 CPU 时钟频率：

    - 默认的 IDLE 过程，
    - 进入睡眠模式时。

    不适用于 ING918。ING916 默认：启用。
- `const uint32_t flag`

  用于禁用或启用项目。可以是以下值之一：

  - `PLATFORM_CFG_ENABLE`
  - `PLATFORM_CFG_DISABLE`

#### 6.1.1.3 返回值 {#返回值}

无。

#### 6.1.1.4 备注 {#备注}

无。

#### 6.1.1.5 示例 {#示例}

```c
// 在 ING918 上启用HCI日志记录
platform_config(PLATFORM_CFG_LOG_HCI, PLATFORM_CFG_ENABLE);
```

### 6.1.2 platform_get_version {#platform_get_version}

获取 platform 的版本号。

#### 6.1.2.1 函数原型 {#函数原型}

```c
const platform_ver_t *platform_get_version(void);
```

#### 6.1.2.2 参数 {#参数-1}

无。

#### 6.1.2.3 返回值 {#返回值-1}

指向 `platform_ver_t` 的指针。

#### 6.1.2.4 备注 {#备注-1}

platform 版本号由三部分组成：主版本号、次版本号和修订号：

```c
typedef struct platform_ver
{
    unsigned short major;
    char  minor;
    char  patch;
} platform_ver_t;
```

#### 6.1.2.5 示例 {#示例-1}

```c
const platform_ver_t *ver = platform_get_version();
printf("platform version: %d.%d.%d\n", ver->major, ver->minor, ver->patch);
```

### 6.1.3 platform_read_info {#platform_read_info}

读取 platform 信息。

#### 6.1.3.1 函数原型 {#函数原型-1}

```c
uint32_t platform_read_info(const platform_info_item_t item);
```

#### 6.1.3.2 参数 {#参数-2}

- `const platform_info_item_t item`

  信息项。

  - `PLATFORM_INFO_RT_OSC_STATUS`: 读取实时晶体振荡器的状态。值为 0：不正常；非 0：正常。

  对于 ING916：此时钟在被选为实时时钟源**之后**才会开始运行。

  - `PLATFORM_INFO_RT_CLK_CALI_VALUE`: 读取当前实时时钟校准结果。
  - `PLATFOFM_INFO_IRQ_NUMBER`: 获取 platform IRQ 的底层 IRQ 编号。

    例如，获取 UART0 的底层 IRQ 编号：

    ```c
    platform_read_info(
        PLATFOFM_INFO_IRQ_NUMBER + PLATFORM_CB_IRQ_UART0)
    ```

#### 6.1.3.3 返回值 {#返回值-2}

信息项的值。

#### 6.1.3.4 备注 {#备注-2}

无。

#### 6.1.3.5 示例 {#示例-2}

```c
platform_read_info(PLATFORM_INFO_RT_OSC_STATUS);
```

### 6.1.4 platform_switch_app {#api-switch-app}

切换到次级应用程序。

#### 6.1.4.1 函数原型 {#函数原型-2}

```c
void platform_switch_app(const uint32_t app_addr);
```

#### 6.1.4.2 参数 {#参数-3}

- `const uint32_t app_addr`

  次级应用程序的入口地址。

#### 6.1.4.3 返回值 {#返回值-3}

无。

#### 6.1.4.4 备注 {#备注-3}

调用此函数后，其后的代码将不会被执行。

#### 6.1.4.5 示例 {#示例-3}

```c
platform_switch_app(0x80000);
```

## 6.2 事件与中断 {#事件与中断}

### 6.2.1 platform_set_evt_callback_table {#platform_set_evt_callback_table}

为所有 platform 事件注册一个回调函数表。

#### 6.2.1.1 函数原型 {#函数原型-3}

```c
void platform_set_evt_callback_table(
    const platform_evt_cb_table_t *table);
```

#### 6.2.1.2 参数 {#参数-4}

- `const platform_evt_cb_table_t *table`

  回调函数表的地址。

#### 6.2.1.3 返回值 {#返回值-4}

无。

#### 6.2.1.4 备注 {#备注-4}

此函数应仅在 `app_main` 中调用。如果使用了 `platform_set_evt_callback`，则不应使用此函数。

与 `platform_set_evt_callback` 相比，使用此函数可以节省 `sizeof(platform_evt_cb_table_t)` 字节的 RAM 空间。

#### 6.2.1.5 示例 {#示例-4}

```c
static const platform_evt_cb_table_t evt_cb_table =
{
    .callbacks = {
        [PLATFORM_CB_EVT_HARD_FAULT] = {
            .f = (f_platform_evt_cb)cb_hard_fault,
        },
        [PLATFORM_CB_EVT_PROFILE_INIT] = {
            .f = setup_profile,
        },
        // ...
    }
};

int app_main()
{
    // ...
    platform_set_evt_callback_table(&evt_cb_table);
    // ...
}
```

### 6.2.2 platform_set_irq_callback_table {#platform_set_irq_callback_table}

为所有 platform 中断请求注册一个回调函数表。

#### 6.2.2.1 函数原型 {#函数原型-4}

```c
void platform_set_irq_callback_table(
    const platform_irq_cb_table_t *table);
```

#### 6.2.2.2 参数 {#参数-5}

- `const platform_irq_cb_table_t *table`

  回调函数表的地址。

#### 6.2.2.3 返回值 {#返回值-5}

无。

#### 6.2.2.4 备注 {#备注-5}

此函数只能在 `app_main` 中调用。如果使用了 `platform_set_irq_callback`，则不应使用此函数。

与 `platform_set_irq_callback` 相比，使用此函数可以节省 `sizeof(platform_irq_cb_table_t)` 字节的 RAM。

#### 6.2.2.5 示例 {#示例-5}

```c
static const platform_irq_cb_table_t irq_cb_table =
{
    .callbacks = {
        [PLATFORM_CB_IRQ_UART0] = {
            .f = (f_platform_irq_cb)cb_irq_uart,
            .user_data = APB_UART0
        },
        // ...
    }
};

int app_main()
{
    // ...
    platform_set_irq_callback_table(&irq_cb_table);
    // ...
}
```

### 6.2.3 platform_set_evt_callback {#platform_set_evt_callback}

注册回调函数以处理 platform 事件。

#### 6.2.3.1 函数原型 {#函数原型-5}

```c
void platform_set_evt_callback(platform_evt_callback_type_t type,
                               f_platform_evt_cb f,
                               void *user_data);
```

#### 6.2.3.2 参数 {#参数-6}

- `platform_evt_callback_type_t type`

  指定要注册回调函数的事件类型。可以是以下值之一：

  - `PLATFORM_CB_EVT_PUTC`：输出 ASCII 字符事件

    当 platform 想要输出 ASCII 字符用于日志记录时，会触发此事件。传递给回调函数的参数 `void *data` 是从 `char *` 类型转换而来。

    如果在创建新项目时在 `Common Function` 中勾选了 `Print to UART`，`Wizard` 可以自动生成将 platform 日志重定向到 UART 的代码。
  - `PLATFORM_CB_EVT_PROFILE_INIT`：配置文件初始化事件

    当主机初始化时，会触发此事件以请求应用程序初始化GATT配置文件。

    在创建新项目时，`Wizard` 可以自动为此事件生成代码。
  - `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP`：从深度睡眠唤醒事件

    当从深度睡眠唤醒时，会触发此事件。在深度睡眠期间，外设接口（如UART、I2C等）都已关闭。因此，唤醒时可能需要重新初始化这些接口。

    如果在创建新项目时在 `Common Function` 中勾选了 `Deep Sleep`，`Wizard` 可以自动为此事件生成代码。

    传递给回调函数的参数 `void *data` 是从 `platform_wakeup_call_info_t *` 类型转换而来。

    此时 RTOS 尚未恢复，某些 RTOS API 不可用；某些 platform API（如`platform_get_us_time`）也可能不可用。
  - `PLATFORM_CB_EVT_ON_IDLE_TASK_RESUMED`：操作系统从节能模式完全恢复。

    如果唤醒原因是 `PLATFORM_WAKEUP_REASON_NORMAL`，则在 `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP` 之后调用此回调。 对于 NoOS 变体，回调由 `platform_os_idle_resumed_hook()`调用。 此事件与 `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP` 不同：

    - 所有操作系统功能都已恢复（对于NoOS变体，这取决于 `platform_os_idle_resumed_hook()` 的正确使用）
    - 所有 platform API都可用
    - 回调在空闲任务中调用。

    参数 `void *data` 始终为 `NULL`。
  - `PLATFORM_CB_EVT_QUERY_DEEP_SLEEP_ALLOWED`：查询是否允许深度睡眠事件

    当platform准备进入深度睡眠模式时，会触发此事件以查询应用程序当前是否允许深度睡眠。回调函数可以通过返回 `0` 拒绝深度睡眠，或通过返回非 `0` 值允许深度睡眠。

    如果在创建新项目时在 `Common Function` 中勾选了 `Deep Sleep`，`Wizard` 可以自动为此事件生成代码。
  - `PLATFORM_CB_EVT_HARD_FAULT`：硬件故障发生

    当硬件故障发生时，会触发此事件。传递给回调函数的参数 `void *data` 是从 `hard_fault_info_t *` 类型转换而来。 如果未定义此回调，当硬件故障发生时，CPU将进入死循环。
  - `PLATFORM_CB_EVT_ASSERTION`：软件断言失败

    当软件断言失败时，会触发此事件。传递给回调函数的参数 `void *data` 是从 `assertion_info_t *` 类型转换而来。 如果未定义此回调，当断言发生时，CPU将进入死循环。
  - `PLATFORM_CB_EVT_LLE_INIT`：链路层引擎初始化。

    当链路层引擎初始化时，会触发此事件。
  - `PLATFORM_CB_EVT_HEAP_OOM`：内存不足。

    当堆分配失败（堆内存不足）时，会触发此事件。 如果触发此事件且未定义回调，CPU将进入死循环。 参数 `void *data` 是从整数转换而来。这个整数代表内存不足的堆的编号：

    - `0`: FreeRTOS 的堆；
    - `1`: 链路层的堆；
    - `2`: 链路层任务池。
  - `PLATFORM_CB_EVT_TRACE`：跟踪输出。

    当发出跟踪项时，会触发此事件。应用程序可以为此事件定义回调函数以保存或记录跟踪输出。回调的 `param` 是从 `platform_trace_evt_t *` 类型转换而来（参见[调试与跟踪](https://ingchips.github.io/user_guide_cn/dive-into-sdk.html#debugging-tracing)）。

    ```c
    typedef struct
    {
        const void *data1;
        const void *data2;
        uint16_t len1;
        uint16_t len2;
    } platform_evt_trace_t;
    ```

    跟踪项是 `data1` 和 `data2` 的组合。注意：

    1. `len1` 或 `len2` 可能为0，但不能同时为0；
    2. 如果回调函数发现无法输出大小为 `len1` + `len2` 的数据，则应丢弃 `data1` 和 `data2` 以避免跟踪项损坏。
  - `PLATFORM_CB_EVT_EXCEPTION`：硬件异常。

    参数 `void *data` 是从 `platform_exception_id_t *` 类型转换而来。
  - `PLATFORM_CB_EVT_IDLE_PROC`：自定义IDLE过程。

    参见“Programmer’s Guide - Power Saving”[24](#fn24)。
  - `PLATFORM_CB_EVT_HCI_RECV`：接管 HCI 并完全隔离内置主机。

    当定义时：

    - HCI事件和ACL数据传递给此回调；
    - `PLATFORM_CB_EVT_PROFILE_INIT`被忽略。

    参数 `void *data` 是从 `const platform_hci_recv_t *` 类型转换而来。另请参见 [`platform_get_link_layer_interf`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_get_link_layer_interf)。
  - `PLATFORM_CB_EVT_BEFORE_DEEP_SLEEP`: Platform 即将进入深度睡眠

    当 platform 决定进入深度睡眠模式时，会触发此事件。应用程序可以借此机会配置外设。回调函数应保持简单并尽快返回。

    参数 `void *data` 是从 `platform_sleep_category_b_t` 转换而来，代表所要进入的深度睡眠的类型。
- `f_platform_evt_cb f`

  注册到事件`type`的回调函数。`f_platform_evt_cb`定义为：

  ```c
  typedef uint32_t (*f_platform_evt_cb)(void *data, void *user_data);
  ```

  若非专门说明，Platform 忽略这个回调函数的返回值。
- `void *user_data`

  此参数原封不动地传递给回调函数的`user_data`。

#### 6.2.3.3 返回值 {#返回值-6}

无。

#### 6.2.3.4 备注 {#备注-6}

不需要为每个事件注册回调函数。

如果未为 `PLATFORM_CB_EVT_PUTC` 事件注册回调函数，所有platform日志（包括`platform_printf`）将被丢弃。

如果未为 `PLATFORM_CB_EVT_PROFILE_INIT` 事件注册回调函数，BLE设备的配置文件将为空。

如果未为 `PLATFORM_CB_EVT_ON_DEEP_SLEEP_WAKEUP` 事件注册回调函数，应用程序在从深度睡眠唤醒时将不会收到通知。

如果未为 `PLATFORM_CB_EVT_QUERY_DEEP_SLEEP_ALLOWED` 事件注册回调函数，深度睡眠将被*禁用*。

#### 6.2.3.5 示例 {#示例-6}

```c
uint32_t cb_putc(char *c, void *dummy)
{
    // TODO: 将字符c输出到UART
    return 0;
}

......

platform_set_evt_callback(PLATFORM_CB_EVT_PUTC, (f_platform_evt_cb)cb_putc,
                          NULL);
```

### 6.2.4 platform_set_irq_callback {#platform_set_irq_callback}

注册中断请求的回调函数。

开发者无需在应用中定义IRQ处理程序，而是使用回调函数代替。

#### 6.2.4.1 函数原型 {#函数原型-6}

```c
void platform_set_irq_callback(platform_irq_callback_type_t type,
                               f_platform_irq_cb f,
                               void *user_data);
```

#### 6.2.4.2 参数 {#参数-7}

- `platform_irq_callback_type_t type`

  指定要注册回调函数的 IRQ 类型。不同芯片系列的值有所不同。以 ING918 为例：

  ```c
  PLATFORM_CB_IRQ_RTC,
  PLATFORM_CB_IRQ_TIMER0,
  PLATFORM_CB_IRQ_TIMER1,
  PLATFORM_CB_IRQ_TIMER2,
  PLATFORM_CB_IRQ_GPIO,
  PLATFORM_CB_IRQ_SPI0,
  PLATFORM_CB_IRQ_SPI1,
  PLATFORM_CB_IRQ_UART0,
  PLATFORM_CB_IRQ_UART1,
  PLATFORM_CB_IRQ_I2C0,
  PLATFORM_CB_IRQ_I2C1
  ```
- `f_platform_irq_cb f`

  注册到 IRQ `type`的回调函数。`f_platform_irq_cb` 定义为：

  ```c
  typedef uint32_t (*f_platform_irq_cb)(void *user_data);
  ```
- `void *user_data`

  该参数将原封不动地传递给回调函数的 `user_data`。

#### 6.2.4.3 返回值 {#返回值-7}

无。

#### 6.2.4.4 备注 {#备注-7}

当回调函数注册到 IRQ 时，IRQ 会自动启用。另请参见 [`platform_enable_irq`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_enable_irq)。

#### 6.2.4.5 示例 {#示例-7}

```c
uint32_t cb_irq_uart0(void *dummy)
{
    // TODO: 添加UART0 IRQ处理代码
    return 0;
}

......

platform_set_irq_callback(
    PLATFORM_CB_IRQ_UART0,
    cb_irq_uart0,
    NULL);
```

### 6.2.5 platform_enable_irq {#platform_enable_irq}

启用或禁用指定的 IRQ（中断请求）。

#### 6.2.5.1 函数原型 {#函数原型-7}

```c
void platform_enable_irq(
    platform_irq_callback_type_t type,
    uint8_t flag);
```

#### 6.2.5.2 参数 {#参数-8}

- `platform_irq_callback_type_t type`:

  需要配置的 IRQ。
- `uint8_t flag`:

  启用（1）或禁用（0）。

#### 6.2.5.3 返回值 {#返回值-8}

无。

#### 6.2.5.4 备注 {#备注-8}

这里的“启用”或“禁用”中断是从CPU的角度来看的。以 UART 为例，UART 本身需要配置为在接收、发送或超时时生成中断，这不在本函数的范围内。

#### 6.2.5.5 示例 {#示例-8}

启用来自 UART0 的中断请求：

```c
platform_enable_irq(
    PLATFORM_CB_IRQ_UART0,
    1);
```

## 6.3 时钟 {#时钟}

另请参阅“Programmer’s Guide - Power Saving”[25](#fn25)中的“The Real-time Clock”[26](#fn26)。

### 6.3.1 platform_calibrate_rt_clk {#platform_calibrate_rt_clk}

校准实时时钟并获取校准值。

#### 6.3.1.1 函数原型 {#函数原型-8}

```c
uint32_t platform_calibrate_rt_clk(void);
```

### 6.3.2 platform_rt_rc_auto_tune {#platform_rt_rc_auto_tune}

自动调整内部实时RC时钟，并获取调整值。

对于ING918，此函数将内部实时RC时钟调整至50kHz[27](#fn27)。 对于其他设备，它将内部实时RC时钟调整至32768Hz。

#### 6.3.2.1 函数原型 {#函数原型-9}

```c
uint16_t platform_rt_rc_auto_tune(void);
```

#### 6.3.2.2 参数 {#参数-9}

无。

#### 6.3.2.3 返回值 {#返回值-9}

16位的调整值。

#### 6.3.2.4 备注 {#备注-9}

如果应用程序启用了省电模式，并且使用实时RC时钟作为时钟源，则必须调用此函数。

此操作耗时约250ms。建议调用一次并存储返回值以供后续使用。

#### 6.3.2.5 示例 {#示例-9}

```c
// 最简单的示例：在`PLATFORM_CB_EVT_PROFILE_INIT`的回调函数中调用此函数，
// 不保存返回值。
uint32_t setup_profile(void *user_data)
{
    platform_rt_rc_auto_tune();
    ...
}
```

### 6.3.3 platform_rt_rc_auto_tune2 {#platform_rt_rc_auto_tune2}

自动调整内部实时RC时钟至特定频率，并获取调整值。

#### 6.3.3.1 函数原型 {#函数原型-10}

```c
uint16_t platform_rt_rc_auto_tune2(
    uint32_t target_frequency);
```

#### 6.3.3.2 参数 {#参数-10}

- `uint32_t target_frequency`

  目标频率，单位为赫兹（Hz）。

#### 6.3.3.3 返回值 {#返回值-10}

返回16位的调整值。

### 6.3.4 platform_rt_rc_tune {#platform_rt_rc_tune}

使用调谐值调整内部实时RC时钟。

#### 6.3.4.1 函数原型 {#函数原型-11}

```c
void platform_rt_rc_tune(uint16_t value);
```

#### 6.3.4.2 参数 {#参数-11}

- `uint16_t value`

  用于调谐时钟的值（由 [`platform_rt_rc_auto_tune`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_rt_rc_auto_tune) 或 [`platform_rt_rc_auto_tune2`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_rt_rc_auto_tune2) 返回）

#### 6.3.4.3 返回值 {#返回值-11}

无。

#### 6.3.4.4 备注 {#备注-10}

无。

#### 6.3.4.5 示例 {#示例-10}

```c
platform_rt_rc_tune(value);
```

## 6.4 RF {#rf}

### 6.4.1 platform_set_rf_clk_source {#platform_set_rf_clk_source}

选择射频时钟源。此函数供内部使用。

### 6.4.2 platform_set_rf_init_data {#platform_set_rf_init_data}

自定义射频初始化数据。此函数供内部使用。

### 6.4.3 platform_set_rf_power_mapping {#platform_set_rf_power_mapping}

功率等级在内部由一个索引表示。存在一个功率映射表，该表列出了每个索引对应的实际发射功率等级。以 ING918 为例，功率索引的范围是 [0..63]，功率映射表是一个包含 64 个条目的数组，每个条目给出了以 0.01 dBm 为单位的发射功率等级。

对于需要更好功率等级控制的应用，可以测量每个索引的实际功率等级。使用此函数更新映射表后，堆栈可以确定请求功率等级的适当索引。

#### 6.4.3.1 函数原型 {#函数原型-12}

```c
void platform_set_rf_power_mapping(
    const int16_t *rf_power_mapping);
```

#### 6.4.3.2 参数 {#参数-12}

- `const int16_t *rf_power_mapping`

  新的功率映射表。

#### 6.4.3.3 返回值 {#返回值-12}

无。

#### 6.4.3.4 备注 {#备注-11}

无。

#### 6.4.3.5 示例 {#示例-11}

```c
static const int16_t power_mapping[] =
{
    -6337,  // 索引 0: -63.37dBm
    // ...
    603     // 索引 63: 6.03dBm
};


platform_set_rf_power_mapping(
    power_mapping);
```

### 6.4.4 platform_patch_rf_init_data {#platform_patch_rf_init_data}

修补部分内部射频初始化数据。此函数供内部使用。

## 6.5 内存与实时操作系统（RTOS） {#内存与实时操作系统rtos}

### 6.5.1 platform_call_on_stack {#platform_call_on_stack}

在独立的专用堆栈上调用函数。当需要偶尔调用一个使用大量堆栈的函数时，可以使用此接口。

#### 6.5.1.1 函数原型 {#函数原型-13}

```c
void platform_call_on_stack(
    f_platform_function f,
    void *user_data,
    void *stack_start,
    uint32_t stack_size);
```

#### 6.5.1.2 参数 {#参数-13}

- `f_platform_function f`

  要调用的函数。
- `void *user_data`

  传递给 `f` 的用户数据。
- `void *stack_start`

  专用堆栈的起始（最低）地址。
- `uint32_t stack_size`

  专用堆栈的大小，以字节为单位。

#### 6.5.1.3 返回值 {#返回值-13}

无。

#### 6.5.1.4 备注 {#备注-12}

尽管提供了 `stack_size`，但此函数不会保护堆栈不被 `f` 覆盖。

### 6.5.2 platform_get_current_task {#platform_get_current_task}

获取调用此API的当前任务。

#### 6.5.2.1 函数原型 {#函数原型-14}

```c
platform_task_id_t platform_get_current_task(void);
```

#### 6.5.2.2 参数 {#参数-14}

无。

#### 6.5.2.3 返回值 {#返回值-14}

```c
typedef enum
{
    PLATFORM_TASK_CONTROLLER,  // 控制器任务
    PLATFORM_TASK_HOST,        // 主机任务
    PLATFORM_TASK_RTOS_TIMER,  // RTOS定时器任务
} platform_task_id_t;
```

#### 6.5.2.4 备注 {#备注-13}

此API仅在带有内置 RTOS 的软件包中可用。

### 6.5.3 platform_get_gen_os_driver {#platform_get_gen_os_driver}

获取通用操作系统驱动。对于“NoOS”变体，返回由应用程序提供的驱动；对于内置 RTOS 的软件包，返回一个模拟出来的驱动接口。

#### 6.5.3.1 函数原型 {#函数原型-15}

```c
const void *platform_get_gen_os_driver(void);
```

#### 6.5.3.2 参数 {#参数-15}

无。

#### 6.5.3.3 返回值 {#返回值-15}

返回值被强制转换为 `const gen_os_driver_t *`。开发者可以将返回值强制转换回 `const gen_os_driver_t *` 并使用其中的API。

#### 6.5.3.4 备注 {#备注-14}

`gen_os_driver_t` 是RTOS上的一个抽象层。使用其中的API而不是直接使用RTOS API可以使应用程序跨RTOS（独立于底层RTOS）。

在 SDK v8.5 及更新的版本里，由于内置 RTOS 可替换，在 `app_main` 调用这个函数就变得“奇怪”。为了向后兼容， `platform_get_gen_os_driver` 像旧版本一样返回模拟出来的驱动接口。如果开发者要替换内置的 RTOS， 那么就不应该在 `app_main` 里使用这个接口。

### 6.5.4 platform_get_heap_status {#platform_get_heap_status}

获取当前内置 RTOS 的堆的状态，例如可用大小等。

#### 6.5.4.1 函数原型 {#函数原型-16}

```c
void platform_get_heap_status(platform_heap_status_t *status);
```

#### 6.5.4.2 参数 {#参数-16}

- `platform_heap_status_t *status`

  堆状态。

#### 6.5.4.3 返回值 {#返回值-16}

无。

#### 6.5.4.4 备注 {#备注-15}

堆状态定义为：

```c
typedef struct
{
    uint32_t bytes_free;                // 总空闲字节数
    uint32_t bytes_minimum_ever_free;   // 自启动以来bytes_free的最小值
} platform_heap_status_t;
```

#### 6.5.4.5 示例 {#示例-12}

```c
platform_heap_status_t status;
platform_get_heap_status(&status);
```

### 6.5.5 platform_get_rtos_heap_mem {#platform_get_rtos_heap_mem}

获取内置 RTOS 用作堆的内存块。

#### 6.5.5.1 函数原型 {#函数原型-17}

```c
void *platform_get_rtos_heap_mem(int *size);
```

#### 6.5.5.2 参数 {#参数-17}

- `int *size`

  内存块的大小，以字节为单位。

#### 6.5.5.3 返回值 {#返回值-17}

内存块的地址。

#### 6.5.5.4 备注 {#备注-16}

当使用自定义 RTOS 替换内置 RTOS 时，这块内存完全不会被使用。 开发者可以通过此 API 获取其地址和大小，并利用它。

#### 6.5.5.5 示例 {#示例-13}

```c
// 将此内存块初始化为 RT-Thread 的堆
int size = 0;
char *heap = platform_get_rtos_heap_mem(&size);
rt_system_heap_init(heap, heap + size);
```

### 6.5.6 platform_get_task_handle {#platform_get_task_handle}

获取特定 platform 任务的 RTOS 句柄。

#### 6.5.6.1 函数原型 {#函数原型-18}

```c
uintptr_t platform_get_task_handle(
    platform_task_id_t id);
```

#### 6.5.6.2 参数 {#参数-18}

- `platform_task_id_t id`

  platform 任务 ID。

#### 6.5.6.3 返回值 {#返回值-18}

如果 platform 知道该任务的句柄，则返回任务句柄；否则返回0。例如，在“NoOS”变体中，platform 不知道`PLATFORM_TASK_RTOS_TIMER`的句柄，因此返回0。

### 6.5.7 platform_install_task_stack {#platform_install_task_stack}

为特定 platform 任务安装一个新的RTOS堆栈。

当默认堆栈大小不足以满足内部任务需求时，使用此函数来扩大堆栈。例如，用户开发的 RTOS 定时器回调可能需要更大的堆栈空间。

开发者可以查阅 RTOS 文档以了解如何检查堆栈使用情况。例如，在FreeRTOS中，`uxTaskGetStackHighWaterMark` 用于查询任务接近溢出分配给它的堆栈空间的程度。

#### 6.5.7.1 函数原型 {#函数原型-19}

```c
void platform_install_task_stack(
    platform_task_id_t id,
    void *start,
    uint32_t size);
```

#### 6.5.7.2 参数 {#参数-19}

- `platform_task_id_t id`

  任务标识符。
- `void *start`

  堆栈的起始（最低）地址。地址应针对底层 CPU 进行适当对齐。
- `uint32_t size`

  新堆栈的大小，以字节为单位。

#### 6.5.7.3 返回值 {#返回值-19}

无。

#### 6.5.7.4 备注 {#备注-17}

此函数应仅在 `app_main` 中调用。

对于NoOS变体，在实现通用操作系统接口时，可以替换 RTOS 堆栈（修改其大小等）。

### 6.5.8 platform_install_isr_stack {#platform_install_isr_stack}

为中断服务例程（ISR）安装一个新的堆栈。

#### 6.5.8.1 函数原型 {#函数原型-20}

```c
void platform_install_isr_stack(void *top);
```

#### 6.5.8.2 参数 {#参数-20}

- `void *top`

  新堆栈的顶部，必须针对底层CPU进行适当对齐。

#### 6.5.8.3 返回值 {#返回值-20}

无。

#### 6.5.8.4 备注 {#备注-18}

如果应用程序需要比 ISR 中默认堆栈更大的堆栈，可以安装一个新堆栈来替换默认堆栈。

此函数仅允许在 `app_main` 中调用。新堆栈将在 `app_main` 返回后投入使用。

#### 6.5.8.5 示例 {#示例-14}

```c
uint32_t new_stack[2048];
...
platform_install_isr_stack(new_stack + sizeof(new_stack) / sizeof(new_stack[0]));
```

## 6.6 时间与定时器 {#时间与定时器}

读取当前时间（定时器计数器）的API：

- `platform_get_timer_counter`
- `platform_get_us_time`

使用625微秒分辨率的定时器的API：

- `platform_set_abs_timer`
- `platform_set_timer`
- `platform_delete_timer`

使用1微秒分辨率的定时器的API：

- `platform_create_us_timer`
- `platform_cancel_us_timer`
- `platform_create_us_timer2`

这两种类型的定时器都可以在节能模式下使用，即当节能模式启用时，它们会按预期工作。表[6.1](#tab:ch-api-compare-timers)比较了这两种定时器。

表: (#tab:ch-api-compare-timers) 两种 platform 定时器的比较

| 类型 | 625微秒分辨率 | 1微秒分辨率 |
| --- | --- | --- |
| 回调 | 从类似任务的上下文中调用 | 从中断服务例程（ISR）或调用者中调用 |
| 标识符 | 回调函数指针 | 定时器句柄 |
| 容量 | 受限于堆空间 | 少量几个 |

SDK v8.5 重新设计微秒分辨率定时器。

- 在旧版本中，

  API 实际上是对一些 Controller 函数的封装，其中 `platform_create_us_timer` 其实表示在时间点 *T* 调度一个持续时间为1微秒的操作。因此，如果 Controller *将要* 在时间点 *T* 附近执行扫描或广告等操作，`platform_create_us_timer` 将 失败。在 `callback` 中调用 `platform_create_us_timer` 也是**禁止的**。
- 在v8.5及之后的版本中，

  这些 API 不再是 Controller 函数的封装，`platform_create_us_timer` 在上面这种情况下也会成功。Controller 也使用此接口来管理所有 RF 操作。 可以在 `callback` 中调用 `platform_create_us_timer`。

`platform_create_us_timer` 从专用内存池中分配数据，该内存池的大小是固定且有限的。 在 v8.5 及之后的版本中，最多可以创建 4 个定时器。注意：Controller 使用并且仅使用其中一个这样的定时器。 如果 Controller 创建定时器失败，将引发 `PLATFORM_CB_EVT_HEAP_OOM` 事件。

### 6.6.1 platform_cancel_us_timer {#platform_cancel_us_timer}

取消之前由 `platform_create_us_timer` 创建的 platform 定时器。

#### 6.6.1.1 函数原型 {#函数原型-21}

```c
int platform_cancel_us_timer(
    platform_us_timer_handle_t timer_handle);
```

#### 6.6.1.2 参数 {#参数-21}

- `platform_us_timer_handle_t timer_handle`

  定时器的句柄。

#### 6.6.1.3 返回值 {#返回值-21}

如果指定的定时器成功取消，该函数返回 0。否则，返回一个非 0 值，这也意味着定时器的回调函数正在执行中。

### 6.6.2 platform_create_us_timer {#platform_create_us_timer}

设置一个具有 1 微秒（μs）分辨率的单次触发 platform 定时器。

#### 6.6.2.1 函数原型 {#函数原型-22}

```c
platform_us_timer_handle_t platform_create_us_timer(
    uint64_t abs_time,
    f_platform_us_timer_callback callback,
    void *param);
```

#### 6.6.2.2 参数 {#参数-22}

- `uint64_t abs_time`

  当 `platform_get_us_timer() == abs_time` 时，回调函数将被调用。
- `f_platform_us_timer_callback callback`

  回调函数。其签名为：

  ```c
  typedef void (* f_platform_us_timer_callback)(
      platform_us_timer_handle_t timer_handle,
      uint64_t time_us,
      void *param);
  ```

  其中，`timer_handle` 是 `platform_create_us_timer` 的返回值， `time_us` 是调用回调时 `platform_get_us_timer` 的当前值， `param` 是创建此定时器时的用户参数。
- `void *param`

  用户参数。

#### 6.6.2.3 返回值 {#返回值-22}

该函数返回创建的定时器的句柄。如果定时器成功创建，则返回非 NULL 值。否则，返回 NULL。

#### 6.6.2.4 备注 {#备注-19}

尽管 `abs_time` 以微秒（μs）为单位，但**不保证**回调函数会以这样的分辨率被调用。

伪代码：

```c
create_us_timer(..)
{
    if (内存不足) return NULL;
    r = 分配句柄;
    if (剩余时间太短) {
        // callback 直接在调用者的上下文中被调用
        callback(param);
        释放内存;
        return r;   // 返回的是非 NULL
    }
    将 r 存储到队列;  // callback 将在后续的 ISR 上下文中调用
    return r;
}
```

### 6.6.3 platform_create_us_timer2 {#platform_create_us_timer2}

设置一个具有 1 微秒（μs）分辨率的单次触发 platform 定时器。

#### 6.6.3.1 函数原型 {#函数原型-23}

```c
int platform_create_us_timer2(
    uint64_t abs_time,
    f_platform_us_timer_callback callback,
    void *param,
    platform_us_timer_handle_t *timer_handle);
```

#### 6.6.3.2 参数 {#参数-23}

- `uint64_t abs_time`

  当 `platform_get_us_timer() == abs_time` 时，回调函数将被调用。
- `f_platform_us_timer_callback callback`

  回调函数。
- `void *param`

  用户参数。
- `platform_us_timer_handle_t *timer_handle`

  当创建成功时，`timer_handle` 被设置为定时器的句柄。如果定时器失败，`timer_handle` 被设置为 NULL。

#### 6.6.3.3 返回值 {#返回值-23}

如果创建成功，返回 `0`，否则返回 `-1`。

#### 6.6.3.4 备注 {#备注-20}

一种常见的用法是在回调函数清除句柄。当使用 `platform_create_us_timer`，这种做法可能存在问题。例如：

```c
platform_us_timer_handle_t handle;
void callback(...)
{
    handle = NULL;
}

// 回调函数可能在返回前就调用了，这时，
// handle 未能清除
handle = platform_create_us_timer(T,
    callback);
```

使用 `platform_create_us_timer2` 可以避免这种问题：

```c
// 在调用 `callback` 之前，
// `handle` 已由 `platform_create_us_timer2`
// 填入了正确的句柄
platform_create_us_timer2(T,
    callback,
    &handle);
```

### 6.6.4 platform_delete_timer {#platform_delete_timer}

删除先前由 `platform_set_timer` 或 `platform_set_abs_timer` 创建的platform定时器。

#### 6.6.4.1 函数原型 {#函数原型-24}

```c
void platform_delete_timer(f_platform_timer_callback callback)
```

#### 6.6.4.2 参数 {#参数-24}

- `f_platform_timer_callback callback`

  回调函数，同时也是定时器的标识符。

#### 6.6.4.3 返回值 {#返回值-24}

无。

#### 6.6.4.4 备注 {#备注-21}

调用此函数时，回调可能已经排队等待在任务中调用。因此，在调用此函数后，回调仍可能被调用。

### 6.6.5 platform_get_timer_counter {#platform_get_timer_counter}

读取platform定时器的计数器，分辨率为625微秒。

#### 6.6.5.1 函数原型 {#函数原型-25}

```c
uint32_t platform_get_timer_counter(void);
```

#### 6.6.5.2 参数 {#参数-25}

无。

#### 6.6.5.3 返回值 {#返回值-25}

一个完整的32位值，表示当前计数器的值，大致等于 `platform_get_us_time() / 625`。 ### `platform_get_us_time`

读取自BLE初始化以来的内部时间计数。

#### 6.6.5.4 函数原型 {#函数原型-26}

```c
int64_t platform_get_us_time(void);
```

#### 6.6.5.5 参数 {#参数-26}

无。

#### 6.6.5.6 返回值 {#返回值-26}

内部时间计数器的值，以1微秒为单位计数。该计数器大约每21.8年溢出一次。

#### 6.6.5.7 备注 {#备注-22}

该计数器在关机后重新启动。

#### 6.6.5.8 示例 {#示例-15}

```c
uint64_t now = platform_get_us_time();
```

### 6.6.6 platform_set_abs_timer {#platform_set_abs_timer}

设置一个单次触发的 platform 定时器，在绝对时间触发，分辨率为 625 微秒。

#### 6.6.6.1 函数原型 {#函数原型-27}

```c
void platform_set_abs_timer(
    f_platform_timer_callback callback,
    uint32_t abs_time);
```

#### 6.6.6.2 参数 {#参数-27}

- `f_platform_timer_callback callback`

  定时器到期时的回调函数，该函数在类似 RTOS 任务的上下文中调用，而不是在中断服务例程（ISR）中调用。
- `uint32_t abs_time`

  当 `platform_get_timer_counter() == abs_time` 时，`callback` 被调用。 如果 `abs_time` 刚刚超过 `platform_get_timer_counter()`，`callback` 会立即被调用， 例如，`abs_time` 为 `platform_get_timer_counter() - 1`。

#### 6.6.6.3 返回值 {#返回值-27}

无。

#### 6.6.6.4 备注 {#备注-23}

此函数总是成功，除非内存不足。

#### 6.6.6.5 示例 {#示例-16}

使用此函数模拟一个周期性定时器。

```c

#define PERIOD  100
static uint32_t last_timer = 0;

void platform_timer_callback(void)
{
    last_timer += PERIOD;
    platform_set_abs_timer(platform_timer_callback, last_timer);

    // 执行周期性任务
    // ...
}

last_timer = platform_get_timer_counter() + PERIOD;
platform_set_abs_timer(platform_timer_callback, last_timer);
```

### 6.6.7 platform_set_timer {#platform_set_timer}

设置一个单次触发的 platform 定时器，从“现在”开始延迟，分辨率为 625 微秒。

#### 6.6.7.1 函数原型 {#函数原型-28}

```c
void platform_set_timer(
    f_platform_timer_callback callback,
    uint32_t delay);
```

#### 6.6.7.2 参数 {#参数-28}

- `f_platform_timer_callback callback`

  定时器到期时的回调函数，该函数在类似 RTOS 任务的上下文中调用，而非中断服务例程（ISR）。
- `uint32_t delay`

  定时器到期前的延迟时间（单位：625 微秒）。

  有效范围：0~0x7fffffff。当 `delay` 为 0 时，定时器被清除。

#### 6.6.7.3 返回值 {#返回值-28}

无。

#### 6.6.7.4 备注 {#备注-24}

此函数总是成功，除非内存耗尽。

`platform_set_timer(f, 100)` 等同于：

```c
platform_set_abs_timer(f,
    platform_get_timer_counter() + 100);
```

`platform_set_timer(f, 0)` 等同于：

```c
platform_delete_timer(f);
```

但不等同于：

```c
platform_set_abs_timer(f,
    platform_get_timer_counter() + 0);
```

由于 `callback` 也是定时器的标识符，以下两行代码仅定义了一个在 200 个单位后到期的定时器，而非两个独立的定时器：

```c
platform_set_timer(f, 100);
platform_set_timer(f, 200); // 更新定时器，而非创建新的
```

如果 `f` 再次用于`platform_set_abs_timer`，则定时器再次被更新：

```c
platform_set_abs_timer(f, ...);
```

## 6.7 节能 {#节能}

本节提供了在 RTOS 中实现节能的 API。 参见 “Programmer’s Guide - Power Saving”[28](#fn28)。

### 6.7.1 platform_pre_suppress_cycles_and_sleep_processing {#platform_pre_suppress_cycles_and_sleep_processing}

准备抑制一些低功耗实时时钟周期以实现无滴答节能。

#### 6.7.1.1 函数原型 {#函数原型-29}

```c
uint32_t platform_pre_suppress_cycles_and_sleep_processing(
    uint32_t expected_cycles);
```

#### 6.7.1.2 参数 {#参数-29}

- `uint32_t expected_cycles`

  预期可以被抑制的周期数（在节能模式下可以安全跳过的周期）。

  支持完整的 `uint32_t` 范围。

#### 6.7.1.3 返回值 {#返回值-29}

调整后的可以被抑制的周期数。

### 6.7.2 platform_pre_sleep_processing {#platform_pre_sleep_processing}

无滴答睡眠的预处理。

#### 6.7.2.1 函数原型 {#函数原型-30}

```c
void platform_pre_sleep_processing(void);
```

#### 6.7.2.2 参数 {#参数-30}

无。

#### 6.7.2.3 返回值 {#返回值-30}

无。

### 6.7.3 platform_post_sleep_processing {#platform_post_sleep_processing}

无滴答睡眠的后处理。

#### 6.7.3.1 函数原型 {#函数原型-31}

```c
void platform_post_sleep_processing(void);
```

#### 6.7.3.2 参数 {#参数-31}

无。

#### 6.7.3.3 返回值 {#返回值-31}

无。

#### 6.7.3.4 备注 {#备注-25}

如果调用了 `platform_pre_sleep_processing`，则必须跟随调用 `platform_post_sleep_processing`。

### 6.7.4 platform_os_idle_resumed_hook {#platform_os_idle_resumed_hook}

空闲任务恢复时的钩子。在空闲任务恢复时调用此函数。

#### 6.7.4.1 函数原型 {#函数原型-32}

```c
void platform_os_idle_resumed_hook(void);
```

#### 6.7.4.2 参数 {#参数-32}

无。

#### 6.7.4.3 返回值 {#返回值-32}

无。

### 6.7.5 platform_os_idle_resumed_hook {#platform_os_idle_resumed_hook-1}

Hook for Idle task got resumed. Call this when Idle task is resumed.

#### 6.7.5.1 函数原型 {#函数原型-33}

```c
void platform_os_idle_resumed_hook(void);
```

#### 6.7.5.2 参数 {#参数-33}

无。

#### 6.7.5.3 返回值 {#返回值-33}

无。

### 6.7.6 platform_pre_suppress_ticks_and_sleep_processing {#platform_pre_suppress_ticks_and_sleep_processing}

预抑制滴答和睡眠处理。此 API 已过时。请使用 `platform_pre_suppress_cycles_and_sleep_processing` 代替。

## 6.8 实用工具 {#实用工具}

### 6.8.1 platform_hrng {#platform_hrng}

使用硬件随机数生成器生成随机字节。

#### 6.8.1.1 函数原型 {#函数原型-34}

```c
void  platform_hrng(uint8_t *bytes, const uint32_t len);
```

#### 6.8.1.2 参数 {#参数-34}

- `uint8_t *bytes`

  随机数据输出。
- `const uint32_t len`

  要生成的随机字节数。

#### 6.8.1.3 返回值 {#返回值-34}

无。

#### 6.8.1.4 备注 {#备注-26}

生成固定长度数据所需的时间是不确定的。

#### 6.8.1.5 示例 {#示例-17}

```c
uint32_t strong_random;
platform_hrng(&strong_random, sizeof(strong_random));
```

### 6.8.2 platform_rand {#platform_rand}

通过内部伪随机数生成器（PRNG）生成一个伪随机整数。

#### 6.8.2.1 函数原型 {#函数原型-35}

```c
int platform_rand(void);
```

#### 6.8.2.2 参数 {#参数-35}

无。

#### 6.8.2.3 返回值 {#返回值-35}

返回一个范围在 0 到 RAND_MAX 之间的伪随机整数。

#### 6.8.2.4 备注 {#备注-27}

内部 PRNG 的种子在启动时由硬件随机数生成器（HRNG）初始化。此函数可用作标准库中 `rand()` 函数的替代。

#### 6.8.2.5 示例 {#示例-18}

```c
printf("rand: %d\n", platform_rand());
```

### 6.8.3 platform_read_persistent_reg {#platform_read_persistent_reg}

从持久寄存器中读取值。另请参阅 [`platform_write_persistent_reg`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_write_persistent_reg)。

#### 6.8.3.1 函数原型 {#函数原型-36}

```c
uint32_t platform_read_persistent_reg(void);
```

#### 6.8.3.2 参数 {#参数-36}

无。

#### 6.8.3.3 返回值 {#返回值-36}

由 [`platform_write_persistent_reg`](https://ingchips.github.io/user_guide_cn/api-ref.html#platform_write_persistent_reg) 写入的值。

#### 6.8.3.4 备注 {#备注-28}

无。

#### 6.8.3.5 示例 {#示例-19}

```c
platform_read_persistent_reg();
```

### 6.8.4 platform_reset {#platform_reset}

重置 platform（SoC）。

#### 6.8.4.1 函数原型 {#函数原型-37}

```c
void platform_reset(void);
```

#### 6.8.4.2 参数 {#参数-37}

无。

#### 6.8.4.3 返回值 {#返回值-37}

无。

#### 6.8.4.4 备注 {#备注-29}

调用此函数后，其后的代码将不会被执行。

#### 6.8.4.5 示例 {#示例-20}

```c
  if (内存不足)
    platform_reset();
```

### 6.8.5 platform_shutdown {#platform_shutdown}

将整个系统置于关机状态，并在指定时间后重新启动。可选地，在关机期间可以保留一部分内存，重启后应用程序可以继续使用这部分内存。

请注意，除非关机过程无法启动，否则此函数不会返回。可能导致失败的原因包括：

1. 外部唤醒信号被发出；
2. 输入参数不正确；
3. 内部组件繁忙。

#### 6.8.5.1 函数原型 {#函数原型-38}

```c
void platform_shutdown(const uint32_t duration_cycles,
                       const void *p_retention_data,
                       const uint32_t data_size);
```

#### 6.8.5.2 参数 {#参数-38}

- `const uint32_t duration_cycles`

  重新上电（重启）前的等待时间（以实时时钟周期为单位）。最短持续时间为 825 个周期（约25.18毫秒）。如果使用 `0`，系统将保持在关机状态，直到外部唤醒信号被发出。
- `const void *p_retention_data`

  指向要保留数据的起始位置的指针。只有 SYSTEM 内存中的数据可以被保留。当 `data_size` 为 `0` 时，此参数可以设置为 `NULL`。
- `data_size`

  要保留的数据的大小。当不需要保留内存时，设置为 `0`。

#### 6.8.5.3 返回值 {#返回值-38}

无。

#### 6.8.5.4 备注 {#备注-30}

无。

#### 6.8.5.5 示例 {#示例-21}

```c
// 关闭系统并在 1 秒后重启
platform_shutdown(32768, NULL, 0);
```

### 6.8.6 platform_write_persistent_reg {#platform_write_persistent_reg}

向持久寄存器写入一个值。该值在省电模式、关机模式或切换到另一个应用程序时仍会保留。

只有少量位被保存，如表 [6.2](#tab:ch-api-reg-bits) 所示。

表: (#tab:ch-api-reg-bits) 持久寄存器位大小

| 芯片系列 | 寄存器大小 (位) |
| --- | --- |
| ING918 | 4 |
| ING916 | 5 |

#### 6.8.6.1 函数原型 {#函数原型-39}

```c
void platform_write_persistent_reg(const uint8_t value);
```

#### 6.8.6.2 参数 {#参数-39}

- `const uint8_t value`

  要写入的值。

#### 6.8.6.3 返回值 {#返回值-39}

无。

#### 6.8.6.4 备注 {#备注-31}

无。

#### 6.8.6.5 示例 {#示例-22}

```c
platform_write_persistent_reg(1);
```

## 6.9 调试与追踪 {#调试与追踪}

### 6.9.1 platform_printf {#platform_printf}

存储在 platform 二进制文件中的 `printf` 函数。

#### 6.9.1.1 原型 {#原型-1}

```c
void  platform_printf(const char *format, ...);
```

#### 6.9.1.2 参数 {#参数-40}

- `const char *format`

  格式化字符串。
- `...`

  格式化字符串的可变参数。

#### 6.9.1.3 返回值 {#返回值-40}

无。

#### 6.9.1.4 备注 {#备注-32}

使用此函数有利有弊。

优点：

- 此函数位于 platform 二进制文件中，可以节省应用程序二进制文件的大小。

缺点：

- 输出被定向到 `PLATFORM_CB_EVT_PUTC` 事件，因此必须定义其回调函数。

#### 6.9.1.5 示例 {#示例-23}

```c
platform_printf("Hello world");
```

### 6.9.2 platform_raise_assertion {#platform_raise_assertion}

触发软件断言。

#### 6.9.2.1 函数原型 {#函数原型-40}

```c
void  platform_raise_assertion(const char *file_name, int line_no);
```

#### 6.9.2.2 参数 {#参数-41}

- `const char *file_name`

  断言发生的文件名。
- `int line_no`

  断言发生的行号。

#### 6.9.2.3 返回值 {#返回值-41}

无。

#### 6.9.2.4 备注 {#备注-33}

无。

#### 6.9.2.5 示例 {#示例-24}

```c
  if (NULL == ptr)
    platform_raise_assertion(__FILE__, __LINE__);
```

### 6.9.3 platform_trace_raw {#platform_trace_raw}

将一块原始数据输出到 TRACE。ID为 `PLATFORM_TRACE_ID_RAW`。

#### 6.9.3.1 函数原型 {#函数原型-41}

```c
void platform_trace_raw(
    const void *buffer,
    const int byte_len);
```

#### 6.9.3.2 参数 {#参数-42}

- `const void *buffer`

  缓冲区的指针。
- `const int byte_len`

  数据缓冲区的长度，以字节为单位。

## 6.10 其他 {#其他}

### 6.10.1 platform_get_link_layer_interf {#platform_get_link_layer_interf}

获取链路层驱动 API。

#### 6.10.1.1 函数原型 {#函数原型-42}

```c
const platform_hci_link_layer_interf_t *
    platform_get_link_layer_interf(void);
```

#### 6.10.1.2 参数 {#参数-43}

无。

#### 6.10.1.3 返回值 {#返回值-42}

返回驱动接口 `platform_hci_link_layer_interf_t *`。

#### 6.10.1.4 备注 {#备注-34}

此API暴露了控制器HCI接口。该驱动接口仅在定义了 `PLATFORM_CB_EVT_HCI_RECV` 时可用，此时内置的主机功能将被禁用。

### 6.10.2 sysSetPublicDeviceAddr {#syssetpublicdeviceaddr}

设置设备的公共地址。

BLE设备的公共地址是一个48位的扩展唯一标识符（EUI-48），按照IEEE 802-2014标准创建[29](#fn29)。

*INGCHIPS* 91x **没有**公共地址。此函数应**仅**用于调试或测试，**切勿**在最终产品中使用。

#### 6.10.2.1 函数原型 {#函数原型-43}

```c
void sysSetPublicDeviceAddr(const unsigned char *addr);
```

#### 6.10.2.2 参数 {#参数-44}

- `const unsigned char *addr`

  新的公共地址。

#### 6.10.2.3 返回值 {#返回值-43}

无。

#### 6.10.2.4 备注 {#备注-35}

为了避免潜在问题，应在调用任何 GAP 函数之前调用此函数。 建议在 `app_main` 或 `PLATFORM_CB_EVT_PROFILE_INIT` 事件回调函数中调用此函数。

#### 6.10.2.5 示例 {#示例-25}

```c
const unsigned char pub_addr[] = {1,2,3,4,5,6};
sysSetPublicDeviceAddr(pub_addr);
```

---

1. <a id="fn23"></a>[https://ingchips.github.io/application-notes/pg_ble_stack_cn/index.html](https://ingchips.github.io/application-notes/pg_ble_stack_cn/index.html)[↩︎](https://ingchips.github.io/user_guide_cn/api-ref.html#fnref23)
2. <a id="fn24"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/](https://ingchips.github.io/application-notes/pg_power_saving_en/)[↩︎](https://ingchips.github.io/user_guide_cn/api-ref.html#fnref24)
3. <a id="fn25"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/](https://ingchips.github.io/application-notes/pg_power_saving_en/)[↩︎](https://ingchips.github.io/user_guide_cn/api-ref.html#fnref25)
4. <a id="fn26"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/ch-api.html#the-real-time-clock](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-api.html#the-real-time-clock)[↩︎](https://ingchips.github.io/user_guide_cn/api-ref.html#fnref26)
5. <a id="fn27"></a>从v8.4.6版本开始。对于更早的版本，使用的是32768Hz。[↩︎](https://ingchips.github.io/user_guide_cn/api-ref.html#fnref27)
6. <a id="fn28"></a>[https://ingchips.github.io/application-notes/pg_power_saving_en/](https://ingchips.github.io/application-notes/pg_power_saving_en/)[↩︎](https://ingchips.github.io/user_guide_cn/api-ref.html#fnref28)
7. <a id="fn29"></a>[http://standards.ieee.org/findstds/standard/802-2014.html](http://standards.ieee.org/findstds/standard/802-2014.html)[↩︎](https://ingchips.github.io/user_guide_cn/api-ref.html#fnref29)