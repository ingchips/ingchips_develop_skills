# SDK 9.0 更新说明

## Highlights: {#highlights}

- 支持 ING20xx 系列（软件包、外设驱动、工具、示例）
- 支持 EATT (目前为“预览”：仅限 *exp*, *noos_exp* 软件包, API 可能修改)

**注意：**对 ING20xx 系列的支持目前为“预览”。注意事项：

- ROM 内的协议栈版本与 v8.4.22 相同。
- 省电功能仍在优化中。
- 对于使用 ROM 的项目，axf_tool 暂不支持基于 dump 的各项分析。

## v9.0.6 {#v906}

### 1. 软件包 {#1-软件包}

- [**修正**] ING20: 周期广播无法同步
- [**修正**] Host: EATT 相关问题（*exp*, *noos_exp*）

  - 解决 EATT 建立与断开事件未上报的问题；
  - 更新 CID 的管理。

### 2. 库函数 {#2-库函数}

- [**修正**] 使用 GCC 编译时的警告
- [**更新**] ING20 SYSCTRL: 增加 `SYSCTRL_SelectSpiClkDiv`, `SYSCTRL_SelectI2sClkDiv`

  与 ING916 兼容的接口（`SYSCTRL_SelectSpiClk`、`SYSCTRL_SelectI2sClk`）仍然保留。
- [**更新**] ING20 ADC：兼容 Keil 4
- [**更新**] `board.c`：适配 `ING2086_DK` 开发板

### 3. 示例 {#3-示例}

- [**更新**] 更好地适配各芯片系列。

### 4. 工具 {#4-工具}

- [**更新**] Wizard: 提升对 IAR, CrossStudio, Embedded Studio 的兼容性

  旧版本中，菜单 “Rebuild” 对于 CrossStudio、Embedded Studio 相当于 “Build”，新版本修正为 “Rebuild”。
