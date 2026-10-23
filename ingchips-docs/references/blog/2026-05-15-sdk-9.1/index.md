# SDK 9.1 更新说明

## Highlights: {#highlights}

- 支持 ING208xx 系列（软件包、外设驱动、工具、示例）

**注意：**

- ROM 内的协议栈版本与 v9.0.4 相同（在 *mass_conn* 软件包基础上补充少量扩展功能）。

**说明：**原有的 ING20xx 系列已删除。对于使用 ING20xx 的项目，请先安装 v9.0.6， 切换为 ING208xx，再安装 v9.1.x。

## v9.1.2 {#v912}

### 软件包 {#软件包}

- [**新增**] 定时器机制：新增一组高精度 625µs 硬件定时器 API；内置 RTOS 平台改用该组 API 替代原有的 RTOS 软件定时器。
- [**更新**] 更新并优化 L2CAP 基于信用点的流控（Credit-Based Flow Control）机制。
- [**更新**] 优化启用省电（Power Saving）模式下的蓝牙连接参数更新（Connection Update）流程。
- [**修正**] 蓝牙广播与 ROM Patch：在扫描及发起连接（Initiating）阶段，增加对异常/畸变扩展广播数据包（Malformed Ext Adv PDU）的过滤与丢弃。

### 库函数 {#库函数}

- [**新增**] ADC 模块与校准增强：

新增硬件校准值手动读写接口 `ADC_GetCalibrationData` `ADC_ApplyVBatCalib`，支持保存与重载校准参数，缩短系统上电校准时间。订正init接口的部分问题。

- [**新增**] ING918 I2C：新增 `I2C_ConfigClkFrequencyCalc` 接口，支持时钟频率动态计算。
- [**更新**] 修正部分pum电压配置，解决系统首次上电-时 AON1 IO 锁存的问题。
- [**更新**] por默认值配置修正
- [**更新**] boost模式新增dcdc配置支持，可选使用ldo模式测试。
- [**修正**] 时钟与初始化：修正未使能 PLL 时直接调用 `sysinit` 导致的系统状态配置不一致问题。
- [**修正**] QDEC 驱动：修复在 `-O3` 编译器优化级别下，QDEC 偶发配置失效的问题。
- [**修正**] ASDM：定制ASDM 模拟模式配置问题，修复 ASDM Init寄存器位配置错误。

### 示例 {#示例}

- [**更新**] 定时器示例：同步更新各应用示例工程，适配全新的 625µs 定时器接口。
- [**修正**] I2C 示例：清理并修复 ING918 I2C 相关示例中的编译告警。

### 工具 {#工具}

- [**新增**] Downloader: 支持下拉菜单选择com口下载，支持扩展选项，可选全片擦除ING916、ING20系列，扩展baud下载支持。
- [**修正**] Downloader: 部分daplink无法支持下载的问题。
- [**修正**] Wizard: 修复创建工程，在部分场景下app_main函数生成不全的问题。

## v9.1.1 {#v911}

### 1. 软件包 {#1-软件包}

- [**更新**] 减少程序启动期间栈空间的大小。

  旧版本程序启动期间（`app_main`）栈空间的大小约为 0x1f00 字节。新版本改为 0xf00 字节。
- [**修正**] EATT 相关问题

### 2. 库函数 {#2-库函数}

- [**修正**] ING208 ADC：解决校准模块问题，并将参考电压调整至标准值
- [**修正**] ING208 Eflash：修正因数据类型不匹配导致的 `flash_enable_write_protection` 配置错误
- [**更新**] ING208 Eflash：新增 OTP 区域访问接口，支持通过 API 进行读写操作
- [**修正**] `-O3` 编译时的相关问题

  涉及 SPI、SYSCTRL、`ringbuf` 等模块。

### 3. 示例 {#3-示例}

- [**新增**] EAD：演示广播数据加密。
- [**更新**] EATT

  演示了启用 EATT 功能后各种 Server、Client API 的用法和表现。
- [**更新**] Platform Companion：支持使用外部 RTOS

### 4. 工具 {#4-工具}

- [**修正**] Wizard: 针对 ING208xx ROM 的内存设置

## v9.1.0 {#v910}

### 1. 软件包 {#1-软件包-1}

- [**修正**] L2CAP：PSM 发送长度小于 8 的短数据时会自动断开。

  此问题由 v8.4.21 引入。
- [**修正**] SM: 当从机配对信息被删除时，重新连接，SM 流程完成后无 `sm_state_t` 状态上报。

  现在会上报 `SM_FINAL_FAIL_PROTOCOL`。
- [**更新**] ATT：增强延迟读取功能

  目前延迟读取支持以下命令：

  - `ATT_READ_BY_TYPE_RESPONSE`
  - `ATT_READ_BLOB_RESPONSE`
  - `ATT_READ_RESPONSE`
- [**修正**] SM：作为主机且使用 L1 Privacy 时，与已配对设备重新连接时，流程异常。
- [**修正**] 低功耗：可能进入长时间（约 31 天）CPU IDLE 状态。
- [**新增**] LL 开关：`LL_FLAG_TX_TEST_RPT_PKT_NUM`

  设置此开关后，停止 TX_TEST 时，`Num_Packets` 为发送的数据包的数目。接合接收端上报的数目可计算误包率。

  ![](https://ingchips.github.io/blog/img/le_test_end.png)

### 2. 库函数 {#2-库函数-1}

- [**更新**] ING208 Eflash：重新设计了 FT 数据的转存和校验。
- [**更新**] ING208 Eflash：增加基于 DMA 的写入方式

  定义 `FLASH_PROGRAM_WITH_DMA` 为 1 后启用 DMA 方式。目前默认不使用 DMA 方式。 不使用 DMA 方式时，建议单次写入数据量不超过 32 字节。
- [**更新**] ING208 SYSCTRL：`SYSCTRL_Init`

  新增功能：自动使用 FT 数据校准内核电压（项目必须包含 `eflash.c`）；自动调谐内部高速 RC 至 1.5MHz。
- [**更新**] ING208 PINCTRL：使用 ROM 内的管脚数据
- [**更新**] ING208/ING916 `TMR_WatchDogEnable`：改为向上查找合适参数

  `TMR_WatchDogEnable` 软件接口兼容 ING918，但由于硬件不同，支持的超时参数范围也不相同。旧版本为向下查找合适参数，将导致实际超时时间明显小于所配参数。
- [**修正**] ING208 `iic.c`：有可能通信失败。

### 3. 工具 {#3-工具}

- [**更新**] Wizard: 支持切换项目使用的软件包类型。

  ![](https://ingchips.github.io/blog/img/wiz_proj_change_bundle.png)
- [**修正**] Tracer：无法生成 MSC

  此问题由 v9.0.6 引入。
