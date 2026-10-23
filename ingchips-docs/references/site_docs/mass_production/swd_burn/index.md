# 使用 SWD 接口进行产品量产

ING918/ING916 系列芯片支持使用 IDE 或者专门的 JTAG/SWD 工具通过 SWD 接口进行批量烧写。具体操作步骤如下。

说明：下文以 ING918 为例说明，ING916 类似。

## 使用 Keil 量产 {#使用-keil-量产}

**说明:** 以下步骤介绍了烧写用 Keil 项目的具体创建方法，Keil μVision 4 或 5 皆适用。 用户可以按照步骤自行创建或者直接 [下载](https://ingchips.github.io/files/keil_burn_plt_start.zip) 我们提供的示例。

### 环境需求 {#环境需求}

- Keil μVision 4 或 5
- 支持 SWD 接口的调试器（如 DAPLink/ULINK/J-Link 等）

### 准备项目 {#准备项目}

1. 创建空白项目

   在 Keil 里新建一个项目，CPU 选为 INGCHIPS -> ING91800。项目创建完成后，确认不包含任何源代码（C 或汇编），如果有， 则将其删除。
2. 修改项目的属性：

   - 将输出的可执行文件改为 platform_entry.hex （注意扩展名为 .hex）

     ![keil4_exe_name](https://ingchips.github.io/docs/mass_production/swd_burn/exe_name_v4.png)
   - 检查 Flash 烧写算法设置是否正确

     ING918 烧写算法已将 Erase 操作内置于 Program，所以不需要勾选“Erase”；一般情况下，为了提高量产速度，“Verify” 也可以不勾选。其它各设置的建议值如下图。

     ![keil5_settings](https://ingchips.github.io/docs/mass_production/swd_burn/burn_algo_v5.png)
   - 确认选择了 SWD 端口而非 JTAG 端口（ING918 只有 SWD 端口，无 JTAG 端口）
3. 复制 platform_entry.hex

   在 SDK 目录中找到与芯片型号对应的 platform_entry.hex，复制到 Keil 项目目录下。

   **说明:** 假设 SDK 的安装路径为 /ING_SDK，则 ING9188xx 系列芯片的 platform_entry.hex 存放于 /ING_SDK/sdk/bundles/typical/ING9188xx。
4. 烧写测试

   在 Keil 里直接点击 Flash Download 按钮即可完成烧写。如果出现错误，请对照检查项目设置是否有误。

### 量产 {#量产}

量产时通过命令行调用 Keil 实现批量烧写:

```highlight
C:\Keil\UV4\UV4 -f C:\project\platform\platform.uvproj
```

## 使用 J-Link 量产 {#使用-j-link-量产}

### 环境需求 {#环境需求-1}

- J-Link 调试器
- [J-Link 软件](https://www.segger.com/downloads/jlink/) v6.80c 或更新版本

**说明:** SDK 安装包不能保证自动为 J-Link 添加芯片支持包。如果无法在找到 INGCHIPS 系列芯片， 那么使用 [Python 脚本](https://ingchips.github.io/docs/getting-started/setup_debuggers/#j-link) 添加。

### 创建 J-Flash 项目 {#创建-j-flash-项目}

打开 J-Flash，新建一个项目，Target Device 选为 ING9188xx。

![target_ing9188xx](https://ingchips.github.io/docs/mass_production/swd_burn/jlink_target_sel.png)

将要写入产品的 platform_entry.hex 拖入 J-Flash 界面。点击 Target -> Connect 菜单， 然后点击 Target ->Manual Programming -> Program，即可将 platform_entry.hex 烧写到产品。

**注意:** J-Flash 需要注册方可使用全部功能。

### 合并数据 {#合并数据}

为了量产方便，可以通过 File -> Merge data file 菜单将前文提到的 platform_entry.hex 和产品固件合并 为一个 hex 数据文件。

### 量产 {#量产-1}

量产时通过命令行调用 J-Flash 实现批量烧写。

## 使用其它 IDE 进行量产 {#使用其它-ide-进行量产}

### IAR Embedded Workbench for ARM {#iar-embedded-workbench-for-arm}

参考 *[Programming binary file(s) into flash](https://www.iar.com/support/tech-notes/general/programming-binary-files-into-flash-within-ewarm/)*。

### Rowley CrossWorks / SEGGER Embedded Studio {#rowley-crossworks--segger-embedded-studio}

在项目选项中把 platform_entry.hex 作为额外需要下载的文件即可。

![extra_bin](https://ingchips.github.io/docs/mass_production/swd_burn/segger_extra_bin.png)

## HEX 文件说明 {#hex-文件说明}

SDK 提供关于 platform 的多个 hex 文件，各自的用途总结如下：

- **platform.hex**：用于产品研发、调试过程中 SDK 的升级；可用于全新的 ING916 芯片的首次烧写；
- **platform_entry.hex**：（仅用于 ING918）将**新**芯片用于研发、调试时的首次烧写；
- **platform_entry_lock.hex**：（仅用于 ING918）用于产品最终量产（启用 IP 保护）；
- **platform_lock.hex**：（仅用于 ING916）用于产品最终量产（启用 IP 保护）。

- [使用 UART/USB 接口进行产品量产](https://ingchips.github.io/docs/mass_production/uart_burn/)
- [使用量产套件进行量产](https://ingchips.github.io/docs/mass_production/prod_suite/)
- [使用 SWD 接口进行产品量产](https://ingchips.github.io/docs/mass_production/swd_burn/)
- [IP 保护](https://ingchips.github.io/docs/mass_production/ip_protection/)
