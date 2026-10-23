<!-- pg_ing918: 2 概览 -->

# 2 概览 {#ch-overview}

欢迎使用 *INGCHIPS* 918xx/916xx 软件开发工具包 （SDK）.

ING918XX 系列芯片支持蓝牙 5.0/5.1 规范，内置高性能 32bit RISC MCU、Flash，以及丰富的外设、 高性能低功耗 BLE RF 收发机。BLE 发射功率。

本文介绍 SoC 外设及其开发方法。每个章节介绍一种外设，各种外设与芯片数据手册之外设一一对应， 但存在以下例外：

- SYSCTRL 是一个“虚拟”外设，负责管理各种 SoC 功能，组合了几种相关的硬件模块

SDK 外设驱动的源代码开放，其中包含很多常数，而且几乎没有注释 —— 这是有意为之，开发者只需要关注头文件，而不要尝试修改源代码。

ING918xx 包含不同的封装、型号。本手册适用于 ING918xx 系列芯片的所有封装、型号。

## 2.1 缩略语及术语 {#缩略语及术语}

*表 2.1: 缩略语*
| 缩略语 | 说明 |
| --- | --- |
| ADC | 模数转换器（Analog-to-Digital Converter） |
| FIFO | 先进先出队列（First In First Out） |
| GPIO | 通用输入输出（General-Purpose Input/Output） |
| I2C | 集成电路间总线（Inter-Integrated Circuit） |
| PWM | 脉宽调制信号（Pulse Width Modulation） |
| RTC | 实时时钟（Real-time Clock） |
| SPI | 串行外设接口（Serial Peripheral Interface） |
| UART | 通用异步收发器（Universal Asynchronous Receiver/Transmitter） |
| 参考文档 |  |

1. Bluetooth SIG[1](#fn1)
2. ING918XX 系列芯片数据手册

---

1. <a id="fn1"></a>[https://www.bluetooth.com/](https://www.bluetooth.com/)[↩︎](https://ingchips.github.io/drafts/pg_ing918/ch-overview.html#fnref1)