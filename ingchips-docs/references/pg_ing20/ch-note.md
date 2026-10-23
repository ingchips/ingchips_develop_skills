<!-- pg_ing20: 23 勘误 -->

# 23 勘误 {#ch-note}

本章节介绍 20xx 系列芯片存在的一些使用限制

## 23.1 概览 {#概览}

下面是所以已经发现的局限性概览：

| 外设 | 内容 |
| --- | --- |
| FLASH | 单次写入最大 32 字节，多次写入效率低 |
| FLASH | 使用 dma 写入会占用 dma 通道和时钟问题 |
| ADC | 通道 0 和 1 默认对输入电压 1/2 采样，低电压场景下（小于 1/3 Vbat）采样精度较低 |
| KEYSCAN | 走线寄生电容较大时，采样率存在限制 |
| KEYSCAN | loop 周期采样存在限制 |
| KEYSCAN | keyscan 对应 IO 上下拉电阻影响功能 |
| KEYSCAN | keyscan 对应 high 和 low 的扫描功能不能关闭 |
| QDEC | qdec 的外设时钟使用低速时钟时，总线访问延迟可能会出现读写寄存器失败问题 |
| UART | 串口使用 timeout 中断时，如果使用 dma 或读 fifo 将数据完全读出，无法触发 timeout 中断 |

## 23.2 FLASH {#flash}

### 23.2.1 单次写入限制 {#单次写入限制}

建议 FLASH 写入操作单次不超过 32 字节，超出 32 字节的写入需要拆分写入，SDK 默认接口都是使用的拆分形式， 拆分写入会导致每写入 32 字节需要等待约 1.2ms，写入超过 32 字节数据会导致写入时间被延长，影响接口返回实现，长时间阻塞系统。

### 23.2.2 DMA 写入限制 {#dma-写入限制}

超过 32 字节的数据写入可以通过使能 `eflash.h` 中的宏 `FLASH_PROGRAM_WITH_DMA` 为 1 来单次编程小于等于一页（256字节）的数据, 但是 DMA 写入也存在限制。

- 会强制占用 DMA 外设的 CH0 且不可更改 DMA 通道
- 调用 DMA 操作 FLASH 时如果 FLASH 时钟较快（大于 40Mhz）需要降低 FLASH 的时钟到 24M，否则可能会出现调用写入接口只能成功编程 16 字节数据的情况。

## 23.3 ADC {#adc}

通道 0 和 1 硬件默认对输入电压进行 1/2 分压采样，在小于 1/3 Vbat 的输入电压下采样精度较低，如果需要采集较低的输入电压，请不要使用这两个输入通道。

## 23.4 KEYSCAN {#keyscan}

### 23.4.1 扫描周期限制 {#扫描周期限制}

keyscan 由默认 GPIO 执行硬件扫描动作，高低电平变换完全有 IO 驱动，驱动能力受限于 IO 的驱动能力，在外部按键走线过长，寄生电容较大的应用场景，可能会出现硬件执行扫描时，上升沿时间过长，无法扫描到按键按下的情况。优化方案有以下两种：

- 增强 IO 的驱动能力：调用接口 `PINCTRL_SetDriveStrength` 设置驱动能力为 `PINCTRL_DRIVE_12mA` 增强拉电流可以加快上升时间。
- 增加检测时间间隔 `release_time`，等待上升时间达到再执行下一组按键的扫描。（会降低扫描周期，硬件设计应注意走线寄生电容）

### 23.4.2 TABLE 模式总线上拉限制 {#table-模式总线上拉限制}

keyscan 的 ROW 和 COL 线上添加上拉或下拉电阻，TABLE 模式存在限制，会一直上报 ROW 和 COL 的独立按键事件（normal 模式也上报，可以手动忽略）。不要为 keyscan 总线添加上拉电阻或下拉电阻。

### 23.4.3 ROW 和 COL 上的独立按键限制 {#row-和-col-上的独立按键限制}

- ROW 和 COL 上的独立按键相比于纯按键矩阵会略微增加扫描时间，该功能不可关闭。
- ROW 和 COL 上的独立按键触发后，后续触发的一排按键不再执行按键扫描，如果此时有矩阵按键按下，可能会丢失按键事件。

### 23.4.4 loop 模式中断限制 {#loop-模式中断限制}

