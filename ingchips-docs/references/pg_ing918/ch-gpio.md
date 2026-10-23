<!-- pg_ing918: 5 通用输入输出（GPIO） -->

# 5 通用输入输出（GPIO） {#ch-gpio}

## 5.1 功能概述 {#功能概述}

GPIO 模块常用于驱动 LED 或者其它指示器，控制片外设备，感知数字信号输入，检测信号边沿， 或者从低功耗状态唤醒系统。ING918XX 系列芯片内部支持最多 20 个 GPIO，通过 [PINCTRL](https://ingchips.github.io/drafts/pg_ing918/ch-pinctrl.html#ch-pinctrl) 可将 GPIO n 引出到芯片 IO 管脚 n。

特性：

- 每个 GPIO 都可单独配置为输入或输出
- 每个 GPIO 都可作为中断请求，中断触发方式支持边沿触发（上升、下降单沿触发，或者双沿触发） 和电平触发（高电平或低电平）

## 5.2 使用说明 {#使用说明}

### 5.2.1 设置 IO 方向 {#设置-io-方向}

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

### 5.2.2 读取输入 {#读取输入}

使用 `GIO_ReadValue` 读取某个 GPIO 当前输入的电平信号，例如读取 GPIO 0 的输入：

```c
uint8_t value = GIO_ReadValue(GIO_GPIO_0);
```

使用 `GIO_ReadAll` 可以同时读取所有 GPIO 当前输入的电平信号。其返回值的第 n 比特 （第 0 比特为最低比特）对应 GPIO n 的输入；如果 GPIO n 当前不支持输入，那么第 n 比特为 0：

```c
uint64_t GIO_ReadAll(void);
```

### 5.2.3 设置输出 {#设置输出}

使用 `GIO_WriteValue` 设置某个 GPIO 输出的电平信号，例如使 GPIO 0 输出高电平（1）：

```c
GIO_WriteValue(GIO_GPIO_0, 1);
```

### 5.2.4 配置中断请求 {#配置中断请求}

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

### 5.2.5 处理中断状态 {#处理中断状态}

在用 `platform_set_irq_callback` 注册好GPIO中断回调函数后，在中断里用 `GIO_GetIntStatus` 可获取某个 GPIO 上的中断触发状态，返回非 0 值表示该 GPIO 上产生了中断请求；用 `GIO_GetAllIntStatus` 一次性获取所有 GPIO 的中断触发状态， 第 n 比特（第 0 比特为最低比特）对应 GPIO n 上的中断触发状态。

GPIO 产生中断后，需要消除中断状态方可再次触发。用 `GIO_ClearIntStatus` 消除某个 GPIO 上中断状态，用 `GIO_ClearAllIntStatus` 一次性清除所有 GPIO 上可能存在的中断触发状态。