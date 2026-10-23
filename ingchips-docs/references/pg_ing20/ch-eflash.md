<!-- pg_ing20: 19 内置 Flash（EFlash） -->

# 19 内置 Flash（EFlash） {#ch-eflash}

**注意：** 20xx系列mcu对于flash的写入存在硬件限制，理论硬件支持单次最大写入32字节数据， 实际受限于硬件，单次写入不能超过32字节数据，sdk通过循环写入32字节或调用DMA模块通道0搬运 的方式实现单次写入256字节的数据。两种方式的影响如下。

- 循环写入： 每次最大写入32字节数据，每次写入32字节之后都要执行约1.2ms的等待时间，单次写入超32字节速度较慢。
- DMA写入：会占用硬件DMA的通道0，写入过程会修改DMA的通道配置，其他外设不能使用DMA通道0， 并且写入flash之前需要降低flash的时钟频率，否则可能出现写入失败只能写入16字节数据的情况。

## 19.1 功能概述 {#功能概述-10}

芯片内置一定容量的 Flash，可编程擦写。擦除时以扇区（sector）为单位进行，每个扇区大小为 `EFLASH_SECTOR_SIZE` 字节；写入时以 32bit 为单位。

20XX系列芯片FLAH在使用不同的工作电压时支持的最大工作频率不同。总结于表 [19.1](https://ingchips.github.io/drafts/pg_ing20/ch-eflash.html#tab:ch-eflash-freq)。

*表 19.1: FLASH 支持的最高工作频率（实际工作频率）*
| 电压(V) | 最大工作频率(MHz) |
| --- | --- |
| 1.65-2.7 | 40 |
| 2.7-3.6 | 104 |

20XX系列芯片FLASH擦写典型时间： | 行为 | 时间（ms） | |———:|————:| | page program | 1.2 | | sector erase | 2.8 | | block erase | 2.8 |

表中的 Flash 时钟频率可通过 `SYSCTRL_GetFlashClk()` 读取。Flash 内部会对这个时钟 2 分频， 实际工作频率是这个时钟频率的一半。

为了保证芯片工作的最大兼容性，芯片默认设置FLAH的工作频率为76.8MHz（实际工作频率约38.4MHz）， 当确认芯片的工作电压一定大于2.7V时候，可通过`SYSCTRL_SelectFlashClk()`手动调整flash的 工作频率，以获取更高的芯片性能.最高设置的工作频率208MHz（实际工作频率约104MHz）。

请用户注意FLASH的工作电压与最大工作频率的关系，避免频率不匹配造成芯片工作异常，程序出现异常跑飞等问题。

## 19.2 使用说明 {#使用说明-10}

### 19.2.1 擦除并写入新数据 {#擦除并写入新数据}

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

### 19.2.2 不擦除直接写入数据 {#不擦除直接写入数据}

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

### 19.2.3 单独擦除 {#单独擦除}

通过 `erase_flash_sector` 擦除一个指定的扇区。

```c
int erase_flash_sector(
    // 待擦除的地址
    const uint32_t addr);
```

`addr` 必须对应于某个扇区的起始地址。本函数如果成功，则返回 0，否则返回非 0。

### 19.2.4 Flash 数据升级 {#flash-数据升级}

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