<!-- pg_ing916: 19 系统控制（SYSCTRL） -->

# 19 系统控制（SYSCTRL） {#ch-sysctrl}

## 19.1 功能概述 {#功能概述-8}

SYSCTRL 负责管理、控制各种片上外设，主要功能有：

- 外设的复位
- 外设的时钟管理，包括时钟源、频率设置、门控等
- DMA 规划
- 其它功能

### 19.1.1 外设标识 {#外设标识}

SYSCTRL 为外设定义了几种不同的标识。最常见的一种标识为：

```c
typedef enum
{
    SYSCTRL_ITEM_APB_GPIO0     ,
    SYSCTRL_ITEM_APB_GPIO1     ,
    // ...
    SYSCTRL_ITEM_NUMBER,
} SYSCTRL_Item;
```

这种标识用于外设的复位、时钟门控等。`SYSCTRL_ResetItem` 和 `SYSCTRL_ClkGateItem` 是 `SYSCTRL_Item` 的两个别名。

下面这种标识用于 DMA 规划：

```c
typedef enum
{
    SYSCTRL_DMA_UART0_RX = 0,
    SYSCTRL_DMA_UART1_RX = 1,
    //...
} SYSCTRL_DMA;
```

### 19.1.2 时钟树 {#时钟树}

从源头看，共有 4 个时钟源：

1. 内部 32KiHz RC 时钟；
2. 外部 32768Hz 晶体；
3. 内部高速 RC 时钟（8M/16M/24M/32M/48M 可调）；
4. 外部 24MHz 晶体。

从 4 个时钟源出发，得到两组时钟：

1. 32KiHz 时钟（*clk_32k*）

   32k 时钟有两个来源：内部 32KiHz RC 电路，外部 32768Hz 晶体。
2. 慢时钟

   慢时钟有两个来源：内部高速 RC 时钟，外部 24MHz 晶体。

   BLE 子系统中射频相关的部分固定使用外部 24MHz 晶体提供的时钟。

之后，

1. PLL 输出（*clk_pll*）

   *clk_pll* 的频率 f_{pll} 可配置，受 div_{pre}（前置分频）、loop（环路分频）和 div_{output}（输出分频）等 3 个参数控制：

   f_{vco}=\frac{f_{in}\times loop}{div_{pre}}

   f_{pll}=\frac{f_{vco}}{div_{output}}

   这里，f_{in} 即慢时钟。要求 f_{vco} \in [60,600]MHz， f_{in}/div_{pre} \in [2,24]MHz。
2. *sclk_fast* 与 *sclk_slow*

   *clk_pll* 经过门控后的时钟称为 *sclk_fast*，慢时钟经过门控后称为 *sclk_slow*。
