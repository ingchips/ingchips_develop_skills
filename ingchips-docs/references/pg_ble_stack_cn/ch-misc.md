<!-- pg_ble_stack_cn: 14 杂项 -->

# 14 杂项 {#ch-misc}

## 14.1 接收 CTE {#接收-cte}

共有四种 CTE 接收、发送方式[64](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn64)。 以 AoA 为例，各种方式的使用方法如下。

### 14.1.1 基于连接的 CTE 接收和发送 {#基于连接的-cte-接收和发送}

这种方式的使用可参考 SDK *Central CTE* 和 *Peripehral LED & CTE*。

#### 14.1.1.1 发送方 {#发送方}

建立连接后：

1. 调用 `gap_set_connection_cte_tx_param` 配置发送参数：

   ```c
   uint8_t gap_set_connection_cte_tx_param(
     // 连接句柄
     const hci_con_handle_t  conn_handle,
     // 允许发送的 CTE 类型组合
     const uint8_t           cte_types,
     // 用于 AoD 发送的天线切换模板的长度
     const uint8_t           switching_pattern_len,
     // 用于 AoD 发送的天线切换模板
     const uint8_t          *antenna_ids
   );
   ```

   对于 AoA 模式，不需要配置天线切换模板，但是模板的长度必须至少为 2：

   ```c
   gap_set_connection_cte_tx_param(
     con_handle, (1 << CTE_AOA), 2, NULL);
   ```
2. 调用 `gap_set_connection_cte_response_enable` 使能 CTE 响应：

   ```c
   uint8_t gap_set_connection_cte_response_enable(
     // 连接句柄
     const hci_con_handle_t  conn_handle,
     // 是否使能
     const uint8_t           enable);
   ```

#### 14.1.1.2 接收方 {#接收方}

使用 `ll_set_def_antenna` 配置默认天线。建立连接后：

1. 调用 `gap_set_connection_cte_rx_param` 配置接收参数：

   ```c
   uint8_t gap_set_connection_cte_rx_param(
     // 连接句柄
     const hci_con_handle_t  conn_handle,
     // 是否使能 CTE 采样
     const uint8_t           sampling_enable,
     // 时隙长度
     const cte_slot_duration_type_t slot_durations,
     // 天线切换模板的长度
     const uint8_t           switching_pattern_len,
     // 天线切换模板
     const uint8_t          *antenna_ids);
   ```

   时隙长度共有两种：

   ```c
   typedef enum
   {
       CTE_SLOT_DURATION_1US = 1,
       CTE_SLOT_DURATION_2US = 2
   } cte_slot_duration_type_t;
   ```

   关于天线切换模板的更多信息请参考《Application Note: Direction Finding Solution》。
2. 调用 `gap_set_connection_cte_request_enable` 开始发送 CTE 请求

   连接模式的 CTE 为按需发送：一方发送一次 CTE 请求，对方就响应一次。

   ```c
   uint8_t gap_set_connection_cte_request_enable(
     // 连接句柄
     const hci_con_handle_t  conn_handle,
     // 是否使能
     const uint8_t           enable,
     // 发送 CTE 请求的间隔
     const uint16_t          requested_cte_interval,
     // 请求的 CTE 的长度（范围 2~20，单位 8μs）
     const uint8_t           requested_cte_length,
     // 请求的 CTE 的类型
     const cte_type_t        requested_cte_type);
   ```

   `requested_cte_interval` 表示每 `requested_cte_interval` 个连接间隔发送一次 CTE 请求， 0 表示只发送一次。 对于 AoA，`requested_cte_type` 为 `CTE_AOA`。
3. 响应 `HCI_SUBEVENT_LE_CONNECTION_IQ_REPORT` 事件

   使用 `decode_hci_le_meta_event` 解析事件内容：

   ```c
   const le_meta_conn_iq_report_t *rpt =
     decode_hci_le_meta_event(packet, le_meta_conn_iq_report_t);
   ```

   如果 CTE 请求失败（未收到响应），则会收到 `HCI_SUBEVENT_LE_CTE_REQ_FAILED` 事件。

### 14.1.2 基于周期广播的 CTE 接收和发送 {#misc-cte-periodic-adv}

这种方式的使用可参考 SDK *Periodic Advertiser* 和 *Periodic Scanner*。

#### 14.1.2.1 发送方 {#发送方-1}

使能周期广播后，

1. 调用 `gap_set_connectionless_cte_tx_param` 配置 CTE 发送参数

   ```c
   uint8_t gap_set_connectionless_cte_tx_param(
     // 广播句柄
     const uint8_t       adv_handle,
     // CTE 长度（范围 2~20，单位 8μs）
     const uint8_t       cte_len,
     // CTE 类型（对于 AoA，即 CTE_AOA）
     const cte_type_t    cte_type,
     // 一个周期广播里 CTE 发送次数
     const uint8_t       cte_count,
     // 用于 AoD 发送的天线切换模板的长度
     const uint8_t       switching_pattern_len,
     // 用于 AoD 发送的天线切换模板
     const uint8_t      *antenna_ids);
   ```
2. 调用 `gap_set_connectionless_cte_tx_enable` 使能 CTE 发送

   ```c
   uint8_t gap_set_connectionless_cte_tx_enable(
     // 广播句柄
     const uint8_t       adv_handle,
     // 是否使能
     const uint8_t       cte_enable);
   ```

   #### 接收方 {#接收方-1}

