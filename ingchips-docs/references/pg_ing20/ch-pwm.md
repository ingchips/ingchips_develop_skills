<!-- pg_ing20: 11 增强型脉宽调制发生器（PWM） -->

# 11 增强型脉宽调制发生器（PWM） {#ch-pwm}

增强型脉宽调制发生器具有：生成脉宽调制信号（PWM），捕捉外部脉冲输入（PCAP），带载波生成IR发送信号， 捕获计算IR信号。 增强型脉宽调制发生器具备 3 个通道，每个通道都可以单独配置为 PWM 或者 PCAP 模式。 每个通道拥有独立的 FIFO。FIFO 里的每个存储单元为 2 个 20bit 数据。 FIFO 深度为 4，即最多存储 4 个单元，共 8 \times 20bit 数据。 这里的 20bit 位宽是因为本硬件模块内部 PWM 使用的各计数器都是 20 比特。 可根据 FIFO 内的数据量触发中断或者 DMA 传输。

说明：[TIMER](https://ingchips.github.io/drafts/pg_ing20/ch-timer.html#ch-timer) 也支持生成脉宽调制信号，但是可配置的参数较简单，不支持死区等。

PWM 特性：

- 最多支持 3 个 PWM 通道，每一个通道包含 A、B 两个输出
- 每个通道参数独立
- 支持死区
- 支持通过 DMA 更新 PWM 配置
- 支持WS2812位带灯控制

PCAP 特性：

- 支持 3 个 PCAP 通道，每一个通道包含两个输入
- 支持捕捉上升沿、下降沿
- 支持通过 DMA 读取数据

IR 特性： * 支持 IR 捕获模式。 * 支持 IR 发送，可配置不同载波频率。

## 11.1 PWM 工作模式 {#pwm-工作模式}

PWM 使用的时钟频率可配置，请参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing20/ch-sysctrl.html#ch-sysctrl)。

每个 PWM 通道支持以下多种工作模式：

```c
typedef enum
{
    PWM_WORK_MODE_UP_WITHOUT_DIED_ZONE          = 0x0,
    PWM_WORK_MODE_UP_WITH_DIED_ZONE             = 0x1,
    PWM_WORK_MODE_UPDOWN_WITHOUT_DIED_ZONE      = 0x2,
    PWM_WORK_MODE_UPDOWN_WITH_DIED_ZONE         = 0x3,
    PWM_WORK_MODE_SINGLE_WITHOUT_DIED_ZONE      = 0x4,
    PWM_WORK_MODE_DMA                           = 0x5,
    PWM_WORK_MODE_PCAP                          = 0x6,
    PWM_WORK_MODE_IR                            = 0x7
} PWM_WorkMode_t;
```

### 11.1.1 最简单的模式：UP_WITHOUT_DIED_ZONE {#最简单的模式up_without_died_zone}

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

### 11.1.2 UP_WITH_DIED_ZONE {#up_with_died_zone}

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

### 11.1.3 UPDOWN_WITHOUT_DIED_ZONE {#updown_without_died_zone}

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

### 11.1.4 UPDOWN_WITH_DIED_ZONE {#updown_with_died_zone}

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

### 11.1.5 SINGLE_WITHOUT_DIED_ZONE {#single_without_died_zone}

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

### 11.1.6 DMA 模式 {#dma-模式}

此模式支持通过 DMA 实时更新门限。

### 11.1.7 输出控制 {#输出控制}

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

## 11.2 PCAP {#pcap}

PCAP 每个通道包含两路输入。PCAP 内部有一个单独的 32 比特计数器[2](#fn2)， 当检测到输入信号变化（包含上升沿和下降沿）时，PCAP 将计数器的值及边沿变化信息作为一个存储单元压入 FIFO：

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

## 11.3 IR模式 {#ir模式}

IR可以使能一路IR信号输出，载波频率可配，通过配置pwm输出步进可生成灵活的IR信号，推荐预定义IR数据流，使用DMA的方式快速完成IR控制信号输出。

### 11.3.1 IR发送(模式1) {#ir发送模式1}

IR通过接口`IR_CycleCarrierSetup`配置两组固定的不同频率的PWM波形。两组不同频率的PWM波形可以组成IR的基本单元，带载波脉冲波形和不带脉冲的低电平。模式一通过向FIFO写入发送某一组波形重复次数的方式实现发送带载波和不带载波的波形。

```c
void IR_CycleCarrierSetup(uint8_t channel, uint8_t carry_channel,
                        uint32_t frequency, uint32_t duty);
```

例如：标准NEC协议使用38K周期的载波，推荐载波占空比为25% - 30%。 - 逻辑0为2，25ms，脉冲时间560us - 逻辑1为1.12ms,脉冲时间560us

对应配置的两组PWM频率

- group1，38k频率30%占空比
- group0 保持低电平

代码调用接口初始化为:

```c
IR_CycleCarrierSetup(0,0,38000,30);// group 1
IR_CycleCarrierSetup(0,1,38000,0);// group 0
```

PWM初始化两组PWM数据完成后，可以通过写入16bit的FIFO数据的方式，控制发送某一组PWM的重复次数来模拟IR的数据发送，**写入 FIFO的数据含义为0-14bit代表重复发送该组频率波形的次数，15bit（最高位）代表要发送的是那一组预先设置的pwm波形**

例如：发送一个NEC的逻辑0序列。脉冲时间和非脉冲时间都约为560us，根据38k的频率周期，持续560us脉冲需要重复发送约21个周期。

```c
while(PWM_GetFifoStatus(0) & 0x2);
IR_WriteCarrierData(0,21);
IR_WriteCarrierData(0,21|(1<<15));
```

对应的发送一个逻辑1序列，持续560us脉冲需要重复发送约21个周期，低电平时间需要重复发送63个周期，代码实现如下

```c
while(PWM_GetFifoStatus(channel_index) & 0x2);
IR_WriteCarrierData(channel_index,21);
IR_WriteCarrierData(channel_index,63|(1<<15));
```

### 11.3.2 IR发送(模式2) {#ir发送模式2}

和只能发送两组预先设置好不同频率的PWM载波的模式1不同，模式2更加的灵活，可以通过向FIFO写入每次要发送的threshold和period值来实时修改每次发送载波的频率或占空比，与之相对的，灵活的代价是操作的复杂性，每次触发一次波形发送需要操作fifo写入两次，第一次写入对应的threshold和period值来表示当前要发送波形的周期（10bit）和占空比（10bit），第二次写入当前要发送波形的重复次数（15bit）

**写入FIFO的数据含义为：**

- 第一次写入10-19bit周期（根据PWM的时钟和载波频率计算） 0-9bit占空比（根据载波占空比和周期值计算）
- 第二次写入0-14bit代表需要发送的波形的重复次数

例如：发送一个NEC的序列,先根据对应的PWM模块时钟计算38k载波对应的周期`pera_38k`和占空比`duty_38k`的值

```c
uint32_t pera_38k = PWM_CLOCK_FREQ / 38000;
uint32_t duty_38k = pera_38k > 1000 ? pera_38k / 100 * (100 - 30) : pera_38k * (100 - 30) / 100;
```

发送一个NEC的逻辑0序列。脉冲时间和非脉冲时间都约为560us，根据38k的频率周期，持续560us脉冲需要重复发送约21个周期。

```c
    while(PWM_GetFifoStatus(channel_index) & 0x2);
    IR_WriteCarrierReloadData(channel_index,(pera_38k<<10)|duty_38k);
    IR_WriteCarrierReloadData(channel_index,21);
    IR_WriteCarrierReloadData(channel_index,(pera_38k<<10)|pera_38k);
    IR_WriteCarrierReloadData(channel_index,21);
```

对应的发送一个逻辑1序列，持续560us脉冲需要重复发送约21个周期，低电平时间需要重复发送63个周期，代码实现如下:

```c
    while(PWM_GetFifoStatus(channel_index) & 0x2);
    IR_WriteCarrierReloadData(channel_index,(pera_38k<<10)|duty_38k);
    IR_WriteCarrierReloadData(channel_index,21);
    IR_WriteCarrierReloadData(channel_index,(pera_38k<<10)|pera_38k);
    IR_WriteCarrierReloadData(channel_index,63);
```

### 11.3.3 IR接收 {#ir接收}

IR抓取模式以PCAP模式为基础，通过PCAP抓取IR信号，通内部配置IR信号解码参数，可完成IR信号的解码，解码结果输出到对应FIFO。 在此模式下，需要将步进配置为预测的IR的3〜6次 频率通过寄存器pera_th，建议使用200kHz，IR给出将抓取 以下时间节点：

- 1，第一个上升的边缘，跌落边缘，第二次上升边缘，跌落边缘，以便 确定载波频率。
- 2，载波停止的时间点以及它开始的时间点。

## 11.4 PWM 使用说明 {#pwm-使用说明}

### 11.4.1 启动与停止 {#启动与停止}

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

### 11.4.2 配置工作模式 {#配置工作模式}

```c
void PWM_SetMode(
    const uint8_t channel_index,    // 通道号
    const PWM_WorkMode_t mode       // 模式
    );
```

### 11.4.3 配置门限 {#配置门限}

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
    const uint8_t multi_duty_index, // 对于 ING20XX，此参数无效
    const uint32_t threshold);
```

各门限值最大支持 0xFFFFF，共 20 个比特。

### 11.4.4 输出控制 {#输出控制-1}

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

### 11.4.5 综合示例 {#综合示例}

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

### 11.4.6 使用 DMA 实时更新配置 {#使用-dma-实时更新配置}

使用 DMA 能够实时更新配置（相当于工作在 UP_WITHOUT_DIED_ZONE，但是每个循环使用不同的参数）： 每当 PWM 计数器计完一圈回零时，自动使用来自 DMA 的数据更新配置。 这些数据以 2 个 `uint32_t` 为一组，依次表示 HIGH_TH 和 PERA_TH。

```c
void PWM_DmaEnable(
    const uint8_t channel_index, // 通道号
    uint8_t trig_cfg,            // DMA 请求触发门限
    uint8_t enable               // 使能
    );
```

当 PWM 内部 FIFO 数据少于 `trig_cfg`，PWM 请求 DMA 传输数据。PWM FIFO 深度为 8 ，可以存储 8 个 32 比特数据（只有低 20 比特有效，其余比特忽略），相当于 4 组 PWM 配置， 所以 `trig_cfg` 的取值范围为 0..7。

## 11.5 PCAP 使用说明 {#pcap-使用说明}

### 11.5.1 配置 PCAP 模式 {#配置-pcap-模式}

要启用 PCAP 模式，需要 5 个步骤：

1. 关闭整个模块的时钟（参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing20/ch-sysctrl.html#ch-sysctrl)）
2. 使用 `PCAP_Enable` 使能 PCAP 模式

```c
void PCAP_Enable(
    const uint8_t channel_index     // 通道号
);
```

1. 使用 `PCAP_EnableEvents` 选择要检测的事件

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

1. 打开整个模块的时钟（参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing20/ch-sysctrl.html#ch-sysctrl)）
2. 配置 DMA 传输

当 PCAP 通道 FIFO 内存储的数据多于或等于 `trig_cfg` 时，请求 DMA 传输数据。`trig_cfg` 的取值范围为 0..7。

```c
 void PCAP_DmaEnable(
     const uint8_t channel_index, // 通道号
     uint8_t trig_cfg,            // DMA 请求触发门限
     uint8_t enable               // 使能
     );
```

1. 使能计数器

```c
 void PCAP_CounterEnable(
     uint8_t enable              // 使能(1)/禁用(0)
     );
```

### 11.5.2 读取计数器 {#读取计数器}

```c
uint32_t PCAP_ReadCounter(void);
```

## 11.6 IR模式示例 {#ir模式示例}

### 11.6.1 IR 发送模式 {#ir-发送模式}

该模式演示了NEC发送一段NEC数据序列的代码，需要根据NEC的序列要求，计算要填入fifo的数值，之后通过写fifo或DMA的形式发送NEC序列。

```c
//IR Step Mode constant
#define IR_REG_SW   (1<<15)
#define NEC_START_P_NUM 342
#define NEC_START_I_NUM 172
#define NEC_LOGIC_NUM 22
#define NEC_STOP_NUM  22

void PWM_Init(void)
{
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ITEM_APB2_PWM) | (1 << SYSCTRL_ITEM_APB1_PinCtrl) | (1 << SYSCTRL_ITEM_APB1_GPIO0));
    PINCTRL_SetPadMux(GIO_GPIO_8,IO_SOURCE_PWM4_A);
    PINCTRL_SetPadMux(GIO_GPIO_7,IO_SOURCE_PWM4_B);
}
void IR_Step_Mode_init(const uint8_t channel_index)
{
    PWM_Init();

    PWM_Enable(channel_index, 0);

    SYSCTRL_EnablePcapMode(channel_index,0);
    PWM_SetMask(channel_index,0,0);//设置通道输出极性
    SYSCTRL_ReleaseBlock(SYSCTRL_ITEM_APB2_PWM);
    SYSCTRL_ClearClkGate(SYSCTRL_ITEM_APB2_PWM);
    PWM_SetMode(channel_index, PWM_WORK_MODE_IR);
    PWM_StepEnabled(channel_index,0);//close step enabled
    IR_CycleCarrierSetup(channel_index,0,38000,70);
    IR_CycleCarrierSetup(channel_index,1,38000,0);

    PWM_Enable(channel_index, 1);
}

