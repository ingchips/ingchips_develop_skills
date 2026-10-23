# SDK 8.2：支持 ING916XX 量产版

## Highlights: {#highlights}

- 开始支持 ING916XX 量产版（不再支持测试版芯片）
- 新增《[ING918XX 系列芯片外设开发者手册](https://ingchips.github.io/application-notes/pg_ing918_cn/index.html)》
- 新增《[ING916XX 系列芯片外设开发者手册](https://ingchips.github.io/application-notes/pg_ing916_cn/index.html)》
- 线程安全的 BLE API
- RPC 系统
- 新版 SIG Mesh 库
- [Cube 工具](https://ingchips.github.io/blog/2022-12-16-cube)（持续开发中）

**兼容性：** 对于不含有 CTE 的 Raw Package，本版本与旧版本**互不兼容**；对于包含 CTE 的情况，本版本与旧版本保持兼容。

**已知问题（局限性）:**

- 调试 ING916xx 时，复位方式不能选择 SYSRESETREQ，应该选择 VECTRESET（不同的调试器可能使用不同的名词，J-Link 里称为 Core）。

  - 复位整个 SoC 的临时措施：对于 JLink，将 [自定义脚本](https://ingchips.github.io/files/JlinkSettings.JLinkScript)放到工程目录，并在进入调试模式后再次点击 IDE 里的 “复位” 按钮。
- ING916XX 省电模式仍在持续开发、改进中，QUERY_DEEP_SLEEP_ALLOWED 回调目前只可返回 0 或者 PLATFORM_ALLOW_DEEP_SLEEP。
- ING916XX 使用内部 RC 为主时钟时，如果要使用省电模式，则 RC 频率暂时只能配置为 24MHz。

## 1. 软件包 {#1-软件包}

- [**新增**] API：platform_install_task_stack 等 (**8.2.0**)

  通过 `platform_install_task_stack` 可以为协议栈内部的 Task 重新设置栈。例如，当 Host 的回调函数复杂、需要更多的栈空间时，可为 Host Task 配置更大的栈空间。

  `btstack_push_user_runnable` 与 `btstack_push_user_msg` 类似，也是用于解决 Host API 的多线程访问问题。两者的区别：后者是将一条消息发送到 Host 消息队列，再由开发者特供的回调处理这条消息； 而前者是直接将函数指针及参数发送到 Host 处理队列，再由 Host Task 调用这个函数。

  以从其它线程使能广播为例。使用 `btstack_push_user_msg` 时：

  ```highlight
    #define USER_MSG_START_ADV ....
    static void user_msg_handler(uint32_t msg_id, void *data, uint16_t size)
    {
        switch (msg_id)
        {
        case USER_MSG_START_ADV:
            gap_set_ext_adv_enable(1, sizeof(adv_sets_en) / sizeof(adv_sets_en[0]), adv_sets_en);
            break;
        //...
        }
    }

    void another_thread(void)
    {
        //...
        btstack_push_user_msg(USER_MSG_START_ADV, NULL, 0);
        //...
    }
  ```

  使用 `btstack_push_user_runnable` 代码或更简洁：

  ```highlight
    static void enable_adv(void *data, uint16_t value)
    {
        gap_set_ext_adv_enable(1, sizeof(adv_sets_en) / sizeof(adv_sets_en[0]), adv_sets_en);
    }

    void another_thread(void)
    {
        //...
        btstack_push_user_runnable(enable_adv, NULL, 0);
        //...
    }
  ```

  借助 `platform_get_gen_os_driver` 可以获得通用 RTOS 接口。对于 NoOS 软件包，这个 API 返回的正是 App 提供给 platform 的通用 RTOS 接口。 使用这个 RTOS 接口的代码，不需要修改就可兼容不同的 RTOS。

  借助 `platform_get_current_task` 可以判断当前所处的线程/任务。

  多线程安全的 BLE API 使用了 `btstack_push_user_runnable`、`platform_get_gen_os_driver` 及 `platform_get_current_task`。
- [**修正**] Raw Packet 接收回调慢的问题 (**8.2.0**)

  旧版本接收不含有 CTE 的 Raw Package 时，从接收完毕到调用回调函数之间存在较大的延时。本版本已修正。 但是对于不含有 CTE 的 Raw Package，本版本与旧版本**互不兼容**。
- [**更新**] `gap_update_connection_parameters` (**8.2.0**)

  现在，主从角色都可以使用 `gap_update_connection_parameters`：对于主角色， 这个函数更新连接参数；对于从角色，这个函数请求主端更新连接参数。
- [**新增**] 配置项：PLATFORM_CFG_24M_OSC_TUNE (**8.2.1**)

  对于内置 24M 晶体振荡器调谐功能的芯片（ING916xx），此配置可配置调谐参数，微调频偏。
- [**新增**] 信息项：PLATFOFM_INFO_IRQ_NUMBER + X (**8.2.1**)

  通过这个信息项可以获取低层的中断编号。例如，获取 `PLATFORM_CB_IRQ_UART0` 对应的低层中断编号：

  ```highlight
    platform_read_info(信息项：PLATFOFM_INFO_IRQ_NUMBER + );
  ```
- [**修正**] 改进 ING916xx 深睡眠模式的稳定性 (**8.2.1**)
- [**更新**] `_ON_DEEP_SLEEP_WAKEUP` 回调增加了 Reason 参数 (**8.2.2**)

  传入回调函数的 `void *data` 参数是从 `platform_wakeup_call_reason_t` 类型转换而来。正常从睡眠中醒来时， 传入的 reason 为 `PLATFORM_WAKEUP_REASON_NORMAL`；如果睡眠过程中止（即芯片实际未进入睡眠）， 那么传入的 reason 为 `PLATFORM_WAKEUP_REASON_ABORTED`。

  旧版本的行为：只有正常从睡眠中醒来（对应 `PLATFORM_WAKEUP_REASON_ABORTED`）时才调用这个回调。

  新版本考虑到与旧版本的兼容性，定义了一个配置项 `PLATFORM_CFG_ALWAYS_CALL_WAKEUP`：当配置为 0 时， 维持旧版本行为；当配置为 1 时，才会以 `PLATFORM_WAKEUP_REASON_ABORTED` 为 reason 调用事件回调。

  对于 ING918xx 的软件包，配置项 `PLATFORM_CFG_ALWAYS_CALL_WAKEUP` 默认为 0，已有的回调函数不需要修改。 对于 ING916xx 的软件包，配置项 `PLATFORM_CFG_ALWAYS_CALL_WAKEUP` 默认为 1，回调函数的流程建议为：

  ```highlight
    uint32_t on_deep_sleep_wakeup(void *data, void *user_data)
    {
        platform_wakeup_call_reason_t reason = (platform_wakeup_call_reason_t)(uintptr_t)(data);
        if (PLATFORM_WAKEUP_REASON_ABORTED == reason)
        {
            // 睡眠中止时，不需要重新配置外设。
            // 如果使用了 GPIO 的低功耗保持功能，可以借此机会解除
            // GIO_EnableRetentionGroupA(0)
            return 0;
        }

        setup_peripherals();
        return 0;
    }
  ```
- [**修正**] ING916xx 软件包未开启 AES (**8.2.2**)
- [**修正**] ING916xx BLE 通信性能问题 (**8.2.3**)
- [**修正**] ING916xx 接收扩展广播时上报的地址错误 (**8.2.3**)
- [**修正**] ING916xx `platform_reset` 可能导致死循环 (**8.2.3**)
- [**修正**] Raw package bare more 与 BLE 的共存 (**8.2.3**)
- [**更新**] L2CAP 模块：开发基于信用点的连接 API (**8.2.3**)
- [**更新**] FreeRTOS FromISR 调用违例时提供明确的提示信息 (**8.2.3**)

  使用 FreeRTOS 是一个常见的错误是在中断服务程序内调用了“普通”版本的 API，而非专门用于中断服务程序的 “…FromISR”。现在，当出现这个问题时，软件包的 ASSERTION 回调将给出明确的提示信息：

  ```highlight
    [ASSERTION] @ USE FromISR:0
  ```

  行末的“:0”没有具体含义。
- [**修正**] SM 存在 2 个或更多可解析地址时的地址解析问题 (**8.2.4**)

  旧版本当已配对设备中包含 2 个或以上使用了可解析地址时的设备时，SM 无法正确解析地址。
- [**更新**] ING916xx 射频性能优化 (**8.2.4**)

  发射功率与标称值更接近，RSSI 测量值更准确（误差 $\pm 1.5dB$）。
- [**修正**] ING916xx `platform_shutdown` 不支持 duration 为 0 的情况 (**8.2.5**)
- [**更新**] ING916xx 优化 DEEP sleep 时的功耗 (**8.2.5**)

## 2. 外设驱动 {#2-外设驱动}

- [**更新**] ING916xx 量产版外设驱动 (**8.2.0**)
- [**更新**] ING916xx 增加 USB 驱动 (**8.2.2**)
- [**更新**] ING916xx 增加 KeyScan/Comparator 驱动 (**8.2.3**)

  ING916xx 所有外设（或“虚拟”外设）驱动都已更新：

  | 名称 | 名称 |
  | --- | --- |
  | ADC | I2S |
  | Comparator | IR |
  | DMA | PDM |
  | eFuse | PinCtrl |
  | KeyScan | RTC |
  | GPIO | SysCtrl |
  | I2C | Timer |
  | USB | QDEC |

## 3. 库函数 {#3-库函数}

- [**新增**] `board.c`：包含所有开发板板载器件的驱动、辅助函数 (**8.2.0**)

  `board.c` 为不同的开发板提供了一套统一、简洁的接口。相关示例也相应更新。
- [**新增**] `btstack_mt.c`：重新封装了一系列线程安全的 BLE API (**8.2.0**)

  这个模块借助 `btstack_push_user_runnable` 等新 API 实现。 *UART GATT Console* 已使用这些 API 重写。
- [**新增**] `btstack_sync.c`：封装了一系列同步的 BLE API (**8.2.0**)

  `btstack_sync.c` 封装了为 GATT 客户端、GAP 等模块同步的 BLE API。 原 `gatt_client_util.c` 模块包含的同步 API 也已转移到 `btstack_sync.c`。 *UART GATT Console* 演示了部分同步 API 的用法。
- [**新增**] ING916xx: USB HID 模块 (**8.2.2**)
- [**修正**] ING916xx: *eflash.c* 模块里的 ``write_flash()` (**8.2.2**)
- [**更新**] *board.c*: 现已支持 DB682AC1A 开发板 (**8.2.2**)
- [**更新**] ING918xx: *power_ctrl.lib* 改善稳定性 (**8.2.2**)
- [**更新**] 新版 SIG Mesh 库 （持续改进中）(**8.2.3**)

  切换为新版 SIG Mesh 库，模型定义与原来（基于 NimBLE Mesh）方式类似，占用资源少，性能更好。具体使用方法可参阅 *Mesh Light* 示例。

## 4. 示例 {#4-示例}

- [**更新**] *IO Over BLE*: 增加 ING916xx USB 透传功能 (**8.2.2**)

  详情参阅示例的说明文档。`ing_usb` 测试工具可在 SDK/tools 目录下找到。
- [**更新**] 若干示例以适配 ING916xx (**8.2.2**)
- [**更新**] *Voice Remote Control*: 增加 ING916xx ADC 输入功能（持续改进中） (**8.2.2**)
- [**更新**] *Peripheral Console*: 增加 ING916xx RC 时钟演示 (**8.2.3**)
- [**更新**] *L2CAP PSM*: 演示基于信用点的连接 (**8.2.3**)
- [**更新**] *HID Mouse*: 使用 QDEC 实现鼠标滚轮 (**8.2.4**)

## 5. 文档 {#5-文档}

- [**新增**] 《ING918XX 系列芯片外设开发者手册》 (**8.2.0**)

## 6. 工具 {#6-工具}

- [**修正**] RF Test Tool Rx 命令发送错误 (**8.2.0**)
- [**更新**] Wizard 在线更新功能 (**8.2.0**)
- [**更新**] BQB RF Tool：增加 ING916xx 频偏调谐功能 (**8.2.1**)

  配合[简易频偏测试工具](https://ingchips.github.io/blog/2021-06-02-sdk-6/#简易频偏测量)，可以进行简单的频偏微调。 详见 BQB RF Test App 文档。
- [**新增**] Cube 工具：用于生成外设初始化代码 (**8.2.1**)
- [**更新**] Cube 工具：开始为 ING916xx 生成代码（持续改进中） (**8.2.2**)
- [**新增**] USB 测试工具 *ing_usb.exe* (**8.2.2**)

  详见 [ING916xx 外设开发者手册](https://ingchips.github.io/application-notes/pg_ing916_cn/)。
- [**更新**] Cube 工具：增加外设帮助菜单 (**8.2.4**)

## 7. RPC 系统 {#7-rpc-系统}

RPC 系统包含运行于芯片的 [BLE RPC 服务器](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples/ble_rpc) 和运行于 PC 的 [RPC 客户端](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/example_host/rpc_client)。 这个客户端具有以下特点：

- 可以使用绝大部分 BLE API：这个程序看起来就像是运行于 BLE SoC;
- 可以使用上位机操作系统提供的所有 API：这是本地程序。

开发者可以使用这种 RPC 客户端方式来：

- 开发原型；
- 开展自动化测试；
- ……
