<!-- pg_ble_stack_cn: 2 简介 -->

# 2 简介 {#ch-intro}

欢迎使用 *INGCHIPS* 918XX/916XX/ING20XX 软件开发工具包 （SDK）.

本手册将带您了解 *INGCHIPS* 各系列 BLE SoC 芯片上的低功耗蓝牙开发，了解整个协议栈设计思路， 熟悉各模块主要接口的使用方法。

本手册侧重从开发者的角度介绍 BLE 的开发，涉及 BLE 规范时采用了更“实用化”的描述， 不去关注规范里的每一个细节。

SDK 工具可以生成本手册里提到的一些常见代码，如回调函数、事件处理等。

## 2.1 缩略语及术语 {#缩略语及术语}

*表 2.1: 缩略语*
| 缩略语 | 说明 |
| --- | --- |
| BLE | 低功耗蓝牙（Bluetooth LE，Bluetooth Low Engergy） |
| CCCD | 客户端特征配置描述符（Client Characteristic Configuration Descriptor） |
| CTE | 定频扩展（Constant Tone Extension） |
| ECC | 椭圆曲线密码学（Elliptic Curve Cryptography） |
| HCI | Host Controller 接口 |
| IRK | 身份解析密钥 (Identity Resolving Key) |
| L2CAP | 逻辑链路控制与适配协议（Logical Link Control and Adaptation Protocol） |
| LL | 链路层（Link Layer） |
| LMP | BR/EDR 的链路管理协议（Link Manager Protocol） |
| LTK | 长期密钥（Long Term Key） |
| MIC | 消息认证码（Message Integrity Code） |
| MITM | 中间人（Man-In-The-Middle） |
| OOB | 带外（Out Of Band） |
| RSSI | 接收信号强度指示（Received Signal Strength Indicator） |
| SCA | 睡眠时钟精度（Sleep Clock Accuracy） |
| SPSM | 简化的协议/服务选择器(Simplified Protocol/Service Multiplexer) |
| UUID | 通用唯一识别码（Universally Unique IDentifier） |

*表 2.2: 术语*
| 术语 | 说明 |
| --- | --- |
| 1M | BLE 使用的一种 PHY，符号速率为 1Msps |
| 2M | BLE 使用的一种 PHY，符号速率为 2Msps |
| Characteristic | 特征，是服务的组成部分 |
| Coded | BLE 使用的一种 PHY，基于卷积码的信道编码 |
| Controller | BLE 控制器，整个蓝牙协议栈偏低层的部分 |
| Handle | 句柄 |
| Host | BLE 主机，整个蓝牙协议栈偏上层的部分 |
| PHY | BLE 的物理层传输方式 |
| Service | 服务，由特征组成 |

蓝牙规范从 v5.3 版本开始更新了部分术语，本手册沿用旧称。表 [2.3](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-intro.html#tab:ch0-new-term) 是这部分术语的新旧对照。

*表 2.3: 新旧术语对照*
| 原名称 | 新名称 | 本手册 |
| --- | --- | --- |
| Master | Central | 主角色 |
| Slave | Peripheral | 从角色 |
| White List | Accept List | 白名单 |

## 2.2 参考文档 {#参考文档}

1. Bluetooth SIG[1](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn1)
2. Controller API Reference
3. Application Note: Direction Finding Solution[2](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn2)

---

1. <a id="fn1"></a>[https://www.bluetooth.com/](https://www.bluetooth.com/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-intro.html#fnref1)
2. <a id="fn2"></a>[https://ingchips.github.io/application-notes/an_aoa/index.html](https://ingchips.github.io/application-notes/an_aoa/index.html)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-intro.html#fnref2)