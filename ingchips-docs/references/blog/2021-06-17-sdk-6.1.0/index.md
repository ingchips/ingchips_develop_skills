# SDK 6.1 新功能：延迟读取

## 原理与用法 {#原理与用法}

(G)ATT Server 可以通过两种方式将特性（Characteristics）的数值传递到 Client：Client 订阅 （Server 主动发送 Indication 或者 Notification）和 Client 主动读取。

Client 主动读取分为“静态”与“动态”两种情况：

- 静态数值存储于 ATT 数据库内，协议栈直接提取数值传递到 Client
- 对于动态数值，协议栈每次读取数值时会两次调用回调函数（`att_read_callback`）：第一次数据指针为空，用来获取数值长度； 第二次数据指针不为空，回调函数此时将数据写入数据指针指向的内存。

这里动态数值的回调是一种同步读取。对于需要消耗较多时间才能读取数据的情况，比如初始化传感器并等待数据稳定， 同步读取的方法并不合适。

SDK 6.1 里新增了一种延迟读取 (Deferred read) 的方法，步骤如下：

1. 回调函数 `att_read_callback` 在第一次被调用（数据指针为空）时返回 `ATT_DEFERRED_READ`；
2. app 开始获取数据；
3. 数据就绪之后，调用 `att_server_deferred_read_response` 发送数据。

## 示例 {#示例}

GATT Relay 首先克隆一个指定设备（设备 A）的广播数据，然后连接到该设备，克隆它的 GATT Profile，再发送克隆得到的广播数据等待连接。 用其它设备（设备 B）连接到 GATT Relay 后，GATT Relay 会把设备 B 里的 GATT Client 发起的所有请求转发到设备 A， 再将响应转发回设备 B。

这个例子里回调函数使用延迟读取方式，待 GATT Client 从设备 A 获得数据后，调用 `att_server_deferred_read_response` 将结果传递到设备 B。

```C
void gatt_read_callback(uint8_t packet_type, uint16_t _, const uint8_t *packet, uint16_t size)
{
    switch (packet[0])
    {
    case GATT_EVENT_CHARACTERISTIC_VALUE_QUERY_RESULT:
        {
            uint16_t value_size;
            const gatt_event_value_packet_t *value =
                gatt_event_characteristic_value_query_result_parse(packet, size, &value_size);
            att_server_deferred_read_response(handle_to_master,
                                              handle_map_from_slave[value->handle],
                                              value->value, value_size);
        }
        break;
    //...
    }
}
```

```C
static uint16_t att_read_callback(hci_con_handle_t connection_handle, uint16_t att_handle, uint16_t offset,
                                  uint8_t * buffer, uint16_t buffer_size)
{
    if (buffer == NULL)
    {
        uint16_t handle = handle_map_to_slave[att_handle];
        gatt_client_read_value_of_characteristic_using_value_handle(gatt_read_callback,
            handle_to_slave,
            handle);
        return ATT_DEFERRED_READ;
    }
    // ...
}
```
