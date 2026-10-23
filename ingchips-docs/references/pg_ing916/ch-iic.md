<!-- pg_ing916: 8 I2C总线 -->

# 8 I2C总线 {#ch-iic}

I2C(Inter－Integrated Circuit)是一种通用的总线协议。 它是一种只需要两个IO并且支持多主多从的双向两线制总线协议标准。

## 8.1 功能概述 {#功能概述-3}

- 两个I2C模块
- 支持Master/Slave模式
- 支持7bit/10bit地址
- 支持速率调整
- 支持DMA

## 8.2 使用说明 {#使用说明-3}

I2C Master有两种使用方式可以选择：

- 方法1：以[blocking](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_i2c_blocking)的方式操作I2C（读写操作完成后API才会返回），针对I2C Master读取外设的单一场景。
- 方法2：使用[I2C中断](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_i2c_interrupt)操作I2C，需要在中断中操作读写的数据。

I2C Slave 则需要使用方法2，以中断方式操作。

### 8.2.1 方法1（blocking） {#iic_i2c_blocking}

#### 8.2.1.1 IO 配置 {#iic_blk_io_config}

1. IO选择，并非所有IO都可以映射成I2C，请查看对应datasheet获取可用IO。
2. 操作模块之前需要打开对应模块的时钟。使用`SYSCTRL_ClearClkGateMulti()`打开时钟。请查看下述代码示例，需要注意的是：

   - `SYSCTRL_ITEM_APB_I2C0`对应I2C0，如果使用I2C1需要对应修改。
3. I2C IO需要配置为默认上拉，芯片内置上拉可以通过`PINCTRL_Pull()`实现（已经包含在`PINCTRL_SelI2cIn()`中）。实际应用中建议在外部实现上拉（可以获得更快的响应速度和时钟）。
4. 将选定IO映射到I2C模块，两个IO均需要配置为双向（输入+输出）。请参考下述代码实现（`PINCTRL_SelI2cIn()`中包含了输入+输出的配置）。

以下示例可以将指定IO映射成I2C引脚：

```c

#define I2C_SCL         GIO_GPIO_10
#define I2C_SDA         GIO_GPIO_11

void setup_peripherals_i2c_pin(void)
{
  SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ITEM_APB_I2C0)
                            | (1 << SYSCTRL_ITEM_APB_PinCtrl));
  PINCTRL_SelI2cIn(I2C_PORT_0,I2C_SCL,I2C_SDA);
}
```

#### 8.2.1.2 模块配置 {#模块配置}

- 参考：`\ING_SDK\sdk\src\BSP\iic.c`
- 包含API：

  ```c
  /**
   * @brief Init an I2C peripheral
   *
   * @param[in]port              I2C peripheral ID
   */
  void i2c_init(const i2c_port_t port);

  /**
   * @brief Write data to an I2C slave
   *
   * @param[in]port              I2C peripheral ID
   * @param[in]addr              address of the slave
   * @param[in]byte_data         data to be written
   * @param[in]length            data length
   * @return                      0 if success else non-0 (e.g. time out)
   */
  int i2c_write(const i2c_port_t port, uint8_t addr, const uint8_t *byte_data,
  int16_t length);

  /**
   * @brief Read data from an I2C slave
   *
   * @param[in]port              I2C peripheral ID
   * @param[in]addr              address of the slave
   * @param[in]write_data        data to be written before reading
   * @param[in]write_len         data length to be written before reading
   * @param[in]byte_data         data to be read
   * @param[in]length            data length to be read
   * @return                      0 if success else non-0 (e.g. time out)
   */
  int i2c_read(const i2c_port_t port, uint8_t addr, const uint8_t *write_data,
  int16_t write_len, uint8_t *byte_data, int16_t length);
  ```
- 使用方法：

  - [配置IO](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_blk_io_config)。
  - 初始化I2C模块：

  ```c
  i2c_init(I2C_PORT_0);
  ```

  - 写数据：

  ```c
  i2c_write(I2C_PORT_0, ADDRESS, write_data, DATA_CNT);
  ```

  当读操作完成后API才会返回，为了避免长时间等待ACK等意外情况，使用I2C_HW_TIME_OUT来控制blocking的时间。

  - 读数据：

  ```c
  i2c_read(I2C_PORT_0, ADDRESS, write_data, DATA_CNT, read_data, DATA_CNT);
  ```

  如果write_data不为空，则会首先执行写操作，然后再执行读操作。

### 8.2.2 方法2（Interrupt） {#iic_i2c_interrupt}

I2C Slave 以及 I2C Master方法2需要使用Interrupt方式。

#### 8.2.2.1 IO 配置 {#iic_int_io_config}

1. IO选择，并非所有IO都可以映射成I2C，请查看对应datasheet获取可用IO。
2. 操作模块之前需要打开对应模块的时钟。使用`SYSCTRL_ClearClkGateMulti()`打开时钟。请查看下述代码示例，需要注意的是：

   - `SYSCTRL_ITEM_APB_I2C0`对应I2C0，如果使用I2C1需要对应修改。
3. I2C IO需要配置为默认上拉，芯片内置上拉，可以通过`PINCTRL_Pull()`实现（已经包含在`PINCTRL_SelI2cIn()`中）。实际应用中建议在外部实现上拉（可以获得更快的响应速度和时钟）。
4. 将选定IO映射到I2C模块，两个IO均需要配置为双向（输入+输出）。请参考下述代码实现（`PINCTRL_SelI2cIn()`中包含了输入+输出的配置）。
5. 如果需要使用中断，使用`platform_set_irq_callback()`配置应用中断。

