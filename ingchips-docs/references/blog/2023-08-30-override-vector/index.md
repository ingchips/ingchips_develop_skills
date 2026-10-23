# 覆写中断向量表

某些特定场景下，需要自定义中断向量表，同时又维持 SDK 现有的功能，比如， 响应未开放的中断（如 SysTick）、精确统计中断处理的开销等等， 此时可以考虑覆写 platform 的中断向量表。

下面介绍具体的步骤。

## 1. 获取芯片的最大中断号 {#1-获取芯片的最大中断号}

找到 `platform_irq_callback_type_t` 里的最末一个中断名称，通过 `platform_read_info` 转换为底层中断号（记为 N）。或者直接取一个足够大的值，如 N = 64。

## 2. 定义完整的中断向量表 {#2-定义完整的中断向量表}

打开初始化文件，修改 `__Vectors` 的定义：

```asm
__Vectors       DCD     0                 ; Top of Stack
        DCD     Reset_Handler             ; Reset Handler
        DCD     Override_Handler          ; NMI Handler
        DCD     Override_Handler          ; Hard Fault Handler
        DCD     Override_Handler          ; MPU Fault Handler
        DCD     Override_Handler          ; Bus Fault Handler
        DCD     Override_Handler          ; Usage Fault Handler
        DCD     0                         ; Reserved
        DCD     0                         ; Reserved
        DCD     0                         ; Reserved
        DCD     0                         ; Reserved
        DCD     Override_Handler          ; SVCall Handler
        DCD     Override_Handler          ; Debug Monitor Handler
        DCD     0                         ; Reserved
        DCD     Override_Handler          ; PendSV Handler
        DCD     Override_Handler          ; SysTick Handler

        ; 重复 N 次
        DCD Override_Handler
        ....
        DCD Override_Handler

__Vectors_End
```

## 3. 用汇编实现 Override_Handler {#3-用汇编实现-override_handler}

```asm
Override_Handler PROC
                IMPORT UserHandler

                ; int irq = SCB->ICSR & SCB_ICSR_VECTACTIVE_Msk;
                LDR     r0, =0xE000ED04
                LDR     r1, [r0]
                BFC     r1,#9,#23

                ; if (irq > 15) call UserHandler; else call default
                CMP     r1, #0x0F
                BGT     CALL_USER_ISR

                ; TODO: 响应 Exception

                ; 继续调用 platform 内的 Exception 处理函数
                ; f_irq_handler isr = (f_irq_handler)io_read(PLATFORM_NVIC_VECT + irq * 4);
                ; 以 ING916xx 为例，platform 内中断向量表起始位置为 0x02002000
                LDR     r0, =0x02002000
                LDR     r0, [r0, r1, LSL #2]
                BX      r0

CALL_USER_ISR
                MOV     r0, r1
                LDR     r1, =UserHandler
                BX      r1

				ENDP
```

其中 `PLATFORM_NVIC_VECT` 可通过 `platform_get_vector_table_address()` 获取。

## 4. 实现 UserHandler {#4-实现-userhandler}

```highlight
void UserHandler(int irq)
{
    typedef void (*f_irq_handler)(void);

    f_irq_handler isr = (f_irq_handler)io_read(PLATFORM_NVIC_VECT + irq * 4);

    // TODO: 实现所需功能

    // 继续调用 platform 内的 ISR
    isr();
}
```

## 4. 替换中断向量表 {#4-替换中断向量表}

在需要的位置（比如 `app_main`）里设置中断向量表：

```highlight
int app_main()
{
    extern uint32_t __Vectors;
    SCB->VTOR = (uint32_t)&__Vectors;

    //....
}
```
