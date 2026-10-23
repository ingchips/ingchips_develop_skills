<!-- pg_ing916: 5 DMA简介 -->

# 5 DMA简介 {#ch-dma}

DMA全称direct memory access，即直接存储器访问。

其主要作用是不占用CPU大量资源，在AMBA AHB总线上的设备之间以硬件方式高速有效地传输数据。

## 5.1 功能描述 {#功能描述-1}

### 5.1.1 特点 {#特点-1}

- 最多8个DMA通道
- 最多16个硬件握手请求/确认配对
- 支持8/16/32/64位宽的数据传输
- 支持24-64位地址宽度
- 支持成链传输数据

### 5.1.2 搬运方式 {#搬运方式}

- 单次数据块搬运：DMA使用单个通道，一次使能将数据从SRC到DST位置搬运一次
- 成串多数据块搬运：DMA使用单个通道，一次使能按照DMA链表信息依次将数据从SRC到DST位置搬运多次或循环搬运。

其根本区别是有无注册有效的DMA链表。

### 5.1.3 搬运类型 {#搬运类型}

- memory到memory搬运
- memory到peripheral搬运
- peripheral到memory搬运
- peripheral到peripheral搬运

### 5.1.4 中断类型 {#中断类型}

- IntErr：错误中断表示DMA传输发生了错误而触发中断，主要包括总线错误、地址没对齐和传输数据宽度没对齐等。
- IntAbt：终止传输中断会在终止DMA通道传输时产生。
- IntTC：TC中断会在没有产生IntErr和IntAbt的情况下完成一次传输时产生。

### 5.1.5 数据地址类型 {#数据地址类型}

- Increment address
- Decrement address
- Fixed address

如果Increment则DMA从地址由小到大搬运数据，相反的Decrement则由大到小搬运。fixed地址适用于外设FIFO的寄存器搬运数据。

### 5.1.6 数据方式 {#数据方式}

- normal mode
- handshake mode

DMA搬运前需要对数据源和数据目的地址的数据方式进行配置。

数据方式的选择有如下建议：

**1.** 从内存搬运数据选择normal mode；

**2.** 从外设FIFO搬运数据选择handshake mode，同时要和外设协商好BurstSize，支持2^n(n = 0-7)大小的BurstSize。

### 5.1.7 数据位宽 {#数据位宽}

DMA传输要求传输两端的数据类型一致，支持数据类型有：

- Byte transfer
- Half-word transfer
- Word transfer
- Double word transfer

覆盖所有常见数据类型。

## 5.2 使用方法 {#使用方法-1}

### 5.2.1 方法概述 {#方法概述}

首先确认数据搬运需求是单次搬运还是成串搬运，以及搬运类型，即memory和peripheral的关系。

#### 5.2.1.1 单次搬运 {#单次搬运}

**1.** 注册DMA中断

**2.** 定义一个DMA_Descriptor变量用来配置DMA通道寄存器

**3.** 根据数据搬运类型选择DMA寄存器配置接口，正确调用驱动接口配置DMA寄存器

**4.** 使能DMA通道开始搬运

#### 5.2.1.2 成串搬运 {#成串搬运}

**1.** 注册一个或多个DMA中断

**2.** 定义多个DMA_Descriptor变量用来配置DMA通道寄存器

**3.** 根据数据搬运类型选择DMA寄存器配置接口，正确调用驱动接口配置DMA寄存器

**4.** 将多个DMA_Descriptor变量首尾相连成串，类似链表

**5.** 使能DMA通道开始搬运

### 5.2.2 注意点 {#注意点}

- 定义DMA_Descriptor变量需要8字节对齐，否则DMA搬运不成功
- 成串搬运如果配置多个DMA中断则需要在每个中断里使能DMA，直到最后一次搬运完成
- 对于从外设搬运需要确认外设是否支持DMA
- 建议从外设搬运选择握手方式，并与外设正确协商burstSize
- burstSize尽量取较大值，有利于减少DMA中断次数提高单次中断处理效率。但burstSize太大可能最后一次不能搬运丢弃较多数据
- 建议设置从外设搬运总数据量为burstSize的整数倍或采用乒乓搬运的方式
- 在DMA从外设搬运的情况下，正确的操作顺序是先配置并使能好DMA，再使能外设开始产生数据

## 5.3 编程指南 {#编程指南-1}

### 5.3.1 驱动接口 {#驱动接口-1}

- DMA_PrepareMem2Mem：memory到memory搬运标准DMA寄存器配置接口
- DMA_PreparePeripheral2Mem：Peripheral到memory搬运标准DMA寄存器配置接口
- DMA_PrepareMem2Peripheral：memory到Peripheral搬运标准DMA寄存器配置接口
- DMA_PreparePeripheral2Peripheral：Peripheral到Peripheral搬运标准DMA寄存器配置接口
- DMA_Reset：DMA复位接口
- DMA_GetChannelIntState：DMA通道中断状态获取接口
- DMA_ClearChannelIntState：DMA通道清中断接口
- DMA_EnableChannel：DMA通道使能接口
- DMA_AbortChannel：DMA通道终止接口

### 5.3.2 代码示例 {#代码示例-1}

#### 5.3.2.1 单次搬运 {#单次搬运-1}

下面以memory到memory单次搬运展示DMA的基本用法：

