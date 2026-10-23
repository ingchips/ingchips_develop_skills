<!-- pg_ble_stack_cn: 10 L2CAP -->

# 10 L2CAP {#ch-l2cap}

## 10.1 概览 {#概览-4}

BLE L2CAP 负责高层协议复用，分包、组包，以及 QoS 信息的传输。

L2CAP 定义了基于信用点的连接。两个设备之间可以建立多个基于信用点的连接，不同连接用 SPSM[43](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn43) 区分。 SPSM 长度为 16 比特，`0x0001`~`0x007f` 为规范保留，`0x0080`~`0x00ff` 可自由使用：

- 对于服务端，SPSM 可以取固定值或根据 GATT Profile 动态设置；
- 对于客户端，应在每次建立连接后借助 GATT 发现服务端的 SPSM。

所谓信用点，指的是接收方允许对方在该连接上发送的 K 帧数目。对方每发送一个 K 帧就消耗一个信用点， 当信用点为 0 时停止发送。接收方可以根据需要给对方补充信用点。 每个传输单元称为一个 SDU。一个 SDU 可能被切分为多个 K 帧，所以发送一个 SDU 可能会消耗多个信用点。通过信用点可控制双方向的流量。

## 10.2 使用说明 {#使用说明-5}

### 10.2.1 从端请求更新连接参数 {#从端请求更新连接参数}

从角色调用 `l2cap_request_connection_parameter_update` 可向主端请求更新连接参数：

```c
int l2cap_request_connection_parameter_update(
  // 连接句柄
  hci_con_handle_t con_handle,
  // 请求的最小连接间隔（单位 1.25ms）
  uint16_t conn_interval_min,
  // 请求的最大连接间隔（单位 1.25ms）
  uint16_t conn_interval_max,
  // 请求的从机延迟
  uint16_t conn_latency,
  // 请求的超时时间（单位 10ms）
  uint16_t supervision_timeout);
```

事件 `HCI_SUBEVENT_LE_CONNECTION_UPDATE_COMPLETE` 标志着参数更新完成。

### 10.2.2 基于信用点的连接 {#基于信用点的连接}

1. 注册 SPSM 及回调

   调用 `l2cap_register_service` 注册 SPSM 及对应的回调函数：

   ```c
   uint8_t l2cap_register_service(
     btstack_packet_handler_t packet_handler,
     uint16_t psm,  // SPSM
     uint16_t mtu,  // MTU 可填 0
     gap_security_level_t security_level
     );
   ```

   这里的 `MTU` 最小为 23，可直接填 0，表示采用协议栈所支持的最大 MTU。无论是服务端还是客户端， 都需要完成这个注册流程。

   这个回调函数将收到以下事件：

   - L2CAP_EVENT_CHANNEL_OPENED：连接已打开

     事件参数详见 `l2cap_event_channel_opened_t`。
   - L2CAP_EVENT_CHANNEL_CLOSED：连接已关闭

     事件参数详见 `l2cap_event_channel_closed_t`。
   - L2CAP_EVENT_COMPLETED_SDU_PACKET：收到完整 SDU[44](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn44)

     事件参数详见 `l2cap_event_complete_sdu_t`。
   - L2CAP_EVENT_FRAGMENT_SDU_PACKET：收到 SDU 片断[45](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn45)

     事件参数详见 l2cap_event_fragment_sdu_t。
2. 建立连接

   BLE 连接建立并发现服务端的 SPSM 后，客户端就可以调用这个函数发起基于信用点的连接：

   ```c
   uint8_t l2cap_create_le_credit_based_connection_request(
     uint16_t credits,   // 赋于对端的初始信用点
     uint16_t psm,       // SPSM
     uint16_t handle,    // 连接句加柄
     uint16_t *local_cid // 本基于信用点的连接的 ID
   );
   ```
3. 发送数据

   连接打开后调用 `l2cap_credit_based_send` 发送数据：

   ```c
   int l2cap_credit_based_send(
     uint16_t local_cid,   // 基于信用点的连接的 ID
     const uint8_t *data,  // SDU 数据
     uint16_t len          // SDU 总长度
   );
   ```

   这个函数如果出错，将返回负数错误码：

   - `-BTSTACK_LE_CHANNEL_NOT_EXIST：连接不存在`

   否则这个函数会返回发送出去[46](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn46)的数据的长度。当整个 SDU 都已发送时， 返回值与 `len` 参数相同，否则小于 `len` 参数[47](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn47)。 这时，需要等待有可用的信用点或者链路层队列出现空余时：如果返回值为 0，则再次调用 `l2cap_credit_based_send` 重新发送；否则调用 `l2cap_credit_based_send_continue` 继续发送剩余数据：

   ```c
   int l2cap_credit_based_send_continue(
     uint16_t local_cid,   // 基于信用点的连接的 ID
     const uint8_t *data,  // SDU 剩余数据
     uint16_t len          // SDU 剩余长度
   );
   ```

   在完整发送一个 SDU 前不可调用 `l2cap_credit_based_send` 发送新的 SDU。
