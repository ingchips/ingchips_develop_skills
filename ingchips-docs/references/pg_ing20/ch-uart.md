<!-- pg_ing20: 16 通用异步收发传输器（UART） -->

# 16 通用异步收发传输器（UART） {#ch-uart}

## 16.1 功能概述 {#功能概述-7}

UART全称Universal Asynchronous Receiver/Transmitter，即通用异步收发传输器件。 UART对接收的数据执行串并转换，对发送的数据执行并串转换。

特性：

- 支持硬件流控
- 可编程波特率发生器，最高波特率可达7000000bps
- 独立的发送和接收 FIFO
- 单个组合中断，包括接收（包括超时）、传输、调制解调器状态和错误状态中断，每个中断可屏蔽
- 支持 DMA 方式

## 16.2 使用说明 {#使用说明-7}

### 16.2.1 设置波特率 {#设置波特率}

使用 `apUART_BaudRateSet` 设置对应UART设备的波特率。

```c
void apUART_BaudRateSet(
  UART_TypeDef* pBase,      //UART参数结构体&设备地址
  uint32_t ClockFrequency,  //时钟信号的频率
  uint32_t BaudRate         //波特率
  );
```

### 16.2.2 获取波特率 {#获取波特率}

使用 `apUART_BaudRateGet` 获取对应UART设备的波特率。

```c
uint32_t apUART_BaudRateGet (
  UART_TypeDef* pBase, 
  uint32_t ClockFrequency
  );
```

### 16.2.3 UART初始化 {#ch-uart-initial}

在使用UART之前，需要先通过 `apUART_Initialize` 对UART进行初始化。

```c
void apUART_Initialize(
  UART_TypeDef* pBase, 
  UART_sStateStruct* UARTx,  //uart状态结构体
  uint32_t IntMask    //中断掩码
  );
```

初始化 UART 之前需要初始化如下所示的 UART 状态结构体：

```c
typedef struct UART_xStateStruct
{
    // Line Control Register, UARTLCR_H
  UART_eWLEN      word_length;   // WLEN
  UART_ePARITY    parity;        // PEN, EPS, SPS
  uint8_t         fifo_enable;   // FEN
  uint8_t         two_stop_bits; // STP2
  // Control Register, UARTCR
  uint8_t         receive_en;        // RXE
  uint8_t         transmit_en;       // TXE
  uint8_t         UART_en;           // UARTEN
  uint8_t         cts_en;            //CTSEN
  uint8_t         rts_en;            //RTSEN
  // Interrupt FIFO Level Select Register, UARTIFLS
  uint8_t         rxfifo_waterlevel; // RXIFLSEL
  uint8_t         txfifo_waterlevel; // TXIFLSEL
  //UART_eFIFO_WATERLEVEL    rxfifo_waterlevel; // RXIFLSEL
  //UART_eFIFO_WATERLEVEL    txfifo_watchlevel; // TXIFLSEL

  // UART Clock Frequency
  uint32_t        ClockFrequency;
  uint32_t        BaudRate;

} UART_sStateStruct;
```

常用的中断掩码如下所示， `IntMask` 是它们的组合。

```c
#define UART_INTBIT_RECEIVE            0x10  //receive interrupt
#define UART_INTBIT_TRANSMIT           0x20  //transmit interrupt
```

例如，配置并初始化串口，开启接收中断和发送中断，设置串口波特率为115200：

- 首先，创建UART配置函数 `config_uart` ，在函数内初始化UART状态结构体，并配置必要的状态参数， 然后调用 `apUART_Initialize` 初始化串口。

  ```c
    void config_uart(uint32_t freq, uint32_t baud)
    {
        UART_sStateStruct config;

        config.word_length       = UART_WLEN_8_BITS;
        config.parity            = UART_PARITY_NOT_CHECK;
        config.fifo_enable       = 1;
        config.two_stop_bits     = 0;
        config.receive_en        = 1;
        config.transmit_en       = 1;
        config.UART_en           = 1;
        config.cts_en            = 0;
        config.rts_en            = 0;
        config.rxfifo_waterlevel = 1;
        config.txfifo_waterlevel = 1;
        config.ClockFrequency    = freq;
        config.BaudRate          = baud;

        apUART_Initialize(PRINT_PORT, &config, UART_INTBIT_RECEIVE | UART_INTBIT_TRANSMIT);
    }
  ```

  使用时只需要如下所示调用 `config_uart` 函数即可。

  ```c
    config_uart(OSC_CLK_FREQ, 115200); 
  ```

### 16.2.4 UART轮询模式 {#uart轮询模式}

在轮询模式下，CPU通过检查线路状态寄存器中的位来检测事件：

- 使用 `apUART_Check_Rece_ERROR` 查询接收产生的错误字。

  ```c
    uint8_t apUART_Check_Rece_ERROR(
      UART_TypeDef* pBase
      );
  ```
