<!-- pg_power_saving_en: 2 Introduction -->

# 2 Introduction {#ch-intro}

Welcome to use *INGCHIPS* 918/916 Software Development Kit.

Power saving is important in Bluetooth LE products, especially for those using batteries. This document is a guide for developing low power products from the perspective of software.

Roughly speaking, the goal of power saving is, when there is something to do, to design the system carefully to reduce power consumption; when there is nothing to do, to put the system into special modes to reduce power consumption. The latter one is covered by the power saving [Framework](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-framework.html#ch-framework), while the former one is briefly discussed in [Tips on Low Power System](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-tips.html#ch-tips).

## 2.1 Abbreviations & Terminology {#abbreviations-terminology}

*Table 2.1: Abbreviations*
| Abbreviation | Notes |
| --- | --- |
| BLE | Bluetooth Low Energy |
| CPU | Central Processing Unit |
| IRQ | Interrupt Request |
| QSPI | Quad Serial Peripheral Interface |
| RAM | Random Access Memory |
| ROM | Read Only Memory |
| RTOS | Real-time Operating System kernel |
| SDK | Software Development Kit |

*Table 2.2: Terminology*
| Terminology | Notes |
| --- | --- |
| Cache | A small but fast memory that stores copies of data from frequently used main memory locations |
| Flash | An electronic non-volatile computer storage medium |
| FreeRTOS | A real-time operating system kernel |
| ISR | Interrupt Service Routine |
| KiB | 1024 Bytes |
| Share memory | Memory in SoC that can be accessed by BLE sub-system (shared by BLE and CPU sub-systems) |
| System memory | Memory in SoC that can be accessed by CPU sub-system, but not BLE sub-system. It is starting from 0x20000000. |
| System tick | A system timer that can be used to generate periodic interrupts or measure time |
| Real-time clock | The clock that keeps running in power saving modes |

## 2.2 References {#references}

1. FreeRTOS[1](#fn1)
2. Mastering the FreeRTOS™ Real Time Kernel[2](#fn2)

---

1. <a id="fn1"></a>[https://freertos.org](https://freertos.org)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-intro.html#fnref1)
2. <a id="fn2"></a>[https://www.freertos.org/Documentation/161204_Mastering_the_FreeRTOS_Real_Time_Kernel-A_Hands-On_Tutorial_Guide.pdf](https://www.freertos.org/Documentation/161204_Mastering_the_FreeRTOS_Real_Time_Kernel-A_Hands-On_Tutorial_Guide.pdf)[↩︎](https://ingchips.github.io/application-notes/pg_power_saving_en/ch-intro.html#fnref2)