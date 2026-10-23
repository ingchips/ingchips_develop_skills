<!-- an_libaudio_cn: 2 概览 -->

# 2 概览 {#ch-overview}

音频处理库包含一组音频处理模块，开发者可以根据需要选用其中的模块，以获得高品质的音频体验。本音频处理库是免费附送的，以预编译库的形式提供。

本音频处理库只能运行于以下芯片：

- ING916XX

## 2.1 模块设计原则 {#模块设计原则}

为了适配资源紧张的嵌入式系统，本音频处理库在设计时遵循下列原则。

- 内存管理

  音频处理往往涉及较大量的数据处理，需要较多的内存。考虑到嵌入式系统的特点，内存由开发者负责分配， 库内的模块可以完全不使用堆（`malloc`/`free`），而且不会从栈上分配大块内存。

  各模块采用面向对象式的接口，需要销毁对象时，直接释放为对象分配的内存即可，无需其它操作， 因此皆未提供专门的销毁接口。
- 线程安全性

  如无特殊说明，一个模块的多个实例可以并发执行。

  一个实例只能在一个线程内使用。如果需要在多个线程中操作某一个实例，必须使用同步机制，避免对同一个实例的并发操作。

## 2.2 依赖关系 {#依赖关系}

音频处理库依赖于 CMSIS-DSP[1](#fn1) v1.15.0 及以上。以 Keil μVision 为例， 打开 “Manage Run-time Environment”，将 CMSIS-DSP 添加到项目。

音频库支持多种编译器。每种编译器提供两种版本，一为开启硬件单精度浮点运算，库文件带有 `_f` 后缀；一为不开启硬件单精度浮点运算，库文件不带有 `_f` 后缀。

- ING916XX

  开启硬件单精度浮点运算时，GCC 版本使用的编译选项为：

  ```
  -mthumb -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard
  ```

  不开启硬件单精度浮点运算时，GCC 版本使用的编译选项为：

  ```
  -mthumb -mcpu=cortex-m4
  ```

## 2.3 缩略语及术语 {#缩略语及术语}

*表 2.1: 缩略语*
| 缩略语 | 说明 |
| --- | --- |
| ADC | 模数转换器（Analog-to-Digital Converter） |
| ADPCM | 自适应脉冲编码调制（ADaptive Pulse Coded Modulation） |
| AMR-WB | 自适应多速率-宽带（Adaptive Multi-Rate WideBand） |
| CMSIS | 微控制器软件接口标准（Common Microcontroller Software Interface Standard） |
| mSBC | 改良低复杂度子带编解码器（modified low complexity SubBand Codec） |
| PCM | 脉冲编码调制（Pulse Coded Modulation） |
| SBC | 低复杂度子带编解码器（low complexity SubBand Codec） |
| TTS | 文本转语音（Text-To-Speech） |

*表 2.2: 术语*
| 术语 | 说明 |
| --- | --- |
| Opus | 一个完全开放、免版税、用途广泛的音频编解码器 |

## 2.4 参考文档 {#参考文档}

1. ING916XX 系列芯片数据手册[2](#fn2)
2. SBC 技术规范[3](#fn3)
3. Opus 交互式音频编解码器[4](#fn4)
4. 汉典[5](#fn5)

---

1. <a id="fn1"></a>[https://github.com/ARM-software/CMSIS-DSP](https://github.com/ARM-software/CMSIS-DSP)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-overview.html#fnref1)
2. <a id="fn2"></a>[http://www.ingchips.com/product/70.html](http://www.ingchips.com/product/70.html)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-overview.html#fnref2)
3. <a id="fn3"></a>[https://www.bluetooth.org/DocMan/handlers/DownloadDoc.ashx?doc_id=544797](https://www.bluetooth.org/DocMan/handlers/DownloadDoc.ashx?doc_id=544797)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-overview.html#fnref3)
4. <a id="fn4"></a>[https://opus-codec.org](https://opus-codec.org)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-overview.html#fnref4)
5. <a id="fn5"></a>[https://www.zdic.net](https://www.zdic.net)[↩︎](https://ingchips.github.io/application-notes/an_libaudio_cn/ch-overview.html#fnref5)