keyscan 的 loop 模式支持开启 loop 中断，loop 的扫描次数可以根据结构体内部 `loop_num_trig_int` 的值配置（最大 31 个扫描周期）。当 loop-num 递减为 0 之后扫描会停止。可选优化方案：

- 关闭 loop 中断，`loop_num_trig_int` 配置为 1，硬件会一直执行 loop 扫描，但是不会上报 loop 中断。

## 23.5 QDEC 时钟配置限制 {#qdec-时钟配置限制}

基于使用场景，我们推荐用户使用 qdec 时，时钟源设置为来自于低速24M的外设时钟，qdec 外设在使用时钟为低速时钟时存在硬件限制，可能会导致配置寄存器（`QDEC_QdecCfg` 等配置接口）配置失败或者读取配置寄存器数据无效。

### 23.5.1 优化方案 {#优化方案}

配置 `SYSCTRL_UpdateQdecClk` 接口（最高 15 分频），降低 pclk 相对于 qdec 配置的时钟，例如 hclk 为 128Mhz，配置 `SYSCTRL_UpdateQdecClk(6)` 设置 qdec-pclk 约 22Mhz。保证寄存器写入和读取都能成功执行。

### 23.5.2 pclk 远大于 qdec-pclk 导致配置失败 {#pclk-远大于-qdec-pclk-导致配置失败}

某些极限场景，例如 hclk 为 128Mhz，配置 `SYSCTRL_UpdateQdecClk(15)` 设置 qdec-pclk 约 8Mhz。由于总线存在访问延迟，CPU 运行速度有可能超过总线指令速度， 连续操作配置寄存器可能出现问题，表现为配置寄存器为错误的值，此时对配置寄存器进行读写 CPU 需要进行等待总线访问写入，可以调整 `peripheral_qdec.c` 中的 `NOP_NUME` 值，增加读写访问的等待时间。**应用场景请尽量不要配置 qdec-pclk 太低，远低于 hclk 时钟**。

## 23.6 UART {#uart}

### 23.6.1 Timeout限制 {#timeout限制}

UART 的接收 timeout 中断在使用时，如果使用 dma 或读 fifo 的方式将数据完全读出，会发生 timout 中断一直无法触发的情况。

优化方案:

- 如果使用 fifo 接收中断: 在接收中断不要将 fifo 数据完全读空，在 fifo 中留 1 个或 2 个数据，等 timeout 触发，再将数据完全读出。

示例代码实现:

```c

#define  RX_FIFO_WATER_LEVEL        5

uint8_t uart_rx_data[256];
uint32_t uart_irq_cb(void *arg)
{
    static uint8_t index = 0;
    uint8_t status, cnt = 0;
    (void) arg;
    status = apUART_Get_all_raw_int_stat(APB_UART1);

    if (status & (1 << bsUART_RECEIVE_INTENAB))
    {
        while(apUART_Check_RXFIFO_EMPTY(APB_UART1) == 0)
        {
            uart_rx_data[index++] = UART_ReceData(APB_UART1);
            cnt++;
            /* To avoid the situation where the RX FIFO data length is the same as that
            of the RX_FIFO_WATER_LEVEL, the rx timeout interrupt cannot be generated.*/
            if(cnt >= RX_FIFO_WATER_LEVEL - 1)
            {
                break;
            }
        }
    }
    if (status & (1 << bsUART_TIMEOUT_INTENAB))
    {
        while(apUART_Check_RXFIFO_EMPTY(APB_UART1) == 0)
        {
            uart_rx_data[index++] = UART_ReceData(APB_UART1);
        }
        uart_rx_data[index] = 0;
        platform_printf("time out\n");
        platform_printf("%s", uart_rx_data);
        index = 0;
    }
    return 0;
}

void uart_init(uint32_t baud)
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
    config.rxfifo_waterlevel = RX_FIFO_WATER_LEVEL;
    config.txfifo_waterlevel = 1;
    config.ClockFrequency    = SYSCTRL_GetClk(SYSCTRL_ITEM_APB_UART1);
    config.BaudRate          = baud;


    SYSCTRL_ClearClkGate(SYSCTRL_ClkGate_APB_GPIO0);//gpio0
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_APB_UART1)
                            | (1 << SYSCTRL_ClkGate_APB_PinCtrl));
    PINCTRL_SetPadMux(GIO_GPIO_7, IO_SOURCE_UART1_TXD);
    PINCTRL_SelUartRxdIn(UART_PORT_1,GIO_GPIO_8);
    apUART_Initialize(APB_UART1, &config, (1ul<<bsUART_RECEIVE_INTENAB) | (1ul<<bsUART_TIMEOUT_INTENAB));

    platform_set_irq_callback(PLATFORM_CB_IRQ_UART1, uart_irq_cb, 0);
}
```

