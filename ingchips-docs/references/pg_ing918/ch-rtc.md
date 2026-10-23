<!-- pg_ing918: 9 实时时钟（RTC） -->

# 9 实时时钟（RTC） {#ch-rtc}

## 9.1 功能概述 {#功能概述-3}

实时时钟（`RTC`）是一个独立的48位定时器，相较于普通`TIMER`，`RTC`精度低，同时功耗也会降低，适用于功耗敏感、对于精度要求不高的应用场景。

## 9.2 接口说明 {#接口说明}

### 9.2.1 RTC使能/禁止 {#rtc使能禁止}

使用`RTC_Enable`使能或者禁止`RTC`。

```
void RTC_Enable(const uint8_t flag);
```

函数根据`flag`的值来执行操作:

- `flag`为0时，禁止`RTC` ；
- `flag`不为0时，使能`RTC`。

`RTC` 使能后，只要不进行禁能，就会根据设置的初始计数值进行递减，计数器递减为0后发生中断，这时只要设置新的计数值，RTC就会马上按照新的计数值进行计时。

### 9.2.2 获取RTC当前值 {#获取rtc当前值}

可以使用`RTC_Current` 读取`RTC`低32位的当前计数值，用`RTC_CurrentFull` 读取全部48位的当前计数值。

```
uint32_t RTC_Current(void);
uint64_t RTC_CurrentFull(void);
```

### 9.2.3 设置中断的计数值 {#设置中断的计数值}

通过`RTC_SetNextIntOffset`设置`RTC`中断的计数值。

```
void RTC_SetNextIntOffset(const uint32_t offset);
```

注意`RTC`使用的时钟为`32.768K`，因此计数值设置为`32768`时，`RTC`的中断时间恰好为1s，可以据此设置中断时间。

### 9.2.4 清RTC中断 {#清rtc中断}

使用`RTC_ClearInt`来清除当前的`RTC` 中断状态，以备下一次使用。

```
void RTC_ClearInt(void);
```

## 9.3 RTC中断使用流程 {#rtc中断使用流程}

- 首先，定义一个中断处理函数`rtc_timer_isr` (名字可以根据需要自己定义）。

  ```
  uint32_t rtc_timer_isr(void *user_data)
  {
      RTC_ClearInt();//清中断状态
      RTC_SetNextIntOffset(32768 * 10);//设置中断计数值
      //这里可以添加用户自己的代码
      return 0;
  }
  ```

  可以通过`user_data`给中断传递参数，这通常作为一个预留功能，不常用到。
- 然后，通过`platform_set_irq_callback` 注册中断：

  ```
  platform_set_irq_callback(PLATFORM_CB_IRQ_RTC, rtc_timer_isr, NULL);
  ```
- 接下来，设置中断时间并使能`RTC` ，时间到后，中断会触发。

  ```
  RTC_SetNextIntOffset(32768 * 10);
  RTC_Enable(RTC_ENABLED);
  ```
- 这里注意，在使用`RTC`时，最好先通过`RTC_SetNextIntOffset`设置好计数值，再进行使能，这样RTC此次计数时间处于可控状态。
- 在RTC计数过程中，随时都可以使用`RTC_SetNextIntOffset` 进行计数值的设置，设置完成后，新值会马上覆盖旧值，`RTC` 会按照新值开始进行计时。