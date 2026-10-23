<!-- pg_power_saving_en: 5 Porting -->

# 5 Porting {#ch-porting}

When using NoOS variants of platform bundles, power saving framework needs to be ported to other RTOS(es). The main work is to port the idle process to the targeting RTOS. The idle process[14](#fn14) looks like this:

```c
void idle_task(void)
{
    for (;;)
    {
        timeout_tick = rtos_next_busy_tick();
        if (platform_pre_suppress_cycles_and_sleep_processing(
          timeout_tick * cycles_per_tick) > some_limit)
        {
            rtos_stop_scheduler();
            platform_pre_sleep_processing();
            platform_post_sleep_processing();
            tick_cnt = how_long_has_I_slept();
            rtos_compensate_system_ticks(tick_cnt);
            restart_system_ticks();
            rtos_resume_scheduler();
        }
        platform_os_idle_resumed_hook();
    }
}
```

What needs to be ported is exactly those `rtos_...` functionalities:

- `rtos_next_busy_tick` returns how many ticks the CPU can be put in sleep modes;
- `rtos_stop_scheduler` stops the scheduler
- `rtos_compensate_system_tick` compensates ticks counter of RTOS
- `rtos_resume_scheduler` resumes the scheduler

`how_long_has_I_slept` calculates how long the last sleep was in ticks which is used to compensates ticks counter of RTOS. The result can be deduced by check system tick registers of CPU, or use other real-time timer including `platform_get_us_time`. `restart_system_tick` restarts system ticks.

Besides, optionally, similar function of `PLATFORM_CFG_RTOS_ENH_TICK` needs to be ported too.

The idle process must be the **only** process having the lowest priority. Some RTOS(es) supported multiple processes have the same lowest priority. Developers should ensure that no other processes are having the lowest priority.

## 5.1 API {#api}

NoOS variants of platform bundles provide a collection of APIs to cooperate the porting [15](#fn15).

```c
// Pre-suppress cycles and sleep processing
// @return  adjusted cycles to sleep
uint32_t platform_pre_suppress_cycles_and_sleep_processing(
  // expected cycles to sleep
  uint32_t expected_cycles
);

// Preprocessing for tick-less sleep
void platform_pre_sleep_processing(void);

// Postprocessing for tick-less sleep
void platform_post_sleep_processing(void);

// Hook for idle task got resumed
void platform_os_idle_resumed_hook(void);
```

## 5.2 Port to FreeRTOS {#port-to-freertos}

FreeRTOS[16](#fn16) is a real-time operating system for micro controllers and small microprocessors. It is a cross-platform RTOS kernel that is distributed freely under the MIT open source license.

Platform binaries that has a built-in RTOS bundles FreeRTOS. NoOS variants are certainly portable to FreeRTOS. The portable can be done by just defining several macros to feed above APIs into FreeRTOS, such as:

```c
#define SYS_CLOCK_CYCLES_PER_TICK   ( configSYSTICK_CLOCK_HZ / configTICK_RATE_HZ )

#define configPRE_SUPPRESS_TICKS_AND_SLEEP_PROCESSING(xExpectedIdleTime)  \
  do {                                                                    \
    xExpectedIdleTime =                                                   \
      platform_pre_suppress_cycles_and_sleep_processing(xExpectedIdleTime \
          * SYS_CLOCK_CYCLES_PER_TICK) / SYS_CLOCK_CYCLES_PER_TICK;       \
  } while (0)
```

A complete example can be found in SDK repository[17](#fn17).

## 5.3 Port to RT-Thread {#port-to-rt-thread}

RT-Thread[18](#fn18) is an open source embedded real-time operating system for IoT devices. It has a small size, rich features, high performance and scalability.

`rtos_...` functionalities can be mapped to relevant RT-Thread APIs as shown in Table [5.1](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#tab:ch-porting-rt-thread).

*Table 5.1: Relevant RT-Thread APIs*
| `rtos_...` Functionalities | RT-Thread APIs |
| --- | --- |
| `rtos_next_busy_tick` | `rt_timer_next_timeout_tick` |
| `rtos_stop_scheduler` | `rt_enter_critical`, `rt_hw_interrupt_disable` |
| `rtos_compensate_system_tick` | `rt_tick_set` |
| `rtos_resume_scheduler` | `rt_exit_critical`, `rt_hw_interrupt_enable` |

A complete example can be found in SDK repository[19](#fn19).

## 5.4 Port to Huawei LiteOS {#port-to-huawei-liteos}

Huawei LiteOS[20](#fn20) was a lightweight real-time operating system for IoT devices developed by Huawei. It was open source, POSIX compliant, and has been incorporated into HarmonyOS.

`rtos_...` functionalities can be mapped to relevant LiteOS APIs as shown in Table [5.2](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#tab:ch-porting-liteos).

*Table 5.2: Relevant LiteOS APIs*
| `rtos_...` Functionalities | LiteOS APIs |
| --- | --- |
| `rtos_next_busy_tick` | `OsSleepTicksGet` |
| `rtos_stop_scheduler` | `LOS_IntLock` |
| `rtos_compensate_system_tick` | `OsSysTimeUpdate` |
| `rtos_resume_scheduler` | `LOS_IntRestore` |

A complete example can be found in SDK repository[21](#fn21).

## 5.5 Port to Azure RTOS ThreadX {#port-to-azure-rtos-threadx}

Azure RTOS ThreadX[22](#fn22) is Microsoft’s Real-Time Operating System (RTOS) for deeply embedded, real-time, and IoT applications. It has a small footprint, fast execution speed, and advanced features such as preemption-threshold scheduling, event chaining.

`rtos_...` functionalities can be mapped to relevant ThreadX APIs as shown in Table [5.3](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#tab:ch-porting-threadx).

*Table 5.3: Relevant ThreadX APIs*
| `rtos_...` Functionalities | ThreadX APIs |
| --- | --- |
| `rtos_next_busy_tick` | `tx_timer_get_next` |
| `rtos_stop_scheduler` | `TX_DISABLE` |
| `rtos_compensate_system_tick` | `tx_time_increment` |
| `rtos_resume_scheduler` | `TX_RESTORE` |

A detailed explanation can be found online[23](#fn23).

## 5.6 Truly No OS {#truly-no-os}

It’s possible to run NoOS bundles without any RTOS, including full functional power saving. A complete example can be found in SDK repository[24](#fn24).

In the example, because there are no software timers, and no next busy tick, the whole idle process couldn’t be simpler:

```c
static void idle_process(void)
{
    uint32_t cycles =
      platform_pre_suppress_cycles_and_sleep_processing((uint32_t)-1);
    if (cycles < 150) return;
    enter_critical();
    platform_pre_sleep_processing();
    platform_post_sleep_processing();
    leave_critical();
    platform_os_idle_resumed_hook();
}
```

---

1. <a id="fn14"></a>Since system tick interrupts are disabled during sleep, it is called tick-less low power feature in some RTOS(es).[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref14)
2. <a id="fn15"></a>`platform_pre_suppress_cycles_and_sleep_processing` is introduced in SDK v8.5.0. For elder SDK versions, use `platform_pre_suppress_ticks_and_sleep_processing` instead.[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref15)
3. <a id="fn16"></a>[https://www.freertos.org/](https://www.freertos.org/)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref16)
4. <a id="fn17"></a>[https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples/peripheral_console_freertos](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples/peripheral_console_freertos)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref17)
5. <a id="fn18"></a>[https://www.rt-thread.io/](https://www.rt-thread.io/)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref18)
6. <a id="fn19"></a>[https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples/peripheral_console_rt-thread](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples/peripheral_console_rt-thread)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref19)
7. <a id="fn20"></a>[https://gitee.com/LiteOS/LiteOS](https://gitee.com/LiteOS/LiteOS)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref20)
8. <a id="fn21"></a>[https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples-gcc/peripheral_console_liteos](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples-gcc/peripheral_console_liteos)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref21)
9. <a id="fn22"></a>[http://docs.microsoft.com/azure/rtos/threadx](http://docs.microsoft.com/azure/rtos/threadx)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref22)
10. <a id="fn23"></a>[https://ingchips.github.io/blog/2022-03-11-threadx-porting/](https://ingchips.github.io/blog/2022-03-11-threadx-porting/)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref23)
11. <a id="fn24"></a>[https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples-gcc/peripheral_console_realtime](https://github.com/ingchips/ING918XX_SDK_SOURCE/tree/master/examples-gcc/peripheral_console_realtime)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-porting.html#fnref24)