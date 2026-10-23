# INGCHIPS Skills

为 ING916、ING918、ING20 原生 ING SDK 提供文档问答、协议栈与外设开发方案。当前包含一个可独立安装的 skill：**`ingchips-docs`**。

它按芯片和主题查阅官方资料，读取有限上下文，给出带来源的解释和示例代码建议。它不修改工程、不编译、不烧录、不操作硬件。运行检索脚本需要 **Python 3.10+**，仅依赖标准库。

## 选择安装方式

| 使用方式 | 推荐入口 | 需要什么 |
|---|---|---|
| Codex、Claude Code、Cursor、Gemini CLI、OpenCode、GitHub Copilot | 本仓库 Python 安装脚本 | 已下载本仓库、Python |
| 已习惯社区 skills CLI | `npx skills add` | Node.js 及 npm；首次使用通常需联网 |
| 使用 CC Switch 管理多个 AI 工具 | 生成 ZIP，在 CC Switch 中导入 | Python 用于打包，支持 ZIP 安装的 CC Switch |
| 自定义路径或其他兼容 Agent Skills 的工具 | `--dest` 或手动复制整个 skill 文件夹 | 先确认目标工具的技能目录 |

只选择一种方式管理同一份安装，更新时沿用该方式。安装脚本是方便本地使用的可选入口，skill 本身仍是标准 `SKILL.md` 文件夹，不依赖安装器。

## 本地安装：无需 Node.js

以下命令在本仓库根目录运行，也就是同时包含 `ingchips-docs/`、`tools/` 和 `maintenance/` 的目录。Windows 可使用 `python` 或 `py -3`；macOS/Linux 通常使用 `python3`。

先查看支持的工具及目标目录：

```text
python tools/skills.py targets
```

安装到当前用户的 Codex：

```text
python tools/skills.py install --agent codex --scope global --dry-run
python tools/skills.py install --agent codex --scope global
```

也可一次指定多个工具，例如 Claude Code 和 Cursor：

```text
python tools/skills.py install --agent claude-code cursor --scope global
```

安装到指定工程，以下路径替换为实际工程目录：

```text
python tools/skills.py install --agent codex claude-code --project "C:/path/to/firmware"
```

`--scope` 默认是 `project`，未提供 `--project` 时使用命令的当前目录。多个工具使用相同目标目录时只复制一次。

### 工具与目录

以下是安装脚本采用的路径；`~` 表示用户主目录，Windows 通常是 `C:\Users\你的用户名`。目标目录下面还会追加 `ingchips-docs/`。

| 工具 | `--agent` | 工程级目录 | 用户级目录 |
|---|---|---|---|
| Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |

目录依据 Codex 官方文档和 `vercel-labs/skills` 当前兼容表核对，来源见文末。工具版本与前端需要支持 Agent Skills；这里只提供本地 CLI/编辑器技能安装，不表示网页聊天产品能读取本机目录。

如果工具使用了自定义配置路径、环境变量覆盖，或旧版只识别特定目录，请直接指定技能容器目录：

```text
python tools/skills.py install --dest "C:/custom/skills" --dry-run
python tools/skills.py install --dest "C:/custom/skills"
```

实际安装结果是 `C:/custom/skills/ingchips-docs/`，不要把 `ingchips-docs` 再写进 `--dest`。脚本使用表中默认路径，不自动解释各工具的配置文件或环境变量。

### 更新、备份与卸载

重复安装相同内容会显示 `unchanged`。已有内容不同时默认停止；明确替换使用：

```text
python tools/skills.py install --agent codex --scope global --replace
```

替换前会备份旧目录，终端打印备份位置。备份放在技能容器目录的上一级 `.ingchips-skill-backups/` 中，不进入技能扫描目录。复制失败不会发布半份 skill；发布中途失败会回滚已替换的安装。

