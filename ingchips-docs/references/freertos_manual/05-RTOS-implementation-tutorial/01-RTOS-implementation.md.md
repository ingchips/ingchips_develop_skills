### Introduction

This section describes part of the FreeRTOS implementation. 

These pages will be helpful if you:
 
* wish to modify the FreeRTOS source code.
* port the real time kernel to another microcontroller or prototyping board.
* are new to using an RTOS and wish to get more information on their operation and implementation.

The FreeRTOS real time kernel has been ported to a 
number of different microcontroller architectures. The Atmel AVR port was chosen for this example due to:

* the simplicity of the [AVR](http://www.microchip.com/wwwproducts/en/atmega32) architecture.
* the free availability of the utilized [WinAVR (GCC) development tools](http://winavr.sourceforge.net/).
* the low cost of the [STK500 prototyping board](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500)

The section concludes with a detailed step by step look at one complete context switch.

### Building Blocks

* [Development Tools](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/02-C-development-tools)
* [The RTOS Tick](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/03-The-RTOS-tick)
* [GCC Signal Attribute](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/05-GCC-signal-attribute)
* [GCC Naked Attribute](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/06-GCC-naked-attributes)
* [FreeRTOS Tick Code](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/07-FreeRTOS-tick-code)
* [The AVR Context](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/08-The-AVR-context)
* [Saving the Context](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/09-Saving-the-RTOS-task-context)
* [Restoring the Context](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/10-Restoring-the-context)


### Detailed Example

The final part of section 2 shows how these building blocks and source code modules are used to achieve a context switch on 
the AVR microcontroller. The example demonstrates in seven steps the process of switching from a lower priority task, called 
TaskA, to a higher priority task, called TaskB.

The source code is compatible with the WinAVR development tools. 

* [Putting It All Together](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/01-Putting-it-all-together)
* [Step 1](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/02-Step-1)
* [Step 2](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/03-Step-2)
* [Step 3](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/04-Step-3)
* [Step 4](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/05-Step-4)
* [Step 5](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/06-Step-5)
* [Step 6](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/07-Step-6)
* [Step 7](https://www.freertos.org/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/08-Step-7)
