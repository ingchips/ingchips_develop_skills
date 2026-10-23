<!-- pg_ing918: 3 模数转换器（ADC） -->

# 3 模数转换器（ADC） {#ch-adc}

ADC 特性：

- 最多有5个通道AIN0~AIN4
- 10位分辨率
- 输入范围0~3.6V
- 支持采样率3/16MHz、3/32MHz、3/64MHz、3/128MHz
- 支持单端输入转换模式
- 支持环路转换模式，每个通道可以启用或禁用

## 3.1 ADC 工作模式 {#adc-工作模式}

ADC 有两种工作模式：单次模式和循环模式。

```c
#define ADC_MODE_SINGLE     1
#define ADC_MODE_LOOP       0
void ADC_SetMode(const uint8_t mode);
```

### 3.1.1 单次模式：ADC_MODE_SINGLE {#单次模式adc_mode_single}

单次模式只能使能一个通道，如果使能多个通道，只有第一个通道为有效通道，完成后ADC将停止，数据可用，知道重置ADC控制器。

### 3.1.2 循环模式：ADC_MODE_LOOP {#循环模式adc_mode_loop}

循环模式需要配置一个控制环路延迟：

```c
void ADC_SetLoopDelay(const uint32_t delay);
```

一旦 ADC 任务开始，它将逐个从启用的通道中采样输入电压。完成一个循环后，循环延迟将启动停止 ADC，直到延迟时间结束，然后下一个循环将开始。数据每个循环都会更新。

## 3.2 ADC 采样数率 {#adc-采样数率}

ADC 支持四种采样率 3/16MHz、3/32MHz、3/64MHz、3/128MHz。

```c
#define ADC_CLK_16      0
#define ADC_CLK_32      1
#define ADC_CLK_64      2
#define ADC_CLK_128     3
#define ADC_CLK_EN      0x4
/** \brief Set ADC clock selection
 *  Note that: remeber to include ADC_CLK_EN.
 */
void ADC_SetClkSel(const uint8_t clk_sel);
```

## 3.3 ADC 校准 {#adc-校准}

如果ADC采样计算得到的结果和实际值偏差比较大，可以对ADC校准，使用校准后的值计算。

### 3.3.1 ADC 校准预处理 {#adc-校准预处理}

```c
enum adc_cali_method
{
    ADC_CALI_METHOD_1 = 1,      // calibration is done in factory
    ADC_CALI_METHOD_2,          // calibration is done in factory
    ADC_CALI_METHOD_SELF        // self-calibration
};
enum adc_cali_method adc_prepare_calibration(void);
```

在主程序内预处理一次即可，该函数会判断当前芯片是否经过校准，如果未经校准会自动校准并将校准后的数据保存到flash里；如果已经校准则跳过校准过程。

### 3.3.2 ADC 读取校准后的值 {#adc-读取校准后的值}

```c
enum adc_sample_mode
{
    ADC_SAMPLE_MODE_SLOW,       // for ADC_CLK_128
    ADC_SAMPLE_MODE_FAST,       // for ADC_CLK_16
};
uint16_t adc_calibrate(enum adc_sample_mode mode, uint8_t channel_id,
                       uint16_t value);
```

value是adc采样的原始值，该函数查表计算后，返回校准后的值。

## 3.4 ADC 综合示例 {#adc-综合示例}

读取ADC数据：

```c
uint16_t read_adc(uint8_t channel)
{
    SYSCTRL_WaitForLDO();

    ADC_Reset();
    ADC_PowerCtrl(1);

    ADC_SetClkSel(ADC_CLK_EN | ADC_CLK_128);
    ADC_SetMode(ADC_MODE_LOOP);
    ADC_EnableChannel(channel == 0 ? 1 : 0, 1);
    ADC_EnableChannel(channel, 1);
    ADC_Enable(1);

    while (ADC_IsChannelDataValid(channel) == 0) ;
    uint16_t voltage = ADC_ReadChannelData(channel);

    ADC_ClearChannelDataValid(channel);
    while (ADC_IsChannelDataValid(channel) == 0) ;
    voltage = ADC_ReadChannelData(channel);

    ADC_Enable(0);
    ADC_PowerCtrl(0);

    return adc_calibrate(ADC_SAMPLE_MODE_SLOW, channel, voltage);
}
```

主函数：

```c
int app_main()
{

    setup_peripherals();

    platform_set_evt_callback(PLATFORM_CB_EVT_PUTC,
                              (f_platform_evt_cb)cb_putc, NULL);

    platform_set_evt_callback(PLATFORM_CB_EVT_PROFILE_INIT, setup_profile, NULL);

    platform_set_irq_callback(PLATFORM_CB_IRQ_TIMER1, timer_isr, NULL);

    adc_prepare_calibration();

    printf("U = %d\n", read_adc(ADC_CHANNEL));

    return 0;
}
```