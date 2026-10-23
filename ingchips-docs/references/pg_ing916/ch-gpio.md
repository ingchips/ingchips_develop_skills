<!-- pg_ing916: 7 通用输入输出（GPIO） -->

# 7 通用输入输出（GPIO） {#ch-gpio}

## 7.1 功能概述 {#功能概述-2}

GPIO 模块常用于驱动 LED 或者其它指示器，控制片外设备，感知数字信号输入，检测信号边沿， 或者从低功耗状态唤醒系统。ING916XX 系列芯片内部支持最多 42 个 GPIO，通过 [PINCTRL](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#ch-pinctrl) 可将 GPIO n 引出到芯片 IO 管脚 n。

特性：

- 每个 GPIO 都可单独配置为输入或输出
- 每个 GPIO 都可作为中断请求，中断触发方式支持边沿触发（上升、下降单沿触发，或者双沿触发） 和电平触发（高电平或低电平）
- 硬件去抖

在硬件上存在 **两个** GPIO 模块，每个模块包含 21 个 GPIO，相应地定义了两个 `SYSCTRL_Item`：

```c
typedef enum
{
    SYSCTRL_ITEM_APB_GPIO0     ,
    SYSCTRL_ITEM_APB_GPIO1     ,
    // ...
} SYSCTRL_Item;
```

注意按照所使用的 GPIO 管脚打开对应的 GPIO 模块。

## 7.2 使用说明 {#使用说明-2}

### 7.2.1 设置 IO 方向 {#设置-io-方向}

在使用 GPIO 之前先按需要配置 IO 方向：

- 需要用于输出信号时：配置为输出
- 需要用于读取信号时：配置为输入
- 需要用于生产中断请求时：配置为输入
- 需要高阻态时：配置为高阻态

使用 `GIO_SetDirection` 配置 GPIO 的方向。GPIO 支持四种方向：

```c
typedef enum
{
    GIO_DIR_INPUT,  // 输入
    GIO_DIR_OUTPUT, // 输出
    GIO_DIR_BOTH,   // 同时支持输入、输出
    GIO_DIR_NONE    // 高阻态
} GIO_Direction_t;
```

如无必要，不要使用 `GIO_DIR_BOTH`。

### 7.2.2 读取输入 {#读取输入}

使用 `GIO_ReadValue` 读取某个 GPIO 当前输入的电平信号，例如读取 GPIO 0 的输入：

```c
uint8_t value = GIO_ReadValue(GIO_GPIO_0);
```

使用 `GIO_ReadAll` 可以同时读取所有 GPIO 当前输入的电平信号。其返回值的第 n 比特 （第 0 比特为最低比特）对应 GPIO n 的输入；如果 GPIO n 当前不支持输入，那么第 n 比特为 0：

```c
uint64_t GIO_ReadAll(void);
```

### 7.2.3 设置输出 {#设置输出}

- 设置单个输出

  使用 `GIO_WriteValue` 设置某个 GPIO 输出的电平信号，例如使 GPIO 0 输出高电平（1）：

  ```c
  GIO_WriteValue(GIO_GPIO_0, 1);
  ```
- 同时设置所有输出

  通过 `GIO_WriteAll` 可同时设置所有 GPIO 输出的电平信号：

  ```c
  void GIO_WriteAll(const uint64_t value);
  ```
- 将若干输出置为高电平

  通过 `GIO_SetBits` 可同时将若干 GPIO 输出置为高电平：

  ```c
  void GIO_SetBits(const uint64_t index_mask);
  ```

  比如要将 GPIO 0、5 置为高电平，那么 `index_mask` 为 `(1 << 0) | (1 << 5)`。
- 将若干输出置为低电平

  通过 `GIO_ClearBits` 可同时将若干 GPIO 输出置为低电平：

  ```c
  void GIO_ClearBits(const uint64_t index_mask);
  ```

  `index_mask` 的使用与 `GIO_SetBits` 相同。

### 7.2.4 配置中断请求 {#配置中断请求}

使用 `GIO_ConfigIntSource` 配置 GPIO 生成中断请求。

```c
void GIO_ConfigIntSource(
  const GIO_Index_t io_index,     // GPIO 编号
  const uint8_t enable,           // 使能的边沿或者电平类型组合
  const GIO_IntTriggerType_t type // 触发类型
  );
```

其中的 `enable` 为以下两个值的组合（0 表示禁止产生中断请求）：

```c
typedef enum
{
    ...LOGIC_LOW_OR_FALLING_EDGE = ..., // 低电平或者下降沿
    ...LOGIC_HIGH_OR_RISING_EDGE = ...  // 高电平或者上升沿
} GIO_IntTriggerEnable_t;
```

触发类型有两种：

```c
typedef enum
{
    GIO_INT_EDGE,   // 边沿触发
    GIO_INT_LOGIC   // 电平触发
} GIO_IntTriggerType_t;
```

- 例如将 GPIO 0 配置为上升沿触发中断

  ```c
  GIO_ConfigIntSource(GIO_GPIO_0,
    ...LOGIC_HIGH_OR_RISING_EDGE,
    GIO_INT_EDGE);
  ```
- 例如将 GPIO 0 配置为双沿触发中断

  ```c
  GIO_ConfigIntSource(GIO_GPIO_0,
    ...LOGIC_HIGH_OR_RISING_EDGE | ..._HIGH_OR_RISING_EDGE,
    GIO_INT_EDGE);
  ```
- 例如将 GPIO 0 配置为高电平触发

  ```c
  GIO_ConfigIntSource(GIO_GPIO_0,
    ...LOGIC_HIGH_OR_RISING_EDGE,
    GIO_INT_LOGIC);
  ```

### 7.2.5 处理中断状态 {#处理中断状态}

用 `GIO_GetIntStatus` 获取某个 GPIO 上的中断触发状态，返回非 0 值表示该 GPIO 上产生了中断请求；用 `GIO_GetAllIntStatus` 一次性获取所有 GPIO 的中断触发状态， 第 n 比特（第 0 比特为最低比特）对应 GPIO n 上的中断触发状态。

GPIO 产生中断后，需要消除中断状态方可再次触发。用 `GIO_ClearIntStatus` 消除某个 GPIO 上中断状态，用 `GIO_ClearAllIntStatus` 一次性清除所有 GPIO 上可能存在的中断触发状态。

### 7.2.6 输入去抖 {#输入去抖}

使用 `GIO_DebounceCtrl` 配置输入去抖参数，每个 GPIO 硬件模块使用单独的参数：

```c
void GIO_DebounceCtrl(
  uint8_t group_mask,     // 比特 0 为 1 时配置模块 0
                          // 比特 1 为 1 时配置模块 1
  uint8_t clk_pre_scale,
  GIO_DbClk_t clk         // 防抖时钟选择
  );
```

所谓去抖就是过滤掉长度小于 `(clk_pre_scale + 1)` 个防抖时钟周期的“毛刺”。

防抖时钟共有 2 种：

```c
typedef enum
{
    GIO_DB_CLK_32K,     // 使用 32k 时钟
    GIO_DB_CLK_PCLK,    // 使用快速 PCLK
} GIO_DbClk_t;
```

快速 PCLK 的具体频率参考 [SYSCTRL](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#ch-sysctrl)。

通过 `GIO_DebounceEn` 为单个 GPIO 使能去抖。例如要在 GPIO 0 上启用硬件去抖，忽略宽度小于 5/32768 \approx 0.15 (ms) 的“毛刺”：

```c
GIO_DebounceCtrl(1, 4, GIO_DB_CLK_32K);
GIO_DebounceEn(GIO_GPIO_0, 1);
```

### 7.2.7 低功耗保持状态 {#低功耗保持状态}

所有 GPIO 可以在芯片进入低功耗状态后保持状态。根据功能的不同，存在两种类型的 GPIO， 总结于表 [7.1](https://ingchips.github.io/drafts/pg_ing916/ch-gpio.html#tab:ch-gpio-func)。

*表 7.1: GPIO 的保持与唤醒功能*
| 序号 | 分类 | 低功耗保持 | DEEP 唤醒源 | DEEPER 唤醒源 |
| --- | --- | --- | --- | --- |
| 0 | A | Y | Y | Y |
| 1 | B | Y | Y |  |
| 2 | B | Y | Y |  |
| 3 | B | Y | Y |  |
| 4 | B | Y | Y |  |
| 5 | A | Y | Y | Y |
| 6 | A | Y | Y | Y |
| 7 | B | Y | Y |  |
| 8 | B | Y | Y |  |
| 9 | B | Y | Y |  |
| 10 | B | Y | Y |  |
| 11 | B | Y | Y |  |
| 12 | B | Y | Y |  |
| 13 | B | Y | Y |  |
| 14 | B | Y | Y |  |
| 15 | B | Y | Y |  |
| 16 | B | Y | Y |  |
| 17 | B | Y | Y |  |
| 18 | C |  |  |  |
| 19 | C |  |  |  |
| 20 | C |  |  |  |
| 21 | A | Y | Y | Y |
| 22 | A | Y | Y | Y |
| 23 | A | Y | Y | Y |
| 24 | B | Y | Y |  |
| 25 | B | Y | Y |  |
| 26 | C |  |  |  |
| 27 | C |  |  |  |
| 28 | C |  |  |  |
| 29 | B | Y | Y |  |
| 30 | B | Y | Y |  |
| 31 | B | Y | Y |  |
| 32 | B | Y | Y |  |
| 33 | B | Y | Y |  |
| 34 | B | Y | Y |  |
| 35 | B | Y | Y |  |
| 36 | A | Y | Y | Y |
| 37 | A | Y | Y | Y |
| 38 | B | Y |  |  |
| 39 | B | Y |  |  |
| 40 | B | Y |  |  |
| 41 | B | Y |  |  |

- 对于 A 型 GPIO

  使用 `GIO_EnableRetentionGroupA` 使能或禁用 A 型 GPIO 的低功耗状态保持功能。 使能状态保持功能时，IOMUX 与之相关的所有配置都被锁存，即使处于各种低功耗状态下。使能后， 对这些 GPIO 的配置再做修改无法生效。只有禁用保持功能后，才会生效。 使能后，低功耗状态下这些 GPIO 不掉电。

  ```c
  void GIO_EnableRetentionGroupA(uint8_t enable);
  ```
- 对于 B 型 GPIO

  使用 `GIO_EnableRetentionGroupB` 使能或禁用 B 型 GPIO 的低功耗状态保持功能。 使能状态保持功能时，与之相关的配置（输出值 —— 对于 IO 方向为输出的 GPIO、上下拉）都被锁存，即使处于各种低功耗状态下。 使能后，对这些 GPIO 的配置再做修改无法生效。只有禁用保持功能后，才会生效。

  说明：对于 IO 方向为输入的 GPIO，使能低功耗状态保持功能并进入低功耗状态后，确实可以保持其 IO 输入功能， 但是并不能产生实际效果（产生中断或者唤醒系统）。

  ```c
  void GIO_EnableRetentionGroupB(uint8_t enable);
  ```

  使用 `GIO_EnableHighZGroupB` 使能或禁用 B 型 GPIO 的低功耗高阻功能。使能该功能后， IO 方向为输出的 B 型 GPIO 处于高阻状态，对这些 GPIO 的配置再做修改无法生效。只有禁用保持功能后，才会生效。

  ```c
  void GIO_EnableHighZGroupB(uint8_t enable);
  ```

  这两个功能是互斥的，比如先后调用这个两个函数，先使能保持再使能高阻，则只有高阻功能生效。
- 对于 C 型 GPIO

  不支持低功耗保持。

这些功能只支持对所有 GPIO 同时使能或禁用，不能对单个 GPIO 分别控制。

### 7.2.8 睡眠唤醒源 {#睡眠唤醒源}

一部分 GPIO 支持作为低功耗状态的唤醒源：出现指定的电平信号时，将系统从低功耗状态下唤醒。 对于深度睡眠（DEEP Sleep），这些 GPIO （\{0..17, 21..25, 29..37\}）可作为唤醒源，包括所有的 A 型 GPIO 和部分 B 型 GPIO； 对于更深度的睡眠（DEEPER Sleep），所有的 A 型 GPIO 可作为唤醒源，参见表 [7.1](https://ingchips.github.io/drafts/pg_ing916/ch-gpio.html#tab:ch-gpio-func)。

- 深度睡眠唤醒源

  使用 `GIO_EnableDeepSleepWakeupSource` 使能（或停用）某个 GPIO 的唤醒功能。 其中，`io_index` 应该为支持该功能的 GPIO 的编号；`mode` 为唤醒方式；对于 A 型 GPIO， 忽略 `pull` 参数，其上下拉由 `PINCTRL_Pull` 控制。共支持以下 5 种唤醒方式：

  - `GIO_WAKEUP_MODE_LOW_LEVEL`：通过低电平唤醒；
  - `GIO_WAKEUP_MODE_HIGH_LEVEL`：通过高电平唤醒；
  - `GIO_WAKEUP_MODE_RISING_EDGE`：通过上升沿唤醒；
  - `GIO_WAKEUP_MODE_FALLING_EDGE`：通过下降沿唤醒；
  - `GIO_WAKEUP_MODE_ANY_EDGE`： 通过任意边沿唤醒，即上升沿或下降沿皆可。

  当使用电平唤醒时，电平与上下拉应该相互配合：高电平唤醒时，使用下拉；低电平唤醒时，使用上拉。 当使用边沿唤醒时，注意脉冲需要维持至少 100 \mu s。

  对于 B 型 GPIO，唤醒源与低功耗保持为两套独立的电路，因此： 1）上下拉独立于 [`PINCTRL_Pull`](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#ch-pinctrl-pull) ，而且一直生效 —— 无论是否处于低功耗状态， 所以，不要用 `PINCTRL_Pull` 配置相反的上下拉；2） 使能或禁用 B 型 GPIO 的低功耗保持或者高阻功能不影响这里的唤醒源设置；3）不要将某 IO 同时设为输出和唤醒源， 比如将某 IO 同时设为输出高电平、高电平唤醒，使能保持功能并进入低功耗时， 这个 IO 上保持电路所输出的高电平将传输到唤醒源电路并触发唤醒。

  ```c
  int GIO_EnableDeepSleepWakeupSource(
    GIO_Index_t io_index,     // GPIO 编号
    uint8_t enable,           // 使能(1)/禁用(0)
    uint8_t mode ,            // 触发方式
    pinctrl_pull_mode_t pull  // 上下拉配置
  );
  ```

  任意一个唤醒源检测到唤醒电平就会将系统从低功耗状态唤醒。
- 更深度睡眠唤醒源

  使用 `GIO_EnableDeeperSleepWakeupSourceGroupA` 使能（或停用）A 型 GPIO 的更深度睡眠唤醒功能。 其中，`level` 为触发电平，1 为高电平唤醒，0 为低电平唤醒。 使能后，所有 IO 方向为输入的 A 型 GPIO 都将作为唤醒源。任意一个唤醒源检测到唤醒电平就会将系统从低功耗状态唤醒。

  ```c
  void GIO_EnableDeeperSleepWakeupSourceGroupA(
    uint8_t enable,           // 使能(1)/禁用(0)
    uint8_t level             // 触发唤醒的电平
  );
  ```