与周期广播建立同步后，调用 `gap_set_connectionless_iq_sampling_enable` 启动 CTE 接收。

```c
uint8_t gap_set_connectionless_iq_sampling_enable(
  // 同步句柄
  const uint16_t      sync_handle,
  // 是否使能采样
  const uint8_t       sampling_enable,
  // 时隙长度
  const cte_slot_duration_type_t slot_durations,
  // 每个周期广播间隔内最多接收多少个 CTE
  const uint8_t       max_sampled_ctes,
  // 天线切换模板长度
  const uint8_t       switching_pattern_len,
  // 天线切换模板
  const uint8_t      *antenna_ids);
```

此后就可以周期性收到 `HCI_SUBEVENT_LE_CONNECTIONLESS_IQ_REPORT` 事件，利用 `decode_hci_le_meta_event` 解析事件内容：

```c
const le_meta_connless_iq_report_t *rpt =
  decode_hci_le_meta_event(packet, le_meta_connless_iq_report_t);
```

### 14.1.3 基于私有方式 #1 的 CTE 接收和发送 {#基于私有方式-1-的-cte-接收和发送}

这种方式最为灵活，需要配置的参数也最多，可参考 SDK *Ext. Raw Packet Tx/Rx*。

### 14.1.4 基于私有方式 #2 的 CTE 接收和发送 {#基于私有方式-2-的-cte-接收和发送}

这种方式的使用可参考 SDK *Central CTE* 和 *Peripehral LED & CTE*。

#### 14.1.4.1 发送方 {#发送方-2}

配置一个扩展广播集，属性设置为不可连接、不可扫描。待广播集使能后，调用 `ll_attach_cte_to_adv_set`[65](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn65) 为扩展广播附加 CTE。

#### 14.1.4.2 接收方 {#接收方-2}

启动扫描之后，调用 `ll_scanner_enable_iq_sampling`[66](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn66) 使能 CTE 采样。 之后，通过 `HCI_SUBEVENT_LE_VENDOR_PRO_CONNECTIONLESS_IQ_REPORT` 事件获得 CTE 报告。

## 14.2 加密与解密 {#加密与解密}

### 14.2.1 AES-128 加密 {#ch-misc-aes-encrypt}

通过 `gap_aes_encrypt` 进行 AES-128 加密：

```c
uint8_t gap_aes_encrypt(
  const uint8_t *key,           // 密钥（大端模式）
  const uint8_t *plaintext,     // 明文（大端模式）
  gap_hci_cmd_complete_cb_t cb, // 加密完成后的回调
  void *user_data);             // 回调函数的用户数据
```

