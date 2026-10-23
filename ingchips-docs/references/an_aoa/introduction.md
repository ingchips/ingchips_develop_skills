<!-- an_aoa: 2 Introduction -->

# 2 Introduction {#introduction}

Bluetooth 5.1 introduced support for Direction Finding by adding the option to send and receive Constant Tone Extensions (CTEs) after Bluetooth packets in both advertising and connection modes. This makes it possible to do phase measurements on antenna arrays and ultimately to determine the direction of an incoming signal.

This application note is organized as following:

- [Direction Finding Fundamentals](https://ingchips.github.io/application-notes/an_aoa/fundamentals.html#fundamentals) talks about the basic theory of Direction Finding, that is how to determine the direction of incoming signals;
- [Quick-Start Guide](https://ingchips.github.io/application-notes/an_aoa/quick-start.html#quick-start) gives a step-by-step introduction on an AoA demo;
- [SDK Support of Direction Finding](https://ingchips.github.io/application-notes/an_aoa/sdk-support.html#sdk-support) provides detailed information on SDK design & relevant APIs, including connection & connectionless mode, and two proprietary modes.
- There are also [Further Information](https://ingchips.github.io/application-notes/an_aoa/futher-info.html#futher-info) on how to integrate reference AoA algorithm implementation into other systems.

## 2.1 Abbreviations & Terminology {#abbreviations-terminology}

*Table 2.1: Abbreviations*
| Abbreviation | Notes |
| --- | --- |
| AoA | Angle of Arrival |
| AoD | Angle of Departure |
| BLE | Bluetooth Low Energy |
| CTE | Constant Tone Extension |
| SDK | Software Development Kit |

## 2.2 References {#references}

1. Bluetooth SIG[1](#fn1)

---

1. <a id="fn1"></a>[https://www.bluetooth.com/](https://www.bluetooth.com/)[↩︎](https://ingchips.github.io/application-notes/an_aoa/introduction.html#fnref1)