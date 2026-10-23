<!-- pg_ing916: 6 一次性可编程存储器(eFuse) -->

# 6 一次性可编程存储器(eFuse) {#ch-efuse}

## 6.1 功能概述 {#功能概述-1}

eFuse是一种片内一次性可编程存储器，可以在断电后保持数据，并且编程后无法被再次修改。 ING916系列提供128bit eFuse，支持按bit编程或者按Word编程，bit的默认值是0，通过编程可以写成1。

## 6.2 使用说明 {#使用说明-1}

### 6.2.1 模块初始化 {#模块初始化}

```c
void setup_peripherals_efuse_module(void)
{
    // 打开clock，并且reset模块
    SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ITEM_APB_EFUSE));
    SYSCTRL_ResetBlock(SYSCTRL_ITEM_APB_EFUSE);
    SYSCTRL_ReleaseBlock(SYSCTRL_ITEM_APB_EFUSE);
}
```

### 6.2.2 按bit编程 {#按bit编程}

```c
void peripherals_efuse_write_bit(void)
{
    // 提供需要编程的bit位置,0到127之间
    EFUSE_UnLock(APB_EFUSE, EFUSE_UNLOCK_FLAG);
    //pos is bit position from 0 to 127
    EFUSE_WriteEfuseDataBitToOne(APB_EFUSE, pos);
    // 等待结束
    while(1 == EFUSE_GetStatusBusy(EFUSE_BASE));
    EFUSE_Lock(EFUSE_BASE);

    //写操作完成
    //如果要读取，需要reset模块
    SYSCTRL_ResetBlock(SYSCTRL_ITEM_APB_EFUSE);
    SYSCTRL_ReleaseBlock(SYSCTRL_ITEM_APB_EFUSE);

    //设置读取flag
    EFUSE_SetRdFlag(APB_EFUSE);
    //等待数据读取标志
    while(!EFUSE_GetDataValidFlag(APB_EFUSE));
    //通过EFUSE_GetEfuseData()读取数据
}
```

### 6.2.3 按word编程 {#按word编程}

```c
void peripherals_efuse_write_word(void)
{
    // 提供需要编程的word位置,0到3之间,每个word 32bit，一共128bit
    // EFUSE_PROGRAMWORDCNT_0代表word 0
    // data是要写入的32bit数据
    EFUSE_WriteEfuseDataWord(APB_EFUSE, EFUSE_PROGRAMWORDCNT_0, data);

    //写操作完成
    //如果要读取，需要reset模块
    SYSCTRL_ResetBlock(SYSCTRL_ITEM_APB_EFUSE);
    SYSCTRL_ReleaseBlock(SYSCTRL_ITEM_APB_EFUSE);

    //设置读取flag
    EFUSE_SetRdFlag(APB_EFUSE);
    //等待数据读取标志
    while(!EFUSE_GetDataValidFlag(APB_EFUSE));
    //通过EFUSE_GetEfuseData()读取数据
}
```

---