以下示例可以将指定IO映射成I2C引脚，并配置了中断回调函数：

```c
#define I2C_SCL         GIO_GPIO_10
#define I2C_SDA         GIO_GPIO_11

void setup_peripherals_i2c_pin(void)
{
  SYSCTRL_ClearClkGateMulti( (1 << SYSCTRL_ITEM_APB_I2C0)
                            | (1 << SYSCTRL_ITEM_APB_PinCtrl));

  PINCTRL_SelI2cIn(I2C_PORT_0,I2C_SCL,I2C_SDA);

  platform_set_irq_callback(PLATFORM_CB_IRQ_I2C0, peripherals_i2c_isr, NULL);

}
```

#### 8.2.2.2 模块初始化 {#模块初始化-1}

I2C模块初始化需要通过以下API来实现：

1. 通过`I2C_Config()`选择Master/Slave角色，以及I2C地址。
2. 使用`I2C_ConfigClkFrequency()`更改时钟配置。
3. 根据使用场景打开相应的中断`I2C_IntEnable()`：

   - I2C_INT_CMPL：该中断的触发代表传输结束。
   - I2C_INT_FIFO_FULL：代表RX FIFO中有数据。
   - I2C_INT_FIFO_EMPTY：TX FIFO空，需要填充发送数据。
   - I2C_INT_ADDR_HIT: 总线上检测到了匹配的地址。
4. 使能I2C模块`I2C_Enable()`。

#### 8.2.2.3 触发传输 {#触发传输}

1. 调用`I2C_CtrlUpdateDirection()`设置传输方向。

   - I2C_TRANSACTION_SLAVE2MASTER：Slave发送数据，Master读取数据。
   - I2C_TRANSACTION_MASTER2SLAVE：Master发送数据，Slave读取数据。
2. 通过`I2C_CtrlUpdateDataCnt()`设置该次传输的数据大小，最大8个bit（256字节），以字节为单位。
3. 使用`I2C_CommandWrite()`触发I2C传输：

   - I2C_COMMAND_ISSUE_DATA_TRANSACTION： Master有效，触发数据传输。
   - I2C_COMMAND_RESPOND_ACK：在接收到的字节后发送一个ACK。
   - I2C_COMMAND_RESPOND_NACK：在接收到的字节后发送一个NACK。
   - I2C_COMMAND_CLEAR_FIFO：清空FIFO。
   - I2C_COMMAND_RESET：reset I2C模块。

#### 8.2.2.4 中断配置 {#中断配置}

数据的读写需要在中断中进行。

1. 在中断触发后，通过`I2C_GetIntState()`来读取中断状态。不同状态需要参考`I2C_STATUS_xxx`定义。

   - I2C_STATUS_FIFO_FULL：读取数据，并通过`I2C_FifoEmpty()`判断FIFO状态。
   - I2C_STATUS_FIFO_EMPTY： 填充数据，并通过`I2C_FifoFull()`判断FIFO状态。
   - I2C_STATUS_CMPL：一次传输数据结束，判断FIFO中是否有剩余数据并读取。
   - I2C_STATUS_ADDRHIT：地址匹配，在该中断中通过`I2C_GetTransactionDir()`判断传输的方向。

     - I2C_TRANSACTION_MASTER2SLAVE：代表Master发送，Slave则需要读取数据。
     - I2C_TRANSACTION_SLAVE2MASTER：代表Slave需要发送，Master读取数据。
2. FIFO相关中断不需要清除标志，其余中断需要通过`I2C_ClearIntState()`来清除标志，避免中断重复触发。

#### 8.2.2.5 编程指南 {#编程指南-2}

##### 8.2.2.5.1 场景1：Master只读，Slave只写，不使用DMA {#场景1master只读slave只写不使用dma}

其中I2C配置为Master读操作，Slave收到地址后，将数据返回给Master，CPU操作读写，没有使用DMA。 配置之前需要决定使用的IO，请参考[IO 配置](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_int_io_config)。

###### 8.2.2.5.1.1 Master配置 {#master配置}

测试数据，每次传输10个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (10)
uint8_t read_data[DATA_CNT] = {0,};
uint8_t read_data_cnt = 0;
```

- 初始化I2C模块

  此处配置为Master, 7bit地址，并打开了传输结束中断和FIFO FULL中断。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_MASTER,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_ConfigClkFrequency(APB_I2C0,I2C_CLOCKFREQUENY_STANDARD);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_CMPL)|(1 << I2C_INT_FIFO_FULL));
  }
  ```
- Master中断实现

  中断中通过I2C_STATUS_FIFO_FULL来读取接收到的数据。当I2C_STATUS_CMPL触发时，当前传输结束，需要判断FIFO中有没有剩余数据。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_FIFO_FULL))
    {
      for(; read_data_cnt < DATA_CNT; read_data_cnt++)
      {
        if(I2C_FifoEmpty(APB_I2C0)){ break; }
        read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
      }
    }

    if(status & (1 << I2C_STATUS_CMPL))
    {
      for(; read_data_cnt < DATA_CNT; read_data_cnt++)
      {
        read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
      }
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
    }

    return 0;
  }
  ```
- Master触发传输

  首先需要设置传输方向，此处是I2C_TRANSACTION_SLAVE2MASTER，即代表Slave发送数据，Master读取数据。

  ```c
  void peripheral_i2c_send_data(void)
  {
    I2C_CtrlUpdateDirection(APB_I2C0,I2C_TRANSACTION_SLAVE2MASTER);
    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);
    I2C_CommandWrite(APB_I2C0, I2C_COMMAND_ISSUE_DATA_TRANSACTION);
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 在需要时候触发I2C读取，peripheral_i2c_send_data()。
  - 检查中断状态。

