<!-- pg_ble_stack_cn: 9 GATT - 客户端 -->

# 9 GATT - 客户端 {#ch-gatt-client}

## 9.1 概览 {#概览-3}

GATT 客户端的主要功能是发现服务，读写和订阅特征。每个连接使用独立的 GATT 客户端实例。

GATT 客户端的操作几乎都需要先发出数据再等待服务器发回响应，需要较长的时间，所以也引入了会话的概念： 如果上一个会话未结束，那么就不允许发起新的会话。每次发起会话时，都要提供一个专门的回调函数。 当这个回调函数收到 `GATT_EVENT_QUERY_COMPLETE` 事件时，会话结束。

使用 GATT 客户端 API 时需要注意检查返回值，常见的返回值有：

- 0：正常、成功；
- `BTSTACK_MEMORY_ALLOC_FAILED` (`0x56`)：内存不足，无法创建 GATT 客户端实例
- `GATT_CLIENT_IN_WRONG_STATE` (`0x95`)：会话冲突

  解决方法：等待上一个会话完成后再发起新的会话。通过 `gatt_client_is_ready` 可以查询当前是否可以发起新的会话。
- `GATT_CLIENT_VALUE_TOO_LONG` (`0x97`)：要写入的值超出 MTU 的限制

  解决方法：缩短值的长度；或者检查对比设备的 MTU 能力。
