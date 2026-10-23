<!-- pg_ing20: 3 ADC简介 -->

# 3 ADC简介 {#ch-adc}

ADC全称Analog-to-Digital Converter，即模数转换器。

其主要作用是通过PIN测量电压，并将采集到的电压模拟信号转换成数字信号。

## 3.1 功能描述 {#功能描述}

### 3.1.1 特点 {#特点}

- 最多10个单端输入通道
- 12位分辨率
- 电压输入范围（0~VBAT）
- 支持APB总线
- 采样频率可编程
- 支持单一转换模式和连续转换模式
- 支持对输入电压进行1/2采样

### 3.1.2 ADC模式 {#adc模式}

- 校准模式（calibration）：用于校准精度。
- 转换模式（conversion）：用于正常工作状态下的模数转换。

根据ADC输入模式完成对应的模式校准，之后在转换模式下进行正常模数转换。

### 3.1.3 ADC输入模式 {#adc输入模式}

- 单端输入（single-ended）：使用单个输入引脚，采样ADC内部的参考电压；

### 3.1.4 ADC转换模式 {#adc转换模式}

- 单次转换（single）：ADC完成单次转换后，ADC将停止，数据将被拉入 `FIFO`；
- 连续转换（continuous）：ADC经过 loop-delay 时间后循环进行转换，直到手动关闭。

### 3.1.5 ADC通道 {#adc通道}

ADC共10个channel，即ch0-ch9。

其中ch0-ch8为通用通道。CH9连接用于计算VBAT。

**ch0、ch1两个通道默认对输入电压进行1/2分压，且不可配置，对较低电压采样精准度较差。**

具体通道的输入连接引脚如下：

*表 3.1: ADC输入连接引脚*
| 通道 | 连接引脚 |
| --- | --- |
| ch0 | GPIO7 |
| ch1 | GPIO8 |
| ch2 | GPIO9 |
| ch3 | GPIO10 |
| ch4 | GPIO30 |
| ch5 | GPIO31 |
| ch6 | GPIO34 |
| ch7 | GPIO35 |
| ch8 | GPIO15 |
| ch9 | VBAT |

以下是关于ADC通道对于开发者的几点使用建议：

**1.** 在使能通道前请先配置ADC输入模式；

**2.** 如需切换ADC输入模式，建议调用ADC_DisableAllChannels关闭之前模式下所有已使能通道，重新使能新的通道；

### 3.1.6 采样率 {#采样率}

采样率和时钟、loop-delay大小以及使能通道个数有关，其计算关系如下：

当loop-delay=0时：SAMPLERATE = \frac{ADC\_CLK}{16\times{CH\_NUM}}

当loop-delay>0时：SAMPLERATE = \frac{ADC\_CLK}{loop\_delay+16\times{CH\_NUM}+5}

## 3.2 使用方法 {#使用方法}

### 3.2.1 时钟配置 {#时钟配置}

当前ADC所用时钟源为 `clock slow` 经过分频得到的ADC工作时钟。

当前ADC工作时钟可以配置范围为500K-8M。

### 3.2.2 ADC参数配置 {#adc参数配置}

ADC参数配置接口的函数声明如下：

```c
void ADC_ConvCfg(SADC_adcCtrlMode ctrlMode,
                 SADC_channelId ch,
                 uint8_t enNum,
                 uint8_t dmaEnNum,
                 uint32_t loopDelay);
```

涉及参数有：ADC转换模式、采样通道、data触发中断数、data触发DMA搬运数、ADC输入模式和 `loop-delay`。

具体的参数取值范围请参考ADC头文件里对应的枚举定义或参数说明。

data触发中断数和data触发DMA搬运数决定了搬运ADC数据的方式。前者用触发中断的方式，后者用触发DMA搬运的方式。

**注意：** data触发中断数和data触发DMA搬运数应该一个为0，一个非0,。如果两值都非0则默认选择触发中断的方式，DMA配置不生效；