###### 8.2.2.5.1.2 Slave配置 {#slave配置}

测试数据，每次传输10个字节（fifo深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (10)
uint8_t write_data[DATA_CNT] = {0,};
uint8_t write_data_cnt = 0;
```

- 初始化I2C模块

  对于Slave，需要打开I2C_INT_ADDR_HIT，此中断的触发代表收到了匹配的地址。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_SLAVE,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_ADDR_HIT)|(1<<I2C_INT_CMPL));
  }
  ```
- Slave中断实现以及发送数据

  1. 首先需要等待I2C_STATUS_ADDRHIT中断，在该中断中通过`I2C_GetTransactionDir()`判断传输的方向。

     - I2C_TRANSACTION_MASTER2SLAVE：代表Slave需要读取数据，打开I2C_INT_FIFO_FULL中断。
     - I2C_TRANSACTION_SLAVE2MASTER：代表Slave需要发送，打开I2C_INT_FIFO_EMPTY。
  2. 如果是Slave写操作，则会触发I2C_STATUS_FIFO_EMPTY中断，此时填写需要发送的数据，直到FIFO满。
  3. 等待I2C_STATUS_CMPL中断，该中断的触发代表传输结束，在中断中关闭打开的FIFO中断。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    static uint8_t dir = 2;
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_ADDRHIT))
    {
      dir = I2C_GetTransactionDir(APB_I2C0);
      if(dir == I2C_TRANSACTION_MASTER2SLAVE)
      {
          I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
      }
      else if(dir == I2C_TRANSACTION_SLAVE2MASTER)
      {
          I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
      }

      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_ADDRHIT));
    }

    if(status & (1 << I2C_STATUS_FIFO_EMPTY))
    {
      for(; write_data_cnt < DATA_CNT; write_data_cnt++)
      {
        if(I2C_FifoFull(APB_I2C0)){ break; }
        I2C_DataWrite(APB_I2C0,write_data[write_data_cnt]);
      }
    }

    if(status & (1 << I2C_STATUS_CMPL))
    {

      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
      // prepare for next
      if(dir == I2C_TRANSACTION_MASTER2SLAVE)
      {
          I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
      }
      else if(dir == I2C_TRANSACTION_SLAVE2MASTER)
      {
          I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
      }

    }

    return 0;
  }
  ```
- 使用流程：

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 检查中断状态，在中断中发送数据，I2C_STATUS_CMPL中断代表传输结束。

##### 8.2.2.5.2 场景2：Master只写，Slave只读，不使用DMA {#场景2master只写slave只读不使用dma}

其中I2C配置为Master写操作，Slave收到地址后，将从Master读取数据，CPU操作读写，没有使用DMA。 配置之前需要决定使用的IO，请参考[IO 配置](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_int_io_config)。

###### 8.2.2.5.2.1 Master配置 {#master配置-1}

测试数据，每次传输10个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (10)
uint8_t write_data[DATA_CNT] = {0,};
uint8_t write_data_cnt = 0;
```

- 初始化I2C模块

  此处配置为Master, 7bit地址，并打开了传输结束中断和FIFO EMPTY中断。 I2C_INT_FIFO_EMPTY中断用来发送数据。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_MASTER,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_ConfigClkFrequency(APB_I2C0,I2C_CLOCKFREQUENY_STANDARD);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_CMPL)|(1 << I2C_INT_FIFO_EMPTY));
  }
  ```
- Master中断实现

  1. 中断中通过I2C_STATUS_FIFO_EMPTY来发送数据。每次填充FIFO直到FIFO为满，当填充完最后一个数据后，需要关掉I2C_INT_FIFO_EMPTY，否则中断会继续触发。
  2. 当I2C_STATUS_CMPL触发时，当前传输结束。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_CMPL))
    {
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
    }

    if(status & (1 << I2C_STATUS_FIFO_EMPTY))
    {
      // push data until fifo is full
      for(; write_data_cnt < DATA_CNT; write_data_cnt++)
      {
        if(I2C_FifoFull(APB_I2C0)){ break; }
        I2C_DataWrite(APB_I2C0,write_data[write_data_cnt]);
      }

      // if its the last, disable empty int
      if(write_data_cnt == DATA_CNT)
      {
        I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
      }

    }

    return 0;
  }
  ```
- Master触发传输

  首先需要设置传输方向，I2C_TRANSACTION_MASTER2SLAVE，即代表Master发送数据，Slave读取数据。 注意！！！中断发送数据完成后关闭了I2C_INT_FIFO_EMPTY（FIFO空）中断，如果需要开始新一次传输需要打开中断。 打开I2C_INT_FIFO_EMPTY：I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));

  ```c
  void peripheral_i2c_send_data(void)
  {
    I2C_CtrlUpdateDirection(APB_I2C0,I2C_TRANSACTION_MASTER2SLAVE);
    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);
    I2C_CommandWrite(APB_I2C0, I2C_COMMAND_ISSUE_DATA_TRANSACTION);
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 在需要时候发送I2C数据，peripheral_i2c_send_data()。
  - 检查中断状态。

###### 8.2.2.5.2.2 Slave配置 {#slave配置-1}

测试数据，每次传输10个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (10)
uint8_t read_data[DATA_CNT] = {0,};
uint8_t read_data_cnt = 0;
```