void NEC_START(const uint8_t channel_index)
{
    IR_WriteCarrierData(channel_index,NEC_START_P_NUM);
    while (IR_BusyState(channel_index));
    IR_WriteCarrierData(channel_index,NEC_START_I_NUM | IR_REG_SW);
    while (IR_BusyState(channel_index));
}

void NEC_LOGIC(const uint8_t channel_index,uint8_t x)
{
    uint8_t pulse;
    IR_WriteCarrierData(channel_index,NEC_LOGIC_NUM);
    while (IR_BusyState(channel_index));
    pulse = NEC_LOGIC_NUM*(x * 2 + 1);
    IR_WriteCarrierData(channel_index,pulse | IR_REG_SW);
    while (IR_BusyState(channel_index));
}
void NEC_STOP(const uint8_t channel_index)
{
    IR_WriteCarrierData(channel_index,NEC_STOP_NUM);
    while(IR_BusyState(channel_index));
}

void IR_Write_data(const uint8_t channel_index,uint8_t  data)
{
    uint8_t  i;
    for(i = 0; i<8; i++)
    {
        NEC_LOGIC(channel_index,((data>>i) & 0x01));
    }
}

void IR_NECSend_Command(const uint8_t channel_index,uint8_t address, uint8_t cmd)
{
    NEC_START(channel_index);
    IR_Write_data(channel_index,address);
    IR_Write_data(channel_index,~address);
    IR_Write_data(channel_index,cmd);
    IR_Write_data(channel_index,~cmd);
    NEC_STOP(channel_index);
}

