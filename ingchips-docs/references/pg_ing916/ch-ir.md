<!-- pg_ing916: 10 红外(IR) -->

# 10 红外(IR) {#ch-ir}

## 10.1 功能概述 {#功能概述-4}

- 支持红外发射&接收
- 时序可调整，支持多种编码

## 10.2 使用说明 {#使用说明-4}

### 10.2.1 IO 配置 {#io-配置}

红外的发射和接收分别需要一个IO，并非所有IO都可以映射成红外，请查看对应的datasheet获取可用的IO。

1. 使用`SYSCTRL_ClearClkGateMulti`打开对应时钟，红外时钟为`SYSCTRL_ClkGate_APB_IR`。
2. 红外输入（接收）需要使用`PINCTRL_SelIrIn`来配置IO。
3. 红外输出（发射）需要使用`PINCTRL_SetPadMux`来配置IO，使用方式请参考下述示例。
4. 使用`platform_set_irq_callback`配置红外中断。

以下示例可以将指定IO配置成红外，并打开红外时钟和中断：

```c
#define IR_DOUT GIO_GPIO_10
#define IR_DIN  GIO_GPIO_11

void setup_peripherals_ir_module(void)
{
    SYSCTRL_ClearClkGateMulti(  (1 << SYSCTRL_ClkGate_APB_IR)
                                | (1 << SYSCTRL_ClkGate_APB_PinCtrl));

    PINCTRL_SelIrIn(IR_DIN);
    PINCTRL_SetPadMux(IR_DOUT,IO_SOURCE_IR_DATA_OUT);
    platform_set_irq_callback(PLATFORM_CB_IRQ_IR_INT, IRQHandler_IR_INT, NULL);
}
```

### 10.2.2 参数(不同编码的时间参数) {#参数不同编码的时间参数}

红外模块支持NEC,RC5，不同编码方式需要提供对应序列中时间参数，具体如下：

- timer1：

  - 发送模式下，表示引导码低电平时间：如NEC为9ms。
  - 接收模式下与timer2组成检测引导码低电平窗口。
- timer2：

  - 发送模式下，表示重复码低电平时间：如NEC为2.25ms。
  - 接收模式下与timer1组成检测引导码低窗口。
- timer3：

  - 发送模式下，表示引导码高电平时间：如NEC为4.5ms。
  - 接收模式下与timer4组成检测引导码高电平+低电平窗口。
- timer4：

  - 发送模式下，表示重复码高电平时间：如NEC为560us。
  - 接收模式下与timer3组成检测引导码高电平+低电平窗口。
- timer5：

  - 接收时接收超时定时器，发射不必关注。
- btimer1：

  - 逻辑 0 的bit时长：如NEC为1.12ms。
- btimer2：

  - 逻辑 1 的bit时长：如NEC为2.25ms。
- bit_cycle：

  - 发射模式下：bit调制周期最小单位，如NEC为560us。
  - 接收模式下为bit检测超时时间。
- carry_low：

  - 载波低电平时长，与carry_high组合形成占空比可调的载波波形，如NEC为38KHz ，30%占空比载波则carry_low = (2/3)/times载波周期，carry_high = (1/3)/times载波周期。
- carry_high：

  - 载波高电平时长，与carry_low组合形成占空比可调的载波波形。

结构体如下：

```c
typedef struct
{
    uint16_t timer1;
    uint16_t timer2;
    uint16_t timer3;
    uint16_t timer4;
    uint16_t timer5;
    uint16_t btimer1;
    uint16_t btimer2;
    uint16_t bit_cycle;
    uint16_t carry_low;
    uint16_t carry_high;
}Ir_mode_param_t;
```

不同参数需要根据内部时钟来计算：

1. 载波参数根据OSC_CLK_FREQ得到：

   NEC的载波频率为38KHz，RC5为36KHz，对应的载波参数为：

   ```c
   #define NEC_WAVE_FREQ 38000 
   #define RC5_WAVE_FREQ 36000

   #define IR_WAVE_NEC_FREQ (OSC_CLK_FREQ/NEC_WAVE_FREQ)
   #define IR_WAVE_TC9012_FREQ (OSC_CLK_FREQ/NEC_WAVE_FREQ)    
   #define IR_WAVE_RC5_FREQ (OSC_CLK_FREQ/RC5_WAVE_FREQ)
   ```
