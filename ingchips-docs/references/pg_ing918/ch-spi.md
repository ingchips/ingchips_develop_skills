<!-- pg_ing918: 10 SPI功能概述 -->

# 10 SPI功能概述 {#ch-spi}

- 两个SPI模块
- 只支持SPI主模式
- 独立的RX&TX FIFO，大小为8*16bit
- 独立可屏蔽中断
- 不支持DMA

## 10.1 SPI使用说明 {#spi使用说明}

SPI Master有两种使用方式可以选择：

- 方法1：以blocking的方式操作SPI（读写操作完成后API才返回），针对SPI Master读取外设的单一场景
- 方法2：使用SPI中断操作SPI，需要在中断中操作读写的数据

### 10.1.1 时钟以及IO配置 {#时钟以及io配置}

使用模块之前，需要打开相应的时钟，并且配置IO，

1. IO选择，并非所有IO都可以映射成SPI，请查看对应datasheet获取可用IO。
2. 通过`SYSCTRL_ClearClkGateMulti`打开SPI时钟，例如SPI0则需要打开`SYSCTRL_ClkGate_AHB_SPI0`。
3. 配置IO的输入功能`PINCTRL_SelSpiDiIn`，没有使用到的IO可以使用IO_NOT_A_PIN替代。
4. 使用`PINCTRL_SetPadMux`配置IO的输出功能。
5. 打开SPI中断`platform_set_irq_callback`。

以下示例可以将指定IO映射成SPI引脚：

```c
#define SPI_MIC_CLK         GIO_GPIO_10
#define SPI_MIC_CS          GIO_GPIO_11
#define SPI_MIC_MOSI        GIO_GPIO_12
#define SPI_MIC_MISO        GIO_GPIO_13

static void setup_peripherals_spi_pin(void)
{
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_AHB_SPI0)
                            | (1 << SYSCTRL_ClkGate_APB_PinCtrl));

    PINCTRL_SetPadMux(SPI_MIC_CLK, IO_SOURCE_SPI0_CLK);
    PINCTRL_SetPadMux(SPI_MIC_CS, IO_SOURCE_SPI0_SSN);
    PINCTRL_SetPadMux(SPI_MIC_MOSI, IO_SOURCE_SPI0_DO);
    PINCTRL_SelSpiDiIn(SPI_PORT_0, SPI_MIC_MISO);
}
```

### 10.1.2 模块初始化 {#模块初始化}

模块的初始化通过`apSSP_DeviceParametersSet`和结构体`apSSP_sDeviceControlBlock`实现，结构体各个参数为：

- `ClockPrescale`：时钟速率预分频器，SSP模块时钟频率的计算公式为：sspclkout = sspclk/(ClockPrescale*(ClockRate+1))。
- `ClockRate`：时钟速率除数，必须是一个2~254之间的偶数。
- `eSCLKPhase`：上升沿还是下降沿采样，参考`apSSP_eSCLKPhase`，仅适用于Motorola 数据帧格式。
- `eSCLKPolarity`：时钟默认是低电平还是高电平，参考`apSSP_xSCLKPolarity`，仅适用于Motorola 数据帧格式。
- `eFrameFormat`：指定数据帧格式，参考`apSSP_eFrameFormat`。
- `eDataSize`：每个传输单位的bit个数，参考`apSSP_xDataSize`。
- `eLoopBackMode`：是否启用Loop back模式，参考`apSSP_eLoopBackMode`。
- `eMasterSlaveMode`：选择是Master还是Slave模式，参考`apSSP_eMasterSlaveMode`。
- `eSlaveOutput`：指定slave output模式，参考`apSSP_eSlaveOutput`。

具体使用请参考`编程指南`

### 10.1.3 中断配置 {#中断配置}

#### 10.1.3.1 处理中断状态 {#处理中断状态-1}

用`apSSP_GetIntRawStatus`获取某个SSP上的中断触发状态，返回非0表示该SSP上产生了中断请求。

SSP产生中断后，需要消除中断状态方可再次触发。用apSSP_ClearInt消除某个SSP上的中断状态，参数bits为需要清除的中断状态

示例：

在中断回调中，获取SSP0的中断状态，并消除

```c
uint32_t spi_irq_cb(void *user_data)
{
    uint32_t status = apSSP_GetIntRawStatus(AHB_SSP0);
    apSSP_ClearInt(AHB_SSP0, status);

    return 0;
}
```

#### 10.1.3.2 使能接收中断 {#使能接收中断}

使用`apSSP_DeviceReceiveEnable`使能接收中断

```c
void apSSP_DeviceReceiveEnable(
    SSP_TypeDef * SSP_Ptr
    );
```

