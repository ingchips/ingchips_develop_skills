# BLE 协议栈场景

主证据书 `pg_ble_stack_cn`；SDK 集成查 `user_guide`，场景实践查带日期的 `blog`。芯片型号不能替代平台包/协议栈功能版本。

SDK 示例汇编使用 `--book sdk_examples` 检索 `references/examples.md`，只读命中片段；它由用户提供的 DOCX 原样转换，SDK 版本未注明，相对链接保留原 SDK 布局。

| 场景 | 章节入口/关键词 | 给方案前核实 |
|---|---|---|
| 广播与扫描 | ch-adv、ch-scan；advertising、scan | 传统/扩展广播、数据长度、PHY、过滤条件 |
| 连接与多角色 | ch-conn；connection、dual role | 角色、连接数、参数更新流程、断连恢复 |
| GATT 服务与客户端 | ch-gatt-server、ch-gatt-client；notify、indicate、CCCD | 属性权限、订阅状态、MTU、发送完成/拥塞处理 |
| 配对与绑定 | ch-sm；pairing、bonding、security | IO 能力、密钥持久化、权限要求、版本支持 |
| 吞吐与音频/大包 | ch-features、ch-controller；MTU、DLE、PHY、throughput | 参数组合、缓存、发送节奏和对端限制 |
| OTA | blog 的 fota/ota；user_guide | 分区、bootloader、镜像格式、升级协议和断电策略 |

检索参数用 `--topic ble`，需要精确章节时以 `--book pg_ble_stack_cn` 缩小范围。不预设任何 API 名或数据包长度。

开发方案描述初始化→事件/回调→数据处理→异常恢复，点明回调上下文、缓冲区生命周期、连接句柄和返回值处理。证据不完整时给流程伪代码，不把伪代码包装为可直接编译的 SDK 示例。

外设数据上传场景需核实生产速率与 BLE 消费速率、队列上限、丢包/背压策略；不要在中断中直接放入未经核实的协议栈调用。OTA 只做方案说明，不操作 Flash。