void PWM_IR_Reset(uint8_t channel)
{
    PWM_Enable(channel, 0);
    PWM_Enable(channel, 1);
}

void IR_test_cycle(const uint8_t channel_index,uint8_t address, uint8_t cmd)
{
    PWM_IR_Reset(channel_index);
    IR_NECSend_Command(channel_index,address, cmd);
    delay_ms(200);
}

void main(void)
{
    IR_Step_Mode_init(0);
    IR_test_cycle(0,0xFF,0x00);
    IR_test_cycle(0,0xFF,0x00);
    while(1);
}
```

### 11.6.2 IR接收模式 {#ir接收模式}

该模式通过抓取载波频率和具体的信号步进的方式解析对应的红外信号，以下是代码示例(部分函数实现可参考发送部分配置)：

```c
//IR Grabbing test function
void IR_Grabbing_TX(void)
{
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ITEM_APB2_PWM) | (1 << SYSCTRL_ITEM_APB1_PinCtrl) | (1 << SYSCTRL_ITEM_APB1_GPIO0));
    PINCTRL_SetPadMux(GIO_GPIO_8,IO_SOURCE_PWM5_A);

    PWM_Enable(1, 0);

    SYSCTRL_EnablePcapMode(1,0);
    PWM_SetMask(1,0,0);
    SYSCTRL_ReleaseBlock(SYSCTRL_ITEM_APB2_PWM);
    SYSCTRL_ClearClkGate(SYSCTRL_ITEM_APB2_PWM);
    PWM_SetMode(1, PWM_WORK_MODE_IR);
    PWM_StepEnabled(1,0);//close step enabled
    IR_CycleCarrierSetup(1,0,38000,70);
    IR_CycleCarrierSetup(1,1,38000,0);

    PWM_Enable(1, 1);
}

