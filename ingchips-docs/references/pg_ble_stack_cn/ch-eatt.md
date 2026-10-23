<!-- pg_ble_stack_cn: 13 Enhanced ATT Bearer -->

# 13 Enhanced ATT Bearer {#ch-eatt}

**EATT**（Enhanced Attribute Protocol Transport）是 Bluetooth Core Specification 5.2 引入的重要特性，通过在单一 LE 连接上建立多个并行的 ATT Bearer 通道，突破了传统 BLE GATT 的串行传输限制，显著提升数据吞吐率和系统实时性。

**核心改进**：从单通道 ATT Bearer（CID 0x0004）→ 多通道 EATT Bearer（CID 0x0040-0x007F）

## 13.1 传统 ATT 的局限性 {#传统-att-的局限性}

传统 BLE 的问题：所有 GATT 数据通过单一 ATT Bearer 串行传输，高并发或高吞吐场景下存在明显瓶颈。

### 13.1.1 单一通道的限制 {#单一通道的限制}

- 固定使用 **L2CAP CID = 0x0004**，所有操作串行排队
- 造成阻塞
- 无法充分利用现代芯片的处理能力

### 13.1.2 性能瓶颈 {#性能瓶颈}

- 高并发特性访问延迟显著
- 多读/写场景吞吐受限
- 不利于多 Profile 或多服务同时工作

## 13.2 EATT 基本原理 {#eatt-principles}

### 13.2.1 多 ATT Bearer 架构 {#多-att-bearer-架构}

EATT 允许在一个 LE 连接上建立 **多个 ATT Bearer**：

- 每个 Bearer 对应一个 **独立的 L2CAP LE Credit Based Channel**
- 每个 Channel 都有独立的 **CID（0x0040 ~ 0x007F）**

```
+---------------- BLE Connection ----------------+
|                                                |
|  ATT Bearer #0  <->  L2CAP CID 0x0040          |
|  ATT Bearer #1  <->  L2CAP CID 0x0041          |
|  ATT Bearer #2  <->  L2CAP CID 0x0042          |
|  ...                                           |
|                                                |
+------------------------------------------------+
```

### 13.2.2 核心特性 {#核心特性}

- 并行 GATT 操作（多个读/写同时进行）
- 更高吞吐率
- 更低访问延迟

## 13.3 EATT 与 L2CAP 的关系 {#eatt-l2cap-relation}

### 13.3.1 LE Credit Based Flow Control {#le-credit-based-flow-control}

EATT 基于 **L2CAP LE Credit Based Flow Control Mode**：

- 每个 Channel 独立维护 Credit
- 避免单一 Channel 阻塞影响全局

### 13.3.2 CID 范围 {#cid-范围}

| 类型 | CID 范围 | 说明 |
| --- | --- | --- |
| 固定 ATT | 0x0004 | 传统 ATT Bearer |
| EATT Dynamic CID | 0x0040 – 0x007F | EATT Channel 范围 |

## 13.4 EATT 建立过程详解 {#eatt-establishment}

### 13.4.1 前置条件：BLE 连接和配对 {#前置条件ble-连接和配对}

在建立 EATT 之前，需要：

1. **建立 LE 连接**：Central 与 Peripheral 成功连接
2. **配对认证**：完成 SM（Security Manager）配对过程
3. **双端都支持 EATT**：通过特性检查

### 13.4.2 Server 端初始化 {#eatt-server-init}

Server 需在启动阶段：

1. 在 GATT 数据库中添加两个必要的特性
2. 调用 `att_server_eatt_init()` 初始化 EATT Bearer 资源池

#### 13.4.2.1 Server 特性配置 {#server-特性配置}

**Server Supported Features** 特性（0x2B3A）：表示服务器支持 EATT

```c
const uint8_t server_supported_features[1] = {
    0x02,   // Bit 1: Enhanced ATT bearer supported
};
```

**特性值定义**：

| Bit | 功能描述 | 说明 |
| --- | --- | --- |
| 0 | Robust Caching | 服务器支持健壮缓存 |
| 1 | Enhanced ATT Bearer | 服务器支持 EATT |
| 2-7 | Reserved | 保留 |

#### 13.4.2.2 初始化 EATT Bearer 资源池 {#初始化-eatt-bearer-资源池}

在 GATT 数据库中提供两个特性：

- **Server Supported Features**（UUID: 0x2B3A）：告知 Client 自身支持 EATT
- **Client Supported Features**（UUID: 0x2B29）：接收 Client 的 EATT 支持情况

