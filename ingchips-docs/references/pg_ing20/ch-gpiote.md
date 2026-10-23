<!-- pg_ing20: 22 GPIOTE简介 （GPIO tasks and events） -->

# 22 GPIOTE简介 （GPIO tasks and events） {#ch-gpiote}

## 22.1 GPIOTE 功能描述 {#gpiote-功能描述}

GPIOTE（GGPIO tasks and events）模块提供了使用任务和事件访问GPIO引脚的功能。每个GPIOTE通道可以分配给一个引脚。 GPIOTE块使GPIO可以在PIN状态更改时生成事件，该事件可用于通过PTE系统执行任务。 GPIO也可以接收PTE系统事件改变IO状态。

GPIOTE系统可以理解为GPIO系统的扩展，GPIO模块无法直接和PTE系统交互，通过GPIOTE系统，可以和PTE系统进行交互，从而实现PTE监听GPIO的输入事件和控制GPIO的输出状态的功能。

### 22.1.1 模块特性 {#模块特性}

- 三个GPIO任务（SET CLR TOGGLE）可选。
- 三个GPIO任务可以在每个GPIOTE的通道上使用。
- 每个GPIOTE通道可以根据输入管脚的中断状态生成输入事件。
- 可以在每个GPIOTE通道中配置引脚的初始值输出电平（仅作为任务模式时，GPIO OUT生效）。
- 共有8个GPIOTE通道与PTE系统相连，每个通道可以配置为任务或事件模式。
- 每个GPIOTE通道可以配置一个IO映射。

### 22.1.2 连接特性 {#连接特性}

所有的GPIO都与GPIOTE块相连接，任意的IO都可作为GPIOTE模块的输入输出源，选取的8个GPIOTE通道可作为PTE模块的任务/事件访问通道。 GPIOTE模块作为连接PTE总线通道的外设，可由PTEC模块进行全局控制。

### 22.1.3 设计概述 {#设计概述}

GPIOTE 模块会接管GPIO模块的输入输出特性，通过GPIOTE模块，可以实现对GPIO的输入事件监听和输出状态控制。当GPIOTE模块接管GPIO模块后，GPIO模块的寄存器设置失效。无法控制对应IO的模式和电平状态。

当IO映射到GPIOTE通道：

- GIOTE通道模式设定为关闭时：GPIO的输入输出模式和外部电平状态取决于GPIO模块的内部设置。
- GIOTE通道模式设定为事件时：对应的GPIO设置为输入模式，GPIOTE模块会监听GPIO的输入状态，当状态变化时，GPIOTE模块会触发事件，并通知PTE系统。
- GIOTE通道模式设定为任务时：对应的GPIO设置为输出模式，GPIOTE模块会根据任务类型对GPIO进行输出控制。并且GPIO的默认输出状态取决于GPIOTE模块的配置。

## 22.2 使用方法 {#使用方法-7}

### 22.2.1 API概述 {#api概述}

GPIOTE模块属于GPIO的扩展，连接到PTE模块，因此API接口放置于peripheral_pte.c文件中。

初始化GPIOTE模块配置,配置对应的通道和设置的IO模式以及设置默认输出电平：

```c
void GPIOTE_Configuration(GPIOTE_Channel channel, GPIOTE_Mode mode, uint8_t pin, uint8_t out_level);
```

### 22.2.2 使用示例 {#使用示例-3}

GPIOTE模块需要配置PTE模块进行使用，对应示例可参考PTE模块的使用DEMO。