2. Bit时长参数根据32K时钟计数得到：

   以NEC为例，其逻辑”0”为562.5µs的有效脉冲加562.5µs的空闲间隔，总时长为1.125ms。而逻辑”1”为562.5µs的有效脉冲加1.6875ms的空闲间隔，总时长为2.25ms。 因此NEC的逻辑0或者1的计数单位约为560µs，以32K计数可以得到对应参数为:32000x560/1000000。

   ```c
   #define BASE_CLK    32000

   #define NEC_UINT    (BASE_CLK*560/1000000+1)
   #define TC9012_UINT (BASE_CLK*560/1000000+1)
   #define RC5_UINT    (BASE_CLK*889/1000000+1)
   ```

根据以上参数可以得到不同编码下的所有时间参数：

```c

typedef struct{
    Ir_mode_param_t param_tx;
    Ir_mode_param_t param_rx;
}Ir_type_param_t;

const static Ir_type_param_t t_ir_type_param_table[] = 
{
    {//NEC param
        {//TX
            16*NEC_UINT-1,4*NEC_UINT-1,8*NEC_UINT-1,1*NEC_UINT-1,0,
            2*NEC_UINT-1, 4*NEC_UINT-1,1*NEC_UINT-1,
            IR_WAVE_NEC_FREQ*2/3,IR_WAVE_NEC_FREQ*1/3},
        {//RX
            14*NEC_UINT-1,18*NEC_UINT-1,22*NEC_UINT-1,26*NEC_UINT-1,0xfff,
            0,2*NEC_UINT-1,0x7f,0,0},
    },
    {//TC9012 param
        {//TX
            8*TC9012_UINT-1,8*TC9012_UINT-1,8*TC9012_UINT-1,2*TC9012_UINT-1,0xfff,
            2*TC9012_UINT-1,4*TC9012_UINT-1,1*TC9012_UINT-1,
            IR_WAVE_TC9012_FREQ*2/3,IR_WAVE_TC9012_FREQ*1/3},
        { //RX
            7*TC9012_UINT-1,9*TC9012_UINT-1,15*TC9012_UINT-1,17*TC9012_UINT-1,0xfff,
            INESSENTIAL,2*TC9012_UINT-1,0x7f,INESSENTIAL,INESSENTIAL},
    },    
    {//RC5 param
        {//TX
            2*RC5_UINT-1,2*RC5_UINT-1,0,0,0,2*RC5_UINT-1,
            0,1*RC5_UINT,IR_WAVE_RC5_FREQ*2/3,IR_WAVE_RC5_FREQ*1/3},

        {//RX
            1*RC5_UINT-2,1*RC5_UINT,3*RC5_UINT-1,5*RC5_UINT-1,0,1*RC5_UINT-3,
            1*RC5_UINT-1,2*RC5_UINT-1,0,0},    
    }
};
```

### 10.2.3 红外发射接收 {#红外发射接收}

#### 10.2.3.1 接收初始化 {#接收初始化}

接收功能的初始化需要配置：

- 编码方式`mode`。
- 配置为接收模式`IR_TXRX_MODE_RX_MODE`。
- 配置接收模式对应的时间参数`Ir_mode_param_t`。
- 通过`IR_CtrlEnable`使能红外模块。

```c
void setup_peripherals_ir_module_rx(IR_IrMode_e mode, 
                                    const Ir_mode_param_t* param_p)
{
    IR_CtrlSetIrMode(APB_IR,mode == IR_IR_MODE_IR_9012 ? 0 : mode);
    IR_CtrlSetTxRxMode(APB_IR,IR_TXRX_MODE_RX_MODE);
    IR_CtrlSetIrIntEn(APB_IR);

    IR_CtrlSetIrEndDetectEn(APB_IR);
    IR_CtrlIrUsercodeVerify(APB_IR);
    IR_CtrlIrDatacodeVerify(APB_IR);
    IR_TimeSetIrTime1(APB_IR,param_p->timer1);
    IR_TimeSetIrTime2(APB_IR,param_p->timer2);
    IR_TimeSetIrTime3(APB_IR,param_p->timer3);
    IR_TimeSetIrTime4(APB_IR,param_p->timer4); 
    IR_TimeSetIrTime5(APB_IR,param_p->timer5); 
    IR_CtrlIrSetBitTime1(APB_IR,param_p->btimer1);
    IR_CtrlIrSetBitTime2(APB_IR,param_p->btimer2);
    IR_CtrlIrSetIrBitCycle(APB_IR,param_p->bit_cycle);

    IR_CtrlEnable(APB_IR);
}
```

