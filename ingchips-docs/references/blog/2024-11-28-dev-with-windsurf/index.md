# 用 Windsurf 打造 AI 辅助集成开发环境

[Windsurf](https://windsurfai.org/) 是一款由 Codeium 开发的智能集成开发环境（IDE），它融合了最先进的 AI 技术，为开发者提供前所未有的编程体验。其号称世界上第一款真正智能化的 IDE，能够与开发者进行自然的对话式交互，真正实现智能协作编程（或称“氛围编程”，[Vibe Coding](https://en.wikipedia.org/wiki/Vibe_coding)）。主要特点：

- **智能代码助手**：内置强大的 AI 助手 Cascade，能够理解开发者的意图，提供准确的代码建议和解决方案。
- **自然语言交互**：开发者可以用自然语言描述需求，Windsurf 能够准确理解并执行相应的编程任务。
- **代码智能分析**：自动分析代码结构和依赖关系，提供深入的代码洞察。
- **协作编程体验**：AI 助手可以作为配对编程伙伴，帮助开发者更快更好地完成编程任务。
- **智能调试能力**：具备强大的代码调试和错误分析能力，帮助开发者快速定位和解决问题。

本文将介绍 Windsurf 结合 INGCHIPS SDK 的配置方法。

**温馨提示：**本文中的配置方式也适用于其它类似的 AI IDE：

- [Cursor](https://www.cursor.com/)；
- [Trea](https://www.trae.com.cn/home)。

## 安装与配置 {#安装与配置}

从 [官网](https://codeium.com/windsurf) 下载并安装。

## 用途 1：问答机器人 {#用途-1问答机器人}

Windsurf 可以作为一个问答机器人，自动阅读文档，回答问题。

1. 克隆或者下载 INGCHIPS 软件文档网站：

   ```highlight
    git clone https://github.com/ingchips/ingchips.github.io.git
   ```

   假设克隆到 `ingchips.github.io` 目录。
2. 按需适当精减内容。

   比如，删除 epub/pdf 文件，删除 `docs-en` 目录，`user_guide` 和 `user_guide_cn` 两个目录只保留其中一个。
3. 用 Windsurf 打开 `ingchips.github.io` 目录，开始问答。

### 对话演示 {#对话演示}

1. 问：SDK v8.4.18 更新了什么？

   ![](https://ingchips.github.io/blog/img/windsurf_ai_assistant.png)

   其中划掉的几项为其它版本的改动，Windsurf 错误地识别了版本号。
2. 问：如何进行 Opus 编码？

   ![](https://ingchips.github.io/blog/img/windsurf_ai_opus_1.png)

   ![](https://ingchips.github.io/blog/img/windsurf_ai_opus_2.png)

## 用途 2：AI 辅助开发 {#用途-2ai-辅助开发}

安装 `clangd` 插件，用于 C/C++ 语言的代码智能分析。插件安装后自动下载 `clangd` 后端程序，请等待下载完成后再使用。

1. 使用 Wizard 以 “**COPY to my project**” 的方式新建项目

   假设新项目的目录为 `c:/tmp/test_sdk`。假设 Wizard 配置的 SDK 路径为 `c:\Program\ING_SDK`。

   可以手动将 SDK 里的例子复制到项目路径下，供 AI 参考。
2. 在项目根目录下新建文件 `.clangd`，内容如下:

   ```highlight
    CompileFlags:
        Add: [-DUSE_STDPERIPH_DRIVER, -D__GNUC__, -D__packed, -Ic:/Program/ING_SDK/wizard/CMSIS/Include, -Ic:/tmp/test_sdk/sdk/bundles/typical/inc, -Ic:/tmp/test_sdk/sdk/bundles/typical/inc/os, -Ic:/tmp/test_sdk/sdk/src/BSP, -Ic:/tmp/test_sdk/sdk/src/FWlib, -Ic:/tmp/test_sdk/sdk/src/StartUP/ing918, -Ic:/tmp/test_sdk/sdk/src/Tools, -Ic:/tmp/test_sdk/sdk/src/SigMesh/inc/mesh, -Ic:/tmp/test_sdk/sdk/src/SigMesh/inc/mesh_host]
   ```

   **说明：**测试表明这里似乎必须使用绝对路径，有待进一步研究。另请参考这个 [讨论](https://github.com/clangd/clangd/discussions/903)。
3. 使用 Windsurf 打开项目，浏览代码，确认 `clangd` 后端已经启动，可以进行智能分析。

   ![](https://ingchips.github.io/blog/img/windsurf_clangd_working.png)

   注意，图中给出了所用函数各参数的名称，对于参数较多的函数，这个功能非常有用。

现在就可以体验 Windsurf 的完整功能了。我们用 Wizard 创建一个广播数据、Profile 都为空的 ING918 Keil 工程。

**温馨提示：**Windsurf 会积极地参与开发过程，请务必注意使用 git 等版本控制工具。

### 演示 1. 设置广播名称 {#演示-1-设置广播名称}

尝试用 Windsurf 设置广播名称。在 Cascade 里输入“set device name to “WINDSURF” in adv data”，它能够自动分析代码， 找到正确的位置，完成设置：

![](https://ingchips.github.io/blog/img/windsurf_cascade_adv_data.png)

更新后的广播数据：

![](https://ingchips.github.io/blog/img/windsurf_ai_update_adv_data.png)

`adv_data` 里的广播名称设置了为“WINDSURF”。

### 演示 2. 加入低功耗功能 {#演示-2-加入低功耗功能}

尝试用 Windsurf 加入低功耗功能。它从 SDK 里找到了 `power_ctrl` lib，在正确的位置添加了 3 个函数的调用。

![](https://ingchips.github.io/blog/img/windsurf_ai_power_lib.png)

提醒 Windsurf 需要找一个 platform 的低功耗配置，它就在 `app_main` 里使能了低功耗，但是使能标志是“幻想”出来的 `ENABLE`， 告诉 Windsurf `ENABLE` 未定义，最终修改如下：

![](https://ingchips.github.io/blog/img/windsurf_ai_platform_cfg.png)

编译发现缺少 `power_ctrl` lib 3 个函数的定义。把这个信息告诉 Windsurf，它首先询问是否把 `power_ctrl.lib` 拷贝到 `src` 目录，拒绝并告诉它可以直接添加到工程，它就自动修改了 `.uvprojx` 工程文件：

![](https://ingchips.github.io/blog/img/windsurf_ai_modify_project.png)

## 总结 {#总结}

INGCHIPS SDK 可以方便地与 Windsurf 结合，在项目开发过程中充分利用 Windsurf 带来的智能化编程。
