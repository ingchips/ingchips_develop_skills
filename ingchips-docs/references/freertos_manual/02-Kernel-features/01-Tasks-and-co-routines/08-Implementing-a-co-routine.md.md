# FreeRTOS co-routines

[[More about co-routines...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### Implementing a Co-Routine

A co-routine should have the following structure: 

```c
void vACoRoutineFunction( CoRoutineHandle_t xHandle,
                          UBaseType_t uxIndex )
{
    crSTART( xHandle );

    for( ;; )
    {
        -- Co-routine application code here. --
    }

    crEND();
}
```

The type crCOROUTINE\_CODE is defined as a function that returns void and takes an CoRoutineHandle\_t 
and an index as its parameters. All functions that implement a co-routine should be of this type (demonstrated 
above).

Co-routines are created by calling xCoRoutineCreate().

Points to note:

* All co-routine functions **must** start with a call to crSTART().
  
* All co-routine functions **must** end with a call to crEND().
  
* Co-routine functions should never return so are typically implemented as a continuous loop.
  
* Many co-routines can be created from a single co-routine function. The uxIndex parameter is provided 
  as a means of distinguishing between such co-routines.
