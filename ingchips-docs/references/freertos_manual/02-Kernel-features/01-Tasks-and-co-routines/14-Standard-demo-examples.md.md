# FreeRTOS co-routines

[[More about co-routines](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### FreeRTOS Demo Application Examples

Two files are included in the download that demonstrate using co-routines with queues:

1. **[crflash.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Common/Minimal/crflash.c)**

   This is functionally equivalent to the [standard demo](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) file flash.c but uses co-routines
   instead of tasks. In addition, and just for demonstration purposes, instead of directly toggling an
   LED from within a co-routine (as per the quick example above) the number of the LED that should be
   toggled is passed on a queue to a higher priority co-routine.

1. **[crhook.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Common/Minimal/crhook.c)**

   Demonstrates passing data from a interrupt to a co-routine. A tick hook function is used as the data
   source.

The [PC](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/Industrial-PC-Port) and one of the older [ARM Cortex-M3](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexkeil) demo applications are already
pre-configured to use these sample co-routine files and can be used as a reference. All the other demo
applications are configured to use tasks only, but can be easily converted to demonstrate co-routines by
following the procedure below. This replaces the functionality implemented within flash.c with that
implemented with crflash.c:

1. In FreeRTOSConfig.h set configUSE\_CO\_ROUTINES and configUSE\_IDLE\_HOOK to 1.

1. In the IDE project or project makefile (depending on the demo project being used):

   1. Replace the reference to file FreeRTOS/Demo/Common/Minimal/flash.c with FreeRTOS/Demo/Common/Minimal/crflash.c.

   2. Add the file FreeRTOS/Source/croutine.c to the build.

1. In main.c:

   1. Include the header file croutine.h which contains the co-routine macros and function prototypes.

   2. Replace the inclusion of flash.h with crflash.h.

   3. Remove the call to the function that creates the flash tasks vStartLEDFlashTasks() ....

   4. ... and replace it with the function that creates the flash co-routines vStartFlashCoRoutines( n ),
      where n is the number of co-routines that should be created. Each co-routine flashes a different
      LED at a different rate.

   5. Add an idle hook function that schedules the co-routines as:

      ```c
      void vApplicationIdleHook( void )
      {
          vCoRoutineSchedule( void );
      }
      ```
      If main() already contains an idle hook then simply add a call to vCoRoutineSchedule() to the existing
      hook function.

1. Replacing the flash tasks with the flash co-routines means there are at least two less stacks that
   need allocating and less heap space can therefore be set aside for use by the RTOS scheduler. If your
   project has insufficient RAM to include croutine.c in the build then simply reduce the definition of
   portTOTAL\_HEAP\_SPACE by ( 2 * portMINIMAL\_STACK\_SIZE ) within FreeRTOSConfig.h.