#### 10.1.3.3 禁用接收中断 {#禁用接收中断}

使用`apSSP_DeviceDisable`禁用接收中断

```c
void apSSP_DeviceDisable(
    SSP_TypeDef * SSP_Ptr
    );
```

#### 10.1.3.4 使能SPI接收Overrun中断 {#使能spi接收overrun中断}

使用`apSSP_DeviceReceiveOverrunEnable`使能Overrun中断

```c
void apSSP_DeviceReceiveOverrunEnable(
    SSP_TypeDef * SSP_Ptr
    );
```

#### 10.1.3.5 使能发送中断 {#使能发送中断}

使用`apSSP_DeviceTransmitEnable`使能发送中断

```c
void apSSP_DeviceTransmitEnable(
    SSP_TypeDef * SSP_Ptr
    );
```

#### 10.1.3.6 禁用发送中断 {#禁用发送中断}

使用`apSSP_DeviceTransmitDisable`禁用发送中断

```c
void apSSP_DeviceTransmitDisable(
    SSP_TypeDef * SSP_Ptr
    );
```

### 10.1.4 发送数据 {#发送数据}

使用`apSSP_WriteFIFO`发送数据

```c
void apSSP_WriteFIFO(
    SSP_TypeDef * SSP_Ptr, uint16_t data
    );
```

### 10.1.5 接收数据 {#接收数据}

使用`apSSP_ReadFIFO`接收数据

```c
uint16_t apSSP_ReadFIFO(
    SSP_TypeDef * SSP_Ptr
    );
```

### 10.1.6 查询TX/RX FIFO状态 {#查询txrx-fifo状态}

使用以下函数查看TX/RX FIFO状态

```c
uint8_t apSSP_RxFifoFull(SSP_TypeDef * SSP_Ptr);

uint8_t apSSP_RxFifoNotEmpty(SSP_TypeDef * SSP_Ptr);

uint8_t apSSP_TxFifoNotFull(SSP_TypeDef * SSP_Ptr);

uint8_t apSSP_TxFifoEmpty(SSP_TypeDef * SSP_Ptr);
```

### 10.1.7 SSP查忙 {#ssp查忙}

使用`apSSP_DeviceBusyGet`函数查忙，可用于blocking的写法

```c
uint8_t apSSP_DeviceBusyGet(
    SSP_TypeDef * SSP_Ptr
    );
```

示例，同时读写时发送数据并接收数据：

```c
/* Exchange a byte */
static uint8_t xchg_spi (
    uint8_t dat /* Data to send */
)
{
    apSSP_WriteFIFO(AHB_SSP0, dat
    while (apSSP_DeviceBusyGet(AHB_SSP0)) ;
    return (uint8_t)apSSP_ReadFIFO(AHB_SSP0);
}
```

### 10.1.8 清空RX FIFO {#清空rx-fifo}

使用`apSSP_DeviceReceiveClear`清空RX FIFO

```c
void apSSP_DeviceReceiveClear(
    SSP_TypeDef * SSP_Ptr
    );
```

## 10.2 编程指南 {#编程指南}

### 10.2.1 blocking方式同时读写 {#blocking方式同时读写}

#### 10.2.1.1 IO初始化 {#io初始化}

```c
#define SPI_MIC_CLK         GIO_GPIO_10
#define SPI_MIC_CS          GIO_GPIO_11
#define SPI_MIC_MOSI        GIO_GPIO_12
#define SPI_MIC_MISO        GIO_GPIO_13

static void setup_peripherals_spi_pin(void)
{
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_AHB_SPI0)
                            | (1 << SYSCTRL_ClkGate_APB_PinCtrl));

    PINCTRL_SetPadMux(SPI_MIC_CLK, IO_SOURCE_SPI0_CLK);
    PINCTRL_SetPadMux(SPI_MIC_CS, IO_SOURCE_SPI0_SSN);
    PINCTRL_SetPadMux(SPI_MIC_MOSI, IO_SOURCE_SPI0_DO);
    PINCTRL_SelSpiDiIn(SPI_PORT_0, SPI_MIC_MISO);
}
```

#### 10.2.1.2 配置SSP模块 {#配置ssp模块}

