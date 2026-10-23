# Keil Example: Anti-Lost (Central)

This example demonstrates how to:

- Make an anti-lost kit based on active scanning;
- Use central role to:
  - Scan for devices;
  - Use white list;
- Use GPIO/PWM (see `main.c` for hardware connections);
- Use software timers.

Note that this example:

1.  Works with `anti_lost_sla`;
2.  Blinks when a proper advertising is received;
3.  Turns on the buzzer when timed out.

# Keil Example: Anti-Lost

This pair of examples, *Anti-Lost (Central)*, and *Anti-Lost (Peripheral)* use BLE scannable advertising and active scan to demonstrate an anti-lost system:

- *Central* adds *Peripheral*’s address into its accept list
- *Peripheral* adds *Central*’s address into its accept list
- *Peripheral* sends scannable (scannable and connectable if legacy adv is used) advertising
- *Central* actively scans for *Peripheral*’s advertising

*Peripheral* creates a lost timer called `timer`, which expires after 10 seconds. When `timer` expires, in `vTimerCallback`, a PWM (for example, 500Hz and 50% on duty) signal is generated to drive the buzzer. Each time *Peripheral* receives a scan request, an `HCI_SUBEVENT_LE_SCAN_REQUEST_RECEIVED` event is emitted. In the handler of this event, `timer` is reset, and an LED is blinked.

*Central* also creates a lost timer called `timer`, which expires after 10 seconds. When `timer` expires, as in *Peripheral*, a PWM (for example, 500Hz and 50% on duty) signal is generated to drive the buzzer. Each time *Central* receives a scan response, an `HCI_SUBEVENT_LE_EXTENDED_ADVERTISING_REPORT` event is emitted, of which `HCI_EXT_ADV_PROP_SCAN_RSP` is set in `evt_type`. In the handler of this event, `timer` is reset, and an LED is blinked.

## Hardware Setup

### ING918XX Dev-Board

Connect these two jumpers (Yellow line), where GPIO8 is connected to the on-board buzzer and GPIO9 is connected to LED4:

# Keil Example: Anti-Lost (Peripheral)

This example demonstrates how to:

- Make an anti-lost kit based on active scanning;
- Send scannable advertising;
- Use white list;
- Use GPIO/PWM (see `main.c` for hardware connections);
- Use software timers.

Note that this example:

1.  Works with `anti_lost_mas`;
2.  Blinks when a proper scan request is received;
3.  Turns on the buzzer when timed out.

# Keil Example: Anti-Lost

See [*Anti-Lost Central*](../../anti_lost_mas/doc/index.md).

# Keil Example: BLE RPC

This example demonstrates how to:

- Create an RPC server for BLE.

Note: This project can only be built by ArmClang.

# Keil Example: BLE RPC

This example exposes an RPC (Remote Procedure Call) server interface over UART.

Download this app to a Dev-Board, and connect to it with the RPC client. For detailed information, see [BLE RPC Client](../../../example_host/rpc_client/doc/index.md).

## Hardware Setup

| IO Pin          | Note                                  |
|:----------------|---------------------------------------|
| Default UART Tx | RPC communication UART Tx             |
| Default UART Rx | RPC communication UART Rx             |
| 4               | Debug UART Tx (i.e. `printf` logging) |

# Keil Example: BQB RF Test App

This example demonstrates how to:

- Handle HCI commands over UART;
- Customize BQB RF Test behaviour.

# Keil Example: BQB RF Test App

This is a customizable BQB RF test app. It parses HCI commands from UART, calls GAP APIs, and sends results to UART. This app uses the default UART for HCI transmission, supports BLE test mode, and CW test.

Recent releases of BLE Core Spec added new variants of test commands. A simple summary:

- **HCI_LE_Receiver_Test_v2**: Support different PHYs and modulation indices;
- **HCI_LE_Receiver_Test_v3**: CTE;
- **HCI_LE_Transmitter_Test_v2**: Support different PHYs;
- **HCI_LE_Transmitter_Test_v3**: CTE;
- **HCI_LE_Transmitter_Test_v4**: Change Tx power.

For ING916xx, this app also demonstrates how to tune frequency offset.

## Customization

1.  UART configuration

- Update `config_uart` to configure UART.

1.  Power Mode

- Power mode can be adjusted by RF Test Tool after connected:

## Testing

1.  BLE Tester

- Connect HCI-UART to testers and do the test as usual.

1.  Self Test

- Download this example to two dev-boards, and use two RF Test Tool to control two boards: let one as transmitter and the other as receiver.

1.  Frequency Offset Tunning (ING916xx only)

    1.  Download this example to a device (or dev-board);
    2.  Start Frequency Offset Tester (another ING918xx dev-board is required);
    3.  Use RF Test Tool to control ING916xx device to send test signal at the same frequency with Frequency Offset Tester;
    4.  Adjust the “Tune” value in RF Test Tool and check frequency offset in Frequency Offset Tester.

# Keil Example: Central CTE

This example demonstrates how to:

- Request CTE AoA in connection mode;
- Forward IQ through UART and/or GATT;
- Configure over the air;
- Reception of (SILabs-compatible) proprietary conn-less AoA.

Note: Use `PRO_MODE` to switch between conn & proprietary conn-less mode.

# Keil Example: Central CTE

This example receives CTE AoA in connection mode or proprietary conn-less mode, then forwards IQ through UART and/or GATT.

Check out *Application Note - Direction Finding Solution* for more information on AoA algorithm, etc.