然后调用 `att_server_eatt_init()` 初始化资源池

### 13.4.3 2. Client 端建立 EATT {#client-端建立-eatt}

#### 13.4.3.1 Client 特性交互流程 {#client-特性交互流程}

Client 需要按以下顺序进行操作：

1. **服务发现**： 发现 Generic Attribute Service
2. **读取 Server 支持**：查看 Server Supported Features 是否支持 EATT（Bit 1）
3. **写入客户端支持**：写 Client Supported Features 宣告自己支持 EATT（触发 EATT 建立）

详细的 API 调用和错误处理见下方”API 参考”部分

#### 13.4.3.2 特性值定义参考 {#特性值定义参考}

**Client Supported Features** Bit 定义：

| Bit | 功能描述 | 说明 |
| --- | --- | --- |
| 0 | Robust Caching | 客户端支持健壮缓存 |
| 1 | Enhanced ATT Bearer | 客户端支持 EATT |
| 2 | Multiple Handle Value Notifications | 客户端支持接收 ATT_MULTIPLE_HANDLE_VALUE_NTF PDU |
| 3-7 | Reserved | 保留 |

### 13.4.4 3. EATT Channel 建立和使用 {#eatt-channel-建立和使用}

完成特性交互后，调用 `gatt_client_le_enhanced_connect()` 建立 EATT 连接。之后协议栈自动处理 L2CAP Channel 建立，建立完成后可进行并行 GATT 操作。

L2CAP 层自动处理多个 Channel 的建立过程（多个连接请求、响应、配置等并行进行）。

## 13.5 EATT 的优势 {#eatt-benefits}

### 13.5.1 性能对比 {#性能对比}

| 维度 | 传统 ATT | EATT |
| --- | --- | --- |
| 并发能力 | ❌ | ✅ |
| 吞吐率 | 低 | 高 |
| 访问延迟 | 高 | 低 |
| 多服务适配 | 差 | 优 |

### 13.5.2 应用场景 {#应用场景}

- **音频（LE Audio）**：多个音频流并行传输
- **多传感器**：多路传感器数据同步上报
- **实时控制**：控制指令与状态反馈分离

## 13.6 主要 API 参考 {#eatt-api}

### 13.6.1 Server 端 API {#eatt-server-api}

#### 13.6.1.1 att_server_eatt_init - 初始化 EATT Bearer 资源池 {#eatt-api-server-init}

```c
uint8_t att_server_eatt_init(uint8_t num_eatt_bearers,
                              uint8_t * storage_buffer,
                              uint16_t storage_size)
```

**功能**：初始化 EATT Bearer 资源池，为后续建立 EATT Channel 准备资源

**参数**：

- `num_eatt_bearers`：最多支持的 EATT Channel 数量（1-64）
- `storage_buffer`：用于存储所有 Bearer 结构体及其收发缓冲区的内存池
- `storage_size`：内存池总大小（字节）

**返回值**：

- `ERROR_CODE_SUCCESS`：初始化成功
- `ERROR_CODE_MEMORY_CAPACITY_EXCEEDED`：内存不足

**调用时机**：在协议栈启动时调用一次

### 13.6.2 Client 端 API {#eatt-client-api}

#### 13.6.2.1 gatt_client_le_enhanced_connect - 建立 EATT 连接 {#eatt-api-client-connect}

```c
uint8_t gatt_client_le_enhanced_connect(
    btstack_packet_handler_t gatt_handler,
    hci_con_handle_t connection_handle,
    uint8_t num_eatt_bearers,
    uint8_t * storage_buffer,
    uint16_t storage_size
)
```

**功能**：在已有的 LE 连接基础上，建立多个 EATT Bearer

**参数**：

- `gatt_handler`：GATT 事件处理回调
- `connection_handle`：HCI 连接句柄
- `num_eatt_bearers`：请求建立的 EATT Channel 数量
- `storage_buffer`：客户端侧的存储缓冲区
- `storage_size`：缓冲区大小（字节）

**返回值**：

- 0：成功
- 非 0：失败

**内存需求计算**：

```
总大小 >= num_eatt_bearers * sizeof(att_server_eatt_bearer_t) 
        + num_eatt_bearers * (receive_buffer_size + send_buffer_size)

通常：总大小 >= num_eatt_bearers * 200 字节（保守估计）
```

**前置条件**：

- LE 连接已建立
- 已确认 Server 支持 EATT（通过读 Server Supported Features）
- 已完成配对