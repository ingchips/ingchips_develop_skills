# 使用 AI

开发者可以多方式使用 AI 辅助开发。

![](https://ingchips.github.io/docs/getting-started/ai_assistant/ai_matrix.png)

## 代码完成 {#代码完成}

代码完成是最基础的 AI 辅助功能。能根据上下文自动补全代码，提供智能的代码建议， 提升开发效率。它不仅可以补全单行代码，还能生成完整的函数实现。支持代码补全的工具很多，既有 [GitHub Copilot](https://github.com/features/copilot) 等商业方案， 也有 [Cline](https://github.com/cline/cline)、[Twinny](https://github.com/twinnydotdev/twinny) 等开源软件、插件。

由于大模型不“熟悉” SDK，代码完成时可能存在较多“幻觉”。

## AI IDE {#ai-ide}

参考这篇 [博客](https://ingchips.github.io/blog/2024-11-28-dev-with-windsurf/)，配置 AI IDE 环境， 体验“氛围编程”（[Vibe Coding](https://en.wikipedia.org/wiki/Vibe_coding)）。

## 智能问答 {#智能问答}

![](https://ingchips.github.io/docs/getting-started/ai_assistant/ima_kb.png)

## AI 捷径（AI Shortcuts） {#ai-捷径ai-shortcuts}

AI Shortcuts 包含了几种常用功能，使用便捷：

![](https://ingchips.github.io/docs/getting-started/ai_assistant/ai_shortcuts_ui.png)

### 安装 {#安装}

AI Shortcuts 通过 Wizard 安装。打开 Option 窗口的 AI Shortcuts 页面，设置安装路径、热键等。 选择不同可用 GPU 显存大小，向导会自动推荐合适的本地大模型。也选择云端大模型，开发者需要填写申请到的 API Key。 完成设置后，点击 Install/Update 完成安装。后续更改设置后，同样可以点击 Install/Update 完成更新。

![](https://ingchips.github.io/docs/getting-started/ai_assistant/ai_shortcuts_install.png)

### MCP 服务器 {#mcp-服务器}

AI Shortcuts 还是一个 MCP 服务器，包含多种 SDK 和 Wizard 工具。 Wizard Options 窗口的 AI Shortcuts 页面显示了 MCP 服务器 的 URL。 下图显示了 [Qwen Code](https://github.com/QwenLM/qwen-code) 使用该服务器的情形。

![](https://ingchips.github.io/blog/img/ai_shortcuts_mcp.png)

### 演示 {#演示}

下面演示了“详细解释代码”功能。这个演示使用的是 DeepSeek R1：

Your browser does not support the video tag.

- [ING91881B 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91881B/)
- [ING91880 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91880/)
- [DB682AC1A 核心板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91682/)
- [DB72C8K1A 扩展板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/)
- [配置调试工具](https://ingchips.github.io/docs/getting-started/setup_debuggers/)
- [Playground](https://ingchips.github.io/docs/getting-started/playground/)
- [使用 AI](https://ingchips.github.io/docs/getting-started/ai_assistant/)
