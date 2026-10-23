# 使用 UART/USB 接口进行产品量产

## 一对一烧录 {#一对一烧录}

SDK 安装包提供两种版本的一对一串口烧录工具，支持客户通过 UART 或者 USB 接口进行量产。

### GUI 版本 {#gui-版本}

功能特点：

1. 支持批量烧写；
2. 内置烧写计数器；
3. 内置 [RemObjects Pascal Script](https://github.com/remobjects/pascalscript) 脚本引擎。

例如通过以下脚本可根据烧写次数配置产品的蓝牙设备地址：

```highlight
const
  BD_ADDR_ADDR = $1;

procedure OnStartRun(const BatchCounter: Integer; var Abort: Boolean);
begin
end;

procedure OnStartBin(const BatchCounter, BinIndex: Integer;
                     var Data: TBytes; var Abort: Boolean);
begin
  // Note that BinIndex counts from 1 (not 0), just as shown on GUI
  if BinIndex <> 2 then Exit;
  Data[BD_ADDR_ADDR + 0] := BatchCounter and $FF;
  Data[BD_ADDR_ADDR + 1] := (BatchCounter shr 8) and $FF;
  Data[BD_ADDR_ADDR + 2] := (BatchCounter shr 8) and $FF;
end;
```

### Python 3 版本 {#python-3-版本}

功能特点：

1. 支持批量烧写；
2. 内置烧写计数器；
3. 开放源代码；
4. 可嵌入任意 Python 脚本；
5. 便于同其它系统集成。

当通过 USB 接口进行量产时，**推荐使用 Python 3 版本**。

详情请参阅 [用户手册](https://ingchips.github.io/user_guide_cn/core-tools.html#ch2-downloader)。

## 一对多烧录（GUI 版本） {#一对多烧录gui-版本}

[详情及源代码](https://github.com/ingchips/batch-burner/)，[程序下载](https://github.com/ingchips/batch-burner/releases)。

通过 GUI 操作配置监听多个串口进行批量一对多烧录，特性如下

- 最多监听 20 个串口，并行烧录
- 最多配置 6 个二进制文件
- 支持个人化（基于Python）
- 支持地址递增烧录

![mb_burn_0](https://ingchips.github.io/docs/mass_production/uart_burn/mb_burn_0.png)

内置的 Python 脚本编辑工具：

- 保存 File/Save 或者快捷键 Ctrl+S
- 退出 File/Quit 或者快捷键 Esc
- 通过 `import burner` 导入内置的 `burner` 模块，提供烧录工具的一些功能，比如 `burner.AppendLog(...)` 可以将脚本执行过程中的日志打印在烧录工具的日志界面。模块
- `on_start_bin(...)` 函数在每个 bin 烧录之前执行，参数 data 就是当前 bin 文件的二进制数据

![mb_config_script](https://ingchips.github.io/docs/mass_production/uart_burn/mb_config_script.png)

## 关于 USB 烧录 {#关于-usb-烧录}

ING916 通过 USB 烧录后，如果需要立即运行程序（下图中的 Launch App 功能），那么，请勾选 “Always Use Ext Bootloader”。选中后， 将首先把支持外部 Flash 的 bootloader 下载到 RAM 并运行。这个 bootloader 修复了 ROM 里的 bootloader 有时无法立即运行程序的问题。

![](https://ingchips.github.io/docs/mass_production/uart_burn/downloader_usb_troubleshooting.png)

- [使用 UART/USB 接口进行产品量产](https://ingchips.github.io/docs/mass_production/uart_burn/)
- [使用量产套件进行量产](https://ingchips.github.io/docs/mass_production/prod_suite/)
- [使用 SWD 接口进行产品量产](https://ingchips.github.io/docs/mass_production/swd_burn/)
- [IP 保护](https://ingchips.github.io/docs/mass_production/ip_protection/)
