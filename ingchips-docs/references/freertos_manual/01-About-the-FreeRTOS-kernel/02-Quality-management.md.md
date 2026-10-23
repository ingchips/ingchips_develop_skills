# Implementation Quality Management

**Value Proposition**
* High quality C source code under strict configuration management 
* Safety critical version ensures dependability 
* Cross platform support secures time investment 
* Tutorial books and training to educate engineers 
* Pre-configured example projects for all supported ports 
* Free support, quoted as better than some commercial alternatives 
* Large and growing user base and community 
* *Peace of mind* - low cost commercial options can be taken at any time 
* **= A low total cost of ownership, risk free, & compelling solution** 

<table>
  <thead>
    <tr>
      <th colSpan={2}>RTOS Technology Highlights</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Pre-emptive scheduling option</td>
      <td>Easy to use message passing</td>
    </tr>
    <tr>
      <td>Co-operative scheduling option</td>
      <td>Round robin with time slicing</td>
    </tr>
    <tr>
      <td>Fast task notifications</td>
      <td>Mutexes with priority inheritance</td>
    </tr>
    <tr>
      <td>6K to 12K ROM footprint</td>
      <td>Recursive mutexes</td>
    </tr>
    <tr>
      <td>Configurable / scalable</td>
      <td>Binary and counting semaphores</td>
    </tr>
    <tr>
      <td>Chip and compiler agnostic</td>
      <td>Very efficient software timers</td>
    </tr>
    <tr>
      <td>Some ports never completely disable interrupts</td>
      <td>Easy to use API</td>
    </tr>
  </tbody>
</table>

FreeRTOS is very strictly quality managed, not just 
in [software coding standards and look and feel](https://www.freertos.org/Documentation/02-Kernel/06-Coding-guidelines/02-FreeRTOS-Coding-Standard-and-Style-Guide), 
but also in implementation. For example:

* FreeRTOS **never** performs a non-deterministic operation, such as walking a linked list, from inside a 
  critical section or interrupt.
* We are particularly proud of the efficient [software timer](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) implementation
  that **does not use any CPU time unless a timer actually needs servicing**. Software timers do not
  contain variables that need to be counted down to zero.
* Likewise, lists of Blocked (pended) tasks do not require time consuming periodic servicing.
* [Direct to task notifications](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) allow fast task signalling, with practically no RAM overhead,
  and can be used in the majority of inter-task and interrupt to task signalling scenarios.
* The [FreeRTOS queue usage model](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues) manages to combine simplicity with flexibility (in
  a tiny code size) - attributes that are normally mutually exclusive.
* FreeRTOS queues are base primitives on top of which other communication and synchronisation primitives are built.
  The code re-use obtained dramatically reduced overall code size, which in turn **assists testing and helps ensure robustness**.

In addition, the [TÜV SÜD](http://www.tuev-sued.com/) certified SIL 
3 [SAFERTOS real time kernel](https://www.freertos.org/Partners/Software/SafeRTOS) was originally derived from 
FreeRTOS, and has undergone the most stringent analysis and test process - the results of which were fed back 
into the FreeRTOS code base (when commonality still existed).
 
