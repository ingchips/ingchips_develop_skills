<!-- pg_ing916: 24 内置 Flash（EFlash） -->

# 24 内置 Flash（EFlash） {#ch-eflash}

## 24.1 功能概述 {#功能概述-13}

芯片内置一定容量的 Flash，可编程擦写。擦除时以扇区（sector）为单位进行，每个扇区大小为 `EFLASH_SECTOR_SIZE` 字节；写入时以 32bit 为单位。

内置 Flash 的电源由单独的 LDO 提供，相关配置请参考[内置 Flash 电压](https://ingchips.github.io/drafts/pg_ing916/ch-sysctrl.html#ch-sysctrl-flash-power)。 不同的芯片系列使用不同的电压供电时，所能支持的最高时钟频率也不相同，见表 [24.1](https://ingchips.github.io/drafts/pg_ing916/ch-eflash.html#tab:ch-eflash-tab-flash-freq-ldo)。 注意实际频率不可超过最高频率。

*表 24.1: 部分芯片系列 Flash 电压与最高时钟频率*
| 芯片系列 | 电压范围（V） | 最高时钟频率（MHz） |
| --- | --- | --- |
| ING9168XX | 最低 \sim 2.500 | 170 |
| ING9168XX | 2.600 \sim 3.100 | 192 |

表中的 Flash 时钟频率可通过 `SYSCTRL_GetFlashClk()` 读取。Flash 内部会对这个时钟 2 分频， 实际工作频率是这个时钟频率的一半。

关于内置 Flash LDO 输出电压的配置建议：

1. 当 V_{BAT} 固定，且 V_{BAT} \geq 2.8V 时，可以按照芯片数据手册给出的 Flash 颗粒的要求配置 Flash LDO 输出电压为 2.1V 或 2.6V；

   当输出电压配置为 2.6V 时，可将 Flash 时钟频率配置为 192 M Hz 以获得最佳性能。
2. 当 V_{BAT} 固定，且 2.3V \leq V_{BAT} < 2.8V 时，配置 Flash LDO 输出电压为 2.1V；
3. 当 V_{BAT} 固定，且 V_{BAT} < 2.3V 时，仍可以配置 Flash LDO 输出电压为 2.1V， 这时当 V_{BAT} < 2.1V 时，Flash LDO输出电压与 V_{BAT} 一致，可保证 Flash 仍有供电；
4. 当 V_{BAT} 不固定，如 V_{BAT} 来自电池输出时，推荐配置 Flash LDO 输出电压为 2.1V。

## 24.2 使用说明 {#使用说明-14}

### 24.2.1 擦除并写入新数据 {#擦除并写入新数据}

通过 `program_flash` 擦除并写入一段数据。

```c
int program_flash(
    // 待写入的地址
    const uint32_t dest_addr,
    // 数据源的地址
    const uint8_t *buffer,
    // 数据长度（以字节为单位，必须是 4 的倍数）
    uint32_t size);
```

`dest_addr` 为统一编址后的地址，而非 Flash 内部从 0 开始的地址。`dest_addr` 必须对应于某个扇区的起始地址。数据源不可位于 Flash 内。

`program_flash` 将根据 `size` 自动擦除一个或多个扇区并写入数据。

本函数如果成功，则返回 0，否则返回非 0。

### 24.2.2 不擦除直接写入数据 {#不擦除直接写入数据}

通过 `write_flash` 不擦除直接写入数据。

```c
int write_flash(
    // 待写入的地址
    const uint32_t dest_addr,
    // 数据源的地址
    const uint8_t *buffer,
    // 数据长度（以字节为单位，必须是 4 的倍数）
    uint32_t size);
```

`dest_addr` 为统一编址后的地址，必须 32bit 对齐。`write_data` 不擦除 Flash，而是直接写入。 数据源不可位于 Flash 内。如果对应的 Flash 空间未被擦除，将无法写入。

本函数如果成功，则返回 0，否则返回非 0。

### 24.2.3 单独擦除 {#单独擦除}

通过 `erase_flash_sector` 擦除一个指定的扇区。

```c
int erase_flash_sector(
    // 待擦除的地址
    const uint32_t addr);
```

`addr` 必须对应于某个扇区的起始地址。本函数如果成功，则返回 0，否则返回非 0。

### 24.2.4 Flash 数据升级 {#flash-数据升级}

通过 `flash_do_update` 可以升级 Flash 里的数据。这个函数可用于 FOTA 升级。

```c
int flash_do_update(
    // 数据块数目
    const int block_num,
    // 每个数据块的信息
    const fota_update_block_t *blocks,
    // 用于缓存一个扇区的内存
    uint8_t *ram_buffer);
```

每个数据块的定为为：

```c
typedef struct fota_update_block
{
    uint32_t src;
    uint32_t dest;
    uint32_t size;
} fota_update_block_t;
```

这个函数的行为大致如下：

```c
flash_do_update() {
    for (block in blocks) {
        flash_copy(block.dest,
                   block.src,
                   block.size);
    }
}
```

如前所述，`program_flash` 的数据源不能位于 Flash，所以 `flash_copy` 需要把各扇区逐个读入 `ram_buffer`，然后使用 `program_flash` 擦除、写入。

这个函数如果成功，将自动重启系统，否则返回非 0。