- 初始化I2C模块

  对于Slave，需要打开I2C_INT_ADDR_HIT，此中断的触发代表收到了匹配的地址。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_SLAVE,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_ADDR_HIT)|(1<<I2C_INT_CMPL));
  }
  ```
- Slave中断实现以及接收数据

  1. 首先需要等待I2C_STATUS_ADDRHIT中断，在该中断中通过`I2C_GetTransactionDir()`判断传输的方向。

     - I2C_TRANSACTION_MASTER2SLAVE：代表Slave需要读取数据，打开I2C_INT_FIFO_FULL中断。
     - I2C_TRANSACTION_SLAVE2MASTER：代表Slave需要发送，打开I2C_INT_FIFO_EMPTY。
  2. I2C_STATUS_FIFO_FULL的触发，代表FIFO中有接收到的数据，读取数据，直到FIFO变空。
  3. I2C_STATUS_CMPL代表传输结束，检查FIFO中有没有剩余数据，并且关掉FIFO中断避免再次触发。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    static uint8_t dir = 2;
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_ADDRHIT))
    {
      dir = I2C_GetTransactionDir(APB_I2C0);
      if(dir == I2C_TRANSACTION_MASTER2SLAVE)
      {
          I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
      }
      else if(dir == I2C_TRANSACTION_SLAVE2MASTER)
      {
          I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
      }

      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_ADDRHIT));
    }

    if(status & (1 << I2C_STATUS_FIFO_FULL))
    {
      for(; read_data_cnt < DATA_CNT; read_data_cnt++)
      {
        if(I2C_FifoEmpty(APB_I2C0)){ break; }
        read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
      }
    }

    if(status & (1 << I2C_STATUS_CMPL))
    {
      for(;read_data_cnt < DATA_CNT; read_data_cnt++)
      {
        read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
      }
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));

      // prepare for next
      if(dir == I2C_TRANSACTION_MASTER2SLAVE)
      {
          I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
      }
      else if(dir == I2C_TRANSACTION_SLAVE2MASTER)
      {
          I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
      }

    }

    return 0;
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 检查中断状态，I2C_STATUS_CMPL中断代表传输结束。

##### 8.2.2.5.3 场景3：Master只读，Slave只写，使用DMA {#场景3master只读slave只写使用dma}

其中I2C配置为Master读操作，Slave收到地址后，将数据返回给Master，DMA操作读写。 配置之前需要决定使用的IO，请参考[IO 配置](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_int_io_config)。

###### 8.2.2.5.3.1 Master配置 {#master配置-2}

测试数据，每次传输23个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (23)
uint8_t read_data[DATA_CNT] = {0,};
```

- 初始化I2C模块

  此处配置为Master, 7bit地址，并打开了传输结束中断，由于使用DMA传输，因此不需要打开FIFO相关中断。其余配置和场景1相同。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_MASTER,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_ConfigClkFrequency(APB_I2C0,I2C_CLOCKFREQUENY_STANDARD);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_CMPL));
  }
  ```
- 初始化DMA模块

  使用前需要配置DMA模块。

  ```c
  static void setup_peripherals_dma_module(void)
  {
      SYSCTRL_ClearClkGateMulti(1 << SYSCTRL_ClkGate_APB_DMA);
      DMA_Reset(1);
      DMA_Reset(0);
  }
  ```
- Master中断实现

  等待I2C_STATUS_CMPL中断的触发，该中断代表传输结束。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_CMPL))
    {
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
    }

    return 0;
  }
  ```
- Master DMA设置

  该API实现了I2C0 RXFIFO到DMA的配置，细节请参考DMA文档。

  ```c
  void peripherals_i2c_rxfifo_to_dma(int channel_id, void *dst, int size)
  {
    DMA_Descriptor descriptor __attribute__((aligned (8)));

    descriptor.Next = (DMA_Descriptor *)0;
    DMA_PreparePeripheral2Mem(&descriptor,dst,SYSCTRL_DMA_I2C0,
                              size,DMA_ADDRESS_INC,0);

    DMA_EnableChannel(channel_id, &descriptor);
  }
  ```
- Master触发传输

  1. 打开I2C模块的DMA功能。
  2. 设置传输方向I2C_TRANSACTION_SLAVE2MASTER，与场景1相同。
  3. 设置需要传输的数据大小。
  4. 配置DMA，并使用I2C_COMMAND_ISSUE_DATA_TRANSACTION触发I2C传输。

  ```c
  void peripheral_i2c_send_data(void)
  {
    I2C_DmaEnable(APB_I2C0,1);
    I2C_CtrlUpdateDirection(APB_I2C0,I2C_TRANSACTION_SLAVE2MASTER);
    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);

    #define I2C_DMA_RX_CHANNEL   (0)//DMA channel 0
    peripherals_i2c_rxfifo_to_dma(I2C_DMA_RX_CHANNEL, read_data,
                                  sizeof(read_data));

    I2C_CommandWrite(APB_I2C0, I2C_COMMAND_ISSUE_DATA_TRANSACTION);
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 初始化DMA，setup_peripherals_dma_module()。
  - 在需要时候触发I2C读取，peripheral_i2c_send_data()。
  - 检查中断状态。

###### 8.2.2.5.3.2 Slave配置 {#slave配置-2}

测试数据，每次传输23个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (23)
uint8_t write_data[DATA_CNT] = {0,};
```

