<!-- pg_ble_stack_cn: 12 Controller -->

# 12 Controller {#ch-controller}

Controller 除了通过 HCI 为 Host 提供服务以外，还提供了一系列接口供开发者直接调用。 这些接口有的弥补 HCI 的不足，有的提供标准以外的扩展功能。这些接口与芯片、软件包紧密耦合， 不同芯片系列、软件包，所提供的 Controller 接口也不相同，比如 `typical` 软件包不提供不符合规范的“非标”接口。

## 12.1 配置项 {#配置项}

### 12.1.1 功能开关 {#功能开关}

链路层包含若干功能开关，通过 `platform_config(PLATFORM_CFG_LL_DBG_FLAGS, ...)` 设置。

各功能开关及设置后所产生的效果如下：

- `LL_FLAG_DISABLE_CTE_PREPROCESSING`：关闭 CTE 预处理。

  用于调试。非必要不应设置。
- `LL_FLAG_LEGACY_ONLY_INITIATING`：仅通过传统广播信道建立连接。

  当待连接的设备仅支持或仅使用传统广播时，建议开启，可明显提高连接建立速度。
- `LL_FLAG_LEGACY_ONLY_SCANNING`：仅扫描传统广播。

  当待扫描的设备仅支持或仅使用传统广播时，建议开启，可明显提高扫描效率。
- `LL_FLAG_REDUCE_INSTANT_ERRORS`：尝试减少“0x28 - 时机已过”错误码的上报。

  多连接场景当遇到较多“0x28 - 时机已过”错误时，可尝试设置。
- `LL_FLAG_DISABLE_RSSI_FILTER`：关闭内部的 RSSI 滤波器

  当需要读取原始 RSSI 时设置。
- `LL_FLAG_RSSI_AFTER_CRC`：仅从 CRC 正常的数据包获取 RSSI

  当需要更稳定的 RSSI 时设置。

通过 `platform_config` 时，应把所有需要打开的开关组合起来，一并设置。如：

- 对方设备仅仅支持或仅使用传统广播，组合使用 `LL_FLAG_LEGACY_ONLY_INITIATING` 和 `LL_FLAG_LEGACY_ONLY_SCANNING`：

  ```c
  platform_config(PLATFORM_CFG_LL_DBG_FLAGS,
        LL_FLAG_LEGACY_ONLY_INITIATING
      | LL_FLAG_LEGACY_ONLY_SCANNING);
  ```
- 要获得尽可能稳定的 RSSI，那么：

  ```c
  platform_config(PLATFORM_CFG_LL_DBG_FLAGS,
        LL_FLAG_RSSI_AFTER_CRC);
  ```
- 要获得尽可能多的原始 RSSI，那么：

  ```c
  platform_config(PLATFORM_CFG_LL_DBG_FLAGS,
        LL_FLAG_DISABLE_RSSI_FILTER);
  ```

### 12.1.2 可配参数 {#可配参数}

链路层还包含若干带有参数值的可配置项，通过 `ll_config` 配置：

```c
void ll_config(ll_config_item_t item, // 项目
    uint32_t value);                  // 值
```

`ll_config_item_t` 包含以下项目：

- `LL_CFG_SLAVE_LATENCY_PRE_WAKE_UP`：使用从机延迟时，用于预唤醒的时间提前量。

  Controller 在处理连接时，包含两部分工作：主要的处理以 RTOS 任务形式进行， 另外少量的工作（配置和触发硬件）在中断中进行。使用从机延迟时，假设按照从机延迟处理流程， 需要在 T 时刻的中断里配置和触发硬件，但是在这之前，RTOS 任务有可能一直未能触发，所以需要在 T 时刻之前主动唤醒 RTOS 任务，完成必要的处理，为 T 时刻的中断做好准备。

  参数值的范围为 1 ~ 255，单位为 0.625ms。默认值为 4。
- `LL_CFG_FEATURE_SET_MASK`：特性集合掩码。

  有时需要“模仿”其它 BLE 设备的链路层协议流程，而支持的特性对链路层协议流程影响很大。 为此可通过该配置项调整上报给对端设备的链路层特性。例如，模仿只支持加密和 2M PHY 两种特性的设备：

  ```c
  const uint8_t feature_mask[8] =
  {
      0x01,       // 比特 0: LE Encryption
      0x01,       // 比特 8: LE 2M PHY
  };

  // 参数值为指向掩码数组的指针
  ll_config(LL_CFG_FEATURE_SET_MASK,
            (uintptr_t)feature_mask);
  ```

  注意，这里只是修改了 Feature Exchange 流程的上报值，对链路层的实际功能没有影响。 需要保证设置的掩码数组一直存在，不可释放。

通过 `ll_set_max_conn_number` 设置可能用到的最大连接数：

```c
int ll_set_max_conn_number(
    int max_number);
```

比如软件包本身支持的最大连接数为 N，但是应用中实际最多用到 2 个连接，通过 `ll_set_max_conn_number(2)` 可优化多连接时的数据吞吐率。`ll_set_max_conn_number(M)`，M > N，并不能增加软件包本身支持的最大连接数。

当一个连接事件中接收到多个 ACL 数据包时，Controller 默认以 4 个[57](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn57)为一组上报，而不是每收到一个即上报，以减少任务间的切换开销。 通过 `ll_set_conn_acl_report_latency` 可以修改上报频率：

```c
void ll_set_conn_acl_report_latency(
    uint16_t conn_handle, // 连接句柄
    int latency);         // 以 latency 个包一组上报
```

当 `latency` 为 0 时，表示总是等到连接事件结束时集中上报；`latency` 为 1 时，每收到一个 ACL 数据包就立即上报。 这个参数保存在连接对象内，当连接断开后，配置消失。

## 12.2 HCI 增强 {#hci-增强}

