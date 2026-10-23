<!-- pg_ing916: 20 定时器（TIMER） -->

# 20 定时器（TIMER） {#ch-timer}

## 20.1 功能概述 {#功能概述-9}

ING916XX系列具有功能完全相同的3个计时器，每个计时器包含两个通道，每个通道支持1个32位计时器， 所以系统中一共有6个32位计时器。既可以用作脉冲宽度调制器(PWM)，也可以用作简单的定时器。

特性：

- 支持AMBA2.0 支持APB总线
- 最多4个多功能定时器
- 提供6种使用场景（定时器和PWM的组合）
- 计时器时钟源可选
- 计时器可以暂停

## 20.2 使用说明 {#使用说明-10}

### 20.2.1 设置TIMER工作模式 {#设置timer工作模式}

使用 `TMR_SetOpMode` 设置TIMER的工作模式。

```c
void TMR_SetOpMode(
  TMR_TypeDef *pTMR,      //定时器外设地址
  uint8_t ch_id,          //通道ID
  uint8_t op_mode,        //工作模式
  uint8_t clk_mode,       //时钟模式
  uint8_t pwm_park_value
  );
```

关于 `TMR_SetOpMode` 中的参数 `pwm_park_value` 的值将影响PWM的输出：

- 若为0：通道被禁用时，PWM输出为低电平；通道启用时，较低周期的PWM计数器先计数；
- 若为1：通道被禁用时，PWM输出为高电平；通道启用时，较高周期的PWM计数器先计数；

TIMER具有6种不同的工作模式，可以大致分为三类：定时器功能、PWM功能、（定时器+PWM）组合功能。

- 定时器功能

  32位定时器可以分别作为1个32位定时器、2个16位定时器、4个8位定时器，定义如下所示。

  ```c
    #define TMR_CTL_OP_MODE_32BIT_TIMER_x1            1  // one 32bit timer
    #define TMR_CTL_OP_MODE_16BIT_TIMER_x2            2  // dual 16bit timers
    #define TMR_CTL_OP_MODE_8BIT_TIMER_x4             3  // four 8bit timers
  ```
- 脉冲宽度调制器功能

  定时器的本质其实是计数器，所以可以拆分为2个16位的计数器来产生PWM信号。

  ```c
    #define TMR_CTL_OP_MODE_16BIT_PWM                 4  // PWM with two 16bit counters
  ```
- 组合功能

  定时器与PWM的功能可以组合使用，对应的组合方式有两种：1）一个8bitPWM和一个16位计时器； 2）一个8位PWM和两个8位计时器。

  ```c
    #define TMR_CTL_OP_MODE_8BIT_PWM_16BIT_TIMER_x1   6   // MIXED: PWM with two 8bit counters + one 16bit timer
    #define TMR_CTL_OP_MODE_8BIT_PWM_8BIT_TIMER_x2    7   // MIXED: PWM with two 8bit counters + dual 8bit timer
  ```

**注意:** 要更改当前工作的定时器通道模式，必须先禁用该通道,然后将通道设置为新模式并启用它。

TIMER的时钟源有两种，分别是内部时钟和外部时钟，定义如下所示。

```c
  #define TMR_CLK_MODE_EXTERNAL                     0   //external clock
  #define TMR_CLK_MODE_APB                          1   //internal clock
```

### 20.2.2 获取时钟频率 {#获取时钟频率}

使用 `TMR_GetClk` 获取TIMER某个通道的时钟频率。

```c
uint32_t TMR_GetClk(
  TMR_TypeDef *pTMR,
  uint8_t ch_id
  );
```

### 20.2.3 重载值 {#重载值}

使用 `TMR_SetReload` 设置 TIMER 某个通道的重载值。

```c
void TMR_SetReload(
  TMR_TypeDef *pTMR,
  uint8_t ch_id,      //通道ID
  uint32_t value
  );
```

