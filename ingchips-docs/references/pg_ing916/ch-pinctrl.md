<!-- pg_ing916: 13 管脚管理（PINCTRL） -->

# 13 管脚管理（PINCTRL） {#ch-pinctrl}

## 13.1 功能概述 {#功能概述-6}

PINCTRL 模块管理芯片所有 IO 管脚的功能，包括外设 IO 的映射，上拉、下拉选择，输入模式控制， 输出驱动能力设置等。

每个 IO 管脚都可以配置为数字或[模拟模式](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#pinctrl-config-analog)，当配置为数字模式时，特性如下：

- 每个 IO 管脚可以映射多种不同功能的外设
- 每个 IO 管脚都支持上拉或下拉
- 每个 IO 管脚都支持施密特触发输入方式
- 每个 IO 管脚支持四种输出驱动能力

鉴于片内外设丰富、IO 管脚多，进行管脚全映射并不现实，为此，PINCTRL 尽量保证灵活性的前提下做了一定取舍、优化。 部分常用外设的输入、输出功能管脚可与 \{{0 .. 17, 21, 22, 31, 34, 35\}} 这 23 个常用 IO 之间任意连接（全映射）， 这部分常用外设功能管脚总结于表 [13.1](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-common-set)。 表 [13.2](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-mapping) 列出了其它外设功能管脚支持映射到哪些 IO 管脚上。 除此以外，所有 IO 管脚都可以配置为 GPIO 或者 DEBUG 模式。GPIO 模式的输入、输出方向由 `GIO_SetDirection` 控制。 DEBUG 模式为保留功能，具体功能暂不开放。

*表 13.1: 支持与常用 IO 全映射的常用功能管脚*
| 外设 | 功能管脚 |
| --- | --- |
| I2C | I2C0_SCL_I, I2C0_SCL_O, I2C0_SDA_I, I2C0_SDA_O, I2C1_SCL_I, I2C1_SCL_O, I2C1_SDA_I, I2C1_SDA_O |
| I2S | I2S_BCLK_I, I2S_BCLK_O, I2S_DIN, I2S_DOUT, I2S_LRCLK_I, I2S_LRCLK_O |
| IR | IR_DATIN, IR_DATOUT, IR_WAKEUP |
| PCAP | PCAP0_IN, PCAP1_IN, PCAP2_IN, PCAP3_IN, PCAP4_IN, PCAP5_IN |
| PDM | PDM_DMIC_IN, PDM_DMIC_MCLK |
| QDEC | QDEC_INDEX, QDEC_PHASEA, QDEC_PHASEB |
| SPI0 | SPI0_CLK_IN, SPI0_CLK_OUT, SPI0_CSN_IN, SPI0_CSN_OUT, SPI0_HOLD_IN, SPI0_HOLD_OUT, SPI0_MISO_IN, SPI0_MISO_OUT, SPI0_MOSI_IN, SPI0_MOSI_OUT, SPI0_WP_IN, SPI0_WP_OUT |
| SPI | SPI1_CLK_IN, SPI1_CLK_OUT, SPI1_CSN_IN, SPI1_CSN_OUT, SPI1_HOLD_IN, SPI1_HOLD_OUT, SPI1_MISO_IN, SPI1_MISO_OUT, SPI1_MOSI_IN, SPI1_MOSI_OUT, SPI1_WP_IN, SPI1_WP_OUT |
| SWD | SWDO, SW_TCK, SW_TMS |
| UART0 | UART0_CTS, UART0_RTS, UART0_RXD, UART0_TXD |
| UART1 | UART1_CTS, UART1_RTS, UART1_RXD, UART1_TXD |

*表 13.2: 其它外设功能管脚的映射关系*
| 外设功能管脚 | 可连接到的 IO 管脚 |
| --- | --- |
| KEY_IN_COL_0 | 0, 23 |
| KEY_IN_COL_1 | 1, 24 |
| KEY_IN_COL_2 | 2, 25 |
| KEY_IN_COL_3 | 3, 29 |
| KEY_IN_COL_4 | 4, 30 |
| KEY_IN_COL_5 | 5, 31 |
| KEY_IN_COL_6 | 6, 32 |
| KEY_IN_COL_7 | 7, 33 |
| KEY_IN_COL_8 | 8, 34 |
| KEY_IN_COL_9 | 9, 35 |
| KEY_IN_COL_10 | 10, 36 |
| KEY_IN_COL_11 | 11, 37 |
| KEY_IN_COL_12 | 12, 38 |
| KEY_IN_COL_13 | 13, 39 |
| KEY_IN_COL_14 | 14, 40 |
| KEY_IN_COL_15 | 15, 41 |
| KEY_IN_COL_16 | 16 |
| KEY_IN_COL_17 | 17 |
| KEY_IN_COL_18 | 21 |
| KEY_IN_COL_19 | 22 |
| KEY_OUT_ROW_0 | 0, 23 |
| KEY_OUT_ROW_1 | 1, 24 |
| KEY_OUT_ROW_2 | 2, 25 |
| KEY_OUT_ROW_3 | 3, 29 |
| KEY_OUT_ROW_4 | 4, 30 |
| KEY_OUT_ROW_5 | 5, 31 |
| KEY_OUT_ROW_6 | 6, 32 |
| KEY_OUT_ROW_7 | 7, 33 |
| KEY_OUT_ROW_8 | 8, 34 |
| KEY_OUT_ROW_9 | 9, 35 |
| KEY_OUT_ROW_10 | 10, 36 |
| KEY_OUT_ROW_11 | 11, 37 |
| KEY_OUT_ROW_12 | 12, 38 |
| KEY_OUT_ROW_13 | 13, 39 |
| KEY_OUT_ROW_14 | 14, 40 |
| KEY_OUT_ROW_15 | 15, 41 |
| KEY_OUT_ROW_16 | 16 |
| KEY_OUT_ROW_17 | 17 |
| KEY_OUT_ROW_18 | 21 |
| KEY_OUT_ROW_19 | 22 |
| ANT_SW0 | 0, 3, 6, 9, 12, 15, 21, 34 |
| ANT_SW1 | 1, 4, 7, 10, 13, 16, 22, 35 |
| ANT_SW2 | 2, 5, 8, 11, 14, 17, 31 |
| ANT_SW3 | 0, 3, 6, 9, 12, 15, 21, 34 |
| ANT_SW4 | 1, 4, 7, 10, 13, 16, 22, 35 |
| ANT_SW5 | 2, 5, 8, 11, 14, 17, 31 |
| ANT_SW6 | 0, 3, 6, 9, 12, 15, 21, 34 |
| ANT_SW7 | 1, 4, 7, 10, 13, 16, 22, 35 |
| PA_RXEN | 11, 12, 13, 14, 15, 16, 17, 34, 35 |
| PA_TXEN | 4, 5, 6, 7, 8, 9, 10, 34, 35 |
| TIMER0_PWM_0A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| TIMER0_PWM_0B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| TIMER0_PWM_1A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| TIMER0_PWM_1B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| TIMER1_PWM_0A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| TIMER1_PWM_0B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| TIMER1_PWM_1A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| TIMER1_PWM_1B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| TIMER2_PWM_0A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| TIMER2_PWM_0B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| TIMER2_PWM_1A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| TIMER2_PWM_1B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| PWM_0A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| PWM_0B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| PWM_1A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| PWM_1B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| PWM_2A | 0, 2, 4, 6, 8, 10, 12, 14, 16, 21, 31, 35 |
| PWM_2B | 1, 3, 5, 7, 9, 11, 13, 15, 17, 22, 34 |
| QDEC_EXT_IN_CLK | 3, 9 |
| QDEC_TIMER_EXT_IN1_A | 1, 7 |
| QDEC_TIMER_EXT_IN2_A | 2, 8 |
| QDEC_TIMER_EXT_IN2_B | 5, 11 |
| QDEC_TIMER_EXT_OUT0_A | 0, 6 |
| QDEC_TIMER_EXT_OUT1_A | 1, 7 |
| QDEC_TIMER_EXT_OUT2_A | 2, 8 |
| QDEC_TIMER_EXT_OUT0_B | 3, 9 |
| QDEC_TIMER_EXT_OUT1_B | 4, 10 |
| QDEC_TIMER_EXT_OUT2_B | 5, 11 |
| SPI0_CLK_IN | 19 |
| SPI0_CLK_OUT | 19 |
| SPI0_CSN_IN | 18 |
| SPI0_CSN_OUT | 18 |
| SPI0_HOLD_IN | 20 |
| SPI0_HOLD_OUT | 20 |
| SPI0_MISO_IN | 27 |
| SPI0_MISO_OUT | 27 |
| SPI0_MOSI_IN | 28 |
| SPI0_MOSI_OUT | 28 |
| SPI0_WP_IN | 26 |
| SPI0_WP_OUT | 26 |
| SPI2AHB_CS | 16 |
| SPI2AHB_DI | 17 |
| SPI2AHB_DO | 17 |
| SPI2AHB_SCLK | 15 |

## 13.2 使用说明 {#使用说明-6}

### 13.2.1 为外设配置 IO 管脚 {#为外设配置-io-管脚}

1. 将外设输出连接到 IO 管脚

   通过 `PINCTRL_SetPadMux` 将外设输出连接到 IO 管脚。 注意按照表 [13.1](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-common-set) 和 表 [13.2](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-mapping) 确认硬件是否支持。对于不支持的配置，显然无法生效，函数将返回非 0 值。

   ```c
   int PINCTRL_SetPadMux(
     const uint8_t io_pin_index, // IO 序号 (0 .. IO_PIN_NUMBER - 1)
     const io_source_t source    // IO 源
   );
   ```

   例如将 IO 管脚 10 配置为 GPIO 模式：

   `PINCTRL_SetPadMux(10, IO_SOURCE_GPIO);`
2. 将 IO 管脚连接到外设的输入

   对于有些外设的输入同样通过 `PINCTRL_SetPadMux` 配置。对于另一些输入， PINCTRL 为不同的外设分别提供了 API 用以配置输入。比如 UART 的数据输入 RXD 和用于硬件流控的 CTS，需要通过 `PINCTRL_SelUartIn` 配置 ：

   ```c
   int PINCTRL_SelUartIn(
     uart_port_t port,     // UART 序号
     uint8_t io_pin_rxd,   // 连接到 RXD 输入的 IO 管脚
     uint8_t io_pin_cts);  // 连接到 CTS 输入的 IO 管脚
   ```

   对于不需要配置的输入，可在对应的参数上填入值 `IO_NOT_A_PIN`。

   表 [13.3](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-sel-in) 罗列了为各外设提供的输入配置函数。

   *表 13.3: 各外设的输入配置函数*
   | 外设 | 配置函数 |
   | --- | --- |
   | KeyScan | `PINCTRL_SelKeyScanColIn` |
   | I2C | `PINCTRL_SelI2cIn` |
   | I2S | `PINCTRL_SelI2sIn` |
   | IR | `PINCTRL_SelIrIn` |
   | PDM | `PINCTRL_SelPdmIn` |
   | PCAP | `PINCTRL_SelPCAPIn` |
   | QDEC | `PINCTRL_SelQDECIn` |
   | SWD | `PINCTRL_SelSwIn` |
   | SPI | `PINCTRL_SelSpiIn` |
   | UART | `PINCTRL_SelUartIn` |
   | USB | `PINCTRL_SelUSB` |

### 13.2.2 配置上拉、下拉 {#ch-pinctrl-pull}

IO 管脚的上拉、下拉模式通过 `PINCTRL_Pull` 配置：

```c
void PINCTRL_Pull(
  const uint8_t io_pin_index,     // IO 管脚序号
  const pinctrl_pull_mode_t mode  // 模式
  );
```

表 [13.4](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-pull-default) 列出了各管脚默认的上下拉配置。

*表 13.4: 管脚上下拉默认配置*
| 管脚 | 默认配置 |
| --- | --- |
| 1 | 上拉 |
| 2 | 上拉 |
| 3 | 上拉 |
| 4 | 上拉 |
| 15 | 下拉 |
| 16 | 下拉 |
| 17 | 下拉 |
| 其它 | 禁用上下拉 |

### 13.2.3 配置驱动能力 {#配置驱动能力}

通过 `PINCTRL_SetDriveStrength` 配置 IO 管脚的驱动能力：

```c
void PINCTRL_SetDriveStrength(
  const uint8_t io_pin_index,
  const pinctrl_drive_strength_t strength);
```

默认驱动能力共分 4 档，分别为 2mA、4mA、8mA、12mA。除了 IO1 驱动能力默认为 12mA 之外， 其它管脚驱动能力默认 8mA。

### 13.2.4 配置天线切换控制管脚 {#配置天线切换控制管脚}

支持最多 8 个管脚用于天线切换控制，相应地，天线切换模板（switching pattern）内每个数字包含 8 个比特， 取值范围为 0..255。这 8 个比特可依次通过 `IO_SOURCE_ANT_SW0`、……、`IO_SOURCE_ANT_SW7` 选择。 例如，查表 [13.2](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-mapping) 可知管脚 0 能够映射为 ANT_SW0，即比特 0。 通过下面这行代码就可将管脚 0 映射为 ANT_SW0：

```c
PINCTRL_SetPadMux(0, IO_SOURCE_ANT_SW0);
```

通过函数 `PINCTRL_EnableAntSelPins` 可批量配置用于天线切换控制的管脚：

```c
int PINCTRL_EnableAntSelPins(
  int count,                // 数目
  const uint8_t *io_pins);  // 管脚数组
```

管脚数组 `io_pins` 里的第 n 个元素代表第 n 个比特所要映射的管脚。如果不需要为某个比特配置管脚，则在 `io_pins` 的对应位置填入 `IO_NOT_A_PIN`。比如，只选用第 0、第 2 等两个比特用作控制，分别映射到管脚 0 和 5：

```c
const uint8_t io_pins[] = {0, IO_NOT_A_PIN, 5};
PINCTRL_EnableAntSelPins(sizeof(io_pins), io_pins);
```

### 13.2.5 配置模拟模式 {#pinctrl-config-analog}

通过以下 3 步可将一个管脚配置为模拟模式：

1. 配置为 GPIO 模式；
2. 禁用上下拉；
3. 将 GPIO 配置为高阻态。

函数 `PINCTRL_EnableAnalog` 封装了以上步骤：

```c
void PINCTRL_EnableAnalog(const uint8_t io_index);
```

模拟模式适用于以下几种外设。

- [USB](https://ingchips.github.io/drafts/pg_ing916/ch-usb.html#ch-usb)

  函数 `PINCTRL_SelUSB()` 内部封装了 `PINCTRL_EnableAnalog`，开发者不需要再为 USB 管脚调用该函数配置模拟模式。
- [ADC](https://ingchips.github.io/drafts/pg_ing916/ch-adc.html#ch-adc)

  开发者需要调用该函数使能某管脚的 ADC 输入功能。支持 ADC 输入功能的管脚如表 [13.5](https://ingchips.github.io/drafts/pg_ing916/ch-pinctrl.html#tab:ch-pinctrl-adc) 所示。

  *表 13.5: 支持 ADC 输入的管脚*
  | 管脚 | 单端模式 | 差分模式 |
  | --- | --- | --- |
  | 7 | AIN 0 | AIN 0 P |
  | 8 | AIN 1 | AIN 0 N |
  | 9 | AIN 2 | AIN 1 P |
  | 10 | AIN 3 | AIN 1 N |
  | 11 | AIN 4 | AIN 2 P |
  | 12 | AIN 5 | AIN 2 N |
  | 13 | AIN 6 | AIN 3 P |
  | 14 | AIN 7 | AIN 3 N |
- 其它还有 [模拟比较器](https://ingchips.github.io/drafts/pg_ing916/ch-comparator.html#ch-comparator)，32k 晶体引脚等。