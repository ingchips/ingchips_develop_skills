# xEventGroupGetStaticBuffer()

[[Event Group API](https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)]

event\_groups.h

```c
 BaseType_t xEventGroupGetStaticBuffer( EventGroupHandle_t xEventGroup,
                                        StaticEventGroup_t ** ppxEventGroupBuffer );
```

configSUPPORT\_STATIC\_ALLOCATION must be defined as 1 for this function to be available. See 
the [RTOS Configuration](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization) documentation 
for more information.

Retrieve a pointer to a statically created event group's data structure buffer. It is the same buffer 
that is supplied at the time of creation.

**Parameters:**

+ `xEventGroup`     

  The event group for which the buffer will be retrieved.

+ `ppxEventGroupBuffer`     

  Used to return a pointer to the event group's data structure buffer.


**Returns:**

+ pdTRUE if the buffer was retrieved 
+ pdFALSE otherwise. 


