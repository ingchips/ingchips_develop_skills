<!-- pg_ing916: 17 实时时钟（RTC） -->

# 17 实时时钟（RTC） {#ch-rtc}

## 17.1 功能描述 {#功能描述-6}

实时时钟是一个独立的定时器。RTC模块拥有一组连续计数的计数器，在相应的软件配置下， 可提供时钟日历的功能。修改计数器的值可以重新设置系统当前的时间和日期。

特性：

- 可配置计数器大小
- 周期性中断包括半秒、秒、分钟、小时和天
- 可编程报警中断
- 硬件数字微调补偿外部时钟源频偏

## 17.2 使用说明 {#使用说明-7}

### 17.2.1 RTC使能 {#rtc使能}

使用 `RTC_Enable` 使能RTC。

```c
void RTC_Enable(
  uint8_t enable  // 使能(1)/禁用(0)
  );
```

### 17.2.2 获取当前时间 {#获取当前时间}

使用 `RTC_GetTime` 获取当前时间，该函数的参数可以读取对应的时、分、秒， 函数的返回值即为RTC使能后所经历的天数 `day`。

```c
uint16_t RTC_GetTime(
  uint8_t *hour,    //时
  uint8_t *minute,  //分
  uint8_t *second   //秒
  );
```

### 17.2.3 修改时间 {#修改时间}

使用 `RTC_ModifyTime` 修改当前时间，其中的 `day` 表示RTC使能后所经过的天数。

```c
void RTC_ModifyTime(
  uint16_t day,   //天数
  uint8_t hour,
  uint8_t minute,
  uint8_t second
  );
```

修改时间后，需要使用 `RTC_IsModificationDone` 获取当前修正是否已经同步到RTC时钟域， 返回值为 `1` 表示已经同步完毕，`0` 则表示正在更新。

```c
int RTC_IsModificationDone(void);
```

### 17.2.4 获取RTC Counter值 {#获取rtc-counter值}

使用 `RTC_Current` 可以获取RTC Counter值的低32bit。

```c
uint32_t RTC_Current(void);
```

使用 `RTC_CurrentFull` 可以获取RTC Counter值的全部43bit。

```c
uint64_t RTC_CurrentFull(void);
```

### 17.2.5 配置闹钟 {#配置闹钟}

使用 `RTC_ConfigAlarm`

```c
void RTC_ConfigAlarm(
  uint8_t hour,
  uint8_t minute,
  uint8_t second
  );
```

### 17.2.6 配置中断请求 {#配置中断请求-1}

使用 `RTC_EnableIRQ` 配置并使能RTC中断请求。

```c
void RTC_EnableIRQ(
uint32_t mask   //比特 2 为 1 时使能alarm中断
                //比特 3 为 1 时使能day中断
                //比特 4 为 1 时使能hour中断
                //比特 5 为 1 时使能minute中断
                //比特 6 为 1 时使能second中断
                //比特 7 为 1 时使能half-second中断
);
```

RTC支持的中断类型一共6种：

```c
typedef enum
{
    RTC_IRQ_ALARM = 0x04,       //alarm中断
    RTC_IRQ_DAY = 0x08,         //day中断
    RTC_IRQ_HOUR = 0x10,        //hour中断
    RTC_IRQ_MINUTE = 0x20,      //minute中断
    RTC_IRQ_SECOND = 0x40,      //second中断
    RTC_IRQ_HALF_SECOND = 0x80, //half-second中断
} rtc_irq_t;
```

上述所提到的六种中断中，alarm中断通过调用 `RTC_ConfigAlarm` 设定alarm时间， 其余中断的出发时间均是固定的，依次为：1天、1小时、1分钟、1秒钟和半秒钟。

- 例如使能 RTC 设的alarm中断，并设定alarm时间的01:45:20

  ```c
  RTC_EnableIRQ(RTC_IRQ_ALARM);
  RTC_ConfigAlarm(0x1,0x2d,0x14);
  RTC_Enable(1);
  ```
- 例如使能 RTC 的day中断

  ```c
  RTC_EnableIRQ(RTC_IRQ_DAY);
  RTC_Enable(1);
  ```

### 17.2.7 获取当前中断状态 {#获取当前中断状态}

使用 `RTC_GetIntState` 获取当前RTC的中断状态。

```c
uint32_t RTC_GetIntState(void);
```

### 17.2.8 清除中断 {#清除中断}

使用 `RTC_ClearIntState` 清除当前RTC的中断状态。

```c
void RTC_ClearIntState(
  uint32_t state    //比特 2 为 1 时清除alarm中断
                    //比特 3 为 1 时清除day中断
                    //比特 4 为 1 时清除hour中断
                    //比特 5 为 1 时清除minute中断
                    //比特 6 为 1 时清除second中断
                    //比特 7 为 1 时清除half-second中断
  );
```

### 17.2.9 处理中断状态 {#处理中断状态-1}

用 `RTC_GetIntState` 获取RTC上的中断触发，返回非 0 值表示 RTC 上产生了中断请求。 RTC产生中断后， 需要消除中断状态方可再次触发。利用 `RTC_ClearIntState`可清除RTC的中断触发状态。

### 17.2.10 睡眠唤醒源 {#睡眠唤醒源-1}

RTC 支持作为低功耗状态的唤醒源：RTC的闹钟唤醒信号在 `RTC_ConfigAlarm` 指定的时间将系统唤醒。 使用 `RTC_EnableDeepSleepWakeupSource` 使能 RTC 的唤醒功能。

```c
void RTC_EnableDeepSleepWakeupSource(
  uint8_t enable    //使能(1)/禁用(0)
);
```

### 17.2.11 数字调校 {#数字调校}

RTC 由外部 32kHz 时钟源驱动，其脉冲发生器产生内部 1Hz 脉冲以增加其时间计数器。 如果外部时钟频率不是准确的 32768Hz，则内部产生的 1Hz 脉冲的周期也不准确。数字微调功能可以补偿这些不准确性。

通过 `RTC_Trim` 就可以根据 32kHz 时钟源实际的频率情况进行数字微调：

```c
int RTC_Trim(uint32_t cali_value);
```

这里的 `cali_value` 为 32kHz 时钟源的校准值，可通过 `platform_read_info(PLATFORM_INFO_32K_CALI_VALUE)` 获取。