<!-- pg_ing916: 12 PDM简介 -->

# 12 PDM简介 {#ch-PDM}

PDM全称pulse density modulation，即脉冲密度调制。

PDM模块处理来自外部音频前端(如数字麦克风)的脉冲密度调制信号的输入。该模块生成PDM时钟，支持双通道数据输入。

## 12.1 功能描述 {#功能描述-3}

### 12.1.1 特点 {#特点-3}

- 支持双通道，数据输入相同
- 16kHz输出采样率，24位采样
- HW抽取过滤器
- 时钟和输出采样率之间的可选比为64或80
- 支持DMA和I2S的样本缓冲

### 12.1.2 PDM & PCM {#pdm-pcm}

PDM和PCM同为用数字信号表示模拟信号的音频数据调制方法，其主要区别是：

- PDM不像PCM等间隔采样
- PDM只有1位非0即1的输出，而PCM采样结果可以是Nbit
- PDM使用远高于PCM采样率的时钟频率进行采样
- PDM逻辑相对PCM复杂

## 12.2 使用方法 {#使用方法-3}

### 12.2.1 方法概述 {#方法概述-2}

PDM使用方法分为PDM结合I2s使用和PDM数据直接DMA搬运两种。

PDM结合I2s：

**1.** PDM引脚GPIO配置（时钟、数据）

**2.** 外部时钟配置，使其处于工作模式

**3.** 写相应配置寄存器

**4.** 配置I2s数据源为PDM，配置I2s时钟、寄存器、中断

**5.** 使能PDM，使能I2s

**6.** 等待I2s中断产生

**7.** 读取状态寄存器，读取RX_MEM中数据

**8.** 传输完毕，关闭PDM和I2S

PDM数据DMA搬运：

**1.** PDM引脚GPIO配置（时钟、数据）

**2.** 外部时钟配置，使其处于工作模式

**3.** 写相应配置寄存器

**4.** 配置DMA寄存器、中断

**5.** 使能DMA，使能PDM

**6.** 等待DMA中断产生

**7.** 传输完毕，关闭PDM和DMA

其中I2s和DMA相关配置不在本节介绍内容范围内，可参考本手册对应章节。

### 12.2.2 注意点 {#注意点-2}

- I2s时钟源可以选择晶振24M时钟和PLL时钟，要注意是选择哪一个时钟源
- 建议选择晶振24M作为时钟源，这样可以获得较好的准确度和防抖动效果
- 需要查阅数字麦克风数据手册了解其时钟要求，并正确配置PDM时钟频率
- 结合I2s使用时要先使能PDM最后开启I2s
- 结合DMA使用时要先使能DMA最后开启PDM
- 建议采用DMA乒乓搬运的方式

## 12.3 编程指南 {#编程指南-4}

### 12.3.1 驱动接口 {#驱动接口-3}

- PDM_Config：PDM配置接口
- PDM_Start：PDM使能接口
- PDM_DmaEnable：PDM使能DMA接口

### 12.3.2 代码示例 {#代码示例-3}

下面以PDM结合I2s使用和PDM数据直接DMA搬运两种方式来展示PDM的具体使用方法。

已知现有mic使用的时钟频率为3M，I2s采样率16K。

#### 12.3.2.1 PDM结合I2s： {#pdm结合i2s}

```c
#define PDM_PIN_MCLK        28
#define PDM_PIN_IN          29
static uint32_t I2s_isr(void *user_data)
{ 
    uint32_t state = I2S_GetIntState(APB_I2S);
    I2S_ClearIntState(APB_I2S, state);

    int i = I2S_GetRxFIFOCount(APB_I2S);
    while (i) {
        // do something with these data
        i--;
    }
}

void audio_input_setup(void)
{
    // GPIO & Pin Ctrl
    PINCTRL_SetPadMux(PDM_PIN_MCLK, IO_SOURCE_PDM_DMIC_MCLK);
    PINCTRL_SetPadMux(PDM_PIN_IN, IO_SOURCE_PDM_DMIC_IN);
    PINCTRL_SelPdmIn(PDM_PIN_IN);

    // PDM clock configuration, 3M
    SYSCTRL_SetPdmClkDiv(8, 1);
    SYSCTRL_SelectTypeAClk(SYSCTRL_ITEM_APB_PDM, SYSCTRL_CLK_ADC_DIV);

    // PDM register configuration
    PDM_Config(APB_PDM, 0, 1, 1, 1, 0);    

    // I2s configuration, bclk=2.4M, samplerate=16K, data from PDM
    I2S_DataFromPDM(1);    
    I2S_ConfigClk(APB_I2S, 5, 75);
    I2S_ConfigIRQ(APB_I2S, 0, 1, 0, 10);
    I2S_DMAEnable(APB_I2S, 0, 0);    
    I2S_Config(APB_I2S, I2S_ROLE_MASTER, I2S_MODE_STANDARD, 0, 1, 0, 1, 24);

    // I2s interruption
    platform_set_irq_callback(PLATFORM_CB_IRQ_I2S, I2s_isr, 0);

    // enable I2s and PDM
    I2S_ClearRxFIFO(APB_I2S);
    PDM_Start(APB_PDM, 1);
    I2S_Enable(APB_I2S, 0, 1);
}
```

上面示例涉及到的关于I2s配置参考手册的I2s章节：

#### 12.3.2.2 PDM数据DMA搬运 {#pdm数据dma搬运}

```c
#define PDM_PIN_MCLK        28
#define PDM_PIN_IN          29
#define CHANNEL_ID          0
uint32_t buff[80];
DMA_Descriptor test __attribute__((aligned (8)));
static uint32_t DMA_cb_isr(void *user_data)
{ 
    uint32_t state = DMA_GetChannelIntState(CHANNEL_ID);
    DMA_ClearChannelIntState(CHANNEL_ID, state);

    DMA_EnableChannel(CHANNEL_ID, &test);

    // do something with data in buff
}

void DMA_SetUp(void)
{
    DMA_Reset(1);
    platform_set_irq_callback(PLATFORM_CB_IRQ_DMA, DMA_cb_isr, 0);
    test.Next = NULL;
    DMA_PreparePeripheral2RAM(&test, 
                              buff, 
                              SYSCTRL_DMA_PDM, 
                              80, 
                              DMA_ADDRESS_INC, 
                              0 | 1 << 24);
    DMA_EnableChannel(CHANNEL_ID, &test);
}
void audio_input_setup(void)
{
    //GPIO & Pin Ctrl
    PINCTRL_SetPadMux(PDM_PIN_MCLK, IO_SOURCE_PDM_DMIC_MCLK);
    PINCTRL_SetPadMux(PDM_PIN_IN, IO_SOURCE_PDM_DMIC_IN);
    PINCTRL_SelPdmIn(PDM_PIN_IN);

    // PDM clock configuration, 3M
    SYSCTRL_SetAdcClkDiv(8);
    SYSCTRL_SelectTypeAClk(SYSCTRL_ITEM_APB_PDM, SYSCTRL_CLK_ADC_DIV);

    // PDM register configuration
    PDM_Config(APB_PDM, 0, 1, 1, 0, 0);    
    PDM_DmaEnable(APB_PDM, 1, 0);

    // DMA setup
    DMA_SetUp();

    // enable DMA and PDM
    PDM_DmaEnable(APB_PDM, 1, 1);
    PDM_Start(APB_PDM, 1);
}
```

建议采用DMA乒乓搬运的方法进行数据搬运，具体讲解参考手册DMA章节。