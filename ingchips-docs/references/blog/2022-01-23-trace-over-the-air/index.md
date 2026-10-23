# 通过 BLE 抓取 Trace

Trace 对于分析协议栈流程问题非常重要。考虑到蓝牙设备的多样性，Trace 数据的导出、记录由开发者在应用里实现。 作为参考，SDK 里提供了 SWD、UART 两种“有线”方式，Wizard 能够[自动生成相关代码](https://ingchips.github.io/user_guide/tutorial.html#common-functions-page)。 在某些情况下，“有线”方式可能难以使用，得益于 ING918xx EFlash 的应用内编程（In-Application Programming，或称自编程，Self Programming）特性，可以先将 Trace [保存到 Flash 里](https://ingchips.github.io/blog/2021-12-04-sdk-6.7-new/#5-trace-到-flash-的使用方法)，然后导出。

还有一条通道可以用来导出数据：**BLE 空口**。本文介绍如何通过 BLE 从空中抓取 Trace 数据。 针对本文提供的参考实现，我们提供了[网页版 Log 记录器](https://ingchips.github.io/web_apps/air_trace/index_cn.html)。

**说明：**该功能相关代码将（或已）在版本 8.0.0 中发布，参考 UART GATT Console 示例。 在版本发布之前，开发者可以按照需要将本文提供的方法加入已有的项目中。

**注意：**本方法仅用调试。强烈不建议在量产产品中保留此功能，以免泄露敏感信息。

目前存在的四种导出/记录 Trace 数据的方法总结如下。

| **方法** | 端口 | 侵入性 | 数据量 | 传输速率 |
| --- | --- | --- | --- | --- |
| **SWD/RTT** | SWD，2 线 | 最低 | 无限 | 高 |
| **UART** | UART，1 线 | 较低。UART 产生较多中断，占用 MCU 处理时间 | 无限 | 较高 |
| **Flash** | 无 | 一般。占用 Flash 空间，写入速率低，占用 MCU 处理时间 | 受限于 Flash 空间 | 一般 |
| **BLE 空口** | 无 | 很高。需要修改 GATT Profile，多一条 BLE 连接 | 无限 | 一般，与原有 BLE 功能竞争 |

### 总体思路 {#总体思路}

1. 定义 Trace 服务，包含一个 Trace Data 特性（Characteristics）；
2. 实现 Trace 事件的回调，将数据写入一个环形缓冲区；
3. 当缓冲区内数据积累到一定量时，通过 Trace Data 特性发送数据。

### 接口定义 {#接口定义}

我们将该功能跟 GATT Profile 做隔离，定义以下接口。

```C
// 初始化。
// msg_id 用于 `btstack_push_user_msg`
// req_thres 用于控制 `btstack_push_user_msg` 的调用时机
void trace_air_init(trace_air_t *ctx, uint32_t msg_id, uint8_t req_thres);

// 当用于 Trace 的 BLE 连接建立时，使能；当连接断开时，禁用
// conn_handle 为连接句柄
// value_handle 为 Trace Data 的句柄
void trace_air_enable(trace_air_t *ctx, int enable, uint16_t conn_handle, uint16_t value_handle);

// 在收到 msg_id 这条用户消息时，调用该函数发送 Trace 数据
void trace_air_send(trace_air_t *ctx);

// Trace 事件的回调
uint32_t cb_trace_air(const platform_evt_trace_t *trace, trace_air_t *ctx);
```

### 具体实现 {#具体实现}

- 定义 Trace Service

  | **项目** | UUID |
  | --- | --- |
  | **Trace Service** | `00000006-494e-4743-4849-505355554944` |
  | **Trace Data 特性** | `bf83f3f2-399a-414d-9035-ce64ceb3ff67` |
- 上下文信息

  上下文信息的定义如下，主要包含环形缓冲区，句柄信息和状态：

  ```C
    typedef struct
    {
        // 环形缓冲区
        uint8_t           buffer[TRACE_BUFF_SIZE];
        uint16_t          write_next;
        uint16_t          read_next;

        SemaphoreHandle_t mutex;
        uint32_t          msg_id;
        uint16_t          value_handle;
        uint16_t          conn_handle;
        uint8_t           req_thres;
        uint8_t           enabled:1;
        uint8_t           msg_sent:1;   // 防止重复调用 btstack_push_user_msg
    } trace_air_t;
  ```
- `cb_trace_air`

  `cb_trace_air` 与 `trace.c` 模块的 `cb_trace_uart` 相似，唯一需要注意的是需要丢弃用于 Trace 的 BLE 连接上的 ACL 数据：

  ```C
    uint32_t cb_trace_air(const platform_evt_trace_t *trace, trace_air_t *ctx)
    {
    #pragma pack (push, 1)

        typedef struct
        {
            uint32_t A;
            uint32_t B;
            uint8_t  id;
            uint8_t  tag;
        } header_t;

        if (trace->len1 == sizeof(header_t))
        {
            const header_t *p = (const header_t *)trace->data1;
            if ((p->id == PLATFORM_TRACE_ID_HCI_ACL) && (p->tag == (ctx->conn_handle << 1)))
                return 0;
        }

    #pragma pack (pop)

        uint16_t next;
        int free_size;
        uint8_t use_mutex = !IS_IN_INTERRUPT();

        if (use_mutex)
            xSemaphoreTake(ctx->mutex, portMAX_DELAY);

        next = ctx->write_next;
        free_size = ctx->read_next - ctx->write_next;
        if (free_size <= 0) free_size += TRACE_BUFF_SIZE;
        if (free_size > 0) free_size--;

        free_size -= trace->len1;
        free_size -= trace->len2;
        if (free_size < 0)
        {
            if (use_mutex)
                xSemaphoreGive(ctx->mutex);
            trace_air_send_req(ctx);
            return 0;
        }

        next = trace_add_buffer(ctx->buffer, (const uint8_t *)trace->data1, trace->len1, next) & TRACE_BUFF_SIZE_MASK;
        next = trace_add_buffer(ctx->buffer, (const uint8_t *)trace->data2, trace->len2, next) & TRACE_BUFF_SIZE_MASK;

        ctx->write_next = next;

        if (use_mutex) xSemaphoreGive(ctx->mutex);

        if (free_size < ctx->req_thres)
            trace_air_send_req(ctx);

        return 0;
    }
  ```

  其中 `trace_air_send_req` 的参考实现如下：

  ```C
    static void trace_air_send_req(trace_air_t *ctx)
    {
        if ((0 == ctx->enabled) || ctx->msg_sent) return;
        ctx->msg_sent = 1;
        btstack_push_user_msg(ctx->msg_id, NULL, 0);
    }
  ```
- `trace_air_send`

  `trace_air_send` 与 `ring_buf.c` 模块的 `ring_buf_peek_data` 类似：

  ```C
    static int peek_data(trace_air_t *ctx, uint8_t *data, int len, uint8_t has_more)
    {
        int r = 0;
        int mtu = att_server_get_mtu(ctx->conn_handle) - 3;

        uint8_t *p = data;
        while (len)
        {
            int size = len > mtu ? mtu : len;
            if (att_server_notify(ctx->conn_handle, ctx->value_handle, p, size))
            {
                break;
            }
            len -= size;
            p += size;
            r += size;
        }

        return r;
    }

    void trace_air_send(trace_air_t *ctx)
    {
        ctx->msg_sent = 0;
        if (0 == ctx->enabled) return;

        uint32_t read_next = ctx->read_next;
        const uint32_t write_next = ctx->write_next;
        while (read_next != write_next)
        {
            int cnt = read_next > write_next ? sizeof(ctx->buffer) - read_next : write_next - read_next;
            int has_more = read_next > write_next ? 1 : 0;
            int c = peek_data(ctx, ctx->buffer + read_next, cnt, has_more);
            if (c < 1)
                break;
            read_next += c;
            if (read_next >= sizeof(ctx->buffer)) read_next = 0;
        }
        ctx->read_next = read_next;
    }
  ```
