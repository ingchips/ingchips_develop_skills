<!-- pg_ing918: 4 嵌入式闪存（Embedded Flash） -->

# 4 嵌入式闪存（Embedded Flash） {#ch-eflash}

闪存（eFlash）分为两个存储块，一个是主存储器块，另一个是信息块。主存储器块大小 512KB，主要用于存放可执行代码。信息块大小为 16KB，可用于存储设备信息。闪存支持页擦除，页擦除操作将擦除一页中的所有字节。

eFlash 特性：

- 0.81V~0.99V/1.62V~3.63V 双电源
- 内存结构 512KB+16KB
- 页面擦除能力：每页 8KB
- 耐久性：10000 次循环（min）
- 125 摄氏度时数据保留期超过 10 年
- 快速页面擦除/程序操作
- 页面擦除时间：20 毫秒（最长）

## 4.1 eFlash 写入数据 {#eflash-写入数据}

写入数据字节数（size）必须是四字节对齐的（二进制表示的低2位为0）。

注意写入数据不要越界（eFlash用户可操作的地址空间为0x4000~0x83FFF）。

### 4.1.1 eFlash 先擦除然后写入数据 {#eflash-先擦除然后写入数据}

```c
int program_flash(const uint32_t dest_addr, const uint8_t *buffer, uint32_t size);
```

eFlash 写入操作只能把1写成0，不能把0写成1，所以如果eFlash某地址之前保存过其他数据，想要写入数据需要把当前页擦除（当前页的所有字节都变为0xFF），再写入数据。

写入的目的地址（dest_addr）必须是页对齐的（地址落在每页的起始地址）。

### 4.1.2 eFlash 不擦除直接写入数据 {#eflash-不擦除直接写入数据}

```c
int write_flash(const uint32_t dest_addr, const uint8_t *buffer, uint32_t size);
```

如果可以确认eFlash写入的目标地址当前数据都是0xFF，可以不擦除直接写入数据。