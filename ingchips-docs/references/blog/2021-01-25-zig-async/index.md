# 用 Zig 语言“消灭”回调函数

**温馨提醒：** 从 v8.2 开始，SDK 为部分蓝牙 API 提供了对应的同步版本，使用 C 语音也能以同步方式编写代码。详情请参考 [文档](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#ch-misc-synced-api)。

[Zig](https://ziglang.org/) 是一门新的、通用的编程语言。Zig 0.5.0 引入了 `async` 函数。 这一特性不依赖于任何操作系统特供的功能（线程、epoll），甚至都不需要在堆上分配内存。 这意思着 `async` 函数可以直接在 ING918xx 这样的嵌入式系统上使用。

以用 C 语言读取远端设备一个特性（Characteristics）的值为例，需要定义一个回调函数， 在这个回调函数里响应 `GATT_EVENT_CHARACTERISTIC_VALUE_QUERY_RESULT` 事件获取特性的值。 代码如下：

```C
void read_characteristic_value_callback(uint8_t packet_type, uint16_t _,
    const uint8_t *packet, uint16_t size)
{
    switch (packet[0])
    {
    case GATT_EVENT_CHARACTERISTIC_VALUE_QUERY_RESULT:
        {
            uint16_t value_size;
            const gatt_event_value_packet_t *value =
                gatt_event_characteristic_value_query_result_parse(packet, size,
                &value_size);
            if (value_size)
            {
                printf("VALUE of %d:\n", value->handle);
                show_value(value->value, value_size);
            }
        }
        break;
    case GATT_EVENT_QUERY_COMPLETE:
        // read a new one?
        break;
    }
}

gatt_client_read_value_of_characteristic_using_value_handle(
                read_characteristic_value_callback,
                conn_handle,
                value_handle);
```

如果需要读取两个特性，需要在 `GATT_EVENT_QUERY_COMPLETE` 事件中再次调用 `read_value_of_characteristic`。这时面临两个选择：

1. 定义一个新的回调函数 `read_characteristic_value_callback_2`

   选择这条路，每读一个特性对应地定义一个回调函数，在每个回调函数的 `GATT_EVENT_QUERY_COMPLETE` 事件里触发下一个特性的读取操作。这一连串的回调、读取，代码高度类似，维护困难。
2. 复用同一个回调函数 `read_characteristic_value_callback`

   这条路看起来虽然回调函数少了，但是回调函数需要识别当前正在读取哪个特性，再决定接下来需要读取哪个特性，逻辑复杂，代码杂乱。

Zig 为我们提供了又一种选择：`async`。 借助一个辅助模块，可以实现下面的效果：`demo` 函数先发现 `GAP` 服务； 如果服务存在，再发现其中的 `DEVICE_NAME` 特性；如果该特性存在，再读取特性的值。这三个 异步操作以同步执行的方式集中在一个函数里，逻辑清晰易懂。

```highlight
fn demo() void {
    var service = service_discoverer.discover_16(0,
        SIG_UUID_SERVICE_GENERIC_ACCESS) orelse return;
    var char_name = characteristics_discoverer.discover_16(0,
        service.start_group_handle, service.end_group_handle,
        SIG_UUID_CHARACT_GAP_DEVICE_NAME) orelse return;
    print("DEVICE_NAME       :");
    show_char_value(0, char_name.value_handle);
}

fn show_char_value(conn_handle: hci_con_handle_t, value_handle: u16) void {
    var value_size: u16 = 0;
    if (value_of_characteristic_reader.read(conn_handle,
        value_handle, &value_size)) |value| {
        print_hex_table(value, @as(c_int, value_size));
    }
}
```

Zig 的“野心”之一是取代 C。与 SDK 已经支持的 [Nim](https://ingchips.github.io/blog/sdk2.0_nim_zh/) 语言相比， Zig 与 C 完全无缝衔接， 几行代码就可以把 `platform` 提供的各种 API 导入：

```highlight
pub usingnamespace @cImport({
    @cInclude("platform_api.h");
    @cInclude("btstack_defines.h");
    @cInclude("gatt_client.h");
    @cInclude("sig_uuid.h");
    @cInclude("gap.h");
    @cInclude("FreeRTOS.h");
    @cInclude("task.h");
});
```

`demo()` 函数用到的 `service_discoverer` 的实现如下。这段 Zig 代码与 C 版本相比， 关键的区别就在于 Zig 引入的 `anyframe` 类型，及两个相应的操作 `suspend` 和 `resume`。

```highlight
bool session_complete = true;

pub var service_discoverer: ServiceDiscoverer = undefined;

const ServiceDiscoverer = struct {
    status: u8 = 0,
    frame: ? (anyframe -> ?gatt_client_service_t)= null,
    service: ?gatt_client_service_t = undefined,

    fn callback(packet_type: u8, _: u16, packet: [*c] const u8, size: u16) callconv(.C) void {
        switch (packet[0]) {
            GATT_EVENT_SERVICE_QUERY_RESULT => {
                var result = gatt_event_service_query_result_parse(packet);
                service_discoverer.service = result.*.service;
            },
            GATT_EVENT_QUERY_COMPLETE => {
                session_complete = true;
                service_discoverer.status = gatt_event_query_complete_parse(packet).*.status;
                if (service_discoverer.frame) |f| {
                    resume f;
                }
            },
            else => { }
        }
    }

    pub fn discover_16(self: *ServiceDiscoverer, conn_handle: hci_con_handle_t, uuid: u16) ?g
            gatt_client_service_t {
        if (!session_complete) return null;

        self.frame = null;
        self.service = null;
        session_complete = false;
        if (0 != gatt_client_discover_primary_services_by_uuid16(callback, conn_handle, uuid)) {
            session_complete = true;
            return null;
        }

        suspend {
            self.frame = @frame();
        }

        return self.service;
    }
};
```

最后，由于 `demo()` 函数遵从 `.Async` 调用规范，无法被 C 世界所调用，需要一个“桥接”函数连通 `.Async` 和 C：

```highlight
var the_frame: @Frame(demo) = undefined;

export fn zig_discover() void {
    the_frame = async demo();
}
```

这个 `zig_discover` 可以在 C 模块里直接调用。

**说明:** 本文使用的是 Zig 主分支最新版本 (撰写本文时 0.8.0 尚未发布)， 编译器在嵌入式系统交差编译方面仍存在一些问题， `@frameSize` 和 `@asyncCall` 的行为异常，上面的 `the_frame` 只能定义为全局变量。 对使用 Zig 进行嵌入式开发感兴趣的读者可以[下载](https://ingchips.github.io/files/zig_demo_0.1.zip)示例代码。