在不同的TIMER模式中， `value` 的值分配如下表。 Table: (#tab:ch-timer-value-distribute)

| TIMER模式 | bits[0:7] | bits[8:15] | bits[16:23] | bits[24:31] |
| --- | --- | --- | --- | --- |
| TMR_CTL_OP_MODE_32BIT_TIMER_x1 |  |  |  |  |
| TMR_CTL_OP_MODE_16BIT_TIMER_x2 |  |  |  |  |
| TMR_CTL_OP_MODE_8BIT_TIMER_x4 | Timer0 | Timer1 | Timer2 |  |
| TMR_CTL_OP_MODE_16BIT_PWM |  |  |  |  |
| TMR_CTL_OP_MODE_8BIT_PWM_16BIT_TIMER_x1 | PWM low period | PWM high period |  |  |
| TMR_CTL_OP_MODE_8BIT_PWM_8BIT_TIMER_x2 | Timer0 | Timer1 | PWM low period | PWM high period |

关于上述格中分配的重载值有两点说明： * 定时器模式下，某个 Timer 在其（重载值 + 1）个计数周期产生一次中断； * PWM模式下， 高周期和低周期的频率值分别是对应重载值 + 1。

### 20.2.4 使能TIMER {#使能timer}

使用 `TMR_Enable` 使能对应通道上的一个或多个timer。

```c
void TMR_Enable(
  TMR_TypeDef *pTMR,
  uint8_t ch_id,
  uint8_t mask  //比特 0 为 1 配置TIMER0
                //比特 1 为 1 配置TIMER1
                //比特 2 为 1 配置TIMER2
                //比特 3 为 1 配置TIMER3
  );
```

注意，如果相应的通道 **不存在** 或在通道模式中它 **不是一个有效的设备** ，则定时器或PWM不能被启用。 例如，当0号通道设置为32位定时器模式时，0号通道的Timer 1不能使能。

### 20.2.5 获取TIMER的比较值 {#获取timer的比较值}

使用 `TMR_GetCMP` 获取定时器的比较输出。

```c
uint32_t TMR_GetCMP(
  TMR_TypeDef *pTMR,
  uint8_t ch_id
  );
```

### 20.2.6 获取TIMER的计数器值 {#获取timer的计数器值}

使用 `TMR_GetCNT` 获取定时器的计数值。

```c
uint32_t TMR_GetCNT(
  TMR_TypeDef *pTMR,
  uint8_t ch_id
  );
```

### 20.2.7 计时器暂停 {#计时器暂停}

使用 `TMR_PauseEnable` 可以将计时器暂停，计时器的counter将保持当前的计数值，取消暂停之后将恢复计数。

```c
void TMR_PauseEnable(
  TMR_TypeDef *pTMR,
  uint8_t enable
  );
```

### 20.2.8 配置中断请求 {#配置中断请求-2}

使用 `TMR_IntEnable` 配置并使能TIMER中断。

```c
void TMR_IntEnable(
  TMR_TypeDef *pTMR,
  uint8_t ch_id,
  uint8_t mask
  );
```

### 20.2.9 处理中断状态 {#处理中断状态-2}

使用 `TMR_IntHappened` 一次性获取某个通道上所有 Timer （最多 4 个 Timer ）的中断触发状态，返回非 0 值表示该 Timer 上产生了中断请求。第 n 比特（第 0 比特为最低比特）对应 Timer n 上的中断触发状态。

```c
uint8_t TMR_IntHappened (
  TMR_TypeDef *pTMR,
  uint8_t ch_id
  );
```

使用 `TMR_IntClr` 可以一次性清除某个通道上所有定时器的中断状态。

```c
void TMR_IntClr(
  TMR_TypeDef *pTMR,
  uint8_t ch_id,
  uint8_t mask  //比特 0 为 1 清除对应通道上的 Timer0
                //比特 1 为 1 清除对应通道上的 Timer1
                //比特 2 为 1 清除对应通道上的 Timer2
                //比特 3 为 1 清除对应通道上的 Timer3
  );
```

## 20.3 使用示例 {#使用示例}

### 20.3.1 使用计时器功能及暂停功能 {#使用计时器功能及暂停功能}

将TIMER1的通道0设置为`TMR_CTL_OP_MODE_32BIT_TIMER_x1`模式，并设定每1秒产生一次中断：

```c
  TMR_SetOpMode(APB_TMR1, 0, TMR_CTL_OP_MODE_32BIT_TIMER_x1, TMR_CLK_MODE_APB, 0);
  TMR_SetReload(APB_TMR1, 0, TMR_GetClk(APB_TMR1, 0));  //4999
  TMR_Enable(APB_TMR1, 0, 0xf);
  TMR_IntEnable(APB_TMR1, 0, 0xf);
```

### 20.3.2 使用TIMER的PWM功能 {#使用timer的pwm功能}

将TIMER1的通道0的工作模式设置为 `TMR_CTL_OP_MODE_16BIT_PWM` ，并使用13号引脚输出10HzPWM信号。

```c
  #define PIN_TMR_PWM 13

  static void setup_peripheral_timer(void)
  {
    SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ITEM_APB_SysCtrl)
                              |(1 << SYSCTRL_ITEM_APB_PinCtrl)
                              |(1 << SYSCTRL_ITEM_APB_TMR1));

    SYSCTRL_SelectTimerClk(TMR_PORT_1, SYSCTRL_CLK_32k);
    TMR_SetOpMode(APB_TMR1, TMR_CTL_OP_MODE_16BIT_PWM, TMR_CLK_MODE_EXTERNAL, 0);
    TMR_SetReload(APB_TMR1, 0, 0x00090009); // 9 9
    TMR_Enable(APB_TMR1, 0, 0xf);

    PINCTRL_SetPadMux(PIN_TMR_PWM, IO_SOURCE_TIMER1_PWM0_B);
  }
```

### 20.3.3 通道0产生2个周期性中断 {#通道0产生2个周期性中断}

使用TIMER1通道0生成2个中断:一个用于每1000个APB时钟周期，另一个用于每3000个APB周期。

```c
  static void setup_peripheral_timer(void)
  {
    SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ITEM_APB_SysCtrl)
                              |(1 << SYSCTRL_ITEM_APB_PinCtrl)
                              |(1 << SYSCTRL_ITEM_APB_TMR1));

    SYSCTRL_SelectTimerClk(TMR_PORT_1, SYSCTRL_CLK_32k);
    TMR_SetOpMode(APB_TMR1, 0, TMR_CTL_OP_MODE_16BIT_TIMER_x2, TMR_CLK_MODE_APB, 0);
    TMR_SetReload(APB_TMR1, 0, 0x0BB703E7);  // 2999  999

    TMR_IntEnable(APB_TMR1, 0, 0x3);  //Ch0Int0 Ch0Int1
    TMR_Enable(APB_TMR1, 0, 0x3);     //Ch0TMR0En Ch0TMR1En
  }
```

### 20.3.4 产生2路对齐的PWM信号 {#产生2路对齐的pwm信号}

使用TIMER1的通道0和通道1分别生成两路PWM信号PWM0和PWM1，对应参数设置如下所示： PWM0:周期= 30个外部时钟周期，占空比= 1/3 PWM1:周期= 60个外部时钟周期，占空比= 1/3 将两路PWM对齐，并分别由引脚13、14输出。

```c
  #define PIN_TMR_PWM0 13
  #define PIN_TMR_PWM1 14

  static void setup_peripheral_timer(void)
  {
    SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ITEM_APB_SysCtrl)
                              |(1 << SYSCTRL_ITEM_APB_PinCtrl)
                              |(1 << SYSCTRL_ITEM_APB_TMR1));

    SYSCTRL_SelectTimerClk(TMR_PORT_1, SYSCTRL_CLK_32k);

    TMR_SetOpMode(APB_TMR1, 0, TMR_CTL_OP_MODE_16BIT_PWM, TMR_CLK_MODE_EXTERNAL, 1);
    TMR_SetOpMode(APB_TMR1, 1, TMR_CTL_OP_MODE_16BIT_PWM, TMR_CLK_MODE_EXTERNAL, 1);
    TMR_SetReload(APB_TMR1, 0, 0x00090013);   //9   19
    TMR_SetReload(APB_TMR1, 1, 0x00130027);   //19  39
    TMR_Enable(APB_TMR1, 0, 0xf);
    TMR_Enable(APB_TMR1, 1, 0xf);

    PINCTRL_SetPadMux(PIN_TMR_PWM0, IO_SOURCE_TIMER1_PWM0_B);
    PINCTRL_SetPadMux(PIN_TMR_PWM1, IO_SOURCE_TIMER1_PWM1_A);
  }
```