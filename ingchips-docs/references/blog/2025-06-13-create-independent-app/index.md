# 创建独立于 platform 版本的应用

一般情况下，app 调用 platform API 时，直接使用 API 的函数地址，当 platform 升级时，API 地址改变，app 必须重新编译。 从 SDK v8.5.4 开始，开发者可以创建与 platform 版本独立的应用：允许单独升级 platform，app 不重新编译、不升级，可直接兼容新版 platform，功能正常。

**局限性:**

- 当 platform 大规模升级或者修改接口时，仍可能出现不兼容；
- 每次 API 调用都需要增加额外操作，功耗可能略有增加。

本文介绍这种 app 的创建和开发方法。

## 以 “Copy to My Project” 的方式新建项目 {#以-copy-to-my-project-的方式新建项目}

建议以 “Copy to My Project” 的方式新建项目。

## 使用脚本修改 platform.bin {#使用脚本修改-platformbin}

调用 [脚本](https://ingchips.github.io/files/mk_api_table.py) 修改 platform.bin。这个脚本在 platform.bin 的结尾追加 API 函数地址表， 并生成 API 代理入口。

导致 platform 与 app “不兼容”的原因主要有：

- API 被删除（一般不会发生）
- API 接口改变（一般不会发生）
- platform 体积变大，与 app 冲突（问题 1）
- platform 使用的内存变多，与 app 的内存重叠（问题 2）

对于问题 1，脚本允许开发者把 app 的烧录、启动地址后移，为将来 platform 变大预留空间； 对于问题 2，脚本允许开发者为 platform 预留一定量的内存空间：使后续版本使用的内存增加，只要不超过所预留的空间，兼容性仍能保持。

脚本在运行时会询问这两个问题，并按照开发者的要求相应修改。假设使用的软件包所在目录为 `/path/to/sdk/bundles/typical/ING9188xx`， 可如下运行脚本：

```highlight
python mk_api_table.py /path/to/sdk/bundles/typical/ING9188xx
```

脚本将为多种编译环境生成 `/path/to/sdk/bundles/typical/ING9188xx/_api_table.*` 汇编文件。

## 更新项目 {#更新项目}

打开项目，从项目中删除 `sysdes.*` 文件， 根据编译器类型选择合适的 `/path/to/sdk/bundles/typical/ING9188xx/_api_table.*` 汇编文件，加到项目。

后续的开发过程正常进行，不需要额外设置。

## 升级 SDK {#升级-sdk}

升级 SDK 后，重新运行脚本。脚本运行过程中会自动检查上述问题 1 和 2 相关的兼容性，如果无法兼容，会输出错误信息。

烧录新的 `platform.bin` 即完成升级。
