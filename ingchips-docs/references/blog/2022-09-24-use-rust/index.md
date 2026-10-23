# 使用 Rust 开发 BLE 应用

Rust 语言原本是 Mozilla 员工 Graydon Hoare 的私人计划，在 2010 年首次公开。Rust 1.0 是第一个稳定版本，于 2015 年 5 月 15 日发布。 Mozilla 2020 年 8 月裁员波及到 Rust 开发团队，一年后，AWS、华为、Google、微软、Mozilla 等五公司发起 Rust Foundation。

最近，在 Linux 内核维护者峰会上，[Linus Torvalds 表示](https://www.zdnet.com/article/linus-torvalds-rust-will-go-into-linux-6-1/)除非有意外发生，Rust 将进入 Linux 6.1； 微软 Azure CTO Mark Russinovich 在[推特上表示](https://new.qq.com/rain/a/20220922A04QBO00.html) “是时候停止用C/C++启动任何新项目了， 一切需要无垃圾回收语言的场景都该使用 Rust”。

对于嵌入式领域，Rust 官方一直着力[推广](https://www.rust-lang.org/what/embedded)，网络上资料、教程众多。本文与这些资料不同：不使用 Rust 的 Cargo 等 *时髦* 工具，坚持使用 `rustc`、`makefile` 这些 *老派* 工具 —— 与 C 共存而不是[从头重写](https://github.com/stm32-rs)，充分享受现有的 C 红利。

## 准备 Rust {#准备-rust}

以 Windows 为例。

1. [下载](https://www.rust-lang.org/learn/get-started)、安装 Rust
2. [下载](http://releases.llvm.org/download.html)、安装 LLVM

   假设 LLVM 的安装目录为 `D:\programs\LLVM`，那么新建一个环境变量 `LIBCLANG_PATH`，值为 `D:\programs\LLVM\bin`。
3. 安装 `bindgen`

   执行命令 `cargo install bindgen` 安装 `bindgen`。
4. 为 Rust 编译器添加编译目标

   关于 ARM Cortex-M 的几种编译目标如下：

   | 编译目标 | 说明 |  |
   | --- | --- | --- |
   | thumbv6m-none-eabi | Cortex-M0, Cortex-M0+ |  |
   | thumbv7m-none-eabi | Cortex-M3 | ING918xx |
   | thumbv7em-none-eabi | Cortex-M4, Cortex-M7 (无 FPU) |  |
   | thumbv7em-none-eabihf | Cortex-M4F, Cortex-M7F (有 FPU) | ING9168x |

   如果使用的是 ING918xx 开发板，则执行命令添加对应的编译目标：

   `rustup target add thumbv7m-none-eabi`

## 创建使用 Gnu 工具链项目 {#创建使用-gnu-工具链项目}

参照 SDK 教程，创建一个使用 Gnu 工具链的外设型项目，广播名称设置为 *Hello from Rust*。

## 生成 Rust Bindings {#生成-rust-bindings}

这一步的目的是为 SDK 的 C 头文件生成对应的 Rust FFI bindings。有了这个，Rust 源代码就可以调用 SDK 提供的所有功能，BLE、外设等等。

### ble_bindings.h {#ble_bindingsh}

同 [Zig 类似](https://ingchips.github.io/blog/2021-01-25-zig-async)，在 *src* 目录下创建文件 *ble_bindings.h*，把可能用到的头文件一并写进去：

```highlight
// ble_bindings.h 文件内容
#include "platform_api.h"
#include "ll_api.h"
#include "btstack_defines.h"
#include "btstack_event.h"
#include "gatt_client.h"
#include "sig_uuid.h"
#include "gap.h"
#include "att_db.h"
#include "btstack_util.h"
#include "FreeRTOS.h"
#include "task.h"
```

### ble_lib 模块 {#ble_lib-模块}

这一步将所有的 bindings 打包为 Rust 模块 *ble_lib* 。在 *src* 目录下创建 *ble_lib* 文件夹。 在 *ble_lib 文件夹里新建两个文件：_mod.rs* 和 *cty.rs*。

```highlight
// mod.rs 文件的内容
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

pub mod cty;

include!("ble_bindings.rs");
```

这里的 *ble_bindings.rs* 稍后通过 `bindgen` 工具从 *ble_bindings.h* 生成。

*cty.rs* 文件定义了 C 常见类型与 Rust 标准类型之间的映射，其完整内容见文末附录。

### 生成 ble_bindings.rs {#生成-ble_bindingsrs}

在 *makefile.conf* 添加 *ble_bindings.rs* 生成规则：

```highlight
src/ble_lib/$(RS_BINDINGS).rs: src/$(RS_BINDINGS).h
	$(info GEN BINDINGS)
	bindgen -o src/ble_lib/$(RS_BINDINGS).rs src/$(RS_BINDINGS).h --no-debug ".*" --no-default ".*" --rustified-enum ".*" --use-core --ctypes-prefix=cty -- $(ING_SRC_INC) $(ING_BUNDLE_INC) -D__SOFTFP__ -target armv7m-none-eabi
```

这里，`--no-debug` 用来禁止 `bindgen` 生成 Debug trait，因为 `bindgen` 只能 *尽力* 生成 Debug trait，不能保证 100%；`--no-default` 用来禁止 `bindgen` 生成 Default traits。`--use-core` 和 `--ctypes-prefix=cty` 配合，告诉 `bindgen` 转换时不要从 `std` 导入 C 类型。

`--` 后面的参数供 LLVM 使用，对于 ING918xx，需要添加参数 `-D__SOFTFP__ -target armv7m-none-eabi`。

## 替换 main.c {#替换-mainc}

我们的目标是用 Rust 重写 *main.c*。删掉这个文件，把 *Makefile* 的 PROJECT_FILES 里的 *main.c* 也删掉。

新建 *main.rs* 文件。最简单的 *main.c* 是这样的：

```highlight
// #include "xxx"
int app_main()
{
    platform_set_evt_callback(PLATFORM_CB_EVT_PROFILE_INIT, setup_profile, NULL);
    return 0;
}
```

与之对应的最简单的 *main.rs* 是这样的：

```highlight
#![no_std]
#![no_main]
#![deny(warnings)]
#![allow(dead_code, unused_imports)]

use core::panic::PanicInfo;

mod ble_lib;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}

extern "C" {
    pub fn setup_profile(data: * mut ble_lib::cty::c_void,
        user_data: * mut ble_lib::cty::c_void) -> u32;
}

#[no_mangle]
unsafe fn app_main() -> i32 {
    ble_lib::platform_set_evt_callback(
        ble_lib::platform_evt_callback_type_t::PLATFORM_CB_EVT_PROFILE_INIT,
        core::prelude::v1::Some(setup_profile),
        ble_lib::cty::null);
    0
}
```

## 更新 makefile {#更新-makefile}

添加 Rust 源代码及目标文件：

```highlight
RUST_FILES += src/main.rs
APP_O_FILES += $(addprefix $(OBJ_PATH)/,$(notdir $(RUST_FILES:.rs=.o)))
```

添加 Rust 编译规则：

```highlight
RC      := rustc

$(OBJ_PATH)/%.o: src/%.rs
	$(info RC $<)
	$(RC) --emit obj --target thumbv7em-none-eabi -o $@ $<
```

## 测试 {#测试}

`make`，回到 *Wizard*，从右键菜单打开 Flash Downder，下载到开发板。通过手机 App 可搜索到名为 *Hello from Rust* 的设备。

至此，Rust 语言开发已全线打通。

## 附录 {#附录}

### cty.rs 文件的内容 {#ctyrs-文件的内容}

```highlight
#![allow(non_camel_case_types)]
#![deny(warnings)]

pub type c_char = u8;

pub type c_int = i32;
pub type c_uint = u32;

mod pwd {}

pub type int8_t = i8;
pub type int16_t = i16;
pub type int32_t = i32;
pub type int64_t = i64;

pub type uint8_t = u8;
pub type uint16_t = u16;
pub type uint32_t = u32;
pub type uint64_t = u64;

pub type c_schar = i8;
pub type c_short = i16;
pub type c_longlong = i64;
pub type c_long = i32;

pub type c_uchar = u8;
pub type c_ushort = u16;
pub type c_ulonglong = u64;
pub type c_ulong = u32;

pub type c_float = f32;
pub type c_double = f64;

pub type intmax_t = i64;
pub type uintmax_t = u64;

pub type size_t = usize;
pub type ptrdiff_t = i32;
pub type intptr_t = isize;
pub type uintptr_t = u32;
pub type ssize_t = isize;

pub type c_void = core::ffi::c_void;

pub const null: * mut c_void = 0 as * mut c_void;
```
