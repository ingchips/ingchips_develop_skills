<!-- pg_ing20: 20 RTIMER简介 （Reduce Timer） -->

# 20 RTIMER简介 （Reduce Timer） {#ch-rtimer}

RTIME是Reduce Timer（递减定时器）的缩写，ING20XX系列芯片提供了两个简单的递减计数器模块。 该模块结构简单，仅支持向下计数，仅支持定时计数。可应用于简单的定时计数场景。

**注意：FWLib中为方便表述将所有代码归类到peripheral_timer.c文件中。为了表述一致，将RTIMER0和RTIMER1分别表述为为TIMER2和TIMER3。**

例如：RTIMER的platform注册回调命名和寄存器基地址如下表述.

```c
typedef enum
{
...
    PLATFORM_CB_IRQ_RTIMER0,
    PLATFORM_CB_IRQ_RTIMER1,
...
} platform_irq_callback_type_t;

...
#define APB_RTIMER0           ((RTMR_TypeDef *)APB_RTIMER0_BASE)
#define APB_RTIMER1           ((RTMR_TypeDef *)APB_RTIMER1_BASE)
...
```

## 20.1 功能描述 {#功能描述-5}

### 20.1.1 特性 {#特性-2}

- 32位增量计数器和32位比较寄存器
- 支持三种工作模式：连续回绕、自由运行、单次模式
- 中断支持

### 20.1.2 工作模式 {#工作模式}

具有三种工作模式：

- 连续回绕（Continuous Wrapping Mode）

  定时器开始运行，并将计数器的值（Counter）和比较值（Compare）进行对比，当定时器值小于比较值时，触发中断和数值重载。
- 自由运行

  与自动回绕模式的区别主要是在计数到比较直的时候不会自动重载数值，而是继续递减计数到0再溢出重新计数，可通过获取cnt支持，标定固定周期的定时器时间戳。
- 单次模式

  定时器开始运行，并将计数器的值（Counter）和比较值（Compare）进行对比，当定时器值小于比较值时，触发中断，并停止计数，即定时器只运行一次就停止。

## 20.2 使用方法 {#使用方法-5}

### 20.2.1 API参考 {#api参考}

初始化RTMR工作模式，RTMR支持WRAPPING、ONESHOT、FREERUN三种工作模式，用户可根据需求选择合适的工作模式。

```c
// timer work mode
#define TMR_CTL_OP_MODE_WRAPPING            0            // 0 - continuous wrapping mode
#define TMR_CTL_OP_MODE_ONESHOT             1            // 1 - one-stop mode
#define TMR_CTL_OP_MODE_FREERUN             2            // 2 - continuous free-run mode
void RTMR_SetOpMode(RTMR_TypeDef *pTMR, uint8_t mode);
```

设置RTMR比较值，比较值是定时器的停止条件参考，除freerun模式，用户要根据自己的定时器工作频率和需要的计时时间计算对应的比较早。

**注意递减计数器值从0递减，需要设定的定时时间值（cnt）为（0xffff - cnt）**

```c
void RTMR_SetCompare(RTMR_TypeDef *pTMR, uint32_t cnt);
```

获取当前计数值，用户在定时器运行过程中可以通过获取当前cnt计数值，，来获取当前时间戳。

```c
uint32_t RTMR_GetCNT(RTMR_TypeDef *pTMR);
```

复位当前定时器计数值，手动停止计数器或计数器初始化时推荐调用，防止定时器初值不为0造成定时时间偏差。

```c
void RTMR_Reload(RTMR_TypeDef *pTMR);
```

定时器使能停止。可通过接口控制定时器的启动和停止。

```c
void RTMR_Enable(RTMR_TypeDef *pTMR);
void RTMR_Disable(RTMR_TypeDef *pTMR);
```

定时器中断控制，可通过接口打开和关闭对应中断。

```c
void RTMR_IntEnable(RTMR_TypeDef *pTMR);
void RTMR_IntDisable(RTMR_TypeDef *pTMR);
```

### 20.2.2 使用示例 {#使用示例-1}

使用自动回绕模式周期触发定时器。

```c
static uint32_t rtimer_callback(void *user_data)
{
    if(RTMR_IntHappened(APB_RTIMER0))
    {
        printf("rtimer int\r\n");
        RTMR_IntClr(APB_RTIMER0);
    }

}

void rtimer_init(void)
{
    SYSCTRL_ClearClkGateMulti(1 << SYSCTRL_ClkGate_APB_RTMR2);
    RTMR_SetCMP(APB_RTIMER0, 0xffffffff - getpll_clk() / 1000);
    RTMR_SetOpMode(APB_RTIMER0, TMR_CTL_OP_MODE_WRAPPING);
    RTMR_Reload(APB_RTIMER0);
    platform_set_irq_callback(PLATFORM_CB_IRQ_RTIMER0, rtimer_callback, 0);
    RTMR_IntEnable(APB_RTIMER0);
}
```

使用单次模式计数一次并触发中断

```c
static uint32_t rtimer_callback(void *user_data)
{
    if(RTMR_IntHappened(APB_RTIMER0))
    {
        printf("rtimer int\r\n");
        RTMR_IntClr(APB_RTIMER0);
    }

}

void rtimer_init(void)
{
    SYSCTRL_ClearClkGateMulti(1 << SYSCTRL_ClkGate_APB_RTMR2);
    RTMR_SetCMP(APB_RTIMER0, 0xffffffff - getpll_clk() / 1000);
    RTMR_SetOpMode(APB_RTIMER0, TMR_CTL_OP_MODE_ONESHOT);
    RTMR_Reload(APB_RTIMER0);
    platform_set_irq_callback(PLATFORM_CB_IRQ_RTIMER0, rtimer_callback, 0);
    RTMR_IntEnable(APB_RTIMER0);
}
```