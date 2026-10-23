# Apps

## Mobile Apps {#mobile-apps}

| Name | ![](https://ingchips.github.io/images/btn_appstore.png) | ![Android](https://ingchips.github.io/images/android.png) Android (Github) | ![Android](https://ingchips.github.io/images/android.png) Android (镜像) |
| --- | --- | --- | --- |
| ![](https://ingchips.github.io/images/app_icon_ing_ble_80.png) [ING BLE](https://github.com/ingchips/INGdemo/) Companion for examples contained in SDK | [AppStore](https://itunes.apple.com/cn/app/ing-ble/id1465051342) ![](https://ingchips.github.io/images/qr_ing_ble.png) | [Download](https://github.com/ingchips/INGdemo/releases/download/v1.7.9/com.ingchips.INGdemo_v1.7.9.apk) ![](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fgithub.com%2Fingchips%2FINGdemo%2Freleases%2Fdownload%2Fv1.7.9%2Fcom.ingchips.INGdemo_v1.7.9.apk) | [Download](https://mirror.ghproxy.com/https://github.com/ingchips/INGdemo/releases/download/v1.7.9/com.ingchips.INGdemo_v1.7.9.apk) ![](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fmirror.ghproxy.com%2Fhttps%3A%2F%2Fgithub.com%2Fingchips%2FINGdemo%2Freleases%2Fdownload%2Fv1.7.9%2Fcom.ingchips.INGdemo_v1.7.9.apk) |
| ![](https://ingchips.github.io/images/app_icon_ing_mesh_80.png) [ING Mesh](https://github.com/ingchips/INGMesh-iOS) BLE SIG Mesh | [AppStore](https://apps.apple.com/cn/app/ing-mesh/id1531712932) ![](https://ingchips.github.io/images/qr_ing_mesh.png) | Stay tuned | Stay tuned |
| ![](https://ingchips.github.io/docs/sdk/img/app_icon_ing_position.png) [ING Position](https://github.com/ingchips/ble_positioning/tree/main/app) Visualization of BLE 2D/3D Positioning | [AppStore](https://apps.apple.com/cn/app/ing-position/id1633924602) ![](https://ingchips.github.io/docs/sdk/img/qr_ing_position.png) | Stay tuned | Stay tuned |
| [ING Conn Test](https://github.com/ingchips/app-conntest-android) BLE Stress testing | Stay tuned | [Download](https://github.com/ingchips/app-conntest-android/releases/download/v0.2/conn_test.apk) ![](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fgithub.com%2Fingchips%2FINGdemo%2Freleases%2Fdownload%2Fv0.2%2Fconn_test.apk) | [Download](https://mirror.ghproxy.com/https://github.com/ingchips/app-conntest-android/releases/download/v0.2/conn_test.apk) ![](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fmirror.ghproxy.com%2Fhttps%3A%2F%2Fgithub.com%2Fingchips%2FINGdemo%2Freleases%2Fdownload%2Fv0.2%2Fconn_test.apk) |

## Mini Programs (小程序) {#mini-programs-小程序}

| ![](https://ingchips.github.io/docs/sdk/img/mini_prog_mesh.png) | 微信扫码 或 搜索“ING Mesh” |
| --- | --- |
| ![](https://ingchips.github.io/docs/sdk/img/mini_prog_mesh.png) | 微信扫码 或 搜索“ING Mesh” |
| ![](https://ingchips.github.io/docs/sdk/img/mini_prog_ble.png) | 微信扫码 或 搜索“ING BLE” |

## Web Apps {#web-apps}

### 1. Callgraph {#1-callgraph}

Web tool for static analysis of call graph & stack usage.

### 2. FOTA {#2-fota}

[中文版](https://ingchips.github.io/web_apps/ing918_ota/index_cn.html).

Web tool for Firmware Over-The-Air update. Web API requirements:

- Bluetooth LE

### 3. Online Power Profiler {#3-online-power-profiler}

Web tool for power consumption & battery life evaluation.

### 4. Trace Over-The-Air Logger {#4-trace-over-the-air-logger}

[中文版](https://ingchips.github.io/web_apps/air_trace/index_cn.html).

Web tool for logging the trace data over BLE. Web API requirements:

- Bluetooth LE

### 5. Stress Test {#5-stress-test}

Web tool for BLE connection stress test. Web API requirements:

- Bluetooth LE

**Note:** Some of above web apps require special Web API for accessing Bluetooth LE & Serial port. Check browser compatibility before using these apps. Recommended browsers: [Edge](https://www.microsoft.com/en-us/edge) ![Edge](https://ingchips.github.io/blog/img/logo_edge.png), [Chrome](https://www.google.cn/chrome/index.html) ![Chrome](https://ingchips.github.io/blog/img/logo_chrome.png).

- [Bluethooth LE](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API#browser_compatibility)

  Generally available in Chromium based browsers on desktop & Android. For some of these browsers, Web Platform feature (about://flags/#enable-experimental-web-platform-features) needs to be enabled.
- [Serial](https://web.dev/serial/)

  Generally available in Chromium based browsers on desktop. For some of these browsers, Web Platform feature (about://flags/#enable-experimental-web-platform-features) needs to be enabled.

## Source Code {#source-code}

We provide building blocks for apps (mobile, mini programs, web) to save time in the development phase.

The code base for all our apps is freely available on the [INGCHIPS repository](https://github.com/ingchips) at Github.

---

- [Download](https://ingchips.github.io/docs/sdk/download/)
- [Apps](https://ingchips.github.io/docs/sdk/apps/)
