# IP 保护

ING918/ING916 内置硬件 IP 保护功能。该保护功能启用后，有效保护客户的固件，防止非法读取。

![concept](https://ingchips.github.io/docs/mass_production/ip_protection/ip_prot_concept.png)

## 启用 IP 保护 {#启用-ip-保护}

### UART/USB 接口 {#uartusb-接口}

在下载工具（Flash Downloader）里点击 Options 按钮，将 Read Protection 使能。如下图所示。

![uart_ip_protection](https://ingchips.github.io/docs/mass_production/ip_protection/uart_setup.png)

当使用 Python 版的 USB 下载工具时：先用 Flash Downloader 打开相应的 ini 文件，使能 Read Protection， 关闭 Flash Downloader；然后下载。

### SWD 接口 {#swd-接口}

- ING918

  参考通过 SWD 接口进行量产的[说明](https://ingchips.github.io/docs/mass_production/swd_burn/)，用 platform_entry_lock.hex 代替 platform_entry.hex。
- ING916

  参考通过 SWD 接口进行量产的[说明](https://ingchips.github.io/docs/mass_production/swd_burn/)，用 platform_lock.hex 代替 platform.hex。

## 注意事项 {#注意事项}

IP 保护一旦启用，SWD 接口将被屏蔽，此后如果需要升级、更新产品固件，方法有二：

1. 利用 FOTA 进行空中升级；
2. 通过 UART 接口先停用 IP 保护（如前述，停用 IP 保护意味着 Flash 被全部擦除一次）。

   **提醒:** 对于 ING918，出厂前写入的 ADC 校准数据也将丢失。如需备份数据，请联系技术支持。

**注意:** 如果客户产品中既未引出 UART0，也无 FOTA 功能，则产品固件将进入“锁定”状态： 无法升级、无法读取、无法调试。

- [使用 UART/USB 接口进行产品量产](https://ingchips.github.io/docs/mass_production/uart_burn/)
- [使用量产套件进行量产](https://ingchips.github.io/docs/mass_production/prod_suite/)
- [使用 SWD 接口进行产品量产](https://ingchips.github.io/docs/mass_production/swd_burn/)
- [IP 保护](https://ingchips.github.io/docs/mass_production/ip_protection/)
