<!-- pg_ing918: 7 管脚管理（PINCTRL） -->

# 7 管脚管理（PINCTRL） {#ch-pinctrl}

## 7.1 功能概述 {#功能概述-2}

PINCTRL 模块管理芯片所有 IO 管脚的功能，包括外设 IO 的映射，上拉、下拉选择，输入模式控制， 输出驱动能力设置等。

IO管脚特性如下：

- 每个 IO 管脚可以映射多种不同功能的外设
- 每个 IO 管脚都支持上拉或下拉
- 每个 IO 管脚都支持施密特触发输入方式
- 每个 IO 管脚支持四种输出驱动能力

鉴于片内外设丰富、IO 管脚多，进行管脚全映射并不现实，为此，PINCTRL 尽量保证灵活性的前提下做了一定取舍、优化。 部分常用外设的输入、输出功能管脚可与 \{{0-19\}} 这 20 个常用 IO 之间任意连接（全映射）， 这部分常用外设功能管脚总结于表 [7.1](https://ingchips.github.io/drafts/pg_ing918/ch-pinctrl.html#tab:ch-pinctrl-common-set)。 表 [7.2](https://ingchips.github.io/drafts/pg_ing918/ch-pinctrl.html#tab:ch-pinctrl-mapping) 列出了其它外设功能管脚支持映射到哪些 IO 管脚上。

*表 7.1: 支持与常用 IO 全映射的常用功能管脚*
| 外设 | 功能管脚 |
| --- | --- |
| I2C0 | I2C0_SCL_O, I2C0_SDO |
| I2C1 | I2C1_SCL_O, I2C1_SDO |
| SPI0 | SPI0_CLK, SPI0_DO, SPI0_SSN |
| SPI1 | SPI1_CLK, SPI1_DO, SPI1_SSN |
| UART0 | UART0_TXD, UART0_RTS |
| UART1 | UART1_TXD, UART1_RTS |

*表 7.2: 其它外设功能管脚的映射关系*
| 外设功能管脚 | 可连接到的 IO 管脚 |
| --- | --- |
| PWM_0A | 0-11 |
| PWM_0B | 0-11 |
| PWM_1A | 0-11 |
| PWM_1B | 0-11 |
| PWM_2A | 0-11 |
| PWM_2B | 0-11 |
| PWM_3A | 0-11 |
| PWM_3B | 0-11 |
| PWM_4A | 0-11 |
| PWM_4B | 0-11 |
| PWM_5A | 0-11 |
| PWM_5B | 0-11 |

## 7.2 使用说明 {#使用说明-1}

### 7.2.1 为外设配置 IO 管脚 {#为外设配置-io-管脚}

1. 将外设输出连接到 IO 管脚

   通过 `PINCTRL_SetPadMux` 将外设输出连接到 IO 管脚。 注意按照表 [7.1](https://ingchips.github.io/drafts/pg_ing918/ch-pinctrl.html#tab:ch-pinctrl-common-set) 和 表 [7.2](https://ingchips.github.io/drafts/pg_ing918/ch-pinctrl.html#tab:ch-pinctrl-mapping) 确认硬件是否支持。对于不支持的配置，显然无法生效。

   ```c
   void PINCTRL_SetPadMux(
     const uint8_t io_pin_index, // IO 序号 (0..19)
     const io_source_t source    // IO 源
   );
   ```
2. 将 IO 管脚连接到外设的输入

   对于有些外设的输入同样通过 `PINCTRL_SetPadMux` 配置。对于另一些输入， PINCTRL 为不同的外设分别提供了 API 用以配置输入。比如对于 UART 用于硬件流控的 RXD，需要通过 `PINCTRL_SelUartRxdIn` 配置 ：

   ```c
   void PINCTRL_SelUartRxdIn(
       const uart_port_t port, //UART 序号
       const uint8_t io_pin_index)//连接到 RXD 输入的 IO 管脚
   ```

### 7.2.2 配置下拉、下拉 {#配置下拉下拉}

IO 管脚的上拉、下拉模式通过 `PINCTRL_Pull` 配置：

```c
void PINCTRL_Pull(
  const uint8_t io_pin_index,     // IO 管脚序号
  const pinctrl_pull_mode_t mode  // 模式
  );
```

### 7.2.3 配置驱动能力 {#配置驱动能力}

通过 `PINCTRL_SetDriveStrength` 配置 IO 管脚的驱动能力：

```c
void PINCTRL_SetDriveStrength(
  const uint8_t io_pin_index,
  const pinctrl_drive_strenght_t strenght);
```

### 7.2.4 配置速率 {#配置速率}

```c
void PINCTRL_SetSlewRate(
  const uint8_t io_pin_index,   //IO 管脚序号
  const pinctrl_slew_rate_t rate);  
```

### 7.2.5 IO口PWM参考代码 {#io口pwm参考代码}

```c
  #define LED1_PIN 10 //在GPIO10上输出
  #define LED1_PWM_CH 4 //映射到PWM_4
  #define  LED_FREQ     4000 //频率4K
  SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_APB_PWM));  //打开PWM时钟域
  PINCTRL_SetGeneralPadMode(LED1_PIN, IO_MODE_PWM, , LED1_PWM_CH, 0); //反向输出
  PWM_SetupSimple(LED1_PWM_CH, LED_FREQ, 10);
  PWM_Enable(LED1_PWM_CH,1);
```

### 7.2.6 IO口配置为UART参考代码 {#io口配置为uart参考代码}

```c
  #define PIN_COMM_RX GIO_GPIO_8
  #define PIN_COMM_TX GIO_GPIO_7
  SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_APB_UART1));
  config_uart(OSC_CLK_FREQ, 921600);

  PINCTRL_SetPadMux(PIN_COMM_RX, IO_SOURCE_GENERAL);
  PINCTRL_SelUartRxdIn(UART_PORT_1, PIN_COMM_RX);
  PINCTRL_SetPadMux(PIN_COMM_TX, IO_SOURCE_UART1_TXD);
```

### 7.2.7 IO口配置为SPI参考代码 {#io口配置为spi参考代码}

```c
{
  #define SPI_MIC_CLK         GIO_GPIO_13
  #define SPI_MIC_MOSI        GIO_GPIO_16
  #define SPI_MIC_MISO        GIO_GPIO_17
  #define SPI_MIC_CS          GIO_GPIO_8

  SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_AHB_SPI0)
                              | (1 << SYSCTRL_ClkGate_APB_PinCtrl)
                              | (1 << SYSCTRL_ClkGate_APB_GPIO));

  PINCTRL_Pull(SPI_MIC_MOSI, PINCTRL_PULL_DOWN);
  PINCTRL_Pull(SPI_MIC_CLK, PINCTRL_PULL_UP);
  PINCTRL_Pull(SPI_MIC_CS, PINCTRL_PULL_UP);
  PINCTRL_Pull(SPI_MIC_MISO, PINCTRL_PULL_UP);

  PINCTRL_SetDriveStrength(SPI_MIC_MOSI, PINCTRL_DRIVE_12mA);
  PINCTRL_SetDriveStrength(SPI_MIC_CLK, PINCTRL_DRIVE_12mA);
  PINCTRL_SetDriveStrength(SPI_MIC_CS, PINCTRL_DRIVE_12mA);

  PINCTRL_SetPadMux(SPI_MIC_MOSI, IO_SOURCE_SPI0_DO);
  PINCTRL_SetPadMux(SPI_MIC_CLK, IO_SOURCE_SPI0_CLK);

  PINCTRL_SetPadMux(SPI_MIC_CS, IO_SOURCE_SPI0_SSN);
  PINCTRL_SelSpiDiIn(SPI_PORT_0, SPI_MIC_MISO);

  apSSP_DeviceDisable(AHB_SSP0);
  SPI_Init(AHB_SSP0);
}
```

### 7.2.8 IO口配置为I2C参考代码 {#io口配置为i2c参考代码}

```c
SYSCTRL_ClearClkGateMulti(  (1 << SYSCTRL_ClkGate_APB_I2C0)
                              | (1 << SYSCTRL_ClkGate_APB_PinCtrl));
PINCTRL_SetPadMux(10, IO_SOURCE_I2C0_SCL_OUT);
PINCTRL_SetPadMux(11, IO_SOURCE_I2C0_SDA_OUT);
```