- 用 `apUART_Check_RXFIFO_EMPTY`查询Rx FIFO是否为空。

  ```c
    uint8_t apUART_Check_RXFIFO_EMPTY(
      UART_TypeDef* pBase
      );
  ```
- 使用 `apUART_Check_RXFIFO_FULL`查询Rx FIFO是否已满。

  ```c
    uint8_t apUART_Check_RXFIFO_FULL(
      UART_TypeDef* pBase
      );
  ```
- 使用 `apUART_Check_TXFIFO_EMPTY` 查询Tx FIFO是否为空。

  ```c
    uint8_t apUART_Check_TXFIFO_EMPTY(
      UART_TypeDef* pBase
      );
  ```
- 使用 `apUART_Check_TXFIFO_FULL` 查询Tx FIFO是否已满。

  ```c
    uint8_t apUART_Check_TXFIFO_FULL(
      UART_TypeDef* pBase
      ); 
  ```

### 16.2.5 UART中断使能/禁用 {#uart中断使能禁用}

用 `apUART_Enable_TRANSMIT_INT` 使能发送中断，用 `apUART_Disable_TRANSMIT_INT` 禁用发送中断； 用 `apUART_Enable_RECEIVE_INT` 使能接收中断，用 `apUART_Disable_RECEIVE_INT` 禁用接收中断。