安装只复制 `ingchips-docs/`，不联网、不更新语料、不修改 AI 工具的配置或 CC Switch 数据库。它使用文件复制，Windows 不需要符号链接权限；遇到其他管理器创建的链接/目录联接会停止，请用原管理器更新。

卸载本脚本安装的副本时，删除安装输出中显示的那一个 `ingchips-docs/` 目录即可；不要删除整个 `skills/`。恢复时把终端提示的备份目录复制回原安装位置。由 CC Switch 或 skills CLI 安装的副本，使用对应管理器卸载。

## 使用社区 skills CLI

参考 [vercel-labs/skills](https://github.com/vercel-labs/skills) 的本地目录安装方式。在本仓库根目录执行：

```text
npx skills add ./ingchips-docs --list
npx skills add ./ingchips-docs --skill ingchips-docs --agent codex --global --copy
npx skills add ./ingchips-docs --skill ingchips-docs --agent claude-code cursor --global --copy
```

`--copy` 让安装副本不依赖本仓库路径持续存在。省略 `--global` 会安装到当前工程，工程级安装时应从目标工程运行，并把 `./ingchips-docs` 换成 skill 的绝对路径。首次运行 npm 可能询问是否下载 skills CLI；Node.js 版本要求以该 CLI 文档为准。

本仓库暂未发布，不提供虚构的远程仓库命令。将来有 Git 仓库地址后，可以把本地源路径换成仓库 URL；本地来源的更新以重新运行安装为准，不依赖远端更新检测。

## CC Switch 安装

### 本地 ZIP 导入（当前推荐）

1. 在本仓库根目录生成只包含 skill 的 ZIP：

   ```text
   python tools/skills.py package
   ```

2. 得到 `dist/ingchips-docs.zip` 和配套 `.sha256` 文件。ZIP 内结构为 `ingchips-docs/SKILL.md` 及所需文档、脚本、许可文件；不包含维护脚本、转换缓存和历史备份。
3. 打开 CC Switch 的 **Skills → 添加 Skill → 从 ZIP 安装**，选择生成的 ZIP。
4. 在已安装技能中，为要使用的应用启用 `ingchips-docs`；不同版本可能使用“安装到”选择器。
5. 在目标 AI 工具刷新技能或开启新会话，核实能找到 `ingchips-docs`。

重新打包使用 `python tools/skills.py package --replace`。按所查 CC Switch 手册，ZIP 中已有同名技能会被跳过；更新 ZIP 副本时，在 CC Switch 中备份/卸载旧项后再导入，或使用你安装版本提供的替换流程。ZIP 导入是本地来源，不会自动获得 GitHub 仓库更新。

### 导入本机已有技能

如果此前已安装到 CC Switch 能扫描的应用目录，可在 **Skills → 添加 Skill → 导入本机已有** 中导入，再为应用启用。它会把技能纳入自身管理；之后沿用 CC Switch 更新。

**Codex 路径区别：**当前 Codex 官方推荐 `~/.agents/skills`，CC Switch 手册仍列出其 Codex 同步目标 `~/.codex/skills`。本脚本采用官方推荐路径；CC Switch 采用其应用配置与存储设置。因此不保证脚本装到 `~/.agents/skills` 后，所有版本的 CC Switch 都能在“本机已有”中发现，ZIP 导入更直接。

CC Switch 的主副本默认位于 `~/.cc-switch/skills`，也可设置为 `~/.agents/skills`，随后由它同步并记录应用启用状态。**仅复制文件到 `~/.cc-switch/skills` 不等于完成 CC Switch 安装**，所以本脚本没有 `--agent cc-switch`，也不改写它的 SQLite 数据库。

### 将来从仓库安装

发布到 GitHub 后，在 CC Switch 的 Skills 仓库管理中填写真实仓库地址、分支以及可选的技能路径 `ingchips-docs`，再从“发现”安装。本仓库当前不进行发布，也无需准备插件市场清单或伪造 CC Switch 配置文件。CC Switch 的 skill 深链接添加的是仓库，不会直接完成单个 skill 的安装。

## 安装后使用

可向工具发送：

```text
使用 ingchips-docs，说明 ING916 UART 接收变长数据的设计，引用官方文档，不修改工程。
```

Codex 可显式使用 `$ingchips-docs`，Claude Code 可使用 `/ingchips-docs`；其他工具通过各自的技能选择器或自然语言选择。若没有出现，核对安装目录中是否直接包含 `ingchips-docs/SKILL.md`，刷新技能或开启新会话。

在安装后的 skill 根目录可以直接检验查询：

```text
python scripts/search_docs.py UART --chip ING916 --topic peripheral --max 3
python scripts/read_excerpt.py pg_ing916/ch-dma.md --line 10 --lines 15
```

文档快照不保证等于项目 SDK 版本；具体限制与来源规则见 [SKILL.md](ingchips-docs/SKILL.md)。

SDK 示例汇编提供 [Markdown 原文版 examples.md](ingchips-docs/references/examples.md)，保留 DOCX 中的标题、正文、表格、代码及链接顺序，不做翻译或改写。原文的 SDK 相对链接仍需在对应 SDK 目录中查看。

## 仓库结构与维护

```text
ingchips_skill/
├── README.md、LICENSE、NOTICE
├── ingchips-docs/       # 唯一安装单元，可整体复制
│   ├── SKILL.md、INDEX.md、catalog.json、sources.json
│   ├── guides/         # 按需加载的场景指南
│   ├── scripts/        # 只读检索与片段读取
│   ├── references/     # 已转换文档
│   └── licenses/       # 第三方许可；根下另有 LICENSE、NOTICE
├── tools/skills.py     # 安装与 ZIP 打包，仅在仓库中运行
├── tests/              # 安装器及打包测试
├── maintenance/        # 维护者手动转换、校验；不安装
└── dist/               # 本地 ZIP 产物，不加入版本控制
```

现有单一 skill 目录可被直接安装，CC Switch 也支持递归发现 `SKILL.md`，无需为了安装再复制一份源目录。仓库级 `.gitignore` 排除了缓存、备份和打包产物，避免将约 115 MB 的转换缓存带入分发。

维护者更新文档：

```text
python -B maintenance/update_docs.py --offline --check
python -B maintenance/update_docs.py --offline
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s maintenance/tests -v
```

详细流程见 [维护说明](maintenance/README.md)。普通安装不会执行转换。

## 许可证

本项目原创脚本、技能指南和仓库说明使用 [Apache License 2.0](LICENSE)。skill 自带同一份许可，安装和 ZIP 打包会保留。

转换后的 INGCHIPS 官方资料保留原版权，Apache-2.0 不替它们授予新的许可。

FreeRTOS 网站文档源仓库的许可为 **CC BY-SA 4.0**，不是内核代码的 MIT；转换后的该部分继续遵循 CC BY-SA 4.0。来源、改动说明和许可范围见 [NOTICE](NOTICE)，许可全文随 skill 保留。

## 安装方式参考

以下是文档和源码依据；不表示已在每个 AI 客户端的所有版本上实机验证。

- [Codex 官方：Skills 与发现目录](https://developers.openai.com/codex/skills/)
- [vercel-labs/skills：安装命令及本地源支持](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
- [vercel-labs/skills：各 Agent 的目录映射](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
- [vercel-labs/skills：skill 目录结构与发现规则](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md)
- [CC Switch：Skills 管理、ZIP 导入及本机导入](https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/zh/3-extensions/3.3-skills.md)
- [CC Switch：实际目录扫描与 ZIP 安装实现](https://github.com/farion1231/cc-switch/blob/main/src-tauri/src/services/skill.rs)
- [CC Switch：深链接的 skill 仓库导入限制](https://github.com/farion1231/cc-switch/blob/main/docs/guides/deeplink-site-integration-guide-zh.md)
