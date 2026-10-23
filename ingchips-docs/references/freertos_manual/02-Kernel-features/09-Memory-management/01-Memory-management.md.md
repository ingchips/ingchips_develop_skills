# FreeRTOS heap memory management

[Also see the [Static Vs Dynamic Memory Allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page, which describes 
the pros and cons of allocating RTOS objects statically (without using the FreeRTOS heap) or dynamically,
the description of the [configAPPLICATION\_ALLOCATED\_HEAP](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
constant, which can be defined in FreeRTOSConfig.h, and 
the [reference project that demonstrates how to use FreeRTOS without a heap implementation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo).]
 
The RTOS kernel needs RAM each time a task, queue, mutex, software timer,
semaphore or event group is created. The RAM can be automatically dynamically
allocated from the RTOS heap within the RTOS API object creation functions, or it
can be [provided by the application writer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation).

If RTOS objects are created dynamically then the standard C library
malloc() and free() functions can sometimes be used for the purpose, but **...**

1. they are not always available on embedded systems,
2. they take up valuable code space,
3. they are not thread safe, and
4. they are not deterministic (the amount of time taken to execute the
   function will differ from call to call)

**...** so more often than not an alternative memory allocation implementation is required.

One embedded / real time system can have very different RAM and timing requirements to another - so a single 
RAM allocation algorithm will only ever be appropriate for a subset of applications.

To get around this problem, FreeRTOS keeps the memory allocation API in its
portable layer. The portable layer is outside of the source files that implement the core
RTOS functionality, allowing an application specific implementation appropriate for the
real time system being developed to be provided. When the RTOS kernel requires
RAM, instead of calling malloc(), it instead calls pvPortMalloc(). When RAM is
being freed, instead of calling free(), the RTOS kernel calls vPortFree().

FreeRTOS offers several heap management schemes that range in complexity and
features. It is also possible to provide your own heap implementation, and even
to use two heap implementations simultaneously. Using two heap implementations
simultaneously permits task stacks and other RTOS objects to be placed in fast
internal RAM, and application data to be placed in slower external RAM.


## Memory allocation implementations included in the RTOS source code download

The FreeRTOS download includes five sample memory allocation implementations, each of
which are described in the following subsections. The subsections also include
information on when each of the provided implementations might be the most appropriate
to select.

Each provided implementation is contained in a separate source file (heap\_1.c,
heap\_2.c, heap\_3.c, heap\_4.c and heap\_5.c respectively) which are located in the
Source/Portable/MemMang directory of the main RTOS source code download.
Other implementations can be added as needed. Exactly one of these source files
should be included in a project at a time [the heap defined by these portable
layer functions will be used by the RTOS kernel even if the application that is
using the RTOS opts to use its own heap implementation].

Following below:

* [heap\_1](#heap_1c) - the very simplest, does not permit memory to be freed.
* [heap\_2](#heap_2c) - permits memory to be freed, but does not coalescence adjacent free blocks.
* [heap\_3](#heap_3c) - simply wraps the standard malloc() and free() for thread safety.
* [heap\_4](#heap_4c) - coalescences adjacent free blocks to avoid fragmentation. Includes absolute address placement option.
* [heap\_5](#heap_5c) - as per heap\_4, with the ability to span the heap across multiple non-adjacent memory areas.


Notes:
* heap\_1 is less useful since FreeRTOS added [support for static allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation).
* heap\_2 is now considered legacy as the newer heap\_4 implementation is preferred.


---

### heap\_1.c

heap\_1 is less useful since FreeRTOS added [support for static allocation](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation).

heap\_1 is the simplest implementation of all. It does *not* permit memory to
be freed once it has been allocated. Despite this, heap\_1.c is appropriate
for a large number of embedded applications. This is because many small and
deeply embedded applications create all the tasks, queues, semaphores, etc. required
when the system boots, and then use all of these objects for the lifetime of
program (until the application is switched off again, or is rebooted). Nothing
ever gets deleted.

The implementation simply subdivides a single array into smaller blocks as RAM
is requested. The total size of the array (the total size of the heap) is set
by configTOTAL\_HEAP\_SIZE - which is defined in FreeRTOSConfig.h.
The [configAPPLICATION\_ALLOCATED\_HEAP](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
FreeRTOSConfig.h configuration constant is provided to allow the heap to be placed
at a specific address in memory.

The xPortGetFreeHeapSize() API function returns the total amount of heap space
that remains unallocated, allowing the configTOTAL\_HEAP\_SIZE setting to be
optimised.

The heap\_1 implementation:

* Can be used if your application never deletes a task, queue, semaphore, mutex, etc.
  (which actually covers the majority of applications in which FreeRTOS
  gets used).

* Is always deterministic (always takes the same amount of time to execute)
  and cannot result in memory fragmentation.

* Is very simple and allocated memory from a statically allocated array,
  meaning it is often suitable for use in applications that do not permit
  true dynamic memory allocation.

---

### heap\_2.c

heap\_2 is now considered legacy as heap\_4 is preferred.

heap\_2 uses a best fit algorithm and, unlike scheme 1, allows previously allocated blocks to be freed.
It does *not* combine adjacent free blocks into a single large block.
See heap\_4.c for an implementation that does coalescence free blocks.

The total amount of available heap space is set by configTOTAL\_HEAP\_SIZE - which is
defined in FreeRTOSConfig.h.
The [configAPPLICATION\_ALLOCATED\_HEAP](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
FreeRTOSConfig.h configuration constant is provided to allow the heap to be placed
at a specific address in memory.

The xPortGetFreeHeapSize() API function returns the total amount of heap space
that remains unallocated, (allowing the configTOTAL\_HEAP\_SIZE setting to be
optimised), but does not provided information on how the unallocated
memory is fragmented into smaller blocks.

The pvPortCalloc() function has the same signature as the standard library calloc function. It allocates 
memory for an array of objects and initializes all bytes in the allocated storage to zero. If allocation succeeds, 
it returns a pointer to the lowest byte in the allocated memory block. On failure, it returns a null pointer.

This implementation:

* Can be used even when the application repeatedly deletes tasks, queues,
  semaphores, mutexes, etc., with the caveat below regarding memory
  fragmentation.

* Should *not* be used if the memory being allocated and freed is of
  a random size. For example:
  
  + If an application dynamically creates and
    deletes tasks, and the size of the stack allocated to the tasks
    being created is always the same, then heap2.c can be used in most cases. However, if the
    size of the stack allocated to the tasks being created was
    not always the same, then the available free memory
    might become fragmented into many small blocks, eventually
    resulting in allocation failures. heap\_4.c would be a better
    choice in this case.
    
  + If an application dynamically creates and deletes queues, and
    the queue storage area is the same in each case (the queue
    storage area is the queue item size multiplied by the length
    of the queue), then heap\_2.c can be used in most cases. However,
    if the queue storage area were not the same in each case, then
    the available free memory
    might become fragmented into many small blocks, eventually
    resulting in allocation failures. heap\_4.c would be a better
    choice in this case.

   + The application called pvPortMalloc() and vPortFree() directly,
     rather than just indirectly through other FreeRTOS API functions.

* Could possible result in memory fragmentation problems if your application
  queues, tasks, semaphores, mutexes, etc. in an unpredictable order. This
  would be unlikely for nearly all applications but should be kept in mind.

* Is not deterministic - but is much more efficient that most standard C library malloc implementations.

heap\_2.c is suitable for many small real time systems that have to dynamically
create objects. See heap\_4 for a similar implementation that combines free
memory blocks into single larger blocks.


---

### heap\_3.c

This implements a simple wrapper for the standard C library malloc() and free()
functions that will, in most cases, be supplied with your chosen compiler. The
wrapper simply makes the malloc() and free() functions thread safe.

This implementation:

* Requires the linker to setup a heap, and the compiler library to provide
  malloc() and free() implementations.
* Is not deterministic.
* Will probably considerably increase the RTOS kernel code size.

Note that the configTOTAL\_HEAP\_SIZE setting in FreeRTOSConfig.h has no effect
when heap\_3 is used.

---

### heap\_4.c

This scheme uses a first fit algorithm and, unlike scheme 2, it does combine adjacent
free memory blocks into a single large block (it does include a coalescence algorithm).

The total amount of available heap space is set by
configTOTAL\_HEAP\_SIZE - which is defined in FreeRTOSConfig.h.
The [configAPPLICATION\_ALLOCATED\_HEAP](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization)
FreeRTOSConfig.h configuration constant is provided to allow the heap to be placed
at a specific address in memory.

The xPortGetFreeHeapSize() API function returns the total amount of heap space
that remains unallocated when the function is called, and the xPortGetMinimumEverFreeHeapSize()
API function returns lowest amount of free heap space that has existed system the
FreeRTOS application booted. Neither function provides information on how the unallocated
memory is fragmented into smaller blocks.

The vPortGetHeapStats() API function provides additional information. It populates the members of
a heap\_t structure, as shown below.

```c
/* Prototype of the vPortGetHeapStats() function. */  
void vPortGetHeapStats( HeapStats_t *xHeapStats );  

/* Definition of the Heap\_stats\_t structure. */  
typedef struct xHeapStats  
{  
	size_t xAvailableHeapSpaceInBytes;      /* The total heap size currently available - this is the sum of all the free blocks, not the largest block that can be allocated. */  
	size_t xSizeOfLargestFreeBlockInBytes; 	/* The maximum size, in bytes, of all the free blocks within the heap at the time vPortGetHeapStats() is called. */  
	size_t xSizeOfSmallestFreeBlockInBytes; /* The minimum size, in bytes, of all the free blocks within the heap at the time vPortGetHeapStats() is called. */  
	size_t xNumberOfFreeBlocks;		/* The number of free memory blocks within the heap at the time vPortGetHeapStats() is called. */  
	size_t xMinimumEverFreeBytesRemaining;	/* The minimum amount of total free memory (sum of all free blocks) there has been in the heap since the system booted. */  
	size_t xNumberOfSuccessfulAllocations;	/* The number of calls to pvPortMalloc() that have returned a valid memory block. */  
	size_t xNumberOfSuccessfulFrees;	/* The number of calls to vPortFree() that has successfully freed a block of memory. */  
} HeapStats_t;  
```

The pvPortCalloc() function has the same signature as the standard library calloc function. It allocates 
memory for an array of objects and initializes all bytes in the allocated storage to zero. If allocation succeeds, 
it returns a pointer to the lowest byte in the allocated memory block. On failure, it returns a null pointer.

heap\_4:

* Can be used even when the application repeatedly deletes tasks, queues, semaphores, mutexes, etc..

* Is much less likely than the heap\_2 implementation to result in a heap
  space that is badly fragmented into multiple small blocks - even when
  the memory being allocated and freed is of random size.

* Is not deterministic - but is much more efficient that most standard C library malloc implementations.

heap\_4.c is particularly useful for applications that want to use the portable
layer memory allocation schemes directly in the application code (rather than
just indirectly by calling API functions that themselves call
pvPortMalloc() and vPortFree()).

---

### heap\_5.c

This scheme uses the same first fit and memory coalescence algorithms as
heap\_4, and allows the heap to span multiple non adjacent (non-contiguous)
memory regions.

Heap\_5 is initialised by calling vPortDefineHeapRegions(), and **cannot be used**
until after vPortDefineHeapRegions() has executed. Creating
an RTOS object (task, queue, semaphore, etc.) will implicitly call pvPortMalloc()
so it is essential that, when using heap\_5, vPortDefineHeapRegions() is called
before the creation of any such object.

vPortDefineHeapRegions() takes a single parameter. The parameter is an array
of HeapRegion\_t structures. HeapRegion\_t is defined in portable.h as

```c
typedef struct HeapRegion  
{  
    /* Start address of a block of memory that will be part of the heap.*/  
    uint8_t *pucStartAddress;  

    /* Size of the block of memory. */  
    size_t xSizeInBytes;  
} HeapRegion_t;  
```
*The HeapRegion_t type definition*

The array is terminated using a NULL zero sized region definition, and the
memory regions defined in the array **must** appear in address order, from
low address to high address. The following source code snippets provide an
example. The [MSVC Win32 simulator demo](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)
also uses heap\_5 so can be used as a reference.


```c
/* Allocate two blocks of RAM for use by the heap. The first is a block of  
   0x10000 bytes starting from address 0x80000000, and the second a block of  
   0xa0000 bytes starting from address 0x90000000. The block starting at  
   0x80000000 has the lower start address so appears in the array fist. */  
const HeapRegion_t xHeapRegions[] =  
{  
    { ( uint8_t * ) 0x80000000UL, 0x10000 },  
    { ( uint8_t * ) 0x90000000UL, 0xa0000 },  
    { NULL, 0 } /* Terminates the array. */  
};  

/* Pass the array into vPortDefineHeapRegions(). */  
vPortDefineHeapRegions( xHeapRegions );  
```
*Initialising heap\_5 after defining the memory blocks to be used by the heap*

The xPortGetFreeHeapSize() API function returns the total amount of heap space
that remains unallocated when the function is called, and the xPortGetMinimumEverFreeHeapSize()
API function returns lowest amount of free heap space that has existed system the
FreeRTOS application booted. Neither function provides information on how the unallocated
memory is fragmented into smaller blocks.

The pvPortCalloc() function has the same signature as the standard library calloc function. It allocates 
memory for an array of objects and initializes all bytes in the allocated storage to zero. If allocation succeeds, 
it returns a pointer to the lowest byte in the allocated memory block. On failure, it returns a null pointer.

The vPortGetHeapStats() API function provides additional information on the heap status.