中断默认是禁用的，使能中断既能用上述 `apUART_Enable_TRANSMIT_INT` 和 `apUART_Enable_RECEIVE_INT` 的方式，也可以通过 `apUART_Initialize` 初始化串口是设置参数 `IntMask` 的值使能相应的中断，详情请参考 [UART初始化](https://ingchips.github.io/drafts/pg_ing20/ch-uart.html#ch-uart-initial)

### 16.2.6 处理中断状态 {#处理中断状态-2}

用 `apUART_Get_ITStatus` 获取某个UART上的中断触发状态，返回非 0 值表示该 UART 上产生了中断请求；用 `apUART_Get_all_raw_int_stat` 一次性获取所有 UART 的中断触发状态， 第 n 比特（第 0 比特为最低比特）对应 UART n 上的中断触发状态。

UART产生中断后，需要消除中断状态方可再次触发。用 `apUART_Clr_RECEIVE_INT` 消除某个 UART上接收中断的状态， 用 `apUART_Clr_TX_INT` 消除某个 UART上发送中断的状态。用 `apUART_Clr_NonRx_INT` 消除某个 UART上除接收以外的中断状态。

### 16.2.7 UART FIFO中断触发逻辑 {#uart-fifo中断触发逻辑}

RX中断：

- 当接收FIFO水位标记被触发时，产生RX中断。

RX Timeout中断：

- 当接收FIFO超时中断被触发时，产生RX Timeout中断。

TX中断：

- 当发送FIFO水位标记被触发时，产生TX中断。
- 当使能TX fifo中断时，不会直接产生中断，需向fifo写入数据后，才会产生中断。例如：txfifo_waterlevel = 1， 则当fifo中有1个字节数据时，产生中断；当fifo中有2个字节数据时，不会产生中断，需写入第2个字节后，才会产生中断。

  注意： 当使能TX时，TX fifo写入的第一个字节会直接发送，因此当txfifo_waterlevel = 0时，写入一个字节不会产生fifo中断。 推荐每次发送数据时，使用apUART_Check_TXFIFO_FULL()接口，写入数据直到TX fifo满，减少中断次数的同时保证中断正常产生。

### 16.2.8 发送数据 {#发送数据}

使用 `UART_SendData` 发送数据。

```c
void UART_SendData(
  UART_TypeDef* pBase, 
  uint8_t Data
  );
```

### 16.2.9 接收数据 {#接收数据}

使用 `UART_ReceData` 接收数据。

```c
uint8_t UART_ReceData(
  UART_TypeDef* pBase
  );
```

### 16.2.10 DMA传输模式使能 {#dma传输模式使能}

使用 `UART_DmaEnable`使能UART的DMA工作模式，可以使用DMA完成对串口数据的收发，从而不占用 CPU 的资源。

```c
void UART_DmaEnable(
  UART_TypeDef *pBase, 
  uint8_t tx_enable,   //发送使能(1)/禁用(0)
  uint8_t rx_enable,   //接收使能(1)/禁用(0)
  uint8_t dma_on_err
  );
```

## 16.3 示例代码 {#示例代码}

### 16.3.1 UART接收变长字节数据 {#uart接收变长字节数据}

1. **UART+FIFO方式**

```c
#define RX_FIFO_WATER_LEVEL     0x10
char dst[256];

void config_uart(uint32_t freq, uint32_t BaudRate)
{
    //config uarts parameter
    UART_sStateStruct config;

    config.word_length       = UART_WLEN_8_BITS;
    config.parity            = UART_PARITY_NOT_CHECK;
    config.fifo_enable       = 1;
    config.two_stop_bits     = 0;
    config.receive_en        = 1;
    config.transmit_en       = 1;
    config.UART_en           = 1;
    config.cts_en            = 0;
    config.rts_en            = 0;   
    config.rxfifo_waterlevel = RX_FIFO_WATER_LEVEL;
    config.txfifo_waterlevel = 1;
    config.ClockFrequency    = freq;
    config.BaudRate          = BaudRate;

    apUART_Initialize(APB_UART0, &config, UART_INTBIT_TIMEOUT | UART_INTBIT_RECEIVE);
}

uint32_t uart_isr(void *user_data)
{
    uint32_t status;
    static int index = 0;
    uint8_t cnt = 0;
    while(1)
    {
        status = apUART_Get_all_raw_int_stat(APB_UART0);

        if (status == 0)
            break;

        APB_UART0->IntClear = status;

        // rx int
        if (status & (1 << bsUART_RECEIVE_INTENAB))
        {
            while (apUART_Check_RXFIFO_EMPTY(APB_UART0) != 1)
            {
                char c = APB_UART0->DataRead;
                dst[index++] = c;
                cnt++;
                /* To avoid the situation where the RX FIFO data length is the same as that 
                   of the RX_FIFO_WATER_LEVEL, the rx timeout interrupt cannot be generated.*/
                if(cnt >= RX_FIFO_WATER_LEVEL - 1) 
                {
                    break;
                }
            }
        }

        // rx timeout_int
        if (status & (1 << bsUART_TIMEOUT_INTENAB))
        {
            while (apUART_Check_RXFIFO_EMPTY(APB_UART0) != 1)
            {
                char c = APB_UART0->DataRead;
                dst[index++] = c;
            }
            dst[index] = 0;
            // 一包数据接收完毕，可在此进行数据处理
            index = 0;
        }
    }
    return 0;
}

void uart_peripherals_read_data()
{
    //注册uart0中断
    platform_set_irq_callback(PLATFORM_CB_IRQ_UART0, uart_isr, NULL);
    config_uart(OSC_CLK_FREQ, 115200);
}
```

1. **UART+FIFO+DMA方式**

```c
char dst[256];
char src[] = "Finished to receive a frame!\n";

#define DMA_RX_CHANNEL_ID  1
#define DMA_TX_CHANNEL_ID  0

void config_uart(uint32_t freq, uint32_t BaudRate)
{
    //config uarts parameter
    UART_sStateStruct config;

    config.word_length       = UART_WLEN_8_BITS;
    config.parity            = UART_PARITY_NOT_CHECK;
    config.fifo_enable       = 1;
    config.two_stop_bits     = 0;
    config.receive_en        = 1;
    config.transmit_en       = 1;
    config.UART_en           = 1;
    config.cts_en            = 0;
    config.rts_en            = 0;   
    config.rxfifo_waterlevel = 7;
    config.txfifo_waterlevel = 1;
    config.ClockFrequency    = freq;
    config.BaudRate          = BaudRate;

    apUART_Initialize(APB_UART0, &config, UART_INTBIT_TIMEOUT);
    UART_DmaEnable(APB_UART0, 1, 1, 0);
}

static void setup_peripheral_dma(void)
{
    DMA_Descriptor descriptor __attribute__((aligned (8))) = {0};
    DMA_PreparePeripheral2Mem(  &descriptor, 
                                dst, SYSCTRL_DMA_UART0_RX, 
                                sizeof(dst), DMA_ADDRESS_INC, 0);
    DMA_EnableChannel(DMA_RX_CHANNEL_ID, &descriptor);
}

//添加UART通过DMA发送的配置
void UART_trigger_DmaSend(void)
{ 
    DMA_Descriptor descriptor __attribute__((aligned (8))) = {0};
    DMA_PrepareMem2Peripheral(  &descriptor,
                                SYSCTRL_DMA_UART0_TX,
                                src, strlen(src),
                                DMA_ADDRESS_INC, 0);
    DMA_EnableChannel(DMA_TX_CHANNEL_ID, &descriptor);
}

uint32_t uart_isr(void *user_data)
{
    uint32_t status;
    int index = 0;
    while(1)
    {
        status = apUART_Get_all_raw_int_stat(APB_UART0);

        if (status == 0)
            break;

        APB_UART0->IntClear = status;

        // rx timeout_int
        if (status & (1 << bsUART_TIMEOUT_INTENAB))
        {
            index = APB_DMA->Channels[DMA_RX_CHANNEL_ID].Descriptor.DstAddr - (uint32_t)rx_buffer;
            while (apUART_Check_RXFIFO_EMPTY(APB_UART0) != 1)
            {
                char c = APB_UART0->DataRead;
                dst[index++] = c;
            }
            dst[index] = 0;
            // 一包数据接收完毕，可在此进行数据处理
            UART_trigger_DmaSend();
            setup_peripheral_dma();
        }
    }
    return 0;
}

void uart_peripherals_read_data()
{
    //注册uart0中断
    platform_set_irq_callback(PLATFORM_CB_IRQ_UART0, uart_isr, NULL);
    config_uart(OSC_CLK_FREQ, 115200);
    setup_peripheral_dma();
}
```