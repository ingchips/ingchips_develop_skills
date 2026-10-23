<!-- pg_ble_stack_cn: 8 GATT - 服务器 -->

# 8 GATT - 服务器 {#ch-gatt-server}

## 8.1 概览 {#ch-gatt-server-overview}

GATT 服务器[33](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn33)为客户端提供服务。 协议栈支持多个连接，每个连接的配置（Profile）可以独立设置。 需要注意，GATT 服务器和客户端这两个角色与主、从两个角色没有任何关联：一个连接的主角色既可以充当 GATT 的客户端，也可以充当服务器， 还可以两种角色一起扮演；一个连接的从角色也是如此。

要使用 GATT 服务器，开发者需要做三件事[34](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn34)：

1. 初试化：设置事件回调

   ```c
   void att_server_register_packet_handler(
     btstack_packet_handler_t handler);
   ```
2. 初始化：提供回调函数

   ```c
   void att_server_init(
     // 特征的读回调
     att_read_callback_t read_callback,
     // 特征的写回调
     att_write_callback_t write_callback);
   ```

   读回调的类型如下：

   ```c
   typedef uint16_t (*att_read_callback_t)(
     // 连接句柄
     hci_con_handle_t con_handle,
     // 特征句柄
     uint16_t attribute_handle,
     // 数据偏移
     uint16_t offset,
     // 缓存
     uint8_t *buffer,
     // 缓存的大小
     uint16_t buffer_size);
   ```

   写回调的类型如下：

   ```c
   typedef int (*att_write_callback_t)(
     // 连接句柄
     hci_con_handle_t con_handle,
     // 特征句柄
     uint16_t attribute_handle,
     // 会话模式
     uint16_t transaction_mode,
     // 数据偏移
     uint16_t offset,
     // 缓存
     const uint8_t *buffer,
     // 缓存的大小
     uint16_t buffer_size);
   ```

   将 `con_handle` 和 `attribute_handle` 组合到一起，回调函数就可以确定是在访问哪个 Profile 里的哪个特征。 对于长度超过(ATT\_MTU - 3)的长值，BLE 支持分块读写模式，相应地，两个回调函数都有一个 `offset` 参数。

   关于会话模式 `transaction_mode` 的说明见后文。
3. 适时提供 Profile 数据

   ```c
   void att_set_db(
     // 要关联的句柄
     hci_con_handle_t con_handle,
     // Profile 数据库
     const uint8_t *db);
   ```

协议栈内的 GATT 服务器可以通过 2 种方式获得特征的值，然后传输到客户端：

1. 保存在 Profile 数据库内部的值

   这种方式适用于值不改变的情况，服务器可能自动将值传输到客户端，不需要开发者参与。
2. 借助回调函数 `att_read_callback_t`

   这种方式适用于值动态改变的情况。 每当客户端读取值时，协议栈会立即调用回调函数，且 `buffer` 为 `NULL`。 这一次调用是为了获取数值长度。回调函数的处理流程又可以分为两种情况：

   - 如果 App 可以立即准备好数据，那么直接返回数值的**总长**；

     之后，协议栈准备内存空间并立即再次调用函数，此时 `buffer` 参数非 `NULL`， 回调函数将数据写入 `buffer` 所指向的内存，读取完成；
   - 如果 App 无法立即准备好数据，那么返回 `ATT_DEFERRED_READ` 进入延迟读取模式；

     待数据就绪之后，App 调用 `att_server_deferred_read_response` 将数据传给协议栈，读取完成。

