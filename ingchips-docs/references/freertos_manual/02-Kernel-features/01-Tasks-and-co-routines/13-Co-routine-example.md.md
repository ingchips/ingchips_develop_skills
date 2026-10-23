# FreeRTOS co-routines

[[More about co-routines...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### Quick Co-routine Example

This quick example demonstrates the use of co-routines.

1. **Creating a simple co-routine to flash an LED**

   The following code defines a very simple co-routine that does nothing but periodically flashes an LED.

   ```c
   void vFlashCoRoutine( CoRoutineHandle_t xHandle,
                         UBaseType_t uxIndex )
   {
       // Co-routines must start with a call to crSTART().
       crSTART( xHandle );

       for( ;; )
       {
           // Delay for a fixed period.
           crDELAY( xHandle, 10 );

           // Flash an LED.
           vParTestToggleLED( 0 );
       }

       // Co-routines must end with a call to crEND().
       crEND();
   }
   ```

   That's it!

2. **Scheduling the co-routine**

   Co-routines are scheduled by repeated calls to vCoRoutineSchedule(). The best place to do this is 
   from within the idle task by writing an idle task hook. First ensure that configUSE\_IDLE\_HOOK is 
   set to 1 within FreeRTOSConfig.h. Then write the idle task hook as:

   ```c
   void vApplicationIdleHook( void )
   {
       vCoRoutineSchedule( void );
   }
   ```

   Alternatively, if the idle task is not performing any other function it would be more efficient to 
   call vCoRoutineSchedule() from within a loop as:

   ```c
   void vApplicationIdleHook( void )
   {
       for( ;; )
       {
           vCoRoutineSchedule( void );
       }
   }
   ```

3. **Create the co-routine and start the RTOS scheduler**

   The co-routine can be created within main().

   ```c
   #include "task.h"
   #include "croutine.h"

   #define PRIORITY_0 0

   void main( void )
   {
       // In this case the index is not used and is passed 
       // in as 0.
       xCoRoutineCreate( vFlashCoRoutine, PRIORITY_0, 0 );

       // NOTE: Tasks can also be created here!

       // Start the RTOS scheduler.
       vTaskStartScheduler();
   }
   ```
   
4. **Extending the example: Using the index parameter**

   Now assume that we want to create 8 such co-routines from the same function. Each co-routine will 
   flash a different LED at a different rate. The index parameter can be used to distinguish between 
   the co-routines from within the co-routine function itself.
 
   This time we are going to create 8 co-routines and pass in a different index to each.

   ```c
   #include "task.h"
   #include "croutine.h"

   #define PRIORITY_0        0
   #define NUM_COROUTINES    8

   void main( void )
   {
       int i;

       for( i = 0; i < NUM_COROUTINES; i++ )
       {
           // This time i is passed in as the index.
           xCoRoutineCreate( vFlashCoRoutine, PRIORITY_0, i );
       }

       // NOTE: Tasks can also be created here!

       // Start the RTOS scheduler.
       vTaskStartScheduler();
   }
   ```

   The co-routine function is also extended so each uses a different LED and flash rate.

   ```c
   const int iFlashRates[ NUM_COROUTINES ] = { 10, 20, 30, 40, 50, 60, 70, 80 };
   const int iLEDToFlash[ NUM_COROUTINES ] = { 0, 1, 2, 3, 4, 5, 6, 7 }

   void vFlashCoRoutine( CoRoutineHandle_t xHandle, UBaseType_t uxIndex )
   {
       // Co-routines must start with a call to crSTART().
       crSTART( xHandle );

       for( ;; )
       {
           // Delay for a fixed period. uxIndex is used to index into
           // the iFlashRates. As each co-routine was created with
           // a different index value each will delay for a different
           // period.
           crDELAY( xHandle, iFlashRate[ uxIndex ] );

           // Flash an LED. Again uxIndex is used as an array index,
           // this time to locate the LED that should be toggled.
           vParTestToggleLED( iLEDToFlash[ uxIndex ] );
       }

       // Co-routines must end with a call to crEND().
       crEND();
   }
   ```