- 使用 dma 方式：设置 fifo 中断触发水线为 3 或 5 等单数，将 dma 的 burt_size 设置为 2 不要设置为 1，即 dma 搬运完成会遗留几个数据在 fifo 中，之后在 timeout 中断中处理剩余数据的接收。

示例代码实现

```c

#define  RX_FIFO_WATER_LEVEL        5
#define UART_RX_CHANNEL_ID  1
#define BUFF_SIZE       0x100

uint8_t uart_rx_data[BUFF_SIZE];
DMA_Descriptor descriptor_uart_rx __attribute__((aligned (8)));

uint32_t uart_irq_cb(void *arg)
{
    static uint8_t index = 0;
    uint8_t status, cnt = 0;
    (void) arg;
    status = apUART_Get_all_raw_int_stat(APB_UART1);

    if (status & (1 << bsUART_TIMEOUT_INTENAB))
    {
        index = APB_DMA->Channels[UART_RX_CHANNEL_ID].Descriptor.DstAddr - (uint32_t)uart_rx_data;
        while(apUART_Check_RXFIFO_EMPTY(APB_UART1) == 0)
        {
            uart_rx_data[index++] = UART_ReceData(APB_UART1);
        }
        uart_rx_data[index] = 0;
        DMA_EnableChannel(UART_RX_CHANNEL_ID, &descriptor_uart_rx);
        platform_printf("time out\n");
        platform_printf("%s", uart_rx_data);
        index = 0;
    }
    return 0;
}

uint32_t dma_irq_cb(void *arg)
{
    (void) arg;
    uint32_t uart_rx_state = DMA_GetChannelIntState(UART_RX_CHANNEL_ID);

    if (uart_rx_state & DMA_IRQ_TC)
    {
        DMA_ClearChannelIntState(UART_RX_CHANNEL_ID, uart_rx_state);
        DMA_EnableChannel(UART_RX_CHANNEL_ID, &descriptor_uart_rx);
    }
    return 0;
}

void uart_dma_init(void)
{
    uint8_t width, burst;
    SYSCTRL_ClearClkGate(SYSCTRL_ITEM_APB_DMA);
    DMA_PreparePeripheral2Mem(&descriptor_uart_rx, (uint32_t*)uart_rx_data, SYSCTRL_DMA_UART1_RX,
        BUFF_SIZE, DMA_ADDRESS_INC, 0);
    DMA_ConfigSrcBurstSize(&descriptor_uart_rx, DMA_BURST_SIZE_2);

    platform_set_irq_callback(PLATFORM_CB_IRQ_DMA, dma_irq_cb, 0);

    DMA_EnableChannel(UART_RX_CHANNEL_ID, &descriptor_uart_rx);
}

void uart_init(uint32_t baud)
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
    config.rxfifo_waterlevel = RX_FIFO_WATER_LEVEL;
    config.txfifo_waterlevel = 1;
    config.ClockFrequency    = SYSCTRL_GetClk(SYSCTRL_ITEM_APB_UART1);
    config.BaudRate          = baud;


    SYSCTRL_ClearClkGate(SYSCTRL_ClkGate_APB_GPIO0);//gpio0
    SYSCTRL_ClearClkGateMulti((1 << SYSCTRL_ClkGate_APB_UART1)
                            | (1 << SYSCTRL_ClkGate_APB_PinCtrl));
    PINCTRL_SetPadMux(GIO_GPIO_7, IO_SOURCE_UART1_TXD);
    PINCTRL_SelUartRxdIn(UART_PORT_1,GIO_GPIO_8);
    apUART_Initialize(APB_UART1, &config, (1ul<<bsUART_TIMEOUT_INTENAB));

    UART_DmaEnable(APB_UART1, 0, 1, 0);

    platform_set_irq_callback(PLATFORM_CB_IRQ_UART1, uart_irq_cb, 0);

    uart_dma_init();
}
```