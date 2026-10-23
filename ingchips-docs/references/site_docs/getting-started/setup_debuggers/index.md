# 配置调试工具

当存在多个 J-Link 版本时，SDK 安装包只会为最近安装的 J-Link 软件添加芯片支持包； SDK 安装包目前不支持为 [pyOCD](https://pyocd.io/) 等工具添加芯片支持包。对于这些情况，可以使用 SDK 附带的 Python 脚本 [`ingchips_packs_addon.py`](https://github.com/ingchips/ING918XX_SDK_SOURCE/blob/master/tools/ingchips_packs_addon.py) 为调试工具添加芯片程序下载和调试支持。

通过 `-h` 参数获取脚本使用帮助：

```highlight
python ingchips_packs_addon.py -h
```

## pyOCD {#pyocd}

假设 SDK 安装目录为 `C:\Programs\ING_SDK`。

### 安装 pyOCD {#安装-pyocd}

```highlight
pip install pyocd
```

使用镜像源加速pyocd安装

```highlight
pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple pyocd
```

### 更新 pack 索引 {#更新-pack-索引}

**注意必须先更新pack索引否则更新pack支持可能会失败**

```highlight
pyocd pack update
```

### 执行 Python 脚本 {#执行-python-脚本}

```highlight
python ingchips_packs_addon.py -t pyocd -tp "C:/Programs/ING_SDK"
```

## J-Link {#j-link}

假设 SDK 安装目录为 `C:\Programs\ING_SDK`。

### V6.80 - V7.60 版本 {#v680---v760-版本}

假设 J-Link 的安装目录为 `C:\Program Files (x86)\SEGGER\JLink_V630d`

执行 Python 脚本

```highlight
python ingchips_packs_addon.py -t jlink_v6 -p "C:/Program Files (x86)/SEGGER/JLink_V630d" -tp "C:/Programs/ING_SDK"
```

### V7.62 以上 {#v762-以上}

执行python脚本

```highlight
python ingchips_packs_addon.py -t jlink_v7 -tp "C:/Programs/ING_SDK"
```

## pyOCD 新版本更新出现的问题（版本大于0.36.0） {#pyocd-新版本更新出现的问题版本大于0360}

pyOCD 版本 >= 0.36.0版本默认关闭了源码的双缓冲区烧录，导致烧录速度性能下降（官方关闭该功能原因未知）。并且新版本的日志格式变化导致 VSCode 的 Cortex-Debug 插件无法正常连接识别 gdb 服务器的启动。

### 烧录速度性能下降解决方案 {#烧录速度性能下降解决方案}

直接修改源码增加双缓冲机制。

1. 克隆仓库源码

   ```highlight
   git clone https://github.com/pyocd/pyOCD.git
   ```
2. 打开安装的 pyOCD 版本源码 (打开源码，打开类似如下路径的 *builder.py* 文件。)

   ```highlight
   path\to\pyocd\flash\builder.py
   ```
3. 打开这个文件找到文件的204行，查看到源代码如下：

   ```highlight
   ...
       def __init__(self, flash):
           super().__init__()
           self.flash = flash
           self.flash_start = flash.region.start
           self.flash_operation_list = []
           self.sector_list: List[_FlashSector] = []
           self.page_list: List[_FlashPage] = []
           self.perf = ProgrammingInfo()
           self.enable_double_buffering = False
           self.log_performance = True
           self._buffered_data_size = 0
           self.program_byte_count = 0
           self.sector_erase_count = 0
           self.chip_erase_count = 0 # Number of pages to program using chip erase method.
           self.chip_erase_weight = 0 # Erase/program weight using chip erase method.
           self.sector_erase_count = 0 # Number of pages to program using sector erase method.
           self.sector_erase_weight = 0 # Erase/program weight using sector erase method.
           self.algo_inited_for_read = False
   ...
   ```

   将 `self.enable_double_buffering = False` 修改为 `self.enable_double_buffering = True` 这样开启双缓冲可以加速下载。
4. 在项目根目录重新安装

   ```highlight
   python -m pip install -e .
   ```

### Cortex-Debug 插件无法连接的方案 {#cortex-debug-插件无法连接的方案}

为 VSCode 的 `launch.json` 文件添加对应的配置信息：

```highlight
"overrideGDBServerStartedRegex":"(started|Listening) on port"
```

pyOCD 使用 `launch.json` 文件的示例：

```highlight
{"version":"0.2.0","configurations":[{"name":"Cortex Debug (pyOCD + ING916XX)","type":"cortex-debug","request":"launch","cwd":"${workspaceFolder}","executable":"${workspaceFolder}/cmake-build-debug-mingw-arm/ING20XX","servertype":"pyocd","targetId":"ING91600","runToEntryPoint":"app_main","interface":"swd","armToolchainPath":"C:\\arm_gcc\\bin\\","showDevDebugOutput":"raw","overrideGDBServerStartedRegex":"(started|Listening) on port"}]}
```

使用时：

- `executable` 需要替换为实际的 elf 文件路径；
- `targetId` 需要替换为实际的芯片 id；
- `armToolchainPath` 需要替换为实际的 `arm-none-eabi-gdb` 文件所在路径。

- [ING91881B 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91881B/)
- [ING91880 开发板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91880/)
- [DB682AC1A 核心板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_91682/)
- [DB72C8K1A 扩展板使用手册](https://ingchips.github.io/docs/getting-started/dev_board_db72c8k1a/)
- [配置调试工具](https://ingchips.github.io/docs/getting-started/setup_debuggers/)
- [Playground](https://ingchips.github.io/docs/getting-started/playground/)
- [使用 AI](https://ingchips.github.io/docs/getting-started/ai_assistant/)
