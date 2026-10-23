<!-- pg_ing918: 12 定时器和看门狗 -->

# 12 定时器和看门狗 {#ch-timer}

## 12.1 功能概述 {#功能概述-5}

ING918xx系列有三个定时器：`Timer0`、`Timer1`和`Timer2`。三个定时器功能基本相同，可以实现定时、比较等功能。唯一的区别在于，`Timer0` 可以用作看门狗。

### 12.1.1 计时器功能 {#计时器功能}

用作计时器时，主要实现了以下功能：

- 用作32位递增计数器或32位比较器。
- 可以设置为普通模式、一次性模式和自由模式：

  - 普通模式（`TMR_CTL_OP_MODE_WRAPPING`）——计数器以恒定间隔产生中断，在达到比较计数器中的比较值后重置为0，并继续计数，这是默认采用的模式。
  - 一次性模式（`TMR_CTL_OP_MODE_ONESHOT`）——当计数器增长到等于比较器的值时，定时器会禁用，直到下次主动启用它。
  - 自由模式（`TMR_CTL_OP_MODE_FREERUN`）——计数器达到定时器中的值时不会停止，而是会一直递加到最大值（`0xffffffff`)，之后重置为零，并继续计数。
- 可以根据设置产生中断。

### 12.1.2 WATCHDOG的功能 {#watchdog的功能}

`Timer0`可以用作看门狗，设定一定的延时时间，在此时间内，如果程序没有主动喂狗，则会发生重启。

看门狗可以在程序跑飞时，让程序复位。

## 12.2 TIMER使用说明 {#timer使用说明}

### 12.2.1 获取Timer计数值 {#获取timer计数值}

可以通过`TMR_GetCNT` 获取计数器的当前计数值。

```
uint32_t TMR_GetCNT(TMR_TypeDef *pTMR);
```

`pTMR` ：可以设置为`APB_TMR0`、`APB_TMR1`、`APB_TMR2`,对应`Timer0`、`Timer1`和`Timer2`。

注意计数器只有使能后，计数值才会随着程序的运行递加，如果计数器未使能，计数值是不变的。

### 12.2.2 TIMER计数值清零 {#timer计数值清零}

可以通过`TMR_Reload` 将计数器的当前计数值清零。

```
void TMR_Reload(TMR_TypeDef *pTMR);
```

### 12.2.3 设置TIMER的比较值 {#设置timer的比较值}

可以通过`TMR_SetCMP` 设置计数器的比较值。

```
void TMR_SetCMP(TMR_TypeDef *pTMR, uint32_t value);
```

`pTMR` ：选择要设置的计数器，`APB_TMR0`、`APB_TMR1`或`APB_TMR2`；

`value` ：设置的比较值。

### 12.2.4 获取TIMER的比较值 {#获取timer的比较值}

使用`TMR_GetCMP` 获取计数器的比较值；

```
uint32_t TMR_GetCMP(TMR_TypeDef *pTMR);
```

### 12.2.5 使能TIMER {#使能timer}

通过`TMR_Enable` 使能计数器。

```
void TMR_Enable(TMR_TypeDef *pTMR);
```

计数器使能之后，计数值才会随着时钟的运行递增。

### 12.2.6 禁能TIMER {#禁能timer}

通过`TMR_Disable` 禁能计数器。

```
void TMR_Disable(TMR_TypeDef *pTMR);
```

### 12.2.7 设置TIMER的工作模式 {#设置timer的工作模式}

通过`TMR_SetOpMode` 设置计数器的工作模式。

```
void TMR_SetOpMode(TMR_TypeDef *pTMR, uint8_t mode);
```

三种模式的定义如下：

```
#define TMR_CTL_OP_MODE_WRAPPING            0
#define TMR_CTL_OP_MODE_ONESHOT             1
#define TMR_CTL_OP_MODE_FREERUN             2
```

具体说明见[上文](https://ingchips.github.io/drafts/pg_ing918/ch-timer.html#function)。

### 12.2.8 使能TIMER中断 {#使能timer中断}

通过`TMR_IntEnable` 使能中断，使能中断后计时器计数值达到比较值后，会触发中断。

```
void TMR_IntEnable(TMR_TypeDef *pTMR);
```

### 12.2.9 禁能TIMER中断 {#禁能timer中断}

通过`TMR_IntDisable`禁能计数器的中断。

```
void TMR_IntDisable(TMR_TypeDef *pTMR);
```

### 12.2.10 清除TIMER中断请求 {#清除timer中断请求}

通过`TMR_IntDisable` 清除计数器的中断请求。注意，进入中断处理函数之后，要第一时间清除中断请求，不然可能会重复触发中断。

```
void TMR_IntDisable(TMR_TypeDef *pTMR);
```

### 12.2.11 获得TIMER的中断状态 {#获得timer的中断状态}

通过`TMR_IntHappened` 来获取计数器的中断状态。

```
uint8_t TMR_IntHappened(TMR_TypeDef *pTMR);
```

## 12.3 TIMER中断使用流程 {#timer中断使用流程}

- 配置对应`Timer`的时钟，下面的代码中配置了三个`Timer`的时钟，使用时可以根据自己使用的`Timer`进行配置。

  ```
  SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ClkGate_APB_TMR0)

                                     | (1 << SYSCTRL_ClkGate_APB_TMR1)

                           | (1 << SYSCTRL_ClkGate_APB_TMR2));
  ```
- 对`Timer`进行初始化，以`Timer1`为例。

  ```
      TMR_SetCMP(APB_TMR1, TMR_CLK_FREQ);
      TMR_SetOpMode(APB_TMR1, TMR_CTL_OP_MODE_WRAPPING);
      TMR_Reload(APB_TMR1);
      TMR_IntEnable(APB_TMR1);
  ```

  上面四条语句分别设置了定时器的比较值，设置工作模式，将定时器的当前计数值清零，并使能中断。
- 注册中断处理函数。

  ```
  platform_set_irq_callback(PLATFORM_CB_IRQ_TIMER1, hr_timer1_isr, NULL);
  ```

  `hr_timer1_isr`为`Timer1`的中断处理函数。
- 编写中断处理函数。

  ```
  uint32_t hr_timer1_isr(void *user_data)
  {
      TMR_IntClr(APB_TMR1);
      //user code
      return 0;
  }
  ```

  需要注意，中断处理函数中，要优先清理对应的中断请求。

## 12.4 Watchdog使用说明 {#watchdog使用说明}

看门狗（`Watchdog` )与`Timer0` 共用一套计数器，看门狗没有使能时，`Timer0` 与`Timer1` 、`Timer2`的使用没有区别，当看门狗使能时，`Timer0`就不再起作用。

### 12.4.1 使能看门狗 {#使能看门狗}

通过`TMR_WatchDogEnable`使能看门狗。

```
void TMR_WatchDogEnable(uint32_t timeout);
```

`timeout`：设置看门狗的超时时间。

### 12.4.2 停用看门狗 {#停用看门狗}

通过`MR_WatchDogDisable`禁能看门狗。

```
void TMR_WatchDogDisable(void);
```

### 12.4.3 喂狗 {#喂狗}

通过`TMR_WatchDogRestart` 定期喂狗，如果没有在看门狗的超时之前喂狗，程序会发生重启。

这种情况下发生的重启仅能通过硬件重置（`POR`或者`RESETN`)清除，在其他复位条件下不会清除，可以帮助启动程序检查最近一次复位发生的原因。