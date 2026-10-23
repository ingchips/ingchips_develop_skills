# Run Time Statistics

*Click to enlarge*
[![](https://www.freertos.org/media/2018/rtos-run-time-stats.jpg)](/media/2018/rtos-run-time-stats.jpg)


### Description

FreeRTOS can optionally collect information on the amount of processing time that has been used by each task.
The [vTaskGetRunTimeStats()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function can then be used to present this
information in a tabular format, as shown on the right.

Two values are given for each task:

1. Abs Time (absolute time)

    This is the total 'time' that the task has actually been executing (the total time that the task has
    been in the Running state). It is up to the user to select a suitable time base for their application.

2. % Time (percentage time)

    This shows essentially the same information but as a percentage of the total processing time rather
    than as an absolute time.


### Configuration and Usage

Three macros are required. These can be defined in FreeRTOSConfig.h.

1. configGENERATE\_RUN\_TIME\_STATS

    Collection of run time statistics is enabled by #defining configGENERATE\_RUN\_TIME\_STATS as 1.
    Once this has been set the other two macros must also be defined to achieve a successful
    compilation.

2. portCONFIGURE\_TIMER\_FOR\_RUN\_TIME\_STATS()

    The run time statistics time base needs to have a higher resolution than the tick interrupt -
    otherwise the statistics may be too inaccurate to be truly useful. It is recommended to make
    the time base between 10 and 100 times faster than the tick interrupt. The faster the time
    base the more accurate the statistics will be - but also the sooner the timer value will overflow.

    If configGENERATE\_RUN\_TIME\_STATS is defined as 1 then the RTOS kernel will automatically call
    portCONFIGURE\_TIMER\_FOR\_RUN\_TIME\_STATS() as it is started (it is called from within the
    vTaskStartScheduler() API function). It is intended that the application designer uses the
    macro to configure a suitable time base. Some examples are provided below.
3. portGET\_RUN\_TIME\_COUNTER\_VALUE()

    This macro should just return the current 'time', as configured by portCONFIGURE\_TIMER\_FOR\_RUN\_TIME\_STATS().
    Again some examples are provided below.

The [vTaskGetRunTimeStats()](https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities) API function is used to retrieve the gathered statistics.
