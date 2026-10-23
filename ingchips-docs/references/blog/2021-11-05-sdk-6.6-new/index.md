# SDK 6.6 更新说明

## Highlights: {#highlights}

- 优化超多连接性能

## 1. 软件包 (Bundles) {#1-软件包-bundles}

### 1.1 Controller {#11-controller}

- [**优化**] `mass_conn` 连接性能 (**6.6.0**)

优化了 `mass_conn` 软件包的连接性能，提升超多连接的可用性。

- [**修正**] ADV/SCAN/INIT/CONN 极端情况下异常停止 (**6.6.0**)

旧版本中，极端情况下 ADV/SCAN/INIT/CONN 可能会异常终止。现在，当这些任务异常终止时会上报相应的事件，app 可以根据事件重新尝试启动任务：

- ADV 异常终止时：上报 `HCI_SUBEVENT_LE_ADVERTISING_SET_TERMINATED`
- SCAN 异常终止时：上报 `HCI_SUBEVENT_LE_SCAN_TIMEOUT`
- INIT 异常终止时：上报 `HCI_SUBEVENT_LE_ENHANCED_CONNECTION_COMPLETE`
- CONN 异常终止时：上报 `HCI_EVENT_DISCONNECTION_COMPLETE`
- [**修正**] `LLCP_CONN_PARAM_REQ/RSP` 里 `Offset` 的范围 (**6.6.1**)

### 1.2 FreeRTOS 相关 {#12-freertos-相关}

- [**新增**] `list` 模块 (**6.6.0**)

`list` 模块 API 现已导出。

### 1.3 其它 {#13-其它}

- [**更新**] 版本信息 (**6.6.2**)

在后续版本中，platform 的版本信息将保存在 platform.bin 文件的固定偏移 (+0xb0)。

## 2. 库函数 {#2-库函数}

- [**更新**] `gatt_client_util` 模块支持多连接 (**6.6.0**)

通过编译选项 (`GATT_UTIL_MAX_DISCOVERER_NUM`) 控制支持的连接数。 当只会存在 1 个连接时，此选项可以设置为 1。可能同时存在多个连接的情况下，此数值应该与软件包支持的连接数保持一致。
