# Source Organization

### Intro

Every RTOS port comes with a pre-configured demo application that already builds the necessary RTOS 
source files, and includes the necessary RTOS header files. It is highly recommended that the provided 
demos are used as a base for all new FreeRTOS based applications. This page is provided to assist in 
locating and understanding the provided projects.


### Basic directory structure

The FreeRTOS download includes source code for every processor port, and every demo application. Placing 
all the ports in a single download greatly simplifies distribution, but the number of files may seem 
daunting. The directory structure is however very simple, and the FreeRTOS real time kernel is 
contained ***in just 3 files*** (additional files are required 
if [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers),  [event group](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups) 
or co-routine functionality is required).

From the top, the download is split into two sub directories; FreeRTOS, and FreeRTOS-Plus. These are shown below:

```c
+-FreeRTOS-Plus    Contains [FreeRTOS-Plus](https://www.freertos.org/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction) components and demo projects.
|
+-FreeRTOS         Contains the FreeRTOS real time kernel source
                   files and demo projects
```

The FreeRTOS-Plus directory tree contains multiple readme files that describe its contents.


### FreeRTOS kernel directory structure

The core FreeRTOS kernel source files and demo projects are contained in two sub directories as shown below:

```c
FreeRTOS
    |
    +-Demo      Contains the demo application projects.
    |
    +-Source    Contains the real time kernel source code.
```

The core RTOS code is contained in three files, which are called tasks.c, queue.c and list.c. 
These three files are in the FreeRTOS/Source directory. The same directory contains two optional files 
called timers.c and croutine.c which implement software timer and co-routine functionality respectively.

Each supported processor architecture requires a small amount of architecture specific RTOS code. This 
is the RTOS portable layer, and it is located in the FreeRTOS/Source/Portable/[compiler]/[architecture] 
sub directories, where [compiler] and [architecture] are the compiler used to create the port, and the 
architecture on which the port runs, respectively.

For the reasons 
stated [on the memory management page](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management), 
the sample heap allocation schemes are also located in the portable layer. The various sample heap\_x.c 
files are located in the FreeRTOS/Source/portable/MemMang directory.

**Examples of portable layer directories:**

* If using the TriCore 1782 port with the GCC compiler:

  The TriCore specific file (port.c) is in the FreeRTOS/Source/Portable/GCC/TriCore\_1782 directory. 
  All the other FreeRTOS/Source/Portable sub directories, other than FreeRTOS/Source/Portable/MemMang, 
  can be ignored or deleted.

* If using the Renesas RX600 port with the IAR compiler:

  The RX600 specific file (port.c) is in the FreeRTOS/Source/Portable/IAR/RX600 directory. All the other 
  FreeRTOS/Source/Portable sub directories, other than FreeRTOS/Source/Portable/MemMang, can be ignored 
  or deleted.

* And so on for all the ports ...

The structure of the FreeRTOS/Source directory is shown below.

```c
FreeRTOS
    |
    +-Source        The core FreeRTOS kernel files
        |
        +-include   The core FreeRTOS kernel header files
        |
        +-Portable  Processor specific code.
            |
            +-Compiler x    All the ports supported for compiler x
            +-Compiler y    All the ports supported for compiler y
            +-MemMang       The sample heap implementations
```

The FreeRTOS download also contains a demo application for every processor architecture and compiler 
port. The majority of the demo application code is common to all ports and is contained in the 
FreeRTOS/Demo/Common/Minimal directory (the code located in the FreeRTOS/Demo/Common/Full directory 
is legacy, and only used by the PC port).

The remaining FreeRTOS/Demo sub directories contain pre-configured projects used to build individual 
demo applications. The directories are named to indicate the port to which they relate. Each RTOS port 
also [has its own web page](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) 
that details the directory in which the demo application for that port can be found.


**Examples of demo directories:**

* If building the TriCore GCC demo application that targets the Infineon TriBoard hardware:

  The TriCore demo application project file is located in the FreeRTOS/Demo/TriCore\_TC1782\_TriBoard\_GCC 
  directory. All the other sub directories contained in the FreeRTOS/Demo directory (other than the Common 
  directory) can be ignored or deleted.

* If building the Renesas RX6000 IAR demo application that targets the RX62N RDK hardware:

  The IAR workspace file is located in the FreeRTOS/Demo/RX600\_RX62N-RDK\_IAR directory. All the other 
  sub directories contained in the FreeRTOS/Demo directory (other than the Common directory) can be ignored 
  or deleted.

* And so on for all the ports ...

The structure of the FreeRTOS/Demo directory is shown below.

```c
FreeRTOS
    |
    +-Demo
        |
        +-Common    The demo application files that are used by all the demos.
        +-Dir x     The demo application build files for port x
        +-Dir y     The demo application build files for port y
```
---


### Creating your own application

**[Much more detail is provided on the [Creating a New FreeRTOS Application](https://www.freertos.org/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) page]**  

The pre-configured demo applications are supplied to ensure projects already exist with the correct 
RTOS kernel source files included, and the correct compiler options set, and therefore build with the 
minimum of user effort. It is therefore highly recommended that new applications are created by modifying 
an existing pre-configured demo application. This can be done by first building an existing demo application 
to ensure a clean build can be achieved, and then incrementally replacing the files included in the 
project from the FreeRTOS/Demo directory with your own application source files.