- `BTSTACK_ACL_BUFFERS_FULL` (`0x57`)：内部缓存已满，数据未进入发送队列

  解决方法：参考 [L2CAP 传输队列](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#ch-i2cap-tx-queue)。

可选地，开发者可以设置 GATT 客户端事件回调：

```c
void gatt_client_register_handler(
  btstack_packet_handler_t handler);
```

这个回调函数会收到以下事件[40](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn40)：

- `GATT_EVENT_MTU`

  这个事件表示 MTU 协商完成。有两个解析函数：

  - `gatt_event_mtu_get_handle(packet)`

    获得连接句柄；
  - `gatt_event_mtu_get_mtu(packet)`

    获得 MTU 大小。
- `GATT_EVENT_UNHANDLED_SERVER_VALUE` [41](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn41)

  这个事件表示收到了服务器某特性的值上报，但是相关句柄未通过 `gatt_client_listen_for_characteristic_value_updates` 注册回调函数。

  - `gatt_event_unhandled_server_value_get_type(packet)`

    获得上报类型，即 `GATT_EVENT_NOTIFICATION` 或 `GATT_EVENT_INDICATION`；
  - `gatt_event_unhandled_server_value_get_value_handle(packet)`

    获得特征的句柄；
  - `gatt_event_unhandled_server_value_get_size(packet)`

    获得上报的值的长度；
  - `gatt_event_unhandled_server_value_get_data(packet)`

    获得指向上报的值的指针。

### 9.1.1 句柄范围 {#句柄范围}

特征包含值和若干个描述符，每个描述符也对应于一个句柄，所以一个特征包含从 `start_handle` 到 `end_handle` 的一系列句柄。 同理，服务也对应一个句柄范围。

本章在不引起误解的前提下，把特征的值的句柄简称为“特征的句柄”。

## 9.2 使用说明 {#使用说明-4}

### 9.2.1 创建客户端 {#创建客户端}

调用 GATT 客户端的绝大多数带有连接句柄参数的 API 时，都会按需自动创建客户端实例。带有连接句柄参数但不会触发创建动作的 API：

- `gatt_client_listen_for_characteristic_value_updates`

通过 `gatt_client_is_ready()` 可显式地“手动”创建客户端实例。

### 9.2.2 发现服务 {#发现服务}

下列 API 用来发现服务：

- `gatt_client_discover_primary_services`：发现所有服务。
- `gatt_client_discover_primary_services_by_uuid16`：发现指定的服务。
- `gatt_client_discover_primary_services_by_uuid128`：发现指定的服务。

下列 API 用来发现服务内部的特征：

- `gatt_client_discover_characteristics_for_service`：发现一个服务里的所有特征
- `gatt_client_discover_characteristics_for_handle_range_by_uuid16`：在一定句柄范围内发现指定的特征
- `gatt_client_discover_characteristics_for_handle_range_by_uuid16`：在一定句柄范围内发现指定的特征
- `gatt_client_discover_characteristic_descriptors`：发现特征的所有描述符。

以 `gatt_client_discover_primary_services` 的使用为例说明使用方法。这个 API 的原型如下：

```c
uint8_t gatt_client_discover_primary_services(
  // 回调
  user_packet_handler_t callback,
  // 连接句柄
  hci_con_handle_t con_handle);
```

其回调函数的例子：

```c
static void service_discovery_callback(
    // 事件包类型（忽略）
    uint8_t packet_type,
    // 连接句柄（这个句柄也可以从事件内部获得，故忽略此参数）
    uint16_t _,
    // 事件包
    const uint8_t *packet,
    // 事件包大小
    uint16_t size)
{
    uint16_t con_handle;
    switch (packet[0])
    {
    // 对于发现的每个服务都有一个 QUERY_RESULT
    case GATT_EVENT_SERVICE_QUERY_RESULT:
        {
            const gatt_event_service_query_result_t *result =
                gatt_event_service_query_result_parse(packet);
            // ....
        }
        break;
    case GATT_EVENT_QUERY_COMPLETE:
        // 会话完成
        break;
    }
}
```

为了简化开发，SDK 提供了 *gatt_client_util* 模块，只调用一个函数就可以完成服务发现：

```c
struct gatt_client_discoverer *gatt_client_util_discover_all(
    // 连接句柄
    hci_con_handle_t con_handle,
    // 发现完成后的回调
    f_on_fully_discovered on_fully_discovered,
    // 传递给黑调的用户数据
    void *user_data);
```

下面的回调函数演示了如何遍历所有服务、特征：

```c
void my_on_fully_discovered(
    // 第一个服务
    service_node_t *first,
    // 用户数据
    void *user_data,
    // 错误码
    int err_code)
{
    if (err_code) ...
    service_node_t *s = first;
    // 遍历服务
    while (s)
    {
        char_node_t *c = s->chars;
        // 遍历服务的所有特征
        while (c)
        {
            desc_node_t *d = c->descs;
            // 遍历特征的所有描述符
            while (d)
            {
                d = d->next;
            }
            c = c->next;
        }
        s = s->next;
    }
}
```

### 9.2.3 读取特征 {#读取特征}

可以通过特征的句柄或者 UUID 读取值：

- `gatt_client_read_value_of_characteristic_using_value_handle`
- `gatt_client_read_value_of_characteristics_by_uuid16`
- `gatt_client_read_value_of_characteristics_by_uuid128`

也可以指定多个句柄批量读取：

- `gatt_client_read_multiple_characteristic_values`

基于句柄的分块读取：

- `gatt_client_read_long_value_of_characteristic_using_value_handle`
- `gatt_client_read_long_value_of_characteristic_using_value_handle_with_offset`

以 `gatt_client_read_value_of_characteristic_using_value_handle` 说明使用方法。其原型为：

```c
uint8_t gatt_client_read_value_of_characteristic_using_value_handle(
  // 回调
  btstack_packet_handler_t callback,
  // 连接句柄
  hci_con_handle_t con_handle,
  // 特征句柄
  uint16_t characteristic_value_handle);
```

其回调函数的例子：

```c
void read_characteristic_value_callback(
    // 事件包类型（忽略）
    uint8_t packet_type,
    // 连接句柄（这个句柄也可以从事件内部获得，故忽略此参数）
    uint16_t _,
    // 事件包
    const uint8_t *packet,
    // 事件包大小
    uint16_t size)
{
    switch (packet[0])
    {
    case GATT_EVENT_CHARACTERISTIC_VALUE_QUERY_RESULT:
        {
            uint16_t value_size;
            const gatt_event_value_packet_t *value =
                gatt_event_characteristic_value_query_result_parse(
                  packet, size, &value_size);
            // value->handle 为特征句柄
            // value_size 为值的长度
            // value->value 是指向值的指针
        }
        break;
    case GATT_EVENT_QUERY_COMPLETE:
        // 会话完成
        break;
    }
}
```

### 9.2.4 写入特征 {#写入特征}

通过特征的句柄写入值：

- `gatt_client_write_value_of_characteristic`：有响应的写入
- `gatt_client_write_value_of_characteristic_without_response`：无响应的写入

基于句柄的分块写入：

- `gatt_client_write_long_value_of_characteristic`
- `gatt_client_write_long_value_of_characteristic_with_offset`

其中 `gatt_client_write_value_of_characteristic` 的原型为：

```c
uint8_t gatt_client_write_value_of_characteristic(
    // 回调
    btstack_packet_handler_t callback,
    // 连接句柄
    hci_con_handle_t con_handle,
    // 特征句柄
    uint16_t characteristic_value_handle,
    // 值的长度
    uint16_t length,
    // 指向值的指针
    const uint8_t * data);
```

其回调函数的例子：

```c
void write_characteristic_value_callback(
    uint8_t packet_type, uint16_t _,
    const uint8_t *packet, uint16_t size)
{
    switch (packet[0])
    {
    case GATT_EVENT_QUERY_COMPLETE:
        platform_printf("特征写入完成。状态码：: %d\n",
            gatt_event_query_complete_parse(packet)->status);
        break;
    }
}
```

状态码的定义见 [ATT 错误码](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#ch0-att-err-codes)。

与之相比，无响应的写入不需要提供回调函数，没有“会话”的概念，下一次写入不需要等待上次完成，数据吞吐率更高。

```c
uint8_t gatt_client_write_value_of_characteristic_without_response(
    // 连接句柄
    hci_con_handle_t con_handle,
    // 特征句柄
    uint16_t characteristic_value_handle,
    // 值的长度
    uint16_t length,
    // 指向值的指针
    const uint8_t * data);
```

### 9.2.5 订阅特征 {#订阅特征}

开发者需要完成两个步骤：

1. 调用 `gatt_client_listen_for_characteristic_value_updates` 添加值更新时的回调函数

   ```c
   void gatt_client_listen_for_characteristic_value_updates(
       // 开发者提供一个回调函数结构体
       gatt_client_notification_t * notification,
       // 回调函数
       btstack_packet_handler_t packet_handler,
       // 连接句柄
       hci_con_handle_t con_handle,
       // 特征的值的句柄
       uint16_t value_handle);
   ```

   由于 `notification` 会被添加到 GATT 客户端实例的回调链表中，所以必须指向一块全局内存，一定**不能**在栈上分配。`notification` 所指向的内容不需要初始化。

   如果 notification 是从动态内存（如堆）里分配的，那么当连接断开时记得释放这块内存，以免泄露。
2. 调用 `gatt_client_write_characteristic_descriptor_using_descriptor_handle` 向 CCCD 写入使能标志

   这个函数的原型及使用方法与 `gatt_client_write_value_of_characteristic` 完全一致：

   ```c
   uint8_t gatt_client_write_characteristic_descriptor_using_descriptor_handle(
       // 回调函数
       btstack_packet_handler_t callback,
       // 连接句柄
       hci_con_handle_t con_handle,
       // CCCD 的句柄
       uint16_t descriptor_handle,
       // 数据长度（固定为 2）
       uint16_t length,
       // 值为 GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NOTIFICATION
       // 或   GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_INDICATION
       // 或   GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NONE
       uint8_t  * data);
   ```

   或者调用 `gatt_client_write_client_characteristic_configuration` 向 CCCD 写入使能标志。 这个函数的原型如下，它会自动发现 CCCD 的句柄而不需要通过参数传入：

   ```c
   uint8_t gatt_client_write_client_characteristic_configuration(
       // 回调函数
       btstack_packet_handler_t callback,
       // 连接句柄
       hci_con_handle_t con_handle,
       // 待订阅的特征
       gatt_client_characteristic_t * characteristic,
       // 值为 GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NOTIFICATION
       // 或   GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_INDICATION
       // 或   GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NONE
       uint16_t configuration);
   ```

   如果待订阅的特征不支持指定的配置，则相应地返回 `GATT_CLIENT_CHARACTERISTIC_NOTIFICATION_NOT_SUPPORTED` (`0x98`) 或 `GATT_CLIENT_CHARACTERISTIC_INDICATION_NOT_SUPPORTED` (`0x99`)。

### 9.2.6 ATT_MTU {#att_mtu-1}

除了通过监听 `GATT_EVENT_MTU` 事件以外，通过 `gatt_client_get_mtu` 可以随时获取 ATT_MTU：

```c
// 返回错误码
uint8_t gatt_client_get_mtu(
    // 连接句柄
    hci_con_handle_t con_handle,
    // 输出 MTU
    uint16_t * mtu);
```

特征的值的最大长度为 (ATT\_MTU - 3)。调用 `gatt_client_write_value_of_characteristic_without_response` 写入值时， 如果超过最大长度，会返回错误码：`GATT_CLIENT_VALUE_TOO_LONG` (`0x97`)。

### 9.2.7 自定义 MTU 42 {#自定义-mtu}

当 GATT 客户端实例创建时，会自动发起 MTU 协商。开发者可通过以下接口干预 MTU 协商过程。

1. 为协议栈配置 `STACK_GATT_CLIENT_DISABLE_MTU_EXCHANGE`，关闭 MTU 自动协商功能；
2. 通过 `gatt_client_exchange_mtu_request` 编程发起 MTU 协商：

   ```c
   int gatt_client_exchange_mtu_request(
       hci_con_handle_t con_handle, // 连接句柄
       uint16_t mtu);               // MTU 建议值
   ```

注意：一个连接上 GATT 客户端最多只能发起一次 MTU 协商过程。

---

1. <a id="fn40"></a>以及转发过来的 `L2CAP_EVENT_CAN_SEND_NOW` 事件。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-client.html#fnref40)
2. <a id="fn41"></a>SDK v8.4.23 及以上版本。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-client.html#fnref41)
3. <a id="fn42"></a>SDK v8.4.23 及以上版本。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-client.html#fnref42)