关于搬运方式的建议：

- 一般在小数据量情况下，如定时采集温度、电池电压，建议采用触发中断并CPU读数的方式。
- 一般大数据量连续采样，如模拟麦克风采样，建议采用DMA搬运方式（乒乓搬运），可以大大提高数据搬运处理效率。

**注意：** 多次调用ADC_ConvCfg则以最后一次调用为准（除通道使能，不会自动关闭之前已使能的通道），如只需使能（关闭）ADC通道可以通过ADC_EnableChannel接口完成。

### 3.2.3 ADC数据处理 {#adc数据处理}

ADC数据处理的推荐步骤为：

**1.** 调用ADC_PopFifoData（或DMA搬运buff）读取FIFO中的ADC原始数据；

**2.** 调用ADC_GetDataChannel得到原始数据中的数据所属通道（如需要）；

**3.** 调用ADC_GetData得到原始数据中的ADC数据；

也可以通过调用ADC_ReadChannelData接口直接得到指定通道的ADC数据，但这样会丢弃其他通道数据，请谨慎使用。其可以作为辅助接口使用，非主要方式。

对于单个数据的读取我们建议采用取若干数据求其平均值的方式，可以明显提高数据稳定性。

我们提供了方便开发者移植的**求平均值程序**，如有需求请参考SDK例程peripheral_battery。

## 3.3 编程指南 {#编程指南}

### 3.3.1 驱动接口 {#驱动接口}

ADC控制：

- ADC_Reset：ADC复位
- ADC_Start：ADC使能
- ADC_AdcClose：ADC关闭

ADC配置：

- ADC_ConvCfg：ADC转换参数配置
- ADC_EnableChannel：通道使能
- ADC_DisableAllChannels：关闭所有通道

数据处理相关：

- ADC_GetFifoEmpty：读取FIFO是否为空
- ADC_PopFifoData：读取FIFO原始数据
- ADC_GetDataChannel：读取原始数据中通道号
- ADC_GetData：读取原始数据中ADC数据
- ADC_ReadChannelData：读取特定通道ADC数据（注意：该接口会丢弃其他通道数据）
- ADC_ClrFifo：清空FIFO
- ADC_HardwareCalibration: 硬件校准，ADC模块每次重新使能都需要调用硬件校准函数
- ADC_GetCalibValueVRefVBat: 获取经过校准后的ADC的值。
- ADC_GetVBatVoltage: 获取Vbat的当前电压值

以上是ADC常用接口，还有部分接口不推荐直接使用，在此不进行罗列，详见头文件声明。

### 3.3.2 代码示例 {#代码示例}

下面展示ADC的基本用法：

（注：以下ADC参数设置仅供参考，具体参数请结合实际需要进行配置）

#### 3.3.2.1 单次中断搬运 {#单次中断搬运}

```c
#define ADC_CHANNEL    ADC_CH_0
#define ADC_CLK_MHZ    6

static uint32_t ADC_cb_isr(void *user_data)
{
    uint32_t data = ADC_PopFifoData();
    float calib_data;
    SADC_channelId channel = ADC_GetDataChannel(data);
    if (channel == ADC_CHANNEL) {
        uint16_t sample = ADC_GetData(data);
        calib_data = ADC_GetCalibValueVRefVBat(ADC_CHANNEL, sample);
        // do something with 'sample'
    }
    return 0;
}

void adc_init(void)
{
    SYSCTRL_ClearClkGate(SYSCTRL_ITEM_APB_ADC);
    SYSCTRL_SetAdcClkDiv(24 / ADC_CLK_MHZ);
    SYSCTRL_ReleaseBlock(SYSCTRL_ITEM_APB_ADC);
    ADC_Reset();
    ADC_ConvCfg(SINGLE_MODE, ADC_CHANNEL, 0, 0, 0);
    platform_set_irq_callback(PLATFORM_CB_IRQ_SADC, ADC_cb_isr, 0);
    ADC_Start(1);
}
```