- [**更新**] Tracer：引入新的图表库 [GPUChart](https://github.com/ChartGPU/ChartGPU)

  GPUChart 性能好，适合大数据量场景，但这个库目前存在一些问题，所以默认仍使用 ECharts，并可通过 Options -> Chart library 切换。
- [**修正**] ING20 Flash 算法：烧录 ING208xx 后程序可能无法运行
- [**修正**] 安装包未更新 Keil 4 芯片数据库 （.cdb）

## v9.0.5 {#v905}

**说明:**新增面向 ING20 系列量产版本的 ING208xx 系列。后续版本将删除 ING20xx 系列。

### 1. 软件包 {#1-软件包-1}

- [**更新**] 推迟上报 `gap_create_connection_cancel` 对应的 `COMMAND_COMPLETE` 事件

  新版本 Controller 完成资源释放再上报 `COMMAND_COMPLETE` 事件。旧版本在收到命令后会连接上报 `COMMAND_COMPLETE` 事件
- [**修正**] ING20: `ll_aes_encrypt` 计算结果错误
- [**修正**] ING20: 从低功耗唤醒后 AES 功能异常
- [**修正**] Host: EATT 相关问题（*exp*, *noos_exp*）
- [**新增**] 关于软件包参数的宏定义

  - `PLATFORM_BUNDLE_VARIANT`：当前软件包类型
  - `SYS_MEMORY_SIZE_KiB`：SYS memory 的大小（单位 KiB）
  - `SHARE_MEMORY_SIZE_KiB`：SHARE memory 的大小（单位 KiB）

### 2. 库函数 {#2-库函数-1}

- [**更新**] Mesh 库：支持 ING20
- [**更新**] ING916/ING20 Eflash: 从 Security 数据区拷贝校准数据时做数据检验，保证数据传输完整性
- [**更新**] ING20 SYSCTRL: `SYSCTRL_Init()` 检查某些参数是否合理，避免芯片工作异常
- [**更新**] ING20 RTIMER: 相关命名，避免误解

  因为两个 RTIMER 的功能与 TIMER0、TIMER1 不同，所以新版本更新了相关命名，避免误解。

  | 原名称 | 新名称 |
  | --- | --- |
  | APB_TMR2 | APB_RTIMER0 |
  | APB_TMR2 | APB_RTIMER1 |
  | PLATFORM_CB_IRQ_TIMER2 | PLATFORM_CB_IRQ_RTIMER0 |
  | PLATFORM_CB_IRQ_TIMER3 | PLATFORM_CB_IRQ_RTIMER1 |
- [**修正**] ING20 PWM/QDEC 的分频计算

### 3. 示例 {#3-示例-1}

- [**更新**] Platform Companion：使用固定的 Patch 函数表地址、App 启动地址
- [**新增**] Enhanced ATT：演示 EATT 的使用

### 4. 工具 {#4-工具-1}

- [**更新**] Cube：增加外设代码片断功能

  ![cube_code_snippets](https://ingchips.github.io/blog/img/cube_code_snippets.png)

  **温馨提示:**目前仅包含 ING20 外设的代码片断。其它芯片系列将在后续版本中得到支持。
- [**更新**] Wizard：增加 BLE 代码片断功能

  ![wiz_code_snippets](https://ingchips.github.io/blog/img/wiz_code_snippets.png)
- [**更新**] AI Shortcuts：MCP 服务器添加了 Wizard 的各种常用功能

  Wizard 启动后，会尝试开启 HTTP 服务器。当 LLM 调用 Wizard MCP 功能时，AI Shortcuts 将请求转发到 Wizard HTTP 服务器执行。Wizard 启动 HTTP 服务器后在右下角显示“Server online”信息。

  Wizard 的某些功能（如下载）依赖 Python，建议参照 [说明](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/tools) 准备 Python 环境，保证 Trace、下载等脚本能够正确运行。
- [**更新**] AI Shortcuts：云端大模型不再单独列出 DeepSeek，统一使用 “Online (OpenAI Compatible)”

## v9.0.4 {#v904}

### 1. 软件包 {#1-软件包-2}

- [**修正**] 低功耗时 `platform_create_us_timer` / `platform_create_us_timer2` 不正常

  启用低功耗，且无蓝牙任务时，`platform_create_us_timer` / `platform_create_us_timer2` 功能不正常。 现已修正。
- [**更新**] 单次睡眠支持更长的睡眠时间

  旧版本单次睡眠最长时间为 0xFFFFFFFF $\mu s$，约合 1.2 小时。现在单次睡眠最长时间约为 0xFFFFFFFF 个实时时钟周期。 设实时时钟频率为 32768 Hz，折合约 36.4 小时。
- [**更新**] `slave_latency` 的处理

  当 `slave_latency` > 0 时：在旧版本里，每 `slave_latency` 个连接事件接收一次；新版本里改为每 `slave_latency + 1` 个连接事件接收一次。

  蓝牙规范 5.2 版本或更低版本中，存在每 `slave_latency` 个连接事件接收一次和每 `slave_latency + 1` 个连接事件接收一次两种说法。 从 5.3 版本开始，明确为每 `slave_latency + 1` 个连接事件接收一次。新版本行为与此一致。
- [**修正**] Host: `..request_can_send_now` 可能递归调用导致栈溢出

  问题分析：

  `..request_can_send_now()` 的伪代码如下：

  ```highlight
    ..request_can_send_now() {
        if (can_send_now()) {
            emit_event();
            return;
        }
        ....
    }
  ```

  `can_send_now()` 通过比较启动时 Controller 上报的包数目（N1）和当前 Controller 中待发送包数目判断是否可以继续填充数据。 当 Controller 的内存以其它占用时（如通过 `ll_malloc` 分配内存），Controller 实际所能缓存的数据将低于 N1，此时 `can_send_now()` 会误判为 `true`， 导致发送 `.._CAN_SEND_NOW` 事件。app 的事件回调中一旦再次调用 `..request_can_send_now()`，就会多层嵌套，栈溢出。

  新版本里的 `..request_can_send_now()` 可以主动防止出现递归。

  对于不方便升级 SDK 的大数据吞吐量的项目，建议：

  - 防止嵌套调用 `..request_can_send_now()`；或者
  - 既不调用 `..request_can_send_now()`，也不响应 `.._CAN_SEND_NOW` 事件，而是响应 `HCI_EVENT_NUMBER_OF_COMPLETED_PACKETS` 事件，在这个事件里尝试发送数据。
- [**更新**] ING20 ROM: 模拟 2 个广播集

  存在以下限制：

  - 仅支持 Legacy 广播；
  - 广播间隔与配置的参数有所不同：设第 1 个广播的广播间隔为 T1，第 2 个广播的广播间隔为 T2，记 K = max(T2 / T1, 1)，实际的发送时序为以 T1 为间隔每发送 K 次广播 1，发送 1 次广播 2。
- [**修正**] ING20：低功耗稳定性
- [**更新**] ING20 默认参数

  修改前后的默认时钟参数：

  ![](https://ingchips.github.io/blog/img/sdk_v904_clock_change.png)

  新版本中，内部 Flash 不再使能连续读取。

### 2. 库函数 {#2-库函数-2}

- [**更新**] ING20 Eflash：自动兼容连续读取、非连续读取；自动清空 Cache
- [**修正**] ING20 PWM：IR mode 2 发送异常
- [**修正**] ING20 SYCTRL: TIMER 时钟读取接口
- [**修正**] ING20 SADC：ADC-DMA 异常

  为 DMA 设置 SADC 默认比特宽度。
- [**修正**] ING20 I2S：FIFO 深度
- [**修正**] ING20 PINCTRL：`PINCTRL_SetPadMux` 输入 `IO_NOT_A_PIN` 时逻辑错误
- [**更新**] ING20 QDEC：补充中断配置等接口
- [**修正**] ING20 SPI: 当载荷长度大于 512 字节时传输出错
- [**修正**] ING20 SYCTRL: `SYSCTRL_GetFlashClk`
- [**修正**] ING20 QDEC：偶而出现的寄存器写入错误
- [**更新**] ING20 GPIO：去除 GPIO 边沿唤醒功能

  请使用电平唤醒。
- [**修正**] ING20 WDT：启用低功耗时 `TMR_WatchDogDisable` 功能异常

### 3. 示例 {#3-示例-2}

- [**更新**] *HID Keyboard*: `kv_impl.c` 适配 ING20

### 4. 工具 {#4-工具-2}

- [**修正**] Wizard：不使用 Cube 时可能生成错误代码
- [**更新**] Wizard：新建项目时，可选择中断服务函数的注册方式
- [**更新**] `ingchips_pack_addon.py`

## v9.0.3 {#v903}

### 1. 软件包 {#1-软件包-3}

- [**修正**] `LL_FLAG_LEGACY_ONLY_SCANNING` 无效

  此问题由 v8.5.4 优化 Controller 调度时引入。
- [**修正**] ING20：`platform_shutdown` 功能异常

### 2. 库函数 {#2-库函数-3}

- [**新增**] USB CDC ACM 模块

  使用此模块可以方便地为应用加入虚拟串口功能。
- [**更新**] ING20 时钟相关: 增加 FastPre 时钟控制接口 `SYSCTRL_SetFastPreDiv`, `SYSCTRL_GetFastPreCLK`
- [**修正**] ING20 时钟相关: `SYSCTRL_GetFlashClk`
- [**修正**] ING20 ASDM：`ASDM_ClrOverflowError`
- [**修正**] ING20 ADC：`ADC_HardwareCalibration`, `ADC_GetDataChannel`

### 3. 示例 {#3-示例-3}

- [**更新**] *Voice Remote Control*: ING20 演示 ASDM + DMA 实现模拟 MIC 声音采集

### 4. 工具 {#4-工具-3}

- [**修正**] GUI Downloader：使用 ING-DAPLink 时可能无法启动应用
- [**更新**] Cube 支持配置 QDEC Step 时钟
- [**更新**] Wizard：新建项目时可选择使用 USB CDC ACM 输出 `printf` 信息
- [**更新**] Wizard：新建项目时调试器默认 CMSIS-DAP

## v9.0.2 {#v902}

### 1. 软件包 {#1-软件包-4}

- [**修正**] ING20：多连接时内存不足

  ING20 *mass_conn* 软件包支持最多 5 连接，*mini* 支持 1 个连接；其它软件包支持最多 3 连接（旧版本支持 2 连接）。
- [**修正**] ING20：*noos* 软件包无法使用
- [**修正**] ING20 ROM：开启低功耗后，`platform_set_timer` 唤醒时间错误
- [**修正**] Platform 启动时 Trace 输出芯片系列总是为 ING918
- [**更新**] Controller：改善 Master 角色对低吞吐率设备的兼容性
- [**更新**] `att_server_init`

  旧版本 `att_server_init` 用于初始化 ATT Server，并设置回调。新版本仅用来设置回调，ATT Server 初始化由 platform 完成。 旧版 `att_server_init`必须在 `PLATFORM_CB_EVT_PROFILE_INIT` 事件中调用，并且只能调用一次。

  新版 SDK：

  - 如果应用不涉及 ATT 特征的写入、或者动态数据的读取，那么可以不调用 `att_sever_init`。
  - 允许多次调用 `att_sever_init`，更新回调函数。

### 2. 库函数 {#2-库函数-4}

- [**修正**] ING20 时钟相关：`TMR_GetClk`, `SYSCTRL_SelectPWMClk`, `SYSCTRL_SelectSpiClk`
- [**更新**] ING20 ASDM：支持两种 `ASDM_Mode`
- [**更新**] ING20 ADC：增加 `ADC_GetData`, `ADC_SetVref`, `ADC_HardwareCalibration`
- [**修正**] USB BSP：`bsp_usb_disable()` 导致的枚举问题
- [**更新**] `rf_enable_powerboost`：适配 ING20

### 3. 示例 {#3-示例-4}

- [**更新**] *Voice Remote Control*: 演示 ING20 ASDM 的使用（包括 AMIC 和 PDM 两种解码方式）
- [**更新**] 示例适配 ING20，修复相关问题，如

  - *Peripheral Beacon*：出现软件断言，无法运行；
  - *Thermometer with FOTA*: 升级时出现 HardFault；
  - *HID Mouse*：`DB_FLASH_ADDRESS` 地址非法。

### 4. 工具 {#4-工具-4}

- [**更新**] Wizard：集成基于 pyOCD 的 RTT log 工具

  目前 Windows 版本的 DAP-Link RTT log 工具传输效率不及基于 [pyOCD](https://pyocd.io/) 的 [RTT log 工具](https://github.com/ingchips/ING918XX_SDK_SOURCE/blob/master/tools/rtt_logger.py)， 所以用这个工具替换了原右键菜单中的 ING-DAP-Link 工具，既支持 J-Link，也支持 DAP-Link。用法：

  1. 安装 Python，参考 [文档](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/tools#rtt-logger) 安装其它依赖项；
  2. 将 Python 主程序（`python.exe`）的完整路径填写到 Wizard 选项中。

  当未配置 `python.exe` 选项时，回退使用 Windows 版本的 DAP-Link RTT log 工具。

## v9.0.1 {#v901}

### 1. 软件包 {#1-软件包-5}

- [**新增**] EATT
- [**修正**] ING20 ROM：广播时可能出现断言

  如果遇到 `assertion@ble50_llm.c:...`，可在 `app_main` 里调用 `platform_rom_hotfix_using_fpb`。 此补丁基于 FPB 的实现，可能与在线调试功能相互影响。
- [**修正**] ING20：开启低功耗后，`platform_set_timer` 无法正确唤醒

### 2. 库函数 {#2-库函数-5}

- [**更新**] ING20：补充和完善了 PTE/GPIOTE/SYSCTRL/KeyScan 等外设的驱动

### 3. 工具 {#3-工具}

- [**修正**] Downloader：显示的 ING916 Flash 大小错误

  此问题由 v9.0.0 引入。

### 4. 文档 {#4-文档}

- [**新增**] 《[ING20XX 系列芯片外设开发者手册](https://ingchips.github.io/application-notes/pg_ing20_cn/index.html)》

## v9.0.0 {#v900}

### 1. 软件包 {#1-软件包-6}

- [**新增**] 支持 ING20
- [**修正**] `ll_set_conn_acl_report_latency` 导致连接不稳定

### 2. 库函数 {#2-库函数-6}

- [**新增**] 支持 ING20

### 3. 示例 {#3-示例-5}

- [**更新**] CherryUSB: 演示 USB Host 功能

### 4. 工具 {#4-工具-5}

- [**新增**] 支持 ING20
- [**更新**] Trace 相关

  Platform 启动时会通过 Trace 输出芯片系列、版本等基础信息。

  ![](https://ingchips.github.io/blog/img/trace_platform_info.png)

  SDK 内置的 Trace 记录工具会自动记录开始时的 PC 时间。调用 `platform_rt_clk_auto_tune` 时， Trace 会输出调谐后的时钟频率。基于这两项数据，Tracer 可以比较准确地显示 PC 时间，方便对照分析。

  利用工具函数 `platform_trace_raw_printf` 可通过 Trace 输出字符串：

  ![](https://ingchips.github.io/blog/img/trace_printf.png)

  新增菜单 “Charts -> RSSI of Advertisers …”，用来生成广播的 RSSI 曲线图，支持通过最小 RSSI、地址等过滤数据。

  ![](https://ingchips.github.io/blog/img/trace_adv_rssi.png)
- [**更新**] AI Shortcuts：MCP 服务器

  AI Shortcuts 的 [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) 服务器提供了几个有关 SDK 的工具。 Options 窗口的 AI Shortcuts 页面显示了 MCP 服务器 的 URL。下图显示了 [Qwen Code](https://github.com/QwenLM/qwen-code) 使用该服务器的情形。

  ![](https://ingchips.github.io/blog/img/ai_shortcuts_mcp.png)

  **温馨提示:**MCP 服务器功能正在持续迭代、优化，请及时更新 AI Shortcuts。

## 使用 ING20 的 ROM {#使用-ing20-的-rom}

ING20 ROM 内置软件包，创建新项目时选择 *rom* 即可。此时烧录的 `platform.bin` 由 *Platform Companion* 项目生成， 负责芯片初始化、启动 ROM 内的 `platform.bin`，并修正其中可能存在的问题。系统的启动流程如图。

![](https://ingchips.github.io/blog/img/ing20_rom_startup.png)

ROM 内 platform 可能错误配置了某些寄存器。为此，*Platform Companion* 提供了热修复补丁， 需要在 `app_main` 加以调用：

```highlight
uintptr_t app_main()
{
#ifdef PLATFORM_IN_ROM
    platform_rom_hotfix();
    // v9.0.1 及以上版本包含了基于 FPB 的补丁，可能与在线调试功能相互影响
    platform_rom_hotfix_using_fpb();
#endif
   ...
}
```

从协议栈功能看，ROM 内置软件包相当于带有扩展功能的 *mini* 包。

另外，ING20 也支持在 Flash 里下载 *typical*/*mini* 等不同类型的软件包，用法与 ING918、ING916 相同。
