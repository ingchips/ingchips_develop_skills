# 为 ING916 搭建 Zephyr 开发环境

对于 ING916/ING918 的 NoOS 软件包，可以使用 [Zephyr OS](https://docs.zephyrproject.org/latest/index.html) 作为实时内核。SDK v8.4.1 提供了完整的 Controller 接口，可以对接 Zephyr BLE Host 协议栈。这里我们将为 ING916 搭建 Zephyr 开发环境。在这个环境下，开发者可以使用 Zephyr RTOS 及其 BLE 协议栈。

## 1. 开发环境配置 {#1-开发环境配置}

请参考 Zephyr [Getting Started](https://docs.zephyrproject.org/latest/develop/getting_started/index.html) 文档， 大致了解配置步骤。

对于 Windows，与 Zephyr 文档相反，我们推荐在 WSL 1 + Ubuntu 中配置开发环境。在 WSL 1 中配置具有下列优点：

- 无阻碍的跨系统文件访问，可使用 SDK 里的各种 Windows 工具；
- 比 Windows 本地安装相比，在 WSL 1+ Ubuntu 里安装步骤更简单。

下面介绍安装步骤时，**都以 Ubuntu 为例**，其它操作系统请参考 Zephyr 文档相应修改。

### 1.1 安装依赖 {#11-安装依赖}

安装依赖这一步骤主要是把保证以下几项工具满足最低版本要求：

| 工具 | 最低版本 |
| --- | --- |
| CMake | 3.20.5 |
| Python | 3.8 |
| Devicetree Compiler | 1.4.6 |

请参考 [Zephyr 文档](https://docs.zephyrproject.org/latest/develop/getting_started/index.html#install-dependencies) 完成。

### 1.2 安装 Zephyr SDK 工具 {#12-安装-zephyr-sdk-工具}

Zephyr SDK 包含 Zephyr 工具链。[这里](https://github.com/ingchips/breezing-sdk/releases) 是针对 Ubuntu 的剪裁版，删除了不必要的工具，体积小。 也可以下载[完整版](https://docs.zephyrproject.org/latest/develop/getting_started/index.html#install-the-zephyr-sdk)。 两种版本在使用上没有任何区别。

将 Zephyr SDK 解压到[推荐的目录](https://docs.zephyrproject.org/latest/develop/getting_started/index.html#install-the-zephyr-sdk)下， 执行 `setup.sh` 完成安装。

从现在开始，假设工作目录为 `~/zephyrproject`。Zephyr 代码仓库、外部模仓库等都将克隆到这个目录，代码开发、程序编译也发生在这里。 对于 WSL 1 + Ubuntu 的情况，建议将 `zephyrproject` 创建在 Windows 文件系统内。

### 1.3 安装 Python 包 {#13-安装-python-包}

这一步只安装 `west`，其它的 Python 包需要在获取代码后再安装。

Python 包有两种安装方式：全局安装；借助 `venv` 只为单个项目安装。

#### 1.3.1 全局安装 {#131-全局安装}

安装 `west`：`pip install west`

#### 1.3.2 使用 venv {#132-使用-venv}

对于 Ubuntu，此时需要安装 `venv` 包：

```highlight
sudo apt install python3-venv
```

创建并激活虚拟环境，然后安装 `west`：

```highlight
python3 -m venv ~/zephyrproject/.venv
source ~/zephyrproject/.venv/bin/activate
pip install west
```

### 1.4 获取 INGCHIPS SDK {#14-获取-ingchips-sdk}

- Windows

  对于 Windows 系统，如果尚未安装 [SDK](https://ingchips.github.io/docs/sdk/download/)，请下载安装。
- 其它操作系统

  对于其它操作系统，请克隆 [SDK 代码仓库](https://github.com/ingchips/ING918XX_SDK_SOURCE)，参考 [说明](https://github.com/ingchips/ING918XX_SDK_SOURCE/blob/master/tools/README.md#file-generator) 生成必要的文件。

## 2. 获取代码 {#2-获取代码}

### 2.1 获取代码仓库 {#21-获取代码仓库}

![](https://ingchips.github.io/blog/img/logo_breezing.png)

[Breezing](https://github.com/ingchips/breezing) 是 Zephyr 剪裁适配版，删除了不必要的芯片型号、代码， 以及所有的版本历史记录，克隆更快捷。开发者也可以使用 [完整版](https://github.com/ingchips/zephyr)。 两种版本在使用上没有任何区别。

选用 Breezing，克隆所有的代码仓库：

```highlight
west init -m https://github.com/ingchips/breezing.git ~/zephyrproject
cd ~/zephyrproject
west update
```

### 2.2 继续安装 Python 包 {#22-继续安装-python-包}

- 自动安装其它包：

  `pip install -r ~/zephyrproject/zephyr/scripts/requirements.txt`
- 或者只安装必要的包：

  `pip install pyelftools`

对于全局安装方式，Python 包安装已完成，后续不再需要任何操作。对于 `venv` 安装方式：

- 如果再次克隆了代码仓库，需要在新的目录下重新执行上述步骤；
- 调用 Python 工具时，注意检查项目里的虚拟环境是否已激活。

### 2.3 链接到 INGCHIPS SDK {#23-链接到-ingchips-sdk}

- 对于 SDK 安装到 Windows 的情况

  假设安装目录为 `C:\Programs\ING_SDK`。如果 Zephyr 配置在 WSL 1 + Ubuntu 里，那么执行这个命令将 Zephyr 链路到该目录：

  ```highlight
  python3 ~/zephyrproject/zephyr/scripts/utils/select_sdk.py /mnt/c/Programs/ING_SDK/sdk
  ```

  如果 Zephyr 配置在 Windows 里，那么执行这个命令将 Zephyr 链路到该目录：

  ```highlight
  python path\to\zephyrproject\zephyr\scripts\utils\select_sdk.py C:\Programs\ING_SDK\sdk
  ```

  请将 `path\to\zephyrproject` 替换为 `zephyrproject` 的实际路径。
- 其它情况

  假设克隆到目录 `~/ING_SDK`，执行命令将 Zephyr 链路到该目录：

  ```highlight
  python3 ~/zephyrproject/zephyr/scripts/utils/select_sdk.py ~/ING_SDK
  ```

**注意:** 每次更新 INGCHIPS SDK 后，请重新运行 `select_sdk.py` 脚本。

## 3. 编译、运行 {#3-编译运行}

### 3.1 代码编译 {#31-代码编译}

```highlight
cd ~/zephyrproject/zephyr
west build -b ing9168_mini samples/bluetooth/direct_adv
```

当需要完全重新编译（如修改设备树、更新 INGCHIPS SDK 时），可添加 `-p` 选项。

### 3.2 代码烧录 {#32-代码烧录}

根据使用的操作系统不同，代码烧录方法也不尽相同。

#### 3.2.1 WSL 1 + Ubuntu {#321-wsl-1--ubuntu}

- 用图形界面版本的 Flash Downloader 烧录

  用 Flash Downloader 打开 `~/zephyrproject/zephyr/flash_download.ini`。如果 bin 路径非法，请手动更正。
- 使用 Windows 下的 `icsdw.py` 脚本

  同样使用 `~/zephyrproject/zephyr/flash_download.ini` 作为项目文件（第 1 个参数）。如果 bin 路径非法，请手动更正。

#### 3.2.2 其它情况 {#322-其它情况}

在宿主操作系统上运行 `icsdw.py` 下载：

```highlight
python3 icsdw.py ~/zephyrproject/zephyr/flash_download.ini
```

#### 3.2.3 远程下载 {#323-远程下载}

还可以在非 Zephyr 所在的机器上使用 `icsdw.py` 进行远程下载。比如 Zephyr 在 MacOS 或 Ubuntu 上开发、编译， 下载则在 Windows 上完成。

1. 在开发机上启动 HTTP 服务器，比如

   ```highlight
    cd ~/zephyrproject/zephyr/build/zephyr`
    python3 -m http.server
   ```

   假设服务器 IP 地址为 `192.168.206.128`。
2. 在 Windows 远程读取文件并下载

   ```highlight
    python icsdw.py http://192.168.206.128:8000/zephyr.bin --addr 0x02027000 --loop
   ```

   这里 `--addr` 指定下载地址；`--loop` 表示多次下载，根据屏幕提示可重复多次下载，适合开发阶段频繁更新程序的场景。

## 4. 代码说明 {#4-代码说明}

SoC 相关代码位于 `zephyr/soc/arm/ingXXXX` 目录下，实现了 `gen_os_driver` 接口和低功耗。

BLE HCI 相关代码位于 `zephyr\drivers\bluetooth\hci\h4_ingchips.c`，对接了 `platform` 内的 Controller 和 Zephyr Host。