### 12.2.1 读取特性和能力 {#读取特性和能力}

通过 `ll_get_capabilities` 可能直接获取 Controller 支持的特性及各种能力。

```c
void ll_get_capabilities(
    ll_capabilities_t *capabilities);
```

`ll_capabilities_t` 的定义如下。

```c
typedef struct ll_capabilities
{
    // 链路层支持的特性集合
    const uint8_t *features;
    // 最大广播集数目
    uint16_t adv_set_num;
    // 最大连接数
    uint16_t conn_num;
    // 白名单列表的大小
    uint16_t whitelist_size;
    // 地址解析列表的大小
    uint16_t resolving_list_size;
    // 周期广播者列表的大小
    uint16_t periodic_advertiser_list_size;
    // 用于检测广播数据重复的过滤器的大小
    uint16_t adv_dup_filter_size;
} ll_capabilities_t;
```

### 12.2.2 工作状态 {#工作状态}

通过 `ll_get_states` 可以获取当前 Controller 的工作状态：

```c
void ll_get_states(uint32_t *adv_states,
    uint32_t *conn_states,
    uint32_t *sync_states,
    uint32_t *other_states);
```

`adv_status[n]` 中第 `n` 的 `uint32_t` 的第 `i` 比特表示第 (n \times 32 + i) 个广播集的工作状态， 为 0 表示未使能，1 表示已使能（正在广播）。`conn_states`、`sync_states` 的含义与之类似。 传入这三个数组指针参数时，数组的长度应为最大数目向上转换为 32 的倍数，再除以 32 所得到的商。 如从 `ll_get_capabilities` 得知最大广播集数目 `adv_set_num` 为 10， 则 `adv_states` 的长度为 1；最大连接数 `conn_num` 为 33，则 `conn_states` 的长度应为 2。

`other_states` 数组长度目前固定为 1，`other_states[0]` 的比特 0 为 1 表示正在扫描；比特 1 为 1 表示正在建立连接。

### 12.2.3 发射功率 {#发射功率}

通过 `ll_set_tx_power_range` 可设置发送功率范围。此范围将被用于广播、连接等各种需要发射的场景。

```c
void ll_set_tx_power_range(
    int16_t min_dBm, // 最小发射功率（单位：dBm）
    int16_t max_dBm);// 最大发射功率（单位：dBm）
```

此范围限制存在于链路层，对 HCI 命令里指定的发射功率起限制作用。如将 `max_dBm` 设置为 0 dBm，则 通过 `gap_set_ext_adv_para` 设置广播的发射功率为 3 dBm 时，最终发射功率会被限制为 0 dBm。

显然，最终的发射功率还受硬件实际支持的范围限制，将 `max_dBm` 设置为 1000 dBm，并不可能得到 1000 dBm 的最大发射功率。

通过 `ll_set_conn_tx_power` 可以直接调节连接的发射功率：

```c
void ll_set_conn_tx_power(
    uint16_t conn_handle, // 连接句柄
    int16_t tx_power);    // 发射功率（单位：dBm）
```

当对端设备支持功率控制特性时，可通过 `ll_adjust_conn_peer_tx_power` 尝试调整对端的发射功率：

```c
void ll_adjust_conn_peer_tx_power(
    uint16_t conn_handle, // 连接句柄
    int8_t delta);        // 功率增量（单位：dB）
```

`delta` 为正数，表示请求对端增加发射功率，为负数则表示降低发射功率。

### 12.2.4 编码方式 {#编码方式}

当需要使用 Coded 编码时，默认采用 S8 方式。

```c
typedef enum coded_scheme_e
{
    BLE_CODED_S8,
    BLE_CODED_S2
} coded_scheme_t;
```

通过 `ll_set_adv_coded_scheme` 修改广播集的 Coded 编码方式：

```c
void ll_set_adv_coded_scheme(
    const uint8_t adv_hdl,       // 广播集句柄
    const coded_scheme_t scheme);//  Coded 编码方式
```

此函数需要在 `adv_hdl` 使能前调用方能生效。

通过 `ll_set_initiating_coded_scheme` 设置以 Coded 编码发送连接请求时的编码方式：

```c
void ll_set_initiating_coded_scheme(
    const coded_scheme_t scheme);
```

此函数需要 `gap_ext_create_connection` 之前调用方能生效。

使用 `ll_set_conn_coded_scheme` 修改连接的 Coded 编码方式：

```c
void ll_set_conn_coded_scheme(
    uint16_t conn_handle, // 连接句柄
    int ci);              //  Coded 编码方式（同 `coded_scheme_t`）
```

### 12.2.5 底层广播参数 {#底层广播参数}