以 [FIPS 197](https://www.nist.gov/publications/advanced-encryption-standard-aes) 里的数据为例：

```
PLAINTEXT: 00112233445566778899aabbccddeeff
KEY:       000102030405060708090a0b0c0d0e0f
CIPHERTEXT:69c4e0d86a7b0430d8cdb78070b4c55a
```

写成大端模式的数组形式：

```c
static const uint8_t plain_text[] =
    {0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
     0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};
static const uint8_t key[] =
    {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
     0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};
static const uint8_t cipher_text[] =
    {0x69, 0xc4, 0xe0, 0xd8, 0x6a, 0x7b, 0x04, 0x30,
     0xd8, 0xcd, 0xb7, 0x80, 0x70, 0xb4, 0xc5, 0x5a};
```

加密：

```c
gap_aes_encrypt(key, plain_text, aes_cb, NULL);
```

在回调函数 `aes_cb` 对比密文如下：

```c
void aes_cb(const uint8_t *return_param, const uint8_t *user_data)
{
    uint8_t reversed[16];
    reverse_bytes(return_param + 1, reversed, sizeof(reversed));
    printf("Matched: %d\n",
      memcmp(reversed, cipher_text, sizeof(cipher_text)) == 0);
}
```

这里 `return_param` 的内容与规范中相应 HCI 命令的 Return Parameters 一致。密文采用小端模式， 所以需要反转为大端模式，再与测试数据比较。

在上一次 AES 加密完成前，允许再次调用 `gap_aes_encrypt`。所有的加密任务保存在一个队列中，顺序完成。

也通过 `ll_aes_encrypt` 进行 AES-128 加密。 使用时务必检查返回值，若不为 0 表示硬件正忙。遇到此情况时可稍后重试。

```c
int ll_aes_encrypt(
  const uint8_t *key,       // 密钥（小端模式）
  const uint8_t *plaintext, // 明文（小端模式）
  uint8_t *ciphertext);     // 密文（大端模式）
```

`ll_aes_encrypt` 与 `gap_aes_encrypt` 的不同点：

- `ll_aes_encrypt` 以阻塞模式工作，不支持队列方式
- `ll_aes_encrypt` 可以更快完成加密
- 数据的大小端

### 14.2.2 AES-CCM {#aes-ccm}

CCM 是 Cipher Block Chaining-Message Authentication Code (CBC-MAC) 和 Counter 模式（CTR）的组合，同时对数据加密和生成认证信息。 通过 `gap_start_ccm` 启动 AES-CCM 计算[67](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn67)：

```c
uint8_t gap_start_ccm(
        uint8_t  type,        // 类型：0 为加密，1 为解密
        uint8_t  mic_size,    // MIC 长度（4 或 8 字节）
        uint16_t msg_len,     // 消息长度（最长 384 字节）
        uint16_t aad_len,     // AAD 长度（最长 16 字节，可为 0）
        uint32_t tag,         // 数据标签（任意值）
        const uint8_t *key,   // 密钥
        const uint8_t *nonce, // Nonce（长度 13 字节）
        const uint8_t *msg,   // 消息
        const uint8_t *aad,   // AAD
        uint8_t *out_msg,     // 加解密输出
        gap_hci_cmd_complete_cb_t cb, // 计算完成后的回调
        void *user_data);             // 回调函数的用户数据
```

AAD 为补充认证证数据（Additional Authenticated Data），可为数据提供额外的完整性保护。 这个函数使用了自定义的 HCI 消息 `HCI_VENDOR_CCM`。由于消息数据量大，这条消息仅传递指针， 因此所有的数据（`key`、`nonce`、`aad`、`msg`、`out_msg`）必须一直存在，直到计算完成方可释放。 加密时，输出到 `out_msg` 的数据长度为 (`msg_len` + `mic_size`)；解密时，`msg` 传入的数据长度为 (`msg_len` + `mic_size`)。

回调函数收到的 `return_param` 参数转换自 `event_vendor_ccm_complete_t *`。

例如：

```c
static const uint8_t plain_text[] =
    {0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
     0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};
static const uint8_t key[] =
    {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
     0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};

#define MSG_LEN     16
#define MIC_SIZE    4

static const uint8_t nonce[13] = {1};
static uint8_t ccm_enc_out[MSG_LEN + MIC_SIZE];
static uint8_t ccm_dec_out[MSG_LEN];
```

加密：

```c
gap_start_ccm(0, MIC_SIZE, MSG_LEN, 0, 0,
            key, nonce, plain_text, NULL,
            ccm_enc_out, ccm_enc_cb, NULL);;
```

在回调函数 `ccm_enc_cb` 里解密：

```c
void ccm_enc_cb(const uint8_t *return_param, const uint8_t *user_data)
{
  const event_vendor_ccm_complete_t *complete =
    (const event_vendor_ccm_complete_t *)return_param;
  gap_start_ccm(1, MIC_SIZE, MSG_LEN, 0, 0,
        key, nonce, ccm_enc_out, NULL,
        ccm_dec_out, ccm_dec_cb, NULL);
}
```

在回调函数 `ccm_dec_cb` 里检查 MIC 验证状态并比对数据：

```c
void ccm_dec_cb(const uint8_t *return_param, void *user_data)
{
  const event_vendor_ccm_complete_t *complete =
    (const event_vendor_ccm_complete_t *)return_param;
  printf("CCM DEC Status: %d\n", complete->status);
  printf("Matched: %d\n",
    memcmp(ccm_dec_out, plain_text, sizeof(plain_text)) == 0);
}
```

`event_vendor_ccm_complete_t` 的定义如下：

```c
typedef struct
{
    uint8_t  status;   // 状态码
    uint8_t  type;
    uint8_t  mic_size;
    uint16_t msg_len;
    uint16_t aad_len;
    uint32_t tag;
    uint8_t *out_msg;
} event_vendor_ccm_complete_t;
```

状态码在加密时，总是为 0；在解密时，0 表示 MIC 验证通过，非 0 表示失败。其它域与传入 `gap_start_ccm` 的参数一一对应、相等。

在上一次 AES-CCM 计算完成前，允许再次调用 `gap_start_ccm`。所有的计算任务保存在一个队列中，顺序完成。

## 14.3 协议栈配置 {#协议栈配置}

协议栈提供若干配置项，通过 `btstack_config` 配置：

```c
void btstack_config(
  // btstack_config_item 的比特组合
  uint32_t flags);
```

每个配置项对应一个比特位，可通过“或”运算同时使能多项配置。

```c
enum btstack_config_item {
    STACK_ATT_SERVER_ENABLE_AUTO_DATA_LEN_REQ = ...,
    STACK_GATT_CLIENT_DISABLE_AUTO_DATA_LEN_REQ = ...,
    STACK_DISABLE_L2CAP_TIMEOUT = ...,
    STACK_SM_USE_FIXED_CSRK = ...
    STACK_GATT_CLIENT_DISABLE_MTU_EXCHANGE = ...
    STACK_CONNECTION_UPDATE_PARAMETER_REPLY_USER = ...
    STACK_DEVICE_DATABASE_SUPPORT_MORE_DEVICES = ...
    ...
};
```

### 14.3.1 Data Length 与 MTU {#data-length-与-mtu}

低功耗蓝牙进入连接模式后，各层分别协商通信中数据包的大小，对于 ATT 层，由 MTU EXCHANGE 流程实现；对于链路层，由 DATA LENGTH 更新流程实现。

按照规范，进入连接模式后，DATA LENGTH 更新流程可以由主或从设备在任何时刻发起。这导致了一个问题：某些芯片无法处理对方设备“随时”发起的 DATA LENGTH 更新流程[68](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn68)。 为了更新地兼容不同的芯片，协议栈定义了两个配置项：

- `STACK_ATT_SERVER_ENABLE_AUTO_DATA_LEN_REQ`
- `STACK_GATT_CLIENT_DISABLE_AUTO_DATA_LEN_REQ`

这两个配置分别控制 GATT Server、Client 在 MTU EXCHANGE 时是否自动发起 DATA LENGTH 更新流程。默认情况下，Servier 不会自动发起更新流程， 而 Client 会自动发起。

### 14.3.2 面向测试 {#面向测试}

`STACK_DISABLE_L2CAP_TIMEOUT` 用于防止 L2CAP 超时，`STACK_SM_USE_FIXED_CSRK` 用来使用固定的 CSRK。

当 GATT 客户端实例创建时，会自动发起 MTU 协商。通过 `STACK_GATT_CLIENT_DISABLE_MTU_EXCHANGE` 可关闭该功能，MTU 保持初始默认值 `ATT_MTU`。

这些配置项用于 PTS 测试。

## 14.4 API 返回值 {#api-返回值}

绝大多数协议栈 API 都带有 `uint8_t` 型的返回值，0 为成功，非 0 为错误。开发者需要关注这些返回值。

几个例子：

- `att_server_notify` 的返回值：

  - 0：成功
  - `BTSTACK_LE_CHANNEL_NOT_EXIST` (`0x59`)：连接不存在（连接句柄参数错误？）
  - `BTSTACK_ACL_BUFFERS_FULL` (`0x57`)：内存已满
- `gap_set_ext_adv_para` 的返回值：

  - 0：成功
  - `BTSTACK_MEMORY_ALLOC_FAILED` (`0x56`)：内存已满

## 14.5 键值存储接口与实现 {#键值存储接口与实现}

### 14.5.1 键值存储接口 {#键值存储接口}

协议栈定义了一个简单的键值存储接口（*kv_storage*），其键（*key*） 为 `uint8_t`，值（*value*） 为长度不超过 `KV_VALUE_MAX_LEN` 的数组。 开发者可以在 App 里使用这个接口，*key* 的取值范围应该在 `KV_USER_KEY_START` 和 `KV_USER_KEY_END` 之间。 这个存储模块的增、删、改、查等功能如下。

- 增/改：`kv_put`

  ```c
  // 如果 key 不存在，为“增”；如果 key 存在，为“改”
  int kv_put(
    const kvkey_t key,
    // 值
    const uint8_t *data,
    // 值的长度
    int16_t len);
  ```
- 删：`kv_remove`

  ```c
  void kv_remove(
    // 键
    const kvkey_t key)
  ```
- 清空：`kv_remove_all`

  ```c
  void kv_remove_all(void);
  ```
- 查：`kv_get`

  ```c
  // 返回：指向值的指针
  uint8_t *kv_get(
    // 键
    const kvkey_t key,
    // 输出：值的长度
    int16_t *len);
  ```

  这个 API 返回的指针直接指向模块内值的存储空间，允许开发者在不改变值的长度的前提下修改其的内容。 修改之后需要调用 `kv_value_modified` 告知存储模块。
- 遍历：`kv_visit`

  ```c
  void kv_visit(
    // 访问者回调
    f_kv_visitor visitor,
    // 传递给回调的用户参数
    void *user_data);
  ```

  使用这个 API 可以遍历存储内所有的键值对。
- 数据已被修改

  ```c
  void kv_value_modified_of_key(
    // 键
    const kvkey_t key);
  ```

协议栈内实现了这个接口。开发者既可以使用内置的默认实现，也可以自定义实现。

### 14.5.2 默认的键值存储实现 {#默认的键值存储实现}

默认的键值存储实现的总储存大小为 1024 字节。这个实现本身没有数据持久化。 持久化需要开发者通过 `kv_init`[69](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn69) 提供回调来实现：

```c
void kv_init(
  // 用来保存数据的回调
  f_kv_write_to_nvm f_write,
  // 用来读取（恢复）数据的回调
  f_kv_read_from_nvm f_read);
```

当键值存储模块初始化时，会调用 `f_read` 恢复之前的数据状态；当存储里的数据更新后，键值存储模块会自动调用 `f_write` 回调。 考虑到 Flash 不宜频繁擦写，键值存储模块通过定时器超时来触发写入。每当数据更新时，复位定时器。

使用这种实现时需要注意以下几点：

1. 该模块查找一个 *key* 的时间复杂度为 \mathcal{O}(n)；
2. 该模块不是线程安全的。

### 14.5.3 自定义键值存储实现 {#自定义键值存储实现}

通过在 `app_main` 里调用 `kv_init_backend` 可以自定义键值存储实现：

```c
void kv_init_backend(
  const kv_backend_t *backend);
```

其中 `kv_backend_t` 包含以下回调接口：

```c
typedef struct kv_backend
{
    // 清空
    f_kv_remove_all kv_remove_all;
    // 删除
    f_kv_remove     kv_remove;
    // 增/改
    f_kv_put        kv_put;
    // 查
    f_kv_get        kv_get;
    // 遍历
    f_kv_visit      kv_visit;
    // 数据已被修改
    f_kv_value_modified_of_key kv_value_modified_of_key;
} kv_backend_t;
```

注意 `app_main` 里不能既调用 `kv_init` 又调用 `kv_init_backend`，会导致混乱。 当 `app_main` 里既没有调用 `kv_init` 也没有调用 `kv_init_backend` 时， 会使用默认的键值存储实现，且不支持数据持久化。

## 14.6 设备数据库 {#ch98-le-dev-db}

设备数据库模块（*le_device_db*）负责存储、管理设备的绑定信息。这个模块是基于键值存储模块实现的， 默认情况下，所能存储的设备个数等于 max(软件包所支持的连接数目, 10)[70](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn70)。 对于 SDK v8.5 及更新版本，使用 `STACK_DEVICE_DATABASE_SUPPORT_MORE_DEVICES` 配置项可以将个数提升为 (`KV_HOST_KEY_END` - `KV_HOST_KEY_START` + 1)。 删、查等接口如下。

- 查：`le_device_db_find`

  ```c
  le_device_memory_db_t *le_device_db_find(
    // 待查设备的地址类型
    const int addr_type,
    // 待查设备的地址
    const bd_addr_t addr,
    // 输出：在数据库里的序号
    int *index);
  ```
- 删

  直接按地址删除：

  ```c
  void le_device_db_remove(
    // 待删设备的地址类型
    const int addr_type,
    // 待删设备的地址
    const bd_addr_t addr);
  ```

  根据在数据库里的编号删除：

  ```c
  void le_device_db_remove_key(
    // 待删设备在数据库里的编号
    int index);
  ```
- 遍历

  这个模块支持迭代器遍历：

  ```c
  le_device_memory_db_iter_t iter;
  le_device_db_iter_init(&iter);
  while (le_device_db_iter_next(&iter))
  {
      le_device_memory_db_t *cur = le_device_db_iter_cur(&iter);
      // ...
  }
  ```

## 14.7 同步版 API {#ch-misc-synced-api}

SDK 提供的工具模块 *btstack_sync* 里包含几个 GAP、GATT 客户端同步版本的 API。 要使用这些 API 必须先初始化同步执行器。

- v8.2 及以上版本（基于 `btstack_push_user_runnable` 实现）

  如下创建同步执行器对象：

  ```c
  struct gatt_client_synced_runner *synced_runner =
      gatt_client_create_sync_runner(enable_gap_api);
  ```

  这里的 `enable_gap_api` 表示是否使能 GAP 同步版 API。
- v8.2 以下版本（基于 `btstack_push_user_msg` 实现）

  v8.2 以下版本的 *gatt_client_util* 模块仅提供 GATT 客户端同步版本 API， 未提供 GAP 同步版 API —— 开发者可参考 v8.2 自行添加。

  1. 基于 `btstack_push_user_msg` 实现一个消息传递函数，

     ```c
     // runner 为同步执行器
     // msg_id 为同步执行器内部的消息，从其数据类型可看出最多只有 256 种 ID，
     // 可以映射到 btstack_push_user_msg 的 uint32_t 型消息 ID 的一个子集里。
     void synced_push_user_msg(
         struct gatt_client_synced_runner *runner,
         uint8_t msg_id)
     {
         // 把同步执行器消息映射到 USER_MSG_SYNC_MSG_START 以上
         // App 可以使用的消息 ID 范围是 [0..USER_MSG_SYNC_MSG_START - 1]
         btstack_push_user_msg(USER_MSG_SYNC_MSG_START + msg_id,
             runner, 0);
     }
     ```
  2. 更新 `user_msg_handler` 把同步执行器内部的消息交给 `gatt_client_sync_handle_msg`

     ```c
     static void user_msg_handler(uint32_t msg_id, void *data,
         uint16_t size)
     {
         switch (msg_id)
         {
         //...
         default:
             if (msg_id >= USER_MSG_SYNC_MSG_START)
             {
                 struct gatt_client_synced_runner *runner =
                     (struct gatt_client_synced_runner *)data;
                 gatt_client_sync_handle_msg(runner,
                     msg_id - USER_MSG_SYNC_MSG_START);
             }
         }
     }
     ```
  3. 创建同步执行器对象

     ```c
     struct gatt_client_synced_runner *synced_runner =
         gatt_client_create_sync_runner(synced_push_user_msg);
     ```

注意：对于一个连接，最多只能存在一个与之关联的同步执行器。最简单的用法是在初始化时创建唯一一个同步执行器对象[71](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn71)。创建多个同步执行器时，最多只能有一个使能了 GAP 同步版 API。

上述准备工作做完，就可以使用同步 API 了。下面这个函数 —— 称为一个同步执行体 —— 使用同步 API 多次读取某个特征的值并打印：

```c
// 用 user_data 表示 value_handle
static void demo_synced_api(
    struct gatt_client_synced_runner *synced_runner,
    void *user_data)
{
    uint16_t handle = (uint16_t)(uintptr_t)user_data;
    static uint8_t data[255];
    int n = 5;
    printf("synced read value for %d times:\n", n);

    for (; n > 0; n--)
    {
        uint16_t length = sizeof(data);
        // 注意：这个函数返回后，数据就读取完成了
        int err = gatt_client_sync_read_value_of_characteristic(
                synced_runner, mas_conn_handle, handle,
                data, &length);
        printf("[%d]: err = %d:\n", n, err);
        if (err) break;
        // print_value(data, length);
        printf("wait for 200ms...\n", n, err);
        vTaskDelay(pdMS_TO_TICKS(200));
    }
    printf("done\n\n");
}
```

这种同步执行体不能直接使用，而要交给同步执行器去执行：

```c
gatt_client_sync_run(synced_runner, demo_synced_api,
    (void *)(uintptr_t)value_handle);
```

这里，`demo_synced_api` 函数运行于同步执行器内的线程。`gatt_client_sync_run` 可以从任意线程调用。

### 14.7.1 GAP 同步 API {#gap-同步-api}

- `gap_sync_ext_create_connection`：建立连接

  ```c
  int gap_sync_ext_create_connection(
      struct btstack_synced_runner *runner,
      const initiating_filter_policy_t filter_policy,
      const bd_addr_type_t own_addr_type,
      const bd_addr_type_t peer_addr_type,
      const uint8_t *peer_addr,
      const uint8_t initiating_phy_num,
      const initiating_phy_config_t *phy_configs,
      uint32_t timeout_ms,
      le_meta_event_enh_create_conn_complete_t *complete);
  ```

  与 `gap_ext_create_connection` 相比，这个函数是“阻塞”的：函数直到连接成功或者超时才返回。 如果调用 `gap_create_connection` 时出错，则 `gap_ext_create_connection` 会返回其错误码； 其它情况下返回的值即 `le_meta_event_enh_create_conn_complete_t` 里的 `status` 字段。 也就是说，连接建立成功时返回值为 0 时，超时时返回值为 0x02[72](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn72) (未知的连接句柄)。

  `complete` 参数为输出，保存了`HCI_SUBEVENT_LE_ENHANCED_CONNECTION_COMPLETE` 事件的数据。 同使用 `gap_ext_create_connection` 一样，已有的 HCI 事件回调函数也会收到 这个 `HCI_SUBEVENT_LE_ENHANCED_CONNECTION_COMPLETE` 事件。
- `gap_sync_le_read_channel_map`：读取某连接所使用的信道集合

  函数原型如下：

  ```c
  int gap_sync_le_read_channel_map(
    struct btstack_synced_runner *runner,
    // 连接句柄
    hci_con_handle_t con_handle,
    // 用前 37 个比特表示的信道集合
    uint8_t channel_map[5]);
  ```
- `gap_sync_read_rssi`：读取某连接的 RSSI

  函数原型如下：

  ```c
  int gap_sync_read_rssi(
    struct btstack_synced_runner *runner,
    // 连接句柄
    hci_con_handle_t con_handle,
    // RSSI 输出
    int8_t *rssi);
  ```
- `gap_sync_read_phy`：读取某连接的 PHY

  函数原型如下：

  ```c
  gap_sync_read_phy(
    struct btstack_synced_runner *runner,
    // 连接句柄
    hci_con_handle_t con_handle,
    // 本设备发送方向使用的 PHY
    phy_type_t *tx_phy,
    // 本设备接收方向使用的 PHY
    phy_type_t *rx_phy);
  ```
- `gap_sync_read_remote_version`：读取某连接对端设备的版本

  函数原型如下：

  ```c
  int gap_sync_read_remote_version(
    struct btstack_synced_runner *runner,
    // 连接句柄
    hci_con_handle_t con_handle,
    // 蓝牙链路层协议版本编号
    uint8_t *version,
    // 厂家编号
    uint16_t *manufacturer_name,
    // Controller 版本号
    uint16_t *subversion);
  ```

  蓝牙链路层协议版本号由 Bluethooth SIG 指定，部分编号与版本号的对应关系如表 [3.5](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#tab:ch-overview-ble-version) 所示； 厂家编号由厂家申请、Bluethooth SIG 指定[73](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn73)； Controller 版本号由 Controller 厂家自行指定。
- `gap_sync_read_remote_used_features`：读取某连接对端设备使用的蓝牙特性

  函数原型如下：

  ```c
  int gap_sync_read_remote_used_features(
    struct btstack_synced_runner *runner,
    // 连接句柄
    hci_con_handle_t con_handle,
    // 蓝牙特性比特图
    uint8_t features[8]);
  ```

  蓝牙特性的定义参见表 [3.4](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#tab:ch-overview-ble-features)。

### 14.7.2 GATT 客户端同步 API {#gatt-客户端同步-api}

本模块提供了以下同步 API，其原型与异步版本基本类似：

- `gatt_client_sync_discover_all`：同步发现所有服务
- `gatt_client_sync_read_value_of_characteristic`：同步读取特征的值
- `gatt_client_sync_read_characteristic_descriptor`：同步读取特征描述符
- `gatt_client_sync_write_value_of_characteristic`：同步有响应地写入特征的值
- `gatt_client_sync_write_value_of_characteristic_without_response`：同步无响应地写入特征的值[74](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn74)
- `gatt_client_sync_write_characteristic_descriptor`：同步写入特征描述符

## 14.8 线程安全的 API {#ch-misc-thread-safe-api}

SDK 提供的工具模块 *btstack_mt* 借助 `btstack_push_user_runnable` 为 Host 常用 API 重新封装了一套线程安全的 API。 每个 API 与原始 API 参数完全一致，得到的返回值也相同，只是函数名称增加了表示多线程的 `mt_` 前辍。

每个 `mt_foo` 函数都有一个 `f_btstack_user_runnable` 类型的辅助函数 `foo_0`，调用背后的 `foo` 所需要的参数及保存返回值的变量等都通过第一个参数 `ctx` 传入，伪代码如下：

```c
static void foo_0(*ctx, uint16_t _)
{
  ctx->_ret = foo(ctx->param);
  event_set(ctx->_event);
}
```

`mt_foo` 的伪代码如下：

```c
type mt_foo(param)
{
  if (in Host task)
    return foo(param);
  ctx->param = param;
  ctx->_event = event_create();
  btstack_push_user_runnable(foo_0, &ctx, 0);
  event_wait(ctx->_event);
  event_free(ctx->_event);
  return ctx->_ret;
}
```

由于通用 OS 接口未提供释放的接口，所以这个模块实现了一个事件对象池以模拟事件的释放（伪代码里的 `event_free`）。

用上述“阻塞”方式实现的线程安全 API，既可以获取实际的返回值，也可以避免复制内存数据。 允许这样的用法：

```c
void do_some_thing()
{
  uint8_t data[10];
  向 data 写入数据;
  mt_att_server_notify(con_handle,
    att_handle, data, sizeof(data));
}

void any_thread()
{
  do_some_thing();
  // 此时 do_some_thing 里的 data 已被释放
}
```

注意事项：

- 这个模块依赖于一个真正的 RTOS。使用 NoOS 软件包时，必需提供真正的队列及事件支持。
- 封装必然存在开销。对于高性能、高实时性的应用，不推荐使用。反之，对于相对简单的应用，则推荐使用，可以简化代码；
- 不要在中断服务程序内使用这些 API[75](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn75)。

## 14.9 链路层隐私 {#ch-misc-privacy}

下面以充分保护隐私为出发点说明链路层隐私特性的使用方法。

### 14.9.1 将已配对设备添加到解析列表 {#将已配对设备添加到解析列表}

同白名单类似，地址解析列表也完全由开发者管理。下面的代码演示了如何将设备数据库里的信息添加到解析列表和白名单。

```c
static void populate_pairing_data(const uint8_t *local_irk)
{
    gap_clear_resolving_list();
    gap_clear_white_lists();

    le_device_memory_db_iter_t device_db_iter;
    le_device_db_iter_init(&device_db_iter);
    while (le_device_db_iter_next(&device_db_iter))
    {
        const le_device_memory_db_t *dev =
            le_device_db_iter_cur(&device_db_iter);
        gap_add_dev_to_resolving_list(dev->addr,
            dev->addr_type, dev->irk, local_irk);
        gap_add_whitelist(dev->addr, dev->addr_type);
    }
}
```

上面的演示代码假定对于所有的配对设备，本端使用的 IRK 相同。与不同的设备配对时，本端使用不同的 IRK 也是可以的。

### 14.9.2 广播 {#广播}

#### 14.9.2.1 未配对时 {#未配对时}

当设备未配对或者期望被新的设备连接时，可事先生成不可解析随机地址或用 IRK 生成可解析地址，将其配置为广播集的随机地址，并使用这个随机地址发送广播， 即：

```c
gap_set_adv_set_random_addr(..., 生成的地址);
gap_set_ext_adv_para(
  ...
  BD_ADDR_TYPE_LE_RANDOM, // own_addr_type
  ...);
```

#### 14.9.2.2 已配对时 {#已配对时}

当设备已与唯一的对端设备配对，发送广播等待与其建立连接时，将对端设备的身份地址填入 `gap_set_ext_adv_para` 的 `peer_addr` 参数， Controller 从解析列表中查到对应的本端 IRK，使用与之对应的可解析地址（如地址不存在，会自动生成）发送广播：

```c
gap_set_ext_adv_para(
  ...
  BD_ADDR_TYPE_LE_RESOLVED_RAN, // own_addr_type
  peer_addr_type,               // peer_addr_type
  peer_addr,                    // peer_addr
  ADV_FILTER_ALLOW_SCAN_WLST_CON_WLST, // adv_filter_policy
  ...);
```

当设备已与多个对端设备配对，发送广播等待与任意对端建立连接时，分为两种情况：

1. 使用了相同的本端 IRK

   由于使用任意对端的身份地址都会检索到这个 IRK，所以可以任意选择一个对端设备的身份地址填入 `gap_set_ext_adv_para` 的 `peer_addr` 参数，代码同上。
2. 使用了各不相同的本端 IRK

   可以轮流使用每个对端设备身份地址，填入 `gap_set_ext_adv_para` 的 `peer_addr` 参数，发送广播并等待一段时间，如无连接则切换到下一个设备。 或者用多个对端设备身份地址同时配置多个广播集。

如果地址解析成功，`HCI_SUBEVENT_LE_ENHANCED_CONNECTION_COMPLETE_..` 事件里的 `peer_addr_type` 将会是 `BD_ADDR_TYPE_LE_RESOLVED_RAN` 或者 `BD_ADDR_TYPE_LE_RESOLVED_PUB`， `peer_addr` 是解析出的对端的身份地址。`HCI_SUBEVENT_LE_SCAN_REQUEST_RECEIVED` 事件里的 `scanner_addr_type` 将会是 `BD_ADDR_TYPE_LE_RESOLVED_RAN` 或者 `BD_ADDR_TYPE_LE_RESOLVED_PUB`， `scanner_addr` 是解析出的扫描者的身份地址。

### 14.9.3 扫描 {#扫描}

可以生成不同于身份地址（如不可解析随机地址或用 IRK 生成可解析地址）的随机地址，并调用 `gap_set_random_device_address`。

如果需要扫描周围全部设备的广播信息，可如下配置扫描参数：

```c
gap_set_ext_scan_para(
  BD_ADDR_TYPE_LE_RANDOM,               // own_addr_type
  SCAN_ACCEPT_ALL_EXCEPT_NOT_DIRECTED,  // filter_policy
  ...);
```

如果只扫描白名单内设备的广播信息，可如下配置扫描参数：

```c
gap_set_ext_scan_para(
  BD_ADDR_TYPE_LE_RANDOM,                // own_addr_type
  SCAN_ACCEPT_WLIST_EXCEPT_NOT_DIRECTED, // filter_policy
  ...);
```

此时，Controller 扫描到某设备的广播时，尝试解析地址。对于主动扫描，如果解析成功且通过了白名单， 就使用对应于本端 IRK 的可解析地址发送扫描请求。

如果地址解析成功，`HCI_SUBEVENT_LE_EXTENDED_ADVERTISING_REPORT` 事件里的 `addr_type` 将会是 `BD_ADDR_TYPE_LE_RESOLVED_RAN` 或者 `BD_ADDR_TYPE_LE_RESOLVED_PUB`， `address` 是解析出的广播者身份地址。

### 14.9.4 建立连接 {#建立连接}

事先生成不可解析随机地址或用 IRK 生成可解析地址，并调用 `gap_set_random_device_address`。

#### 14.9.4.1 未配对时 {#未配对时-1}

如果需要连接一个未配对的设备，可如下配置：

```c
gap_ext_create_connection(
  INITIATING_ADVERTISER_FROM_PARAM,   // filter_policy
  BD_ADDR_TYPE_LE_RANDOM,             // own_addr_type
  peer_addr_type, // peer_addr_type
  peer_addr,      // peer_addr
  ...);
```

#### 14.9.4.2 已配对时 {#已配对时-1}

如果需要连接单一的确定的已配对设备，可如下配置：

```c
gap_ext_create_connection(
  INITIATING_ADVERTISER_FROM_PARAM,   // filter_policy
  BD_ADDR_TYPE_LE_RESOLVED_RAN,       // own_addr_type
  peer_addr_type, // peer_addr_type
  peer_addr,      // peer_addr
  ...);
```

如果需要连接白名单内的任一已知设备，可如下配置：

```c
gap_ext_create_connection(
  INITIATING_ADVERTISER_FROM_LIST,   // filter_policy
  BD_ADDR_TYPE_LE_RESOLVED_RAN,      // own_addr_type
  ...);
```

如果地址解析成功，`HCI_SUBEVENT_LE_ENHANCED_CONNECTION_COMPLETE_..` 事件里的 `peer_addr_type` 将会是 `BD_ADDR_TYPE_LE_RESOLVED_RAN` 或者 `BD_ADDR_TYPE_LE_RESOLVED_PUB`， `peer_addr` 是解析出的对端的身份地址。

## 14.10 干预连接参数请求流程 {#干预连接参数请求流程}

当双方支持时，主、从都可以发起连接参数请求流程。Host 默认会接收对方发送的任意连接参数请求。开发者可以通过多种方式干预流程。

- 指定连接参数范围

  通过 `gap_set_connection_parameter_range` 可以指定所能接收的参数范围。Host 自动完成流程。
- 拒绝所有连接参数请求

  通过 `gap_set_connection_parameter_range` 设置一组特殊无效参数，Host 将拒绝所有连接参数请求。无效参数是指：

  - `le_conn_interval_min` 为 `0xffff`；
  - 其它参数为 `0`。
- 由 App 完成流程

  使用 `STACK_CONNECTION_UPDATE_PARAMETER_REPLY_USER` 配置项可将连接参数请求交由 App 处理。这时 App 可以响应 `HCI_SUBEVENT_LE_REMOTE_CONNECTION_PARAMETER_REQUEST` 事件，并通过 `gap_connection_parameter_update_reply` 或者 `gap_connection_parameter_update_negative_reply` 作出响应。

---

1. <a id="fn64"></a>参考《Application Note: Direction Finding Solution》。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref64)
2. <a id="fn65"></a>参考《Controller API Reference》。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref65)
3. <a id="fn66"></a>参考《Controller API Reference》。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref66)
4. <a id="fn67"></a>为防止与 Media Access Controller 混淆，蓝牙规范使用 MIC 代替 MAC。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref67)
5. <a id="fn68"></a>[https://ingchips.github.io/blog/2021-06-02-sdk-6/#%E5%85%BC%E5%AE%B9%E6%80%A7](https://ingchips.github.io/blog/2021-06-02-sdk-6/#%E5%85%BC%E5%AE%B9%E6%80%A7)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref68)
6. <a id="fn69"></a>只能在 `app_main` 就调用。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref69)
7. <a id="fn70"></a>对于 v8.4.12 或更旧的版本，所能存储的设备个数等于软件包所支持的连接数目。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref70)
8. <a id="fn71"></a>为多个连接创建多个同步执行器的优势在于多个 GATT 客户端上的会话可以并发。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref71)
9. <a id="fn72"></a>由规范规定。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref72)
10. <a id="fn73"></a>[https://www.bluetooth.com/specifications/assigned-numbers/](https://www.bluetooth.com/specifications/assigned-numbers/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref73)
11. <a id="fn74"></a>这个函数的原始版本不是严格意义上的异步操作。考虑到在一个同步执行体内可能既会用到有响应的写入，也会用到无响应的写入，加入这个 API 可以带来便利。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref74)
12. <a id="fn75"></a>可以使用 `btstack_push_user_runnable`。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref75)