- 初始化I2C模块

  对于Slave，需要打开I2C_INT_ADDR_HIT，此中断的触发代表收到了匹配的地址。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_SLAVE,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_ADDR_HIT)|(1<<I2C_INT_CMPL));
  }
  ```
- 初始化DMA模块

  使用前需要配置DMA模块。

  ```c
  static void setup_peripherals_dma_module(void)
  {
      SYSCTRL_ClearClkGateMulti(1 << SYSCTRL_ClkGate_APB_DMA);
      DMA_Reset(1);
      DMA_Reset(0);
  }
  ```
- Slave中断实现以及发送数据

  1. 首先需要等待I2C_STATUS_ADDRHIT中断，在该中断中通过`I2C_GetTransactionDir()`判断传输的方向。

     - I2C_TRANSACTION_SLAVE2MASTER：代表Slave需要发送，设置DMA发送数据。
  2. I2C_STATUS_CMPL代表传输结束，关闭I2C DMA功能。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    static uint8_t dir = 2;
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_ADDRHIT))
    {
      dir = I2C_GetTransactionDir(APB_I2C0);
      if(dir == I2C_TRANSACTION_SLAVE2MASTER)
      {
        peripherals_i2c_write_data_dma_setup();
      }
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_ADDRHIT));
    }

    if(status & (1 << I2C_STATUS_CMPL))
    {
      I2C_DmaEnable(APB_I2C0,0);
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
    }

    return 0;
  }
  ```
- Slave发送数据以及DMA设置

  该API实现了DMA传输数据到I2C0 FIFO的配置，细节请参考DMA文档。

  ```c
  void peripherals_i2c_dma_to_txfifo(int channel_id, void *src, int size)
  {
    DMA_Descriptor descriptor __attribute__((aligned (8)));

    descriptor.Next = (DMA_Descriptor *)0;
    DMA_PrepareMem2Peripheral(&descriptor,SYSCTRL_DMA_I2C0,
                              src,size,DMA_ADDRESS_INC,0);

    DMA_EnableChannel(channel_id, &descriptor);
  }
  ```

  设置DMA并打开I2C DMA功能。

  ```c
  void peripherals_i2c_write_data_dma_setup(void)
  {
    #define I2C_DMA_TX_CHANNEL   (0)//DMA channel 0
    peripherals_i2c_dma_to_txfifo(I2C_DMA_TX_CHANNEL, write_data,
                                  sizeof(write_data));

    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);
    I2C_DmaEnable(APB_I2C0,1);
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 初始化DMA，setup_peripherals_dma_module()。
  - 检查中断状态，在中断中设置DMA发送数据，I2C_STATUS_CMPL中断代表传输结束。

##### 8.2.2.5.4 场景4：Master只写，Slave只读，使用DMA {#场景4master只写slave只读使用dma}

其中I2C配置为Master写操作，Slave收到地址后，读取Master发送的数据，DMA操作读写。 配置之前需要决定使用的IO，请参考[IO 配置](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_int_io_config)。

###### 8.2.2.5.4.1 Master配置 {#master配置-3}

测试数据，每次传输23个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (23)
uint8_t write_data[DATA_CNT] = {0,};
```

- 初始化I2C模块

  请参考场景3中Master配置的`初始化I2C模块`。
- 初始化DMA模块

  请参考场景3中Master配置的`初始化DMA模块`。
- I2C中断实现

  请参考场景3中Master配置的`Master中断实现`。
- I2C Master DMA设置

  该API实现了DMA传输数据到I2C0 FIFO的配置，细节请参考DMA文档。

  ```c
  void peripherals_i2c_dma_to_txfifo(int channel_id, void *src, int size)
  {
      DMA_Descriptor descriptor __attribute__((aligned (8)));

      descriptor.Next = (DMA_Descriptor *)0;
      DMA_PrepareMem2Peripheral(&descriptor,SYSCTRL_DMA_I2C0,
                                src,size,DMA_ADDRESS_INC,0);

      DMA_EnableChannel(channel_id, &descriptor);
  }
  ```
- I2C Master触发传输

  1. 打开I2C DMA 功能。
  2. 设置传输方向为I2C_TRANSACTION_MASTER2SLAVE，和场景2相同。
  3. 配置DMA，并使用I2C_COMMAND_ISSUE_DATA_TRANSACTION触发I2C传输。

  ```c
  void peripheral_i2c_send_data(void)
  {
    I2C_DmaEnable(APB_I2C0,1);
    I2C_CtrlUpdateDirection(APB_I2C0,I2C_TRANSACTION_MASTER2SLAVE);
    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);

    #define I2C_DMA_TX_CHANNEL   (0)//DMA channel 0
    peripherals_i2c_dma_to_txfifo(I2C_DMA_TX_CHANNEL, write_data,
                                  sizeof(write_data));

    I2C_CommandWrite(APB_I2C0, I2C_COMMAND_ISSUE_DATA_TRANSACTION);

  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 初始化DMA，setup_peripherals_dma_module()。
  - 在需要时候触发I2C读取，peripheral_i2c_send_data()。
  - 检查中断状态。

###### 8.2.2.5.4.2 Slave配置 {#slave配置-3}

测试数据，每次传输23个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (23)
uint8_t read_data[DATA_CNT] = {0,};
```

