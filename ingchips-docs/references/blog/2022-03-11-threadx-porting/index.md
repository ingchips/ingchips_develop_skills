# 使用 Azure RTOS ThreadX

**说明：**微软于 2023 年 11 月宣布 Azure RTOS 将在 Eclipse 基金会的管理下过渡到开源模式（采用 MIT 协议）。

继 Amazon 将 FreeRTOS 收入麾下之后，微软于 2019 年 4 月将 Express Logic 收购， ThreadX 随之更名为 [Azure RTOS ThreadX](http://docs.microsoft.com/azure/rtos/threadx)。 本文以 Azure RTOS ThreadX 为例，说明如何在一种新的 RTOS 上运行 NoOS 项目。 首先创建一个新项目（开发环境可随意选择，ThreadX 全部兼容。），RTOS Options 选择“No RTOS”。下载 ThreadX [最新版](https://github.com/azure-rtos/threadx/releases)， 将 common、ports\cortex_m3、utility\low_power 等三部分代码添加到我们的项目里。

### 初识 ThreadX {#初识-threadx}

ThreadX 具有几个鲜明的特点：

- （几乎）一个函数对应一个独立的源文件，醒目、直接；
- 模块化程度高，比如，内存管理 `byte_allocate` 模块可以去除；
- 每个 API 都存在两个版本，一个以 `_txe_` 开头，包含**详尽**的参数检查，适合调试、学习；另一个是以 `_tx` 开头的“正常”版本； 调用 API 时只用 `tx_` 开头的宏版本，这个宏版本会依照编译选项映射成 `_txe_` 或者 `_tx`；
- 其它特性（如 preemption-threshold, event chaining, 性能分析等）跟移植关系不大，不再赘述。

### 移植 _tx_initialize_low_level {#移植-_tx_initialize_low_level}

从 ThreadX 示例项目的启动文件里找到这个函数，只保留栈指针相关内容：

```asm
    EXPORT  _tx_initialize_low_level
_tx_initialize_low_level

    IMPORT  _tx_thread_system_stack_ptr

    CPSID   i

    ; Set system stack pointer from vector value.
    LDR     r0, =_tx_thread_system_stack_ptr
    LDR     r1, =__Vectors
    LDR     r1, [r1]
    STR     r1, [r0]

    BX      lr
```

SysTick 和 MCU 异常优先级配置重新封装成两个函数：

```highlight
void _setup_sys_handlers(void)
{
    // Setup System Handlers 4-7 Priority Registers
    io_write(NVIC_ADDR + 0xD18, 0x00000000);

    // SVCl, Rsrv, Rsrv, Rsrv
    // Setup System Handlers 8-11 Priority Registers
    // Note: SVC must be lowest priority, which is 0xFF
    io_write(NVIC_ADDR + 0xD1C, 0xFF000000);

    // SysT, PnSV, Rsrv, DbgM
    // Setup System Handlers 12-15 Priority Registers
    // Note: PnSV must be lowest priority, which is 0xFF
    io_write(NVIC_ADDR + 0xD20, 0x40FF0000);
}

#define TICK_PER_SECOND                     1024
#define RTC_CYCLES_PER_TICK                 (RTC_CLK_FREQ / TICK_PER_SECOND)

void _systick_init(void)
{
    portNVIC_SYSTICK_LOAD_REG = RTC_CYCLES_PER_TICK - 1;
    portNVIC_SYSTICK_CURRENT_VALUE_REG  = 0;
    portNVIC_SYSTICK_CTRL_REG = portNVIC_SYSTICK_INT_BIT | portNVIC_SYSTICK_ENABLE_BIT | portNVIC_SYSTICK_CLK_BIT;
}
```

下面是通用 OS 接口在 ThreadX 上的具体实现。

### 堆相关 API {#堆相关-api}

我们分配一块大小确定的内存作为堆。

```highlight
#ifndef RTOS_HEAP_SIZE
#define RTOS_HEAP_SIZE             (20 * 1024)
#endif
static uint32_t heap[RTOS_HEAP_SIZE / sizeof(uint32_t)];
static TX_BYTE_POOL pool;

tx_byte_pool_create(&pool, NULL, heap, sizeof(heap));
```

实现一对分配、释放函数：

```highlight
static void *port_malloc(size_t size)
{
    void *p;
    return tx_byte_allocate(&pool, &p, size, 0) == TX_SUCCESS ? p : NULL;
}

static void port_free(void *p)
{
    tx_byte_release(p);
}
```

查看 ThreadX 源代码可知，这对函数是线程安全的。

### 软件定时器相关 API {#软件定时器相关-api}

软件定时器的存储空间由我们在堆上分配，然后将指针作为 `gen_handle_t`。具体实现如下：

```highlight
gen_handle_t port_timer_create(
        uint32_t timeout_in_ms,
        void *user_data,
        void (* timer_cb)(void *)
    )
{
    TX_TIMER *timer = (TX_TIMER *)port_malloc(sizeof(TX_TIMER));
    tx_timer_create(timer, NULL,
                    (fun_void_ul_f)timer_cb, (ULONG)user_data,
                    ms_to_ticks(timeout_in_ms), 0, TX_NO_ACTIVATE);
    return timer;
}

void port_timer_start(gen_handle_t timer)
{
    TX_TIMER *t = (TX_TIMER *)timer;
    tx_timer_activate(t);
}

void port_timer_stop(gen_handle_t timer)
{
    TX_TIMER *t = (TX_TIMER *)timer;
    tx_timer_deactivate(t);
}

void port_timer_delete(gen_handle_t timer)
{
    TX_TIMER *t = (TX_TIMER *)timer;
    tx_timer_delete(t);
    port_free(t);
}
```

### 任务相关 API {#任务相关-api}

ThreadX 里，优先级数目越大，优先级越低，最高为 0，最低为 (TX_MAX_PRIORITIES - 1)。参考实现：

```highlight
// ThreadX: Numerically smaller values imply higher priority
#define APP_PRIO_LOW               4
#define APP_PRIO_HIGH              2

gen_handle_t port_task_create(
        const char *name,
        void (*entry)(void *),
        void *parameter,
        uint32_t stack_size,                    // stack size in bytes
        enum gen_os_task_priority priority
    )
{
    TX_THREAD *thread = (TX_THREAD *)port_malloc(sizeof(TX_THREAD));
    VOID *stack = port_malloc(stack_size);
    tx_thread_create(thread, (char *)name,
                     (fun_void_ul_f)entry, (ULONG)parameter,
                     stack, stack_size,
                     priority == GEN_TASK_PRIORITY_LOW ? APP_PRIO_LOW : APP_PRIO_HIGH,
                     2,
                     TX_NO_TIME_SLICE, TX_AUTO_START);
    return (gen_handle_t)thread;
}
```

### 消息队列相关 API {#消息队列相关-api}

ThreadX 里消息长度必须是 4 字节的倍数，最长为 64 字节（TX_16_ULONG）。 通用 OS 接口里消息大小可能不是 4 字节的倍数，不过好在不会超过 64 字节（虽然文档里没注明）。

基于这些考虑，在从 ThreadX 取消息时，为了防止内存溢出，事先准备一段足够长度内存空间。实现如下：

```highlight
typedef struct
{
    TX_QUEUE queue;
    int msg_len;
    uint32_t msg[];
} tx_queue_sup_t;

gen_handle_t port_queue_create(int len, int item_size)
{
    // msg size is in 32-bit words
    int word_size = (item_size + 3) >> 2;
    int queue_byte_size = len * word_size * 4;
    tx_queue_sup_t *queue = (tx_queue_sup_t *)port_malloc(sizeof(tx_queue_sup_t) + word_size * 4);
    queue->msg_len = item_size;
    VOID *queue_start = (VOID *)port_malloc(queue_byte_size);

    if (tx_queue_create(&queue->queue, NULL, word_size, queue_start, queue_byte_size) != TX_SUCCESS)
        platform_raise_assertion(__FILE__, __LINE__);

    return (gen_handle_t)queue;
}

int port_queue_send_msg(gen_handle_t queue, void *msg)
{
    tx_queue_sup_t *q = (tx_queue_sup_t *)queue;
    return tx_queue_send(&q->queue, msg, TX_WAIT_FOREVER);
}

// return 0 if msg received; otherwise failed (timeout)
int port_queue_recv_msg(gen_handle_t queue, void *msg)
{
    tx_queue_sup_t *q = (tx_queue_sup_t *)queue;
    if (TX_SUCCESS == tx_queue_receive(&q->queue, q->msg, TX_WAIT_FOREVER))
    {
        memcpy(msg, q->msg, q->msg_len);
        return 0;
    }
    else
        return 1;
}
```

### 事件相关 API {#事件相关-api}

使用 ThreadX 的 EVENT_FLAGS 实现事件接口，设置事件时对应于 ThreadX 的 OR 操作：

```highlight
gen_handle_t port_event_create()
{
    TX_EVENT_FLAGS_GROUP *group = (TX_EVENT_FLAGS_GROUP *)port_malloc(sizeof(TX_EVENT_FLAGS_GROUP));
    tx_event_flags_create(group, NULL);

    return (gen_handle_t)group;
}

// return 0 if msg received; otherwise failed (timeout)
int port_event_wait(gen_handle_t event)
{
    ULONG actual_flags_ptr;
    return tx_event_flags_get((TX_EVENT_FLAGS_GROUP *)event, 1,
                    TX_AND_CLEAR, &actual_flags_ptr, TX_WAIT_FOREVER);
}

// event_set(event) will release the task in waiting.
void port_event_set(gen_handle_t event)
{
    tx_event_flags_set((TX_EVENT_FLAGS_GROUP *)event, 1, TX_OR);
}
```

### 全局临界区 API {#全局临界区-api}

可以借助 `TX_DISABLE`、`TX_RESTORE` 配合计数器实现。

### OS 入口 API {#os-入口-api}

ThreadX 的入口是 `tx_kernel_enter`。把它拆成两个部分：一部分在 `app_main` 返回 platform 之前执行，此时 ThreadX 允许创建线程；后一部分封装成通用 OS 的入口。

```highlight
// 前一部分
static void port_tx_initialize_kernel(void)
{
    // ...
    _systick_init();
    _setup_sys_handlers();
    _tx_thread_system_state =  TX_INITIALIZE_IN_PROGRESS;
}

// 后一部分
static void port_tx_start(void)
{
    _tx_thread_system_state =  TX_INITIALIZE_IS_FINISHED;

    /// ...

#ifdef TX_SAFETY_CRITICAL
    /* If we ever get here, raise safety critical exception.  */
    TX_SAFETY_CRITICAL_EXCEPTION(__FILE__, __LINE__, 0);
#endif
}
```

### 整合 {#整合}

```highlight
const gen_os_driver_t gen_os_driver =
{
    .timer_create = port_timer_create,
    .timer_start = port_timer_start,
    .timer_stop = port_timer_stop,
    .timer_delete = port_timer_delete,

    .task_create = port_task_create,

    .queue_create = port_queue_create,
    .queue_send_msg = port_queue_send_msg,
    .queue_recv_msg = port_queue_recv_msg,

    .event_create = port_event_create,
    .event_set = port_event_set,
    .event_wait = port_event_wait,

    .malloc = port_malloc,
    .free = port_free,
    .enter_critical = port_enter_critical,
    .leave_critical = port_leave_critical,
    .os_start = port_tx_start,
    .tick_isr = _tx_timer_interrupt,
    .svc_isr = no_op,
    .pendsv_isr = __tx_PendSVHandler,
};

const gen_os_driver_t *os_impl_get_driver(void)
{
    tx_byte_pool_create(&pool, NULL, heap, sizeof(heap));
    port_tx_initialize_kernel();

    return &gen_os_driver;
}
```

ThreadX 目前不使用 SVC 中断，`no_op` 是一个桩函数。

### 测试 {#测试}

参照 SDK 里 `Peripheral Console` 项目的 `profile.c`、`service_console.c` 加入项目，然后参照 `Peripheral Console (RT-Thread)` 修改 `main.c`，准备一条欢迎信息：

```highlight
#define expand2(X)  #X
#define expand(X)   expand2(X)

const char welcome_msg[] = "Built with Azure ThreadX (" expand(THREADX_MAJOR_VERSION) "."
                     expand(THREADX_MINOR_VERSION)  "." expand(THREADX_PATCH_VERSION) ")";
```

编译、下载、测试。

### 低功耗 {#低功耗}

ThreadX 默认的低功耗实现方式不合适，需要自行创建一个空闲线程，实现“无滴答”低功耗。空闲线程的具体实现与 `Peripheral Console (RT-Thread)` 类似，主要流程如下：

```highlight
void thread_idle_entry(ULONG thread_input)
{
    for (;;)
    {
        tx_timer_get_next(&tx_low_power_next_expiration);

        tx_low_power_next_expiration = platform_pre_suppress_ticks_and_sleep_processing(tx_low_power_next_expiration);

        tx_low_power_adjust_ticks = rtos_sleep_process(tx_low_power_next_expiration);

        tx_time_increment(tx_low_power_adjust_ticks);

        platform_os_idle_resumed_hook();
    }
}
```

至此，蓝牙协议栈、低功耗等两项功能都在 ThreadX 上运行起来了。

### 下载 {#下载}

直接 [下载](https://ingchips.github.io/blog/2022-03-11-threadx-porting/files/ing9187_demo_use_azure_rtos.zip) 完整的 Keil 5 项目代码。
