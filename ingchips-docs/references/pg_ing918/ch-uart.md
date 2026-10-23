<!-- pg_ing918: 13 通用异步收发传输器（UART） -->

# 13 通用异步收发传输器（UART） {#ch-uart}

## 13.1 功能概述 {#功能概述-6}

UART负责处理数据总线和串行口之间的串/并、并/串转换，并规定了相应的帧格式，通信双方只要采用相同的帧格式和波特率， 就能在未共享时钟信号的情况下，仅用两根信号线（RX和TX）完成通信过程。

特性：

- 异步串行通信，可为全双工、半双工、单发送（TX）或单接收（RX）模式；
- 支持5~8位数据位的配置，波特率几百bps至几百Kbbps；
- 可配置奇校验、偶校验或无校验位；可配置1、1.5或2位停止位；
- 将并行数据写入内存缓冲区，再通过FIFO逐位发送，接收时同理；
- 输出传输时，从低位到高位传输。

## 13.2 使用说明 {#使用说明-3}

### 13.2.1 设置波特率 {#设置波特率}

使用 `apUART_BaudRateSet` 设置对应UART设备的波特率。

```c
void apUART_BaudRateSet(
  UART_TypeDef* pBase,
  uint32_t ClockFrequency,
  uint32_t BaudRate
  );
```

### 13.2.2 获取波特率 {#获取波特率}

使用 `apUART_BaudRateGet` 获取对应UART设备的波特率。

```c
uint32_t apUART_BaudRateGet (
  UART_TypeDef* pBase,
  uint32_t ClockFrequency
  );
```

### 13.2.3 接收错误查询 {#接收错误查询}

使用 `apUART_Check_Rece_ERROR` 查询接收产生的错误。

```c
uint8_t apUART_Check_Rece_ERROR(
  UART_TypeDef* pBase
  );
```

### 13.2.4 FIFO轮询模式 {#fifo轮询模式}

在轮询模式下，CPU通过检查线路状态寄存器中的位来检测事件：

- 使用 `apUART_Check_Rece_ERROR` 查询接收产生的错误字。

  ```c
    uint8_t apUART_Check_Rece_ERROR(
      UART_TypeDef* pBase
      );
  ```
- 用 `apUART_Check_RXFIFO_EMPTY`查询RXFIFO是否为空。

  ```c
    uint8_t apUART_Check_RXFIFO_EMPTY(
      UART_TypeDef* pBase
      );
  ```
- 使用 `apUART_Check_RXFIFO_FULL`查询RXFIFO是否已满。

  ```c
    uint8_t apUART_Check_RXFIFO_FULL(
      UART_TypeDef* pBase
      );
  ```
- 使用 `apUART_Check_TXFIFO_EMPTY` 查询TXFIFO是否为空。

  ```c
    uint8_t apUART_Check_TXFIFO_EMPTY(
      UART_TypeDef* pBase
      );
  ```
- 使用 `apUART_Check_TXFIFO_FULL` 查询TXFIFO是否已满。

  ```c
    uint8_t apUART_Check_TXFIFO_FULL(
      UART_TypeDef* pBase
      );
  ```

### 13.2.5 发送数据 {#发送数据-1}

使用 `UART_SendData` 发送8bits数据。

```c
void UART_SendData(
  UART_TypeDef* pBase,
  uint8_t Data
  );
```

### 13.2.6 接收数据 {#接收数据-1}

使用 `UART_ReceData` 接收8bits数据。

```c
uint8_t UART_ReceData(
  UART_TypeDef* pBase
  );
```

### 13.2.7 配置中断请求 {#配置中断请求-1}

使用 `apUART_Enable_TRANSMIT_INT` 使能发送中断状态。

```c
void apUART_Enable_TRANSMIT_INT(
  UART_TypeDef* pBase
  );
```

使用 `apUART_Disable_TRANSMIT_INT` 禁用发送中断状态。

```c
void apUART_Disable_TRANSMIT_INT(
  UART_TypeDef* pBase
  );
```

使用 `apUART_Enable_RECEIVE_INT` 使能接收中断状态。

```c
void apUART_Enable_RECEIVE_INT(
  UART_TypeDef* pBase
  );
```

使用 `apUART_Disable_RECEIVE_INT` 禁用接收中断状态。

```c
void apUART_Disable_RECEIVE_INT(
  UART_TypeDef* pBase
  );
```

### 13.2.8 处理中断状态 {#处理中断状态-2}

uint8_t apUART_Get_ITStatus(UART_TypeDef* pBase,uint8_t UART_IT); uint32_t apUART_Get_all_raw_int_stat(UART_TypeDef* pBase);

void apUART_Clr_RECEIVE_INT(UART_TypeDef* pBase); void apUART_Clr_TX_INT(UART_TypeDef* pBase); void apUART_Clr_NonRx_INT(UART_TypeDef* pBase);

### 13.2.9 UART初始化 {#uart初始化}

两个设备使用UART通讯时，必须先约定好传输速率和一些数据位。

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

定义函数 `config_uart` ,

```c
void config_uart(
  uint32_t freq,
  uint32_t baud
  );
```

在函数中，对UART_sStateStruct的各项参数初始化，并调用 `apUART_Initialize` 对UART进行初始化。

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

    apUART_Initialize(PRINT_PORT, &config, 0);
}
```

### 13.2.10 发送数据 {#发送数据-2}

使用 `UART_SendData` 发送数据。

```c
void UART_SendData(
  UART_TypeDef* pBase,
  uint8_t Data
  );
```

### 13.2.11 接收数据 {#接收数据-2}

使用 `UART_ReceData` 接收数据。

```c
uint8_t UART_ReceData(
  UART_TypeDef* pBase
  );
```

### 13.2.12 清空FIFO {#清空fifo}

使用 `uart_empty_fifo` 清空UART的FIFO。

```c
static void uart_empty_fifo(
  UART_TypeDef* pBase
  );
```

### 13.2.13 使能FIFO {#使能fifo}

使用 `uart_enable_fifo` 使能UART的FIFO。

```c
static void uart_enable_fifo(
  UART_TypeDef* pBase
  );
```

### 13.2.14 处理中断状态 {#处理中断状态-3}

用 `apUART_Get_ITStatus` 获取某个UART上的中断触发状态，返回非 0 值表示该 UART 上产生了中断请求；用 `apUART_Get_all_raw_int_stat` 一次性获取所有 UART 的中断触发状态， 第 n 比特（第 0 比特为最低比特）对应 UART n 上的中断触发状态。

UART产生中断后，需要消除中断状态方可再次触发。用 `apUART_Clr_RECEIVE_INT` 消除某个 UART上接收中断的状态， 用 `apUART_Clr_TX_INT` 消除某个 UART上发送中断的状态。用 `apUART_Clr_NonRx_INT` 消除某个 UART上除接收以外的中断状态。