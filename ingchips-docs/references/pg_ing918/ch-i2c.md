<!-- pg_ing918: 6 集成电路间总线（I2C） -->

# 6 集成电路间总线（I2C） {#ch-i2c}

## 6.1 功能概述 {#功能概述-1}

- 两个I2C模块
- 支持Master/Slave模式
- 支持7bit/10bit地址
- 支持DMA和QUEUE模式

## 6.2 I2C使用说明 {#i2c使用说明}

以下场景中均以I2C0为例，如果需要I2C1则可以根据情况修改

## 6.3 使用方法 {#使用方法}

### 6.3.1 Master读些，采用QUEUE模式 {#master读些采用queue模式}

```c
#define I2C_PORT        I2C_PORT_0
#define I2C_ADDR        0X76
```

#### 6.3.1.1 打开I2C时钟 {#打开i2c时钟}

```c
    SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ClkGate_APB_I2C0)
                              |(1 << SYSCTRL_ClkGate_APB_PinCtrl));
```

#### 6.3.1.2 配置I2C的IO口 {#配置i2c的io口}

```c
    PINCTRL_SetPadMux(10, IO_SOURCE_I2C0_SCL_O);
    PINCTRL_SetPadMux(11, IO_SOURCE_I2C0_SDO);
    PINCTRL_SelI2cSclIn(I2C_PORT, 10);
```

#### 6.3.1.3 I2C模块初始化 {#i2c模块初始化}

```c
I2C_CTRL0_CLR(I2C_BASE(I2C_PORT), I2C_CTRL0_SFTRST | I2C_CTRL0_CLKGATE);
```

#### 6.3.1.4 I2C写操作 {#i2c写操作}

```c
int i2c_do_write(const i2c_port_t port, const uint32_t nrm, uint8_t addr, const uint8_t *byte_data, int16_t length)
{
    uint32_t *p_data = (uint32_t *)(byte_data + 3);
    uint32_t data = (addr <<  1) | 0;     // control: write
    I2C_TypeDef *BASE = I2C_BASE(port);
    int timeout = I2C_HW_TIME_OUT;

    if (length > 0)
        data |= (byte_data[0] <<  8) | (byte_data[1] << 16) | (byte_data[2] << 24);

    I2C_CTRL0_CLR(BASE, I2C_CTRL0_SFTRST | I2C_CTRL0_CLKGATE);

    // ONLY SUPPORT PIO QUEUE MODE, SET HW_I2C_QUEUECTRL_PIO_QUEUE_MODE AT FRIST
    I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_PIO_QUEUE_MODE);

    // frist operation, do not need clear I2C_QUEUECTRL and I2C_QUEUECMD.
    BASE->I2C_QUEUECMD.NRM = nrm + 1 + length;

    I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_QUEUE_RUN);


    length += 1;
    while (1)
    {
        while_with_timeout(I2C_QUEUESTAT_WR_QUEUE_FULL(BASE));
        BASE->I2C_DATA = data;
        length -= 4;
        if (length <= 0)
            break;
        data = *p_data;
        p_data++;
    }

    // WAIT I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ (software polling)
    while_with_timeout(GET_I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ(BASE) == 0);
    I2C_CTRL1_CLR(BASE, I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ);

    // NOTE : MUST SET I2C_QUEUECTRL_WR_CLEAR
    I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_WR_CLEAR);
    I2C_QUEUECTRL_CLR(BASE, I2C_QUEUECTRL_WR_CLEAR);

    return 0;
}
```

#### 6.3.1.5 I2C读操作 {#i2c读操作}

```c
int i2c_read(const i2c_port_t port, uint8_t addr,
              const uint8_t *write_data, int16_t write_len,
              uint8_t *read_data, int16_t read_length)
{
    I2C_TypeDef *BASE = I2C_BASE(port);
    int timeout = I2C_HW_TIME_OUT;

    if (write_len)
    {
        // STEP 1: send write command
        int r = i2c_do_write(port, I2C_QUEUECMD_PRE_SEND_START | I2C_QUEUECMD_MASTER_MODE | I2C_QUEUECMD_DIRECTION,
                     addr, write_data, write_len);
        if (r != 0) return r;
    }
    else
    {
        I2C_CTRL0_CLR(BASE, I2C_CTRL0_SFTRST | I2C_CTRL0_CLKGATE);

        // ONLY SUPPORT PIO QUEUE MODE, SET HW_I2C_QUEUECTRL_PIO_QUEUE_MODE AT FRIST
        I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_PIO_QUEUE_MODE);
    }

    // STEP 2 : transmit (control byte + Read command), need hold SCL (I2C_QUEUECMD_RETAIN_CLOCK)
    BASE->I2C_QUEUECMD.NRM = (I2C_QUEUECMD_RETAIN_CLOCK | I2C_QUEUECMD_PRE_SEND_START | I2C_QUEUECMD_MASTER_MODE | I2C_QUEUECMD_DIRECTION |
          1);

    I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_QUEUE_RUN);

    BASE->I2C_DATA = 0xA5UL << 24 | 0x5A   << 16 |0xAA   <<  8 | (addr <<  1) | 1;

    while_with_timeout(GET_I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ(BASE) == 0);

    // CLEAR I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ
    I2C_CTRL1_CLR(BASE, I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ);

    // NOTE : MUST SET I2C_QUEUECTRL_WR_CLEAR
    I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_WR_CLEAR);
    I2C_QUEUECTRL_CLR(BASE, I2C_QUEUECTRL_WR_CLEAR);


    //
    // STEP 3 : read data byte + (NO ACK) + STOP
    //

    BASE->I2C_QUEUECMD.NRM = (I2C_QUEUECMD_SEND_NAK_ON_LAST | I2C_QUEUECMD_POST_SEND_STOP | I2C_QUEUECMD_MASTER_MODE |
         /*I2C_QUEUECMD_XFER_COUNT*/
         read_length);

    I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_QUEUE_RUN);

    // Receive DATA use I2C_QUEUEDATA;
    while (read_length > 0)
    {
        // check whether rdFIFO is empty
        while_with_timeout(I2C_QUEUESTAT_RD_QUEUE_EMPTY(BASE));

        int len = write_bytes(read_data, BASE->I2C_QUEUEDATA, read_length);
        read_data += len;
        read_length -= len;
    }

    // WAIT I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ (software polling)
    while_with_timeout(GET_I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ(BASE) == 0);

    // cLEAR I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ
    I2C_CTRL1_CLR(BASE, I2C_CTRL1_DATA_ENGINE_CMPLT_IRQ);

    // NOTE : CLEAR I2C_QUEUECTRL_RD_CLEAR
    I2C_QUEUECTRL_SET(BASE, I2C_QUEUECTRL_RD_CLEAR);
    I2C_QUEUECTRL_CLR(BASE, I2C_QUEUECTRL_RD_CLEAR);


    return 0;
}
```