- 初始化I2C模块

  请参考场景3中Slave配置的`初始化I2C模块`。
- 初始化DMA模块

  请参考场景3中Slave配置的`初始化DMA模块`。
- Slave中断实现以及接收数据

  1. 首先需要等待I2C_STATUS_ADDRHIT中断，在该中断中通过`I2C_GetTransactionDir()`判断传输的方向。

     - I2C_TRANSACTION_MASTER2SLAVE：代表Slave需要接收，设置DMA接收数据。
  2. I2C_STATUS_CMPL代表传输结束，关闭I2C DMA功能。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    static uint8_t dir = 2;
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_ADDRHIT))
    {
      dir = I2C_GetTransactionDir(APB_I2C0);
      if(dir == I2C_TRANSACTION_MASTER2SLAVE)
      {
        peripherals_i2c_read_data_dma_setup();
      }

      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_ADDRHIT));
    }

    if(status & (1 << I2C_STATUS_CMPL))
    {
      I2C_DmaEnable(APB_I2C0,0);
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
    }

    return 0;
  }
  ```
- Slave 发送数据以及DMA设置

  该API实现了I2C0 RXFIFO到DMA的配置，细节请参考DMA文档。

  ```c
  void peripherals_i2c_rxfifo_to_dma(int channel_id, void *dst, int size)
  {
      DMA_Descriptor descriptor __attribute__((aligned (8)));

      descriptor.Next = (DMA_Descriptor *)0;
      DMA_PreparePeripheral2Mem(&descriptor,dst,SYSCTRL_DMA_I2C0,
                                size,DMA_ADDRESS_INC,0);

      DMA_EnableChannel(channel_id, &descriptor);
  }
  ```

  设置DMA并打开I2C DMA功能。

  ```c
  void peripherals_i2c_read_data_dma_setup(void)
  {
    #define I2C_DMA_RX_CHANNEL   (0)//DMA channel 0
    peripherals_i2c_rxfifo_to_dma(I2C_DMA_RX_CHANNEL, read_data,
                                  sizeof(read_data));

    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);
    I2C_DmaEnable(APB_I2C0,1);
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 初始化DMA，setup_peripherals_dma_module()。
  - 检查中断状态，在中断中设置DMA读取数据，I2C_STATUS_CMPL中断代表传输结束。

##### 8.2.2.5.5 场景5：Master/Slave同时读写 {#场景5masterslave同时读写}

