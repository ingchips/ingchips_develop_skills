# DB72C8K1A 扩展板使用手册

## 1、概述 {#1概述}

该文档主要介绍桃芯科技 DB72C8K1A 扩展板的硬件资源及其使用方法。

**注意:** 扩展板不包含 INGCHIPS SoC，需与核心板连接使用。

## 2、硬件资源 {#2硬件资源}

主要包括温度传感器、加速度传感器、按键、LED、蜂鸣器等相关资源。

![](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/board_overview.png)

**图 1 开发板**

### 2.1、供电 {#21供电}

通过 micro USB 接口供电。

### 2.2、调试接口 {#22调试接口}

开发板集成了 [DAPLink (CMSIS-DAP 的升级版)](https://daplink.io/) 功能， 支持 CDC 串口、拖放烧写。该功能通过一片 STM32 来实现，实际使用中通过 micro USB 接口与 PC 机通信。 虚拟出的串口端口号在 PC 机设备管理器中查看，此串口使用丝印为 UART_TX 和 UART_RX 的两个管脚。 DAPLink 使用丝印为 SW_CLK 和 SW_DIO 的两个管脚。

DAPLink 固件 [开源](https://github.com/ingchips/DAPLink)。

**说明:** 不同调试器提供的串口能力不同，某些调试器从 ING91X 向 PC 机进行高速传输时可能丢失数据。 而 ING91X 可立即响应串口数据，所以从 PC 机到 ING918 传输时不存在此问题。 例如使用了相同型号 STM32 芯片的 DAPLink 与 J-Link OB，以 921600 波特从 ING91X 向 PC 机传输时，DAPLink 不丢数据， 而 J-Link OB 则存在问题。

### 2.3、传感器 {#23传感器}

开发板自带两颗传感器，MTS01B 和 STK8BA58，IIC 接口，对应管脚的丝印为 IIC_SCL 和 IIC_SDA。 MTS01B 为温度传感器，IIC 地址为 0b1000100；STK8BA58 为三轴加速度传感器，IIC 地址为 0b0011000。

有关传感器的使用方法，可参考以下示例：

- Thermometer with FOTA （温度计）
- Peripheral Pedometer （计步器）

### 2.4、LED {#24led}

开发板上有 1 个三色 LED 和 4 个绿色 LED，三色 LED 可以用于 PWM 调光功能，绿色 LED 可以做为指示灯。三色 LED 通过专门的三色调光芯片 TLC57931，该芯片 通过单线发送相应的控制命令，对应的管脚丝印为 TLED。

有关 LED 的使用方法，可参考以下示例：

- Peripheral LED （控制三色 LED）

### 2.5、按键 {#25按键}

开发板上的按键分为两种：

1. 系统按键

   用于复位芯片，位置见图 1 中 RESET 标志处，用于复位 ING91X。
2. 功能按键

   KEY1-4 用户可以自行分配功能，位置见图 1。默认上拉，按下为低。 各按键对应的管脚丝印为 KEY1 ~ KEY4。

   有关按键的使用方法，可参考以下示例：

   - HID Keyboard （蓝牙键盘示例）
   - Peripheral ANCS （苹果通知中心服务）

### 2.6、蜂鸣器 {#26蜂鸣器}

开发板上包含 1 个蜂鸣器，工作频率 4KHz，对应的管脚丝印为 BUZZER。

有关蜂鸣器的使用方法，可参考以下示例：

- Peripheral Piano （通过 PWM 驱动蜂鸣器）

### 2.7、ADC {#27adc}

开发板上留有模拟电压输出 AIN，其电压由可调电压控制，可用于测试芯片的 ADC 功能。

有关 ADC 的使用方法，可参考以下示例：

- Peripheral Battery （通过 ADC 监测电压）

## 3、烧写程序 {#3烧写程序}

### 3.1、用 Flash Downloader 烧写 {#31用-flash-downloader-烧写}

1. 在 ingWizard 主界面找到要下载的项目，点击右键；

   ![](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/start_download.png)
2. 从弹出的快捷菜单中选择“Download to Flash…”，ingWizard 自动打开 Flash Downloader；
3. 在 Flash Downloader 里点击“Setup UART”修改开发板使用的串口号；
4. 点击“Start”；

   ![](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/start_downloading.png)

   **说明:** 一般情况下一个完整的程序包含两个二进制文件，platform.bin（包含协议栈、实时内核）和 App Bin。程序编译时，只有 App Bin 发生变化，platform.bin 不变。所以 platform.bin 只需要烧写一次。 详情请参阅 SDK [用户手册](https://ingchips.github.io/user_guide)关于[软件架构](https://ingchips.github.io/user_guide_cn/intro.html#架构)的介绍。
5. 按动一次下载键（丝印为 LOAD），开发板即可进入下载模式。下载过程中界面显示如图所示。

   ![](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/downloading_gui.png)

### 3.2、使用调试器烧写 {#32使用调试器烧写}

所有示例都可以在（支持 CMSIS-DAP 的） IDE 直接通过 DAPLink 调试器下载，例如在 Keil 里直接点击“Download”。 如果开发者选择使用 J-Link 调试器，那么所有示例都可以在 IDE 直接通过 J-Link 调试器下载，例如在 Keil 里直接点击“Download”。

**注意:** 此方法只烧写 App 编译出的程序，不烧写 platform.bin，所以开发板初次使用时，应该先 使用 Flash Downloader 完整烧写 platform.bin 和 App Bin。 有些 IDE （如 CrossStudio/SEGGER）可以修改设置同时烧写 platform.bin，但是 SDK 中的示例未做此设置。 具体烧写方法请参照“使用 SWD 接口进行产品量产”。

**说明:** 如果单独安装过 J-Link 软件，第一次下载时 J-Link 将弹出对话框要求 用户选择芯片类型。需要根据核心板上的芯片型号选择。对于 ING916，请选择“Unspecified Cortex-M4”。

### 3.3、拖放烧写 {#33拖放烧写}

DAPLink 调试器会在上位机里呈现一个 U 盘，将 .bin 文件或者 .hex 文件复制（通过命令行或者**拖放**）到 U 盘即可完成烧写。 烧写完成后，U 盘会重新挂载，查看 U 盘内的 DETAILS.TXT 文件，可发现 Remount count 计数增加 1。如果烧写失败，则会出现 FAIL.TXT 文件，里面包含了详细错误信息；如果烧写成功，U 盘内无此文件。无论烧写是否成功，重新挂载后的 U 盘都不会“保存” 所烧写的 .bin 文件或者 .hex 文件。

![](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/dap_drag.png)

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