```c
#define CHANNEL_ID  0
char src[] = "hello world!";
char dst[20];
DMA_Descriptor test __attribute__((aligned (8)));
static uint32_t DMA_cb_isr(void *user_data)
{
    uint32_t state = DMA_GetChannelIntState(CHANNEL_ID);
    DMA_ClearChannelIntState(CHANNEL_ID, state);

    printf("dst = %s\n", dst);
    return 0;
}

void DMA_Test(void)
{
    DMA_Reset();
    platform_set_irq_callback(PLATFORM_CB_IRQ_DMA, DMA_cb_isr, 0);
    DMA_PrepareMem2Mem(&test[0],
                       dst,
                       src, strlen(src),
                       DMA_ADDRESS_INC, DMA_ADDRESS_INC, 0);
    DMA_EnableChannel(CHANNEL_ID, &test);
}
```

最终会在DMA中断程序里面将搬运到dst中的“hello world!”字符串打印出来。

#### 5.3.2.2 成串搬运 {#成串搬运-1}

下面以memory到memory两块数据搬运拼接字符串展示DMA成串搬运的基本用法：

```c
#define CHANNEL_ID  0
char src[] = "hello world!";
char src1[] = "I am ING916.";
char dst[100];
DMA_Descriptor test[2] __attribute__((aligned (8)));
static uint32_t DMA_cb_isr(void *user_data)
{
    uint32_t state = DMA_GetChannelIntState(CHANNEL_ID);
    DMA_ClearChannelIntState(CHANNEL_ID, state);

    printf("dst = %s\n", dst);
    return 0;
}

void DMA_Test(void)
{
    DMA_Reset();
    platform_set_irq_callback(PLATFORM_CB_IRQ_DMA, DMA_cb_isr, 0);
      test[0].Next = &test[1];    // make a DMA link chain
      test[1].Next = NULL;
    DMA_PrepareMem2Mem(&test[0],
                       dst,
                       src, strlen(src),
                       DMA_ADDRESS_INC, DMA_ADDRESS_INC, 0);
    DMA_PrepareMem2Mem(&test[1],
                       dst + strlen(src),
                       src1, sizeof(src1),
                       DMA_ADDRESS_INC, DMA_ADDRESS_INC, 0);
    DMA_EnableChannel(CHANNEL_ID, &test[0]);
}
```

最终将会打印出“hello world!I am ING916.”字符串。

#### 5.3.2.3 DMA乒乓搬运 {#dma乒乓搬运}

DMA乒乓搬运是一种DMA搬运的特殊用法，其主要应用场景是将外设FIFO中数据循环搬运到memory中并处理。

可实现“搬运”和“数据处理”分离，从而大大提高程序处理数据的效率。

对于大量且连续的数据搬运，如音频，我们推荐选用DMA乒乓搬运的方式。

##### 5.3.2.3.1 DMA乒乓搬运接口 {#dma乒乓搬运接口}

在最新SDK中我们已将DMA乒乓搬运封装成标准接口，方便开发者调用，提高开发效率。

使用时请添加 `pingpong.c`文件，并包含 `pingpong.h`文件。

- DMA_PingPongSetup：DMA乒乓搬运建立接口
- DMA_PingPongIntProc：DMA乒乓搬运标准中断处理接口
- DMA_PingPongGetTransSize：获取DMA乒乓搬运数据量接口
- DMA_PingPongEnable：DMA乒乓搬运使能接口
- DMA_PingPongDisable：DMA乒乓搬运去使能接口

更多程序开发者可以参考voice_remote_ctrl例程。

##### 5.3.2.3.2 DMA乒乓搬运示例 {#dma乒乓搬运示例}

下面将以最常见的DMA乒乓搬运I2s数据为例展示DMA乒乓搬运的用法。

I2s的相关配置不在本文的介绍范围内，默认I2s已经配置好，DMA和I2s协商burstSize=8。

```c
#include "pingpong.h"
#define CHANNEL_ID  0
DMA_PingPong_t PingPong;

static uint32_t DMA_cb_isr(void *user_data)
{
    uint32_t state = DMA_GetChannelIntState(CHANNEL_ID);
    DMA_ClearChannelIntState(CHANNEL_ID, state);

    // call 'DMA_PingPongIntProc' to get the pointer of data-buff.
    uint32_t *rr = DMA_PingPongIntProc(&PingPong, CHANNEL_ID);
    uint32_t i = 0;
    // call 'DMA_PingPongGetTransSize' to kwon how much data in data-buff.
    uint32_t transSize = DMA_PingPongGetTransSize(&PingPong);
    while (i < transSize) {
        // do something with data 'rr[i]'
        i++;
    }

    return 0;
}

void DMA_Test(void)
{
    // call 'DMA_PingPongSetup' to setup ping-pong DMA.
    DMA_PingPongSetup(&PingPong, SYSCTRL_DMA_I2S_RX, 100, 8);
    platform_set_irq_callback(PLATFORM_CB_IRQ_DMA, DMA_cb_isr, 0);

    // call 'DMA_PingPongEnable' to start ping-pong DMA transmission.
    DMA_PingPongEnable(&PingPong, CHANNEL_ID);
    I2S_ClearRxFIFO(APB_I2S);
    I2S_DMAEnable(APB_I2S, 1, 1);
    I2S_Enable(APB_I2S, 0, 1);   // Enable I2s finally
}
```

停止DMA乒乓搬运可以调用以下接口：

```c
void Stop(void)
{
    // call 'DMA_PingPongEnable' to disable ping-pong DMA transmission.
    DMA_PingPongDisable(&PingPong, CHANNEL_ID);
    I2S_Enable(APB_I2S, 0, 0);
    I2S_DMAEnable(APB_I2S, 0, 0);
}
```