一个广播事件会在多个主广播信道上各发送一个广播数据包（参见 [`primary_adv_channel_map`](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-adv.html#gap_set_ext_adv_para) 参数）。 通过 `ll_legacy_adv_set_interval` 可配置相邻两个广播数据包的间隔：

```c
void ll_legacy_adv_set_interval(
    uint16_t for_hdc, // 用于高占空比情况（单位：μs），默认 1250 μs
    uint16_t not_hdc);// 用于其它情况（单位：μs），默认 1500 μs
```

`platform_config(PLATFORM_CFG_LL_LEGACY_ADV_INTERVAL, flag)` 等效于：

```c
ll_legacy_adv_set_interval(flag >> 16, flag & 0xffff);
```

适当减小间隔可以略微降低功耗。

### 12.2.6 底层连接参数 {#底层连接参数}

Controller 调度连接事件时，以连接事件长度（`ce_len`）为参考。连接建立后的从设备，`ce_len` 总是初始化为连接间隔，即追求最大吞吐率。对于多连接或多状态并发，这种初始设置并不合适。此时，可通过 `ll_hint_on_ce_len` 提示 Controller 实际需要的连接事件长度。将 `ce_len` 调小后，Controller 就可以在连接事件结束后调度其它任务，有效实现多任务并发。

```c
void ll_hint_on_ce_len(
    const uint16_t conn_handle, // 连接句柄
    const uint16_t min_ce_len,  // 事件长度的最小值（单位：0.625 ms）
    const uint16_t max_ce_len); // 事件长度的最大值（单位：0.625 ms）
```

这个函数调整已建立的连接调用。

此函数同样适应于主设备。主设备与从设备的不同在于其 `ce_len` 来自 [phy_configs](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-conn.html#ch-scan-create-connection) 参数。

从机延迟参数可以有效降低速低功耗应用的耗电，但主机端往往把从机延迟设为 0。通过 `ll_set_conn_latency` 可以为从机**主动**设置从机延迟参数降低功耗：

```c
void ll_set_conn_latency(
    uint16_t conn_handle,   // 连接句柄
    int latency);           // 从机延迟参数
```

注意：不建议在使用了减速模式的情况下使用。

通过 `ll_get_conn_info` 可以读取连接的基础参数：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_get_conn_info(
    const uint16_t conn_handle, // 连接句柄
    uint32_t *access_addr,      // 接入地址
    uint32_t *crc_init,         // CRC 初始值
    uint8_t *hop_inc);          // 信道选择算法 #1 跳频增量
```

通过 `ll_get_conn_events_info` 获取未来若干连接事件的参数信息：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_get_conn_events_info(
    const uint16_t conn_handle, // 连接句柄
    int number,                 // 连接事件个数
    uint64_t from_time,         // 时间参考
    uint32_t *interval,         // 输出：连接间隔（单位：μs）
    uint32_t *time_offset,      // 输出：第一个连接事件与 `from_time` 的时间差
    uint16_t *event_count,      // 输出：第一个连接事件的事件计数值
    uint8_t *channel_ids);      // 输出：`number` 个物理信道号
```

这个函数输出 `from_time` 之后 `number` 个连接事件的物理信道号等参数。注意：这个函数假定从当前时刻到 `number` 个连接事件结束信道参数不发生变化，并且忽略减速模式参数。当信道参数发生变化时（如连接参数更新、信道集合更新）， 输出的参数将是不可靠的。

### 12.2.7 默认天线 {#默认天线}

当系统配置了多个天线（如使用 CTE、信道探测等特性时）时，通过 `ll_set_def_antenna` 可设置射频工作时的默认天线 ID：

```c
void ll_set_def_antenna(uint8_t ant_id);
```

这个设置直接写入硬件，立即生效。

### 12.2.8 单信道扫描 {#单信道扫描}

扫描广播时，在每个扫描窗口轮流扫描 3 个主广播信道。可通过 `ll_scan_set_fixed_channel` 限定只扫描其中一个主广播信道。

```c
void ll_scan_set_fixed_channel(
    int channel_index);
```

`channel_index` 可以是 37、38 或 39；也可以是 0，表示解除锁定，恢复为轮流扫描所有主广播信道。

此项设置一直生效。

## 12.3 连接中止与重建 {#连接中止与重建}

通过 `ll_create_conn` 可以跳过广播、连接建立过程，直接创建或者恢复连接：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_create_conn(
    uint8_t role,               // 角色。主（0），从（1）
    uint8_t addr_types,         // 广播者和连接发起者的地址类型
    const uint8_t *adv_addr,    // 广播者地址
    const uint8_t *init_addr,   // 连接发起者的地址
    uint8_t rx_phy,             // 接收 PHY（以主角色为参考）
    uint8_t tx_phy,             // 发射 PHY（以主角色为参考）
    uint32_t access_addr,       // 接入地址
    uint32_t crc_init,          // CRC 初始值
    uint32_t interval,          // 连接间隔（单位：μs）
    uint16_t sup_timeout,       // 超时时间（单位：10 ms）
    const uint8_t *channel_map, // 信道集合（5 个字节，37 个信道的 bitmap）
    uint8_t  ch_sel_algo,       // 信道选择算法（0: 算法 #1; 1：算法 #2）
    uint8_t  hop_inc,           // 跳频增量（仅用于信道选择算法 #1）
    uint8_t  last_unmapped_ch,  // 上一次未映射信道号（仅用于信道选择算法 #1）
    uint16_t min_ce_len,        // 事件长度的最小值（单位：0.625 ms）
    uint16_t max_ce_len,        // 事件长度的最大值（单位：0.625 ms）
    uint64_t start_time,        // 首个连接事件的起始时间（单位：μs）
    uint16_t event_counter,     // 首个连接事件的事件计数值
    uint16_t slave_latency,     // 从机延迟参数
    uint8_t  sleep_clk_acc,     // 睡眠时钟精度（仅用于从角色）
    uint32_t sync_window,       // 首个连接事件的同步窗口长度（单位：0.625ms）
    const void *security);      // 链路层安全上下文
```

`security` 来自 `HCI_SUBEVENT_LE_VENDOR_CONNECTION_ABORTED` 事件，NULL 表示不加密。

使用 `ll_conn_abort` 中止连接：

```c
// 中止流程成功启动时返回 0，否则返回非 0 值。
int ll_conn_abort(
    uint16_t conn_handle);      // 连接句柄
```

连接中止后，将上报 `HCI_SUBEVENT_LE_VENDOR_CONNECTION_ABORTED` 事件。

## 12.4 广播上的 CTE {#广播上的-cte}

CTE 私有方案 #2[58](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn58) 使用扩展广播发送 CTE。通过 `ll_attach_cte_to_adv_set` 为已初始化且未使能的广播集附着 CTE：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_attach_cte_to_adv_set(
    uint8_t adv_handle,             // 广播集句柄
    uint8_t cte_type,               // CTE 类型
    uint8_t cte_len,                // CTE 长度（单位：8 μs）
    uint8_t switching_pattern_len,  // 天线切换模板（发送 AoD 时使用）
    const uint8_t *switching_pattern);
```

CTE 类型 `cte_type` 包含 AoA（0）、AoD 1μs 切换（1）、AoD 1μs 切换（1）。

会导致的该函数失败的几种原因：

- 指定的广播集未初始化（参见“[广播的配置](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-adv.html#gap_set_ext_adv_para)”）；
- 指定的广播集不是扩展广播；
- 内存不足。

启动了扫描后，通过 `ll_scanner_enable_iq_sampling` 开始接收扩展广播上附着的 CTE：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_scanner_enable_iq_sampling(
    uint8_t cte_type,                 // 固定填 0
    uint8_t slot_len,                 // 时隙长度
    uint8_t switching_pattern_len,    // 天线切换模板（接收 AoA 时使用）
    const uint8_t *switching_pattern,
    uint8_t slot_sampling_offset,     // 时隙内采样偏移（0..23）
    uint8_t slot_sample_count);       // 时隙内采样数（1..5）
```

`slot_len` 的取值与 `cte_slot_duration_type_t` 相同。采样时，从每个时隙的 `slot_sampling_offset` / 24 μs 处开始， 连续采样 `slot_sample_count` 次，采样频率 24MHz。`slot_sampling_offset` 与 `slot_sample_count` 的和必须小于等于 24。建议 `slot_sampling_offset` 取 12，`slot_sample_count` 取 1。

如果扫描未开始，则该函数将失败。扫描停止后，CTE IQ 采样同步停止。再次开始扫描时，需要重新调用该函数才能继续采样。

IQ 采样通过 `HCI_SUBEVENT_LE_VENDOR_PRO_CONNECTIONLESS_IQ_REPORT` 事件上报。

通过 `ll_scanner_enable_iq_sampling_on_legacy`[59](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn59) 可对传统广播的数据部分做 IQ 采样：

```c
int ll_scanner_enable_iq_sampling_on_legacy(
    uint16_t sampling_offset,        // 采样起始位置（单位：比特）
    uint8_t cte_type,                // 固定填 0
    uint8_t cte_time,                // CTE 时长（单位：8 μs）
    uint8_t slot_len,                // 时隙长度
    uint8_t switching_pattern_len,   // 天线切换模板（接收 AoA 时使用）
    const uint8_t *switching_pattern,
    uint8_t slot_sampling_offset,    // 时隙内采样偏移（0..23）
    uint8_t slot_sample_count);      // 时隙内采样数（1..5）
```

与 `ll_scanner_enable_iq_sampling` 相比，这个函数增加了两个参数：`sampling_offset` 和 `cte_time`。 `sampling_offset` 表示采样起始位置，0 对应于 Payload 的第 0 个比特。例如，要采样 `ADV_IND` 的 `AdvData` 部分， 则把 `sampling_offset` 取做 (6 \times 8 =) 48，以跳过长度为 6 个字节的 `AdvA`。 IQ 采样通过 `HCI_SUBEVENT_LE_VENDOR_PRO_CONNECTIONLESS_IQ_REPORT` 事件上报。[60](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn60)。

此功能可能导致系统卡死或者产生 HardFault。务必配合硬件看门狗使用。

## 12.5 原始包（Raw Packet）对象 {#原始包raw-packet对象}

Raw Packet 对象是一种不透明的数据结构：

```c
struct ll_raw_packet;
```

这部分接口是面向对象的，不同功能的对象使用不同的函数创建。 销毁统一使用 `ll_raw_packet_free` 接口：

```c
void ll_raw_packet_free(
    struct ll_raw_packet *packet); // 要销毁的对象
```

必须待工作完成才能销毁。工作完成时通过回调函数通知应用。回调函数类型如下：

```c
typedef void (* f_ll_raw_packet_done)(
    struct ll_raw_packet *packet, // 产生回调的对象
    void *user_data);             // 用户数据
```

不同功能的对象使用方法类似：1）创建对象；2）设置信道参数；3）设置数据；4）运行；5）在回调函数中读取数据和状态。 对象的运行函数，如 `ll_raw_packet_send`，立即返回而不是阻塞到运行完成；只要运行函数返回了表示成功的值，回调函数就必然被调用。 运行函数一旦返回了表示成功的值，在完成运行之前（即回调函数被调用前），不允许再调用对象的其它方法。

没有用于“取消运行”的接口。

### 12.5.1 无响应的包 {#无响应的包}

无响应的 Raw Packet 通信包含两个角色：

- 发送方：在指定的时间发送一包数据，发送完成即任务完成；
- 接收方：在指定的时间窗口内持续接收数据，接收成功一包数据或者接收窗口结束时任务完成。

#### 12.5.1.1 创建与配置 {#创建与配置}

使用 `ll_raw_packet_alloc` 创建对象：

```c
struct ll_raw_packet *ll_raw_packet_alloc(
    uint8_t for_tx,               // 角色（0: 接收方；1：发送方）
    f_ll_raw_packet_done on_done, // 回调函数
    void *user_data);             // 传给回调函数的用户数据
```

使用 `ll_raw_packet_set_param` 配置信道参数：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_raw_packet_set_param(
    struct ll_raw_packet *packet,
    int8_t tx_power,        // 发射功率（单位：dBm）
    int8_t rf_channel_id,   // 射频信道号
    uint8_t phy,            // PHY
    uint32_t access_addr,   // 接入地址
    uint32_t crc_init);     // CRC 初始值
```

射频信道号 `rf_channel_id` 范围为 0 ~ 39，当其值为 k 时，信道中心频率为 (2402 + 2k) MHz。 PHY 的取值见表 [12.1](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#tab:ch-ctrl-phy-types)。

*表 12.1: PHY 类型*
| 取值 | 含义（发送方） | 含义（接收方） |
| --- | --- | --- |
| 1 | 1M | 1M |
| 2 | 2M | 2M |
| 3 | Coded S8 | Coded |
| 4 | Coded S2 | — |

接入地址 `access_addr` 和 CRC 初始值 `crc_init` 的含义和用法与蓝牙核心规范一致。

#### 12.5.1.2 发送 {#发送}

发送方通过 `ll_raw_packet_set_tx_data` 设置待发送的数据：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_raw_packet_set_tx_data(
    struct ll_raw_packet *packet,
    uint8_t header,     // 头数据（仅限低 2 比特）
    const void *data,   // 数据
    int size);          // 数据长度（单位：字节。最大 254)
```

如果附着了 CTE，`size` 最大支持 252 字节。当数据长度过长时，返回 1。

通过 `ll_raw_packet_send` 在指定的时刻发送：

```c
// 可以在指定时刻发送时返回 0，否则返回非 0 值。
int ll_raw_packet_send(
    struct ll_raw_packet *packet,
    uint64_t when); // 发送时刻（单位：μs）
```

当 `platform_get_us_time()` 等于 `when` 时，启动发送。当 Controller 无法在指定的时间发送时（如与其它任务时间冲突， 时间太迟等），返回非 0 值。 `ll_raw_packet_send(packet, platform_get_us_time() + OFFSET)`，当 `OFFSET` 小于一定值 `T` 时，会因为时间太迟而返回非 0 值。 `T` 值与芯片处理能力有关，一般为 100 到几百微秒。其它接口的 `when` 参数用法与此相同。

发送完成后，如果需要再次发送相同的数据，直接调用 `ll_raw_packet_send` 即可，无需重新设置数据。

#### 12.5.1.3 接收 {#接收}

通过 `ll_raw_packet_recv` 在一定时间窗口内尝试接收数据包：

```c
// 可以在指定窗口接收则返回 0，否则返回非 0 值。
int ll_raw_packet_recv(
    struct ll_raw_packet *packet,
    uint64_t when,      // 接收窗口开始的时刻（单位：μs）
    uint32_t rx_window);// 窗口长度（单位：μs）
```

当 `platform_get_us_time()` 等于 `when` 时，开始尝试接收。这个函数立即返回，而非阻塞到接收完成再返回。 从成功调用 `ll_raw_packet_set_tx_data` 到收到回调前，不可调用这个对象的其它方法。

在回调函数里调用 `ll_raw_packet_get_rx_data` 读取接收状态和数据：

```c
// 返回接收状态
int ll_raw_packet_get_rx_data(
    struct ll_raw_packet *packet,
    uint64_t *air_time, // 数据包在空口出现的时间
    uint8_t *header,    // 头数据（仅 2 比特）
    void *data,         // 用来接收数据的缓存
    int *size,          // 接收到的数据包的长度
    int *rssi);         // 接收到的数据包的 RSSI
```

返回值解释：

- 0：成功接收，CRC 正确；
- 1：未接收到任何信息（指定的信道上无信号，或者任务未执行）；
- 2：接收到数据，但是出现接入码错误、CRC 错误等；
- 5：数据长度错误；
- 6：帧结构错误。

当出现非 0 错误码，但是错误码不属于 \{1, 2\} 时，`air_time`、`header`、`rssi` 等 3 项输出有效。

#### 12.5.1.4 附着 CTE {#附着-cte}

CTE 私有方案 #1[61](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn61) 使用 Raw Packet 发送 CTE。发送方通过 `ll_raw_packet_set_tx_cte` 附着 CTE：

```c
int ll_raw_packet_set_tx_cte(
    struct ll_raw_packet *packet,
    uint8_t cte_type,
    uint8_t cte_len,
    uint8_t switching_pattern_len,
    const uint8_t *switching_pattern);
```

`ll_raw_packet_set_tx_cte` 各参数含义与 `ll_attach_cte_to_adv_set` 类似，不再赘述。 需要 `ll_raw_packet_send(...)` 之前调用。

接收方通过 `ll_raw_packet_set_rx_cte` 设置 CTE 接收参数：

```c
int ll_raw_packet_set_rx_cte(
    struct ll_raw_packet *packet,
    uint8_t cte_type,
    uint8_t slot_len,
    uint8_t switching_pattern_len,
    const uint8_t *swiching_pattern,
    uint8_t slot_sampling_offset,
    uint8_t slot_sample_count);
```

`ll_raw_packet_set_rx_cte` 各参数含义与 `ll_scanner_enable_iq_sampling` 类似，不再赘述。 需要 `ll_raw_packet_recv(...)` 之前调用。

完成接收后，在回调函数里通过 `ll_raw_packet_get_iq_samples` 获取 IQ 采样：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_raw_packet_get_iq_samples(
    struct ll_raw_packet *packet,
    void *iq_samples,    // 接收 IQ 采样的缓存
    int *iq_sample_cnt,  // 采样的数量
    int preprocess);     // 是否进行预处理
```

`iq_samples` 得到的数据顺序为“IQIQIQ……”。 `preprocess` 为 0 时，不进行预处理，直接输出原始 IQ 采样数据，每个分量类型为`int16_t`； `preprocess` 为非 0 时，进行预处理，输出处理后的 IQ 采样数据，每个分量类型为`int8_t`。 预处理仅支持 `slot_sample_count` 为 1 的情况。 必须为 `iq_samples` 预留足够的空间。

函数返回的错误码如下：当未收到 CTE 时，该函数返回 1；`preprocess` 非 0 且 `slot_sample_count` 大于 1 时，返回 2。

对于发送方，提供了一种发送虚假 CTEInfo 数据域的方法：待调用了 `ll_raw_packet_set_tx_cte` 之后，通过 `ll_raw_packet_set_fake_cte_info` 填写虚假 CTEInfo 数据域。在发送时，CTE 按照 `ll_raw_packet_set_tx_cte` 指定的参数发送，但是数据包内协带的 CTEInfo 数据域却是修改过的。接收方处理 CTE 时将按照这个虚假的 CTEInfo 接收 CTE。

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_raw_packet_set_fake_cte_info(
    struct ll_raw_packet *packet,
    uint8_t cte_type,
    uint8_t cte_len);
```

如果对象未通过 `ll_raw_packet_set_tx_cte` 配置 CTE，则返回 1；如果 CTE 参数错误，则返回 2。其它情况返回 0。

用途举例：通过 `ll_raw_packet_set_tx_cte` 设置发送 AoD；通过 `ll_raw_packet_set_fake_cte` 填入 AoA。 这样，双方在发送和接收 CTE 时分别切换天线，在天线控制端口可产生严格同步的脉冲信号输出。

#### 12.5.1.5 “裸包”模式 {#裸包模式}

无响应的 Raw Packet 通信默认使用与蓝牙规范一致的信道白化和 CRC 校验。另外提供一种关闭白化和 CRC 校验的“裸包”模式。 在这种模式下，空口数据完全由开发者负责生成和校验，硬件只负责 PREAMBLE 和接入地址的比对。 收发双方都通过 `ll_raw_packet_set_bare_mode` 启用“裸包”模式：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_raw_packet_set_bare_mode(
    struct ll_raw_packet *packet,
    uint8_t header, // 在数据包长之前发送的头数据
    int freq_mhz);  // 信道中心频点（单位：MHz）
```

仅支持发送 `header` 里部分比特，建议固定填写 0。当 `freq_mhz` 为 0 时，继续使用 `ll_raw_packet_set_param` 所指定的信道；当其非 0 时，需要注意仍可能对邻近蓝牙信道产生干扰；当其在蓝牙 2.4GHz 频段以外时，行为未知。 当输入参数不合理时，这个函数将返回非 0 值。

通过 `ll_raw_packet_set_bare_data` 设置数据：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_raw_packet_set_bare_data(
    struct ll_raw_packet *packet,
    const void *data,       // 数据
    int size,               // 最大 255 字节
    uint32_t crc_value);    // 附加在数据之后的 CRC（低 24 比特）
```

在接收端回调里通过 `ll_raw_packet_get_bare_rx_data` 获取接收状态和数据：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_raw_packet_get_bare_rx_data(
    struct ll_raw_packet *packet,
    uint64_t *air_time,   // 数据包在空口出现的时间
    uint8_t *header,      // 头数据
    void *data,           // 用来接收数据的缓存
    int *size,            // 接收到的数据包的长度
    int *rssi,            // 接收到的数据包的 RSSI
    uint32_t *crc_value); // 附加在数据之后的 CRC（低 24 比特）
```

在指定的信道、指定的窗口未能与接入地址比对成功时，返回 2；否则返回 0。

### 12.5.2 带确认的包（Ack-able Packet） {#带确认的包ack-able-packet}

带确认的包可以在通信双方之间可靠地向对方传输一包数据。通信双方分别称为：

- 发起者（Initiator）：在指定的时间开始发送数据，并在一定的时间窗口内等待对方发来的确认和数据包；
- 应答者（Responder）：从指定的时间开始尝试接收数据，如果成功，自动向对方发送确认信息和己方数据包。

在接收数据过程中，如果一方发现 CRC 错误，会自动请求对方重传。

#### 12.5.2.1 创建与配置 {#创建与配置-1}

通过 `ll_ackable_packet_alloc` 创建带确认的包对象：

```c
// 创建成功返回对象指针；否则返回 NULL
struct ll_raw_packet *ll_ackable_packet_alloc(
    uint8_t for_initiator,        // 角色（1：发起者；0：应答者）
    f_ll_raw_packet_done on_done, // 回调函数
    void *user_data);             // 传给回调函数的用户数据
```

使用 `ll_raw_packet_set_param` 配置参数。通过 `ll_ackable_packet_set_tx_data` 设置已方要发送数据（如不设置，则表示要发送的数据长度为 0）：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_ackable_packet_set_tx_data(
    struct ll_raw_packet *packet,
    const void *data, // 数据
    int size);        // 长度（单位：字节），最大 255 字节
```

#### 12.5.2.2 运行 {#运行}

通过 `ll_ackable_packet_run` 设置对象的运行时机：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_ackable_packet_run(
    struct ll_raw_packet *packet,
    uint64_t when,      // 接收窗口开始的时刻（单位：μs）
    uint32_t window);   // 窗口长度（单位：μs）
```

`window` 至少应为 0.625 ms，建议取 1.25ms 以上。

收到回调后通过 `ll_ackable_packet_get_status` 获取己方数据的确认状态和接收到的数据：

```c
// 返回对方数据的接收状态
int ll_ackable_packet_get_status(
    struct ll_raw_packet *packet,
    int *acked,         // 己方数据的确认状态
    uint64_t *air_time, // 对方数据包的空口时间
    void *data,         // 对方数据包的数据
    int *size,          // 对方数据包的大小
    int *rssi);         // 对方数据包的 RSSI
```

成功接收到对方数据时这个函数返回 0；否则返回其它错误码，无具体含义。`acked` 为 1 说明己方的数据被对方成功收到。

`acked` 是否为 1 与这个函数是否返回 0 没有必然联系。

### 12.5.3 信道监听 {#信道监听}

信道监听是在指定的信道上持续接收数据包，直到收到指定的数目或者接收窗口结束。可能的用途：

- 在单一信道上接收广播数据；
- 监听一个连接事件内通信双方的所有数据包；

  理想情况下（合理配置启动时间），收到的第 1 个 PDU 是主角色发送给从角色的，第 2 个是从角色发送给主角色的，依此类推。

#### 12.5.3.1 创建与配置 {#创建与配置-2}

通过 `ll_channel_monitor_alloc` 创建信道监听对象：

```c
// 创建成功时返回对象指针，否则返回 NULL
struct ll_raw_packet *ll_channel_monitor_alloc(
    int pdu_num,     // 一次监听最多接收的包的数量
    f_ll_raw_packet_done on_done, // 回调函数
    void *user_data);             // 用户数据
```

使用 `ll_raw_packet_set_param` 配置参数。

#### 12.5.3.2 运行 {#运行-1}

通过 `ll_channel_monitor_run` 运行监听对象：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_channel_monitor_run(
    struct ll_raw_packet *packet,
    uint64_t when,    // 监听启动时间（单位：μs）
    uint32_t window); // 窗长（单位：μs）
```

收到回调后，通过 `ll_channel_monitor_check_each_pdu` 依次遍历收到的数据包：

```c
// 返回 `visitor` 的调用次数
int ll_channel_monitor_check_each_pdu(
    struct ll_raw_packet *packet,
    f_ll_channel_monitor_pdu_visitor visitor, // 访问者回调
    void *user_data);   // 用户数据
```

访问者回调的类型如下：

```c
typedef void (* f_ll_channel_monitor_pdu_visitor)(
    int index,          // 包序号
    int status,         // 接收状态
    uint8_t reserved,   // 保留
    const void *data,   // 数据
    int size,           // 数据长度
    int rssi,           // RSSI
    void *user_data);   // 用户数据
```

`index` 从 0 开始，最大到 `pdu_num - 1`。`status` 为 0 表示该包成功接收；不为 0 时，表示接收失败， `data`、`size`、`rssi` 等输出皆无效。

ING918 仅支持获取 `rssi`。`data`、`size` 无输出。

通过 `ll_channel_monitor_get_1st_pdu_time` 获得第 1 个数据包的空口时间：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_channel_monitor_get_1st_pdu_time(
    struct ll_raw_packet *packet,
    uint64_t *air_time); // 空口时间
```

如果未成功收到数据包，这个函数会失败，返回非 0 值。

## 12.6 内存管理 {#内存管理}

Controller 管理了一个单独的堆空间，并对外提供接口供开发者使用。

使用 `ll_malloc` 分配内存：

```c
// 分配失败时返回 NULL
void *ll_malloc(
    uint16_t size); // 大小（单位：字节）
```

使用 `ll_free` 释放内存：

```c
void ll_free(void *buffer);
```

通过 `ll_get_heap_free_size` 获取当前未分配的空间大小：

```c
// 返回当前未分配的空间大小（单位：字节）
int ll_get_heap_free_size(void);
```

过多地从 Controller 分配内存，将影响蓝牙功能。

## 12.7 低时延接口 {#低时延接口}

### 12.7.1 ACL 预览 {#acl-预览}

ACL 数据从 Controller 传输到 Host 再通知应用存在一定的时延。如果开发者需要更及时地获取 ACL 数据， 可通过 `ll_register_hci_acl_previewer` 注册数据预览回调：

```c
void ll_register_hci_acl_previewer(
    f_ll_hci_acl_data_preview preview);
```

回调函数的类型如下：

```c
typedef void (*f_ll_hci_acl_data_preview)(
    uint16_t conn_handle,    // 连接句柄
    const uint8_t acl_flags, // ACL 标志位
    const void *data,        // 数据
    int len);                // 数据长度
```

ACL 标志位的含义如下：

- `0x01`：L2CAP 消息的一个接续片断或者空 PDU；
- `0x02`：L2CAP 新消息的第一个片断或者一条完整的 L2CAP 消息。

### 12.7.2 AES 加密 {#aes-加密}

通过 GAP 接口进行 [AES-128 加密](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#ch-misc-aes-encrypt)，存在一定的时延。通过 `ll_aes_encrypt` 可以以阻塞模式立即调用硬件完成加密并得到结果：

```c
// 函数执行成功时返回 0，否则返回非 0 值。
int ll_aes_encrypt(
    const uint8_t *key,       // 密钥（小端模式）
    const uint8_t *plaintext, // 明文（小端模式）
    uint8_t *ciphertext);     // 密文（大端模式）
```

当硬件正忙，无法计算时，该函数返回非 0 值。使用时请注意参数的大小端模式与 `gap_aes_encrypt` 不同。

## 12.8 “非标”选项 {#非标选项}

### 12.8.1 锁频 {#锁频}

锁频功能可将后续所有的射频行为（蓝牙广播、扫描、连接，原始包等）全部固定在指定的信道上。 通过 `ll_lock_frequency` 开启锁定并指定频率：

```c
void ll_lock_frequency(
    int freq_mhz); // 频率（单位：MHz）
```

锁频是一种底层设置，链路层并不知晓。例如，将广播者锁频在 2402 MHz，扫描者扫描 37 信道时，在一个广播件内并不能同时收到 3 个广播包。 这是因为广播者链路层在发送 3 个广播包时仍然按照 37/38/39 设置白化参数，虽然它们最终都在 37 信道发送。

通过 `ll_unlock_frequency` 解除锁定：

```c
void ll_unlock_frequency(void);
```

嵌套 `ll_lock_frequency` 时，可能产生意外效果，例如：

```c
lock(f0);       // 锁定到 f0
    lock(f1);   // 锁定到 f1
    unlock();
    ...         // 此时依然处于锁频状态，锁定于 f1
unlock();
...             // 已解锁
```

### 12.8.2 自定义参数62 {#自定义参数}

通过 `ll_set_adv_access_address` 替换蓝牙核心规范定义的广播包接入地址：

```c
void ll_set_adv_access_address(
    uint32_t acc_addr);
```

通过 `ll_override_whitening_init_value` 替换蓝牙核心规范定义的白化初始值：

```c
void ll_override_whitening_init_value(
    uint8_t override,  // 是否替换
    uint8_t value);    // 白化初始值
```

当 `override` 为 0 时，恢复使用规范值，`value` 参数忽略；为 1 时，`value` 的各比特依次放入移位寄存器的相应位置，即 `lfsr[0]` 填入最低比特，`lfsr[1]` 填入 `(value >> 1) & 1`，依此类推。 使用这种表示法，规范为 37 信道定义的白化初始值表示为 `0x53`。

广播物理信道 PDU 包含长度为 4 个比特的 `PDU Type`。 Controller 接收到的 `PDU Type` 为预留值时，整个 PDU 会被丢弃。通过 `ll_allow_nonstandard_adv_type` 可以使能接收一种非标 `PDU Type`：

```c
void ll_allow_nonstandard_adv_type(
    uint8_t allowed, // 是否使能非标 ADV 接收
    uint8_t type);   // 非标类型值
```

当 `allowed` 为 0 时，功能关闭，`type` 参数忽略；为 1 时，扫描时会接收 `type` 类型的广播 PDU 并上报。

规范定义 CTE 比特为 1。通过 `ll_set_cte_bit` 可修改其定义：

```c
void ll_set_cte_bit(
    uint8_t bit);  // CTE 比特（0 或 1）
```

规范定义连接间隔时，单位为 1.25 ms。通过 `ll_set_conn_interval_unit` 可自定义该值：

```c
void ll_set_conn_interval_unit(
    uint16_t unit); // （单位：μs）默认值：1250
```

此设置应该在连接建立前修改，通信双方必须使用相同的设置。`unit` 允许的最小值依赖硬件处理能力， ING918 为 800 μs 左右。将连接间隔调小，可明显降低通信时延。例如，标准中最小连接间隔为 7.5 ms； 使用 *extension* 包，ING918 连接间隔最小可降为 (800 \times 1 =) 800 μs。

## 12.9 ECC 引擎 {#ecc-引擎}

当 Controller 未内置 ECC 硬件时，允许应用提供 ECC 引擎，并通过 HCI 为 Host 提供服务。 通过 `ll_install_ecc_engine` 定义 ECC 引擎：

```c
void ll_install_ecc_engine(
    f_start_generate_p256_key_pair start_generate_p256_key_pair,
    f_start_generate_dhkey start_generate_dhkey);
```

ECC 引擎应该能够安全地保存一个公钥对，并实现两个接口（回调函数），：

- `start_generate_p256_key_pair`：开始生成新的 P256 密钥对；
- `start_generate_dhkey`：开始生成 DHKey。

`f_start_generate_p256_key_pair` 的定义为：

```c
typedef void (*f_start_generate_p256_key_pair)(void);
```

这个函数在 Controller 的上下文中调用，应该立即返回。当 P256 密钥对生成或出现错误后，通过 `ll_p256_key_pair_generated` 告知结果：

```c
void ll_p256_key_pair_generated(
    int status,              // 是否成功（0：成功）
    const uint8_t *pub_key); // 生成的公钥
```

`status` 表示是否成功生成了新的密钥对，0 为成功，其它值为不成功。当成功时，`pub_key` 包含新生成的公钥，长度为 64 字节， 前 32 字节为 X 坐标，后 32 字节为 Y 坐标，大端模式。

`f_start_generate_dhkey` 的定义为：

```c
typedef int  (*f_start_generate_dhkey)(
    int key_type,                   // 本端的密钥类型
    const uint8_t *remote_pub_key); // 远端的公钥
```

`key_type` 为 0 时，选用引擎生成的私钥；为 1 时使用规范定义的调试用私钥[63](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn63)。 `remote_pub_key` 为远端的公钥，长度为 64 字节，前 32 字节为 X 坐标，后 32 字节为 Y 坐标，大端模式。

这个函数也是在 Controller 的上下文中调用，应该立即返回。当 DHKey 生成或出现错误后，通过 `ll_p256_key_pair_generated` 告知结果：

```c
void ll_dhkey_generated(
    int status,             // 是否成功（0：成功）
    const uint8_t *dh_key); // Diffie Hellman Key
```

`status` 为 0 时，表示 DHKey 生成成功，其它值为不成功。当成功时，`dh_key` 包含新生成的 DHKey，长度为 32 字节， 大端模式。ECC 引擎必须首先检验远端公钥是否合法，如不合法，直接调用 `ll_dhkey_generated`，将 `status` 设为非 0 值。

---

1. <a id="fn57"></a>典型值。不同软件包有所不同。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref57)
2. <a id="fn58"></a>更多信息请参考《Application Note: Direction Finding Solution》, [https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2](https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref58)
3. <a id="fn59"></a>ING918 不支持此功能。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref59)
4. <a id="fn60"></a>关于原理、使用方法等更多信息请参考《使用 ING916 定位传统蓝牙设备》，[https://ingchips.github.io/blog/2023-03-11-legacy-aoa/](https://ingchips.github.io/blog/2023-03-11-legacy-aoa/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref60)
5. <a id="fn61"></a>更多信息请参考《Application Note: Direction Finding Solution》, [https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2](https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref61)
6. <a id="fn62"></a>本节功能中，ING918 仅支持自定义连接间隔。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref62)
7. <a id="fn63"></a>参见蓝牙核心规范 Vol 3, Part H, 2.3.5.6 LE Secure Connections pairing phase 2.[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref63)