4. 为对端补充信用点

   调用 `l2cap_le_send_flow_control_credit` 即可为对端补充信用点：

   ```c
   uint8_t l2cap_le_send_flow_control_credit(
     uint16_t local_cid,   // 基于信用点的连接的 ID
     uint16_t credits      // 要补充的点数
   );
   ```
5. 查询信用点数

   调用 `l2cap_get_le_credit_based_connection_credits` 查询当前的信用点情况：

   ```c
   uint8_t l2cap_get_le_credit_based_connection_credits(
     uint16_t local_cid,     // 基于信用点的连接的 ID
     uint32_t *peer_credits,
     uint32_t *local_credits
   );
   ```

   `local_credits` 表示对方还能允许本方在该连接上发送多少 K 帧；`peer_credits` 表示对方的 `local_credits`。

### 10.2.3 传输队列 {#ch-i2cap-tx-queue}

通过 GATT 向对方上报或者写入数据时，数据会存入 Controller 的传输队列。 如果传输队列的缓存已满，相关 API 会返回 `BTSTACK_ACL_BUFFERS_FULL` (`0x57`)。如果这些数据必须传输到对方、不可丢弃， 那么可参考以下几种方法重新尝试发送：

- 响应 `HCI_EVENT_NUMBER_OF_COMPLETED_PACKETS` 事件，重新尝试发送；
- 要求协议栈产生“可发送”事件，在事件中重新尝试发送；

  对于 GATT 服务器，调用 `att_server_request_can_send_now_event`。待传输队列不满时， GATT 服务器的[事件回调函数](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-gatt-server.html#ch-gatt-server-overview)会收到 `ATT_EVENT_CAN_SEND_NOW` 事件。 也可以调用 `att_dispatch_server_request_can_send_now_event`[48](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-cap.html#fn48)，待传输队列不满时，会收到 `L2CAP_EVENT_CAN_SEND_NOW` 事件。

  对于 GATT 客户端，调用 `att_dispatch_client_request_can_send_now_event`。待传输队列不满时， GATT 客户端的事件回调函数会收到 `L2CAP_EVENT_CAN_SEND_NOW` 事件。

  另有 `att_server_can_send_now`、`att_dispatch_client_can_send_now`、`att_dispatch_server_can_send_now` 等几个以 `can_send_now` 为后缀的 API，用于查询当前是否可发送数据。这几个 API 一般不需要调用。 以 `att_server_notify` 为例，其伪代码如下：

  ```c
  int att_server_notify(con_handle, attribute_handle, value){
      if (con_handle 不存在)
        return BTSTACK_LE_CHANNEL_NOT_EXIST;

      if (!att_dispatch_server_can_send_now(con_handle))
        return BTSTACK_ACL_BUFFERS_FULL;

      return l2cap_send(con_handle, L2CAP_CID_ATTRIBUTE_PROTOCOL,
                        header, value);
  }
  ```

  可见，调用 `att_server_notify` 之前不需要先调用 `att_dispatch_server_can_send_now`。
- 也可以延迟一段时间后重试。

---

1. <a id="fn43"></a>5.1 及更低版本里称为 LE_PSM[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref43)
2. <a id="fn44"></a>整个 SDU 只占用一个 K 帧[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref44)
3. <a id="fn45"></a>整个 SDU 占用多个 K 帧 这个事件对应其中一个 K 帧[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref45)
4. <a id="fn46"></a>指进入链路层发送队列。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref46)
5. <a id="fn47"></a>当信用点用完或者链路层队列已满时，会出现此情况[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref47)
6. <a id="fn48"></a>`att_server_request_can_send_now_event` 是基于 `att_dispatch_server_request_can_send_now_event` 实现的。[↩︎](https://ingchips.github.io/application-notes/pg_ble_stack_cn/ch-l2cap.html#fnref48)