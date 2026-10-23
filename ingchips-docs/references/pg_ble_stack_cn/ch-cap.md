<!-- pg_ble_stack_cn: 15 协议栈能力 -->

# 15 协议栈能力 {#ch-cap}

对于不同的软件包、不同的芯片系列，协议栈能力不同，汇总[76](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn76)于表 [15.1](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#tab:ch99-typical-stack-cap)，表 [15.2](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#tab:ch99-mass-conn-stack-cap)，表 [15.3](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#tab:ch99-mini-stack-cap) 和 表 [15.4](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#tab:ch99-rom-stack-cap)。

*表 15.1: {typical, extension, exp} 软件包协议栈能力*
| 系列 | 广播集数目 | 连接数目 | 白名单容量 | CTE | 最大 MTU |
| --- | --- | --- | --- | --- | --- |
| ING9188X | 8 | 8 | 16 | \checkmark | 247 |
| ING9187X | 8 | 8 | 16 | 247 |  |
| ING9168X | 5 | 5 | 8 | \checkmark | 247 |
| ING20X | 3 | 3 | 4 | \checkmark | 247 |

*表 15.2: {mass_conn} 软件包协议栈能力*
| 系列 | 广播集数目 | 连接数目 | 白名单容量 | CTE | 最大 MTU |
| --- | --- | --- | --- | --- | --- |
| ING9188X | 8 | 26 | 24 | \checkmark | 247 |
| ING9187X | 8 | 26 | 24 | 247 |  |
| ING9168X | 5 | 10 | 10 | \checkmark | 247 |
| ING20X | 5 | 5 | 5 | \checkmark | 247 |

*表 15.3: {mini} 软件包协议栈能力*
| 系列 | 广播集数目 | 连接数目 | 白名单容量 | CTE | 最大 MTU |
| --- | --- | --- | --- | --- | --- |
| ING9188X | 1 | 1 | 4 | \checkmark | 247 |
| ING9187X | 1 | 1 | 4 | 247 |  |
| ING9168X | 1 | 1 | 4 | \checkmark | 247 |
| ING20X | 1 | 1 | 4 | \checkmark | 247 |

*表 15.4: {rom} 软件包协议栈能力*
| 系列 | 广播集数目 | 连接数目 | 白名单容量 | CTE | 最大 MTU |
| --- | --- | --- | --- | --- | --- |
| ING20X | 5 | 5 | 5 | \checkmark | 247 |

其中，ING20X 的 *rom* 软件包功能类似 *extension* 软件包，但协议栈能力类似 *mass_conn* 软件包。

通过 `ll_get_capabilities` 和 `btstack_get_capabilities` 可分别获取链路层和 Host 的协议栈能力[77](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn77)。

---

1. <a id="fn1"></a>[https://www.bluetooth.com/](https://www.bluetooth.com/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-intro.html#fnref1)
2. <a id="fn2"></a>[https://ingchips.github.io/application-notes/an_aoa/index.html](https://ingchips.github.io/application-notes/an_aoa/index.html)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-intro.html#fnref2)
3. <a id="fn3"></a>特殊情况下，Controller、Host 也可以融合到一起运行，请参考 SDK 示例 *Peripheral Console (Real-time)*。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref3)
4. <a id="fn4"></a>FreeRTOS 提供了 `uxTaskPriorityGet`、`vTaskPrioritySet` 等，用于查询和修改优先级。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref4)
5. <a id="fn5"></a>如无特殊说明，本文档中的 App 皆指运行在芯片上的蓝牙程序。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref5)
6. <a id="fn6"></a>指示服务器端主动报告特征的值。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref6)
7. <a id="fn7"></a>[https://www.bluetooth.com/16-bit-uuids-for-sdos/](https://www.bluetooth.com/16-bit-uuids-for-sdos/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref7)
8. <a id="fn8"></a>私有事件（如 HCI_SUBEVENT_LE_VENDOR_PRO_CONNECTIONLESS_IQ_REPORT）除外。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref8)
9. <a id="fn9"></a>Core Specification Supplement, Part B, Common Profile and Service Error Codes[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref9)
10. <a id="fn10"></a>更准确地说，只是把一条 HCI 消息放入消息队列。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref10)
11. <a id="fn11"></a>[https://ingchips.github.io/blog/2021-01-25-zig-async/](https://ingchips.github.io/blog/2021-01-25-zig-async/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref11)
12. <a id="fn12"></a>地址改变后，曾与之配对的设备无法自动重连。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref12)
13. <a id="fn13"></a>参照蓝牙核心规范。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref13)
14. <a id="fn14"></a>ING918 芯片家族不支持此特性。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-overview.html#fnref14)
15. <a id="fn15"></a>称为一个 PDU 队列（train）。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref15)
16. <a id="fn16"></a>AuxPtr 里的时间偏移略有不同。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref16)
17. <a id="fn17"></a>将原始编号再映射到当前的信道集合得到实际的信道号。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref17)
18. <a id="fn18"></a>Periodic Advertising Sync Transfer。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref18)
19. <a id="fn19"></a>SDK v9.0.1 或更新版本。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref19)
20. <a id="fn20"></a>PAwR 每个子事件、每个响应都只包含一个数据包，不支持 PDU 队列。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref20)
21. <a id="fn21"></a>[https://github.com/ingchips/ING918XX_SDK_SOURCE/blob/75cbf9928711c39e0b234ae11796bc1696111998/bundles/typical/inc/platform_api.h#L265](https://github.com/ingchips/ING918XX_SDK_SOURCE/blob/75cbf9928711c39e0b234ae11796bc1696111998/bundles/typical/inc/platform_api.h#L265)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref21)
22. <a id="fn22"></a>旧版本下可以由 Host 随机更新 RPA，一般由软件实现，所以功率比用 Controller 实现功耗高。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-features.html#fnref22)
23. <a id="fn23"></a>广播间隔小于 3.75ms。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-adv.html#fnref23)
24. <a id="fn24"></a>在不引起混淆的前提下，本手册混用“广播”、“广播集”这两个名词。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-adv.html#fnref24)
25. <a id="fn25"></a>请参阅 SDK 用户手册。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-adv.html#fnref25)
26. <a id="fn26"></a>关闭之后，其它设备无法再与该周期广播建立同步。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-adv.html#fnref26)
27. <a id="fn27"></a>后两种策略在规范中称为 Extended filter policy。ING916 和 ING918 不支持后两种策略。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-scan.html#fnref27)
28. <a id="fn28"></a>即周期性地接收周期广播。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-scan.html#fnref28)
29. <a id="fn29"></a>需要连接多个设备，使用白名单方式效率更高。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-conn.html#fnref29)
30. <a id="fn30"></a>参考 《Controller API Reference》。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-conn.html#fnref30)
31. <a id="fn31"></a>对于 v8.2 以下版本，这个函数仅用于主角色， 从角色需要使用 `l2cap_request_connection_parameter_update` 请求更新。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-conn.html#fnref31)
32. <a id="fn32"></a>调用之前建议先检查对方是否支持此特性。此 API 无论主从角色都可以调用。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-conn.html#fnref32)
33. <a id="fn33"></a>在不引起混淆的前提下，本手册混用 ATT 服务器、GATT 服务器，代码里也用 `att_server` 代指 `gatt_server`。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref33)
34. <a id="fn34"></a>事实上，这几件事已由 Wizard 工具代劳。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref34)
35. <a id="fn35"></a>在手册、工具、代码的不同位置可能使用了不同的名词，如 Profile 数据库、GATT 数据库、GATT 数据等。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref35)
36. <a id="fn36"></a>协议栈里称为“会话”，规范里称为“队列”。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref36)
37. <a id="fn37"></a>仅适用于有响应的写入，无响应的写入无效。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref37)
38. <a id="fn38"></a>解决方法参考 [L2CAP 传输队列](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#ch-i2cap-tx-queue)。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref38)
39. <a id="fn39"></a>解决方法参考 [L2CAP 传输队列](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#ch-i2cap-tx-queue)。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#fnref39)
40. <a id="fn40"></a>以及转发过来的 `L2CAP_EVENT_CAN_SEND_NOW` 事件。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-client.html#fnref40)
41. <a id="fn41"></a>SDK v8.4.23 及以上版本。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-client.html#fnref41)
42. <a id="fn42"></a>SDK v8.4.23 及以上版本。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-client.html#fnref42)
43. <a id="fn43"></a>5.1 及更低版本里称为 LE_PSM[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref43)
44. <a id="fn44"></a>整个 SDU 只占用一个 K 帧[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref44)
45. <a id="fn45"></a>整个 SDU 占用多个 K 帧 这个事件对应其中一个 K 帧[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref45)
46. <a id="fn46"></a>指进入链路层发送队列。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref46)
47. <a id="fn47"></a>当信用点用完或者链路层队列已满时，会出现此情况[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref47)
48. <a id="fn48"></a>`att_server_request_can_send_now_event` 是基于 `att_dispatch_server_request_can_send_now_event` 实现的。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref48)
49. <a id="fn49"></a>生成时需要保证具有足够高的熵。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref49)
50. <a id="fn50"></a>IRK、DHK、LTK、CSRK 等的具体含义及作用请参考蓝牙核心规范。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref50)
51. <a id="fn51"></a>以及给予用户必要的提示的能力。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref51)
52. <a id="fn52"></a>没必要过于频繁地更新地址。尤其是对于可解析地址，每更新一次，就意味着泄露了一点关于 IRK 的消息。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref52)
53. <a id="fn53"></a>注意：当该广播是可连接的并且正在广播时，不允许修改地址。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref53)
54. <a id="fn54"></a>[https://www.bluetooth.com/learn-about-bluetooth/key-attributes/bluetooth-security/method-vulnerability/](https://www.bluetooth.com/learn-about-bluetooth/key-attributes/bluetooth-security/method-vulnerability/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref54)
55. <a id="fn55"></a>dx.doi.org/10.6028/NIST.FIPS.186-4[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref55)
56. <a id="fn56"></a>BLUETOOTH CORE SPECIFICATION Version 5.4 | Vol 3, Part H, 2.3.6[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-sm.html#fnref56)
57. <a id="fn57"></a>典型值。不同软件包有所不同。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref57)
58. <a id="fn58"></a>更多信息请参考《Application Note: Direction Finding Solution》, [https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2](https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref58)
59. <a id="fn59"></a>ING918 不支持此功能。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref59)
60. <a id="fn60"></a>关于原理、使用方法等更多信息请参考《使用 ING916 定位传统蓝牙设备》，[https://ingchips.github.io/blog/2023-03-11-legacy-aoa/](https://ingchips.github.io/blog/2023-03-11-legacy-aoa/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref60)
61. <a id="fn61"></a>更多信息请参考《Application Note: Direction Finding Solution》, [https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2](https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#proprietary-solution-2)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref61)
62. <a id="fn62"></a>本节功能中，ING918 仅支持自定义连接间隔。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref62)
63. <a id="fn63"></a>参见蓝牙核心规范 Vol 3, Part H, 2.3.5.6 LE Secure Connections pairing phase 2.[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-controller.html#fnref63)
64. <a id="fn64"></a>参考《Application Note: Direction Finding Solution》。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref64)
65. <a id="fn65"></a>参考《Controller API Reference》。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref65)
66. <a id="fn66"></a>参考《Controller API Reference》。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref66)
67. <a id="fn67"></a>为防止与 Media Access Controller 混淆，蓝牙规范使用 MIC 代替 MAC。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref67)
68. <a id="fn68"></a>[https://ingchips.github.io/blog/2021-06-02-sdk-6/#%E5%85%BC%E5%AE%B9%E6%80%A7](https://ingchips.github.io/blog/2021-06-02-sdk-6/#%E5%85%BC%E5%AE%B9%E6%80%A7)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref68)
69. <a id="fn69"></a>只能在 `app_main` 就调用。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref69)
70. <a id="fn70"></a>对于 v8.4.12 或更旧的版本，所能存储的设备个数等于软件包所支持的连接数目。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref70)
71. <a id="fn71"></a>为多个连接创建多个同步执行器的优势在于多个 GATT 客户端上的会话可以并发。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref71)
72. <a id="fn72"></a>由规范规定。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref72)
73. <a id="fn73"></a>[https://www.bluetooth.com/specifications/assigned-numbers/](https://www.bluetooth.com/specifications/assigned-numbers/)[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref73)
74. <a id="fn74"></a>这个函数的原始版本不是严格意义上的异步操作。考虑到在一个同步执行体内可能既会用到有响应的写入，也会用到无响应的写入，加入这个 API 可以带来便利。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref74)
75. <a id="fn75"></a>可以使用 `btstack_push_user_runnable`。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-misc.html#fnref75)
76. <a id="fn76"></a>依据 SDK v9.0.0。ING916XX 协议栈能力可能发生变化。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fnref76)
77. <a id="fn77"></a>限 SDK v8.4.13 或更高版本。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fnref77)

---

1. <a id="fn76"></a>依据 SDK v9.0.0。ING916XX 协议栈能力可能发生变化。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fnref76)
2. <a id="fn77"></a>限 SDK v8.4.13 或更高版本。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fnref77)