# 外设场景

用 `--chip ING916|ING918|ING20 --topic peripheral`，进一步用目标 `pg_*` 限定书籍。签名核对仅在用户提供的 SDK 内进行，不自动调用开发或调试 skill。

完整 SDK 示例汇编在 `references/examples.md`，通过 `--book sdk_examples` 定位相关段落；保留原文及原 SDK 相对链接，版本需另行核实，不通读整份汇编。

| 场景 | 查询词 | 方案必须核实的条件 |
|---|---|---|
| UART 变长收包 | UART、FIFO、timeout、变长 | 帧边界、FIFO 排空、中断清除、缓冲区溢出 |
| SPI / I2C | SPI、IIC、I2C、master、slave | 引脚复用、时钟、模式、地址/片选、超时 |
| GPIO / PWM / Timer | GPIO、PWM、timer、interrupt | 边沿/电平、计数源、极性、清中断语义 |
| ADC | ADC、reference、sampling | 通道与引脚、参考电压、采样条件、换算范围 |
| DMA | DMA、request、descriptor | 目标型号是否支持、请求源、对齐、长度、描述符生命周期 |

每个方案按需核对：时钟/复位→引脚复用→参数→IRQ/DMA→启动→完成和错误处理。不要凭其他芯片经验编造初始化顺序、状态位清除方式或 IRQ 号。

DMA 支持首先查目标芯片手册，不能因其他系列有 DMA 就生成同一方案；证据不足时提出中断/FIFO 备选，并说明待核实条件。

ISR/任务共享数据要说明所有权、长度边界和同步方式；是否需要缓存一致性操作必须依据该芯片及 SDK，不能机械添加。低功耗收包再读取低功耗指南。

给示例时标明目标系列与依据，区分示意流程和已核对签名的代码；未编译、未上板必须如实说明，不写入用户工程。