To ease app downloading/updating, this app also includes [*INGCHIPS FOTA Sevice*](../../thermo_ota/doc/index.md#other-resources).

## Work Modes

Use compiler switch `PRO_MODE` to switch between connection mode and proprietary conn-less mode:

- **When** `PRO_MODE` **not defined**: Standard connection mode is selected;
- **When** `PRO_MODE` **is defined**: proprietary conn-less mode is selected.

Proprietary conn-less mode is SILabs-compatible (with limitation).

## Data Output

This example also acts as a peripheral. Once connected, it will forward IQ data through GATT. When not connected, data is forwarded to UART.

Data is Base64 encoding of `le_meta_conn_iq_report_t` for connection mode, and `le_meta_pro_connless_iq_report_t` for proprietary conn-less mode.

## Switching Patterns

Up to `PAT_NUMBER` switching patterns can be configured in this example. A different pattern is used for each AoA reception.

Note:

- For the 4x4 Antenna Array Board, only one switching pattern is enough for precious direction calculation;
- Modify `CURRENT_ARRAY` in [`profile.c`](../src/profile.c) to select a sub array for evaluation, such as `#define CURRENT_ARRAY ANTENNA_ARRAY_1x4`.

## Configure over BLE

Once connected over BLE, this example accepts several commands, see [`service_console.c`](../src/service_console.c) for details.

# Keil Example: Central FOTA

This example demonstrates how to:

- Update a peripheral over the air.

Note: \* FOTA client is implemented in the Gnu example; \* Use `TARGET_FAMILY` to configure target chip family.

# Keil Example: Central FOTA

See the [GCC version](../../../examples-gcc/central_fota/doc/index.md) of this example.

# Keil Example: Massive Connections (Central)

This example demonstrates how to:

- Auto connect using whitelist;
- Connect to up to 24 peripherals.

# Keil Example: Massive Connections

This example demonstrate that `MAX_CONN_NUMBER` connections can be supported for both central & peripheral roles.

When each new connection is established or a connection is lost, connection and heap status are printed.

*Central* tries to connect to peripherals whose most significant 5 bytes of addresses are defined by `peer_addr`, and the least significant byte is `[0 .. MAX_CONN_NUMBER - 1]`. When *Peripheral* sets up its advertising, it uses the first connection ID that has not been established as the least significant byte of address: if no connection is established, `peer_addr` is its address; if connection ID 0 & 1 have been established and ID 2 not, the least significant byte of address is `2`.

## Test

1.  Use `MAX_CONN_NUMBER + 1` Dev-Boards or modules

    - Download *Central* to one Dev-Board, and *Peripheral* to all other boards or modules, and check UART log of *Central* that all *Peripherals* can be connected, (**Remember** to update *Peripheral* to use a fixed address), or

    - Download *Peripheral* to one Dev-Board, and *Central* to all other boards or modules, and check UART log of *Peripheral* that all *Centrals* can be connected.

2.  Use 2 Dev-Boards

- Since both *Central* and *Peripheral* can supported `MAX_CONN_NUMBER` simultaneous connections, we can download *Central* & *Peripheral* to two Dev-Boards and wait for the establishing of all connections between these boards.

  Note: BLE Spec does not allow multiple connections between two devices. This is for test only.

After *Central* connects to all `MAX_CONN_NUMBER` peripheral, it will output (take `MAX_CONN_NUMBER` is 24 as an example):

    Connected to #xx. Total = 24
    Conn Map:
     0: ********
     8: ********
    16: ********
    ALL Connected
    heap status:
        free: ... B
    min free: ... B

## Performance Tips

1.  Connection parameters for initiation need to be fine tuned for better performance;
2.  `gap_update_connection_parameters` is critical.

# Keil Example: Central Throughput

This example demonstrates how to:

- Use central role to:
  - Scan & connect to peripheral devices;
  - Discovery services & characteristics defined by 128bit UUID;
  - Get notification when characteristics value updated;
  - Write to characteristics value;
- Update PHY/connection parameters;
- Moniter connection (check RSSI);
- Use keys;
- Use OLED to display information.

Note: 1. This example works with `peripheral_throughput`; 1. To use command `loopback`, `peripheral_throughput` should be running in `LOOPBACK` mode; 1. OLED can be enabled by defining `USE_DISPLAY` (see `oled_ssd1306.h` for hardware setup).

# Keil Example: Throughput

*Peripheral Throughput* & *Central Throughput* use *INGCHIPS Throughput Service* for testing.

Two test modes are implemented:

1.  **Throughput Mode**

- *Central* and *Peripheral* try their best to achieve the peak throughput in a single direction or both directions simultaneously.

  To achieve the peak throughput from *Peripheral* to *Central*, *Peripheral* needs to push as much data as possible into BLE stack, like:

      void send_data(void)
      {
          uint16_t len = att_server_get_mtu(handle_send) - 3;
          while (att_server_notify(handle_send, HANDLE_GENERIC_OUTPUT, (uint8_t *)0x0, len) == 0) ;
          att_server_request_can_send_now_event(handle_send);
      }

  To achieve the peak throughput from *Central* to *Peripheral*, *Central* also needs to push as much data as possible into BLE stack, like:

      void send_data(void)
      {
          while (gatt_client_write_value_of_characteristic_without_response(slave.conn_handle,
                      slave.input_char.value_handle, send_packet_len, (uint8_t *)0x0) == 0) ;

          att_dispatch_client_request_can_send_now_event(slave.conn_handle);
      }

  Here, `0x0` is a valid address in SoC, and its content is irrelevant to this test.

1.  **Loopback Mode**

- *Central* sends a block of data to *Peripheral* who bounces it back to *Central*. *Central* checks the content and measures the round trip time.

Mode of *Peripheral* is controlled by Key 1: keep Key 1 **released** and reset, then it will run in throughput mode; while keep Key 1 **pressed** and reset, it will run in loopback mode. Mode of *Central* is controlled by entering commands through the default UART interface.

## Hardware Setup

Take ING918xx Dev-Board as an example:

- *Peripheral* (Left):

<!-- -->

- Jumper for Key 1 needs to be connected

<!-- -->

- *Central* (Right):

<!-- -->

- Optionally, jumper for Key 1 & Key2 can be connected, and a 128x64 OLED display driven by SSD1306 can also be connected. Key 1 & 2 are used for start/stop throughput test on two directions respectively, and the OLED is used for displaying statistical information by defining `USE_DISPLAY`.

## Test Commands

*Central* supports following commands (ref to [`uart_console.c`](../src/uart_console.c)).

### Connection Parameters

1.  `phy`: modify PHY

- `phy PHY`: `PHY` can be `1m`, `2m`, `s2` or `s8`

  When `s2` or `s8` is used, *Central*’s Tx PHY is changed to `s2` or `s8` respectively; *Peripheral*’s PHY is changed to Coded, but `s2` or `s8` can not be controlled by this command. Use `ll_set_conn_coded_scheme` in *Peripheral* to control coded scheme.

1.  `interval`: modify connection interval

- `interval X`: change interval to \$ X 1.25ms \$

### Throughput Test Control

For throughput test, *Peripheral* must be put into throughput mode

1.  `start`

    - `start s->m`: start throughput testing from *Peripheral* to *Central*
    - `start m->s`: start throughput testing from *Central* to *Peripheral*

- Test on both directions can be started simultaneously.

1.  `stop`

    - `stop s->m`: stop throughput testing from *Peripheral* to *Central*
    - `stop m->s`: stop throughput testing from *Central* to *Peripheral*

### Loopback Test Control

For loopback test, *Peripheral* must be put into loopback mode.

1.  `loopback`

    - `loopback start`: start loopback test
    - `loopback stop`: stop loopback test

When each round of loopback test is done, round trip time & RSSI is reported automatically.

## Design Details

After *Central* starts, it scans for advertising containing `UUID_TPT` service, then it connects to that device, and discovers its service & characteristics. Once connected, *Central* asks to change to 2M PHY.

Throughput from *Central* to *Peripheral* is got by accumulating number of completed packages in `HCI_EVENT_NUMBER_OF_COMPLETED_PACKETS`.

# Keil Example: CoreMark

Run CoreMark benchmark on ING918xx/ING916xx.

Tune compiler options and check the scores.

# Keil Example: CoreMark

Run [CoreMark](https://www.eembc.org/coremark) benchmark on ING918xx or ING916xx families.

Compiler options affects final score significantly. To achieve higher score, always use latest IDE/toolchain, and below are recommendations on compiler options:

- ING918xx Family

  - Use compiler version 6 (ARMClang)
  - Enable LTO
  - Optimization: `-Ofast`
  - One ELF per function
  - Preprocessor: `ITERATIONS=3000`

- ING916xx Family

  - Use compiler version 6 (ARMClang)
  - Enable LTO
  - Optimization: `-Ofast`
  - One ELF per function
  - Preprocessor: `ITERATIONS=15000`

# Keil Example: Data Logger

This example demonstrates how to:

- Save data from UART/BLE to SD cards;
- Port FatFs (FAT/exFAT file system);
- Use SPI/QSPI;
- Discover services & receive notifications.

# Keil Example: Data Logger

[中文版](index_cn.md)

This app is inspired by [OpenLog](https://github.com/sparkfun/OpenLog). It can read configuration and save data from serial or BLE to SD/TF cards.

The configuration is stored in a file named **CONFIG.TXT** in the card. If this file does not exist, when this app starts, it will create one containing default values for each key. In this file, each line contains a key-value pair: `key=value`.

[FatFs](http://elm-chan.org/fsw/ff/00index_e.html) is used for file I/O. The SD card must be using FAT or exFAT Filesystem. Log files are named as **XXXXX.TXT**, where `XXXXX` is a number increased each new log is created.

## Hardware Setup

See [profile.c](../src/profile.h) for default PIN definition. To run this app, an SD/TF module with SPI interface, an SD or TF card, and a 3.3v power supply are needed.

When using an ING918xx Dev-Board, the default setup looks like this:

## Configuration

| Key | Note | Allowed Values |
|:---|----|----|
| mode | Work mode (data source) | ble \| uart |
| use_timestamp | If add timestamp in log or not | 0 \| 1 |
| uart_baud | UART baud rate | integer (115200, 9600, etc) |
| uart_parity | UART parity | none \| odd \| even |
| uart_stop_bits | UART stop bits number | 1 \| 2 |
| uart_data_bits | UART data bits number | 5 \| 6 \| 7 \| 8 |
| uart_data_fmt | recording format of UART data. | raw \| str |
| ble_data_fmt | recording format of BLE data | raw \| hex |
| ble_phy | BLE PHY for connection | coded \| 1M \| 2M |
| ble_addr_type | BLE device address type | public \| random |
| ble_addr | BLE devide address | 16 bytes. any. |
| ble_service_uuid | BLE service UUID | 16 bytes. any. |
| ble_char_uuid | BLE characteristic UUID | 16 bytes. any. |

Note:

- For UART mode, timestamp is only available when `uart_data_fmt` is set to `str`.

For BLE mode, there are also keys for configure BLE connection.

| Key                 | Note                            |
|:--------------------|---------------------------------|
| scan_int            | scan interval                   |
| scan_win            | scan window                     |
| interval_min        | minimum connection interval     |
| interval_max        | maximum connection interval     |
| latency             | slave latency                   |
| supervision_timeout | supervision timeout             |
| min_ce_len          | minimum connection event length |
| max_ce_len          | maximum connection event length |

## Test

Insert an empty card, download the app and check `printf` output from the default UART to see if the filesystem is successfully mounted. Move the card to a card reader and check if **CONFIG.TXT** is created. If everything is OK, the data logger is ready.

### Record serial data

Get another Dev-Board (Board-B), use the Wizard to create a new app. Make it to continuously print strings to UART. For example:

    uint32_t setup_profile(void *data, void *user_data)
    {
       int i = 0;
       for (;;)
       {
          printf("message #%d\n", i++);
          vTaskDelay(100);
       }
    }

Make sure the relevant configurations in **CONFIG.TXT** are:

    mode=uart
    use_timestamp=1
    uart_baud=115200
    uart_parity=none
    uart_stop_bits=1
    uart_data_bits=8
    uart_data_fmt=str

Connect **UART Rx Probe** to UART Tx of Board-B, power on both Dev-Boards. Wait a while (1 minute or longer), move the card to a card read, and check if there is a new **XXXXX.TXT** file containing strings from Board-B:

    [00:00:05.936,004]message #406
    [00:00:06.137,664]message #407
    [00:00:06.239,135]message #408

### Record temperature measurements

Get another Dev-Board (Board-B), download the `Thermometer with FOTA` example.

Modify relevant configurations in **CONFIG.TXT** as below:

    mode=ble
    use_timestamp=1
    ble_data_fmt=hex
    ble_phy=2M
    ble_addr_type=random
    ble_addr=CDA32811893e
    ble_service_uuid=00001809-0000-1000-8000-00805F9B34FB
    ble_char_uuid=00002A1C-0000-1000-8000-00805F9B34FB

Power on both Dev-Boards. Wait a while (1 minute or longer), move the card to a card read, and check if there is a new **XXXXX.TXT** file containing temperature measurements reported by Board-B, where each report is format as a hexadecimal table:

    [00:00:02.470,153]
     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
    ===============================================
    00 D1 09 00 FE                                   | .....

# Keil Example: 数据记录器 (Data Logger)

[English](index.md)

本应用受 [OpenLog](https://github.com/sparkfun/OpenLog) 启发而开发。它可以读取配置，把从串口或者 BLE 采集到的数据保存到 SD/TF 卡。

配置文件为卡里的 **CONFIG.TXT**。如果该文件不存在，应用启动时会自动创建并将各配置项的默认值写入。 这个文件的每一行都是一个项-值对：`key=value`。

文件 I/O 借助 [FatFs](http://elm-chan.org/fsw/ff/00index_e.html) 实现。SD 卡必须格式化为 FAT 或者 exFAT。 日志文件名为 **XXXXX.TXT**，其中 `XXXXX` 为序号，每次新建日志文件时会增加。

## 硬件搭建

PIN 默认设置见 [profile.c](../src/profile.h)。要运行这个应用，需要准备 1 个 SPI 接口的 SD/TF 模块，1 张 SD 或者 TF 卡，1 个 3.3v 电源。

当使用 ING918xx 开发板时，默认的硬件搭建方式如图所示：

## 配置

| 项               | 说明                 | 允许值                   |
|:-----------------|----------------------|--------------------------|
| mode             | 工作模式（数据源）   | ble \| uart              |
| use_timestamp    | 日志中是否添加时间戳 | 0 \| 1                   |
| uart_baud        | UART 波特率          | 整数 (115200, 9600, etc) |
| uart_parity      | UART 校验            | none \| odd \| even      |
| uart_stop_bits   | UART 停止位          | 1 \| 2                   |
| uart_data_bits   | UART 数据位          | 5 \| 6 \| 7 \| 8         |
| uart_data_fmt    | UART 数据记录格式    | raw \| str               |
| ble_data_fmt     | BLE 数据记录格式     | raw \| hex               |
| ble_phy          | BLE PHY              | coded \| 1M \| 2M        |
| ble_addr_type    | BLE 设备地址类型     | public \| random         |
| ble_addr         | BLE 设备地址         | 16 字节. 任意值.         |
| ble_service_uuid | BLE 服务 UUID        | 16 字节. 任意值.         |
| ble_char_uuid    | BLE 特征 UUID        | 16 字节. 任意值.         |

说明：

- 对于 UART 模式，时间戳设置仅在 `uart_data_fmt` 为 `str` 才有效。

对于 BLE 模式，还有一些针对 BLE 连接的配置项：

| 项                  | 说明             |
|:--------------------|------------------|
| scan_int            | 扫描间隔         |
| scan_win            | 扫描窗口         |
| interval_min        | 最小连接间隔     |
| interval_max        | 最大连接间隔     |
| latency             | 从设备延迟       |
| supervision_timeout | 超时时间         |
| min_ce_len          | 连接事件最小长度 |
| max_ce_len          | 连接事件最大长度 |

## 测试

插入一张空白卡，下载应用，检查 UART 的 `printf` 打印，判断文件系统是否成功挂载。将卡转移到读卡器，检查 **CONFIG.TXT** 文件是否创建。如果一切正常，数据记录器就准备好了。

### 记录串口数据

另外准备一块开发板 (Board-B)，使用向导 (Wizard) 创建一个新应用，使其不断向串口输出字符串。比如：

    uint32_t setup_profile(void *data, void *user_data)
    {
       int i = 0;
       for (;;)
       {
          printf("message #%d\n", i++);
          vTaskDelay(100);
       }
    }

确认 **CONFIG.TXT** 里的相关配置如下所示：

    mode=uart
    use_timestamp=1
    uart_baud=115200
    uart_parity=none
    uart_stop_bits=1
    uart_data_bits=8
    uart_data_fmt=str

将 **UART Rx Probe** 连接到 Board-B 的串口输出脚 (Tx)，给两个开发板上电。等待一段时间（1 分钟或更长）， 将卡转移到读卡器，检查是否生成了一个新的 **XXXXX.TXT** 文件，里面包含 Board-B 打印出的字符串：

    [00:00:05.936,004]message #406
    [00:00:06.137,664]message #407
    [00:00:06.239,135]message #408

### 记录温度数据

另外准备一块开发板 (Board-B)，下载 `Thermometer with FOTA` 示例。

如下所示，修改 **CONFIG.TXT** 里的相关配置：

    mode=ble
    use_timestamp=1
    ble_data_fmt=hex
    ble_phy=2M
    ble_addr_type=random
    ble_addr=CDA32811893e
    ble_service_uuid=00001809-0000-1000-8000-00805F9B34FB
    ble_char_uuid=00002A1C-0000-1000-8000-00805F9B34FB

给两个开发板上电。等待一段时间（1 分钟或更长），将卡转移到读卡器，检查是否生成了一个新的 **XXXXX.TXT** 文件， 里面以十六进制表格形式记录了 Board-B 上报的每个温度数据：

    [00:00:02.470,153]
     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
    ===============================================
    00 D1 09 00 FE                                   | .....

# Keil Example: Direct Connection

This example demonstrates how to:

- Directly create a connection using `ll_create_conn`.

# Keil Example: Direct Connection

This example demonstrates how to directly create a connection between two devices using `ll_create_conn` without advertising.

Before calling `ll_create_conn`, all connection parameters (PHY, interval, access address, CRC init value, master clock accuracy, etc) need to be exchanged using other methods which is designed by developers. In this example, raw packet API is used to pass these parameters to the Peripheral device in packet (named `paging_packet` here); when Peripheral device receives such paging, it will respond with a another raw packet (named `access_packet` here) carrying its address. When Central receives `access_packet`, the connection is created by `ll_create_conn`.

## Test

Build this project twice with compiling switch `CONN_ROLE` set to `0` & `1` respectively, and download it two Dev-Boards.

Check `printf` log to see if the connection can be established or not.

# Keil Example: Ext. Ack-able Packet Tx/Rx

This example demonstrates how to:

- Tx/Rx ack-able packets using “extension” bundle.

Note: Build with macro “FOR_INITATOR=1” & “FOR_INITATOR=0” to get a pair of initiator/responder apps.

# Keil Example: Extension: Ack-able Packet Tx/Rx

This example use “extension” bundle to transmit/receive ack-able packets.

## Test

Build this example twice, one with `FOR_INITATOR=1`, and the other `FOR_INITATOR=0`, and download them to two Dev-Boards. Check the log printed through the default UART.

## Other Resources

- *BLE Extensions Reference*

# Keil Example: Ext. Raw Packet Tx/Rx

This example demonstrates how to:

- Tx/Rx raw packets using “extension” bundle;
- Make ING916 into a tester for Freq Offset Tester.

# Keil Example: Extension: Packet Tx/Rx

This example use “extension” bundle to transmit/receive raw packets.

## Test

### Raw Packet Tx/Rx

Build this example twice, one with `FOR_TX=1`, and the other `FOR_TX=0`, and download them to two Dev-Boards. Check the log printed through the default UART.

`APP_TESTER` should not be defined.

### Make ING916 into a Tester

Build this example with `APP_TESTER` and download it to an ING916 Dev-Board. Then, this Dev-Board can be used as a tester by Frequency Offset Tester program.

## Other Resources

- *BLE Extensions Reference*

# Keil Example: Ext. Raw Packet Tx/Rx (NoOS)

This example demonstrates how to:

- Tx/Rx raw packets using “noos_extension” bundle;
- Use extenstion APIs without RTOS.

Note: Build with macro “FOR_TX=1” & “FOR_TX=0” to get a pair of Tx/Rx apps.

# Keil Example: Extension: Packet Tx/Rx (NoOS)

This example use “extension” bundle to transmit/receive raw packets without any RTOS.

This example is the same as [*Extension: Packet Tx/Rx*](../../ext_raw_packet/doc/index.md), except that in this example no RTOS is used. See also [*Peripheral Console (Realtime)*](../../peripheral_console_realtime/doc/index.md) which runs the whole BLE stack without RTOS.

This example also demonstrates the usage of `platform_set_timer`.

## Other Resources

- *BLE Extensions Reference*

# Keil Example: GATT Relay

This example demonstrates how to:

- Receive & clone advertising data;
- Discover & clone full GATT profile;
- Use deferred read;
- GATT operation relay.

# Keil Example: GATT Relay

This example scans for the device with `peer_addr`, copies advertising data to its own advertising, then connects to it and copies its GATT profile. Other devices can now connect to this example, and everything appears to be the same as connected to the device with `peer_addr`.

## Design Details

[`gatt_client_util`](../../../src/Tools/gatt_client_util.c) module is used for dumping the whole profile.

Deferred read is used to support reading the value of a characteristic:

1.  Return `ATT_DEFERRED_READ` in the read callback querying for data size;
2.  Use `att_server_deferred_read_response` to send value when data is ready.

# Keil Example: HID Keyboard

This example demonstrates how to:

- Define an HID keyboard profile;
- Enable paring using passkey;
- Use GPIO interrupts;
- Report keyboard events;
- Usage of public address (debug only);
- LE Secure Connection pairing;
- Customize kv backend.

Note: \* Use Key1/Key2/Key3 to input `1`, `2` and ‘3’; \* Use UART to emulate printable ASCII inputs; \* Test Result: \* OK: RedMi Note5 (MIUI 11.0.2) \* OK: iPhone XR (iOS 14.5) \* OK: Thinkbook 13s (Win10 Home 20H2, Win11 Home).

# Keil Example: HID Keyboard

This example implements an HID keyboard with passkey paring.

[`kv_impl.c`](../src/kv_impl.c) demonstrates a customized k-v backend. Comparing to the default one,

1.  Flash written operation occurs on the granularity of a k-v pair.
2.  Dual flash blocks are used for secure operation.

## Hardware Setup

On ING918xx Dev-Board, Key 1/2/3 are used to input 1/2/3.

## Test

Take this example as a normal Bluetooth keyboard and add it to the system. This example has been tested on below systems:

- RedMi Note5 (MIUI 11.0.2)
- iPhone XR (iOS 14.5)
- Thinkbook 13s (Win10 Home 20H2, Win11 Home).

When pairing, use a terminal emulator or other serial tools to send the passkey since there are only three keys on board.

## Terminal Input

Besides pressing on-board keys to input “1/2/3”, it also possible to use a terminal emulator (such as PuTTY) to connect to the default UART, type some printable ASCII characters into the terminal tool, and these characters will be sent to host system to which this BLE keyboard is attached.

Tip: Do **NOT** run the terminal emulator on the same system to which this BLE keyboard is attached.

## Design Details

Changes of keyboard status are printed to UART (`set_led_state`).

Up to `INPUT_REPORT_KEYS_MAX` keys are supported in a single report, which is configurable.

Paring data is stored into Flash with the help of `kv_storage` module.

# Keil Example: HID Mouse

This example demonstrates how to:

- Define an HID mouse profile;
- Enable simple paring;
- Manage bonding/paring data;
- Report *fake* mouse movements;
- Use resolvable address;
- Use high duty adv;
- Use LL Privacy (ING916xx);
- Use QDEC (ING916xx).

Note: \* Press `KEY_4` for several seconds to clear bonding \* Test Result: \* OK: RedMi Note5 (MIUI 11.0.2) \* OK: iPhone XR (iOS 14.5) \* OK: Thinkbook 13s (Win10 Home 20H2, Win11 Home).

# Keil Example: HID Mouse

This example implements an HID mouse with Just Works paring.

## Hardware Setup

- ING918xx Dev-Board

<!-- -->

- Connect jumpers for GPIO 4 (Key 4) & 6 (LED 3).

<!-- -->

- ING916xx Dev-Board

<!-- -->

- Connect jumpers for GPIO 9 (Key 4) & 6 (LED 3).

  On ING916xx, two work modes are supported, `SIMULATION` and mouse wheel mode. To test mouse wheel mode, remove compiling option `SIMULATION` and connect a scroll wheel’s A/B signals to GPIO 21 & 32.

## Test

Keep Key 4 pressed for several seconds then release, LED 3 will start flashing. Now take this example as a normal Bluetooth mouse and add it to the system. This example has been tested on below systems:

- RedMi Note5 (MIUI 11.0.2)

- iPhone XR (iOS 14.5)

<!-- -->

- Note: If their is no pointer on the screen, turn on AssistiveTouch.

<!-- -->

- Thinkbook 13s (Win10 Home 20H2, Win11 Home).

### Simulation Mode

After the mouse is added, the pointer will start to move in a cycle. Size of the cycle depends on the resolution of the hardware and the underlying operating system.

### Mouse Wheel Mode

Scroll the wheel and check if it works like the middle “wheel” of a mouse.

## Design Details

This example uses resolvable address, and device’s identity address is protected from unintentional access.

Mouse movement is simulated by sending predefined $`(dx,dy)`$ pairs (see `delta_xy`) periodically.

Paring data is stored into Flash with the help of `kv_storage` module.

# Keil Example: iBeacon Scanner

This example demonstrates how to:

- Define a central device;
- Scan for BLE devices;
- Parse advertising data;
- Decode iBeacon data;
- Estimate distance.

# Keil Example: iBeacon Scanner

Refer to the [tutorials](https://ingchips.github.io/user_guide/tutorial.html#ibeacon-scanner).

# Keil Example: I/O Over BLE (Central)

This example demonstrates how to:

- Build a generic I/O service over BLE (central part):
  - Scanning for devices;
  - Scan & connect to peripheral devices;
  - Discovery services & characteristics;
  - Get notification when characteristics value updated
- Transfer different data types over the generic I/O service:
  - Controlled by IO_TYPE (see `io_interf.h`)
  - Support UART and others

Note: 1. This example can work with “I/O Over BLE (Peripheral)”. For UART data, this example also works with “Peripheral Console”.

# Keil Example: I/O Over BLE

This pair of examples (*Central* and *Peripheral*) create a opaque channel over BLE between two devices identified by `pair_config`.

Following types of I/O are defined:

1.  `IO_TYPE_UART_STR`

- Strings send to device A’s UART will be transfer to device B, and output from its UART, and vice versa.

1.  `IO_TYPE_UART_BIN`

- Data send to device A’s UART will be transfer to device B, and output from its UART, and vice versa.

  Data input from UART are treated as raw bytes and transferred to peer device untouched, while in `IO_TYPE_UART_STR`, data are firstly split into strings then transferred.

1.  `IO_TYPE_LOOPBACK`

- Data received from BLE are automatically bounced back. Obviously that, only one device (*Central* or *Peripheral*) is allowed to use this type of I/O.

1.  `IO_TYPE_USB_BIN`

- Valid only for 916 series. Receive data from USB of device A( *Central* or *Peripheral*), transfer the data through wireless ble to device B( *Central* or *Peripheral*), and then send the data to USB of device B.

## Hardware Setup

Jumpers of both *Central* and *Peripheral* marked as yellow should be connected:

## Design Details

*Central* and *Peripheral* share some source codes.

A ring buffer (`ring_buf` module) is used to cache UART data. High water mark event is used to trigger BLE transmission.

### IO_TYPE_USB_BIN type

- Change IO_TYPE to IO_TYPE_USB_BIN in macro definition in both *Central* and *Peripheral*.
- USB driver is initialized at `io_interf_init()`, after initialization, usb device should be identified by host(or PC), default usb class in `usb_driver.c` is WINUSB. Refer to chapter `USB -> example 0: WINUSB` in *Programmer’s Guide - ING916xx Peripherals* for more information.
- `io_interf_push_data()` is called in `usb_driver.c` whenever there is data received on USB OUT endpoint.
- Similarly, `HANDLE_FUNC()` will send any data received by wireless ble to USB IN endpoint.
- Test this app via write and read command with `ing_usb.exe`. Refer to chapter `USB -> example 0: WINUSB` in *Programmer’s Guide - ING916xx Peripherals* for more information.

# Keil Example: I/O Over BLE (Peripheral)

This example demonstrates how to:

- Build a generic I/O service over BLE (peripheral part).

Note: this example works with “I/O Over BLE (Central)”.

# Keil Example: I/O Over BLE Peripheral

See [*I/O Over BLE Central*](../../io_over_ble_mas/doc/index.md).

# Keil Example: L2CAP PSM

This example demonstrates how to:

- Use L2CAP LE credit based connection:
- Register SPSM service;
- Manage credits.

# Keil Example: L2CAP PSM

This example can be built as *Central* or *Peripheral* role, and create an LE credit based connection between two devices. Role is defined by macro `APP_ROLE`:

| Value | Role         |
|:-----:|--------------|
|   0   | *Central*    |
|   1   | *Peripheral* |

Once connected, *Central* sends “PING” to the peer periodically. *Peripheral* responses “PONG” to each “PING” message.

Both roles will track each other’s credits, and assign more credits to the peer automatically.

:exclamation:**IMPORTANT:** Value of SPSM should be negotiated properly. This example focuses on the usage L2CAP APIs.

## Test

Build this example for two times, one with `APP_ROLE=0`, and the other `APP_ROLE=1`. Download to two Dev-Boards respectively. Check the output from the default UART.

# Keil Example: LittlevGL

This example demonstrates how to:

- Port LVGL (LittlevGL);
- Show a simple chart with LittlevGL.

Note: Keil 4 can’t build LittlevGL.

# Keil Example: LittlevGL (LVGL)

This example is a port of [LVGL](https://lvgl.io) on ING918xx/ING916xx chip families.

A collection of TFT LCD modules is supported by specifying compiling macroes (see [LCD driver](../src/port/lcd_drv.c)):

Macro Name \| Note \| Values \| Default \|

\|: ——– :\| : ————— : \| : ————— : \| : —– :\| \| SPI_LCD_DRIVER \| Name of the driver chip \|

LCD_DRIVER_ST7735

LCD_DRIVER_ST7789

LCD_DRIVER_ILI9488

\|LCD_DRIVER_ST7735 \| \| LCD_WIDTH \| Horizontal resolution of the LCD in pixels \| Integer \| 128 \| \| LCD_HEIGHT \| Vertical resolution of the LCD in pixels \| Integer \| 160 \|

These TFT LCD modules have been tested:

- [1.44inch SPI Module ST7735S (128x128)](http://www.lcdwiki.com/1.44inch_SPI_Module_ST7735S_SKU:MSP1443)
- [1.8inch SPI Module ST7735S (128x160)](http://www.lcdwiki.com/1.8inch_SPI_Module_ST7735S_SKU:MSP1803)
- [3.5inch SPI Module ILI9488](http://www.lcdwiki.com/3.5inch_SPI_Module_ILI9488_SKU:MSP3520)

## Hardware Setup

Take ING918xx Dev-Board as an example, the LCD module is connected like this:

# Keil Example: LLSync Light

This example demonstrates how to:

- Create a RGB LED light with LLSync.

To test this:

- Either, use Tencent LianLian WeChat mini program;
- Or, Tencent LianLian App.

Note: Light temperature is not supported in this demo.

# Keil Example: LLSync Light

This example creates a RGB LED light with [LLSync](https://github.com/TencentCloud/tencentcloud-iot-explorer-ble-sdk-embedded).

## Hardware Setup

- ING918XX Dev-Board

Jumpers marked in below figure should be connected:

## Test

In WeChat, search and launch *Tencent LianLian* mini program. Add this device, then the light can be controlled in the mini program:

# Keil Example: Mesh Light

This example demonstrates how to:

- Integreate NoOS bundle with FreeRTOS;
- Develop a mesh application.

Test Result: \* OK: nRF Mesh (Android) \* OK: nRF Mesh (iOS)

# Keil Example: Mesh Light

This example creates a SIG Mesh light.

## Hardware Setup

- ING918XX Dev-Board

Jumpers marked in below figure should be connected:

## Test

This example can be tested with following apps:

- ING Mesh (WeChat mini program) - recommended
- ING Mesh (iOS App) - recommended
- nRF Mesh (iOS/Android)

## Software Setup

### BOARD_ID setup

- At present, In order to make LED work normally, please switch the project macro definition **BOARD_ID** to the proper value according to the silkscreen of the IC on your board.

### Storage setup

- By default, this example stores the following information in flash:

  - **Device name**
  - **MAC address** (gatt_adv_addr and non-connect_adv_addr)
  - **Adv UUID**
  - **Provisioning Information**

- Press **KEY-2** and then press **KEY-RESET** to clear flash information of **Provisioning Information**, keep the others.

- If you don’t want to store any information in flash, you can disable the corresponding flash storage function by masking the following macro definitions:

  - **MESH_UUID_USE_FLASH** : For Adv UUID
  - **MESH_NAME_USE_FLASH** : For Device name
  - **MESH_GATT_ADV_ADDR_USE_FLASH** : For gatt_adv_addr
  - **MESH_BEACON_ADV_ADDR_USE_FLASH** : For non-connect_adv_addr
    - After you mask above macro definitions, the uuid, the name and the address will always use the default value.
  - **MESH_STACK_TLV_USE_FLASH** : For Provisioning Information
    - After you mask above macro definition, The provisioning information will not be stored in flash each time the provisioning is complete, so, if a chip reset occurs, the provisioning information will be lost.

# Keil Example: Pairing with OOB

This example demonstrates how to do:

- LE Legacy paring using OOB (out of band) data;
- LE Secure Connection paring using OOB data.

# Keil Example: Pairing with OOB

## Test

Build this project twice with compiling switch `ROLE` set to `0` & `1` respectively, and download it two Dev-Boards.

To test LE Secure Connection pairing, define `LE_SECURE_CONNECTION_PAIRING`; to test LE legacy pairing, do not define `LE_SECURE_CONNECTION_PAIRING`.

Check that those two Dev-Boards can be paired.

# Keil Example: Periodic Advertising with Response

This example demonstrates how to use PAwR API to:

- Periodic advertising with subevents;
- Synchronize to subevents;
- Respond to subevents;
- Create connection from PAwR.

Note: ING916xx ONLY.

# Keil Example: Periodic Advertising with Response

This example demonstrates how to use PAwR API.

This example contains two roles, Advertiser and Scanner, which is defined by setting compiling switch `ROLE` to `ROLE_ADVERTISER` and `ROLE_SCANNER`.

Advertiser broadcasts one periodic advertising set with two subevents. Data of these subevents are updated from a counter. Once a response on a subevent is received, it will try to initiate a connection (`gap_ext_create_connection_v2`).

Scanner tries to establish synchronization to the periodic advertising set from Advertiser. Then, it synchronizes to the first two subevents. When it receives data from subevent \#0, it send a response on subevent \#1.

## Test

Build this project twice with compiling switch `ROLE` set to `0` & `1` respectively, and download it two Dev-Boards.

Check `printf` log to see if the connection can be established or not.

### `printf` log of Advertiser

- Subevents data request:

<!-- -->

-     SUBEVT_DATA_REQ:
         adv_handle          = 0
         subevent_start      = 0
         subevent_data_count = 1
      SUBEVT_DATA_REQ:
         adv_handle          = 0
         subevent_start      = 1
         subevent_data_count = 1

<!-- -->

- Response of subevents:

<!-- -->

-     RSP_REPORT:
         subevent      = 1
         response_slot = 0
         data      : ..........

<!-- -->

- Connected:

<!-- -->

-     CONNECTED

### `printf` log of Scanner

- Subevents data:

<!-- -->

-     SUBEVT REPORT (#10)
         subevent = 0
         data     : ......
      SUBEVT REPORT (#10)
         subevent = 1
         data     : ......

<!-- -->

- Connected:

<!-- -->

-     CONNECTED

# Keil Example: Periodic Advertiser

This example demonstrates how to:

- Send periodic advertising PDUs with CTE;
- Update advertising data periodically.

# Keil Example: Periodic Advertiser

This example sends a periodic advertising. The advertising data contains a faking temperature which is updated periodically.

When `CTE` is defined, it will attach CTE signal in the advertising.

For the reception/scanning functionality, see [*Periodic Scanner*](../../periodic_scanner/doc/index.md).

# Keil Example: Periodic Scanner

This example demonstrates how to:

- Receive (synchronize to) periodic advertising PDUs;
- Parse advertising PDUs.

Note: 1. CTE samples are reported to UART (Base64 encoded); 2. Need an antenna array.

# Keil Example: Periodic Scanner

This example scans for the periodic advertising from `target_addr`, and then synchronizes to it.

The temperature contained in the advertising is printed to UART. The CTE signal attached to the advertising is also sampled and printed to UART in Base64 encoding.

## Test

Download *Periodic Advertiser* and *Periodic Scanner* to two Dev-Boards, and check the UART output from *Periodic Scanner*.

*Periodic Scanner* needs to be downloaded to an array board when AoA calculation is going to be performed on the CTE samples.

# Keil Example: Peripheral ANCS

This example demonstrates how to:

- Implement ANCS (Apple Notification Client Serivce):
  - Accept/reject incoming calls
  - Show messages
- Use GPIO interrupts.

# Keil Example: Peripheral ANCS

This example implements the Apple Notification Client Serivce. After paired with an iPhone, this example can display various notifications generated by the phone, including:

- Accept/reject incoming calls
- Show messages

## Hardware Setup

Three keys are used in this example, the marked jumpers should be connected:

Functions of keys:

- Key 1: Accept
- Key 2: Reject
- Key 3: Erase bonding information and restart

## Test

Use an iPhone to connect and pair with this example, then do the following tests:

- Call the phone and try use key 1 & 2 to accept or reject the incoming call;
- Send a message to the phone, and a portion of the message will be printed to UART.

Note: The message is encoded in UTF-8.

# Keil Example: Peripheral Band

This example demonstrates how to:

- Use Heart Rate Measurement profile;
- Use hardware (I2C, RTC) & OS timers;
- Create & use tasks;
- Notify values.

Note: To run this on development board, define `SIMULATION`; Without this switch, the band demo board is required.

# Keil Example: Peripheral Band

This example demonstrate a wearable band, which includes an SPI OLED display and a heart rate sensor.

## Hardware Setup

To test this example, an 128x32 SPI OLED, a BH1790 sensor are needed. Check [`spi.h`](../src/spi.h) and [`main.c`](../src/main.c) for hardware setup.

## Design Details

- BH1790 sensor is sampled @ `SAMPLING_CNT_32HZ`, and heart rate calculation can be found in [`heartRate.c`](../src/bh1790/heartRate.c);

- *Heart Rate Service* and *Running Speed and Candence Service* are defined in GATT profile;

  - Heart rate is reported through *Heart Rate Service*

  - Randomly generated values are reported through *Running Speed and Candence Service*

  - See [*Peripheral Pedometer*](../../peripheral_pedometer/doc/index.md) for reporting real values through *Running Speed and Candence Service*

# Keil Example: Peripheral Battery

This example demonstrates how to:

- Use battery profile;
- Use hardware & software timers;
- Use ADC with calibration;
- Define interrupt service routines.

# Keil Example: Peripheral Battery

This example demonstrate the *Battery Service* and usage of ADC.

## Hardware Setup

To test this example on ING918xx Dev-Board, jumper of ADC 4 should be connected:

## Test

Download this example to a Dev-Board, use *ING BLE* to connect to it, turn the on board variable resistor slowly and check if the reported battery level changed accordingly. Also check the UART output.

## Design Details

- This example shows how to do ADC self calibration:

  1.  Call `adc_prepare_calibration()` in `app_main()`
  2.  Call `adc_calibrate` to post-process the raw ADC value.

- `read_adc()` should be used as a reference to read ADC value although it looks like weird.

# Keil Example: Peripheral Console

This example demonstrates how to:

- Design something like serial port in BLE;
- Power saving;
- Use RC for *slow_clk*
- Detect `EXT_INT` key events in power saving;
- Over-the-air debugging;
- RF power mapping.

Note: 1. ‘\0’ masks the end of a string; 1. Connect `EXT_INT` key to both `EXT_INT` and `KEY_PIN`.

Known Issue: When `USE_POWER_LIB`, only single click is OK, and other key events (multiple clicked & long pressed) might break BLE connection with small interval.

# Keil Example: Peripheral Console

This example provides a simple console over BLE, after connected with *ING BLE*, commands can be issued, and response are displayed.

This example also demonstrate the use of power saving, which can be turned on and off on-the-fly through a command.

There are several compiling switches:

- **LISTEN_TO_POWER_SAVING**

<!-- -->

- When defined, a buzzer can be used as an indicator that the SoC has entered deep sleep and waken up again.

<!-- -->

- **USE_WATCHDOG**

<!-- -->

- Enable watchdog.

<!-- -->

- **USE_POWER_LIB** (ONLY for ING918xx)

<!-- -->

- To further reduce power consumption.

<!-- -->

- **USE_SLOW_CLK_RC** (ONLY for ING916xx)

<!-- -->

- Use internal RC clock as source for *slow_clk*. Different frequencies can be selected:

<table style="width:84%;">
<colgroup>
<col style="width: 42%" />
<col style="width: 42%" />
</colgroup>
<thead>
<tr>
<th><ul>
<li><strong>USE_SLOW_CLK_RC</strong></li>
</ul></th>
<th><ul>
<li>Frequency (MHz)</li>
</ul></th>
</tr>
</thead>
<tbody>
<tr>
<td><ul>
<li>8</li>
</ul></td>
<td><ul>
<li>8</li>
</ul></td>
</tr>
<tr>
<td><ul>
<li>16</li>
</ul></td>
<td><ul>
<li>16</li>
</ul></td>
</tr>
<tr>
<td><ul>
<li>24</li>
</ul></td>
<td><ul>
<li>24</li>
</ul></td>
</tr>
<tr>
<td><ul>
<li>32</li>
</ul></td>
<td><ul>
<li>32</li>
</ul></td>
</tr>
<tr>
<td><ul>
<li>48</li>
</ul></td>
<td><ul>
<li>48</li>
</ul></td>
</tr>
<tr>
<td><ul>
<li>64</li>
</ul></td>
<td><ul>
<li>64</li>
</ul></td>
</tr>
</tbody>
</table>

## Hardware Setup

### ING918xx Dev-Board

| Dev-Board | Pin     | Note                   |
|:---------:|---------|------------------------|
|  EXT_INT  | EXT_INT |                        |
|  EXT_INT  | GPIO 9  | Key detection          |
|  Buzzer   | GPIO 8  | Listen to power saving |

### ING916xx Dev-Board

| Dev-Board | Pin    | Note                          |
|:---------:|--------|-------------------------------|
|  EXT_INT  | GPIO 0 | Emulating EXT_INT on ING918xx |
|  EXT_INT  | GPIO 9 | Key detection                 |
|  Buzzer   | GPIO 8 | Listen to power saving        |

## Test

Download this example to Dev-Board, the buzzing indicates that the SoC has entered deep sleep and waken up again, busy with advertising, etc. Connect it with *ING BLE*, the buzzing will become faster indicating that the SoC is now busy with connection activities which is more frequent than advertising.

The console supports several commands. Some notable ones are listed below. Check out [`service_console.c`](../src/service_console.c) for more commands.

- `ps`

<!-- -->

- `ps 0` will disable power saving and the buzzing will stop, while `ps 1` will re-enable it.

<!-- -->

- `ver`

<!-- -->

- Show the version number of platform binary.

<!-- -->

- `f`

<!-- -->

- Show the actual frequency of the 32k clock.

<!-- -->

- `f-cpu`

<!-- -->

- Show the configured frequency of CPU.

<!-- -->

- `m`

<!-- -->

- Show memory usage information.

<!-- -->

- `latency`

<!-- -->

- Self-assign a peripheral latency parameter. For example, after issuing command `latency 4`, the buzzing will become slower since some connection events are skipped, and power consumption is reduced too.

Hold the `EXT_INT` key down will prevent the SoC from entering deep sleep mode, and the buzzing will stop, too. Release the key, the buzzing resumes. If connected with *ING BLE*, a key event is also reported when `EXT_INT` is clicked, clicked for multiple times, or keep pressed for a period of time.

# Keil Example: Peripheral Console (FreeRTOS)

This example demonstrates how to:

- Integreate NoOS bundle with FreeRTOS;
- See also `Peripheral Console`.

# Keil Example: Peripheral Console (FreeRTOS)

This example is the same as [*Peripheral Console*](../../peripheral_console/doc/index.md), except that the RTOS is within the app but not the platform.

# Keil Example: Peripheral Console (Realtime)

This example demonstrates how to:

- Run BLE stack without any RTOS;
- Implement power saving without RTOS;
- See also `Peripheral Console`.

# Keil Example: Peripheral Console (Realtime)

This example is the same as [*Peripheral Console*](../../peripheral_console/doc/index.md), except that no RTOS is used, and `EXT_INT` key event report is not available, either.

Since no RTOS is used, it is expected to have better performance in some realtime scenarios.

## Design Details

The generic RTOS driver interface is in [`noos_impl.c`](../src/noos_impl.c).

### Task Scheduling

There two tasks in the BLE stack, the Host task and Controller task. Generally, a RTOS is used to run these two tasks. The Host task looks like:

    void host_task(void)
    {
        host_init();
        while (true)
        {
            if (recv_msg(msg) != 0) continue;
            process_msg(msg);
        }
    }

The Controller task looks like:

    void controller_task(void)
    {
        platform_init_controller();
        while (true)
        {
            if (wait_for_event(event) != 0) continue;
            platform_controller_run();
        }
    }

Due to the differences of these two tasks, Controller task can be merged with the Host task, then RTOS is not needed any more. This is what `queue_recv_msg` does:

    static int queue_recv_msg(gen_handle_t queue, void *msg)
    {
        platform_controller_run();

        struct simple_queue *q = (struct simple_queue *)queue;
        if (no message in queue)
        {
            idle_process();
            return -1;
        }

        copy message;
        return 0;
    }

### Power Saving

The idle process `idle_process` is called each time the message queue is empty.

### SysTick

Although this example does not need ticks, SysTick’s counter must be enabled because the internal wake up process will always ensure that SysTick is counting normally. SysTick exception is disabled.

### Timers

Timer API in the generic RTOS driver interface is used by Host task. With the help of `platform_set_timer`, timers are implemented without SysTick. For simplicity, the supported number of timers (`SW_TIMER_NUMBER`) is hard-coded.

## Limitations

`noos_impl.c` is not a fully functional RTOS. Events, message queues, SysTick are not implemented. When these features are required, please use a **true** RTOS instead. There are some tool modules provided in SDK that requires a fully functional RTOS, therefore, these modules are can’t be used with this `noos_impl.c`:

- `btstack_mt`
- `btstack_sync`
- `ecc_driver`
- `trace` (`trace_full_dump2` does depends on RTOS, so it is OK.)
- `uart_driver`
- `ble_brpc`

# Keil Example: Peripheral Console (RT-Thread)

This example demonstrates how to:

- Integreate NoOS bundle with RT-Thread;
- See also `Peripheral Console`.

# Keil Example: Peripheral Console (RT-Thread)

This example is the same as [*Peripheral Console*](../../peripheral_console/doc/index.md), except that the RTOS is within the app but not the platform, and `EXT_INT` key event report is not available, either.

| :exclamation: Warning on RT-Thread Nano 3.1.5      |
|:---------------------------------------------------|
| <https://github.com/RT-Thread/rt-thread/pull/5637> |

# Keil Example: Peripheral eTag

This example demonstrates how to:

- Design fully functional electronic shelf labels (ESL);
- Use SPI interface.

Note: check spi.h for hardware connections.

# Keil Example: Peripheral eTAG

This example demonstrates an eTAG or ESL (electronic shelf label), and its content can be updated by *ING BLE*.

## Hardware Setup

An triple color (white/black/red, or white/black/yellow) E-ink display (EPD) driven by UC8151D. Supported resolutions are 296x128 (default) and 296x152.

| EPD           | ING918xx Dev-Board (Default) |
|:--------------|------------------------------|
| SPI_EPD_BUSY  | GIO_GPIO_6                   |
| SPI_EPD_RST   | GIO_GPIO_7                   |
| SPI_EPD_DC    | GIO_GPIO_8                   |
| SPI_EPD_CS    | GIO_GPIO_5                   |
| SPI_EPD_SCK   | GIO_GPIO_0                   |
| SPI_EPD_SDI   | GIO_GPIO_1                   |
| SPI_EPD_POWER | GIO_GPIO_9                   |

Use compiler option `HEIGHT=128` or `HEIGHT=152` to set the actual height resolution.

## Test

Download this example to a Dev-Board, connect with *ING BLE*. Select EPD type, take a photo, then upload it to the EPD.

## Design Details

- *ING BLE* reads the resolution of the EPD from *eTag Resolution* characteristics, therefore it can support other resolutions;

- Image is saved in `eink_image_t`. Each pixel uses two bits: one controls the position of the black capsule, the other one controls the position of the red (or yellow) capsule.

# Keil Example: Peripheral Beacon

This example demonstrates how to:

- Create iBeacon(Apple) or Eddystone (Google) beacon without writing code;
- Create multiple iBeacons using different advertising sets.

# Keil Example: iBeacon

This example sends 4 iBeacon + 1 Eddystone simultaneously using unique addresses.

Refer to the [tutorials](https://ingchips.github.io/user_guide/tutorial.html#ibeacon).

# Keil Example: Peripheral IRC

This example demonstrates how to:

- Define multiple GATT profiles;
- Use multiple ATT servers;
- Connect to multiple central devices concurrently;
- Create a simple BLE relay chat server.

# Keil Example: Peripheral IRC

This is a BLE chat relay, demonstrating that the device can be connect by several Central devices.

## Test

Download this example to a Dev-Board. Connect 4 devices with *ING BLE* to the *ING Relay Chat - X* devices. Then a simple chat room is created:

## Design Details

- When a piece of data (a chatting message) is written to the device from one *Central* device, it is forwarded to all other *Central* devices.

# Keil Example: Peripheral LED && CTE

This example demonstrates how to:

- Use PWM/GPIO peripheral;
- Make a CTE AoA responder;
- Use (SILabs-compatible) proprietary conn-less AoA.

Note: For PWM controlled LED, define `PWM_LED` (check `impl_led.c` for hardware connections).

# Keil Example: Peripheral LED & CTE

This example is threefold:

- a RGB LED that can be controlled by *ING BLE*
- a CTE responder in connection mode
- Proprietary connection-less AoA

## Hardware Setup

- ING918xx Dev-Board: Marked jumpers should be connected:

<!-- -->

- 

## Test

Download the this example. Then test each function:

- RGB LED: The on-board LED goes between dim and bright when unconnected.

<!-- -->

- Connect with *ING BLE* to the device, and modify its RGB components.

<!-- -->

- CTE responder in connection mode: Ref to [*Central CTE*](../../central_cte/doc/index.md) without `PRO_MODE`.

- Proprietary connection-less AoA: Ref to [*Central CTE*](../../central_cte/doc/index.md) with `PRO_MODE`.

# Keil Example: Massive Connections (Peripheral)

This example demonstrates how to:

- Connect to up to 26 central devices.

# Keil Example: Massive Connections

See [*Massive Connections (Central)*](../../central_mass_conn/doc/index.md).

# Keil Example: Peripheral Pedometer

This example demonstrates how to:

- Use RSC profile;
- Use hardware (I2C) & OS timers;
- Create a separate task;
- Notify values.

# Keil Example: Peripheral Pedometer

This example creates a pedometer using the on-board acceleration sensor. Relevant data is reported through *Running Speed and Candence Service*.

## Hardware Setup

- ING918xx Dev-Board: Marked jumpers should be connected, and make sure the sensor in the yellow rectangle is not missing:

<!-- -->

- 

Note: If the sensor is missing, compiling option `SIMULATION` can be used to generate fake data.

## Test

Download this example to a Dev-Board, and connect it with *ING BLE*. Walk around for several seconds and check if number of steps is reported.

## Design Details

- Step estimation is implemented in [`step_calc.c`](../src/step_calc.c)

# Keil Example: Peripheral Piano

This example demonstrates how to:

- Control buzzer with PWM.

Note: Buzzer is connected to PIN8.

# Keil Example: Peripheral Piano

This example enables *ING BLE* to control the frequency of the buzzer hopefully. The buzzer is driven by PWM output.

## Hardware Setup

- ING918xx Dev-Board: Marked jumpers should be connected,

<!-- -->

- 

# Test

Download this example to a Dev-Board, connect it with *ING BLE* and play your favorite songs:

# Keil Example: Peripheral Throughput

This example demonstrates how to:

- Input/output raw data with central;
- Measure GATT throughput.

Note: Support loopback test (reset while pressing Key1 ).

# Keil Example: Throughput

See [*Central Throughput*](../../central_throughput/doc/index.md).

# Keil Example: Reset Handler

This example demonstrates how to:

- Add custom functionalities into platform’s reset handler.

Note: 1. This example initializes Watchdog to reset every 2 seconds; 2. Use “Patching Tool” to patch platform binaries.

# Keil Example: Reset Handler

[中文版](index_cn.md)

`platform.bin` provided by SDK is pre-built, and function-fixed. With the help of binary patching tool, a small program can be inserted before ISRs defined by `platform.bin` are called, making it possible to customize `platform.bin`.

There are following limitations for a patch program:

1.  When entering the patch program, stack has not been initialized, therefore, it must be guaranteed that,

    1.  There are no *push* or *pop* operations, or,
    2.  The program take in charge of stack allocation for its own usage;

2.  Binary patching tool will append the patch to free space of the last Flash page storing `platform.bin`, so its size is limited;

3.  The load address of the patch program is not fixed.

This example configures the watchdog right after the system resets. This example is written in assembly, do not use stack, and its size is very small. Patching tool will recognize the last two lines of `Reset_Handler`, and modify it automatically.

    Reset_Handler   PROC
                    EXPORT  Reset_Handler

                    ; ...

                    LDR  R0, =0xFEED4000    ; will be modified by tool
                    BX R0

                    ENDP

When the patch program is ready, open patching tool from the main menu of *Wizard*: Tools → More → Patching Platform. Choose `platform.bin` and patch program, then click “Make Patch” to generate a new `platform.bin` with the patch attached. When downloading, use this one to replace the original `platform.bin`.

# Keil Example: Reset Handler

[English](index.md)

SDK 提供的 `platform.bin` 功能固定、不可更改。通过平台补丁工具可以将开发者编写的一段程序作为补丁插入到 `platform.bin` 已有的中断服务程序之前，在一定程序上定制 `platform.bin` 的功能。

对补丁程序存有以下限制和注意事项：

1.  进入补丁程序时，未配置栈空间。因此需要保证：

    1.  程序中不存在压、弹栈操作，或者
    2.  程序自行配置栈空间；

2.  工具会将补丁程序附加到 `platform.bin` 最后一页 eFlash 存储空间的空白处，所以其大小受限；

3.  补丁程序的加载位置不固定。

本示例在系统复位之后立即配置看门狗。这个示例使用汇编开发，未使用栈空间，体积也很小。补丁工具会识别 `Reset_Handler` 函数的最后两行代码，自动调整。

    Reset_Handler   PROC
                    EXPORT  Reset_Handler

                    ; ...

                    LDR  R0, =0xFEED4000    ; will be modified by tool
                    BX R0

                    ENDP

补丁程序准备好之后，在 `Wizard` 里选择菜单 Tools → More → Patching Platform 打开补丁工具。选择 `platform.bin`、补丁程序，然后点击 “Make Patch” 生成带有补丁程序的新的 `platform.bin`，烧录时使用 用这个文件替换掉原有的 `platform.bin` 即可。

# Keil Example: Secondary FOTA

This example demonstrates how to:

- Develop a secondary app;
- Use Firmware Over-The-Air update.

# Keil Example: Secondary FOTA

This example is a secondary, dedicated FOTA (Firmware Over-The-Air) app using *INGCHIPS FOTA Serivce*.

## Test

Download [*Thermometer with FOTA*](../../thermo_ota/doc/index.md) to a Dev-Board, and test with FOTA tools, such as *ING BLE*, *Central FOTA*, or *FOTA Web Tool*.

# Keil Example: Smart Meter

This example demonstrates how to:

- Use central role to:
  - Scan & connect to peripheral devices;
  - Discovery services & characteristics;
  - Get notification when characteristics value updated;
- Use multiple central & multiple periphral roles simultaneously.

Note:

1.  This demo has a command line interface on UART0 (see also `uart_console`), and output temperature information over the air (see also `peripheral_console`);
2.  This demo searches for peripherals with specific addresses;
3.  Peripherals should support SIG Health Thermometer service.

# Keil Example: Smart Meter

[中文版](index_cn.md)

*Smart Meter* as a *Central* device, can connect to up to 4 peripheral devices (4 *Thermometer with FOTA*); as a *Peripheral* device, it can be connected by a smart phone and reports temperature measurements collected from 4 thermometers to the smart phone. Also, *Smart Meter* can be controlled by host machine through UART, setting addresses of thermometers, starting/stopping the program, etc.

*Smart Meter* defines a customized GATT service, with which a character based communication channel is created between the smart phone and the device. *Smart Meter* uses this channel to report temperature measurements. [*Peripheral Console*](../../peripheral_console/doc/index.md) also uses this service.

## Development Details

### 1. Use Wizard to Create a Peripheral App

Use *Wizard* to setup advertising data and GATT Profile. Add the customized GATT service into the profile.

### 2. Define the Peripheral (i.e. Thermometer)

A thermometer is identified by its address and `id`. Each device uses a dedicated connection (\`conn_handle).

    typedef struct slave_info
    {
        uint8_t     id;
        bd_addr_t   addr;
        uint16_t    conn_handle;
        gatt_client_service_t                   service_thermo;
        gatt_client_characteristic_t            temp_char;
        gatt_client_characteristic_descriptor_t temp_desc;
        gatt_client_notification_t              temp_notify;
    } slave_info_t;

### 3. Scan & Connect to Thermometers

Call two GAP functions to start scanning, once a thermometer waiting for connection is found, stop scanning and call `gap_ext_create_connection` to create a connection. After a connection is established, check if there are remaining once: if so, start scanning again.

### 4. Discover Services

This part uses a series of `gatt_client` API. These API share the similar logic as those of Android and iOS.

### 5. Data Transmission

Subscribe to temperature value, convert the value to strings, then sent them to the host through UART. If a *Central* device (*ING BLE*) has connected, data are also transferred to it through GATT service.

### 6. Robustness

- If a connection with a thermometer is lost, start scanning

- If the connection with *Central* is lost, start advertising and wait for connection

## Test

### 1. Prepare Thermometers

Downloader has a built-in Pasal engine, when a .bin file start downloading, a user proviced function is called where the data can be modified on the fly. Addresses of each thermometer is stored in a bin file, add the file to the Downloader (assume it is the 6th file), the script below will modify the first byte of the address according to the downloading counter:

    procedure OnStartBin(const BatchCounter, BinIndex: Integer;
                         var Data: TBytes; var Abort: Boolean);
    begin
      if BinIndex <> 6 then Exit;
      Data[0] := BatchCounter;
    end;

It is also possible to use the Python Downloader, and in this case [Python script](https://ingchips.github.io/user_guide/core-tools.html#python-%E7%89%88%E6%9C%AC) can be used to do the job.

Suppose the download address of the bin is `X`, modify *Thermometer with FOTA* to get address from this location like this:

    gap_set_adv_set_random_addr(0, (uint8_t *)X);

Download the modified *Thermometer with FOTA* to four Dev-Boards.

### 2. Test

Download *Smart Meter* to another Dev-Board, input `start` from host to start *Start Meter*. Use *ING BLE* to connect to the device named *ING Smart Meter*, and check the temperature reports. Randomly reset one or more thermometers, and check that *Smart Meter* can automatically re-establish the connections.

# Keil Example: Smart Meter

[English](index.md)

*Smart Meter* 作为中心设备，可以连接最多四个外围设备（四个 *Thermometer with FOTA* 温度计）；作为外围设备， 可与手机连接并将收集到的温度数据传输到手机。此外，*Smart Meter* 通过 UART 口接受上位机的控制，可以设置各温度计的地址、控制程序的启动等。

*Smart Meter* 与手机的连接使用了一个自定义的 GATT 服务，通过这个服务在手机和蓝牙设备之间建立了 一个基于字符串的输入、输出通道。*Smart Meter* 使用输出通道传输温度数据。有关这个自定义服务的使用 方法可参考 [*Peripheral Console*](../../peripheral_console/doc/index.md) 示例。

## 详细开发步骤

### 1. 使用项目向导创建一个 Peripheral 应用

使用向导工具设置广播数据和 GATT Profile。在 GATT Profile 里添加自定义的 GATT 服务。

### 2. 定义从设备（即温度计）

温度计设备用设备地址和 `id` 作为标识。每个设备占用一条独立的链路（`conn_handle`）。

    typedef struct slave_info
    {
        uint8_t     id;
        bd_addr_t   addr;
        uint16_t    conn_handle;
        gatt_client_service_t                   service_thermo;
        gatt_client_characteristic_t            temp_char;
        gatt_client_characteristic_descriptor_t temp_desc;
        gatt_client_notification_t              temp_notify;
    } slave_info_t;

### 3. 扫描并连接到温度计

调用两个 GAP 函数开始扫描，一旦扫描到待连接的温度计，就停止扫描并调用 `gap_ext_create_connection` 发起连接。连接建立成功后，检查是否还有待连接的温度计，如果有，再次开始扫描。

### 4. 发现服务

这部分功能需要调用一系列 `gatt_client` 模块的 API。这部分 API 的整体逻辑跟 Android、iOS 蓝牙 API 基本类似。

### 5. 数据传输

订阅温度数据，将温度转换成字符串，通过 UART 上传给上位机。如果已经连接到了中心设备（ING BLE app）， 则将数据通过自定义的 GATT 服务传输到中心设备。

### 6. 加入容错性

- 如果检查到与某温度计的连接断开，则再次开始扫描。

- 如果与中心设备的连接断开，则再次开始广播。

## 测试方法

### 1. 准备蓝牙温度计

Downloader 内置 Pascal 脚本引擎，开始下载每个 bin 文件时会调用用户编写的脚本。通过脚本我们可以任意修改 bin 的内容。 将蓝牙地址写在一个 bin 文件内，然后添加到 Download 内（假设是第 6 个 bin 文件），下面的脚本会按照下载次数修改蓝牙地址的第一个字节：

    procedure OnStartBin(const BatchCounter, BinIndex: Integer;
                         var Data: TBytes; var Abort: Boolean);
    begin
      if BinIndex <> 6 then Exit;
      Data[0] := BatchCounter;
    end;

或者使用 Python 版本下载工具，并用 [Python 脚本](https://ingchips.github.io/user_guide_cn/core-tools.html#python-%E7%89%88%E6%9C%AC)实现上述功能。

假设这个 bin 文件的烧录地址为 `X`，修改 *Thermometer with FOTA*，使其从该地址获取地址：

    gap_set_adv_set_random_addr(0, (uint8_t *)X);

将修改后的 *Thermometer with FOTA* 下载到 4 块开发板。

### 2. 测试

将 *Smart Meter* 下载到另一块开发板，在上位机上通过串口工具输入 `start` 命令启动 *Smart Meter* ， 用手机连接到名为 ING Smart Meter 的设备，就可以看到四个温度计上报的温度了。随机重启几个温度计， 可以看到 *Smart Meter* 能够自动重新建立连接。

# Keil Example: Thermometer with FOTA

This example demonstrates how to:

- Define profiles;
- Read temperature;
- Notify values;
- Use Firmware Over-The-Air update.

Note: 1. Sensor is connected to I2C0; 1. Define `SECURE_FOTA` to enable secure FOTA.

# Keil Example: Thermometer with FOTA

This example collects temperature data using the on board sensor, and report it using *Health Thermometer* service.

This example supports two type of FOTA using *INGCHIPS FOTA Serivce*, secure and unsecure, which is configurable by defining `SECURE_FOTA`.

## Hardware Setup

- ING918xx Dev-Board: Marked jumpers should be connected, and make sure the sensor in the yellow rectangle is not missing:

<!-- -->

- 

Note: If the sensor is missing, compiling option `SIMULATION` can be used to generate fake data.

## Test

Download this example to a Dev-Board. Use *ING BLE* to connect to it, and check the temperature reports.

Rebuild this example by defined `V2`, than create FOTA package and test FOTA with FOTA tools, such as *ING BLE*, *Central FOTA*, or *FOTA Web Tool*.

[*Secondary FOTA*](../../secondary_fota/doc/index.md) can also be activated through the FOTA service.

## Other Resources

- [A Quick Demo of FOTA](https://ingchips.github.io/blog/fota_demo_zh/)
- [Secure Update Over the Air](https://ingchips.github.io/blog/2021-04-20-secure-fota/)

# Keil Example: TTS Demo Project

This is a demo of TTS & stretch.

Please check [doc](doc/index.md) for details.

Only Keil 5 is supported. See also the [GCC](../gcc/readme.md) version.

# Keil Example: TTS Demo Project

[中文版](index_cn.md)

Important: this project needs [external flash](https://ingchips.github.io/blog/2024-02-05-external-flash/).

Examples:

> 欢迎使用 ING916 桃芯语音合成。支付宝收款 916.80 元。

Your browser does not support the audio element

> 京 A123456789，祝您一路顺风。

Your browser does not support the audio element

Synthesized wave will be sent to UART or I2S, which is selected by `WAVE_SINK`:

| `WAVE_SINK` | Output         | Note                                            |
|:-----------:|----------------|-------------------------------------------------|
|      0      | UART (Default) | Python script `tts_demo.py` will play the wave. |
|      1      | I2S            | Audio DAC with I2S is needed for playback.      |

When I2S is selected as `WAVE_SINK`, an additional audio DAC with I2S is required for playback. Take PCM5102A as an example:

Use Cube to find out which PIN are used as I2S.

## Test

1.  Download to ING916 Dev-Board which has connected to external flash large enough for the voice definition;

2.  Run [`tts_demo.py`](../../../../../tools/tts_demo.py). Suppose COM1 is used:

-     python tts_demo.py COM1

# Keil Example: TTS 演示项目

[English](index.md)

重要提示：此项目需要[外部闪存](https://ingchips.github.io/blog/2024-02-05-external-flash/)。

语音样例：

> 欢迎使用 ING916 桃芯语音合成。支付宝收款 916.80 元。

您的浏览器不支持 audio 元素。

> 京 A123456789，祝您一路顺风。

您的浏览器不支持 audio 元素。

合成的波形将通过 UART 或 I2S 发送，具体由 WAVE_SINK 选择：

| WAVE_SINK | 输出        | 备注                                   |
|:---------:|-------------|----------------------------------------|
|     0     | UART (默认) | Python 脚本 `tts_demo.py` 将播放波形。 |
|     1     | I2S         | 需要使用带有 I2S 的音频 DAC 进行播放。 |

当选择 I2S 作为 `WAVE_SINK` 时，需要额外的带有 I2S 的音频 DAC 进行播放。以 PCM5102A 为例：

请使用 Cube 找出哪些引脚用作 I2S。

## 测试

1.  下载到连接了足够大外部闪存的 ING916 开发板；

2.  运行 [`tts_demo.py`](../../../../../tools/tts_demo.py)。假设使用 COM1：

-     python tts_demo.py COM1

# Keil Example: UART GATT Console

This example demonstrates how to:

- Usage of UART;
- Dynamic changing of advertising data & address;
- GATT client operations (discovering, subscribing, etc);
- Trace Demo: SWD/UART/Flash/Air.
- Power Control
- Subrating
- Connection abort & resume
- Dump through UART

Note: Use a serial tool to communicate. CR/LF is used to mark the end of a command.

# Keil Example: UART GATT Console

This example demonstrates lots of BLE functionalities controlled through UART:

- Advertising data modification
- Scanning (passive and active)
- Connect to a device
- Service discovery
- Read/write/subscribe to a characteristic
- Different trace sink driver
- Power Control
- Subrating
- Dump through UART

## Commands

This example exposes a command line interface through UART. Some notable commands are listed below.

:exclamation:**IMPORTANT:** This example’s purpose is to demonstrate functionalities and usage of APIs. Some of the commands may not work if another specific command is sent, such as `ascan` after `scan`, `conn AAA` after `conn BBB`. Just reset before sending these commands.

### Advertising

- `name new_name`

<!-- -->

- Change advertising name to `new_name`.

<!-- -->

- `addr new_address`

<!-- -->

- Change the random address to `new_address`, such as `01:02:03:04:05:06`.

<!-- -->

- `start`/`stop`

<!-- -->

- Start/Stop advertising using the settings given above.

### Scanning

- `scan`

<!-- -->

- Start passive scanning, not using acceptance list.

<!-- -->

- `scan address`

<!-- -->

- Start passive scanning, only receiving data from `address` (such as `01:02:03:04:05:06`).

<!-- -->

- `ascan`

<!-- -->

- Start active scanning, not using acceptance list.

<!-- -->

- `ascan address`

<!-- -->

- Start active scanning, only receiving data from `address` (such as `01:02:03:04:05:06`).

When scanning is started, advertising data and other information are printed to UART.

### Connection

- `conn address`

<!-- -->

- Try to connect to device with `address` (such as `01:02:03:04:05:06`).

<!-- -->

- `cancel`

<!-- -->

- Cancel (Abort) the attempt to connect to the device specified in above `conn` command.

After the connection is established, the whole GATT profile is discovered and printed. GATT client & connection control commands can be sent.

### GATT Client

- `read value_handle`

<!-- -->

- Read the value of the characteristic with `value_handle`. The value is printed in hex format.

<!-- -->

- `write value_handle XX XX ...`

<!-- -->

- Write value to the characteristic with `value_handle`. The value `XX XX ...` is input in hex format (such as `01 02 0A ...`).

<!-- -->

- `w/or value_handle XX XX ...`

<!-- -->

- Write value (use the Write Without Response procedure) to the characteristic with `value_handle`. The value `XX XX ...` is input in hex format (such as `01 02 0A ...`).

<!-- -->

- `sub value_handle`

<!-- -->

- Subscribe to the characteristic with `value_handle`. Once a notification is received, the value is printed in hex format.

<!-- -->

- `unsub value_handle`

<!-- -->

- Unsubscribe to the characteristic with `value_handle`.

### Connection Control

- `phy new_phy`

<!-- -->

- Change PHY to `new_phy`, where `new_phy` is `1m`, `2m`, `s2`, or `s8`. When `s2` or `s8` is used, this example’s Tx PHY is changed to `s2` or `s8` respectively; the peer’s PHY is changed to Coded, whether it is `s2` or `s8` is unknown.

<!-- -->

- `conpar interval latency timeout`

<!-- -->

- Change (*Central* role) or request (*Peripheral* role) to change connection parameters, where *interval* is \$ X 1.25ms \$, *timeout* is \$ X 10ms \$. *latency* and *timeout* are optional.

### Power Control

Firstly, connect to a device with LE Power Control & Path Loss Monitoring features. When path loss state or transmit power level changed, detailed information is printed.

- `cpwr   power`

<!-- -->

- Change local Tx power level to `power` in dBm.

<!-- -->

- `pwrctl delta`

<!-- -->

- Adjust peer Tx power by `delta` in dB. A positive value means to increase power level, while a negtive value means to decrease it.

<!-- -->

- `auto flag`

<!-- -->

- Enable (1) or disable(0) automatic power control.

  When enabled and path lose state is changed, RSSI is checked against golden range, and peer Tx power is adjusted accordingly.

<!-- -->

- `rssi`

<!-- -->

- Read RSSI.

  When automatic power control is enabled, RSSI is checked against golden range, and peer Tx power is adjusted accordingly.

### Subrating

Firstly, connect to a device with Connection Subrating feature.

- `subr factor`

<!-- -->

- Request to use subrating `factor`. After subrating parameters changed, information is printed.

  Use BLE sniffers or high-end digital multi-meters to check the behavior of subrating. Below figure shows that after subrating (fator = 8) is activated, some (or rather 7) connection events are *skipped*:

  Trigger some ATT operations (for example `read 3`), check the behavior again. Below figure show that ATT request is delayed to the next subrated event, and the response is got quickly after that event:

### Connection Abort & Resume

Firstly, start advertising and get connected with *ING BLE* app.

- `re-conn`

<!-- -->

- This command will abort current connection (SLAVE role), and resume it immediately.

  Pass `HCI_SUBEVENT_LE_VENDOR_CONNECTION_ABORTED` and timing information to another device, then the connection can be resumed on that device, and *handover* is achieved.

### Others

- `status`

<!-- -->

- This command will show states of Controller.

## Trace

This example has 4 trace sink drivers (i.e. how to export/save trace data):

- **SEGGER RTT** is the default driver
- **UART** is selected if `TRACE_TO_UART` is defined
- **FLASH** is selected if `TRACE_TO_FLASH` is defined
- **Over the Air (BLE)** is selected if `TRACE_TO_AIR` is defined

## Dump

Memory dump can be used by Axf Tool for runtime analysis. This example dumps memory through UART when an assertion is raised. Use `assert` command to trigger an assertion manually.

For further information on memory dump, see `trace_full_dump2` in `trace.c`.

## Test

Download this example to a Dev-Board (C), and test varies commands.

To test Power Control & Subrating, download this example to another Dev-Board (P) and send command `start`. Send command `conn C6:FA:5C:20:87:A7` to the the former Dev-Board (C) to establish the connection.

Rebuild this example using different trace sink driver, re-download and check trace log.

# Keil Example: Voice Remote Control

This example demonstrates how to:

- Real-time 4-bit ADPCM encoding of audio data;
- Real-time SBC encoding of audio data;
- Use hardware timer & ADC (loop mode);
- Use I2S/PDM/DMA;
- Scan keyboard state;
- Update connection parameters.

Note: Define `BOARD=BOARD_DEV` to run this on development board (no keyboard); define `BOARD=BOARD_REM` to a special remote controller.

Use `AUDIO_INPUT` to select input.

# Keil Example: Voice Remote Control

This example is a remote control with voice.

## Hardware Setup

The key matrix is available on the dedicated remote control board. To simplify the test, `BOARD=BOARD_DEV` has been used to test audio feature only on Dev-Boards.

This example support several audio input types which is selected by defining `AUDIO_INPUT=0..3`. Below table shows how to connect the microphone to the Dev-Board for each input type:

| Audio Input | Note | ING918xx Family | ING916xx Family | Tested Microphone |
|:---|----|----|----|----|
| 0 | Simulated | Universal | Universal | – |
| 1 | ADC | ADC Channel 4 | ADC Channel 4 | Analog MIC |
| 2 | I2S | Not available | BCLK(21),IN(22),LRCLK(35) | INMP441: |
| 3 | PDM | Not available | MCLK(28),IN(29) | MP34DT01: |

Note: for type `0`, audio is playback from a data file (ITU standard testing data), and no microphone is used. The [data file](../data/itu_female_16k.bin) containing raw PCM samples needs to be downloaded to [`SAMPLES_LOCATION`](../src/audio_input_sim.c).

## Audio Codec

Supported codecs:

|    Name     | Identifier              | Note |
|:-----------:|-------------------------|------|
| 4-bit ADPCM | `AUDIO_CODEC_ALG_ADPCM` |      |
|     SBC     | `AUDIO_CODEC_ALG_SBC`   |      |

Audio codec can be configured by defining `AUDIO_CODEC_ALG` to the corresponding codec identifier.

SBC codec implementation used in this project is [libsbc](https://github.com/google/libsbc).

## Test

Download this example to a Dev-Board, use *ING BLE* to connect to it. Keep the “Capture” button pressed to capture voice data. Say something to the microphone if other types than `0` is used. Check the playback of voice data.

Choose an audio decoding algorithm, and press the “Capture” button to start capturing voice data. Audio that has been processed by different audio codec algorithms may have different effects. Note: algorithm selection on APP side should be consistent with algorithm selection on MIC side.

## Design Details

- Software based key matrix scan is implemented in [`kb_scan.c`](../src/kb_scan.c);
- Audio is encoded in ADPCM or SBC and transmitted to *ING demo* through *INGCHIPS Voice Output* Service;
- Encoder selected macro defined switch in [`audio_encoder.h`](../src/audio_encoder.h).

# GCC Example: Central FOTA

This example demonstrates how to:

- Update a peripheral over the air;
- Use Zig + C for development.

# GCC Example: Central FOTA

This example update a peripheral over the air. This example shares the same design with [*ING BLE*](https://github.com/ingchips/INGdemo/) and [*FOTA Web Tool*](https://ingchips.github.io/web_apps/ing918_ota/index.html).

The core FOTA procedure is implemented by module [`fota_client.zig`](../src/fota_client.zig) which is written in [Zig](https://ziglang.org) programming language due to its simplicity in developing `async` programs:

    pub fn update(...) {
        if (!self.enable_fota()) return -2;
        if (!self.burn_items(bitmap, item_cnt, items)) return -3;
        if (!self.burn_meta(bitmap, item_cnt, items, entry)) return -4;
        if (!self.reboot()) return -5;
        return 0;
    }

This example supports both secure and unsecure FOTA.

## Data Storage

Data storage of both local and remote are defined in `ota_items` in [`profile.c`](../src/profile.c). This example can be built for different chip families (`INGCHIPS_FAMILY`), and the device to be updated is of another family which is defined by compiler switch `TARGET_FAMILY`. There are three addresses related to each `ota_item_t`:

1.  `local_storage_addr`: Where the item (binary) is store in **this** device;
2.  `target_storage_addr`: Where the item (binary) is going to be stored in the peripheral device, i.e. the location to hold the new version;
3.  `target_load_addr`: The actual address of the item (binary) in the peripheral device, i.e. the location to be replace by the new version after updating.

Since all data are stored in the embedded flash, an ING918xx device may not be able to hold the whole firmware for an ING916xx device. [*Data Logger*](../../../examples/data_logger/doc/index.md) demonstrate how to use an external mass storage device.

## Test

**Zig 0.8.1** is required to build this project.

[Get familiar](https://ingchips.github.io/blog/fota_demo_zh/) with the whole FOTA procedure, and test it using [*ING BLE*](https://github.com/ingchips/INGdemo/) and [*FOTA Web Tool*](https://ingchips.github.io/web_apps/ing918_ota/index.html). After this,

1.  Download `Thermometer with FOTA` to one Dev-Board (Board-A) and run;

2.  Rebuild `Thermometer with FOTA` with `V2`;

3.  Make sure `TARGET_FAMILY` is set to chip family of Board-A, rebuild & download to another Dev-Board (Board-B), and run;

4.  Output of Board-B will be somethings like

-     connecting...
      discovering...

      === UNSECURE FOTA ===
      device version:
      platform: 1.7.12
          app: 1.1.0
      update bitmap: 02

      start new item: 1
      burn_page: 00066000, 00066000, 8192
      burn_page: 00068000, 00068000, 8192

      fota_done: 0
      disconnected

1.  Connect to Board-A and check if its app has been updated, or

2.  Reset Board-B to try to update it once more, and output of Board-B will be somethings like

-     connecting...
      discovering...

      === UNSECURE FOTA ===
      device version:
      platform: 1.7.12
          app: 1.2.0
      fota_done: 1

# GCC Example: Get Started

This is a playground for dev boards.

This example demonstrates how to:

- Use standard C/C++ lib.

Note: This project can only be built by Gnu Toolchain V10+.

# GCC Example: Get Started

See the [Keil version](../../../examples/get_started/doc/index.md) of this example.

# GCC Example: Peripheral Console (LiteOS)

This example demonstrates how to:

- Integreate NoOS bundle with Huawei LiteOS;
- See also `Peripheral Console`.

Note: This is EXPERIMENTAL!

# GCC Example: Peripheral Console (LiteOS)

This example is the same as [Keil version](../../../examples/peripheral_console/doc/index.md) of this example, except that the RTOS (Huawei LiteOS) is within the app but not the platform, and `EXT_INT` key event report is not available, either.

# GCC Example: Peripheral iBeacon

This example demonstrates how to:

- Create an iBeacon without writing code;
- Create multiple iBeacons using different advertising sets.

# GCC Example: iBeacon

See the [Keil version](../../../examples/peripheral_ibeacon/doc/index.md) of this example.

# GCC Example: Smart Home Hub

This example demonstrates how to:

- Use Nim together with C:
  - Compile time evaluation;
  - Functional programming;
- Design an BLE hub (BLE gateway) supporting lights and thermometers;
- Use central role to:
  - Scan & connect to peripheral devices;
  - Discovery SIG and user defined services & characteristics;
  - Get notification when characteristics value updated;
- Indicate values;
- Use multiple central & multiple periphral roles simultaneously.

Note:

1.  This demo searches for peripherals with specific addresses;
2.  Peripherals should support SIG Health Thermometer and/or INGChips LED service;
3.  This demo only support ING918xx.

# GCC Example: Smart Home Hub

This example is developed using [Nim](https://nim-lang.org) programming language. It demonstrates how to:

- Use Nim together with C:
  - Compile time evaluation;
  - Functional programming;
- Design an BLE hub (BLE gateway) supporting lights and thermometers;
- Use central role to:
  - Scan & connect to peripheral devices;
  - Discovery SIG and user defined services & characteristics;
  - Get notification when characteristics value updated;
- Indicate values;
- Use multiple central & multiple periphral roles simultaneously.

## Build

| :exclamation: This demo only support ING918xx. |
|:-----------------------------------------------|

To build this project, both Gnu Arm Toolchain & 32-bit Nim are needed.

Set `NIM_PATH` to the path containing `nim` executable, and `make`.

## Test

To test this project, another *room* project is needed.

### The *room* Project

Develop a peripheral project which contains the SIG [Health Thermometer service](../../../examples/thermo_ota/doc/index.md) and/or [INGChips LED service](../../../examples/peripheral_led/doc/index.md).

Download the project to 1~4 Dev-Boards using addresses in [`slaveAddreses`](../src/profile.nim).

### Test

Download this project to another Dev-Board, and connect to it using *ING BLE*. After all peripherals are connected, read temperature values and control the LED light in each room.

## Design Details

Modules in [`nimmodules`](../nimmodules/) are converted from C headers by [`c2nim`](https://github.com/nim-lang/c2nim).

# IAR Example: Peripheral iBeacon

This example demonstrates how to:

- Create an iBeacon without writing code;
- Create multiple iBeacons using different advertising sets.

# IAR Example: iBeacon

See the [Keil version](../../../examples/peripheral_ibeacon/doc/index.md) of this example.

# Rowley Example: Peripheral iBeacon

This example demonstrates how to:

- Create an iBeacon without writing code;
- Create multiple iBeacons using different advertising sets.

# Rowley Example: iBeacon

See the [Keil version](../../../examples/peripheral_ibeacon/doc/index.md) of this example.

# SEGGER Example: Peripheral iBeacon

This example demonstrates how to:

- Create an iBeacon without writing code;
- Create multiple iBeacons using different advertising sets.

# SEGGER Example: iBeacon

See the [Keil version](../../../examples/peripheral_ibeacon/doc/index.md) of this example.
