# FreeRTOS software timers

[[More about software timers...](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

### One-shot timers versus auto-reload timers

There are two types of timer, one-shot timers, and auto-reload timers. Once
started, a one-shot timer will execute its callback function only once. It can
be manually re-started, but will not automatically re-start itself. Conversely,
once started, an auto-reload timer will automatically re-start itself after each
execution of its callback function, resulting in periodic callback execution.

The difference in behaviour between a one-shot timer and an auto-reload timer is
demonstrated by the timeline in the diagram below. In this diagram, Timer 1 is
a one-shot timer that has a period equal to 100, and Timer 2 is an auto-reload
timer that has a period equal to 200.

![The behaviour of one-shot timers and auto-reload timers](https://www.freertos.org/media/2018/one-shot-timer-behaviour-vs-auto-reload-timer-behaviour.png)

The behaviour of one-shot timers and auto-reload timers