3. *hclk*

   *sclk_fast* 经过分频后得到 *hclk*。下列外设（包括 CPU）固定使用这个时钟[4](#fn4)：

   - DMA
   - 片内 Flash
   - QSPI
   - USB[5](#fn5)
   - 其它内部模块如 AES、Cache 等

   *hclk* 经过分频后得到 *pclk*。*pclk* 主要用于硬件内部接口。
4. *sclk_slow* 的进一步分频

   *sclk_slow* 经过若干独立的分频器得到以下多种时钟：

   - *sclk_slow_pwm_div*：专供 PWM 选择使用
   - *sclk_slow_timer_div*：供 TIMER0、TIMER1、TIMER2 选择使用
   - *sclk_slow_ks_div*：专供 KeyScan 选择使用
   - *sclk_slow_adc_div*：供 EFUSE、ADC、IR 选择使用
   - *sclk_slow_pdm_div*：专供 PDM 选择使用
5. *sclk_fast* 的进一步分频：

   *sclk_fast* 经过若干独立的分频器得到以下多种时钟：

   - *sclk_fast_i2s_div*：专供 I2S 选择使用
   - *sclk_fast_qspi_div*：专供 SPI0 选择使用
   - *sclk_fast_flash_div*：专供片内 Flash 选择使用
   - *sclk_fast_usb_div*：专供 USB 使用

各硬件外设可配置的时钟源汇总如表 [19.1](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-tab-clk)。

*表 19.1: 各硬件外设的时钟源*
| 外设 | 时钟源 |
| --- | --- |
| GPIO0、GPIO1 | 选择 *sclk_slow* 或者 *clk_32k* |
| TMR0、TMR1、TMR2 | 独立配置 *sclk_slow_timer_div* 或者 *clk_32k* |
| WDT | *clk_32k* |
| PWM | *sclk_slow_pwm_div* 或者 *clk_32k* |
| PDM | *sclk_slow_pdm_div* |
| QDEC | 对 *hclk* 或者 *sclk_slow* |
| KeyScan | *sclk_slow_ks_div* 或者 *clk_32k* |
| IR、ADC、EFUSE | 独立配置 *sclk_slow_adc_div* 或者 *sclk_slow* |
| DMA | *hclk* |
| SPI0 | *sclk_fast_qspi_div* 或者 *sclk_slow* |
| I2S | *sclk_fast_i2s_div* 或者 *sclk_slow* |
| UART0、UART1、SPI1 | 独立配置 *hclk* 或者 *sclk_slow* |
| I2C0、I2C1 | *pclk* |

### 19.1.3 DMA 规划 {#dma-规划}

由于 [DMA](https://ingchips.github.io/drafts/pg_ing916/ch-dma.html#ch-dma) 支持的硬件握手信号只有 16 种，无法同时支持所有外设。 因此需要事先确定将要的外设握手信号，并通过 `SYSCTRL_SelectUsedDmaItems` 接口声明。

一个外设可能具备一个以上的握手信号，需要注意区分。比如 UART0 有两个握手信号 UART0_RX 和 UART0_TX，分别用于触发 DMA 发送请求（通过 DMA 传输接收到的数据）和读取请求（向 DMA 请 求新的待发送数据）。外设握手信号定义在 `SYSCTRL_DMA` 内：

```c
typedef enum
{
    SYSCTRL_DMA_UART0_RX = 0,
    SYSCTRL_DMA_UART1_RX = 1,
    // ...
} SYSCTRL_DMA;
```

## 19.2 使用说明 {#使用说明-9}

### 19.2.1 外设复位 {#外设复位}

通过 `SYSCTRL_ResetBlock` 复位外设，通过 `SYSCTRL_ReleaseBlock` 释放复位。

```c
void SYSCTRL_ResetBlock(SYSCTRL_ResetItem item);
void SYSCTRL_ReleaseBlock(SYSCTRL_ResetItem item);
```

### 19.2.2 时钟门控 {#时钟门控}

通过 `SYSCTRL_SetClkGate` 设置门控（即关闭时钟），通过 `SYSCTRL_ClearClkGate` 消除门控（即恢复时钟）。

```c
void SYSCTRL_SetClkGate(SYSCTRL_ClkGateItem item);
void SYSCTRL_ClearClkGate(SYSCTRL_ClkGateItem item);
```

`SYSCTRL_SetClkGateMulti` 和 `SYSCTRL_ClearClkGateMulti` 可以同时控制多个外设的门控。 `items` 参数里的各个比特与 `SYSCTRL_ClkGateItem` 里的各个外设一一对应。

```c
void SYSCTRL_SetClkGateMulti(uint32_t items);
void SYSCTRL_ClearClkGateMulti(uint32_t items);
```

### 19.2.3 时钟配置 {#时钟配置-3}

举例如下。

1. *clk_pll* 与 *hclk*

   使用 `SYSCTRL_ConfigPLLClk` 配置 *clk_pll*：

   ```c
   int SYSCTRL_ConfigPLLClk(
       uint32_t div_pre,   // 前置分频
       uint32_t loop,      // 环路分频
       uint32_t div_output // 输出分频
   );
   ```

   例如，假设慢时钟配置为 24MHz，下面的代码将 *hclk* 配置为 112MHz 并读取到变量：

   ```c
   SYSCTRL_ConfigPLLClk(5, 70, 1);
   SYSCTRL_SelectHClk(SYSCTRL_CLK_PLL_DIV_3);
   uint32_t SystemCoreClock = SYSCTRL_GetHClk();
   ```
2. 为硬件 I2S 配置时钟

   使用 `SYSCTRL_SelectI2sClk` 为 I2S 配置时钟：

   ```c
   void SYSCTRL_SelectI2sClk(SYSCTRL_ClkMode mode);
   ```

   `SYSCTRL_ClkMode` 的定义为：

   ```c
   typedef enum
   {
       SYSCTRL_CLK_SLOW,             // 使用 sclk_slow
       SYSCTRL_CLK_32k = ...,        // 使用 32KiHz 时钟
       SYSCTRL_CLK_HCLK,             // 使用 hclk
       SYSCTRL_CLK_ADC_DIV = ...,    // 使用 sclk_slow_adc_div
       SYSCTRL_CLK_PLL_DIV_1 = ...,  // 对 sclk_fast 分频
       SYSCTRL_CLK_SLOW_DIV_1 = ..., // 对 sclk_slow 分配
   } SYSCTRL_ClkMode;
   ```

   根据表 [19.1](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-tab-clk) 可知，I2S 可使用 *slk_slow*：

   ```c
   SYSCTRL_SelectI2sClk(SYSCTRL_CLK_SLOW);
   ```

   或者独占一个分频器，对 *sclk_fast* 分频得到 *sclk_fast_i2s_div*，比如使用 *sclk_fast* 的 5 分频：

   ```c
   SYSCTRL_SelectI2sClk(SYSCTRL_CLK_PLL_DIV_5);
   ```
3. 读取时钟频率

   使用 `SYSCTRL_GetClk` 读取指定外设的时钟频率：

   ```c
   uint32_t SYSCTRL_GetClk(SYSCTRL_Item item);
   ```

   比如，

   ```c
   // I2S 使用 PLL 的 5 分频
   SYSCTRL_SelectI2sClk(SYSCTRL_CLK_PLL_DIV_5);
   // freq = sclk_fast 的频率 / 5
   uint32_t freq = SYSCTRL_GetClk(SYSCTRL_ITEM_APB_I2S);
   ```
4. 降低频率以节省功耗

   降低系统各时钟的频率可以显著降低动态功耗。相关函数有：

   - `SYSCTRL_SelectHClk`：选择 *hclk*
   - `SYSCTRL_SelectFlashClk`：选择内部 Flash 时钟
   - `SYSCTRL_SelectSlowClk`：选择慢时钟
   - `SYSCTRL_EnablePLL`：开关 PLL
5. 配置用于慢时钟的高速 RC 时钟

   通过 `SYSCTRL_EnableSlowRC` 可以使能并配置内部高速 RC 时钟的频率模式：

   ```c
   void SYSCTRL_EnableSlowRC(
       uint8_t enable,             // 使能或禁用
       SYSCTRL_SlowRCClkMode mode  // 频率模式
   );
   ```

   频率模式为：

   ```c
   typedef enum
   {
       SYSCTRL_SLOW_RC_8M = ...,
       SYSCTRL_SLOW_RC_16M = ...,
       SYSCTRL_SLOW_RC_24M = ...,
       SYSCTRL_SLOW_RC_32M = ...,
       SYSCTRL_SLOW_RC_48M = ...,
   } SYSCTRL_SlowRCClkMode;
   ```

   由于内部（芯片之间）、外部环境（温度）存在微小差异或变化，所以这个 RC 时钟的频率或存在一定误差， 需要进行调谐以尽量接近标称值。通过 `SYSCTRL_AutoTuneSlowRC` 可自动完成调谐[6](#fn6)：

   ```c
   uint32_t SYSCTRL_AutoTuneSlowRC(void);
   ```

   这个函数返回的数据为调谐参数。如果认为有必要[7](#fn7)，可以把此参数储存起来，如果系统重启， 可通过 `SYSCTRL_TuneSlowRC` 直接写入参数调谐频率。

**温馨提示**：

- 关闭 PLL 时，务必先将 CPU、Flash 时钟切换至慢时钟；
- 修改慢时钟配置时，需要保证 PLL 的输出、CPU 时钟等在支持的频率内；
- 推荐使用 SDK 提供的工具生成时钟配置代码，规避错误配置。

### 19.2.4 DMA 规划 {#dma-规划-1}

使用 `SYSCTRL_SelectUsedDmaItems` 配置要使用的 DMA 握手信号：

```c
int SYSCTRL_SelectUsedDmaItems(
  uint32_t items // 各比特与 SYSCTRL_DMA 一一对应
  );
```

使用 `SYSCTRL_GetDmaId` 可获取为某外设握手信号的 DMA 信号 ID，如果返回 -1， 说明没有规划该外设握手信号[8](#fn8)：

```c
int SYSCTRL_GetDmaId(SYSCTRL_DMA item);
```

### 19.2.5 电源相关 {#电源相关}

#### 19.2.5.1 内核电压 {#内核电压}

使用 `SYSCTRL_SetLDOOutput` 配置内核 LDO 的输出电压（默认 1.200V）：

```c
void SYSCTRL_SetLDOOutput(int level);
```

其中 `level` 的表示方式为 `SYSCTRL_LDO_OUTPUT_CORE_1V000`、……、 `SYSCTRL_LDO_OUTPUT_CORE_1V300`，对应的电压范围是 [1.000 V, 1.300 V]，以 20mV 步进。 此配置在低功耗模式下不会丢失。

#### 19.2.5.2 内置 Flash 电压 {#ch-sysctrl-flash-power}

使用 `SYSCTRL_SetLDOOutputFlash` 配置内部 Flash LDO 的输出电压（默认 2.100V）：

```c
void SYSCTRL_SetLDOOutputFlash(int level);
```

其中 `level` 的表示方式为 `SYSCTRL_LDO_OUTPUT_FLASH_2V100`、……、 `SYSCTRL_LDO_OUTPUT_FLASH_3V100`，对应的电压范围是 [2.100 V, 3.100 V]，以 100mV 步进。 此配置在低功耗模式下不会丢失。

### 19.2.6 唤醒后的时钟配置 {#唤醒后的时钟配置}

ROM 内的启动程序包含一个时钟配置程序，当系统初始上电或者从低功耗状态唤醒时， 这个程序就按照预定参数配置几个关键时钟及看门狗。

默认情况下，这个时钟配置程序是打开的，所使用的预定参数如下：

- PLL：打开，`div_pre`、`loop`、`div_output` 分别为 5、70、1；
- *hclk*：*clk_pll* 3 分频；
- 片内 Flash 时钟：*clk_pll* 2 分频；
- 看门狗：不使能。

由于初始上电或者唤醒后，慢时钟来自外部 24MHz 晶体， 可计算出上述几个时钟的频率如表 [19.2](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-def-clocks)。

*表 19.2: 默认参数对应的时钟频率*
| 时钟 | 频率（MHz） |
| --- | --- |
| PLL | 336 |
| *hclk* | 112 |
| 片内 Flash | 168 |

通过以下两个函数向这个程序传递参数：

1. 使能这个程序并设置参数

   ```c
   void SYSCTRL_EnableConfigClocksAfterWakeup(
       uint8_t enable_pll,         // 是否使能 PLL
       uint8_t pll_loop,           // PLL loop
       SYSCTRL_ClkMode hclk,       // hclk
       SYSCTRL_ClkMode flash_clk,  // 片内 Flash 时钟
       uint8_t enable_watchdog);   // 是否使能看门狗
   ```

   如果使能看门狗，系统唤醒后，时钟配置程序将其配置为 4.5s 后触发超时、复位系统。
2. 禁用这个程序

   ```c
   void SYSCTRL_DisableConfigClocksAfterWakeup(void);
   ```

   如果禁用这个程序，系统唤醒后几个时钟的频率见表 [19.3](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-clocks-disabled)。

   *表 19.3: 禁用时钟配置程序时重新唤醒后几个关键时钟的频率*
   | 时钟 | 频率（MHz） |
   | --- | --- |
   | PLL | 384 |
   | *hclk* | 24 |
   | 片内 Flash | 24 |

### 19.2.7 RAM 相关 {#ram-相关}

SoC 内部包含多个内存块，根据用途可分为：仅供 CPU 使用的 SYS RAM，CPU 和蓝牙 Modem 皆可使用的 SHARE RAM 以及高速缓存（Cache）。部分内存块既可以作为 SYS RAM 也可以作为 SHARE RAM（见表 [19.4](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-remapped-ram)）， 在不同的软件包内将被配置为不同用途。

*表 19.4: 可作为 SYS/SHARE RAM 的内存块*
| 名称 | 大小 (KiB) | 配置为 SYS RAM 时的地址范围 | 配置为 SHARE RAM 时的地址范围 | 备注 |
| --- | --- | --- | --- | --- |
| SYS_MEM_BLOCK_0 | 16 | 0x20000000 ~ 0x20003FFF | 不支持 | 不可关闭 |
| SYS_MEM_BLOCK_1 | 16 | 0x20004000 ~ 0x20007FFF | 0x40128000 ~ 0x4012BFFF |  |
| REMAPPABLE_BLOCK_0 | 16 | 0x20008000 ~ 0x2000BFFF | 0x40124000 ~ 0x40127FFF |  |
| REMAPPABLE_BLOCK_1 | 8 | 0x2000C000 ~ 0x2000DFFF | 0x40122000 ~ 0x40123FFF |  |
| SHARE_MEM_BLOCK_0 | 8 | 不支持 | 0x40120000 ~ 0x40121FFF |  |

在 *noos_mini*, *mini* 软件包共配置 56 KiB SYS RAM，8 KiB SHARE RAM； 在其它软件包里，SYS、SHARE RAM 各 32 KiB。详见表 [19.5](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-bundle-mem)。 注意，虽然 SYS_MEM_BLOCK_1 也可用作 SHARE RAM，但是在所有的软件包里它总是被用作 SYS RAM。

*表 19.5: 各软件包里的 SYS/SHARE RAM 配置*
| 名称 | SYS RAM |  | SHARE RAM |  |
| --- | --- | --- | --- | --- |
|  | 地址范围 | 包含的内存块 | 地址范围 | 包含的内存块 |
| *mini*, *noos_mini* | 0x20000000 ~ 0x2000DFFF | SYS_MEM_BLOCK_0 SYS_MEM_BLOCK_1 REMAPPABLE_BLOCK_0 REMAPPABLE_BLOCK_1 | 0x40120000 ~ 0x40121FFF | SHARE_MEM_BLOCK_0 |
| 其它 | 0x20000000 ~ 0x20007FFF | SYS_MEM_BLOCK_0 SYS_MEM_BLOCK_1 | 0x40120000 ~ 0x40127FFF | SHARE_MEM_BLOCK_0 REMAPPABLE_BLOCK_0 REMAPPABLE_BLOCK_1 |

表 [19.4](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-remapped-ram) 中的内存块支持低功耗数据保持。 所有这些内存块默认都是开启的，部分内存块可关闭以节省功耗。如果程序中实际用到的 SYS RAM 较少，可通过 `SYSCTRL_SelectMemoryBlocks` 选择所要使用的内存块，并关闭不使用的内存块：

```c
void SYSCTRL_SelectMemoryBlocks(
    uint32_t block_map);
```

例如在一个使用 *mini* 软件包的程序里，如果确认只需要 32 KiB 的 SYS RAM，那么为了降低功耗，可关闭 REMAPPABLE_BLOCK_0 和 REMAPPABLE_BLOCK_1，保留其它内存块：

```c
SYSCTRL_SelectMemoryBlocks(
    SYSCTRL_SYS_MEM_BLOCK_0 | SYSCTRL_SYS_MEM_BLOCK_1 |
    SYSCTRL_SHARE_MEM_BLOCK_0);
```

另有 2 个内存块可配置为 SYS RAM 或者高速缓存，其配置可通过 `SYSCTRL_CacheControl` 动态修改。 将其映射为 SYS RAM 后，可按照表 [19.6](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#tab:ch-sysctrl-cache-memory-blocks) 中的地址访问。

*表 19.6: 可用作高速缓存的内存块*
| 名称 | 大小 (KiB) | 配置为 SYS RAM 时的地址范围 |
| --- | --- | --- |
| D-Cache-M | 8 | 0x2000E000~0x2000FFFF |
| I-Cache-M | 8 | 0x20010000~0x20011FFF |

这两个内存块都默认处于 Cache 模式。当需要更多的 RAM 时，通过 `SYSCTRL_CacheControl` 可将这两块内存映射为普通 RAM：

```c
void SYSCTRL_CacheControl(
    SYSCTRL_CacheMemCtrl i_cache,
    SYSCTRL_CacheMemCtrl d_cache
);
```

`SYSCTRL_CacheMemCtrl` 包含两个值，对应 Cache 模式和 SYS MEM 模式：

```c
typedef enum
{
    SYSCTRL_MEM_BLOCK_AS_CACHE = 0,
    SYSCTRL_MEM_BLOCK_AS_SYS_MEM = 1,
} SYSCTRL_CacheMemCtrl;
```

**务必注意**：

1. 从低功耗状态唤醒时，这两个内存块都将恢复默认值 `AS_CACHE`；
2. 低功耗状态时，这两个内存块里的数据（无论处于哪种模式）都会丢失；
3. 映射为普通 RAM 后，系统缺少高速缓存，性能有可能明显下降。

---

1. <a id="fn4"></a>每个外设可单独对 *hclk* 门控。[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#fnref4)
2. <a id="fn5"></a>仅高速时钟。[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#fnref5)
3. <a id="fn6"></a>以 24MHz 晶体为参考。[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#fnref6)
4. <a id="fn7"></a>比如认为 `SYSCTRL_AutoTuneSlowRC` 耗时过长。[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#fnref7)
5. <a id="fn8"></a>`SYSCTRL_SelectUsedDmaItems` 的 `items` 参数里对应的比特为 0[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#fnref8)