# 基于 Trace 实现 LLPC预览功能

在蓝牙协议栈开发过程中，有时需要预先知道 LLCP。本文将介绍如何利用 Trace 机制实现 LLCP 预览功能。

## 实现原理 {#实现原理}

打开 Trace `PLATFORM_TRACE_ID_LLCP` 类型，Controller 会在接收到 LLCP 时通过 Trace 回调函数导出数据。 我们可以在回调函数里截获 `PLATFORM_TRACE_ID_LLCP`，并预览数据。这个的“预览”包含两层含义：

1. Controller 尚未处理该 PDU（Controller 将于 Trace 回调完成后处理 PDU）；
2. 只可读取 PDU 内容，不可修改。

让我们详细介绍实现方法。

### 1. Trace 数据结构 {#1-trace-数据结构}

`PLATFORM_TRACE_ID_LLCP` Trace 类型使用的头信息结构如下：

```highlight
#pragma pack (push, 1)
typedef struct
{
    uint32_t A;
    uint32_t B;
    uint8_t  id;
    uint8_t  tag;
} header_t;
#pragma pack (pop)
```

这个结构使用 `#pragma pack (push, 1)` 指令确保内存对齐。

### 2. Trace 回调处理 {#2-trace-回调处理}

假设 `cb_trace_read_llcp` 函数为 Trace 回调函数，在函数开头添加代码截获接收到的 LLCP：

```highlight
static uint32_t cb_trace_read_llcp(const platform_evt_trace_t *Trace, void *ctx)
{
    if (Trace->len1 == sizeof(header_t))
    {
        const header_t *p = (const header_t *)Trace->data1;
        if ((p->id == PLATFORM_TRACE_ID_LLCP) && (p->tag & 1))
        {
            const uint8_t *p8 = (const uint8_t *)Trace->data2;
            llcp_preview(p->tag >> 1, p8[0], p8 + 1, Trace->len2 - 1);
        }
    }

    // ...

    return 0;
}
```

### 3. PDU 预览显示 {#3-pdu-预览显示}

`llcp_preview` 函数负责预览 LLCP。下面的参考代码打印了关于 LLCP 的完整信息：

- 连接句柄（handle）
- 操作码（op_code）
- 控制数据

```highlight
static void llcp_preview(hci_con_handle_t handle, uint8_t op_code, const uint8_t *ctr_data, int ctr_data_len)
{
    platform_printf("LLCP[%d] OP %02x: ", handle, op_code);
    printf_hexdump(ctr_data, ctr_data_len);
    platform_printf("\n");
}
```

## 其它用法 {#其它用法}

### 修改公司 ID {#修改公司-id}

目前 SDK 未提供设置公司 ID 的接口，暂时可以通过直接修改 `LLCP_VERSION_IND` 内容的方法修改公司 ID（修改这个值不影响 Controller 的行为和流程。） 在下面的代码里，公司 ID 被修改为 `0xABCD`，小版本号被修改为 `0x1234`。

```highlight
#pragma pack (push, 1)
typedef struct
{
    uint8_t  version;
    uint16_t company_id;
    uint16_t subversion;
} llcp_version_ind_t;
#pragma pack (pop)

static uint32_t cb_trace_read_llcp(const platform_evt_trace_t *trace, void *ctx)
{
    if (trace->len1 == sizeof(header_t))
    {
        const header_t *p = (const header_t *)trace->data1;
        // 判断是否为发送方向的 LLCP
        if ((p->id == PLATFORM_TRACE_ID_LLCP) && (0 == (p->tag & 1)))
        {
            const uint8_t *p8 = (const uint8_t *)trace->data2;
            const uint16_t con_handle = p->tag >> 1;
            const uint8_t  op_code    = p8[0];
            const int ctrl_data_len   = trace->len2 - 1;
            uint8_t * ctrl_data       = (uint8_t *)p8 + 1;
            // 判断是否为 LLCP_VERSION_IND
            if ((op_code == 0x0c) && (ctrl_data_len == sizeof(llcp_version_ind_t)))
            {
                llcp_version_ind_t *ver_ind = (llcp_version_ind_t *)(ctrl_data);
                ver_ind->company_id = 0xABCD;
                ver_ind->subversion = 0x1234;
            }
        }
    }

    // ...

    return 0;
}
```

### 监控连接事件 {#监控连接事件}

下面的 Trace 回调函数 `cb_trace_connect_event` 演示了连接事件的判断，在每个连接结束时调用回调函数 `on_connection_event_end`。 注意这里 `header_t` 与上面不同。

```highlight
static void on_connection_event_end(uint8_t is_slave, uint8_t handle)
{
    platform_printf("end:%d,%d\n", is_slave, handle);
}

static uint32_t cb_trace_connect_event(const platform_evt_trace_t *trace, trace_rtt_t *ctx)
{
#pragma pack (push, 1)
    typedef struct
    {
        uint32_t A;
        uint32_t B;
        uint8_t  id;
    } header_t;

    typedef struct
    {
        uint8_t category;
        uint8_t param1, param2;
    } event_t;
#pragma pack (pop)

    if (trace->len1 == sizeof(header_t))
    {
        const header_t *p = (const header_t *)trace->data1;
        if (p->id == PLATFORM_TRACE_ID_EVENT)
        {
            if (trace->len2 == sizeof(event_t))
            {
                const event_t *e = (const event_t *)(trace->data2);
                if ((e->category == 1) && (2 <= e->param1) && (e->param1 <= 3))
                {
                    on_connection_event_end(e->param1 == 3, e->param2);
                }
            }
        }
    }

    // ...

    return 0;
}
```

## 总结 {#总结}

利用 Trace 机制实现的 PDU 预览功能，能帮助开发者实时监控 LLCP 通信，实现必要功能。

**温馨提示：**不要忘记设置 `PLATFORM_CFG_TRACE_MASK`，其中要包含所依赖的 Trace 项，如 `PLATFORM_TRACE_ID_LLCP` 或 `PLATFORM_TRACE_ID_EVENT`。
