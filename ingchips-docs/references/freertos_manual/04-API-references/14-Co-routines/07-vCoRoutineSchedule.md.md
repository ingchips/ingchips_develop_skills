[[Co-Routine Specific](https://www.freertos.org/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
void vCoRoutineSchedule( void );
```

Run a co-routine.

`vCoRoutineSchedule()` executes the highest priority co-routine that is able
to run. The co-routine will execute until it either blocks, yields or is
preempted by a task. Co-routines execute cooperatively so one
co-routine cannot be preempted by another, but can be preempted by a task.

If an application comprises of both tasks and co-routines then
`vCoRoutineSchedule` should be called from the idle task (in an idle task
hook).


**Example usage:**

```c
    void vApplicationIdleHook( void )
    {
        vCoRoutineSchedule( void );
    }
```

Alternatively, if the idle task is not performing any other function it would be more efficient to
call `vCoRoutineSchedule()` from within a loop as:

```c
    void vApplicationIdleHook( void )
    {
        for( ;; )
        {
            vCoRoutineSchedule( void );
        }
    }
```
