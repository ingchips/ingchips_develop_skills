# ING91880 开发板使用手册

## 1、概述 {#1概述}

该文档主要介绍桃芯科技 ING91880 开发板的硬件资源及其使用 方法，以使研发人员了解 ING9188 系列芯片的硬件资源，并测试其功能， 使开发人员尽快掌握 ING9188 系列芯片的使用。

## 2、硬件资源 {#2硬件资源}

ING91880 的开发板见下图，主要包括温湿度传感器、加速度传感 器、SPI Flash、按键、LED、蜂鸣器等相关资源。

![](https://ingchips.github.io/docs/getting-started/dev_board_91880/board_overview.png)

**图 1 开发板**

### 2.1、供电 {#21供电}

ING91880 开发板有两种供电方式:

1. 通过开发板上丝印位号为 J2 的 micro USB 接口供电
2. 通过开发板背面的装入纽扣电池供电

![](https://ingchips.github.io/docs/getting-started/dev_board_91880/power.png)

**图 1 开发板电源拓扑**

开发板上留有 3.3V 对外供电接口，位号为 J8 的插针为 3.3V，位 号为 J7 的插针为 GND，供电时要注意电流限值：通过 micro USB 供电 时，3.3V 电流限值是 200mA；通过纽扣电池供电时，根据具体纽扣 电池的输出能力来确定。

### 2.2、GPIO 功能 {#22gpio-功能}

开发板上丝印位号为 J5，靠近板边的奇数管脚为 ING91880 直接 相连的 GPIO，见下图。用户可以根据实际需要通过排线连接具体的 外部设备，并通过软件配置相应的功能。若要使用开发板上的硬件资 源，比如传感器、串口、蜂鸣器等资源，需要用跳线帽把 J5 对应位 置短接。

![](https://ingchips.github.io/docs/getting-started/dev_board_91880/gpio_conn.png)

**图 3 GPIO 连接情况**

有关 GPIO 的使用方法，可参考以下示例：

- HID Keyboard （蓝牙键盘示例）
- Peripheral ANCS （苹果通知中心服务）

### 2.3、调试接口 {#23调试接口}

开发板集成了 [DAPLink (CMSIS-DAP 的升级版)](https://daplink.io/) 功能， 支持 CDC 串口、拖放烧写。该功能通过一片 STM32 来实现，在开发板上的丝印为 U1，实际使用中通过 micro USB 接口与 PC 机通信， 虚拟出的串口端口号在 PC 机设备管理器中查看，使用此串口与 ING91881B 通信前，必须在 UART_TX 和 UART_RX 处用跳线帽短接。

DAPLink 的 SW_CLK 和 SW_DIO 与 ING918 的 SWD 接口使用跳帽连接，断开跳帽， 既可以将开发板用做 DAPLink 调试其它设备，也可以使用其它调试器来调试开发板。 STM32 芯片的 SW_CLK 和 SW_DIO 用插针引出，可以用来烧写STM32。

DAPLink 固件 [开源](https://github.com/ingchips/DAPLink)。

**说明:** 不同调试器提供的串口能力不同，某些调试器从 ING918 向 PC 机进行高速传输时可能丢失数据。 而 ING918 可立即响应串口数据，所以从 PC 机到 ING918 传输时不存在此问题。 例如使用了相同型号 STM32 芯片的 DAPLink 与 J-Link OB，以 921600 波特从 ING918 向 PC 机传输时，DAPLink 不丢数据， 而 J-Link OB 则存在问题。

### 2.4、传感器 {#24传感器}

开发板自带两颗传感器，BME280 和 BMA280，IIC 接口，通过 ING91880 的 IIC1 接口互联，使用前需在 J5 IIC1 处用跳线帽短接。 BME280 为湿度、压力、温度传感器，IIC 地址为：0b1110110；BMA280 为三轴加速度传感器，IIC 地址为：0b0011000。

有关传感器的使用方法，可参考以下示例：

- Thermometer with FOTA （基于 BME280 的温度计）
- Peripheral Pedometer （基于 BMA280 的计步器）

### 2.5、Flash {#25flash}

开发板上自带了一颗 SPI flash，用于验证 SPI 接口，型号 为 W25Q16DVSS，使用时需在 J5 SPI 处用跳线帽短接。

### 2.6、LED {#26led}

开发板上有 1 个三色 LED 和 1 个绿色 LED，三色 LED 可以用于 PWM 调光功能，绿色 LED 可以做为指示灯。使用前需要在 J5 相应位置用 跳线帽短接，三色 LED 通过专门的三色调光芯片 TLC57931，该芯片 通过单线发送相应的控制命令，插座 J5 中对应的信号为 TLED。

有关 LED 的使用方法，可参考以下示例：

- Peripheral LED （通过 TLC57931 控制三色 LED）

### 2.7、按键 {#27按键}

开发板上的按键分为两种：

1. 系统按键

   用于复位芯片，位置见图 1 中 RESET 标志处，用于复位 ING91880。
2. 功能按键

   KEY1-4 用户可以自行分配功能，位置见图 1 红色标志处所示，默认上拉，按 下为低，使用前需在 J5 相应位置用跳线帽短接。

   有关按键的使用方法，可参考以下示例：

   - HID Keyboard （蓝牙键盘示例）
   - Peripheral ANCS （苹果通知中心服务）

### 2.8、蜂鸣器 {#28蜂鸣器}

开发板上包含 1 个蜂鸣器，工作频率 4KHz，使用前需在 J5 相应 位置用跳线帽短接。

有关蜂鸣器的使用方法，可参考以下示例：

- Peripheral Piano （通过 PWM 驱动蜂鸣器）

### 2.9、ADC {#29adc}

开发板上留有 ADC 接口，J12 用跳线帽短接时，输入电压为 1.65V， 为分压电阻从 3.3V 得到，用户也可以通过跳线外接其他输入，输入 点为 J12 的 1 脚。

有关 ADC 的使用方法，可参考以下示例：

- Peripheral Battery （通过 ADC 监测电压）

### 2.10、配置管脚 {#210配置管脚}

- TESTMODE

  通过 J11 可设置 ING91880 的工作模式，默认为下拉， 正常工作模式，可以通过跳线帽短把 J11 的 1、2 脚短接设置为调试 模式。
- EXTINT

  为外置中断，用于在待机模式下唤醒 ING91880，开发 板上可以通过 BMA280 唤醒，也可通过外部设备唤醒，通过 BMA280 唤醒时，用跳线帽把 J3 的 1、2 脚短接，外部设备唤醒时通过跳线连 接 J3 的 1 脚。图 1 中标志 EXT_INT 的按键与 EXTINT 为同一信号，按 键按下时触发中断。该信号有两种功能：

  1. 复位时使芯片进入烧写模式；
  2. 工作过程中用来将芯片从睡眠模式中唤醒。

### 2.11、芯片功耗测试 {#211芯片功耗测试}

J9 为芯片 ING91880 供电端，**正常使用时，用跳线帽短接**。 测试芯片 ING91880 的供电电流时，把万用表串接在 J9 的两 端。

## 3、烧写程序 {#3烧写程序}

### 3.1、用 Flash Downloader 烧写 {#31用-flash-downloader-烧写}

1. 在 ingWizard 主界面找到要下载的项目，点击右键；

   ![](https://ingchips.github.io/docs/getting-started/dev_board_91880/start_download.png)
2. 从弹出的快捷菜单中选择“Download to Flash…”，ingWizard 自动打开 Flash Downloader；
3. 在 Flash Downloader 里点击“Setup UART”修改开发板使用的串口号；
4. 点击“Start”；

   ![](https://ingchips.github.io/docs/getting-started/dev_board_91880/start_downloading.png)

   **说明:** 一般情况下一个完整的程序包含两个二进制文件，platform.bin（包含协议栈、实时内核）和 App Bin。程序编译时，只有 App Bin 发生变化，platform.bin 不变。所以 platform.bin 只需要烧写一次。 详情请参阅 SDK [用户手册](https://ingchips.github.io/user_guide)关于[软件架构](https://ingchips.github.io/user_guide_cn/intro.html#架构)的介绍。
5. 保持开发板 EXT_INT 按键处于按下状态，按动一次 RESET，开发板即可进入下载模式。下载过程中界面显示如图所示。

   **说明:** 从复位状态释放时，Bootloader 会检测 EXT_INT，如果为高电平则进入 UART 下载模式，否则正常启动。 也就是说若要进入 UART 下载模式，要保证 RESET 按键弹起的瞬间， EXT_INT 按键处于按下状态。

   ![](https://ingchips.github.io/docs/getting-started/dev_board_91880/downloading_gui.png)

### 3.2、使用调试器烧写 {#32使用调试器烧写}

所有示例都可以在（支持 CMSIS-DAP 的） IDE 直接通过 DAPLink 调试器下载，例如在 Keil 里直接点击“Download”。 如果开发者选择使用 J-Link 调试器，那么所有示例都可以在 IDE 直接通过 J-Link 调试器下载，例如在 Keil 里直接点击“Download”。

**注意:** 此方法只烧写 App 编译出的程序，不烧写 platform.bin，所以开发板初次使用时，应该先 使用 Flash Downloader 完整烧写 platform.bin 和 App Bin。 有些 IDE （如 CrossStudio/SEGGER）可以修改设置同时烧写 platform.bin，但是 SDK 中的示例未做此设置。 具体烧写方法请参照“使用 SWD 接口进行产品量产”。

**说明:** 如果单独安装过 J-Link 软件，第一次下载时 J-Link 将弹出对话框要求 用户选择芯片类型，请选择“Unspecified Cortex-M3”。 ![](https://ingchips.github.io/docs/getting-started/dev_board_91880/jlink_m3.png)

### 3.3、拖放烧写 {#33拖放烧写}

DAPLink 调试器会在上位机里呈现一个 U 盘，将 .bin 文件或者 .hex 文件复制（通过命令行或者**拖放**）到 U 盘即可完成烧写。 烧写完成后，U 盘会重新挂载，查看 U 盘内的 DETAILS.TXT 文件，可发现 Remount count 计数增加 1。如果烧写失败，则会出现 FAIL.TXT 文件，里面包含了详细错误信息；如果烧写成功，U 盘内无此文件。无论烧写是否成功，重新挂载后的 U 盘都不会“保存” 所烧写的 .bin 文件或者 .hex 文件。

![](https://ingchips.github.io/docs/getting-started/dev_board_91880/dap_drag.png)

- .bin 文件烧写

  此模式只支持完整烧写，.bin 文件必须**完整**，同时包含 platform.bin 和 App Bin。建议通过 Flash Downloader 菜单项 File → Merge & Export … 自动合并导出完整 .bin 文件，然后烧写。
- .hex 文件烧写

  [Intel Hex](http://en.wikipedia.org/wiki/Intel_HEX) 文件包含地址信息，支持部分烧写。

## 4、注意事项 {#4注意事项}

- 通过开发板给外部设备供电时，注意电流限值；
- 增减外部设备时，请断电；
- 不要用金属部件遮挡印制板天线。

- [ING91881B 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91881B/)
- [ING91880 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91880/)
- [DB682AC1A 核心板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91682/)
- [DB72C8K1A 扩展板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/)
- [配置调试工具](https://ingchips.github.io/docs/getting-started/setup_debuggers/)
- [Playground](https://ingchips.github.io/docs/getting-started/playground/)
- [使用 AI](https://ingchips.github.io/docs/getting-started/ai_assistant/)