void IR_Grabbing_init(void)
{
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ITEM_APB1_PinCtrl) | (1 << SYSCTRL_ITEM_APB1_GPIO0));
    PINCTRL_SelPCAPIn(0, GIO_GPIO_7);
    SYSCTRL_EnablePcapMode(0,1);
    SYSCTRL_ReleaseBlock(SYSCTRL_ITEM_APB2_PWM);
    SYSCTRL_ClearClkGate(SYSCTRL_ITEM_APB2_PWM);
    PCAP_Enable(0);
    PWM_StepEnabled(0,1);
    PCAP_EnableEvents(0,
                        PCAP_PULSE_RISING_EDGE | PCAP_PULSE_FALLING_EDGE,
                        PCAP_PULSE_RISING_EDGE | PCAP_PULSE_FALLING_EDGE);
    APB2_PWM->Channels[0].Ctrl0 &= ~(0x7 << 12);
    APB2_PWM->Channels[0].Ctrl0 |=  (0x1 << 12);
    uint32_t pera = PWM_CLOCK_FREQ / 200000;
    APB2_PWM->Channels[0].PeraTh = pera;
    NVIC_Configuration();
    PWM_FifoIntEnable(0,1,PWM_FIFO_TRIGGER_EN);
    PCAP_CounterEnable(1);
    PWM_Enable(0, 1);
}

void IR_Grabbing_test(void)
{
    IR_Grabbing_init();
    IR_Grabbing_TX();

    IR_test_cycle(1,0xFF,0x00);
}
```

---

1. <a id="fn2"></a>所有 6 路输入共有此计数器。[↩︎](https://ingchips.github.io/drafts/pg_ing20/ch-pwm.html#fnref2)