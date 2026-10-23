<!-- pg_ing918: 8 脉宽调制发生器（PWM） -->

# 8 脉宽调制发生器（PWM） {#ch-pwm}

PWM 模块实现脉冲宽度调制信号的产生，控制 LED 等外部器件。通过 APB 总线读写 寄存器来实现整个过程。ING918x 包括 6 个 PWM 模块，每个模块包含 2 个通道，因 此可以使用 12 个 PWM 通道。

PWM 特性：

- 每个通道都可以通过寄存器或 PWM 序列来控制
- 每个通道都可以屏蔽
- 寄存器中定义最多四个占空比序列
- 可以使用多种模式：命令模式、单步模式、对称模式、空白区模式

## 8.1 PWM 工作模式 {#pwm-工作模式}

PWM 使用的时钟频率可配置，请参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing918/ch-sysctrl.html#ch-sysctrl)。

每个 PWM 通道支持以下多种工作模式：

```c
typedef enum
{
    ..._UP_WITHOUT_DIED_ZONE          = ...,
    ..._UP_WITH_DIED_ZONE             = ...,
    ..._UPDOWN_WITHOUT_DIED_ZONE      = ...,
    ..._UPDOWN_WITH_DIED_ZONE         = ...,
    ..._SINGLE_WITHOUT_DIED_ZONE      = ...,
} PWM_WorkMode_t;
```

### 8.1.1 最简单的模式：UP_WITHOUT_DIED_ZONE {#最简单的模式up_without_died_zone}

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

### 8.1.2 UP_WITH_DIED_ZONE {#up_with_died_zone}

与 UP_WITHOUT_DIED_ZONE 相比，此模式需要一个新的死区门限 DZONE_TH，DZONE_TH 必须小于 HIGH_TH。以伪代码描述 A、B 输出如下：

cnt = 0; on_clock_rising_edge() { cnt = cnt < PERA_TH ? cnt + 1 : 0; A = HIGH_TH + DZONE_TH <= cnt; B = DZONE_TH <= cnt < HIGH_TH); }

### 8.1.3 UPDOWN_WITHOUT_DIED_ZONE {#updown_without_died_zone}

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

### 8.1.4 UPDOWN_WITH_DIED_ZONE {#updown_with_died_zone}

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

### 8.1.5 SINGLE_WITHOUT_DIED_ZONE {#single_without_died_zone}

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

### 8.1.6 输出控制 {#输出控制}

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

## 8.2 PWM 使用说明 {#pwm-使用说明}

### 8.2.1 启动与停止 {#启动与停止}

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

### 8.2.2 配置工作模式 {#配置工作模式}

```c
void PWM_SetMode(
    const uint8_t channel_index,    // 通道号
    const PWM_WorkMode_t mode       // 模式
    );
```

### 8.2.3 配置门限 {#配置门限}

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

### 8.2.4 输出控制 {#输出控制-1}

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

### 8.2.5 综合示例 {#综合示例}

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