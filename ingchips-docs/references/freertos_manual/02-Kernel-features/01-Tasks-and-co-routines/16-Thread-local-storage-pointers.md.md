# Thread Local Storage Pointers

### Introduction

Thread local storage (or TLS) allows the application writer to store values inside a task's
control block, making the value specific to (local to) the task itself, and allowing
each task to have its own unique value.

Thread local storage is most often used to store values that a single
threaded program would otherwise store in a global variable. For example, many libraries include a global
variable called errno. If a library function returns an error condition to the calling
function, then the calling function can inspect the errno value to determine what
the error was. In a single threaded application it is sufficient to declare
errno as a global variable, but in a multi-threaded application each thread (task)
must have its own unique errno value - otherwise one task might read an errno
value that was intended for another task.


### Thread Local Storage Pointers

FreeRTOS provides the application writer with a flexible thread local storage
mechanism through the use of thread local storage pointers.

The [configNUM\_THREAD\_LOCAL\_STORAGE\_POINTERS](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
compile time configuration constant dimensions a per task array of void pointers (void*). 
The [vTaskSetThreadLocalStoragePointer()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/07-vTaskSetThreadLocalStoragePointer) API function is used to set
a value within the array of void pointers, and [pvTaskGetThreadLocalStoragePointer()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/08-pvTaskGetThreadLocalStoragePointer)
API function is used to read a value from the array of void pointers.


### Thread Local Integers

Values that have a size less than or equal to the size of a void pointer can
be stored directly within the thread local storage pointer array. For example,
if sizeof( void * ) is 4 then a 32-bit value can be stored in a void pointer
variable, using a simple cast to avoid compiler warnings. However, if
sizeof( void * ) is 2, then only a 16-bit value can be stored directly.


```c
uint32_t ulVariable;  

/* Write the 32-bit 0x12345678 value directly into index 1 of the thread   
   local storage array. Passing NULL as the task handle has the effect of writing   
   to the calling task's thread local storage array. */  
vTaskSetThreadLocalStoragePointer( NULL,  /* Task handle. */  
                                   1,     /* Index into the array. */  
                                   ( void * ) 0x12345678 );  

/* Store the value of the 32-bit variable ulVariable to index 0 of the calling  
   task's thread local storage array. */  
ulVariable = ERROR_CODE;  

vTaskSetThreadLocalStoragePointer( NULL,  /* Task handle. */  
                                   0,     /* Index into the array. */  
                                   ( void * ) ulVariable );  

/* Read the value stored in index 5 of the calling task's thread local storage  
   array into ulVariable. */  
ulVariable = ( uint32_t ) pvTaskGetThreadLocalStoragePointer( NULL, 5 );  
```
*Storing and retrieving 32-bit values directly from an index in the thread local storage array*


### Thread Local Structures

The previous example stored values directly into the thread local storage array. This next example demonstrates 
how to use a value in the array as a pointer to a structure that exists elsewhere in memory.

```c
typedef struct  
{  
    uint32_t ulValue1;  
    uint32_t ulValue2;  
} xExampleStruct;  

xExampleStruct *pxStruct;  

/* Create a structure for use by this task. */  
pxStruct = pvPortMalloc( sizeof( xExampleStruct ) );  

/* Set the structure members. */  
pxStruct->ulValue1 = 0;  
pxStruct->ulValue2 = 1;  

/* Store a pointer to the structure in index 0 of the calling task's thread   
   local storage array. */  
vTaskSetThreadLocalStoragePointer( NULL,  /* Task handle. */  
                                   0,     /* Index into the array. */  
                                   ( void * ) pxStruct );  

/* Locate the structure used by the calling task by reading its location from  
   index 0 of the calling task's thread local storage array. */  
pxStruct = ( xExampleStruct * ) pvTaskGetThreadLocalStoragePointer( NULL, 0 );  
```
*Storing a pointer to a structure in the calling task's thread local storage array*
