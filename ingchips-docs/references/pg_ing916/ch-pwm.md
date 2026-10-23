<!-- pg_ing916: 15 增强型脉宽调制发生器（PWM） -->

# 15 增强型脉宽调制发生器（PWM） {#ch-pwm}

增强型脉宽调制发生器具有两大功能：生成脉宽调制信号（PWM），捕捉外部脉冲输入（PCAP）。 增强型脉宽调制发生器具备 3 个通道，每个通道都可以单独配置为 PWM 或者 PCAP 模式。 每个通道拥有独立的 FIFO。FIFO 里的每个存储单元为 2 个 20bit 数据。 FIFO 深度为 4，即最多存储 4 个单元，共 8 \times 20bit 数据。 这里的 20bit 位宽是因为本硬件模块内部 PWM 使用的各计数器都是 20 比特。 可根据 FIFO 内的数据量触发中断或者 DMA 传输。

说明：[TIMER](https://ingchips.github.io/drafts/pg_ing916/ch-timer.html#ch-timer) 也支持生成脉宽调制信号，但是可配置的参数较简单，不支持死区等。

PWM 特性：

- 最多支持 3 个 PWM 通道，每一个通道包含 A、B 两个输出
- 每个通道参数独立
- 支持死区
- 支持通过 DMA 更新 PWM 配置

PCAP 特性：

- 支持 3 个 PCAP 通道，每一个通道包含两个输入
- 支持捕捉上升沿、下降沿
- 支持通过 DMA 读取数据

## 15.1 PWM 工作模式 {#pwm-工作模式}

PWM 使用的时钟频率可配置，请参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#ch-sysctrl)。

每个 PWM 通道支持以下多种工作模式：

```c
typedef enum
{
    ..._UP_WITHOUT_DIED_ZONE          = ...,
    ..._UP_WITH_DIED_ZONE             = ...,
    ..._UPDOWN_WITHOUT_DIED_ZONE      = ...,
    ..._UPDOWN_WITH_DIED_ZONE         = ...,
    ..._SINGLE_WITHOUT_DIED_ZONE      = ...,
    ..._DMA                           = ...,
} PWM_WorkMode_t;
```

### 15.1.1 最简单的模式：UP_WITHOUT_DIED_ZONE {#最简单的模式up_without_died_zone}

此模式需要配置两个门限：计数器回零门限 PERA_TH、高门限 HIGH_TH，HIGH_TH 必须小于 HIGH_TH。以伪代码描述 A、B 输出如下：

```c
cnt = 0;
on_clock_rising_edge()
{
    cnt = cnt < PERA_TH ? cnt + 1 : 0;
    A = HIGH_TH <= cnt;
    B = !A;
}
```

### 15.1.2 UP_WITH_DIED_ZONE {#up_with_died_zone}

与 UP_WITHOUT_DIED_ZONE 相比，此模式需要一个新的死区门限 DZONE_TH，DZONE_TH 必须小于 HIGH_TH。以伪代码描述 A、B 输出如下：

```c
cnt = 0;
on_clock_rising_edge()
{
    cnt = cnt < PERA_TH ? cnt + 1 : 0;
    A = HIGH_TH + DZONE_TH <= cnt;
    B = DZONE_TH <= cnt < HIGH_TH);
}
```

### 15.1.3 UPDOWN_WITHOUT_DIED_ZONE {#updown_without_died_zone}

此模式需要的门限参数与 UP_WITHOUT_DIED_ZONE 相同。以伪代码描述 A、B 输出如下：

```c
cnt = 0;
on_clock_rising_edge()
{
    cnt = cnt < 2 * PERA_TH ? cnt + 1 : 0;
    A = PERA_TH - HIGH_TH <= cnt <= PERA_TH + HIGH_TH;
    B = !A;
}
```

### 15.1.4 UPDOWN_WITH_DIED_ZONE {#updown_with_died_zone}

与 UP_WITHOUT_DIED_ZONE 相比，此模式需要一个新的死区门限 DZONE_TH。 以伪代码描述 A、B 输出如下：

```c
cnt = 0;
on_clock_rising_edge()
{
    cnt = cnt < 2 * PERA_TH ? cnt + 1 : 0;
    A = PERA_TH - HIGH_TH + DZONE_TH <= cnt <= PERA_TH + HIGH_TH;
    B = (cnt < PERA_TH - HIGH_TH) || (cnt > PERA_TH + HIGH_TH + DZONE_TH);
}
```

### 15.1.5 SINGLE_WITHOUT_DIED_ZONE {#single_without_died_zone}

此模式需要配置两个门限：计数器回零门限 PERA_TH、高门限 HIGH_TH，HIGH_TH 必须小于 HIGH_TH。此模式只产生一个脉冲，以伪代码描述 A、B 输出如下：

```c
cnt = 0;
on_clock_rising_edge()
{
    cnt++;
    A = HIGH_TH <= cnt < PERA_TH;
    B = !A;
}
```

以上伪代码仅用于辅助描述硬件行为，与实际行为可以存在微小差异。

### 15.1.6 DMA 模式 {#dma-模式}

此模式支持通过 DMA 实时更新门限。

### 15.1.7 输出控制 {#输出控制}

对于每个通道的每一路输出，另有 3 个参数控制最终的两路输出：掩膜、停机输出值、反相。 最终的输出以伪代码描述如下：

```c
output_control(v)
{
    if (掩膜 == 1) return A 路输出 0、B 路输出 1;
    if (本通道已停机) return 停机输出值;
    if (反相) v = !v;
    return v;
}
```

## 15.2 PCAP {#pcap}

PCAP 每个通道包含两路输入。PCAP 内部有一个单独的 32 比特计数器[3](#fn3)， 当检测到输入信号变化（包含上升沿和下降沿）时，PCAP 将计数器的值及边沿变化信息作为一个存储单元压入 FIFO：

```c
struct data0
{
    uint32_t cnt_high:12;
    uint32_t p_cap_0_p:1; // A 路出现上升沿
    uint32_t p_cap_0_n:1; // A 路出现下降沿
    uint32_t p_cap_1_p:1; // B 路出现上升沿
    uint32_t p_cap_1_n:1; // B 路出现下降沿
    uint32_t tag:4;
    uint32_t padding:12;
};
struct data1
{
    uint32_t cnt_low:20;
    uint32_t padding:12;
};
```

通过复位整个模块可以清零 PCAP 计数器。

## 15.3 PWM 使用说明 {#pwm-使用说明}

### 15.3.1 启动与停止 {#启动与停止}

共有两个开关与 PWM 的启动和停止有关：使能（Enable）、停机控制（HaltCtrl）。只有当 `Enable` 为 1， `HaltCtrl` 为 0 时，PWM 才真正开始工作。

相关的 API 为：

```c
// 使能 PWM 通道
void PWM_Enable(
    const uint8_t channel_index,    // 通道号
    const uint8_t enable            // 使能或禁用
    );

// PWM 通道停机控制
void PWM_HaltCtrlEnable(
    const uint8_t channel_index,    // 通道号
    const uint8_t enable            // 停机(1) 或运转(0)
    );
```

### 15.3.2 配置工作模式 {#配置工作模式}

```c
void PWM_SetMode(
    const uint8_t channel_index,    // 通道号
    const PWM_WorkMode_t mode       // 模式
    );
```

### 15.3.3 配置门限 {#配置门限}

```c
// 配置 PERA_TH
void PWM_SetPeraThreshold(
    const uint8_t channel_index,
    const uint32_t threshold);
```

```c
// 配置 DZONE_TH
void PWM_SetDiedZoneThreshold(
    const uint8_t channel_index,
    const uint32_t threshold);
```

```c
// 配置 HIGH_TH
void PWM_SetHighThreshold(
    const uint8_t channel_index,
    const uint8_t multi_duty_index, // 对于 ING916XX，此参数无效
    const uint32_t threshold);
```

各门限值最大支持 0xFFFFF，共 20 个比特。

### 15.3.4 输出控制 {#输出控制-1}

```c
// 掩膜控制
void PWM_SetMask(
    const uint8_t channel_index,    // 通道号
    const uint8_t mask_a,           // A 路掩膜
    const uint8_t mask_b            // B 路掩膜
    );
```

```c
// 配置停机输出值
void PWM_HaltCtrlCfg(
    const uint8_t channel_index,    // 通道号
    const uint8_t out_a,            // A 路停机输出值
    const uint8_t out_b             // B 路停机输出值
    );
```

```c
// 反相
void PWM_SetInvertOutput(
    const uint8_t channel_index,    // 通道号
    const uint8_t inv_a,            // A 路是否反相
    const uint8_t inv_b             // B 路是否反相
    );
```

### 15.3.5 综合示例 {#综合示例}

下面的例子将 `channel_index` 通道配置成输出频率为 `frequency`、占空比为 `(on_duty)%` 的方波， 涉及 3 个关键参数：

- 生成这种最简单的 PWM 信号需要的模式为 UP_WITHOUT_DIED_ZONE；
- PERA_TH 控制输出信号的频率，设置为 `PWM_CLOCK_FREQ / frequency`；
- HIGH_TH 控制信号的占空比，设置为 `PERA_TH * (100 - on_duty) %`

```c
void PWM_SetupSimple(
    const uint8_t channel_index,
    const uint32_t frequency,
    const uint16_t on_duty)
{
    uint32_t pera = PWM_CLOCK_FREQ / frequency;
    uint32_t high = pera > 1000 ?
          pera / 100 * (100 - on_duty)
        : pera * (100 - on_duty) / 100;
    PWM_HaltCtrlEnable(channel_index, 1);
    PWM_Enable(channel_index, 0);
    PWM_SetPeraThreshold(channel_index, pera);
    PWM_SetHighThreshold(channel_index, 0, high);
    PWM_SetMode(channel_index, PWM_WORK_MODE_UP_WITHOUT_DIED_ZONE);
    PWM_SetMask(channel_index, 0, 0);
    PWM_Enable(channel_index, 1);
    PWM_HaltCtrlEnable(channel_index, 0);
}
```

### 15.3.6 使用 DMA 实时更新配置 {#使用-dma-实时更新配置}

使用 DMA 能够实时更新配置（相当于工作在 UP_WITHOUT_DIED_ZONE，但是每个循环使用不同的参数）： 每当 PWM 计数器计完一圈回零时，自动使用来自 DMA 的数据更新配置。 这些数据以 2 个 `uint32_t` 为一组，依次表示 HIGH_TH 和 PERA_TH。

```c
void PWM_DmaEnable(
    const uint8_t channel_index, // 通道号
    uint8_t trig_cfg,            // DMA 请求触发门限
    uint8_t enable               // 使能
    );
```

当 PWM 内部 FIFO 数据少于 `trig_cfg`，PWM 请求 DMA 传输数据。PWM FIFO 深度为 8 ，可以存储 8 个 32 比特数据（只有低 20 比特有效，其余比特忽略），相当于 4 组 PWM 配置， 所以 `trig_cfg` 的取值范围为 0..7。

## 15.4 PCAP 使用说明 {#pcap-使用说明}

### 15.4.1 配置 PCAP 模式 {#配置-pcap-模式}

要启用 PCAP 模式，需要 5 个步骤：

1. 关闭整个模块的时钟（参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#ch-sysctrl)）
2. 使用 `PCAP_Enable` 使能 PCAP 模式

   ```c
   void PCAP_Enable(
       const uint8_t channel_index     // 通道号
   );
   ```
3. 使用 `PCAP_EnableEvents` 选择要检测的事件

   ```c
   void PCAP_EnableEvents(
       const uint8_t channel_index,
       uint8_t events_on_0,
       uint8_t events_on_1);
   ```

   `events` 为下面两个事件的组合：

   ```c
   enum PCAP_PULSE_EVENT
   {
       PCAP_PULSE_RISING_EDGE  = 0x1,
       PCAP_PULSE_FALLING_EDGE = 0x2,
   };
   ```

   比如在通道 1 的 A 路输入上同时检测、上报上升沿和下降沿：

   ```c
   PCAP_EnableEvents(1,
       PCAP_PULSE_RISING_EDGE
       | PCAP_PULSE_FALLING_EDGE,
       ...);
   ```
4. 打开整个模块的时钟（参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#ch-sysctrl)）
5. 配置 DMA 传输

   当 PCAP 通道 FIFO 内存储的数据多于或等于 `trig_cfg` 时，请求 DMA 传输数据。`trig_cfg` 的取值范围为 0..7。

   ```c
   void PCAP_DmaEnable(
       const uint8_t channel_index, // 通道号
       uint8_t trig_cfg,            // DMA 请求触发门限
       uint8_t enable               // 使能
       );
   ```
6. 使能计数器

   ```c
   void PCAP_CounterEnable(
       uint8_t enable              // 使能(1)/禁用(0)
       );
   ```

### 15.4.2 读取计数器 {#读取计数器}

```c
uint32_t PCAP_ReadCounter(void);
```

---

1. <a id="fn3"></a>所有 6 路输入共有此计数器。[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-pwm.html#fnref3)