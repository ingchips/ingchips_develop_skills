# Download

| **Platform** | ![](https://ingchips.github.io/images/windows.png) Windows | ![](https://ingchips.github.io/images/linux.png) Linux | ![](https://ingchips.github.io/images/mac_os.png) mac OS |
| --- | --- | --- | --- |
| **Requirement** | 7 or newer 32 or 64bit | gtk 2.8 for gtk2 32 or 64bit | 10.12 or newer Carbon32 or 64bit |
| **Download** (Github) | [9.1.2](https://github.com/ingchips/ING918XX_SDK_SOURCE/releases/download/v9.1.2/ingchips_sdk_setup_v9.1.2.exe) | [5.6.4](https://github.com/ingchips/sdk/releases/download/v5.6.4/ingchips_sdk_linux_x86_v5.6.4.tar.gz) | [5.6.4](https://github.com/ingchips/sdk/releases/download/v5.6.4/ingchips_sdk_macos_x86_64_v5.6.4.tar.gz) |
| **Download** (镜像 1) | [9.1.2](https://ghproxy.net/https://github.com/ingchips/ING918XX_SDK_SOURCE/releases/download/v9.1.2/ingchips_sdk_setup_v9.1.2.exe) | [5.6.4](https://ghproxy.net/https://github.com/ingchips/sdk/releases/download/v5.6.4/ingchips_sdk_linux_x86_v5.6.4.tar.gz) | [5.6.4](https://ghproxy.net/https://github.com/ingchips/sdk/releases/download/v5.6.4/ingchips_sdk_macos_x86_64_v5.6.4.tar.gz) |
| **Download** (镜像 2) | [9.1.2](https://mirror.ghproxy.com/https://github.com/ingchips/ING918XX_SDK_SOURCE/releases/download/v9.1.2/ingchips_sdk_setup_v9.1.2.exe) | [5.6.4](https://mirror.ghproxy.com/https://github.com/ingchips/sdk/releases/download/v5.6.4/ingchips_sdk_linux_x86_v5.6.4.tar.gz) | [5.6.4](https://mirror.ghproxy.com/https://github.com/ingchips/sdk/releases/download/v5.6.4/ingchips_sdk_macos_x86_64_v5.6.4.tar.gz) |

**Note:** macOS SDK is a work-in-progress. Known Issues:

- Wizard can't open downloader from popup menu on projects. (Workaround: open downloader, then open flash_download.ini)
- Wizard can't open documents. (Workaround: documents are in "doc" folder)
- Wizard can't display created projects in "My Projects".
- Log window of downloader can't show colorful background.

### Compatibility {#compatibility}

SDK has been tested against following IDE/Toolchains:

| **IDE/Toolchains** | Status: OK | Not Supported |
| --- | --- | --- |
| [**Keil μVision**](https://www.keil.com) | ✅**v4.72.10.0** ❓**v5.21.1.0[1]** ✅**v5.28** **~** **v5.42** | ❌**v5.11.0.0** |
| [**IAR EB for ARM**](https://www.iar.com/iar-embedded-workbench/) | ✅**v8.32.3** ✅**v9.10.2****~****v9.50.1** | ❌**v7.8** |
| [**SEGGER Embedded Studio**](https://www.segger.com/products/development-tools/embedded-studio) | ✅**v4.5.0** ✅**v5.26** ✅**v8.10** |  |
| [**Rowlay CrossStudio for ARM**](https://www.crossworks.com/index.htm/) | ✅**v4.4** ✅**v4.8** ✅**v5.4** |  |
| [**GNU Arm Embedded Toolchain**](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm) | ✅**8-2018-q4-major** ✅**10-2020-q4-major** ✅**10.3-2021.10** ✅**12.3.rel1** ✅**15.2.rel1** |  |

**Note:**

1. SDK 6.7.0 or newer will use V6 compiler, and the support of V6 compiler in v5.21.1.0 is immature. **Workaround**: 1) for SDK examples, change to V5 compiler and add "--gnu" option; 2) for new projects, change default compiler to v5 in Options windows.

### Source Code {#source-code}

The code base for all our SDK examples and platform bundles for ING918 is freely available on the [INGCHIPS repository](https://github.com/ingchips/ING918XX_SDK_SOURCE) at Github.

Although with the SDK source code itself is enough for development, it’s highly recommended to download & install our SDK package, which includes not only source code, but also GUI tools and documentation.

Checkout the [tutorials](https://ingchips.github.io/user_guide/tutorial.html) in the [user guide](https://ingchips.github.io/user_guide/index.html) now to see how easy and seamless it is to develop BLE apps with our SDK.

---

- [Download](https://ingchips.github.io/docs/sdk/download/)
- [Apps](https://ingchips.github.io/docs/sdk/apps/)
