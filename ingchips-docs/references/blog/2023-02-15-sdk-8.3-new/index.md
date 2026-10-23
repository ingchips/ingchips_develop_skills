# SDK 8.3：支持 ING916XX 量产版

- [Highlights:](https://ingchips.github.io/blog/2023-02-15-sdk-8.3-new/#highlights)

## Highlights: {#highlights}

**已知问题（局限性）:**

- 调试 ING916xx 时，复位方式不能选择 SYSRESETREQ，应该选择 VECTRESET（不同的调试器可能使用不同的名词，J-Link 里称为 Core）。

  - 复位整个 SoC 的临时措施：对于 JLink，将 [自定义脚本](https://github.com/ingchips/doc_release/releases/download/v1.0/JlinkSettings.JLinkScript)放到工程目录，并在进入调试模式后再次点击 IDE 里的 “复位” 按钮。
- ING916XX 省电模式仍在持续开发、改进中，QUERY_DEEP_SLEEP_ALLOWED 回调目前只可返回 0 或者 PLATFORM_ALLOW_DEEP_SLEEP。
- ING916XX Extension 软件包：`ll_raw_packet_set_bare_mode` 暂不支持指定频率。
