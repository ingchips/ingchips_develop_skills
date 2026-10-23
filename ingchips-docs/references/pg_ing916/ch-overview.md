<!-- pg_ing916: 2 概览 -->

# 2 概览 {#ch-overview}

欢迎使用 *INGCHIPS* 918xx/916xx 软件开发工具包 （SDK）.

ING916XX 系列芯片支持蓝牙 5.3 规范，内置高性能 32bit RISC MCU（支持 DSP 和 FPU）、Flash、低功耗 PMU， 以及丰富的外设、高性能低功耗 BLE RF 收发机。

本文介绍 SoC 外设及其开发方法。每个章节介绍一种外设，各种外设与芯片数据手册之外设一一对应， 基于 API 的兼容性、避免误解等因素，存在以下例外：

- PINCTRL 对应于数据手册之 IOMUX
- PCAP 对应于数据手册之 PCM
- SYSCTRL 是一个“虚拟”外设，负责管理各种 SoC 功能，组合了几种相关的硬件模块

SDK 外设驱动的源代码开放，其中包含很多常数，而且几乎没有注释 —— 这是有意为之，开发者只需要关注头文件，而不要尝试修改源代码。

## 2.1 缩略语及术语 {#缩略语及术语}

*表 2.1: 缩略语*
| 缩略语 | 说明 |
| --- | --- |
| ADC | 模数转换器（Analog-to-Digital Converter） |
| DMA | 直接存储器访问（Direct Memory Access） |
| EFUSE | 电编程熔丝（Electronic Fuses） |
| FIFO | 先进先出队列（First In First Out） |
| FOTA | 固件空中升级（Firmware Over-The-Air） |
| GPIO | 通用输入输出（General-Purpose Input/Output） |
| I2C | 集成电路间总线（Inter-Integrated Circuit） |
| I2S | 集成电路音频总线（Inter-IC Sound） |
| IR | 红外线（Infrared） |
| PCAP | 脉冲捕捉（Pulse CAPture） |
| PDM | 脉冲密度调制（Pulse Density Modulation） |
| PLL | 锁相环（Phase Locked Loop） |
| PTE | 外设触发引擎（Peripheral Trigger Engine） |
| PWM | 脉宽调制信号（Pulse Width Modulation） |
| QDEC | 正交解码器（Quadrature Decoder） |
| RTC | 实时时钟（Real-time Clock） |
| SPI | 串行外设接口（Serial Peripheral Interface） |
| UART | 通用异步收发器（Universal Asynchronous Receiver/Transmitter） |
| USB | 通用串行总线（Universal Serial Bus） |

## 2.2 参考文档 {#参考文档}

1. Bluetooth SIG[1](#fn1)
2. ING916XX 系列芯片数据手册[2](#fn2)

---

1. <a id="fn1"></a>[https://www.bluetooth.com/](https://www.bluetooth.com/)[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-overview.html#fnref1)
2. <a id="fn2"></a>[http://www.ingchips.com/product/70.html](http://www.ingchips.com/product/70.html)[↩︎](https://ingchips.github.io/drafts/pg_ing916/ch-overview.html#fnref2)