其中I2C操作为，首先执行写操作然后再执行读操作，CPU操作读写，没有使用DMA。 配置之前需要决定使用的IO，请参考[IO 配置](https://ingchips.github.io/drafts/pg_ing916/ch-iic.html#iic_int_io_config)。

###### 8.2.2.5.5.1 Master配置 {#master配置-4}

测试数据，每次传输8个字节（FIFO深度是8字节），每个传输单元必须是1字节。

```c
#define DATA_CNT (8)
uint8_t write_data[DATA_CNT] = {0,};
uint8_t write_data_cnt = 0;
uint8_t read_data[DATA_CNT] = {0,};
uint8_t read_data_cnt = 0;
```

- 初始化I2C模块

  1. 配置为Master, 7bit地址。
  2. 打开传输结束中断和ADDR_HIT中断。对于Master来说，如果有Slave响应了该地址，则会有I2C_INT_ADDR_HIT中断。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_MASTER,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_ConfigClkFrequency(APB_I2C0,I2C_CLOCKFREQUENY_STANDARD);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_CMPL)|(1<<I2C_INT_ADDR_HIT));

  }
  ```
- Master中断实现

  1. I2C_STATUS_ADDRHIT，代表Slave响应了Master发送的地址:

     - 如果Master执行写操作，需要打开I2C_INT_FIFO_EMPTY，用来发送数据。
     - 如果Master执行读操作，需要打开I2C_INT_FIFO_FULL，用来接收数据。
  2. 如果Master执行写操作，I2C_STATUS_FIFO_EMPTY中断会出现，此时需要填充待发送的数据。如果数据发送完成，需要关闭I2C_STATUS_FIFO_EMPTY中断，避免重复触发。
  3. 如果Master执行读操作，I2C_STATUS_FIFO_FULL中断会出现，此时需要读取数据。
  4. I2C_STATUS_CMPL，代表传输结束：

     - 如果Master执行写操作，代表写成功。
     - 如果Master执行读操作，需要读取FIFO中的剩余数据。

  ```c
  uint8_t master_write_flag = 0;
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_ADDRHIT))
    {
      if(master_write_flag)
      {
        I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
        I2C_IntEnable(APB_I2C0,(1<<I2C_INT_CMPL)|(1 << I2C_INT_FIFO_EMPTY));
      }
      else
      {
        I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
        I2C_IntEnable(APB_I2C0,(1<<I2C_INT_CMPL)|(1 << I2C_INT_FIFO_FULL));
      }
      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_ADDRHIT));
    }

    if(status & (1 << I2C_STATUS_FIFO_EMPTY))
    {
      if(master_write_flag)
      {
        // push data until fifo is full
        for(; write_data_cnt < DATA_CNT; write_data_cnt++)
        {
          if(I2C_FifoFull(APB_I2C0)){ break; }
          I2C_DataWrite(APB_I2C0,write_data[write_data_cnt]);
        }

        // if its the last, disable empty int
        if(write_data_cnt == DATA_CNT)
        {
          I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
        }

      }
    }

    if(status & (1 << I2C_STATUS_FIFO_FULL))
    {
      if(!master_write_flag)
      {
        for(; read_data_cnt < DATA_CNT; read_data_cnt++)
        {
          if(I2C_FifoEmpty(APB_I2C0)){ break; }
          read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
        }
      }
    }

    // 传输结束中断，代表DATA_CNT个字节接收或者发射完成
    if(status & (1 << I2C_STATUS_CMPL))
    {
      if(master_write_flag)
      {
        I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
      }
      else
      {
        for(; read_data_cnt < DATA_CNT; read_data_cnt++)
        {
          read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
        }

        I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));

        // prepare for next
      }
    }

    return 0;
  }
  ```
- Master写传输

  首先需要设置传输方向，I2C_TRANSACTION_MASTER2SLAVE，即代表Master发送数据，Slave读取数据。

  ```c
  void peripheral_i2c_write_data(void)
  {
    master_write_flag = 1;

    //write data use fifo empty Interrupt,so disable I2C_INT_FIFO_FULL,enable I2C_INT_FIFO_EMPTY.
    I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
    I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
    I2C_CtrlUpdateDirection(APB_I2C0,I2C_TRANSACTION_MASTER2SLAVE);
    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);
    I2C_CommandWrite(APB_I2C0, I2C_COMMAND_ISSUE_DATA_TRANSACTION);
  }
  ```
- Master读传输

  首先需要设置传输方向，此处是I2C_TRANSACTION_SLAVE2MASTER，即代表Slave发送数据，Master读取数据。

  ```c
  void peripheral_i2c_read_data(void)
  {
    master_write_flag = 0;

    //read data use fifo full Interrupt,so disable I2C_INT_FIFO_EMPTY,enable I2C_INT_FIFO_FULL.
    I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
    I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
    I2C_CtrlUpdateDirection(APB_I2C0,I2C_TRANSACTION_SLAVE2MASTER);
    I2C_CtrlUpdateDataCnt(APB_I2C0, DATA_CNT);
    I2C_CommandWrite(APB_I2C0, I2C_COMMAND_ISSUE_DATA_TRANSACTION);
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 在需要时候触发I2C写数据，peripheral_i2c_write_data()。
  - 当写结束后，可以触发I2C读取，peripheral_i2c_read_data()。
  - 检查中断状态。

###### 8.2.2.5.5.2 Slave配置 {#slave配置-4}

- 初始化I2C模块

  1. 配置为Slave, 7bit地址。
  2. 打开传输结束中断和ADDR_HIT中断。对于Slave来说，如果有匹配的地址，则会有I2C_INT_ADDR_HIT中断。

  ```c
  #define ADDRESS (0x71)
  void setup_peripherals_i2c_module(void)
  {
    I2C_Config(APB_I2C0,I2C_ROLE_SLAVE,I2C_ADDRESSING_MODE_07BIT,ADDRESS);
    I2C_Enable(APB_I2C0,1);
    I2C_IntEnable(APB_I2C0,(1<<I2C_INT_ADDR_HIT)|(1<<I2C_INT_CMPL));
  }
  ```
- Slave中断实现

  1. I2C_STATUS_ADDRHIT，在该中断中通过`I2C_GetTransactionDir()`判断传输的方向:

     - I2C_TRANSACTION_MASTER2SLAVE：代表Slave需要读取数据，打开I2C_INT_FIFO_FULL中断。
     - I2C_TRANSACTION_SLAVE2MASTER：代表Slave需要发送，打开I2C_INT_FIFO_EMPTY。
  2. 如果Slave需要发送，I2C_STATUS_FIFO_EMPTY中断会出现，此时需要填充待发送的数据。
  3. 如果Slave需要读取数据，I2C_STATUS_FIFO_FULL中断会出现，此时需要读取数据。
  4. I2C_STATUS_CMPL，代表传输结束：

     - 如果Slave执行写操作，代表写成功，关闭I2C_STATUS_FIFO_EMPTY中断。
     - 如果Slave执行读操作，需要读取FIFO中的剩余数据，关闭I2C_STATUS_FIFO_FULL中断。

  ```c
  static uint32_t peripherals_i2c_isr(void *user_data)
  {
    static uint8_t dir = 2;
    uint32_t status = I2C_GetIntState(APB_I2C0);

    if(status & (1 << I2C_STATUS_ADDRHIT))
    {
      dir = I2C_GetTransactionDir(APB_I2C0);
      if(dir == I2C_TRANSACTION_MASTER2SLAVE)
      {
          master_write_flag = 1;
          I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
      }
      else if(dir == I2C_TRANSACTION_SLAVE2MASTER)
      {
          master_write_flag = 0;
          I2C_IntEnable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
      }

      I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_ADDRHIT));

    }

    if(status & (1 << I2C_STATUS_FIFO_EMPTY))
    {
      // master read
      if(!master_write_flag)
      {
        // push data until fifo is full
        for(; write_data_cnt < DATA_CNT; write_data_cnt++)
        {
          if(I2C_FifoFull(APB_I2C0)){break;}
          I2C_DataWrite(APB_I2C0,write_data[write_data_cnt]);
        }

      }
    }

    if(status & (1 << I2C_STATUS_FIFO_FULL))
    {
      // master write
      if(master_write_flag)
      {
        for(; read_data_cnt < DATA_CNT; read_data_cnt++)
        {
          if(I2C_FifoEmpty(APB_I2C0)){break;}
          read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
        }
      }
    }

    if(status & (1 << I2C_STATUS_CMPL))
    {
      if(master_write_flag)
      {
        for(;read_data_cnt < DATA_CNT; read_data_cnt++)
        {
          read_data[read_data_cnt] = I2C_DataRead(APB_I2C0);
        }

        I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
      }
      else
      {
        I2C_ClearIntState(APB_I2C0, (1 << I2C_STATUS_CMPL));
      }

      if(dir == I2C_TRANSACTION_MASTER2SLAVE)
      {
          I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_FULL));
      }
      else if(dir == I2C_TRANSACTION_SLAVE2MASTER)
      {
          I2C_IntDisable(APB_I2C0,(1 << I2C_INT_FIFO_EMPTY));
      }

    }

    return 0;
  }
  ```
- 使用流程

  - 设置IO，setup_peripherals_i2c_pin()。
  - 初始化I2C，setup_peripherals_i2c_module()。
  - 检查中断状态，在中断中发送数据，I2C_STATUS_CMPL中断代表传输结束。
  - 如果是读操作，slave应该在master_write_flag=0之后准备好数据写到FIFO。

### 8.2.3 时钟配置 {#时钟配置-1}

I2C时钟配置使用API：

```c
/**
 * @brief Set clk frequency for controller.
 * @param[in]I2C_BASE              base address
 * @param[in]option                see I2C_ClockFrequenyOptions
 */
void I2C_ConfigClkFrequency(I2C_TypeDef *I2C_BASE, I2C_ClockFrequenyOptions option);
```

其中option中定义了几个可选项（I2C时钟和系统时钟有关系，以下枚举可能需要根据实际时钟调整）:

```c
typedef enum
{
    I2C_CLOCKFREQUENY_NULL,
    I2C_CLOCKFREQUENY_STANDARD,//up to 100kbit/s
    I2C_CLOCKFREQUENY_FASTMODE,//up to 400kbit/s
    I2C_CLOCKFREQUENY_FASTMODE_PLUS,//up to 1Mbit/s
    I2C_CLOCKFREQUENY_MANUAL
} I2C_ClockFrequenyOptions;
```

如果选择MANUAL,需要手动配置相关寄存器来生成需要的时钟:

- `I2C_BASE->TPM` : 乘数因子, 位宽5bit, 所有`I2C_BASE->Setup`中的时间参数都会被乘以（TPM+1）。
- `I2C_BASE->Setup`: 使用`I2C_ConfigSCLTiming()`配置该寄存器，参数如下：

  - `scl_hi`：高电平持续时间，位宽 9bit，默认 0x10。
  - `scl_ratio`: 低电平持续时间因子，位宽 1bit，默认 1。
  - `hddat`：SCL拉低后SDA的保持时间，位宽 5bit，默认 5。
  - `sp`: 可以被过滤的脉冲毛刺宽度，位宽 3bit，默认 1。
  - `sudat`: 释放SCL之前的数据建立时间，位宽 5bit，默认 5。

  每个参数和时钟的计算关系如下：

  - 高电平持续时间计算：

    SCL high period = (2\times pclk)+(2+sp+sclhi)\times pclk\times(TPM+1)
     其中pclk为I2C模块的系统时钟，默认为24M，实际时钟可以从`SYSCTRL_GetClk()`获取。

    如果sp = 1, pclk = 42ns, TPM = 3, sclhi = 150 ，则：

    SCL high period = (2\times42)+(2+1+150)\times42\times(3+1) = 25788ns
  - 低电平持续时间计算：

    SCL low period = (2\times pclk)+(2+sp+sclhi\times (sclratio+1))\times pclk\times (TPM+1)

    如果sp = 1, pclk = 42ns, TPM = 3, sclhi = 150, sclratio = 0，则：

    SCL low period = (2\times42)+(2+1+150\times1)\times42\times(3 + 1) = 25788ns
  - 毛刺抑制宽度： spike suppression width = sp\times pclk\times (TPM+1)

    如果sp = 1, pclk = 42ns, TPM = 3，则：

    spike suppression width = 1\times42\times(3+1) = 168ns
  - SCL之前的数据建立时间：

    setup time = (2\times pclk)+(2+sp+sudat)\times pclk\times (TPM+1)

    如果sp = 1, pclk = 42ns, TPM = 3, sudat = 5，则：

    setup time = (2\times42)+(2+1+5)\times42\times(3+1) = 1428ns

    协议对SCL之前的数据建立时间要求为：

    ```
    -   standard mode: 最小250ns。
    -   fast mode: 最小100ns。 
    -   fast mode plus: 最小50ns。
    ```
  - SCL拉低后SDA的保持时间：

    hold time = (2\times pclk)+(2+sp+hddat)\times pclk\times (TPM+1)

    如果sp = 1, pclk = 42ns, TPM = 3, hddat = 5，则:

    hold time = (2\times 42)+(2+1+5)\times 42\times(3+1) = 1428ns

    协议对SCL拉低后SDA的保持时间要求为：

    ```
    -   standard mode: 最小300ns。
    -   fast mode: 最小300ns。 
    -   fast mode plus: 最小0ns。
    ```