每个特性具有若干属性，见表 [8.1](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#tab:ch3-char-properties)。

*表 8.1: 特征的属性*
| 属性 | 说明 |
| --- | --- |
| ATT_PROPERTY_BROADCAST | 允许广播该特性的值 |
| ATT_PROPERTY_READ | 允许读取 |
| ATT_PROPERTY_WRITE_WITHOUT_RESPONSE | 允许无响应写入 |
| ATT_PROPERTY_WRITE | 允许（有响应的）写入 |
| ATT_PROPERTY_NOTIFY | 允许通知（Notification） |
| ATT_PROPERTY_INDICATE | 允许指示（Indication） |
| ATT_PROPERTY_AUTHENTICATED_SIGNED_WRITE | 允许带签名的写入 |
| ATT_PROPERTY_EXTENDED_PROPERTIES | 支持扩展属性 |
| ATT_PROPERTY_DYNAMIC | 为动态特性（即需要使用回调函数） |

其中 `DYNAMIC` 为协议栈自定义的属性，只有加上了这个属性，对特性的读写操作才会交由回调函数处理。对于支持写入的特征， 由于总是需要通过回调函数处理，必须加上此属性。

对于支持通知（Notification）和/或指示（Indication）的特征，必须带有 Client Characteristic Configuration 描述符（常被简称为 CCCD）：

- 将 `GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NOTIFICATION` 写入 CCCD 就可以使能通知，
- 将 `GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_INDICATION` 写入 CCCD 就可以使能指示，
- 将 `GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NONE` 写入 CCCD 就可以关闭通知和指示。

通知相当于无响应的上报，而指示相当于有响应的上报。

## 8.2 使用说明 {#使用说明-3}

### 8.2.1 Profile 数据 {#profile-数据}

Profile 数据[35](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn35) 使用了协议栈自定义的数据结构。 开发者不需要了解这个数据结构的定义，而是借助图形化工具或者编程地生成。

1. 使用图形化的 Profile 编辑器。

   请参考 《SDK 用户手册》。
2. 使用 `att_db_util` 模块。

   调用 `att_db_util_init` 告知 Profile 数据的存储空间。 调用 `att_db_util_add_service_uuid??` 添加服务，然后通过 `att_db_util_add_characteristic_uuid??` 添加若干特性。 重复上述步骤可以添加多个服务。最后调用 `att_db_util_get_size` 查看整个 Profile 数据的大小，相应调整存储空间的大小，再重新编译程序。

   上面的 `....._uuid??` 函数都包含 `uuid16` 和 `uuid128` 等两种形式，分别对应 16-bit 的简短 UUID 和 16 字节的完整 UUID。

   `att_db_util_add_characteristic_uuid??` 函数返回的是特性的值的句柄。 调用 `att_db_util_add_characteristic_uuid??` 时需要注意根据情况添加 `ATT_PROPERTY_DYNAMIC` 属性。 对于带有 `ATT_PROPERTY_NOTIFY` 和/或 `ATT_PROPERTY_INDICATE` 属性的特性，`att_db_util_add_characteristic_uuid??` 函数会自动添加 CCCD。 设特性的值句柄为 N，那么 CCCD 的句柄为 N + 1。

### 8.2.2 实现读回调 {#实现读回调}

一个典型的读回调函数大概是这种样子：

```c
static uint16_t att_read_callback(hci_con_handle_t connection_handle,
  uint16_t att_handle, uint16_t offset,
  uint8_t * buffer, uint16_t buffer_size)
{
    switch (att_handle)
    {
    case HANDLE_0:
        if (buffer)
        {
            memcpy(buffer, ...)
            return buffer_size;
        }
        else
            return size of value;
    //...
    default:
        return 0;
    }
}
```

延迟读取的情况：

```c
static uint16_t att_read_callback(hci_con_handle_t connection_handle,
  uint16_t att_handle, uint16_t offset,
  uint8_t * buffer, uint16_t buffer_size)
{
    switch (att_handle)
    {
    case HANDLE_0:
        //...
        return ATT_DEFERRED_READ;
    //...
    default:
        return 0;
    }
}
```

延迟读取的数据通过 `att_server_deferred_read_response` 传递给协议栈：

```c
int att_server_deferred_read_response(
  // 连接句柄
  hci_con_handle_t con_handle,
  // 特征句柄
  uint16_t attribute_handle,
  // 指向值的指针
  const uint8_t *value,
  // 值的长度
  uint16_t value_len);
```

SDK *GATT Relay* 演示了延迟读取的具体用法。

### 8.2.3 实现写回调 {#实现写回调}

当写特性时，可能触发服务器执行某个动作。BLE 为了精度控制动作的执行引入了会话[36](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn36)概念： 一个会话包含对 1 个或多个特性的写入，最后是一个显式的“执行”命令通知服务器开始执行。此外还有一个“取消”命令，通知服务器会话不要执行动作、直接终止。相应地， 写回调的会话模式 `transaction_mode` 参数包含四种值：

```c
// 无会话的普通写入
#define ATT_TRANSACTION_MODE_NONE      ...
// 带会话的写入
#define ATT_TRANSACTION_MODE_ACTIVE    ...
// 执行
#define ATT_TRANSACTION_MODE_EXECUTE   ...
// 取消
#define ATT_TRANSACTION_MODE_CANCEL    ...
```

对于 `NONE` 和 `ACTIVE` 两种模式，都会传入要写入的数据，而 `EXECUTE` 和 `CANCEL` 则既不会传入特征句柄，也不传入数据， 也就是说这两个命令只关联到连接，施加于整个服务器，而不针对某个特征。

一个典型的写回调函数大概是这种样子：

```c
static int att_write_callback(
  hci_con_handle_t connection_handle, uint16_t att_handle,
  uint16_t transaction_mode,
  uint16_t offset, const uint8_t *buffer, uint16_t buffer_size)
{
    处理 EXECUTE 和 CANCEL 两种会话模式并返回;

    //
    switch (att_handle)
    {
    case HANDLE_0:
        //...
        return 0;
    //...
    default:
        return 0;
    }
}
```

如果发现错误，可以返回非 0 值告知客户端[37](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn37)。

### 8.2.4 发送通知（Notification） {#发送通知notification}

通过 `att_server_notify` 发送通知：

```c
int att_server_notify(
  // 连接句柄
  hci_con_handle_t con_handle,
  // 特征句柄
  uint16_t attribute_handle,
  // 指向值的指针
  const uint8_t *value,
  // 值的长度
  uint16_t value_len);
```

该函数返回的状态代码及含义如下：

- 0：数据正常进入发送队列；
- `BTSTACK_LE_CHANNEL_NOT_EXIST` (`0x59`)：参数 `con_handle` 指定的连接不存在；
- `BTSTACK_ACL_BUFFERS_FULL` (`0x57`)：内部缓存已满，数据未进入发送队列[38](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn38)。

### 8.2.5 发送指示（Indication） {#发送指示indication}

通过 `att_server_indicate` 发送指示：

```c
int att_server_indicate(
  // 连接句柄
  hci_con_handle_t con_handle,
  // 特征句柄
  uint16_t attribute_handle,
  // 指向值的指针
  const uint8_t *value,
  // 值的长度
  uint16_t value_len);
```

指示的响应通过 `ATT_EVENT_HANDLE_VALUE_INDICATION_COMPLETE` 事件通知 App，事件里的状态码的定义见 [ATT 错误码](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#ch0-att-err-codes)。

该函数返回的状态代码及含义如下：

- 0：数据正常进入发送队列；
- `BTSTACK_LE_CHANNEL_NOT_EXIST` (`0x59`)：参数 `con_handle` 指定的连接不存在；
- `BTSTACK_ACL_BUFFERS_FULL` (`0x57`)：内部缓存已满，数据未进入发送队列[39](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn39)；
- `ATT_HANDLE_VALUE_INDICATION_IN_PROGRESS` (`0x90`)：在收到 `ATT_EVENT_HANDLE_VALUE_INDICATION_COMPLETE` 事件前， 不能发送新的指示，否则 `att_server_indicate` 将返回此错误码。

### 8.2.6 响应事件 {#响应事件}

GATT 服务器模块会弹出以下事件。

- `ATT_EVENT_MTU_EXCHANGE_COMPLETE`

  这个事件表示 MTU 协商完成。有两个解析函数：

  - `att_event_mtu_exchange_complete_get_handle(packet)` 获得连接句柄；
  - `att_event_mtu_exchange_complete_get_MTU(packet)` 获得 MTU 大小。
- `ATT_EVENT_HANDLE_VALUE_INDICATION_COMPLETE`

  这个事件表示指示发送完成。有三个解析函数：

  - `att_event_handle_value_indication_complete_get_conn_handle(packet)` 获得连接句柄；
  - `att_event_handle_value_indication_complete_get_attribute_handle(packet)` 获得特征句柄；
  - `att_event_handle_value_indication_complete_get_status(packet)` 获得响应状态。

    共有两种状态：0 表示成功送达，`ATT_HANDLE_VALUE_INDICATION_TIMEOUT` (`0x91`) 表示超时。

### 8.2.7 ATT_MTU {#att_mtu}

除了通过监听 `ATT_EVENT_MTU_EXCHANGE_COMPLETE` 事件以外，通过 `att_server_get_mtu` 可以随时获取 ATT_MTU：

```c
uint16_t att_server_get_mtu(
  // 连接句柄
  hci_con_handle_t con_handle);
```

特征的值的最大长度为 (ATT\_MTU - 3)。调用 `att_server_indicate` 或 `att_server_notify` 上报数据时， 如果超过最大长度，会被自动截短。

---

1. <a id="fn33"></a>在不引起混淆的前提下，本手册混用 ATT 服务器、GATT 服务器，代码里也用 `att_server` 代指 `gatt_server`。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref33)
2. <a id="fn34"></a>事实上，这几件事已由 Wizard 工具代劳。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref34)
3. <a id="fn35"></a>在手册、工具、代码的不同位置可能使用了不同的名词，如 Profile 数据库、GATT 数据库、GATT 数据等。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref35)
4. <a id="fn36"></a>协议栈里称为“会话”，规范里称为“队列”。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref36)
5. <a id="fn37"></a>仅适用于有响应的写入，无响应的写入无效。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref37)
6. <a id="fn38"></a>解决方法参考 [L2CAP 传输队列](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#ch-i2cap-tx-queue)。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref38)
7. <a id="fn39"></a>解决方法参考 [L2CAP 传输队列](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#ch-i2cap-tx-queue)。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref39)