```c
{
    //...
    SYSCTRL_ResetBlock(SYSCTRL_Reset_AHB_SPI0);
    SYSCTRL_ReleaseBlock(SYSCTRL_Reset_AHB_SPI0);  

    apSSP_sDeviceControlBlock param;

    apSSP_Initialize(SSP_Ptr);  

    /* Set Device Parameters */
    param.ClockRate        = 11;  // sspclkout = sspclk/(ClockPrescale*(ClockRate+1))
    param.ClockPrescale    = 2;  // Must be an even number from 2 to 254
    param.eSCLKPhase       = apSSP_SCLKPHASE_LEADINGEDGE;
    param.eSCLKPolarity    = apSSP_SCLKPOLARITY_IDLELOW;
    param.eFrameFormat     = apSSP_FRAMEFORMAT_MOTOROLASPI;
    param.eDataSize        = apSSP_DATASIZE_8BITS;
    param.eLoopBackMode    = apSSP_LOOPBACKOFF;
    param.eMasterSlaveMode = apSSP_MASTER;
    param.eSlaveOutput     = apSSP_SLAVEOUTPUTDISABLED;
    apSSP_DeviceParametersSet(SSP_Ptr, &param);

    apSSP_DeviceEnable(AHB_SSP0);
}
```

#### 10.2.1.3 发送并同时接收据 {#发送并同时接收据}

```c
/* Exchange a byte */
static uint8_t xchg_spi (
    uint8_t dat /* Data to send */
)
{
    apSSP_WriteFIFO(AHB_SSP0, dat);
    while (apSSP_DeviceBusyGet(AHB_SSP0)) ;
    return (uint8_t)apSSP_ReadFIFO(AHB_SSP0);
}
```

### 10.2.2 中断方式读取数据 {#中断方式读取数据}

#### 10.2.2.1 IO初始化 {#io初始化-1}

IO初始化，并设置SPI中断处理函数

```c
#define SPI_MIC_CLK         GIO_GPIO_10
#define SPI_MIC_CS          GIO_GPIO_11
#define SPI_MIC_MOSI        GIO_GPIO_12
#define SPI_MIC_MISO        GIO_GPIO_13

static void setup_peripherals_spi_pin(void)
{
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_AHB_SPI0)
                            | (1 << SYSCTRL_ClkGate_APB_PinCtrl));

    PINCTRL_SetPadMux(SPI_MIC_CLK, IO_SOURCE_SPI0_CLK);
    PINCTRL_SetPadMux(SPI_MIC_CS, IO_SOURCE_SPI0_SSN);
    PINCTRL_SetPadMux(SPI_MIC_MOSI, IO_SOURCE_SPI0_DO);
    PINCTRL_SelSpiDiIn(SPI_PORT_0, SPI_MIC_MISO);

    /* 配置中断处理函数 */
    platform_set_irq_callback(PLATFORM_CB_IRQ_SPI0, spi_irq_cb, NULL);
}
```

#### 10.2.2.2 配置SSP模块 {#配置ssp模块-1}

配置SSP模块，并使能接收中断

```c
{
    //...
    SYSCTRL_ResetBlock(SYSCTRL_Reset_AHB_SPI0);
    SYSCTRL_ReleaseBlock(SYSCTRL_Reset_AHB_SPI0);  

    apSSP_sDeviceControlBlock param;

    apSSP_Initialize(SSP_Ptr);  

    /* Set Device Parameters */
    param.ClockRate        = 11;  // sspclkout = sspclk/(ClockPrescale*(ClockRate+1))
    param.ClockPrescale    = 2;  // Must be an even number from 2 to 254
    param.eSCLKPhase       = apSSP_SCLKPHASE_LEADINGEDGE;
    param.eSCLKPolarity    = apSSP_SCLKPOLARITY_IDLELOW;
    param.eFrameFormat     = apSSP_FRAMEFORMAT_MOTOROLASPI;
    param.eDataSize        = apSSP_DATASIZE_8BITS;
    param.eLoopBackMode    = apSSP_LOOPBACKOFF;
    param.eMasterSlaveMode = apSSP_MASTER;
    param.eSlaveOutput     = apSSP_SLAVEOUTPUTDISABLED;
    apSSP_DeviceParametersSet(SSP_Ptr, &param);

    /* 使能接收中断 */
    apSSP_DeviceReceiveEnable(SSP_Ptr);
    apSSP_DeviceEnable(AHB_SSP0);
}
```

#### 10.2.2.3 中断处理函数中接收数据 {#中断处理函数中接收数据}

```c
uint8_t read_cnt = 0;
uint8_t read_data[8] = {0};

uint32_t spi_irq_cb(void *user_data)
{
    /* 获取中断状态 */
    uint32_t status = apSSP_GetIntRawStatus(AHB_SSP0);
    /* 清除中断状态 */
    apSSP_ClearInt(AHB_SSP0, status);

    /* 读取RX FIFO中的数据 */
    while (apSSP_RxFifoNotEmpty(AHB_SSP0))
    {
        uint8_t data = (uint8_t) apSSP_ReadFIFO(AHB_SSP0);
        read_data[read_cnt++] = data;
    }
    return 0;
}
```