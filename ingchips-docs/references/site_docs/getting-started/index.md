# 快速上手

桃芯 SDK 包含核心工具、平台代码包、程序示例及文档。

## 0. 获取开发板 {#0-获取开发板}

在淘宝商城 [购买开发板](https://shop362579575.taobao.com/search.htm?spm=a1z10.3-c-s.0.0.45e679edEnctyQ&search=y&orderType=hotsell_desc)。

**立即体验:** 现在，使用 [Playground](https://ingchips.github.io/docs/getting-started/playground)（游乐园）软件 ， **不需要**任何开发经验，甚至**不需要**懂英语， 只需要一块 [ING91881B 开发板](https://ingchips.github.io/docs/getting-started/dev_board_91881B/) 和一台 Windows 计算机， 立即开始体验桃芯科技。

## 1. 准备开发环境 {#1-准备开发环境}

SDK 不包含开发环境和编译器，用户需要事先准备好所有的开发环境。桃芯 SDK 支持 Keil MDK、IAR 等IDE，也支持 GNU Arm Embedded 工具链。

## 2. 下载 SDK 安装包 {#2-下载-sdk-安装包}

根据所使用的操作系统，[下载](https://ingchips.github.io/docs/sdk/download) 相应的 SDK 版本。

## 3. 安装 SDK {#3-安装-sdk}

SDK 支持两种安装方式：如果只用到 Keil、Gnu 工具链，那么不提升权限就能安装，可以选择“Install for me only”； 如果准备使用 IAR、Segger 等其它开发工具，那么需要提升权限，请选择“Install for all users”：

![](https://ingchips.github.io/docs/getting-started/setup_type.png)

在安装向导的组件选择页面，提供了 IDE/Toolchain 集成选项，勾选某 IDE/Toolchain 表示对该 IDE/Toolchain 做适当配置，而非表示自动安装该 IDE/Toolchain。因此，只需要勾选已安装的开发环境和工具链，不要勾选没有安装的开发环境和工具链。

![](https://ingchips.github.io/docs/getting-started/quick_start_install.png)

## 4. 阅读文档、示例 {#4-阅读文档示例}

安装完毕后，打开 ingWizard，可以查看 SDK [用户手册](https://ingchips.github.io/user_guide_cn/)、示例程序。

开发板的使用方法请参阅[ING91881B 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91881B)、[ING91880 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91880)。

[准备 Markdown 文档查看器](https://ingchips.github.io/docs/faq/#5-如何查看-sdk-示例的-markdown-文档)以便查看 SDK 示例的文档。

## 5. 编译、烧写示例程序 {#5-编译烧写示例程序}

以 LED 示例程序 Peripheral LED 为例， 在 ingWizard 里点击该程序即可在 Keil 里打开，编译后回到 ingWizard 下载程序。 （详情可参考 SDK 用户手册中的[教程](https://ingchips.github.io/user_guide_cn/tutorial.html#编译您的项目)部分）

开发板烧写了 Peripheral LED 程序后，通过手机 App 可以实时控制开发板上的三色 LED。

## 6. 用 APP 连接 {#6-用-app-连接}

[扫码下载](https://ingchips.github.io/docs/sdk/apps) iOS、Android 演示 App（ING BLE）。打开 App，点按扫描按钮，扫描到名为“ING LED”的设备后， 点按设备名以连接到设备，然后在 App 里控制 LED 的 R/G/B 三色分量。

**Note:** iOS/Android 应用需要授予定位权限才能使用蓝牙设备。

## 7. 温馨提示 {#7-温馨提示}

1. 推荐使用 Keil µVision 开发环境。

   **注意:** 需要安装 Keil MDK 版本，而非 51 版本。
2. SDK 目前优先支持 Windows，Linux，MacOS 更新较慢。
3. 开发版支持使用 USB 供电，不需要外接电源。
4. 开发板内置 DAPLink，即插即用。

---

- [ING91881B 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91881B/)
- [ING91880 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91880/)
- [DB682AC1A 核心板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91682/)
- [DB72C8K1A 扩展板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/)
- [配置调试工具](https://ingchips.github.io/docs/getting-started/setup_debuggers/)
- [Playground](https://ingchips.github.io/docs/getting-started/playground/)
- [使用 AI](https://ingchips.github.io/docs/getting-started/ai_assistant/)