#### 10.2.3.2 发射初始化 {#发射初始化}

发射功能的初始化需要配置：

- 编码方式`mode`。
- 配置为发射模式`IR_TXRX_MODE_TX_MODE`。
- 配置发射模式对应的时间参数`Ir_mode_param_t`。
- 通过`IR_CtrlEnable`使能红外模块。

```c
void setup_peripherals_ir_module_tx(IR_IrMode_e mode, 
                                    const Ir_mode_param_t* param_p)
{
    IR_CtrlSetIrMode(APB_IR,mode == IR_IR_MODE_IR_9012 ? 0 : mode);
    IR_CtrlSetTxRxMode(APB_IR,IR_TXRX_MODE_TX_MODE);
    IR_CtrlSetIrIntEn(APB_IR);

    IR_TxConfigIrTxPol(APB_IR);
    IR_TxConfigCarrierCntClr(APB_IR);
    IR_TxConfigIrIntEn(APB_IR);
    IR_CarryConfigSetIrCarryLow(APB_IR,param_p->carry_low);
    IR_CarryConfigSetIrCarryHigh(APB_IR,param_p->carry_high);
    IR_TimeSetIrTime1(APB_IR,param_p->timer1);
    IR_TimeSetIrTime2(APB_IR,param_p->timer2);
    IR_TimeSetIrTime3(APB_IR,param_p->timer3 );
    IR_TimeSetIrTime4(APB_IR,param_p->timer4); 
    IR_CtrlIrSetBitTime1(APB_IR,param_p->btimer1);
    IR_CtrlIrSetBitTime2(APB_IR,param_p->btimer2);
    IR_CtrlIrSetIrBitCycle(APB_IR,param_p->bit_cycle);

    IR_CtrlEnable(APB_IR);
}
```

#### 10.2.3.3 发射数据 {#发射数据}

1. 使用`IR_TxCodeSetIrTxUsercode`填充16bit地址。
2. 使用`IR_TxCodeSetIrTxDatacode`填充16bit数据。
3. 关闭重复码功能。
4. 发送数据`IR_TxConfigTxStart`。
5. 如果需要，可以通过`IR_FsmGetIrTransmitOk`等待直到发送完成，或者通过中断等待。

```c
void ir_transmit_fun(uint16_t addr,uint16_t data)
{
    IR_TxCodeSetIrTxUsercode(APB_IR,addr);
    IR_TxCodeSetIrTxDatacode(APB_IR,data);
    IR_CleanIrTxRepeatMode(APB_IR);
    IR_TxConfigTxStart(APB_IR);
}
```

如果需要发送重复码，则需要打开重复码功能`IR_CtrlIrTxRepeatMode`。

```c
void ir_transmit_repeat(void)
{
    IR_CtrlIrTxRepeatMode(APB_IR);   
    IR_TxConfigTxStart(APB_IR);
}
```

#### 10.2.3.4 中断实现(以及红外接收) {#中断实现以及红外接收}

中断触发后，通过状态寄存器判断对应的操作：

- `IR_FsmGetIrTransmitOk`代表发送成功。
- `IR_FsmGetIrTxRepeat`代表重复码发送成功。
- `IR_FsmGetIrReceivedOk`代表接收到了数据，通过以下API获取数据：

  - `IR_RxCodeGetIrRxUsercode`获取地址。
  - `IR_RxCodeGetIrRxDatacode`获取数据。
- 通过`IR_FsmClearIrInt`清除中断避免重复触发。

以下示例演示了从中断中接收数据：

```c
static uint32_t IRQHandler_IR_INT(void *user_data)
{
    if(IR_FsmGetIrReceivedOk(APB_IR))
    {
        uint32_t value = IR_RxCodeGetIrRxUsercode(APB_IR)<<16 |
                         IR_RxCodeGetIrRxDatacode(APB_IR);
    }

    IR_FsmClearIrInt(APB_IR);
    return 0;
}
```