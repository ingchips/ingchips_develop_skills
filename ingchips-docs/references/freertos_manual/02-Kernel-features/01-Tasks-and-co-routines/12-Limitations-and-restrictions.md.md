# FreeRTOS co-routines

[[More about co-routines...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### Limitations and Restrictions

The benefit of a co-routines lower RAM usage when compared to an equivalent task comes at the cost of 
some restrictions on how a co-routine can be used. Co-routines are more restrictive and complex to use 
than tasks.

* **Sharing a stack**   

  The stack of a co-routine is not maintained when a co-routine blocks. This means variables allocated 
  on the stack will most probably lose their values. To overcome this a variable that must maintain its 
  value across a blocking call must be declared as static. For example:

  ```c
  void vACoRoutineFunction( CoRoutineHandle_t xHandle,
                            UBaseType_t uxIndex )
  {
      static char c = 'a';

      // Co-routines must start with a call to crSTART().
      crSTART( xHandle );

      for( ;; )
      {
          // If we set c to equal 'b' here ...
          c = 'b';

          // ... then make a blocking call ...
          crDELAY( xHandle, 10 );

          // ... c will only be guaranteed to still 
          // equal 'b' here if it is declared static
          // (as it is here).
      }

      // Co-routines must end with a call to crEND().
      crEND();
  }
  ```

  Another consequence of sharing a stack is that calls to API functions that could cause the co-routine 
  to block can only be made from the co-routine function itself - *not* from within a function called by 
  the co-routine. For example:

  ```c
  void vACoRoutineFunction( CoRoutineHandle_t xHandle, UBaseType_t uxIndex )
  {
      // Co-routines must start with a call to crSTART().
      crSTART( xHandle );

      for( ;; )
      {
          // It is fine to make a blocking call here,
          crDELAY( xHandle, 10 );

          // but a blocking call cannot be made from within
          // vACalledFunction().
          vACalledFunction();
      }

      // Co-routines must end with a call to crEND().
      crEND();
  }

  void vACalledFunction( void )
  {
      // Cannot make a blocking call here!
  }
  ```

* **Use of switch statements**   

  The default co-routine implementation included in the FreeRTOS download does not permit a blocking 
  call to be made from within a switch statement. For example:

  ```c
  void vACoRoutineFunction( CoRoutineHandle_t xHandle, UBaseType_t uxIndex )
  {
      // Co-routines must start with a call to crSTART().
      crSTART( xHandle );

      for( ;; )
      {
          // It is fine to make a blocking call here,
          crDELAY( xHandle, 10 );

          switch( aVariable )
          {
              case 1 : // Cannot make a blocking call here!
                       break;
              default: // Or here!
          }
      }

      // Co-routines must end with a call to crEND().
      crEND();
  }
  ```
  
