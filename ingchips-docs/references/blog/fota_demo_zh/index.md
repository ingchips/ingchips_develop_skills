# 空中固件升级（FOTA）的快速演示

使用 ING918 系列芯片 SDK 里的 ingWizard 可以为应用轻松加入空中固件升级（FOTA）功能， 用户手册的[教程部分](https://ingchips.github.io/user_guide_cn/tutorial.html#fota温度计)也详细介绍了具体的实现方法。本文是 FOTA 完整功能的快速演示。

**注意:** 本文仅为 FOTA 功能概念演示，不可用于实际产品。在实际产品中使用 FOTA 时，建议参阅 [安全地进行空中固件升级](https://ingchips.github.io/blog/2021-04-20-secure-fota/)。

## 环境准备 {#环境准备}

1. 下载/安装 [ING BLE](https://ingchips.github.io/docs/sdk/apps/) App （若只使用 Web 版工具可跳过此步骤）

   **说明:** 需要 v1.4 以上版本。
2. 下载测试程序升级包

   - ING91881B 开发板：[下载](https://ingchips.github.io/files/thermo_fota_demo_ING91881B.zip)
   - ING91880 开发板：[下载](https://ingchips.github.io/files/thermo_fota_demo.zip)
   - 其它 ING918xx 模块（无需传感器，温度为随机数）：[下载](https://ingchips.github.io/files/thermo_fota_demo_ING9185xx_simulation.zip)
   - ING916xx 开发板/模块（无需传感器，温度为随机数）：[下载](https://ingchips.github.io/files/thermo_fota_demo_916_sim.zip)

   说明：不同程序升级包所使用的 platform 版本号可能与截图中的不同，但不影响演示流程。
3. 烧写测试程序

   解压测试程序升级包，用 Downloader 打开 `full_app` 文件夹下的 `flash_download.ini`，然后烧录到开发板。

如果需要测试在线升级，还需要准备网络环境及 HTTP 服务器，步骤如下。

1. 网络准备

   进行空中升级时，ING BLE 需要联系升级服务器获取信息，所以需要保证 ING BLE 与服务器之间的 TCP/IP 网络畅通。 如果自行编译 Windows 10 版本的 ING BLE 测试程序，可在同一机器上启动 HTTP 服务器。 对于使用手机的情况，可以选用以下任一方法配置网络：

   - 手机与服务器接入同一 WLAN （**推荐**）
   - 服务器开启 WIFI 热点，手机接入该热点
   - 手机开启 WIFI 热点，服务器接入该热点
   - 服务器与手机之间通过 Internet 连接（**不推荐**）
2. 为 ING BLE 准备升级服务器

   对于 ING BLE 的在线模式，直接使用 Python 内置的 HTTP 服务器作升级服务嚣。切换到解压出的文件夹，启动服务器，命令如下（各平台即可，以 WSL 里的 Python 为例）：

   - Python 3

     ```highlight
       $ ls -a
       .  ..  body  full_app  toe ...
       $ sudo python3 -m http.server 80
     ```
   - Python 2

     ```highlight
       $ ls -a
       .  ..  body  full_app  toe ...
       $ sudo python -m SimpleHTTPServer 80
     ```

   检查服务器是否正常工作（假设服务器 IP 地址为 192.168.100.102。下同）：

   ```highlight
    $ curl http://192.168.100.102/body/latest.json
    {
        "app": [1,3,0],
        "platform": [1,0,5],
        "package": "v1.zip"
    }
   ```
3. 为 Web 版工具准备升级服务器

   对于 Web 版升级工具的在线模式，浏览器可能要求服务器使用 HTTPS，并允许资源跨域访问。

   **说明:** 不同浏览器、同一浏览器的不同版本都有可能采用不同的安全策略， 此处搭建的服务器可能无法正常工作（不为浏览器所接受）。如果遇到问题，需要使用浏览器的开发者工具进行调试、解决。

   1. 生成 HTTPS 证书

      ```highlight
       openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
      ```

      此命令成功后，将在当前目录下生成 key.pem 和 cert.pem 两个文件。**显然**，此自行签发的证书无法为浏览器验证、接受。

      ```highlight
       $ ls -a
       .  ..  CrossHTTPServer.py  body  cert.pem  full_app  key.pem  toe
      ```
   2. 启动 CrossHTTPServer 服务器

      升级包内为 Python 2/3 分别准备了一个简单的 CrossHTTPServer。启动服务器，需要输入生成证书时的口令。

      - Python 2 版本

        ```highlight
          $ sudo python CrossHTTPServer.py
          Enter PEM pass phrase: ...
        ```
      - Python 3 版本

        ```highlight
          $ sudo python3 CrossHTTPServer.py
          Enter PEM pass phrase: ...
        ```

## 演示 1：使用手机 App {#演示-1使用手机-app}

如果需要在手机 App 上使用本地模式，需要将几个升级包（v1.zip、v2.zip）事先复制到手机。

用 ING BLE 连接到名为“ING Thermometer”的蓝牙设备，查看温度计显示为“Body”状态。

![](https://ingchips.github.io/blog/img/fota_body_app.jpg)

1. 部分升级到“Toe”版本

   - 在线模式

     进入 FOTA 服务，在升级服务 URL 里填入“http://192.168.100.102/toe”，点击“Re-check”按钮，出现版本升级提示信息。 点击 “Update” 按钮完成升级。由于此时 platform 版本一致，故升级过程中只升级了 App Bin，速度很快。

     ![](https://ingchips.github.io/blog/img/fota_toe_update_ready.jpg)
   - 本地模式

     **注意:** 使用本地模式之前需要等待 App 退出在线模式的 “Checking” 状态（这可能需要一段时间。事先屏蔽 App 的互联网访问，可以使 App 快速退出 “Checking” 状态）。

     点击“Local File”按钮，然后选择 v2.zip，会出现与在线模式相同的版本升级提示信息。点击“Update”按钮完成升级。

     ![](https://ingchips.github.io/blog/img/fota_app_local_mode.png)

     后续步骤只演示在线模式，本地模式用法类似。

   重新连接到“ING Thermometer”，查看温度计显示为“Toe”状态。

   ![](https://ingchips.github.io/blog/img/fota_toe_updated.jpg)
2. 部分升级回退到“Body”版本

   再次进入 FOTA 服务，在升级服务 URL 里填入“http://192.168.100.102/body”，重复上述步骤，可将版本回退到“Body”版本。

   ![](https://ingchips.github.io/blog/img/fota_back_to_body.jpg)
3. 切换到附属 FOTA 程序

   再次进入 FOTA 服务，点击“Activate Secondary FOTA”按钮重启开发板并进入 FOTA 附属 App。

   ![](https://ingchips.github.io/blog/img/fota_activate_sec_fota.jpg)

   重新扫描，可发现名为“ING Secondary FOTA”的设备：

   ![](https://ingchips.github.io/blog/img/fota_sec_fota_run.jpg)
4. 完整升级

   连接到名为“ING Secondary FOTA”的设备，进入 FOTA 服务，在升级服务 URL 里填入上述任何一个 URL，重复上述步骤， 同样可以进行升级。

   ![](https://ingchips.github.io/blog/img/fota_sec_full_update.jpg)

   出于演示目的，辅助 FOTA 程序故意上报了错误的 platform 版本号，故升级过程会同时升级 platform 和 App Bin， 需要的时间明显多于部分升级。

## 演示 2：使用 Web 版工具 {#演示-2使用-web-版工具}

[Web 版 FOTA 工具](https://ingchips.github.io/web_apps/ing918_ota/index_cn.html) 支持本地、在线两种升级模式。在使用这个工具之前， 请确认浏览器的[兼容性](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API#browser_compatibility)。 部分浏览器需要启用 Web Platform 特性（about://flags/#enable-experimental-web-platform-features）方可使用该工具。

通过“选择”按钮选择名为“ING Thermometer”的蓝牙设备，连接成功后可看到查看当前版本。

![](https://ingchips.github.io/blog/img/web_fota_select.png)

1. 本地升级模式

   将升级包里的 toe/v2.zip 文件拖入“本地文件”界面（或者通过点击“选择一个文件”选择 toe/v2.zip），出现版本升级提示信息， 点击“更新”即可。

   ![](https://ingchips.github.io/blog/img/web_fota_main.png)
2. 在线升级模式

   进入“在线”页面，填入“https://192.168.100.102/body”，重复上述步骤，可将版本回退到“Body”版本。

其它操作与手机 App 类似，不再赘述。
